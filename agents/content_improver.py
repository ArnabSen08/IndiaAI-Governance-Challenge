"""Content Improver Agent - Proposes better titles, summaries, and content."""
import os
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from tools.text_processor import TextProcessorTool
from tools.web_search_tool import WebSearchTool


class ContentImproverAgent:
    """Agent that improves project titles, summaries, and introductions."""
    
    def __init__(self, model_name: str = None, temperature: float = 0.7):
        """Initialize the Content Improver Agent."""
        self.llm = ChatOpenAI(
            model=model_name or os.getenv("MODEL_NAME", "gpt-4-turbo-preview"),
            temperature=temperature,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Initialize tools
        self.tools = [TextProcessorTool(), WebSearchTool()]
        
        # Create agent prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Content Improver Agent. Your role is to:
1. Analyze existing project titles, summaries, and introductions
2. Propose improved versions that are more engaging and clear
3. Suggest better project descriptions that highlight key features
4. Recommend structural improvements to documentation
5. Provide alternative titles and summaries with explanations

Use the text processor to analyze current content quality and the web search tool to find examples of well-written project descriptions."""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        # Create agent
        agent = create_openai_tools_agent(self.llm, self.tools, prompt)
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )
    
    def improve(self, current_content: str, repo_analysis: str = None) -> Dict[str, Any]:
        """Improve project content."""
        query = f"""Analyze and improve the following project content:
        
{current_content}"""
        
        if repo_analysis:
            query += f"\n\nRepository analysis context:\n{repo_analysis}"
        
        query += """
        
Please:
1. Analyze the current content quality and readability
2. Propose 3 alternative titles with explanations
3. Suggest an improved project summary/description
4. Recommend improvements to the introduction section
5. Provide specific suggestions for making the content more engaging"""
        
        try:
            result = self.agent_executor.invoke({"input": query, "chat_history": []})
            return {
                "agent": "Content Improver",
                "status": "success",
                "improvements": result.get("output", "")
            }
        except Exception as e:
            return {
                "agent": "Content Improver",
                "status": "error",
                "error": str(e)
            }
