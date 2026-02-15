#!/usr/bin/env python3
"""
Example API Client
Demonstrates how to interact with the Medical Chatbot API
"""

import requests
import json
from typing import Optional


class MedicalChatbotClient:
    """Simple client for the Medical Chatbot API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize the client
        
        Args:
            base_url: Base URL of the API server
        """
        self.base_url = base_url
        self.session_id = None
    
    def health_check(self) -> dict:
        """Check if the API is healthy"""
        response = requests.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    def chat(self, query: str, session_id: Optional[str] = None) -> dict:
        """
        Send a chat message
        
        Args:
            query: User's medical query
            session_id: Optional session ID for conversation tracking
            
        Returns:
            dict: API response with answer and sources
        """
        data = {"query": query}
        if session_id:
            data["session_id"] = session_id
        elif self.session_id:
            data["session_id"] = self.session_id
        
        response = requests.post(
            f"{self.base_url}/chat",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()
    
    def get_history(self, session_id: Optional[str] = None) -> dict:
        """Get conversation history"""
        params = {}
        if session_id:
            params["session_id"] = session_id
        elif self.session_id:
            params["session_id"] = self.session_id
        
        response = requests.get(f"{self.base_url}/chat/history", params=params)
        response.raise_for_status()
        return response.json()
    
    def reset_conversation(self, session_id: Optional[str] = None) -> dict:
        """Reset conversation memory"""
        data = {"confirm": True}
        if session_id:
            data["session_id"] = session_id
        elif self.session_id:
            data["session_id"] = self.session_id
        
        response = requests.post(f"{self.base_url}/chat/reset", json=data)
        response.raise_for_status()
        return response.json()
    
    def get_metrics(self) -> dict:
        """Get performance metrics"""
        response = requests.get(f"{self.base_url}/admin/metrics")
        response.raise_for_status()
        return response.json()
    
    def get_database_info(self) -> dict:
        """Get vector database information"""
        response = requests.get(f"{self.base_url}/admin/database/info")
        response.raise_for_status()
        return response.json()


def interactive_demo():
    """Run an interactive demo of the API"""
    print("🏥 Medical Chatbot API Client Demo")
    print("=" * 50)
    
    # Initialize client
    client = MedicalChatbotClient()
    
    # Check health
    print("\n📊 Checking API health...")
    try:
        health = client.health_check()
        print(f"✅ API Status: {health['status']}")
        print(f"   LLM Model: {health['llm_model']}")
        print(f"   Database: {health['database_status']}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        print("   Make sure the API server is running: python main.py")
        return
    
    # Get database info
    print("\n📚 Database Information:")
    try:
        db_info = client.get_database_info()
        print(f"   Status: {db_info['status']}")
        if db_info.get('document_count'):
            print(f"   Documents: {db_info['document_count']}")
            print(f"   Size: {db_info.get('size_mb', 0):.2f} MB")
    except Exception as e:
        print(f"   ⚠️ Database not initialized: {e}")
    
    # Interactive chat
    print("\n💬 Starting interactive chat...")
    print("   Type 'history' to see conversation history")
    print("   Type 'reset' to reset conversation")
    print("   Type 'metrics' to see performance metrics")
    print("   Type 'quit' to exit")
    print("-" * 50)
    
    while True:
        try:
            # Get user input
            query = input("\n🧑 You: ").strip()
            
            if not query:
                continue
            
            # Handle special commands
            if query.lower() == 'quit':
                print("\n👋 Goodbye!")
                break
            
            elif query.lower() == 'history':
                history = client.get_history()
                print(f"\n📜 Conversation History ({history['total_messages']} messages):")
                for msg in history['messages']:
                    role = "🧑" if msg['role'] == 'human' else "🤖"
                    content = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
                    print(f"   {role} {content}")
                continue
            
            elif query.lower() == 'reset':
                result = client.reset_conversation()
                print(f"\n✅ {result['message']}")
                continue
            
            elif query.lower() == 'metrics':
                metrics = client.get_metrics()
                print(f"\n📊 Performance Metrics:")
                print(f"   Total Queries: {metrics['total_queries']}")
                print(f"   Success Rate: {metrics['successful_queries']}/{metrics['total_queries']}")
                print(f"   Avg Response Time: {metrics['average_response_time']:.2f}s")
                print(f"   Avg Confidence: {metrics['average_confidence']:.2f}")
                continue
            
            # Send chat message
            print("🤖 Bot: ", end="", flush=True)
            response = client.chat(query)
            
            # Display answer
            print(response['answer'])
            
            # Display confidence
            confidence_emoji = {
                'high': '🟢',
                'medium': '🟡',
                'low': '🔴'
            }
            confidence = response.get('confidence', 'medium')
            print(f"\n   {confidence_emoji.get(confidence, '⚪')} Confidence: {confidence} ({response.get('confidence_score', 0):.2f})")
            
            # Display sources
            if response.get('sources'):
                print(f"   📚 Sources: {len(response['sources'])} documents")
            
            # Display response time
            print(f"   ⏱️  Response time: {response.get('response_time', 0):.2f}s")
            
            # Display disclaimer if present
            if response.get('disclaimer'):
                print(f"\n   ⚠️  {response['disclaimer']}")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        
        except Exception as e:
            print(f"\n❌ Error: {e}")


def simple_example():
    """Simple usage example"""
    print("🏥 Simple API Example")
    print("=" * 50)
    
    client = MedicalChatbotClient()
    
    # Check health
    health = client.health_check()
    print(f"API Status: {health['status']}")
    
    # Ask a question
    query = "What are the symptoms of diabetes?"
    print(f"\nQuestion: {query}")
    
    response = client.chat(query)
    print(f"\nAnswer: {response['answer']}")
    print(f"Confidence: {response['confidence']}")
    print(f"Sources: {len(response['sources'])}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "simple":
        simple_example()
    else:
        interactive_demo()
