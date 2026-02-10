"""Multi-Agent Orchestrator using LangGraph for workflow management."""
import os
from typing import Dict, Any, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from agents.repo_analyzer import RepoAnalyzerAgent
from agents.metadata_recommender import MetadataRecommenderAgent
from agents.content_improver import ContentImproverAgent
from agents.reviewer import ReviewerAgent


class AgentState(TypedDict):
    """State shared between agents in the workflow."""
    repo_url: str
    project_description: str
    repo_analysis: str
    project_content: str
    metadata_recommendations: str
    content_improvements: str
    review_feedback: str
    final_report: str
    step: str
    errors: Annotated[list, lambda x, y: x + y]


class MultiAgentOrchestrator:
    """Orchestrates multiple agents using LangGraph for collaborative analysis."""
    
    def __init__(self, model_name: str = None, temperature: float = 0.7):
        """Initialize the orchestrator with all agents."""
        self.repo_analyzer = RepoAnalyzerAgent(model_name, temperature)
        self.metadata_recommender = MetadataRecommenderAgent(model_name, temperature)
        self.content_improver = ContentImproverAgent(model_name, temperature)
        self.reviewer = ReviewerAgent(model_name, temperature)
        
        # Build the workflow graph
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow."""
        workflow = StateGraph(AgentState)
        
        # Add nodes (agent steps)
        workflow.add_node("analyze_repo", self._analyze_repo_node)
        workflow.add_node("recommend_metadata", self._recommend_metadata_node)
        workflow.add_node("improve_content", self._improve_content_node)
        workflow.add_node("review", self._review_node)
        workflow.add_node("generate_report", self._generate_report_node)
        
        # Define the flow
        workflow.set_entry_point("analyze_repo")
        workflow.add_edge("analyze_repo", "recommend_metadata")
        workflow.add_edge("recommend_metadata", "improve_content")
        workflow.add_edge("improve_content", "review")
        workflow.add_edge("review", "generate_report")
        workflow.add_edge("generate_report", END)
        
        return workflow.compile()
    
    def _analyze_repo_node(self, state: AgentState) -> AgentState:
        """Node for repository analysis."""
        try:
            result = self.repo_analyzer.analyze(
                state["repo_url"],
                state.get("project_description", "")
            )
            
            if result["status"] == "success":
                state["repo_analysis"] = result["analysis"]
                state["project_content"] = result["analysis"]  # Use analysis as initial content
                state["step"] = "analyze_repo"
            else:
                state["errors"] = state.get("errors", []) + [f"Repo Analyzer: {result.get('error', 'Unknown error')}"]
                state["repo_analysis"] = "Analysis failed"
        except Exception as e:
            state["errors"] = state.get("errors", []) + [f"Repo Analyzer Exception: {str(e)}"]
        
        return state
    
    def _recommend_metadata_node(self, state: AgentState) -> AgentState:
        """Node for metadata recommendations."""
        try:
            result = self.metadata_recommender.recommend(
                state.get("project_content", ""),
                state.get("repo_analysis", "")
            )
            
            if result["status"] == "success":
                state["metadata_recommendations"] = result["recommendations"]
                state["step"] = "recommend_metadata"
            else:
                state["errors"] = state.get("errors", []) + [f"Metadata Recommender: {result.get('error', 'Unknown error')}"]
                state["metadata_recommendations"] = "Recommendations failed"
        except Exception as e:
            state["errors"] = state.get("errors", []) + [f"Metadata Recommender Exception: {str(e)}"]
        
        return state
    
    def _improve_content_node(self, state: AgentState) -> AgentState:
        """Node for content improvement."""
        try:
            result = self.content_improver.improve(
                state.get("project_content", ""),
                state.get("repo_analysis", "")
            )
            
            if result["status"] == "success":
                state["content_improvements"] = result["improvements"]
                state["step"] = "improve_content"
            else:
                state["errors"] = state.get("errors", []) + [f"Content Improver: {result.get('error', 'Unknown error')}"]
                state["content_improvements"] = "Improvements failed"
        except Exception as e:
            state["errors"] = state.get("errors", []) + [f"Content Improver Exception: {str(e)}"]
        
        return state
    
    def _review_node(self, state: AgentState) -> AgentState:
        """Node for review and validation."""
        try:
            # Combine all suggestions for review
            suggestions = f"""
Metadata Recommendations:
{state.get('metadata_recommendations', 'N/A')}

Content Improvements:
{state.get('content_improvements', 'N/A')}
"""
            
            result = self.reviewer.review(
                state.get("project_content", ""),
                state.get("repo_url", ""),
                suggestions
            )
            
            if result["status"] == "success":
                state["review_feedback"] = result["review"]
                state["step"] = "review"
            else:
                state["errors"] = state.get("errors", []) + [f"Reviewer: {result.get('error', 'Unknown error')}"]
                state["review_feedback"] = "Review failed"
        except Exception as e:
            state["errors"] = state.get("errors", []) + [f"Reviewer Exception: {str(e)}"]
        
        return state
    
    def _generate_report_node(self, state: AgentState) -> AgentState:
        """Node for generating final report."""
        try:
            report = f"""
# Publication Assistant Report

## Repository Analysis
{state.get('repo_analysis', 'N/A')}

## Metadata Recommendations
{state.get('metadata_recommendations', 'N/A')}

## Content Improvements
{state.get('content_improvements', 'N/A')}

## Review Feedback
{state.get('review_feedback', 'N/A')}

## Summary
This report was generated by a multi-agent system consisting of:
- Repo Analyzer Agent: Analyzed the repository structure and content
- Metadata Recommender Agent: Suggested tags, categories, and keywords
- Content Improver Agent: Proposed improvements to titles and descriptions
- Reviewer Agent: Reviewed the project for completeness and clarity

"""
            
            if state.get("errors"):
                report += f"\n## Errors Encountered\n" + "\n".join(f"- {e}" for e in state["errors"])
            
            state["final_report"] = report
            state["step"] = "complete"
        except Exception as e:
            state["errors"] = state.get("errors", []) + [f"Report Generation Exception: {str(e)}"]
            state["final_report"] = f"Error generating report: {str(e)}"
        
        return state
    
    def analyze_repository(self, repo_url: str, project_description: str = None) -> Dict[str, Any]:
        """Main entry point to analyze a repository."""
        initial_state: AgentState = {
            "repo_url": repo_url,
            "project_description": project_description or "",
            "repo_analysis": "",
            "project_content": "",
            "metadata_recommendations": "",
            "content_improvements": "",
            "review_feedback": "",
            "final_report": "",
            "step": "initialized",
            "errors": []
        }
        
        try:
            # Execute the workflow
            final_state = self.workflow.invoke(initial_state)
            
            return {
                "status": "success",
                "report": final_state.get("final_report", ""),
                "repo_analysis": final_state.get("repo_analysis", ""),
                "metadata_recommendations": final_state.get("metadata_recommendations", ""),
                "content_improvements": final_state.get("content_improvements", ""),
                "review_feedback": final_state.get("review_feedback", ""),
                "errors": final_state.get("errors", [])
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "errors": initial_state.get("errors", [])
            }
