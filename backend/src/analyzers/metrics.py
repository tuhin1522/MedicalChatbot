from typing import Dict, List, Any
import json


class PerformanceMetrics:
    """Track performance metrics"""
    
    def __init__(self):
        self.metrics = {
            "total_queries": 0,
            "successful_queries": 0,
            "failed_queries": 0,
            "total_response_time": 0.0,
            "avg_response_time": 0.0,
            "avg_confidence": 0.0,
            "emergency_detections": 0
        }
    
    def record_query(self, success: bool, response_time: float, 
                    confidence: float = 0.0, is_emergency: bool = False):
        """Record query metrics"""
        self.metrics["total_queries"] += 1
        
        if success:
            self.metrics["successful_queries"] += 1
            self.metrics["total_response_time"] += response_time
            
            # Update averages
            queries = self.metrics["successful_queries"]
            self.metrics["avg_response_time"] = (
                self.metrics["total_response_time"] / queries
            )
            
            # Update average confidence
            prev_avg = self.metrics["avg_confidence"]
            self.metrics["avg_confidence"] = (
                (prev_avg * (queries - 1) + confidence) / queries
            )
        else:
            self.metrics["failed_queries"] += 1
        
        if is_emergency:
            self.metrics["emergency_detections"] += 1
    
    def get_summary(self) -> Dict[str, Any]:
        """Get metrics summary as dictionary"""
        m = self.metrics
        success_rate = (m["successful_queries"] / m["total_queries"] * 100 
                       if m["total_queries"] > 0 else 0)
        
        return {
            "total_queries": m["total_queries"],
            "successful_queries": m["successful_queries"],
            "failed_queries": m["failed_queries"],
            "success_rate": success_rate,
            "average_response_time": m["avg_response_time"],
            "average_confidence_score": m["avg_confidence"],
            "emergency_detections": m["emergency_detections"]
        }
    
    def get_summary_text(self) -> str:
        """Get formatted metrics summary as text"""
        m = self.metrics
        success_rate = (m["successful_queries"] / m["total_queries"] * 100 
                       if m["total_queries"] > 0 else 0)
        
        summary = f"""
        Performance Metrics:
        • Total Queries: {m['total_queries']}
        • Success Rate: {success_rate:.1f}%
        • Avg Response Time: {m['avg_response_time']:.2f}s
        • Avg Confidence: {m['avg_confidence']:.2%}
        • Emergencies Detected: {m['emergency_detections']}
        • Failed Queries: {m['failed_queries']}
        """
        return summary.strip()
    
    def get_metrics_dict(self) -> Dict[str, Any]:
        """Get metrics as dictionary"""
        return self.metrics.copy()
    
    def to_json(self) -> str:
        """Export metrics as JSON"""
        return json.dumps(self.metrics, indent=2)
    
    def reset(self):
        """Reset all metrics to zero"""
        self.metrics = {
            "total_queries": 0,
            "successful_queries": 0,
            "failed_queries": 0,
            "total_response_time": 0.0,
            "avg_response_time": 0.0,
            "avg_confidence": 0.0,
            "emergency_detections": 0
        }
