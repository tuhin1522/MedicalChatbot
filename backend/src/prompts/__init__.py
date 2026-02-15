"""
Prompts module for Medical Chatbot
Contains all prompt templates for the RAG system
"""

from .medical_prompts import conversational_prompt, conversational_prompt_template

__all__ = [
    "conversational_prompt",
    "conversational_prompt_template",
]
