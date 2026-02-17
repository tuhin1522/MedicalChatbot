import re
from typing import Any, Dict, Optional
from ..core import config, logger

class SafetyValidator:
    """Validate queries and responses for medical safety"""
    
    # Emergency keywords that require immediate medical attention
    EMERGENCY_KEYWORDS = [
        'chest pain', 'heart attack', 'stroke', 'seizure', 'unconscious',
        'severe bleeding', 'difficulty breathing', 'can\'t breathe',
        'suicide', 'overdose', 'severe burn', 'choking', 'anaphylaxis'
    ]
    
    # Harmful intent keywords to block
    HARMFUL_KEYWORDS = [
        'how to die', 'kill myself', 'end my life', 'suicide methods',
        'self harm', 'cutting myself', 'overdose on'
    ]
    
    MEDICAL_DISCLAIMER = (
        "\n\nMEDICAL DISCLAIMER:\n"
        "This information is for educational purposes only and is not a substitute "
        "for professional medical advice, diagnosis, or treatment. Always seek the "
        "advice of your physician or qualified health provider with any questions "
        "regarding a medical condition. Never disregard professional medical advice "
        "or delay seeking it because of information provided here."
    )
    
    EMERGENCY_MESSAGE = (
        "\n\nEMERGENCY ALERT:\n"
        "Your question suggests a medical emergency. Please:\n"
        "• Call emergency services (911 in US, 999 in UK, 112 in EU) immediately\n"
        "• Go to the nearest emergency room\n"
        "• Contact your local emergency services\n\n"
        "Do NOT rely on this chatbot for emergency medical situations!"
    )
    
    # Common greetings and conversational phrases
    GREETINGS = [
        'hi', 'hello', 'hey', 'yo', 'sup', 'greetings', 'good morning',
        'good afternoon', 'good evening', 'howdy', 'hola', 'bonjour'
    ]
    
    @staticmethod
    def validate_query(query: str) -> Dict[str, Any]:
        """
        Validate if query is safe and appropriate
        Returns: dict with validation results
        """
        query_lower = query.lower().strip()
        
        # Allow greetings and short conversational messages
        if len(query) < 3:
            # Check if it's a greeting or common short message
            if query_lower in SafetyValidator.GREETINGS or any(
                greeting in query_lower for greeting in SafetyValidator.GREETINGS
            ):
                return {
                    "is_valid": True,
                    "is_greeting": True,
                    "is_emergency": False,
                    "is_harmful": False,
                    "needs_disclaimer": False
                }
            return {
                "is_valid": False,
                "reason": "Query too short. Please ask a complete question.",
                "is_emergency": False,
                "is_harmful": False,
                "needs_disclaimer": True
            }
        
        if len(query) > config.MAX_QUERY_LENGTH:
            return {
                "is_valid": False,
                "reason": f"Query too long (max {config.MAX_QUERY_LENGTH} characters).",
                "is_emergency": False,
                "is_harmful": False,
                "needs_disclaimer": True
            }
        
        # Check for harmful intent
        for keyword in SafetyValidator.HARMFUL_KEYWORDS:
            if keyword in query_lower:
                logger.warning(f"Harmful query detected: {keyword}")
                return {
                    "is_valid": False,
                    "reason": (
                        "I cannot provide information that could cause harm.\n\n"
                        "If you're experiencing a mental health crisis:\n"
                        "• National Suicide Prevention Lifeline: 988 (US)\n"
                        "• Crisis Text Line: Text HOME to 741741\n"
                        "• International: https://findahelpline.com"
                    ),
                    "is_emergency": False,
                    "is_harmful": True,
                    "needs_disclaimer": True
                }
        
        # Check for emergency
        is_emergency = SafetyValidator.detect_emergency(query)
        if is_emergency:
            return {
                "is_valid": True,
                "is_emergency": True,
                "emergency_type": "medical",
                "is_harmful": False,
                "needs_disclaimer": True
            }
        
        return {
            "is_valid": True,
            "is_emergency": False,
            "is_harmful": False,
            "needs_disclaimer": True
        }
    
    @staticmethod
    def detect_emergency(query: str) -> bool:
        """Detect if query describes a medical emergency"""
        query_lower = query.lower()
        for keyword in SafetyValidator.EMERGENCY_KEYWORDS:
            if keyword in query_lower:
                logger.warning(f"Emergency keyword detected: {keyword}")
                return True
        return False
    
    @staticmethod
    def add_disclaimer(response: str, is_emergency: bool = False) -> str:
        """Add medical disclaimer to response"""
        if is_emergency:
            response = SafetyValidator.EMERGENCY_MESSAGE + "\n\n" + response
        
        if config.ENABLE_MEDICAL_DISCLAIMER:
            response += SafetyValidator.MEDICAL_DISCLAIMER
        
        return response