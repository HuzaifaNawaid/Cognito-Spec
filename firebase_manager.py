import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from typing import Dict, List, Optional
import json

class FirebaseManager:
    def __init__(self):
        if not firebase_admin._apps:
            try:
                # Convert st.secrets to a dictionary for credentials
                firebase_config = dict(st.secrets["firebase"])
                cred = credentials.Certificate(firebase_config)
                firebase_admin.initialize_app(cred)
            except Exception as e:
                st.error(f"Firebase initialization failed: {str(e)}")
                raise
        
        self.db = firestore.client()
    
    def save_requirement(self, project_id: str, req_data: Dict) -> str:
        """Save requirement to Firestore and return document ID"""
        doc_ref = self.db.collection(f"projects/{project_id}/requirements").add(req_data)
        return doc_ref[1].id
    
    def fetch_all_requirements(self, project_id: str) -> List[Dict]:
        """Fetch all requirements for a project"""
        requirements = []
        try:
            docs = self.db.collection(f"projects/{project_id}/requirements").stream()
            
            for doc in docs:
                req_data = doc.to_dict()
                req_data['id'] = doc.id
                requirements.append(req_data)
        except Exception as e:
            st.error(f"Error fetching requirements: {str(e)}")
        
        return requirements
    
    def update_requirement(self, project_id: str, doc_id: str, data: Dict) -> None:
        """Update a specific requirement"""
        try:
            doc_ref = self.db.collection(f"projects/{project_id}/requirements").document(doc_id)
            doc_ref.update(data)
        except Exception as e:
            st.error(f"Error updating requirement: {str(e)}")
    
    def delete_requirement(self, project_id: str, doc_id: str) -> None:
        """Delete a requirement"""
        try:
            doc_ref = self.db.collection(f"projects/{project_id}/requirements").document(doc_id)
            doc_ref.delete()
        except Exception as e:
            st.error(f"Error deleting requirement: {str(e)}")

# Global instance
firebase_manager = FirebaseManager()