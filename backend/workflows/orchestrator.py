"""
Agent Orchestrator - Manages multi-agent workflow execution
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
from backend.agents.coordinator_agent import CoordinatorAgent
from backend.agents.research_agent import ResearchAgent
from backend.agents.retrieval_agent import RetrievalAgent
from backend.agents.summarization_agent import SummarizationAgent
from backend.agents.citation_agent import CitationAgent
from backend.agents.planning_agent import PlanningAgent
from backend.agents.memory_agent import MemoryAgent
from backend.agents.web_search_agent import WebSearchAgent
from backend.agents.file_analysis_agent import FileAnalysisAgent
from backend.agents.report_generation_agent import ReportGenerationAgent

logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """Orchestrates multi-agent workflow execution"""
    
    def __init__(self):
        self.agents = {
            "coordinator": CoordinatorAgent(),
            "research": ResearchAgent(),
            "retrieval": RetrievalAgent(),
            "summarization": SummarizationAgent(),
            "citation": CitationAgent(),
            "planning": PlanningAgent(),
            "memory": MemoryAgent(),
            "web_search": WebSearchAgent(),
            "file_analysis": FileAnalysisAgent(),
            "report_generation": ReportGenerationAgent()
        }
        
        self.execution_history = []
        self.active_workflows = {}
    
    async def execute_workflow(
        self, 
        workflow_name: str, 
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a complete workflow
        
        Args:
            workflow_name: Name of workflow to execute
            input_data: Input data for workflow
        
        Returns:
            Workflow execution result
        """
        try:
            logger.info(f"Executing workflow: {workflow_name}")
            
            start_time = datetime.utcnow()
            
            # Route to appropriate workflow
            if workflow_name == "research":
                result = await self._execute_research_workflow(input_data)
            elif workflow_name == "document_analysis":
                result = await self._execute_document_analysis_workflow(input_data)
            elif workflow_name == "web_research":
                result = await self._execute_web_research_workflow(input_data)
            else:
                raise ValueError(f"Unknown workflow: {workflow_name}")
            
            end_time = datetime.utcnow()
            execution_time = (end_time - start_time).total_seconds()
            
            # Log execution
            execution_record = {
                "workflow": workflow_name,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "execution_time_seconds": execution_time,
                "status": "completed"
            }
            self.execution_history.append(execution_record)
            
            return {
                "status": "success",
                "workflow": workflow_name,
                "result": result,
                "execution_time": execution_time
            }
        
        except Exception as e:
            logger.error(f"Workflow execution error: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "workflow": workflow_name
            }
    
    async def _execute_research_workflow(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute research workflow:
        1. Coordinator receives query
        2. Planning agent creates plan
        3. Research agent analyzes intent
        4. Retrieval agent finds relevant documents
        5. Summarization agent summarizes
        6. Report generation agent creates report
        """
        
        query = input_data.get("query", "")
        
        # Step 1: Coordinator
        coordinator_result = await self.agents["coordinator"].process({
            "query": query,
            "action": "delegate"
        })
        
        # Step 2: Planning
        planning_result = await self.agents["planning"].process({
            "task": query,
            "available_tools": list(self.agents.keys())
        })
        
        # Step 3: Research
        research_result = await self.agents["research"].process({
            "query": query
        })
        
        # Step 4: Retrieval
        retrieval_result = await self.agents["retrieval"].process({
            "query": query,
            "top_k": 5
        })
        
        # Step 5: Summarization
        content = retrieval_result.get("result", {}).get("content", "")
        summarization_result = await self.agents["summarization"].process({
            "content": content,
            "summary_type": "extractive"
        })
        
        # Step 6: Report Generation
        report_result = await self.agents["report_generation"].process({
            "title": f"Research Report: {query}",
            "content": summarization_result.get("result", {}).get("summary", ""),
            "report_type": "research"
        })
        
        return {
            "coordinator": coordinator_result,
            "planning": planning_result,
            "research": research_result,
            "retrieval": retrieval_result,
            "summarization": summarization_result,
            "report": report_result
        }
    
    async def _execute_document_analysis_workflow(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute document analysis workflow:
        1. File analysis agent processes file
        2. Memory agent stores document info
        3. Retrieval agent indexes content
        4. Summarization agent creates summary
        """
        
        file_path = input_data.get("file_path", "")
        file_type = input_data.get("file_type", "")
        
        # Step 1: File Analysis
        analysis_result = await self.agents["file_analysis"].process({
            "file_path": file_path,
            "file_type": file_type,
            "action": "analyze"
        })
        
        # Step 2: Memory Storage
        memory_result = await self.agents["memory"].process({
            "action": "store",
            "memory_type": "long_term",
            "content": f"Analyzed file: {file_path}",
            "metadata": analysis_result.get("result", {})
        })
        
        # Step 3: Retrieval/Indexing
        retrieval_result = await self.agents["retrieval"].process({
            "query": file_path,
            "top_k": 1
        })
        
        # Step 4: Summarization
        summarization_result = await self.agents["summarization"].process({
            "content": analysis_result.get("result", {}).get("extracted_text", ""),
            "summary_type": "extractive"
        })
        
        return {
            "file_analysis": analysis_result,
            "memory_storage": memory_result,
            "retrieval": retrieval_result,
            "summarization": summarization_result
        }
    
    async def _execute_web_research_workflow(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute web research workflow:
        1. Web search agent searches internet
        2. Memory agent stores results
        3. Summarization agent summarizes findings
        4. Citation agent manages references
        5. Report generation creates report
        """
        
        query = input_data.get("query", "")
        
        # Step 1: Web Search
        search_result = await self.agents["web_search"].process({
            "query": query,
            "num_results": 5,
            "search_type": "web"
        })
        
        # Step 2: Memory Storage
        memory_result = await self.agents["memory"].process({
            "action": "store",
            "memory_type": "short_term",
            "content": query,
            "metadata": {"search_results": len(search_result.get("results", []))}
        })
        
        # Step 3: Summarization
        results_text = "\n".join([
            f"- {r['title']}: {r['snippet']}" 
            for r in search_result.get("results", [])
        ])
        summarization_result = await self.agents["summarization"].process({
            "content": results_text,
            "summary_type": "extractive"
        })
        
        # Step 4: Citation Management
        citations = []
        for result in search_result.get("results", []):
            citation = await self.agents["citation"].process({
                "source_info": {
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "author": result.get("source", "")
                },
                "format": "apa"
            })
            citations.append(citation.get("citation", ""))
        
        # Step 5: Report Generation
        report_result = await self.agents["report_generation"].process({
            "title": f"Web Research Report: {query}",
            "content": summarization_result.get("result", {}).get("summary", ""),
            "citations": citations,
            "report_type": "research"
        })
        
        return {
            "web_search": search_result,
            "memory": memory_result,
            "summarization": summarization_result,
            "citations": citations,
            "report": report_result
        }
    
    async def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        
        status = {
            "total_agents": len(self.agents),
            "agents": {name: agent.get_status() for name, agent in self.agents.items()},
            "execution_history_length": len(self.execution_history)
        }
        
        return status
    
    async def get_execution_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get execution history"""
        
        return self.execution_history[-limit:]
    
    async def cancel_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Cancel running workflow"""
        
        if workflow_id in self.active_workflows:
            self.active_workflows.pop(workflow_id)
            return {"status": "success", "message": "Workflow cancelled"}
        
        return {"status": "error", "message": "Workflow not found"}
