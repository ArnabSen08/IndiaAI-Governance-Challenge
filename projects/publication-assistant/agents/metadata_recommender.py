"""Metadata Recommender Agent - Suggests tags, categories, and keywords."""
import os
from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from tools.keyword_extractor import KeywordExtractorTool
from tools.web_search_tool import WebSearchTool


class MetadataRecommenderAgent:
    """Agent that recommends metadata like tags, categories, and keywords."""
    
    def __init__(self, model_name: str = None, temperature: float = 0.7):
        """Initialize the Metadata Recommender Agent."""
        self.llm = ChatOpenAI(
            model=model_name or os.getenv("MODEL_NAME", "gpt-4-turbo-preview"),
            temperature=temperature,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Initialize tools
        self.tools = [KeywordExtractorTool(), WebSearchTool()]
        
        # Create agent prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Metadata Recommender Agent. Your role is to:
1. Extract keywords and key phrases from project content
2. Suggest relevant tags and categories based on project type and technologies
3. Recommend appropriate keywords for discoverability
4. Research similar projects to identify common metadata patterns
5. Provide metadata recommendations that improve project discoverability

Use the keyword extractor to identify important terms and the web search tool to find similar projects and best practices."""),
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
    
    def recommend(self, project_content: str, repo_analysis: str = None) -> Dict[str, Any]:
        """Recommend metadata for a project."""
        query = f"""Based on the following project content, recommend metadata (tags, categories, keywords):
        
{project_content}"""
        
        if repo_analysis:
            query += f"\n\nRepository analysis context:\n{repo_analysis}"
        
        query += """
        
Please:
1. Extract key terms and phrases from the content
2. Suggest 10-15 relevant tags
3. Recommend 3-5 main categories
4. Identify important keywords for search optimization
5. Research similar projects to validate recommendations"""
        
        try:
            result = self.agent_executor.invoke({"input": query, "chat_history": []})
            return {
                "agent": "Metadata Recommender",
                "status": "success",
                "recommendations": result.get("output", "")
            }
        except Exception as e:
            return {
                "agent": "Metadata Recommender",
                "status": "error",
                "error": str(e)
            }
