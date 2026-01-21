import streamlit as st
from openai import OpenAI
from agents import Agent, Runner
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
import json

class RequirementAnalysis(BaseModel):
    classification: str = Field(description="Requirement type: FR, NFR, IR, DR, or Constraint")
    category: str = Field(description="Specific category")
    priority: str = Field(description="Priority level: Critical, High, Medium, or Low")
    description: str = Field(description="Clear, structured description")
    status: str = Field(description="Current status: Draft, Confirmed, or Implemented")

class AnalysisResponse(BaseModel):
    conflict_detected: bool = Field(description="Whether a conflict with existing requirements was found")
    conflict_details: Optional[str] = Field(None, description="Detailed explanation of the conflict if found")
    analysis: Optional[RequirementAnalysis] = Field(None, description="Structured analysis of the requirement if no conflict")

class OpenAIAgentAdapter:
    def __init__(self):
        # Read OpenRouter configuration from Streamlit secrets
        try:
            # Access secrets with the exact keys from secrets.toml
            self.api_key = st.secrets["openrouter_key"]
            self.base_url = st.secrets.get("openrouter_base_url", "https://openrouter.ai/api/v1")
            self.model = st.secrets.get("openrouter_model", "openai/gpt-oss-120b")
            
            # Debug info (remove in production or use st.write for debugging)
            st.session_state.openrouter_config = {
                "base_url": self.base_url,
                "model": self.model,
                "api_key_present": bool(self.api_key)
            }
            
            if not self.api_key:
                st.error("OpenRouter API key not found in secrets.toml. Please check your configuration.")
                raise ValueError("OpenRouter API key missing")
                
        except KeyError as e:
            st.error(f"Missing configuration in secrets.toml: {e}")
            st.info("Please ensure your .streamlit/secrets.toml contains: openrouter_key, openrouter_base_url, openrouter_model")
            raise
        
        # Initialize OpenAI client for OpenRouter
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )
        
        # Try to initialize Agents SDK
        try:
            self.runner = Runner(client=self.client)
            self.use_agents_sdk = True
            st.session_state.agents_sdk_status = "Available"
        except Exception as e:
            st.warning(f"Agents SDK initialization failed: {e}. Using direct API calls.")
            self.use_agents_sdk = False
            st.session_state.agents_sdk_status = "Unavailable - using direct API"
    
    def run_agent(self, name: str, system_prompt: str, history: List[Dict], output_type: Any = None):
        """Run an agent conversation"""
        
        # Method 1: Try using Agents SDK if available
        if self.use_agents_sdk:
            try:
                # Create agent
                agent = Agent(
                    name=name,
                    instructions=system_prompt,
                    model=self.model,
                )
                
                # Set output type if specified
                if output_type:
                    agent.output_type = output_type
                
                # Run the agent
                result = self.runner.run(
                    task=system_prompt,
                    agent=agent,
                    messages=history,
                )
                
                # Extract output
                if hasattr(result, 'final_output'):
                    return type('Result', (), {'final_output': result.final_output})()
                elif hasattr(result, 'output'):
                    return type('Result', (), {'final_output': result.output})()
                else:
                    return type('Result', (), {'final_output': str(result)})()
                    
            except Exception as e:
                st.warning(f"Agent SDK failed: {e}. Falling back to direct API.")
                self.use_agents_sdk = False
        
        # Method 2: Direct API call (fallback)
        return self._direct_api_call(name, system_prompt, history, output_type)
    
    def _direct_api_call(self, name: str, system_prompt: str, history: List[Dict], output_type: Any = None):
        """Direct API call to OpenRouter"""
        try:
            # Prepare messages
            messages = [{"role": "system", "content": system_prompt}] + history
            
            # Make API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000,
                stream=False
            )
            
            content = response.choices[0].message.content
            
            # Handle structured output if requested
            if output_type and issubclass(output_type, BaseModel):
                # Try to extract JSON from response
                try:
                    # Look for JSON pattern
                    import re
                    json_match = re.search(r'\{.*\}', content, re.DOTALL)
                    if json_match:
                        json_str = json_match.group()
                        data = json.loads(json_str)
                        return type('Result', (), {'final_output': output_type(**data)})()
                except:
                    # If JSON parsing fails, return as text
                    pass
            
            return type('Result', (), {'final_output': content})()
            
        except Exception as e:
            st.error(f"OpenRouter API call failed: {str(e)}")
            return None
    
    def simple_chat_completion(self, messages: List[Dict], temperature: float = 0.7) -> Optional[str]:
        """Simple chat completion without agent framework"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"Chat completion failed: {e}")
            return None

# Helper function for simple calls
def get_openai_response(system_prompt: str, user_message: str, model: str = None) -> Optional[str]:
    """Simple function to get OpenAI response"""
    try:
        adapter = OpenAIAgentAdapter()
        
        response = adapter.client.chat.completions.create(
            model=model or adapter.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"OpenAI call failed: {e}")
        return None