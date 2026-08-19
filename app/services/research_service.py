import os
import json
import logging
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

from app.tools.search import search_web
from app.schemas.research import ResearchReportSchema, ResearchResponse

load_dotenv()
logger = logging.getLogger("research_pilot")


def get_fallback_llm():
    # Primary Groq model
    primary_llm = ChatGroq(
        model="qwen/qwen3.6-27b",
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.2,
        max_retries=2
    )

    # Fallback Gemini model
    fallback_llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.2,
        max_retries=1
    )

    return primary_llm.with_fallbacks([fallback_llm])


async def generate_basic_research(topic: str, depth: str = "medium") -> ResearchResponse:
    try:
        # Phase 1: ReAct Agent execution
        llm = get_fallback_llm()
        agent_executor = create_react_agent(
            model=llm,
            tools=[search_web],
            prompt=(
                "You are an efficient research assistant. "
                "CRITICAL RULE: Execute a maximum of 1 or 2 search queries using the search tool. "
                "As soon as you receive search results, analyze them and summarize your complete findings."
            )
        )

        input_message = f"Conduct a research summary on: {topic}. Depth: {depth}."
        agent_response = await agent_executor.ainvoke(
            {"messages": [HumanMessage(content=input_message)]},
            config={"recursion_limit": 25}
        )

        raw_context = agent_response["messages"][-1].content
        if isinstance(raw_context, list):
            raw_context = "\n".join([str(block) for block in raw_context])

        # Phase 2: Extract raw JSON output without direct schema binding
        formatter_llm = ChatGroq(
            model="qwen/qwen3.6-27b",
            groq_api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.1,
            max_tokens=4000,
            model_kwargs={"response_format": {"type": "json_object"}}
        )

        synthesis_prompt = f"""Format the research into a plain JSON object.

Output ONLY a raw JSON object with these EXACT keys:
- "title": string
- "executive_summary": string
- "key_findings": array of objects, each with "title" and "description"
- "summary_outlook": string

Topic: {topic}
Research Context:
{raw_context}
"""

        llm_response = await formatter_llm.ainvoke(synthesis_prompt)
        content = llm_response.content.strip()

        # Clean Markdown code block wrappers if present (e.g., ```json ... ```)
        if content.startswith("```"):
            lines = content.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            content = "\n".join(lines).strip()

        data = json.loads(content)

        # Phase 3: Defensive unwrapping of nested response wrappers
        # Recursively extract inner 'result' key if the LLM wrapped the object
        while isinstance(data, dict) and "result" in data:
            data = data["result"]

        # Ensure required 'summary_outlook' key exists to prevent Pydantic validation errors
        if isinstance(data, dict) and ("summary_outlook" not in data or not data["summary_outlook"]):
            data["summary_outlook"] = "Rapid evolution expected in this sector. Continuous monitoring recommended."

        # Parse cleaned dictionary into ResearchReportSchema
        structured_report = ResearchReportSchema.model_validate(data)

        # Phase 4: Construct and return final API response payload
        return ResearchResponse(
            message="Research completed successfully",
            topic=topic,
            status="completed",
            result=structured_report
        )

    except Exception as e:
        logger.error(f"Error during research execution: {str(e)}", exc_info=True)
        raise e