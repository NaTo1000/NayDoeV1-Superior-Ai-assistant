# NayDoeV1 API Documentation

## Table of Contents
1. [Main Classes](#main-classes)
2. [Core Components](#core-components)
3. [Data Structures](#data-structures)
4. [Usage Examples](#usage-examples)

---

## Main Classes

### NayDoeV1

Main orchestrator class integrating all system components.

#### Methods

##### `__init__()`
Initialize the NayDoeV1 system with all components.

```python
assistant = NayDoeV1()
```

##### `process_code(code: str, language: str) -> Dict[str, Any]`
Process code with full NayDoeV1 capabilities including scenario analysis and suggestions.

**Parameters:**
- `code` (str): The source code to analyze
- `language` (str): Programming language (python, javascript, java, etc.)

**Returns:**
- Dictionary containing:
  - `success` (bool): Whether processing succeeded
  - `processing_time_ms` (float): Time taken in milliseconds
  - `language` (str): Language processed
  - `scenarios_analyzed` (int): Number of scenarios generated
  - `best_scenario` (dict): Highest probability scenario
  - `suggestions` (list): Real-time suggestions
  - `warnings` (list): Critical warnings
  - `monitoring_status` (dict): TwinBrain status

**Example:**
```python
result = assistant.process_code("def hello(): pass", "python")
print(f"Processed in {result['processing_time_ms']}ms")
```

##### `create_rollback_marker(description: str, code_state: Dict[str, str]) -> str`
Create a rollback marker for the current state.

**Parameters:**
- `description` (str): Human-readable description of the marker
- `code_state` (dict): Dictionary mapping file paths to code content

**Returns:**
- `marker_id` (str): Unique identifier for the created marker

**Example:**
```python
marker_id = assistant.create_rollback_marker(
    "Before refactoring",
    {"main.py": code_content}
)
```

##### `rollback(marker_id: str) -> bool`
Rollback system state to a specific marker.

**Parameters:**
- `marker_id` (str): ID of the marker to rollback to

**Returns:**
- `success` (bool): Whether rollback succeeded

**Example:**
```python
success = assistant.rollback(marker_id)
```

##### `list_rollback_markers() -> List[Dict[str, Any]]`
List all available rollback markers.

**Returns:**
- List of dictionaries containing marker information:
  - `marker_id` (str): Unique marker identifier
  - `timestamp` (str): ISO format timestamp
  - `description` (str): Marker description

**Example:**
```python
markers = assistant.list_rollback_markers()
for marker in markers:
    print(f"{marker['description']} - {marker['timestamp']}")
```

##### `get_system_status() -> Dict[str, Any]`
Get comprehensive system status.

**Returns:**
- Dictionary containing:
  - `status` (str): System operational status
  - `uptime_seconds` (float): System uptime
  - `languages_supported` (int): Number of supported languages
  - `patterns_available` (int): Number of design patterns
  - `algorithms_available` (int): Number of algorithms
  - `active_scenarios` (int): Currently active scenarios
  - `rollback_markers` (int): Number of rollback markers
  - `suggestions_generated` (int): Total suggestions generated
  - `twin_brain_monitoring` (bool): TwinBrain status
  - `realtime_updates` (bool): Real-time engine status

**Example:**
```python
status = assistant.get_system_status()
print(f"System: {status['status']}")
```

---

## Core Components

### KnowledgeBase

Comprehensive knowledge base for languages, patterns, and algorithms.

#### Methods

##### `get_language_info(language: str) -> Dict[str, Any]`
Get comprehensive information about a programming language.

**Parameters:**
- `language` (str): Language identifier

**Returns:**
- Dictionary containing language data:
  - `syntax` (dict): Syntax information
  - `best_practices` (list): Best practices
  - `common_pitfalls` (list): Common mistakes
  - `libraries` (list): Popular libraries
  - `frameworks` (list): Available frameworks
  - `versions` (list): Version information

##### `get_pattern_info(pattern_type: str) -> List[str]`
Get design patterns of a specific type.

**Parameters:**
- `pattern_type` (str): Type of pattern (creational, structural, behavioral, concurrency)

**Returns:**
- List of pattern names

---

### TwinBrain

Autonomous monitoring and parallel scenario planning system.

#### Methods

##### `analyze_code(code: str, language: str) -> List[Scenario]`
Analyze code and generate 40 different optimization scenarios.

**Parameters:**
- `code` (str): Source code to analyze
- `language` (str): Programming language

**Returns:**
- List of 40 Scenario objects

##### `get_best_scenario() -> Optional[Scenario]`
Get the scenario with the highest probability of success.

**Returns:**
- Scenario object or None if no scenarios available

##### `monitor_execution() -> Dict[str, Any]`
Monitor system execution and return current status.

**Returns:**
- Dictionary containing monitoring data:
  - `active` (bool): Whether monitoring is active
  - `scenarios_analyzed` (int): Number of scenarios
  - `best_scenario_probability` (float): Best scenario probability
  - `timestamp` (float): Current timestamp

---

### RollbackSystem

System for managing rollback markers and state restoration.

#### Methods

##### `create_marker(description: str, code_state: Dict[str, str]) -> str`
Create a new rollback marker.

**Parameters:**
- `description` (str): Marker description
- `code_state` (dict): Code snapshot

**Returns:**
- `marker_id` (str): Unique marker identifier

##### `rollback_to_marker(marker_id: str) -> bool`
Restore system to a specific marker state.

**Parameters:**
- `marker_id` (str): Target marker ID

**Returns:**
- `success` (bool): Whether rollback succeeded

##### `list_markers() -> List[Dict[str, Any]]`
Get list of all available markers.

**Returns:**
- List of marker information dictionaries

##### `get_marker(marker_id: str) -> Optional[RollbackMarker]`
Get a specific marker by ID.

**Parameters:**
- `marker_id` (str): Marker identifier

**Returns:**
- RollbackMarker object or None

##### `delete_marker(marker_id: str) -> bool`
Delete a specific marker.

**Parameters:**
- `marker_id` (str): Marker to delete

**Returns:**
- `success` (bool): Whether deletion succeeded

---

### RealtimeUpdateEngine

Engine for providing real-time updates, suggestions, and warnings.

#### Methods

##### `analyze_and_suggest(code: str, language: str) -> List[Suggestion]`
Analyze code and generate real-time suggestions.

**Parameters:**
- `code` (str): Source code
- `language` (str): Programming language

**Returns:**
- List of Suggestion objects

##### `get_critical_warnings() -> List[Suggestion]`
Get all critical-severity warnings.

**Returns:**
- List of critical Suggestion objects

##### `clear_suggestions()`
Clear all accumulated suggestions.

---

## Data Structures

### Scenario

Represents a potential future scenario with optimization.

**Attributes:**
- `scenario_id` (str): Unique identifier
- `probability` (float): Success probability (0.0-1.0)
- `outcome` (str): Predicted outcome description
- `optimized_solution` (str): Optimized code suggestion
- `estimated_time_ms` (float): Estimated execution time
- `risks` (List[str]): Potential risks
- `benefits` (List[str]): Expected benefits

### RollbackMarker

Represents a rollback point in the system.

**Attributes:**
- `marker_id` (str): Unique identifier
- `timestamp` (float): Creation time
- `description` (str): Human-readable description
- `state_snapshot` (Dict): System state snapshot
- `code_snapshot` (Dict): Code state snapshot

### Suggestion

Represents a real-time code suggestion.

**Attributes:**
- `suggestion_id` (str): Unique identifier
- `timestamp` (float): Creation time
- `type` (str): Suggestion type (optimization, warning, recommendation)
- `message` (str): Suggestion message
- `code_snippet` (Optional[str]): Example code
- `severity` (str): Severity level (info, warning, critical)

---

## Usage Examples

### Complete Workflow

```python
from naydoev1 import NayDoeV1

# Initialize
assistant = NayDoeV1()

# 1. Analyze code
code = "def calculate(x): return x * 2"
result = assistant.process_code(code, "python")

# 2. Review scenarios
best = result['best_scenario']
print(f"Best scenario: {best['probability']:.1%} probability")

# 3. Create checkpoint
marker_id = assistant.create_rollback_marker(
    "Initial implementation",
    {"calc.py": code}
)

# 4. Make changes and analyze again
new_code = "def calculate(x, multiplier=2): return x * multiplier"
result2 = assistant.process_code(new_code, "python")

# 5. Review suggestions
for suggestion in result2['suggestions']:
    print(f"{suggestion['type']}: {suggestion['message']}")

# 6. Rollback if needed
if not_satisfied:
    assistant.rollback(marker_id)

# 7. Check system status
status = assistant.get_system_status()
print(f"Languages: {status['languages_supported']}")
```

### Multi-Language Processing

```python
codes = {
    "python": "lambda x: x ** 2",
    "javascript": "x => x ** 2",
    "java": "x -> Math.pow(x, 2)"
}

for lang, code in codes.items():
    result = assistant.process_code(code, lang)
    print(f"{lang}: {result['processing_time_ms']:.2f}ms")
```

### Marker Management

```python
# Create multiple markers
markers = []
for i in range(5):
    marker_id = assistant.create_rollback_marker(
        f"Version {i}",
        {f"file{i}.py": f"code{i}"}
    )
    markers.append(marker_id)

# List all markers
all_markers = assistant.list_rollback_markers()
print(f"Total markers: {len(all_markers)}")

# Rollback to specific version
assistant.rollback(markers[2])  # Go to version 2
```

---

## Enumerations

### LanguageSupport

Supported programming languages:
- PYTHON, JAVASCRIPT, TYPESCRIPT, JAVA, CPP, CSHARP
- GO, RUST, PHP, RUBY, SWIFT, KOTLIN, SCALA
- R, SQL, HTML, CSS, BASH, POWERSHELL

### PatternType

Design pattern categories:
- CREATIONAL: Singleton, Factory, Builder, etc.
- STRUCTURAL: Adapter, Decorator, Proxy, etc.
- BEHAVIORAL: Observer, Strategy, Command, etc.
- CONCURRENCY: Thread Pool, Producer-Consumer, etc.
- FUNCTIONAL: Functional programming patterns
- REACTIVE: Reactive programming patterns

---

## Performance Characteristics

- **Response Time**: Milliseconds (typically < 2 seconds for 40 scenarios)
- **Scenario Generation**: Exactly 40 scenarios per analysis
- **Languages**: 19+ supported languages
- **Patterns**: 26+ design patterns
- **Algorithms**: 21+ algorithm implementations

---

## Error Handling

All methods return appropriate status indicators:
- Boolean return values for success/failure operations
- Optional types for operations that may not find results
- Comprehensive status dictionaries with error information

Example error handling:

```python
try:
    result = assistant.process_code(code, language)
    if not result['success']:
        print("Processing failed")
except Exception as e:
    print(f"Error: {e}")

# Safe rollback
success = assistant.rollback(marker_id)
if not success:
    print("Marker not found")
```

---

## Thread Safety

Note: The current implementation is not thread-safe. For concurrent usage, implement appropriate locking mechanisms or use separate instances per thread.

---

## Configuration

System behavior can be customized via `config.json`:
- Scenario count
- Performance targets
- Feature toggles
- Threshold settings

See `config.json` for full configuration options.
