"""
Test script to verify analyzers module works correctly
Run: python -m src.analyzers.test_analyzers
"""

if __name__ == "__main__":
    print("Testing analyzers module...\n")
    
    # Test imports
    from src.analyzers import ResponseAnalyzer, analyzer, PerformanceMetrics
    print("✅ All analyzers imported successfully\n")
    
    # Test ResponseAnalyzer
    print("🧪 Testing ResponseAnalyzer:\n")
    
    # Test case 1: High confidence response
    result1 = {
        "answer": "Diabetes is a chronic metabolic disorder characterized by elevated blood glucose levels. It occurs when the pancreas doesn't produce enough insulin or when the body cannot effectively use the insulin it produces.",
        "source_documents": [
            type('obj', (object,), {
                'metadata': {'source': '/data/medical.pdf'},
                'page_content': 'Diabetes mellitus is a group of metabolic diseases...'
            })(),
            type('obj', (object,), {
                'metadata': {'source': '/data/health.pdf'},
                'page_content': 'Blood glucose regulation is essential...'
            })(),
        ]
    }
    
    confidence1 = analyzer.calculate_confidence(result1)
    label1 = analyzer.get_confidence_label(confidence1)
    print(f"✅ Test 1 - Good response:")
    print(f"   Confidence: {confidence1} - {label1}")
    
    # Test case 2: Low confidence response
    result2 = {
        "answer": "I don't have enough information about that.",
        "source_documents": []
    }
    
    confidence2 = analyzer.calculate_confidence(result2)
    label2 = analyzer.get_confidence_label(confidence2)
    print(f"\n✅ Test 2 - Uncertain response:")
    print(f"   Confidence: {confidence2} - {label2}")
    
    # Test comprehensive analysis
    analysis = analyzer.analyze_response(result1)
    print(f"\n✅ Test 3 - Comprehensive analysis:")
    print(f"   Confidence: {analysis['confidence']}")
    print(f"   Label: {analysis['confidence_label']}")
    print(f"   Source Count: {analysis['source_count']}")
    
    # Test PerformanceMetrics
    print("\n\n🧪 Testing PerformanceMetrics:\n")
    
    metrics = PerformanceMetrics()
    
    # Record some queries
    metrics.record_query(success=True, response_time=2.5, confidence=0.85)
    metrics.record_query(success=True, response_time=1.8, confidence=0.92)
    metrics.record_query(success=False, response_time=0.5)
    metrics.record_query(success=True, response_time=3.2, confidence=0.78, is_emergency=True)
    
    print("✅ Recorded 4 queries (3 success, 1 failure, 1 emergency)\n")
    
    # Get summary as text
    summary = metrics.get_summary("text")
    print("📊 Metrics Summary:")
    print(summary)
    
    # Test JSON export
    print("\n✅ JSON Export:")
    json_metrics = metrics.get_summary("json")
    print(f"   Exported {len(json_metrics)} characters")
    
    # Test metrics dict
    metrics_dict = metrics.get_summary()
    print(f"\n✅ Metrics Dictionary:")
    print(f"   Total Queries: {metrics_dict['total_queries']}")
    print(f"   Success Rate: {metrics_dict['successful_queries']}/{metrics_dict['total_queries']}")
    print(f"   Avg Response Time: {metrics_dict['avg_response_time']:.2f}s")
    print(f"   Avg Confidence: {metrics_dict['avg_confidence']:.2%}")
    
    # Test reset
    metrics.reset()
    print(f"\n✅ Reset metrics:")
    print(f"   Total Queries after reset: {metrics.get_summary()['total_queries']}")
    
    print("\n🎉 All analyzer tests passed!")
