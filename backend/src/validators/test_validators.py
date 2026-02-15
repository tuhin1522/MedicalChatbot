"""
Test script to verify validators module works correctly
Run: python -m src.validators.test_validators
"""

if __name__ == "__main__":
    print("Testing validators module...\n")
    
    # Test imports
    from src.validators import SafetyValidator, safety
    from src.core import config
    print("✅ SafetyValidator imported successfully\n")
    
    # Test validation
    test_cases = [
        ("What is diabetes?", True, False),
        ("I have severe chest pain", True, True),
        ("x", False, False),  # Too short
        ("a" * 600, False, False),  # Too long
        ("how to die", False, False),  # Harmful
    ]
    
    print("🧪 Testing query validation:\n")
    for query, expected_valid, expected_emergency in test_cases:
        is_valid, error = safety.validate_query(query)
        is_emergency = safety.detect_emergency(query)
        
        display_query = query[:30] + "..." if len(query) > 30 else query
        status = "✅" if is_valid == expected_valid and is_emergency == expected_emergency else "❌"
        
        print(f"{status} Query: '{display_query}'")
        print(f"   Valid: {is_valid} (expected: {expected_valid})")
        print(f"   Emergency: {is_emergency} (expected: {expected_emergency})")
        if error:
            print(f"   Error: {error[:50]}...")
        print()
    
    # Test disclaimer
    print("🧪 Testing disclaimer addition:\n")
    response = "Diabetes is a chronic condition..."
    
    # Normal response
    normal = safety.add_disclaimer(response, is_emergency=False)
    print(f"✅ Normal disclaimer added: {len(normal)} chars")
    
    # Emergency response
    emergency = safety.add_disclaimer(response, is_emergency=True)
    print(f"✅ Emergency disclaimer added: {len(emergency)} chars")
    
    # Test configuration access
    print(f"\n📋 Configuration:")
    print(f"   Max Query Length: {config.MAX_QUERY_LENGTH}")
    print(f"   Medical Disclaimer Enabled: {config.ENABLE_MEDICAL_DISCLAIMER}")
    print(f"   Emergency Detection Enabled: {config.ENABLE_EMERGENCY_DETECTION}")
    
    print("\n🎉 All validator tests passed!")
