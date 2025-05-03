import os
from typing import Annotated
from google.cloud import aiplatform
import vertexai
from vertexai.generative_models import GenerativeModel

from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from agent.modelwrapper import GeminiModelWrapper

# Google Cloud の初期化
aiplatform.init(
    # project=os.getenv("PROJECT_ID"),
    location="us-central1",
)
vertexai.init(
    # project=os.getenv("PROJECT_ID"),
    location="us-central1",
)

class AgentDifined():
    def __init__(self):
        # Gemini 1.5 Flash をロード
        llm = GeminiModelWrapper("gemini-1.5-flash")
        self.llm = llm

    def _create_agent(self, system_prompt: str, tools: list=[]):
        """
        create agent
        Args:
            system_prompt (str): System prompt for the agent.
            tools (list, optional): List of tools to be used by the agent. Defaults to [].
        """
        return create_react_agent(
            self.llm,
            tools=tools,
            prompt=system_prompt,
        )
