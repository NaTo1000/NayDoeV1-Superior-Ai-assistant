#!/usr/bin/env python3
"""
Autonomous System Demonstration
Shows logging, auditing, error analysis, self-healing, and self-optimization
"""

import time
from naydoev1 import NayDoeV1
from autonomous_system import get_autonomous_system


def print_header(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def demo_logging_and_auditing():
    """Demonstrate logging and auditing capabilities"""
    print_header("📝 Logging & Auditing")
    
    assistant = NayDoeV1(enable_autonomous=True)
    
    print("\n🔍 Performing operations with automatic logging...")
    
    # Process some code
    assistant.process_code("def test(): pass", "python")
    assistant.process_code("function hello() {}", "javascript")
    
    # Create markers
    assistant.create_rollback_marker("Test 1", {"file.py": "code"})
    assistant.create_rollback_marker("Test 2", {"file.js": "code"})
    
    # Get status
    status = assistant.get_system_status()
    auto_status = status["autonomous_system"]
    
    print(f"\n📊 Logging Statistics:")
    logging = auto_status["logging"]
    print(f"   • Total log entries: {logging['total_entries']}")
    print(f"   • Log counts by level:")
    for level, count in logging["counts_by_level"].items():
        print(f"      - {level}: {count}")
    
    print(f"\n📋 Audit Statistics:")
    auditing = auto_status["auditing"]
    print(f"   • Total operations: {auditing['total_operations']}")
    print(f"   • Operations by type:")
    for op_type, count in list(auditing["operations_by_type"].items())[:3]:
        print(f"      - {op_type}: {count}")


def demo_error_analysis():
    """Demonstrate error analysis capabilities"""
    print_header("🔍 Error Analysis")
    
    assistant = NayDoeV1(enable_autonomous=True)
    autonomous = get_autonomous_system()
    
    print("\n⚠️  Simulating various errors...")
    
    # Simulate different error types
    class CacheError(Exception):
        pass
    
    class MemoryError(Exception):
        pass
    
    # Analyze errors
    error1 = CacheError("Cache timeout")
    error_entry1 = autonomous.error_analyzer.analyze_error(
        error1, "CacheSystem", "get_data", {"key": "test"}
    )
    print(f"   • Cache error categorized as: {error_entry1.category}")
    print(f"     Severity: {error_entry1.severity}")
    
    error2 = MemoryError("Out of memory")
    error_entry2 = autonomous.error_analyzer.analyze_error(
        error2, "MemoryManager", "allocate", {"size": 1000000}
    )
    print(f"   • Memory error categorized as: {error_entry2.category}")
    print(f"     Severity: {error_entry2.severity}")
    
    # Get error patterns
    patterns = autonomous.error_analyzer.get_error_patterns()
    print(f"\n📈 Error Pattern Analysis:")
    print(f"   • Total errors tracked: {patterns['total_errors']}")
    print(f"   • Unique patterns: {patterns['unique_patterns']}")


def demo_self_healing():
    """Demonstrate self-healing capabilities"""
    print_header("🔧 Self-Healing System")
    
    assistant = NayDoeV1(enable_autonomous=True)
    autonomous = get_autonomous_system()
    
    print("\n🩹 Testing automatic error recovery...")
    
    # Simulate errors and healing
    class CacheTimeoutError(Exception):
        pass
    
    error = CacheTimeoutError("Cache operation timed out")
    error_entry = autonomous.error_analyzer.analyze_error(
        error, "CacheSystem", "fetch", {"timeout": 30}
    )
    
    print(f"   • Error detected: {error_entry.error_message}")
    print(f"   • Category: {error_entry.category}")
    
    # Attempt healing
    healing_success = autonomous.self_healer.attempt_healing(
        error_entry,
        {"retry_count": 0}
    )
    
    print(f"   • Healing attempted: {error_entry.resolution_attempted}")
    print(f"   • Healing successful: {healing_success}")
    print(f"   • Retry count: {error_entry.retry_count}")
    
    # Get healing statistics
    healing_stats = autonomous.self_healer.get_healing_statistics()
    print(f"\n📊 Self-Healing Statistics:")
    print(f"   • Total healing attempts: {healing_stats['total_healing_attempts']}")
    print(f"   • Successful healings: {healing_stats['successful_healings']}")
    print(f"   • Success rate: {healing_stats['success_rate']:.1%}")


def demo_self_optimization():
    """Demonstrate self-optimization capabilities"""
    print_header("⚡ Self-Optimization System")
    
    assistant = NayDoeV1(enable_autonomous=True)
    autonomous = get_autonomous_system()
    
    print("\n🔄 Analyzing system performance...")
    
    # Simulate some operations to generate metrics
    for i in range(5):
        assistant.process_code(f"def func{i}(): pass", "python")
    
    # Get system metrics
    status = assistant.get_system_status()
    
    # Analyze performance
    performance_data = {
        "cache_hit_rate": status["performance_metrics"]["cache_hits"] / 
                         max(1, status["performance_metrics"]["cache_hits"] + 
                         status["performance_metrics"]["cache_misses"]),
        "avg_processing_time_ms": status["performance_metrics"]["average_processing_time_ms"],
        "total_size_mb": status["rollback_efficiency"]["total_size_mb"]
    }
    
    print(f"\n📊 Current Performance:")
    print(f"   • Cache hit rate: {performance_data['cache_hit_rate']:.1%}")
    print(f"   • Avg processing time: {performance_data['avg_processing_time_ms']:.2f}ms")
    print(f"   • Memory usage: {performance_data['total_size_mb']:.2f}MB")
    
    # Generate recommendations
    recommendations = autonomous.self_optimizer.analyze_performance_data(performance_data)
    
    print(f"\n💡 Optimization Recommendations:")
    for rec in recommendations:
        print(f"   • [{rec.priority.upper()}] {rec.description}")
        print(f"     Current: {rec.current_value}, Recommended: {rec.recommended_value}")
        print(f"     Expected improvement: {rec.expected_improvement}")
        print(f"     Auto-applicable: {rec.auto_applicable}")
    
    if recommendations:
        # Apply optimizations
        print(f"\n⚙️  Applying auto-applicable optimizations...")
        results = autonomous.self_optimizer.apply_optimizations(auto_only=True)
        print(f"   • Applied {results['applied_count']} optimizations")


def demo_monthly_optimization():
    """Demonstrate monthly optimization cycle"""
    print_header("📅 Monthly Autonomous Optimization")
    
    assistant = NayDoeV1(enable_autonomous=True)
    autonomous = get_autonomous_system()
    
    print("\n🔄 Checking optimization schedule...")
    
    # Check if optimization is due
    optimizer = autonomous.self_optimizer
    should_run = optimizer.should_run_optimization()
    
    print(f"   • Optimization due: {should_run}")
    
    if should_run or optimizer.last_optimization_run is None:
        print(f"\n⚡ Running monthly optimization cycle...")
        
        # Run optimization
        system_metrics = assistant.get_system_status()
        result = optimizer.run_monthly_optimization(system_metrics)
        
        print(f"\n✅ Optimization Complete:")
        print(f"   • Timestamp: {result['timestamp']}")
        print(f"   • Recommendations generated: {result['recommendations_generated']}")
        print(f"   • Optimizations applied: {result['optimizations_applied']}")
        print(f"   • Next optimization: {result['next_optimization_date']}")
    else:
        print(f"   • Next optimization not yet due")


def demo_comprehensive_status():
    """Show comprehensive autonomous system status"""
    print_header("📊 Comprehensive System Status")
    
    assistant = NayDoeV1(enable_autonomous=True)
    
    # Perform some operations
    for i in range(3):
        assistant.process_code(f"code{i}", "python")
    
    assistant.create_rollback_marker("Status demo", {"file.py": "code"})
    
    # Get full status
    status = assistant.get_system_status()
    auto_status = status["autonomous_system"]
    
    print(f"\n🖥️  System Overview:")
    print(f"   • Status: Operational")
    print(f"   • Uptime: {auto_status['uptime_days']:.2f} days")
    print(f"   • Fully Autonomous: {auto_status['fully_autonomous']}")
    
    print(f"\n📝 Logging:")
    logging = auto_status["logging"]
    print(f"   • Total entries: {logging['total_entries']}")
    for level, count in logging["counts_by_level"].items():
        print(f"   • {level}: {count}")
    
    print(f"\n📋 Auditing:")
    auditing = auto_status["auditing"]
    print(f"   • Total operations: {auditing['total_operations']}")
    print(f"   • Pending entries: {auditing['pending_entries']}")
    
    print(f"\n🔍 Error Analysis:")
    errors = auto_status["error_analysis"]
    print(f"   • Total errors: {errors['total_errors']}")
    print(f"   • Unique patterns: {errors['unique_patterns']}")
    
    print(f"\n🩹 Self-Healing:")
    healing = auto_status["self_healing"]
    print(f"   • Total attempts: {healing['total_healing_attempts']}")
    print(f"   • Successful: {healing['successful_healings']}")
    print(f"   • Success rate: {healing['success_rate']:.1%}")
    
    print(f"\n⚡ Self-Optimization:")
    optimization = auto_status["self_optimization"]
    print(f"   • Total recommendations: {optimization['total_recommendations']}")
    print(f"   • Applied optimizations: {optimization['applied_optimizations']}")
    print(f"   • Pending: {optimization['pending_recommendations']}")
    print(f"   • Next optimization due: {optimization['next_optimization_due']}")


def main():
    """Run all autonomous system demos"""
    print("\n" + "=" * 70)
    print(" NayDoeV1 Autonomous System Demonstration")
    print("=" * 70)
    
    try:
        demo_logging_and_auditing()
        time.sleep(0.5)
        
        demo_error_analysis()
        time.sleep(0.5)
        
        demo_self_healing()
        time.sleep(0.5)
        
        demo_self_optimization()
        time.sleep(0.5)
        
        demo_monthly_optimization()
        time.sleep(0.5)
        
        demo_comprehensive_status()
        
        print("\n" + "=" * 70)
        print(" ✨ Autonomous System Demonstration Complete!")
        print(" 🤖 System is fully autonomous with self-healing and optimization")
        print("=" * 70)
        print()
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        raise


if __name__ == "__main__":
    main()
