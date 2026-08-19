import os
import logging
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from app.tools.search import search_web

load_dotenv()
logger = logging.getLogger("research_pilot")


def get_fallback_llm():
    primary_llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        max_retries=1
    )

    fallback_llm = ChatGroq(
        model="qwen/qwen3.6-27b",
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.3
    )

    return primary_llm.with_fallbacks([fallback_llm])


async def generate_basic_research(topic: str, depth: str = "medium") -> str:
    try:
        llm = get_fallback_llm()
        tools = [search_web]

        # Prompt حازم يجبر الوكيل على التوقف بعد البحث المبدئي
        system_prompt = (
            "You are an efficient research assistant. "
            "CRITICAL RULE: You MUST execute a maximum of 1 or 2 search queries using the search tool. "
            "As soon as you receive the search results, STOP searching immediately and write the final report. "
            "Do NOT perform repetitive searches for the same topic."
        )

        agent_executor = create_react_agent(
            model=llm,
            tools=tools,
            prompt=system_prompt
        )

        input_message = f"Conduct a research summary on: {topic}. Depth: {depth}."

        # رفع Limit لـ 25 لتجنب الانهيار
        response = await agent_executor.ainvoke(
            {"messages": [HumanMessage(content=input_message)]},
            config={"recursion_limit": 25}
        )

        final_message = response["messages"][-1].content

        if isinstance(final_message, list):
            final_message = "\n".join([str(block) for block in final_message])

        return str(final_message)

    except Exception as e:
        logger.error(f"Error during research execution: {str(e)}", exc_info=True)
        raise e