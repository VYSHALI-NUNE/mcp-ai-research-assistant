"""
Report Generation Agent - Creates structured research reports
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
from backend.agents.base_agent import BaseAgent
import logging
import json

logger = logging.getLogger(__name__)


class ReportGenerationAgent(BaseAgent):
    """Agent responsible for generating structured reports"""
    
    def __init__(self):
        super().__init__(
            name="Report Generation Agent",
            description="Generates structured research reports and summaries",
            agent_type="report_generation"
        )
        self.report_templates = {
            "research": self._research_template,
            "analysis": self._analysis_template,
            "summary": self._summary_template,
            "executive": self._executive_template
        }
    
    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process report generation request
        
        Args:
            data: Dictionary containing:
                - report_type: research, analysis, summary, executive
                - title: Report title
                - content: Report content/findings
                - citations: List of citations
                - metadata: Additional metadata
        
        Returns:
            Generated report
        """
        try:
            self.log_action("processing", data)
            
            report_type = data.get("report_type", "research")
            title = data.get("title", "Research Report")
            content = data.get("content", "")
            citations = data.get("citations", [])
            metadata = data.get("metadata", {})
            
            if not content:
                raise ValueError("Report content is required")
            
            # Generate report
            report = await self._generate_report(
                report_type, title, content, citations, metadata
            )
            
            self.log_action("completed", {"report_type": report_type})
            
            return {
                "status": "success",
                "report": report
            }
        
        except Exception as e:
            logger.error(f"Report generation error: {str(e)}")
            self.log_action("error", {"error": str(e)})
            return {"status": "error", "error": str(e)}
    
    async def _generate_report(
        self, 
        report_type: str, 
        title: str, 
        content: str, 
        citations: List[str],
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate structured report"""
        
        template = self.report_templates.get(report_type, self._research_template)
        
        report = {
            "title": title,
            "type": report_type,
            "generated_at": datetime.utcnow().isoformat(),
            "metadata": metadata,
            "sections": {
                "introduction": await self._generate_introduction(title),
                "content": content,
                "findings": await self._extract_findings(content),
                "conclusion": await self._generate_conclusion(content),
                "references": citations
            }
        }
        
        return report
    
    async def _generate_introduction(self, title: str) -> str:
        """Generate report introduction"""
        return f"This report presents a comprehensive analysis of '{title}'."
    
    async def _extract_findings(self, content: str) -> List[str]:
        """Extract key findings from content"""
        # In production, use NLP to extract findings
        findings = [
            "Key finding 1: Analysis reveals important insight",
            "Key finding 2: Data demonstrates significant trend",
            "Key finding 3: Results support the research hypothesis"
        ]
        return findings
    
    async def _generate_conclusion(self, content: str) -> str:
        """Generate report conclusion"""
        return "In conclusion, this research demonstrates important implications for future studies."
    
    def _research_template(self) -> str:
        """Research report template"""
        return """
        # Research Report
        
        ## Executive Summary
        {summary}
        
        ## Introduction
        {introduction}
        
        ## Methodology
        {methodology}
        
        ## Findings
        {findings}
        
        ## Analysis
        {analysis}
        
        ## Conclusion
        {conclusion}
        
        ## References
        {references}
        """
    
    def _analysis_template(self) -> str:
        """Analysis report template"""
        return """
        # Analysis Report
        
        ## Overview
        {overview}
        
        ## Data Analysis
        {data_analysis}
        
        ## Key Insights
        {insights}
        
        ## Recommendations
        {recommendations}
        
        ## References
        {references}
        """
    
    def _summary_template(self) -> str:
        """Summary report template"""
        return """
        # Summary Report
        
        ## Overview
        {overview}
        
        ## Key Points
        {key_points}
        
        ## Conclusion
        {conclusion}
        """
    
    def _executive_template(self) -> str:
        """Executive summary template"""
        return """
        # Executive Summary
        
        ## Situation
        {situation}
        
        ## Action
        {action}
        
        ## Results
        {results}
        
        ## Recommendation
        {recommendation}
        """
    
    async def generate_markdown_report(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate markdown formatted report"""
        try:
            self.log_action("generating_markdown", report_data)
            
            markdown = f"""# {report_data.get('title', 'Report')}

**Generated:** {datetime.utcnow().isoformat()}

## Executive Summary

{report_data.get('summary', 'No summary provided')}

## Findings

{self._format_findings(report_data.get('findings', []))}

## Details

{report_data.get('content', 'No content provided')}

## References

{self._format_references(report_data.get('citations', []))}

---

*Generated by MCP Research Assistant*
"""
            
            return {
                "status": "success",
                "format": "markdown",
                "content": markdown
            }
        
        except Exception as e:
            logger.error(f"Markdown generation error: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    async def generate_pdf_report(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate PDF formatted report"""
        try:
            self.log_action("generating_pdf", report_data)
            
            # In production, use reportlab or similar library
            pdf_content = {
                "title": report_data.get('title', 'Report'),
                "generated_at": datetime.utcnow().isoformat(),
                "sections": report_data.get('sections', {}),
                "format": "PDF"
            }
            
            return {
                "status": "success",
                "format": "pdf",
                "content": json.dumps(pdf_content, indent=2)
            }
        
        except Exception as e:
            logger.error(f"PDF generation error: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    async def generate_html_report(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate HTML formatted report"""
        try:
            self.log_action("generating_html", report_data)
            
            html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{report_data.get('title', 'Report')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #333; }}
        .section {{ margin: 20px 0; }}
        .citation {{ margin-left: 20px; font-style: italic; }}
    </style>
</head>
<body>
    <h1>{report_data.get('title', 'Report')}</h1>
    <p>Generated: {datetime.utcnow().isoformat()}</p>
    
    <div class="section">
        <h2>Summary</h2>
        <p>{report_data.get('summary', 'No summary provided')}</p>
    </div>
    
    <div class="section">
        <h2>Findings</h2>
        {self._format_html_findings(report_data.get('findings', []))}
    </div>
    
    <div class="section">
        <h2>References</h2>
        {self._format_html_references(report_data.get('citations', []))}
    </div>
</body>
</html>
"""
            
            return {
                "status": "success",
                "format": "html",
                "content": html
            }
        
        except Exception as e:
            logger.error(f"HTML generation error: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    def _format_findings(self, findings: List[str]) -> str:
        """Format findings as markdown"""
        return "\n".join([f"- {finding}" for finding in findings])
    
    def _format_references(self, citations: List[str]) -> str:
        """Format references as markdown"""
        return "\n".join([f"- {citation}" for citation in citations])
    
    def _format_html_findings(self, findings: List[str]) -> str:
        """Format findings as HTML"""
        return "<ul>" + "".join([f"<li>{finding}</li>" for finding in findings]) + "</ul>"
    
    def _format_html_references(self, citations: List[str]) -> str:
        """Format references as HTML"""
        citations_html = "".join([f'<div class="citation">{citation}</div>' for citation in citations])
        return citations_html
    
    async def add_metadata_to_report(self, report: Dict[str, Any], metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Add metadata to report"""
        try:
            report["metadata"] = {
                **report.get("metadata", {}),
                **metadata,
                "updated_at": datetime.utcnow().isoformat()
            }
            
            return {
                "status": "success",
                "report": report
            }
        
        except Exception as e:
            logger.error(f"Metadata addition error: {str(e)}")
            return {"status": "error", "error": str(e)}
