"""Repo Analyzer Agent - Parses and interprets repository content."""
import os
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from tools.github_tool import GitHubTool
from tools.text_processor import TextProcessorTool


class RepoAnalyzerAgent:
    """Agent that analyzes GitHub repositories and extracts key information."""
    
    def __init__(self, model_name: str = None, temperature: float = 0.7):
        """Initialize the Repo Analyzer Agent."""
        self.llm = ChatOpenAI(
            model=model_name or os.getenv("MODEL_NAME", "gpt-4-turbo-preview"),
            temperature=temperature,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Initialize tools
        self.tools = [GitHubTool(), TextProcessorTool()]
        
        # Create agent prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Repository Analyzer Agent. Your role is to:
1. Fetch and parse README files and repository structure from GitHub
2. Analyze the code organization and project structure
3. Extract key information about the project's purpose, features, and setup
4. Identify the main technologies, frameworks, and dependencies used
5. Assess the current state of documentation and code organization

Be thorough and provide detailed analysis. Use the GitHub tool to fetch repository information and the text processor to analyze documentation quality."""),
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
    
    def analyze(self, repo_url: str, project_description: str = None) -> Dict[str, Any]:
        """Analyze a GitHub repository."""
        query = f"""Analyze the GitHub repository at {repo_url}"""
        if project_description:
            query += f"\n\nProject description provided: {project_description}"
        query += """
        
Please:
1. Fetch the README file and repository structure
2. Analyze the project's purpose, features, and organization
3. Identify technologies and frameworks used
4. Assess documentation quality and completeness
5. Provide a comprehensive summary of your findings"""
        
        try:
            result = self.agent_executor.invoke({"input": query, "chat_history": []})
            return {
                "agent": "Repo Analyzer",
                "status": "success",
                "analysis": result.get("output", ""),
                "repo_url": repo_url
            }
        except Exception as e:
            return {
                "agent": "Repo Analyzer",
                "status": "error",
                "error": str(e),
                "repo_url": repo_url
            }
