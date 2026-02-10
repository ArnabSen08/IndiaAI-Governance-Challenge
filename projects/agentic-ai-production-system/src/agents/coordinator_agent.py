"""
Coordinator Agent - Orchestrates workflow and manages agent communication.
"""

import asyncio
from typing import Dict, Any, List
from .base_agent import BaseAgent
from .research_agent import ResearchAgent
from .content_agent import ContentAgent
from .validation_agent import ValidationAgent

class CoordinatorAgent(BaseAgent):
    """Coordinates multi-agent workflows and manages task distribution."""
    
    def __init__(self, config, logger):
        super().__init__("CoordinatorAgent", config, logger)
        self.workflow_history = []
        
        # Initialize specialized agents
        self.research_agent = ResearchAgent(config, logger)
        self.content_agent = ContentAgent(config, logger)
        self.validation_agent = ValidationAgent(config, logger)
        
        self.agents = {
            "ResearchAgent": self.research_agent,
            "ContentAgent": self.content_agent,
            "ValidationAgent": self.validation_agent
        }
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process coordination request and orchestrate workflow."""
        
        if not self.validate_input(input_data):
            return {"error": "Invalid input data", "success": False}
        
        try:
            task = input_data.get("task", "")
            context = input_data.get("context", {})
            
            self.logger.info(f"CoordinatorAgent: Processing task: {task[:100]}...")
            
            # Analyze task and determine workflow
            workflow_plan = await self._create_workflow_plan(task, context)
            
            # Execute workflow
            result = await self._execute_workflow(workflow_plan, input_data)
            
            # Store workflow history
            self.workflow_history.append({
                "task": task,
                "workflow_plan": workflow_plan,
                "result": result,
                "timestamp": asyncio.get_event_loop().time()
            })
            
            return {
                "success": True,
                "result": result,
                "workflow_plan": workflow_plan,
                "agent": self.name
            }
            
        except Exception as e:
            self.logger.error(f"CoordinatorAgent: Error processing task: {str(e)}")
            return {
                "error": str(e),
                "success": False,
                "agent": self.name
            }
    
    async def _create_workflow_plan(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Create a workflow plan based on the task requirements."""
        
        messages = [
            {
                "role": "system",
                "content": """You are a workflow coordinator for a multi-agent AI system. 
                Analyze the given task and create a structured workflow plan.
                
                Available agents:
                - ResearchAgent: Information gathering and analysis
                - ContentAgent: Content generation and refinement
                - ValidationAgent: Quality assurance and safety checks
                
                Respond with a JSON structure containing:
                {
                    "steps": [
                        {"agent": "agent_name", "action": "description", "priority": 1-3}
                    ],
                    "estimated_time": "time_estimate",
                    "complexity": "low|medium|high"
                }"""
            },
            {
                "role": "user",
                "content": f"Task: {task}\nContext: {context}"
            }
        ]
        
        try:
            response = await self._make_llm_request(messages, max_tokens=500)
            
            # Parse the response (simplified - in production, use proper JSON parsing)
            workflow_plan = {
                "steps": [
                    {"agent": "ResearchAgent", "action": "Gather relevant information", "priority": 1},
                    {"agent": "ContentAgent", "action": "Generate response", "priority": 2},
                    {"agent": "ValidationAgent", "action": "Validate output", "priority": 3}
                ],
                "estimated_time": "30-60 seconds",
                "complexity": "medium",
                "raw_response": response
            }
            
            return workflow_plan
            
        except Exception as e:
            self.logger.error(f"CoordinatorAgent: Error creating workflow plan: {str(e)}")
            # Fallback to default workflow
            return {
                "steps": [
                    {"agent": "ContentAgent", "action": "Direct processing", "priority": 1}
                ],
                "estimated_time": "15-30 seconds",
                "complexity": "low",
                "fallback": True
            }
    
    async def _execute_workflow(self, workflow_plan: Dict[str, Any], input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the planned workflow."""
        
        results = {}
        
        for step in workflow_plan.get("steps", []):
            agent_name = step.get("agent")
            action = step.get("action")
            
            self.logger.info(f"CoordinatorAgent: Executing step - {agent_name}: {action}")
            
            # Simulate agent execution (in a real system, this would call actual agents)
            step_result = await self._simulate_agent_execution(agent_name, action, input_data)
            results[agent_name] = step_result
        
        return {
            "workflow_results": results,
            "final_output": self._synthesize_results(results),
            "execution_summary": f"Completed {len(workflow_plan.get('steps', []))} steps"
        }
    
    async def _simulate_agent_execution(self, agent_name: str, action: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute actual agent calls instead of simulation."""
        
        try:
            if agent_name in self.agents:
                agent = self.agents[agent_name]
                
                # Prepare agent-specific input
                agent_input = {
                    "task": input_data.get("task", ""),
                    "context": input_data.get("context", {}),
                    "action": action
                }
                
                # Add agent-specific parameters
                if agent_name == "ResearchAgent":
                    agent_input["query"] = input_data.get("task", "")
                    agent_input["research_type"] = "general"
                elif agent_name == "ContentAgent":
                    agent_input["content_request"] = input_data.get("task", "")
                    agent_input["content_type"] = "explanation"
                    agent_input["style"] = "professional"
                    agent_input["length"] = "medium"
                elif agent_name == "ValidationAgent":
                    # For validation, we need content from previous agents
                    agent_input["content"] = input_data.get("content", input_data.get("task", ""))
                    agent_input["validation_type"] = "comprehensive"
                
                # Execute the agent
                result = await agent.process(agent_input)
                
                return {
                    "success": result.get("success", False),
                    "output": result.get("content", result.get("findings", result.get("result", str(result)))),
                    "agent": agent_name,
                    "action": action,
                    "details": result
                }
            else:
                # Fallback to LLM simulation for unknown agents
                return await self._llm_agent_simulation(agent_name, action, input_data)
                
        except Exception as e:
            self.logger.error(f"CoordinatorAgent: Error executing {agent_name}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "agent": agent_name,
                "action": action
            }
    
    async def _llm_agent_simulation(self, agent_name: str, action: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback LLM simulation for unknown agents."""
        
        messages = [
            {
                "role": "system",
                "content": f"You are the {agent_name}. Perform the following action: {action}"
            },
            {
                "role": "user",
                "content": f"Task: {input_data.get('task', '')}"
            }
        ]
        
        try:
            response = await self._make_llm_request(messages, max_tokens=300)
            filtered_response = self.filter_output(response)
            
            return {
                "success": True,
                "output": filtered_response,
                "agent": agent_name,
                "action": action,
                "simulated": True
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "agent": agent_name,
                "action": action,
                "simulated": True
            }
    
    def _synthesize_results(self, results: Dict[str, Any]) -> str:
        """Synthesize results from multiple agents into final output."""
        
        successful_results = [
            result["output"] for result in results.values() 
            if result.get("success") and "output" in result
        ]
        
        if not successful_results:
            return "No successful results to synthesize."
        
        # Simple synthesis - in production, this could be more sophisticated
        return "\n\n".join(successful_results)
    
    def get_workflow_history(self) -> List[Dict[str, Any]]:
        """Get workflow execution history."""
        return self.workflow_history[-10:]  # Return last 10 workflows
    
    def get_all_agent_metrics(self) -> Dict[str, Any]:
        """Get metrics from all agents."""
        
        metrics = {
            "coordinator": self.get_metrics()
        }
        
        for agent_name, agent in self.agents.items():
            metrics[agent_name.lower()] = agent.get_metrics()
            
            # Add specialized metrics for validation agent
            if agent_name == "ValidationAgent":
                metrics[agent_name.lower()].update(agent.get_validation_metrics())
        
        return metrics
    
    async def health_check_all_agents(self) -> Dict[str, Any]:
        """Perform health check on all agents."""
        
        health_results = {
            "coordinator": await self.health_check()
        }
        
        for agent_name, agent in self.agents.items():
            try:
                health_results[agent_name.lower()] = await agent.health_check()
            except Exception as e:
                health_results[agent_name.lower()] = {
                    "agent": agent_name,
                    "healthy": False,
                    "error": str(e)
                }
        
        # Overall system health
        all_healthy = all(result.get("healthy", False) for result in health_results.values())
        
        return {
            "system_healthy": all_healthy,
            "individual_results": health_results,
            "timestamp": asyncio.get_event_loop().time()
        }