import streamlit as st
from openai_adapter import OpenAIAgentAdapter, AnalysisResponse, get_openai_response
from firebase_manager import firebase_manager
from typing import List, Dict
from datetime import datetime
import json
import re

class AIController:
    def __init__(self):
        try:
            self.openai_adapter = OpenAIAgentAdapter()
            st.session_state.ai_controller_status = "Initialized"
        except Exception as e:
            st.error(f"Failed to initialize AI Controller: {e}")
            st.session_state.ai_controller_status = f"Error: {str(e)}"
            self.openai_adapter = None
    
    def _is_initialized(self):
        """Check if adapter is initialized"""
        if not self.openai_adapter:
            st.error("AI Controller not initialized. Please check your OpenRouter configuration.")
            return False
        return True
    
    # Agent 1: Enhanced Elicitation Agent
    def elicit_requirement(self, domain: str, conflict_context: str = None) -> str:
        """Agent 1: Ask domain-specific questions"""
        
        if not self._is_initialized():
            return "I'm having trouble connecting to the AI service. Please check your configuration."
        
        if conflict_context:
            system_prompt = f"""You are a requirements engineering specialist helping resolve a conflict.

Context: {conflict_context}

Ask ONE clear question to help resolve this conflict. Be neutral and helpful."""
        else:
            system_prompt = f"""You are a requirements engineering specialist for {domain} systems.

Ask ONE clear, specific question about the software requirements. Focus on one of these areas:

1. Functional Requirements (what the system should DO)
2. Non-Functional Requirements (how well it should perform)
3. Inverse Requirements (what it should NOT do)
4. Domain-specific Requirements (unique to {domain})
5. Constraints (limitations)

Ask only ONE question. Make it specific to {domain}."""
        
        history = st.session_state.get('chat_history', [])
        
        try:
            result = self.openai_adapter.run_agent("Elicitor", system_prompt, history)
            
            if result and hasattr(result, 'final_output'):
                response = str(result.final_output)
                if response and len(response.strip()) > 0:
                    return response
        except Exception as e:
            st.warning(f"Elicitation failed: {e}")
        
        # Fallback question
        fallback_questions = {
            "Healthcare": "What is the most critical function this healthcare system must perform?",
            "Finance": "What security measures are essential for this financial system?",
            "E-commerce": "What are the key user actions in this e-commerce system?",
            "Education": "How should users interact with this educational platform?",
            "Manufacturing": "What production data needs to be tracked in real-time?",
            "Other": "Can you describe the main purpose of this system?"
        }
        
        return fallback_questions.get(domain, "What are the key requirements for your system?")
    
    # Agent 2: Analysis Agent
    def analyze_and_detect_conflicts(self, user_input: str, project_id: str) -> Dict:
        """Analyze requirement and detect conflicts"""
        
        if not self._is_initialized():
            return {
                "conflict_detected": False,
                "conflicting_req_id": None,
                "conflict_details": "",
                "analysis": {
                    "classification": "FR",
                    "category": "General",
                    "priority": "Medium",
                    "description": user_input,
                    "status": "Draft"
                }
            }
        
        # Get existing requirements
        existing_reqs = firebase_manager.fetch_all_requirements(project_id)
        
        system_prompt = """You are a requirements analyst. Analyze the user input as a software requirement.

Provide analysis in this JSON format:
{
    "conflict_detected": true/false,
    "conflict_details": "explain conflict if any",
    "analysis": {
        "classification": "FR/NFR/IR/DR/Constraint",
        "category": "specific category like 'Security', 'Performance', etc.",
        "priority": "Critical/High/Medium/Low",
        "description": "clear requirement statement",
        "status": "Draft"
    }
}

Classification guide:
- FR: Functional Requirement (what system does)
- NFR: Non-Functional Requirement (quality attributes)
- IR: Inverse Requirement (what system should NOT do)
- DR: Domain Requirement (industry-specific)
- Constraint: Technical/business limitation

Check for conflicts with existing requirements. Be concise."""
        
        # Add context of existing requirements
        existing_text = ""
        if existing_reqs:
            existing_text = "Existing requirements:\n" + "\n".join([
                f"- {req.get('description', '')} [{req.get('classification', 'Unknown')}]"
                for req in existing_reqs[-3:]  # Last 3 requirements
            ])
        
        user_message = f"{existing_text}\n\nNew requirement to analyze: {user_input}"
        
        messages = st.session_state.get('chat_history', []) + [
            {"role": "user", "content": user_message}
        ]
        
        response_data = {
            "conflict_detected": False,
            "conflicting_req_id": None,
            "conflict_details": "",
            "analysis": None
        }
        
        try:
            result = self.openai_adapter.run_agent(
                "Analyzer", 
                system_prompt, 
                messages,
                output_type=AnalysisResponse
            )
            
            if result and hasattr(result, 'final_output'):
                output = result.final_output
                
                if isinstance(output, AnalysisResponse):
                    # Handle structured output
                    response_data["conflict_detected"] = output.conflict_detected
                    response_data["conflict_details"] = output.conflict_details or ""
                    
                    if output.analysis:
                        response_data["analysis"] = output.analysis.model_dump()
                        
                    if output.conflict_detected and existing_reqs:
                        response_data["conflicting_req_id"] = existing_reqs[-1].get("id")
                        
                else:
                    # Handle text output
                    response_data = self._parse_text_analysis(str(output), user_input, existing_reqs, response_data)
                    
        except Exception as e:
            st.warning(f"Analysis failed: {e}")
            response_data = self._simple_analysis(user_input, existing_reqs, response_data)
        
        return response_data
    
    def _parse_text_analysis(self, text: str, user_input: str, existing_reqs: List[Dict], response_data: Dict) -> Dict:
        """Parse text analysis response"""
        try:
            # Try to extract JSON
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                
                response_data["conflict_detected"] = data.get("conflict_detected", False)
                response_data["conflict_details"] = data.get("conflict_details", "")
                
                if data.get("analysis"):
                    response_data["analysis"] = data["analysis"]
                    
                if response_data["conflict_detected"] and existing_reqs:
                    response_data["conflicting_req_id"] = existing_reqs[-1].get("id")
                    
                return response_data
        except:
            pass
        
        # If JSON parsing fails, use simple analysis
        return self._simple_analysis(user_input, existing_reqs, response_data)
    
    def _simple_analysis(self, user_input: str, existing_reqs: List[Dict], response_data: Dict) -> Dict:
        """Simple fallback analysis"""
        # Simple keyword-based classification
        input_lower = user_input.lower()
        
        if any(word in input_lower for word in ["not", "never", "cannot", "must not", "should not"]):
            classification = "IR"
        elif any(word in input_lower for word in ["fast", "secure", "reliable", "user-friendly", "scalable"]):
            classification = "NFR"
        elif any(word in input_lower for word in ["must", "shall", "should", "will"]):
            classification = "FR"
        else:
            classification = "FR"
        
        response_data["analysis"] = {
            "classification": classification,
            "category": "General",
            "priority": "Medium",
            "description": user_input,
            "status": "Draft"
        }
        
        # Simple conflict detection
        if existing_reqs:
            last_desc = existing_reqs[-1].get('description', '').lower()
            if ("not" in input_lower and "not" not in last_desc) or \
               ("must" in input_lower and "cannot" in last_desc):
                response_data["conflict_detected"] = True
                response_data["conflict_details"] = "Possible logical contradiction"
                response_data["conflicting_req_id"] = existing_reqs[-1].get("id")
        
        return response_data
    
    # Agent 3: SRS Generation
    def compile_srs_document(self, project_id: str) -> str:
        """Compile requirements into SRS document"""
        
        if not self._is_initialized():
            return "# Software Requirements Specification\n\n*AI service unavailable*\n\nPlease check your OpenRouter configuration."
        
        requirements = firebase_manager.fetch_all_requirements(project_id)
        
        if not requirements:
            return "# Software Requirements Specification\n\n*No requirements collected yet*\n\nPlease collect requirements in the Interview section."
        
        system_prompt = """You are a technical writer creating a Software Requirements Specification (SRS).

Create a professional SRS document with these sections:
1. INTRODUCTION
2. FUNCTIONAL REQUIREMENTS
3. NON-FUNCTIONAL REQUIREMENTS  
4. INVERSE REQUIREMENTS
5. DOMAIN REQUIREMENTS
6. CONSTRAINTS
7. APPENDIX

Use IEEE SRS format. Be thorough and professional.
Format in markdown with proper headings."""
        
        # Prepare requirements text
        req_by_type = {}
        for req in requirements:
            req_type = req.get('classification', 'Unknown')
            if req_type not in req_by_type:
                req_by_type[req_type] = []
            req_by_type[req_type].append(req)
        
        reqs_text = "Requirements by type:\n\n"
        for req_type in ["FR", "NFR", "IR", "DR", "Constraint", "Unknown"]:
            if req_type in req_by_type:
                reqs_text += f"\n{req_type} Requirements:\n"
                for req in req_by_type[req_type]:
                    reqs_text += f"- {req.get('description', '')}\n"
        
        messages = [{"role": "user", "content": reqs_text}]
        
        try:
            result = self.openai_adapter.run_agent("Scribe", system_prompt, messages)
            
            if result and hasattr(result, 'final_output'):
                return str(result.final_output)
        except Exception as e:
            st.warning(f"SRS generation failed: {e}")
        
        # Fallback SRS
        return self._generate_fallback_srs(requirements)
    
    def _generate_fallback_srs(self, requirements: List[Dict]) -> str:
        """Generate a simple SRS when AI fails"""
        project_name = st.session_state.get('project_name', 'Project')
        domain = st.session_state.get('domain', 'General')
        
        srs = f"""# Software Requirements Specification

## 1. INTRODUCTION
**Project:** {project_name}
**Domain:** {domain}
**Date:** {datetime.now().strftime('%Y-%m-%d')}
**Total Requirements:** {len(requirements)}

## 2. FUNCTIONAL REQUIREMENTS
"""
        
        # Add requirements by type
        for req in requirements:
            if req.get('classification') == 'FR':
                srs += f"- {req.get('description', '')}\n"
        
        srs += "\n## 3. NON-FUNCTIONAL REQUIREMENTS\n"
        for req in requirements:
            if req.get('classification') == 'NFR':
                srs += f"- {req.get('description', '')}\n"
        
        srs += "\n## 4. OTHER REQUIREMENTS\n"
        for req in requirements:
            if req.get('classification') not in ['FR', 'NFR']:
                srs += f"- [{req.get('classification', 'Unknown')}] {req.get('description', '')}\n"
        
        return srs
    
    # Agent 4: Gap Analysis
    def perform_gap_analysis(self, project_id: str, domain: str) -> str:
        """Perform gap analysis"""
        
        if not self._is_initialized():
            return f"# Gap Analysis Report\n\n*AI service unavailable for {domain} system*\n\nPlease check your OpenRouter configuration."
        
        requirements = firebase_manager.fetch_all_requirements(project_id)
        
        if not requirements:
            return f"# Gap Analysis Report\n\n*No requirements found for {domain} system*\n\nPlease collect requirements first."
        
        system_prompt = f"""You are a senior systems analyst performing gap analysis for a {domain} system.

Generate a comprehensive gap analysis report with this structure:

# Gap Analysis Report
**Date:** {datetime.now().strftime('%B %d, %Y')}
**Domain:** {domain}
**Prepared By:** Requirements Engineer

## Executive Summary
## Identified Gaps
## Risk Assessment  
## Recommendations
## Next Steps

Be specific to {domain}. Identify missing requirements, potential issues, and provide actionable recommendations.
Format in markdown. Don't generate long validation report, be concise and specific to the domain.
Don't generate any additional text other than the gap analysis report."""
        
        reqs_text = f"Current requirements for {domain} system:\n\n"
        for req in requirements:
            reqs_text += f"- {req.get('description', '')} [{req.get('classification', 'Unknown')}]\n"
        
        messages = [{"role": "user", "content": reqs_text}]
        
        try:
            result = self.openai_adapter.run_agent("Validator", system_prompt, messages)
            
            if result and hasattr(result, 'final_output'):
                return str(result.final_output)
        except Exception as e:
            st.warning(f"Gap analysis failed: {e}")
        
        # Fallback gap analysis
        return self._generate_fallback_gap_analysis(domain, requirements)
    
    def _generate_fallback_gap_analysis(self, domain: str, requirements: List[Dict]) -> str:
        """Simple gap analysis fallback"""
        return f"""# Gap Analysis Report

**Date:** {datetime.now().strftime('%B %d, %Y')}
**Domain:** {domain}
**Prepared By:** Requirements Engineer
**Total Requirements Analyzed:** {len(requirements)}

## Executive Summary
Analysis of {len(requirements)} requirements for {domain} system. Review completed.

## Key Findings
- Requirements cover basic functionality
- Consider adding more specific {domain}-related requirements
- Review non-functional aspects (security, performance)

## Recommendations
1. Conduct stakeholder review session
2. Validate requirements with domain experts
3. Prioritize requirements for implementation

## Next Steps
- Schedule requirements validation meeting
- Develop detailed use cases
- Create implementation roadmap"""

# Global instance
ai_controller = AIController()