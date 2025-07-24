# xnewsbot/agents.py

from smolagents import CodeAgent, PythonInterpreterTool, OpenAIServerModel
from smolagents import DuckDuckGoSearchTool, VisitWebpageTool
from smolagents import tool
from smolagents.models import ChatMessage
from .tools import (
    instantiate_bot,
    available_images,
    download_image,
    fetch_news_from_homepage,
    search_bbc,
    memory_manager,
)
from .model import get_model
import os


def create_agents(gemini_api_key: str):

    model = get_model(gemini_api_key)
    @tool
    def summarizer(text: str,  special_instructions:str="") -> str:
        """
        Summarizes the given text using a language model.
        Args:
            text (str): The text to summarize.
            special_instructions (str): Additional instructions for the summarization model, if any.
        Returns:
            str: The summarized text.
        """

        prompt = """
            You are a professional news summarizer.

            Your task is to read full news articles and summarize them clearly, accurately, and objectively. Focus only on **factual** information. Do not include personal opinions, assumptions, or unnecessary background.

            When summarizing:
            - Use **3 to 5 concise bullet points**
            - Include **only the main events, facts, or decisions**
            - Keep language **neutral and journalistic**
            - Avoid repetition or vague language
            - Do not copy the full text — always condense
            - If teh publishing date is mentioned in the article, then ALWAYS include it in the summary.

            The summary will be used by a journalist AI for social media and news briefs, so keep it clean and readable.
            

        """

        if special_instructions:
            prompt += f"\n\nSpecial Instructions: {special_instructions}\n\n"

        response = model.generate(
            messages=[
                ChatMessage(role="system", content=prompt),
                ChatMessage(role="user", content=text)
            ],
        )
        return response.content.strip()
    """Returns main_agent, x_agent, research_agent, writer_agent"""
    # Load prompts
    base_path = os.path.join(os.path.dirname(__file__), "prompts")
    prompt = open(os.path.join(base_path, "x_agent_prompt.txt")).read()
    research_agent_prompt = open(os.path.join(base_path, "research_agent_prompt.txt")).read()
    writer_prompt = open(os.path.join(base_path, "writer_prompt.txt")).read()
    main_prompt = open(os.path.join(base_path, "main_prompt.txt")).read()

    model = OpenAIServerModel(
        model_id="gemini-2.0-flash",
        api_base="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key=gemini_api_key
    )

    # === X Agent ===
    x_agent = CodeAgent(
        model=model,
        tools=[instantiate_bot, available_images, download_image],
        additional_authorized_imports=["selenium.*", "bs4.*"],
        max_steps=20,
        name="XHandlerAgent",
        description="Agent for interacting with X.com (posting, following, etc.)"
    )
    x_agent.prompt_templates["system_prompt"] += "Addiitional instructions:\n" + prompt

    # === Research Agent ===
    research_agent = CodeAgent(
        model=model,
        tools=[
            VisitWebpageTool(),
            DuckDuckGoSearchTool(),
            available_images,
            download_image,
            fetch_news_from_homepage,
            search_bbc,
            summarizer,
        ],
        additional_authorized_imports=["bs4.*", "requests.*", "datetime.*"],
        max_steps=10,
        name="ResearchAgent",
        description="Discovers and verifies news stories from credible sources.",
    )
    research_agent.prompt_templates["system_prompt"] += "Secondary instructions:\n" + research_agent_prompt

    # === Writer Agent ===
    writer_agent = CodeAgent(
        model=model,
        tools=[VisitWebpageTool(), available_images, download_image],
        additional_authorized_imports=["bs4.*", "requests.*"],
        name="WriterAgent",
        description="Writes X.com posts based on summaries provided by ResearchAgent."
    )
    writer_agent.prompt_templates["system_prompt"] += "Additional instructions:\n" + writer_prompt

    # === Main Agent ===
    main_agent = CodeAgent(
        model=model,
        tools=[memory_manager, available_images, download_image, summarizer, PythonInterpreterTool()],
        additional_authorized_imports=["datetime.*"],
        name="MainAgent",
        description="Manages the X.com news account.",
        planning_interval=30,
        managed_agents=[x_agent, research_agent, writer_agent]
    )
    main_agent.prompt_templates["system_prompt"] += "Additional instructions:\n" + main_prompt

    return main_agent, x_agent, research_agent, writer_agent
