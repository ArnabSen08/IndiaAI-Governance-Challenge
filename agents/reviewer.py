"""Reviewer Agent - Checks for missing sections and unclear areas."""
import os
from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from tools.text_processor import TextProcessorTool
from tools.github_tool import GitHubTool


class ReviewerAgent:
    """Agent that reviews projects for missing sections and unclear areas."""
    
    def __init__(self, model_name: str = None, temperature: float = 0.7):
        """Initialize the Reviewer Agent."""
        self.llm = ChatOpenAI(
            model=model_name or os.getenv("MODEL_NAME", "gpt-4-turbo-preview"),
            temperature=temperature,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Initialize tools
        self.tools = [TextProcessorTool(), GitHubTool()]
        
        # Create agent prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Reviewer Agent. Your role is to:
1. Check for missing sections in project documentation (README, etc.)
2. Identify unclear or confusing areas
3. Verify that suggestions are grounded in actual repository content
4. Assess overall documentation completeness
5. Provide constructive feedback on structure and clarity

Use the text processor to analyze documentation structure and the GitHub tool to verify claims against actual repository content."""),
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
    
    def review(self, content: str, repo_url: str = None, suggestions: str = None) -> Dict[str, Any]:
        """Review project content and suggestions."""
        query = f"""Review the following project content:
        
{content}"""
        
        if suggestions:
            query += f"\n\nPrevious suggestions made:\n{suggestions}"
        
        if repo_url:
            query += f"\n\nRepository URL: {repo_url}"
        
        query += """
        
Please:
1. Check for missing essential sections (installation, usage, examples, etc.)
2. Identify unclear or confusing parts
3. Verify any claims against the actual repository (if URL provided)
4. Assess documentation completeness and structure
5. Provide specific, actionable feedback"""
        
        try:
            result = self.agent_executor.invoke({"input": query, "chat_history": []})
            return {
                "agent": "Reviewer",
                "status": "success",
                "review": result.get("output", "")
            }
        except Exception as e:
            return {
                "agent": "Reviewer",
                "status": "error",
                "error": str(e)
            }
