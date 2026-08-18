import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

async def generate_basic_research(topic: str, depth: str = "medium") -> str:
    # 1. Initialize the Gemini LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3,
        google_api_key=os.getenv("GEMINI_API_KEY")
    )

    # 2. Prepare system and user prompts
    system_prompt = SystemMessage(
        content="You are an expert research assistant. Provide a structured, accurate, and concise research summary on the requested topic."
    )
    user_prompt = HumanMessage(
        content=f"Conduct a research summary on: {topic}. Requested research depth: {depth}."
    )

    # 3. Invoke the model asynchronously
    response = await llm.ainvoke([system_prompt, user_prompt])
    
    return response.content