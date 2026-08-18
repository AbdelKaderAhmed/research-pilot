import os
import logging
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

# Setup basic logging to see errors in terminal
logger = logging.getLogger("research_pilot")
logging.basicConfig(level=logging.INFO)

async def generate_basic_research(topic: str, depth: str = "medium") -> str:
    try:
        # Initialize Gemini LLM with LangChain
        llm = ChatGoogleGenerativeAI(
            model="gemini-3.6-flash",
            temperature=0.3,
            google_api_key=os.getenv("GEMINI_API_KEY")
        )

        # Prepare messages
        system_prompt = SystemMessage(
            content="You are an expert research assistant. Provide a structured, accurate, and concise research summary on the requested topic."
        )
        user_prompt = HumanMessage(
            content=f"Conduct a research summary on: {topic}. Requested research depth: {depth}."
        )

        # Asynchronously invoke the model
        response = await llm.ainvoke([system_prompt, user_prompt])
        
        return str(response.content)

    except Exception as e:
        logger.error(f"Error during research generation: {str(e)}", exc_info=True)
        raise e