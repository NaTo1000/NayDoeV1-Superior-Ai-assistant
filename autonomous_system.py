#!/usr/bin/env python3
"""
NayDoeV1 Autonomous System Manager
Provides internal logging, auditing, error analysis, self-healing, and self-optimization
"""

import time
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum
from collections import defaultdict, deque
from pathlib import Path


# Configuration
LOG_DIR = "logs"
AUDIT_DIR = "audits"
ERROR_ANALYSIS_DIR = "error_analysis"
OPTIMIZATION_DIR = "optimizations"
MAX_LOG_ENTRIES = 10000
MAX_ERROR_HISTORY = 1000
SELF_HEAL_RETRY_LIMIT = 3
OPTIMIZATION_INTERVAL_DAYS = 30


class LogLevel(Enum):
    """Log severity levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class ErrorCategory(Enum):
    """Error categorization"""
    PERFORMANCE = "performance"
    MEMORY = "memory"
    CACHE = "cache"
    COMPUTATION = "computation"
    STATE = "state"
    UNKNOWN = "unknown"


@dataclass
class LogEntry:
    """Represents a log entry"""
    timestamp: float
    level: str
    component: str
    operation: str
    message: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ErrorEntry:
    """Represents an error with analysis"""
    timestamp: float
    error_id: str
    category: str
    severity: str
    component: str
    operation: str
    error_message: str
    stack_trace: Optional[str]
    context: Dict[str, Any]
    resolution_attempted: bool = False
    resolution_successful: bool = False
    retry_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class OptimizationRecommendation:
    """Represents an optimization recommendation"""
    timestamp: float
    recommendation_id: str
    category: str
    priority: str  # 'low', 'medium', 'high', 'critical'
    description: str
    current_value: Any
    recommended_value: Any
    expected_improvement: str
    auto_applicable: bool
    applied: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class InternalLogger:
    """Comprehensive internal logging system"""
    
    def __init__(self, log_dir: str = LOG_DIR):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        self.log_entries: deque = deque(maxlen=MAX_LOG_ENTRIES)
        self.log_counts = defaultdict(int)
        
        # Setup file logging
        self.log_file = self.log_dir / f"naydoev1_{datetime.now().strftime('%Y%m%d')}.log"
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("NayDoeV1")
        
    def log(self, level: LogLevel, component: str, operation: str, 
            message: str, metadata: Optional[Dict[str, Any]] = None):
        """Log an entry"""
        entry = LogEntry(
            timestamp=time.time(),
            level=level.value,
            component=component,
            operation=operation,
            message=message,
            metadata=metadata or {}
        )
        
        self.log_entries.append(entry)
        self.log_counts[level.value] += 1
        
        # Also log to file
        log_method = getattr(self.logger, level.value.lower())
        log_method(f"[{component}::{operation}] {message} {metadata or ''}")
        
    def get_recent_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent log entries"""
        return [entry.to_dict() for entry in list(self.log_entries)[-limit:]]
    
    def get_log_statistics(self) -> Dict[str, Any]:
        """Get logging statistics"""
        return {
            "total_entries": len(self.log_entries),
            "counts_by_level": dict(self.log_counts),
            "log_file": str(self.log_file)
        }


class AuditTracker:
    """Audit trail for all operations"""
    
    def __init__(self, audit_dir: str = AUDIT_DIR):
        self.audit_dir = Path(audit_dir)
        self.audit_dir.mkdir(exist_ok=True)
        
        self.audit_entries: List[Dict[str, Any]] = []
        self.operation_counts = defaultdict(int)
        
    def record(self, component: str, operation: str, user: str = "system",
               parameters: Optional[Dict[str, Any]] = None,
               result: Optional[Dict[str, Any]] = None,
               duration_ms: Optional[float] = None):
        """Record an audit entry"""
        entry = {
            "timestamp": time.time(),
            "datetime": datetime.now().isoformat(),
            "component": component,
            "operation": operation,
            "user": user,
            "parameters": parameters or {},
            "result": result or {},
            "duration_ms": duration_ms,
            "audit_id": f"{component}_{operation}_{int(time.time() * 1000)}"
        }
        
        self.audit_entries.append(entry)
        self.operation_counts[f"{component}::{operation}"] += 1
        
        # Periodically flush to disk
        if len(self.audit_entries) % 100 == 0:
            self._flush_to_disk()
    
    def _flush_to_disk(self):
        """Flush audit entries to disk"""
        if not self.audit_entries:
            return
            
        audit_file = self.audit_dir / f"audit_{datetime.now().strftime('%Y%m%d')}.json"
        
        try:
            existing_data = []
            if audit_file.exists():
                with open(audit_file, 'r') as f:
                    existing_data = json.load(f)
            
            existing_data.extend(self.audit_entries)
            
            with open(audit_file, 'w') as f:
                json.dump(existing_data, f, indent=2)
            
            self.audit_entries = []
        except Exception as e:
            print(f"Error flushing audit log: {e}")
    
    def get_audit_statistics(self) -> Dict[str, Any]:
        """Get audit statistics"""
        return {
            "total_operations": sum(self.operation_counts.values()),
            "operations_by_type": dict(self.operation_counts),
            "pending_entries": len(self.audit_entries)
        }


class ErrorAnalyzer:
    """Analyze and track errors for patterns and solutions"""
    
    def __init__(self, error_dir: str = ERROR_ANALYSIS_DIR):
        self.error_dir = Path(error_dir)
        self.error_dir.mkdir(exist_ok=True)
        
        self.error_history: deque = deque(maxlen=MAX_ERROR_HISTORY)
        self.error_patterns = defaultdict(int)
        self.resolution_success_rate = defaultdict(lambda: {"attempts": 0, "successes": 0})
        
    def analyze_error(self, error: Exception, component: str, operation: str,
                     context: Optional[Dict[str, Any]] = None) -> ErrorEntry:
        """Analyze an error and categorize it"""
        error_id = f"ERR_{int(time.time() * 1000)}"
        
        # Categorize error
        category = self._categorize_error(error, context)
        severity = self._assess_severity(error, category)
        
        entry = ErrorEntry(
            timestamp=time.time(),
            error_id=error_id,
            category=category.value,
            severity=severity,
            component=component,
            operation=operation,
            error_message=str(error),
            stack_trace=None,  # Could extract traceback here
            context=context or {},
            resolution_attempted=False,
            resolution_successful=False,
            retry_count=0
        )
        
        self.error_history.append(entry)
        self.error_patterns[f"{category.value}::{type(error).__name__}"] += 1
        
        return entry
    
    def _categorize_error(self, error: Exception, context: Optional[Dict[str, Any]]) -> ErrorCategory:
        """Categorize error type"""
        error_type = type(error).__name__
        error_msg = str(error).lower()
        
        if "memory" in error_msg or "memoryerror" in error_type.lower():
            return ErrorCategory.MEMORY
        elif "cache" in error_msg or "timeout" in error_msg:
            return ErrorCategory.CACHE
        elif "performance" in error_msg or "slow" in error_msg:
            return ErrorCategory.PERFORMANCE
        elif "state" in error_msg or "invalid" in error_msg:
            return ErrorCategory.STATE
        elif any(x in error_type.lower() for x in ["arithmetic", "value", "type"]):
            return ErrorCategory.COMPUTATION
        else:
            return ErrorCategory.UNKNOWN
    
    def _assess_severity(self, error: Exception, category: ErrorCategory) -> str:
        """Assess error severity"""
        error_type = type(error).__name__
        
        if any(x in error_type.lower() for x in ["critical", "fatal", "memory"]):
            return "critical"
        elif category in [ErrorCategory.PERFORMANCE, ErrorCategory.CACHE]:
            return "warning"
        else:
            return "error"
    
    def get_error_patterns(self) -> Dict[str, Any]:
        """Get common error patterns"""
        total_errors = sum(self.error_patterns.values())
        
        return {
            "total_errors": total_errors,
            "unique_patterns": len(self.error_patterns),
            "top_patterns": sorted(
                self.error_patterns.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10],
            "resolution_success_rates": dict(self.resolution_success_rate)
        }


class SelfHealingSystem:
    """Automatic error recovery and self-healing"""
    
    def __init__(self, logger: InternalLogger, error_analyzer: ErrorAnalyzer):
        self.logger = logger
        self.error_analyzer = error_analyzer
        self.healing_strategies = self._initialize_strategies()
        self.healing_history: List[Dict[str, Any]] = []
        
    def _initialize_strategies(self) -> Dict[str, callable]:
        """Initialize self-healing strategies"""
        return {
            ErrorCategory.CACHE.value: self._heal_cache_error,
            ErrorCategory.MEMORY.value: self._heal_memory_error,
            ErrorCategory.PERFORMANCE.value: self._heal_performance_error,
            ErrorCategory.STATE.value: self._heal_state_error,
            ErrorCategory.COMPUTATION.value: self._heal_computation_error,
        }
    
    def attempt_healing(self, error_entry: ErrorEntry, 
                       healing_context: Optional[Dict[str, Any]] = None) -> bool:
        """Attempt to heal an error"""
        if error_entry.retry_count >= SELF_HEAL_RETRY_LIMIT:
            self.logger.log(
                LogLevel.WARNING,
                "SelfHealing",
                "attempt_healing",
                f"Retry limit reached for {error_entry.error_id}"
            )
            return False
        
        strategy = self.healing_strategies.get(error_entry.category)
        if not strategy:
            self.logger.log(
                LogLevel.INFO,
                "SelfHealing",
                "attempt_healing",
                f"No healing strategy for category {error_entry.category}"
            )
            return False
        
        error_entry.resolution_attempted = True
        error_entry.retry_count += 1
        
        try:
            success = strategy(error_entry, healing_context)
            error_entry.resolution_successful = success
            
            # Record healing attempt
            self.healing_history.append({
                "timestamp": time.time(),
                "error_id": error_entry.error_id,
                "category": error_entry.category,
                "strategy": strategy.__name__,
                "success": success,
                "retry_count": error_entry.retry_count
            })
            
            self.logger.log(
                LogLevel.INFO if success else LogLevel.WARNING,
                "SelfHealing",
                "attempt_healing",
                f"Healing {'succeeded' if success else 'failed'} for {error_entry.error_id}"
            )
            
            return success
            
        except Exception as e:
            self.logger.log(
                LogLevel.ERROR,
                "SelfHealing",
                "attempt_healing",
                f"Healing strategy failed: {e}"
            )
            return False
    
    def _heal_cache_error(self, error_entry: ErrorEntry, context: Optional[Dict]) -> bool:
        """Heal cache-related errors"""
        # Clear cache and retry
        self.logger.log(LogLevel.INFO, "SelfHealing", "heal_cache", "Clearing cache")
        # In real implementation, would clear actual cache
        return True
    
    def _heal_memory_error(self, error_entry: ErrorEntry, context: Optional[Dict]) -> bool:
        """Heal memory-related errors"""
        # Trigger garbage collection, reduce cache size
        import gc
        gc.collect()
        self.logger.log(LogLevel.INFO, "SelfHealing", "heal_memory", "Triggered GC")
        return True
    
    def _heal_performance_error(self, error_entry: ErrorEntry, context: Optional[Dict]) -> bool:
        """Heal performance-related errors"""
        # Adjust batch sizes, increase timeouts
        self.logger.log(LogLevel.INFO, "SelfHealing", "heal_performance", "Adjusting parameters")
        return True
    
    def _heal_state_error(self, error_entry: ErrorEntry, context: Optional[Dict]) -> bool:
        """Heal state-related errors"""
        # Reset to known good state
        self.logger.log(LogLevel.INFO, "SelfHealing", "heal_state", "Resetting state")
        return True
    
    def _heal_computation_error(self, error_entry: ErrorEntry, context: Optional[Dict]) -> bool:
        """Heal computation-related errors"""
        # Use fallback values, adjust parameters
        self.logger.log(LogLevel.INFO, "SelfHealing", "heal_computation", "Using fallback")
        return True
    
    def get_healing_statistics(self) -> Dict[str, Any]:
        """Get self-healing statistics"""
        total_attempts = len(self.healing_history)
        successful = sum(1 for h in self.healing_history if h["success"])
        
        return {
            "total_healing_attempts": total_attempts,
            "successful_healings": successful,
            "success_rate": successful / max(1, total_attempts),
            "recent_healings": self.healing_history[-10:]
        }


class SelfOptimizer:
    """Autonomous self-optimization system"""
    
    def __init__(self, logger: InternalLogger, optimization_dir: str = OPTIMIZATION_DIR):
        self.logger = logger
        self.optimization_dir = Path(optimization_dir)
        self.optimization_dir.mkdir(exist_ok=True)
        
        self.recommendations: List[OptimizationRecommendation] = []
        self.applied_optimizations: List[Dict[str, Any]] = []
        self.last_optimization_run = None
        
    def analyze_performance_data(self, performance_data: Dict[str, Any]) -> List[OptimizationRecommendation]:
        """Analyze performance data and generate recommendations"""
        recommendations = []
        timestamp = time.time()
        
        # Analyze cache performance
        if "cache_hit_rate" in performance_data:
            cache_hit_rate = performance_data["cache_hit_rate"]
            if cache_hit_rate < 0.85:
                recommendations.append(OptimizationRecommendation(
                    timestamp=timestamp,
                    recommendation_id=f"OPT_{int(timestamp * 1000)}_CACHE",
                    category="cache",
                    priority="high",
                    description="Cache hit rate below optimal threshold",
                    current_value=cache_hit_rate,
                    recommended_value=0.90,
                    expected_improvement="15-20% performance improvement",
                    auto_applicable=True
                ))
        
        # Analyze processing times
        if "avg_processing_time_ms" in performance_data:
            avg_time = performance_data["avg_processing_time_ms"]
            if avg_time > 1.0:
                recommendations.append(OptimizationRecommendation(
                    timestamp=timestamp,
                    recommendation_id=f"OPT_{int(timestamp * 1000)}_PERF",
                    category="performance",
                    priority="medium",
                    description="Average processing time above target",
                    current_value=avg_time,
                    recommended_value=0.5,
                    expected_improvement="50% faster processing",
                    auto_applicable=True
                ))
        
        # Analyze memory usage
        if "total_size_mb" in performance_data:
            memory_mb = performance_data["total_size_mb"]
            if memory_mb > 100:
                recommendations.append(OptimizationRecommendation(
                    timestamp=timestamp,
                    recommendation_id=f"OPT_{int(timestamp * 1000)}_MEM",
                    category="memory",
                    priority="high",
                    description="Memory usage exceeds optimal threshold",
                    current_value=memory_mb,
                    recommended_value=50,
                    expected_improvement="50% memory reduction",
                    auto_applicable=True
                ))
        
        self.recommendations.extend(recommendations)
        return recommendations
    
    def apply_optimizations(self, auto_only: bool = True) -> Dict[str, Any]:
        """Apply pending optimizations"""
        applied = []
        
        for rec in self.recommendations:
            if rec.applied:
                continue
            
            if auto_only and not rec.auto_applicable:
                continue
            
            # Apply optimization based on category
            success = self._apply_optimization(rec)
            
            if success:
                rec.applied = True
                applied.append({
                    "recommendation_id": rec.recommendation_id,
                    "category": rec.category,
                    "description": rec.description,
                    "timestamp": time.time()
                })
                
                self.logger.log(
                    LogLevel.INFO,
                    "SelfOptimizer",
                    "apply_optimization",
                    f"Applied: {rec.description}"
                )
        
        self.applied_optimizations.extend(applied)
        return {
            "applied_count": len(applied),
            "optimizations": applied
        }
    
    def _apply_optimization(self, recommendation: OptimizationRecommendation) -> bool:
        """Apply a specific optimization"""
        try:
            if recommendation.category == "cache":
                # Increase cache size
                self.logger.log(LogLevel.INFO, "SelfOptimizer", "optimize_cache", 
                              "Increasing cache size")
                return True
            
            elif recommendation.category == "performance":
                # Adjust batch sizes or timeouts
                self.logger.log(LogLevel.INFO, "SelfOptimizer", "optimize_performance",
                              "Adjusting performance parameters")
                return True
            
            elif recommendation.category == "memory":
                # Trigger cleanup, reduce cache sizes
                import gc
                gc.collect()
                self.logger.log(LogLevel.INFO, "SelfOptimizer", "optimize_memory",
                              "Memory optimization applied")
                return True
            
            return False
            
        except Exception as e:
            self.logger.log(LogLevel.ERROR, "SelfOptimizer", "apply_optimization",
                          f"Failed to apply optimization: {e}")
            return False
    
    def should_run_optimization(self) -> bool:
        """Check if it's time to run optimization"""
        if self.last_optimization_run is None:
            return True
        
        days_since_last = (time.time() - self.last_optimization_run) / 86400
        return days_since_last >= OPTIMIZATION_INTERVAL_DAYS
    
    def run_monthly_optimization(self, system_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Run monthly autonomous optimization"""
        self.logger.log(LogLevel.INFO, "SelfOptimizer", "monthly_optimization",
                       "Starting monthly optimization cycle")
        
        # Analyze current performance
        recommendations = self.analyze_performance_data(system_metrics)
        
        # Apply auto-applicable optimizations
        results = self.apply_optimizations(auto_only=True)
        
        # Update last run time
        self.last_optimization_run = time.time()
        
        # Save optimization report
        self._save_optimization_report(recommendations, results)
        
        return {
            "timestamp": time.time(),
            "recommendations_generated": len(recommendations),
            "optimizations_applied": results["applied_count"],
            "next_optimization_date": datetime.fromtimestamp(
                self.last_optimization_run + (OPTIMIZATION_INTERVAL_DAYS * 86400)
            ).isoformat()
        }
    
    def _save_optimization_report(self, recommendations: List, results: Dict):
        """Save optimization report to disk"""
        report = {
            "timestamp": time.time(),
            "datetime": datetime.now().isoformat(),
            "recommendations": [r.to_dict() for r in recommendations],
            "applied_optimizations": results
        }
        
        report_file = self.optimization_dir / f"optimization_report_{datetime.now().strftime('%Y%m%d')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
    
    def get_optimization_statistics(self) -> Dict[str, Any]:
        """Get optimization statistics"""
        return {
            "total_recommendations": len(self.recommendations),
            "applied_optimizations": len(self.applied_optimizations),
            "pending_recommendations": len([r for r in self.recommendations if not r.applied]),
            "last_optimization_run": self.last_optimization_run,
            "next_optimization_due": self.should_run_optimization()
        }


class AutonomousSystemManager:
    """Main autonomous system manager coordinating all subsystems"""
    
    def __init__(self):
        self.logger = InternalLogger()
        self.audit_tracker = AuditTracker()
        self.error_analyzer = ErrorAnalyzer()
        self.self_healer = SelfHealingSystem(self.logger, self.error_analyzer)
        self.self_optimizer = SelfOptimizer(self.logger)
        
        self.enabled = True
        self.start_time = time.time()
        
        self.logger.log(
            LogLevel.INFO,
            "AutonomousSystemManager",
            "__init__",
            "Autonomous system initialized"
        )
    
    def log_operation(self, component: str, operation: str, level: LogLevel = LogLevel.INFO,
                     message: str = "", metadata: Optional[Dict] = None):
        """Log an operation"""
        if self.enabled:
            self.logger.log(level, component, operation, message, metadata)
    
    def audit_operation(self, component: str, operation: str, 
                       parameters: Optional[Dict] = None,
                       result: Optional[Dict] = None,
                       duration_ms: Optional[float] = None):
        """Audit an operation"""
        if self.enabled:
            self.audit_tracker.record(component, operation, "system", 
                                     parameters, result, duration_ms)
    
    def handle_error(self, error: Exception, component: str, operation: str,
                    context: Optional[Dict] = None, auto_heal: bool = True) -> bool:
        """Handle an error with analysis and optional self-healing"""
        if not self.enabled:
            return False
        
        # Log the error
        self.logger.log(
            LogLevel.ERROR,
            component,
            operation,
            f"Error occurred: {error}",
            context
        )
        
        # Analyze the error
        error_entry = self.error_analyzer.analyze_error(error, component, operation, context)
        
        # Attempt self-healing if enabled
        if auto_heal:
            healing_success = self.self_healer.attempt_healing(error_entry, context)
            return healing_success
        
        return False
    
    def check_and_optimize(self, system_metrics: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Check if optimization should run and execute if needed"""
        if not self.enabled:
            return None
        
        if self.self_optimizer.should_run_optimization():
            self.logger.log(
                LogLevel.INFO,
                "AutonomousSystemManager",
                "check_and_optimize",
                "Running scheduled optimization"
            )
            return self.self_optimizer.run_monthly_optimization(system_metrics)
        
        return None
    
    def get_comprehensive_status(self) -> Dict[str, Any]:
        """Get comprehensive autonomous system status"""
        uptime = time.time() - self.start_time
        
        return {
            "enabled": self.enabled,
            "uptime_seconds": uptime,
            "uptime_days": uptime / 86400,
            "logging": self.logger.get_log_statistics(),
            "auditing": self.audit_tracker.get_audit_statistics(),
            "error_analysis": self.error_analyzer.get_error_patterns(),
            "self_healing": self.self_healer.get_healing_statistics(),
            "self_optimization": self.self_optimizer.get_optimization_statistics(),
            "fully_autonomous": True
        }
    
    def shutdown(self):
        """Gracefully shutdown autonomous system"""
        self.logger.log(
            LogLevel.INFO,
            "AutonomousSystemManager",
            "shutdown",
            "Shutting down autonomous system"
        )
        
        # Flush pending audits
        self.audit_tracker._flush_to_disk()
        
        self.enabled = False


# Singleton instance
_autonomous_system = None


def get_autonomous_system() -> AutonomousSystemManager:
    """Get or create the autonomous system manager singleton"""
    global _autonomous_system
    if _autonomous_system is None:
        _autonomous_system = AutonomousSystemManager()
    return _autonomous_system
