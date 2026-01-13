#!/usr/bin/env python3
"""
Example usage demonstrations for NayDoeV1 Superior AI Assistant
This file shows various ways to use the NayDoeV1 system.
"""

from naydoev1 import NayDoeV1


def example_basic_code_analysis():
    """Example: Basic code analysis"""
    print("\n" + "=" * 70)
    print("Example 1: Basic Code Analysis")
    print("=" * 70)
    
    assistant = NayDoeV1()
    
    code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

result = factorial(5)
print(f"Factorial of 5 is {result}")
"""
    
    result = assistant.process_code(code, "python")
    
    print(f"\n✓ Analysis completed in {result['processing_time_ms']:.2f}ms")
    print(f"✓ {result['scenarios_analyzed']} scenarios analyzed")
    print(f"✓ Best scenario probability: {result['best_scenario']['probability']}")
    print(f"✓ Generated {len(result['suggestions'])} suggestions")


def example_multi_language_support():
    """Example: Processing multiple languages"""
    print("\n" + "=" * 70)
    print("Example 2: Multi-Language Support")
    print("=" * 70)
    
    assistant = NayDoeV1()
    
    code_samples = {
        "python": "def hello(): return 'Hello, World!'",
        "javascript": "function hello() { return 'Hello, World!'; }",
        "java": "public String hello() { return \"Hello, World!\"; }",
        "go": "func hello() string { return \"Hello, World!\" }"
    }
    
    for language, code in code_samples.items():
        result = assistant.process_code(code, language)
        print(f"\n{language.upper():12} - ✓ Processed in {result['processing_time_ms']:.2f}ms")


def example_rollback_markers():
    """Example: Using rollback markers"""
    print("\n" + "=" * 70)
    print("Example 3: Rollback Marker System")
    print("=" * 70)
    
    assistant = NayDoeV1()
    
    # Version 1 of the code
    code_v1 = "def add(a, b): return a + b"
    marker_v1 = assistant.create_rollback_marker(
        "Version 1 - Simple addition",
        {"calculator.py": code_v1}
    )
    print(f"\n✓ Marker V1 created: {marker_v1}")
    
    # Version 2 of the code
    code_v2 = "def add(a, b, c=0): return a + b + c"
    marker_v2 = assistant.create_rollback_marker(
        "Version 2 - Addition with optional third parameter",
        {"calculator.py": code_v2}
    )
    print(f"✓ Marker V2 created: {marker_v2}")
    
    # Version 3 of the code
    code_v3 = "def add(*args): return sum(args)"
    marker_v3 = assistant.create_rollback_marker(
        "Version 3 - Addition with variable arguments",
        {"calculator.py": code_v3}
    )
    print(f"✓ Marker V3 created: {marker_v3}")
    
    # List all markers
    markers = assistant.list_rollback_markers()
    print(f"\n✓ Total markers available: {len(markers)}")
    for marker in markers:
        print(f"  - {marker['description']} [{marker['marker_id']}]")
    
    # Rollback to version 1
    print(f"\n✓ Rolling back to V1...")
    success = assistant.rollback(marker_v1)
    print(f"  Rollback {'successful' if success else 'failed'}")


def example_realtime_suggestions():
    """Example: Real-time suggestions and warnings"""
    print("\n" + "=" * 70)
    print("Example 4: Real-time Suggestions")
    print("=" * 70)
    
    assistant = NayDoeV1()
    
    # Code with various issues
    problematic_code = """
# Long function without proper structure
def process_data(data):
    for i in range(len(data)):
        for j in range(len(data)):
            for k in range(len(data)):
                result = data[i] + data[j] + data[k]
                print(result)
    return None
""" + "\n" * 100  # Make it large
    
    result = assistant.process_code(problematic_code, "python")
    
    print(f"\n✓ Analysis completed")
    print(f"\nSuggestions ({len(result['suggestions'])}):")
    for i, suggestion in enumerate(result['suggestions'], 1):
        severity_symbol = {
            'info': 'ℹ️',
            'warning': '⚠️',
            'critical': '❌'
        }.get(suggestion['severity'], '•')
        
        print(f"\n{i}. {severity_symbol} [{suggestion['type'].upper()}]")
        print(f"   {suggestion['message']}")
        if suggestion['code_snippet']:
            print(f"   Suggestion: {suggestion['code_snippet']}")


def example_scenario_analysis():
    """Example: Exploring scenario analysis"""
    print("\n" + "=" * 70)
    print("Example 5: 40-Scenario Analysis")
    print("=" * 70)
    
    assistant = NayDoeV1()
    
    code = """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
"""
    
    result = assistant.process_code(code, "python")
    
    print(f"\n✓ TwinBrain analyzed {result['scenarios_analyzed']} scenarios")
    
    best = result['best_scenario']
    print(f"\n📊 Best Scenario:")
    print(f"   ID: {best['scenario_id']}")
    print(f"   Probability: {best['probability']:.1%}")
    print(f"   Outcome: {best['outcome']}")
    print(f"   Processing Time: {best['estimated_time_ms']:.2f}ms")
    
    print(f"\n   Risks ({len(best['risks'])}):")
    for risk in best['risks']:
        print(f"   ⚠️  {risk}")
    
    print(f"\n   Benefits ({len(best['benefits'])}):")
    for benefit in best['benefits']:
        print(f"   ✓ {benefit}")


def example_system_monitoring():
    """Example: System status and monitoring"""
    print("\n" + "=" * 70)
    print("Example 6: System Status Monitoring")
    print("=" * 70)
    
    assistant = NayDoeV1()
    
    # Process some code to generate activity
    assistant.process_code("x = 1", "python")
    assistant.create_rollback_marker("Test", {"file.py": "code"})
    
    status = assistant.get_system_status()
    
    print(f"\n🖥️  System Status: {status['status'].upper()}")
    print(f"⏱️  Uptime: {status['uptime_seconds']:.2f} seconds")
    print(f"\n📚 Knowledge Base:")
    print(f"   • Languages: {status['languages_supported']}")
    print(f"   • Patterns: {status['patterns_available']}")
    print(f"   • Algorithms: {status['algorithms_available']}")
    print(f"\n🧠 TwinBrain:")
    print(f"   • Active Scenarios: {status['active_scenarios']}")
    print(f"   • Monitoring: {'Active ✓' if status['twin_brain_monitoring'] else 'Inactive ✗'}")
    print(f"\n💾 Rollback System:")
    print(f"   • Available Markers: {status['rollback_markers']}")
    print(f"\n📡 Real-time Engine:")
    print(f"   • Suggestions Generated: {status['suggestions_generated']}")
    print(f"   • Status: {'Active ✓' if status['realtime_updates'] else 'Inactive ✗'}")


def example_workflow():
    """Example: Complete workflow"""
    print("\n" + "=" * 70)
    print("Example 7: Complete Development Workflow")
    print("=" * 70)
    
    assistant = NayDoeV1()
    
    print("\n📝 Step 1: Write initial code")
    code = "def multiply(a, b): return a * b"
    
    print("📊 Step 2: Analyze code")
    result = assistant.process_code(code, "python")
    print(f"   ✓ Analyzed in {result['processing_time_ms']:.2f}ms")
    
    print("\n💾 Step 3: Create checkpoint")
    checkpoint_id = assistant.create_rollback_marker("Initial version", {"math.py": code})
    print(f"   ✓ Checkpoint: {checkpoint_id}")
    
    print("\n🔄 Step 4: Refactor code")
    improved_code = """
def multiply(*numbers):
    '''Multiply any number of values'''
    result = 1
    for num in numbers:
        result *= num
    return result
"""
    
    print("📊 Step 5: Analyze refactored code")
    result2 = assistant.process_code(improved_code, "python")
    print(f"   ✓ Analyzed in {result2['processing_time_ms']:.2f}ms")
    print(f"   ✓ Suggestions: {len(result2['suggestions'])}")
    
    print("\n💾 Step 6: Create new checkpoint")
    checkpoint2_id = assistant.create_rollback_marker("Improved version", {"math.py": improved_code})
    print(f"   ✓ Checkpoint: {checkpoint2_id}")
    
    print("\n📋 Step 7: Review all checkpoints")
    markers = assistant.list_rollback_markers()
    print(f"   ✓ Total checkpoints: {len(markers)}")
    
    print("\n✅ Workflow complete!")


def main():
    """Run all examples"""
    print("\n" + "=" * 70)
    print(" NayDoeV1 Superior AI Assistant - Usage Examples")
    print("=" * 70)
    
    examples = [
        example_basic_code_analysis,
        example_multi_language_support,
        example_rollback_markers,
        example_realtime_suggestions,
        example_scenario_analysis,
        example_system_monitoring,
        example_workflow
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\n❌ Error in {example.__name__}: {e}")
    
    print("\n" + "=" * 70)
    print(" All examples completed!")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
