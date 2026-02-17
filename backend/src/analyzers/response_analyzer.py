from typing import Dict, List, Any
import json

class ResponseAnalyzer:
    """Analyze and score chatbot responses"""
    
    # Phrases indicating uncertainty
    UNCERTAINTY_PHRASES = [
        "i don't know",
        "not sure",
        "cannot find",
        "unclear",
        "insufficient information",
        "i don't have enough information"
    ]
    
    @staticmethod
    def calculate_confidence(result: Dict[str, Any]) -> float:
        """
        Calculate confidence score based on retrieval and response
        Returns: confidence score between 0 and 1
        """
        confidence = 0.5  # Base confidence
        
        # Check if we have source documents
        if result.get("source_documents"):
            docs = result["source_documents"]
            
            # More documents = higher confidence (up to 0.3 boost)
            doc_boost = min(len(docs) * 0.1, 0.3)
            confidence += doc_boost
            
            # Check document relevance scores if available
            # ChromaDB provides distance/similarity scores
            # Lower distance = higher relevance
        
        # Check response for uncertainty
        answer = result.get("answer", result.get("result", "")).lower()
        for phrase in ResponseAnalyzer.UNCERTAINTY_PHRASES:
            if phrase in answer:
                confidence -= 0.3
                break
        
        # Check response length (very short = low confidence)
        if len(answer) < 50:
            confidence -= 0.2
        
        # Ensure confidence is between 0 and 1
        confidence = max(0.0, min(1.0, confidence))
        
        return round(confidence, 2)
    
    @staticmethod
    def get_confidence_label(confidence: float) -> str:
        """Get human-readable confidence label"""
        if confidence >= 0.8:
            return "🟢 High Confidence"
        elif confidence >= 0.5:
            return "🟡 Medium Confidence"
        else:
            return "🔴 Low Confidence"
    
    @staticmethod
    def format_sources(source_documents: List[Any]) -> List[Dict[str, str]]:
        """Format source documents for display"""
        formatted_sources = []
        seen_sources = set()
        
        for doc in source_documents:
            source = doc.metadata.get("source", "Unknown")
            filename = source.split("/")[-1] if "/" in source else source
            
            # Avoid duplicate sources
            if filename not in seen_sources:
                formatted_sources.append({
                    "filename": filename,
                    "content_preview": doc.page_content[:150] + "..."
                })
                seen_sources.add(filename)
        
        return formatted_sources
    
    @staticmethod
    def analyze_response(result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive response analysis
        Returns enriched result with confidence, sources, and quality metrics
        """
        confidence = ResponseAnalyzer.calculate_confidence(result)
        confidence_label = ResponseAnalyzer.get_confidence_label(confidence)
        
        analysis = {
            "confidence": confidence,
            "confidence_label": confidence_label,
            "source_count": len(result.get("source_documents", [])),
        }
        
        # Format sources if available
        if result.get("source_documents"):
            analysis["formatted_sources"] = ResponseAnalyzer.format_sources(
                result["source_documents"]
            )
        
        return analysis
