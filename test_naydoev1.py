#!/usr/bin/env python3
"""
Test suite for NayDoeV1 Superior AI Assistant
"""

import unittest
import time
from naydoev1 import (
    NayDoeV1, KnowledgeBase, TwinBrain, RollbackSystem,
    RealtimeUpdateEngine, LanguageSupport, PatternType
)


class TestKnowledgeBase(unittest.TestCase):
    """Test the KnowledgeBase component"""
    
    def setUp(self):
        self.kb = KnowledgeBase()
    
    def test_language_support(self):
        """Test that all languages are supported"""
        self.assertEqual(len(self.kb.languages), len(LanguageSupport))
        
    def test_get_language_info(self):
        """Test getting language information"""
        info = self.kb.get_language_info("python")
        self.assertIsInstance(info, dict)
        self.assertIn("syntax", info)
        self.assertIn("best_practices", info)
    
    def test_pattern_types(self):
        """Test pattern type initialization"""
        patterns = self.kb.get_pattern_info("creational")
        self.assertIn("Singleton", patterns)
        self.assertIn("Factory", patterns)
    
    def test_algorithms_available(self):
        """Test that algorithms are available"""
        self.assertGreater(len(self.kb.algorithms), 0)
        self.assertIn("sorting", self.kb.algorithms)


class TestTwinBrain(unittest.TestCase):
    """Test the TwinBrain autonomous system"""
    
    def setUp(self):
        self.brain = TwinBrain()
    
    def test_scenario_generation(self):
        """Test that 40 scenarios are generated"""
        code = "def test(): pass"
        scenarios = self.brain.analyze_code(code, "python")
        self.assertEqual(len(scenarios), 40)
    
    def test_scenario_properties(self):
        """Test that scenarios have required properties"""
        code = "def test(): pass"
        scenarios = self.brain.analyze_code(code, "python")
        scenario = scenarios[0]
        
        self.assertIsNotNone(scenario.scenario_id)
        self.assertIsInstance(scenario.probability, float)
        self.assertGreater(scenario.probability, 0)
        self.assertLessEqual(scenario.probability, 1)
    
    def test_best_scenario_selection(self):
        """Test getting the best scenario"""
        code = "def test(): pass"
        self.brain.analyze_code(code, "python")
        best = self.brain.get_best_scenario()
        
        self.assertIsNotNone(best)
        self.assertIsInstance(best.probability, float)
    
    def test_monitoring_active(self):
        """Test that monitoring is active"""
        status = self.brain.monitor_execution()
        self.assertTrue(status["active"])
        self.assertIn("scenarios_analyzed", status)


class TestRollbackSystem(unittest.TestCase):
    """Test the Rollback System"""
    
    def setUp(self):
        self.rollback = RollbackSystem()
    
    def test_create_marker(self):
        """Test creating a rollback marker"""
        marker_id = self.rollback.create_marker(
            "Test marker",
            {"file.py": "code content"}
        )
        self.assertIsNotNone(marker_id)
        self.assertIn(marker_id, self.rollback.markers)
    
    def test_list_markers(self):
        """Test listing markers"""
        self.rollback.create_marker("Marker 1", {})
        self.rollback.create_marker("Marker 2", {})
        
        markers = self.rollback.list_markers()
        self.assertEqual(len(markers), 2)
    
    def test_rollback_to_marker(self):
        """Test rolling back to a marker"""
        self.rollback.current_state = {"version": 1}
        marker_id = self.rollback.create_marker("Before change", {})
        
        self.rollback.current_state = {"version": 2}
        
        success = self.rollback.rollback_to_marker(marker_id)
        self.assertTrue(success)
        self.assertEqual(self.rollback.current_state["version"], 1)
    
    def test_delete_marker(self):
        """Test deleting a marker"""
        marker_id = self.rollback.create_marker("To delete", {})
        success = self.rollback.delete_marker(marker_id)
        
        self.assertTrue(success)
        self.assertNotIn(marker_id, self.rollback.markers)


class TestRealtimeUpdateEngine(unittest.TestCase):
    """Test the Real-time Update Engine"""
    
    def setUp(self):
        self.engine = RealtimeUpdateEngine()
    
    def test_suggestion_generation(self):
        """Test that suggestions are generated"""
        code = "x = 1\n" * 500  # Large code block
        suggestions = self.engine.analyze_and_suggest(code, "python")
        
        self.assertGreater(len(suggestions), 0)
    
    def test_suggestion_properties(self):
        """Test suggestion object properties"""
        code = "for i in range(10): pass"
        suggestions = self.engine.analyze_and_suggest(code, "python")
        
        suggestion = suggestions[0]
        self.assertIsNotNone(suggestion.suggestion_id)
        self.assertIsNotNone(suggestion.message)
        self.assertIn(suggestion.type, ["optimization", "warning", "recommendation"])
        self.assertIn(suggestion.severity, ["info", "warning", "critical"])
    
    def test_clear_suggestions(self):
        """Test clearing suggestions"""
        self.engine.analyze_and_suggest("code", "python")
        self.assertGreater(len(self.engine.suggestions), 0)
        
        self.engine.clear_suggestions()
        self.assertEqual(len(self.engine.suggestions), 0)


class TestNayDoeV1Integration(unittest.TestCase):
    """Integration tests for the complete NayDoeV1 system"""
    
    def setUp(self):
        self.assistant = NayDoeV1()
    
    def test_system_initialization(self):
        """Test that system initializes correctly"""
        self.assertIsNotNone(self.assistant.knowledge_base)
        self.assertIsNotNone(self.assistant.twin_brain)
        self.assertIsNotNone(self.assistant.rollback_system)
        self.assertIsNotNone(self.assistant.update_engine)
    
    def test_process_code_performance(self):
        """Test that code processing is fast (milliseconds)"""
        code = "def hello(): return 'world'"
        start = time.time()
        result = self.assistant.process_code(code, "python")
        elapsed_ms = (time.time() - start) * 1000
        
        self.assertTrue(result["success"])
        self.assertLess(elapsed_ms, 5000)  # Should complete within 5 seconds
    
    def test_process_code_completeness(self):
        """Test that code processing returns complete results"""
        code = "def test(): pass"
        result = self.assistant.process_code(code, "python")
        
        self.assertIn("scenarios_analyzed", result)
        self.assertEqual(result["scenarios_analyzed"], 40)
        self.assertIn("suggestions", result)
        self.assertIn("best_scenario", result)
        self.assertIn("monitoring_status", result)
    
    def test_rollback_marker_creation(self):
        """Test creating rollback markers"""
        marker_id = self.assistant.create_rollback_marker(
            "Test checkpoint",
            {"main.py": "code"}
        )
        
        self.assertIsNotNone(marker_id)
        markers = self.assistant.list_rollback_markers()
        self.assertEqual(len(markers), 1)
    
    def test_rollback_functionality(self):
        """Test rollback functionality"""
        marker_id = self.assistant.create_rollback_marker("Checkpoint", {})
        success = self.assistant.rollback(marker_id)
        self.assertTrue(success)
    
    def test_system_status(self):
        """Test getting system status"""
        status = self.assistant.get_system_status()
        
        self.assertEqual(status["status"], "operational")
        self.assertGreater(status["languages_supported"], 0)
        self.assertGreater(status["patterns_available"], 0)
        self.assertGreater(status["algorithms_available"], 0)
        self.assertTrue(status["twin_brain_monitoring"])
        self.assertTrue(status["realtime_updates"])
    
    def test_multiple_language_support(self):
        """Test processing code in multiple languages"""
        languages = ["python", "javascript", "java"]
        
        for lang in languages:
            result = self.assistant.process_code("code", lang)
            self.assertTrue(result["success"])
            self.assertEqual(result["language"], lang)


class TestPerformanceBenchmarks(unittest.TestCase):
    """Performance benchmark tests"""
    
    def setUp(self):
        self.assistant = NayDoeV1()
    
    def test_millisecond_response_time(self):
        """Test that responses are in milliseconds"""
        code = "x = 1"
        result = self.assistant.process_code(code, "python")
        
        # Response time should be reasonable (under 2 seconds for 40 scenarios)
        self.assertLess(result["processing_time_ms"], 2000)
    
    def test_40_scenarios_generated(self):
        """Test that exactly 40 scenarios are always generated"""
        code = "def complex_function(): pass"
        result = self.assistant.process_code(code, "python")
        
        self.assertEqual(result["scenarios_analyzed"], 40)


def run_tests():
    """Run all tests"""
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == "__main__":
    run_tests()
