import os
from typing import Literal

# from langchain_core.message import BaseMessage, HumanMessage
from langchain.tools import Tool
from langgraph.graph import MessagesState, END
from langgraph.types import Command
from langgraph.graph import StateGraph, START

from agent.agent_difined import AgentDifined
from get_file import get_md_file_content

class AgentCreate():
    def __init__(self, user_prompt: str):
        # bucket_name = os.getenv("BUCKET_NAME")
        manager_file_path = "manager_agent_prompt.md"
        research_file_path = "researcher_agent_prompt.md"
        create_file_path = "creater_agent_prompt.md"
        # GCS から Markdown ファイルを取得
        manager_prompt = get_md_file_content(bucket_name, manager_file_path)
        research_prompt = get_md_file_content(bucket_name, research_file_path)
        create_prompt = get_md_file_content(bucket_name, create_file_path)
        # エージェントの作成
        manager_agent = AgentDifined()._create_agent(
            system_prompt=manager_prompt,
            # tools=[self.to_tools()]
        )
        research_agent = AgentDifined()._create_agent(
            system_prompt=research_prompt
        )
        create_agent = AgentDifined()._create_agent(
            system_prompt=create_prompt
        )
        self.user_prompt = user_prompt
        self.manager_agent = manager_agent
        self.research_agent = research_agent
        self.create_agent = create_agent
    
    def manage_node(self, state: MessagesState,):
        result = self.manager_agent.invoke(state)
        return Command(
            updata={
                "messages": result["messages"],
            },
            goto=END,
        )
    
    def research_node(self, state: MessagesState):
        result = self.research_agent.invoke(state)
        return Command(
            updata={
                "messages": result["messages"],
            },
        )
    
    def create_node(self, state: MessagesState):
        result = self.create_agent.invoke(state)
        return Command(
            updata={
                "messages": result["messages"],
            },
        )
    
    def to_tools(self):
        """
        agentをツールに変換する
        Returns:
            list: ツールのリスト
        """
        tools = [
            Tool(
                name="ResearchAgent",  # ツールの名前（識別用）
                func=self.research_node,  # 実行する関数（調査を行う）
                description="調査・検索を行うエージェント"  # ツールの説明（LLMが選択するときに参考にする）
            ),
            Tool(
                name="CreateAgent",  # ツールの名前（識別用）
                func=self.create_node,  # 実行する関数（エージェントを作成する）
                description="レポートを作成するエージェント"  # ツールの説明（LLMが選択するときに参考にする）
            ),
        ]
        return tools
    
    def workflow(self):
        """
        ワークフローを定義する
        """
        final_result = []
        workflow = StateGraph(MessagesState)
        workflow.add_node("manager_agent", self.manage_node, start=True)
        workflow.add_node("resercher_agent", self.research_node)
        workflow.add_node("create_agent", self.create_node)

        workflow.add_edge(START, "manager_agent")
        workflow.add_edge("manager_agent", "resercher_agent")
        workflow.add_edge("manager_agent", "create_agent")
        graph = workflow.compile()

        event = graph.stream(
            {
                "messages": [
                    (
                        "user",
                        f"{self.user_prompt}"
                    )
                ],
            },
            {"recursion_limit": 15},
        )
        for s in event:
            print(s)
            final_result.append(s)

        final_result_dict = final_result[-1]
        final_result_final_answer = final_result_dict[next(iter(final_result_dict))][-1].content

        return final_result_final_answer
