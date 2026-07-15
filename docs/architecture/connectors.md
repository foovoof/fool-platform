# Data Connectors Architecture

## Overview

Data Connectors provide infrastructure-independent acquisition of external data sources. They form the data acquisition layer of the FOOL Platform.

## Purpose

Connectors retrieve data from external sources and convert it into standardized connector artifacts. They serve as the foundation for all data access within the platform.

### Key Responsibilities

1. **Data Retrieval** - Fetch data from files, URLs, APIs, etc.
2. **Data Standardization** - Convert data into ConnectorArtifact format
3. **Lifecycle Management** - Initialize, start, stop connectors
4. **Policy Enforcement** - Evaluate policies before execution
5. **Event Emission** - Emit events for observability
6. **Execution Recording** - Maintain audit/replay records

### What Connectors Do NOT Do

- ❌ Parse data
- ❌ Normalize data
- ❌ Transform data
- ❌ Create intelligence
- ❌ Make decisions
- ❌ Apply business logic

## Architecture Position

```
┌─────────────────────────────────────────────────────────────┐
│                    FOOL Platform                            │
├─────────────────────────────────────────────────────────────┤
│  Standards                                                 │
│      ↓                                                     │
│  Contracts                                                 │
│      ↓                                                     │
│  Domain                                                    │
│      ↓                                                     │
│  Knowledge                                                 │
│      ↓                                                     │
│  Inference                                                 │
│      ↓                                                     │
│  Intelligence                                              │
│      ↓                                                     │
│  CONNECTORS ← THIS LAYER                                   │
│      ↓                                                     │
│  Processing                                                │
│      ↓                                                     │
│  Cyber Intelligence                                        │
│      ↓                                                     │
│  AI Augmentation                                           │
│      ↓                                                     │
│  Applications                                              │
└─────────────────────────────────────────────────────────────┘
```

## Dependency Rules

### Allowed Dependencies

Connectors may depend on:

- ✅ `standards` - Standards definitions
- ✅ `contracts` - Domain contracts
- ✅ `platform/kernel` - Platform kernel
- ✅ `platform/events` - Event bus
- ✅ `platform/policies` - Policy engine
- ✅ `platform/configuration` - Configuration
- ✅ `python standard library` - Standard library only

### Forbidden Dependencies

Connectors MUST NOT depend on:

- ❌ `knowledge` - Knowledge layer
- ❌ `inference` - Inference engine
- ❌ `intelligence` - Intelligence layer
- ❌ `cyber` - Cyber intelligence
- ❌ `ai` - AI/ML components
- ❌ `applications` - Application layer

## Connector Contracts

### ConnectorDefinition

Defines a connector's capabilities and configuration.

```python
@dataclass
class ConnectorDefinition:
    connector_id: str
    name: str
    description: str
    connector_type: ConnectorType
    capabilities: list[ConnectorCapability]
    inputs: dict[str, Any]
    outputs: dict[str, Any]
```

### ConnectorRequest

Request for connector operation.

```python
@dataclass
class ConnectorRequest:
    request_id: str
    connector_id: str
    connector_type: ConnectorType
    operation: str
    source: str
    inputs: dict[str, Any]
    parameters: dict[str, Any]
```

### ConnectorResult

Result of connector execution.

```python
@dataclass
class ConnectorResult:
    result_id: str
    request_id: str
    connector_id: str
    status: ConnectorStatus
    artifacts: list[ConnectorArtifact]
    outputs: dict[str, Any]
    errors: list[str]
    execution_time_ms: float
```

### ConnectorArtifact

Raw data retrieved by connector.

```python
@dataclass
class ConnectorArtifact:
    artifact_id: str
    artifact_type: str
    name: str
    content: Any
    content_type: str
    size: int
    metadata: dict[str, Any]
```

## Base Connector

The `BaseConnector` class provides the foundation for all connectors.

### Responsibilities

- **Lifecycle Management** - Initialize, start, stop
- **Request Validation** - Validate incoming requests
- **Policy Evaluation** - Check policies before execution
- **Event Emission** - Emit lifecycle and execution events
- **Error Handling** - Catch and report errors
- **Result Generation** - Create structured results

### Subclass Responsibilities

Subclasses implement `_execute()` to provide connector-specific logic.

```python
class FileConnector(BaseConnector):
    def _execute(self, request, result):
        # Read file and populate result
        ...
        return result
```

## Connector Lifecycle

```
┌──────────┐
│ PENDING  │
└────┬─────┘
     │ initialize()
     ↓
┌──────────┐
│INITIALIZED│
└────┬─────┘
     │ start()
     ↓
┌──────────┐     start()
│ STARTING ├──────────────────┐
└────┬─────┘                  │
     │                        │
     ↓                        ↓
┌──────────┐            ┌──────────┐
│ RUNNING  │            │ FAILED   │
└────┬─────┘            └──────────┘
     │ stop()                 ↑
     ↓                        │
┌──────────┐                  │
│STOPPING  │──────────────────┘
└────┬─────┘
     │ stop()
     ↓
┌──────────┐
│ STOPPED  │
└──────────┘
```

## Connector Runtime

The `ConnectorRuntime` manages connector instances.

### Responsibilities

- **Registration** - Register/unregister connectors
- **Execution** - Execute requests through connectors
- **Records** - Maintain execution records
- **Events** - Emit runtime events

### Usage

```python
runtime = ConnectorRuntime()

# Register connector
runtime.register(FileConnector())

# Execute request
result = runtime.execute(ConnectorRequest(...))
```

## Registry

The `ConnectorRegistryLoader` loads connector definitions from YAML manifests.

### Manifest Format

```yaml
connectors:
  - connector_id: file-connector
    name: File Connector
    connector_type: file
    capabilities:
      - read
      - list
```

## Events

Connectors emit events for observability:

| Event | Description |
|-------|-------------|
| `connector.initialized` | Connector initialized |
| `connector.started` | Connector started |
| `connector.completed` | Operation completed |
| `connector.failed` | Operation failed |
| `connector.validated` | Request validated |
| `connector.stopped` | Connector stopped |

Events integrate with `platform/events` when available.

## Policies

Policies control connector operations:

```python
# Deny access to specific paths
PolicyRule(
    rule_id="deny-blocked",
    name="Deny Blocked",
    action=PolicyAction.DENY,
    conditions={"source": "/blocked"},
)

# Warn on large files
PolicyRule(
    rule_id="warn-large",
    name="Warn Large Files",
    action=PolicyAction.WARN,
    conditions={"size": {"gt": 1000000}},
)
```

## Reference Connectors

### File Connectors

| Connector | Description |
|-----------|-------------|
| `FileConnector` | Reads files from filesystem |
| `DirectoryConnector` | Lists directory contents |
| `ZipConnector` | Extracts from ZIP archives |
| `TarConnector` | Extracts from TAR archives |

### Format Connectors

| Connector | Description |
|-----------|-------------|
| `JsonConnector` | Reads JSON files |
| `CsvConnector` | Reads CSV files |
| `TextConnector` | Reads text files |
| `BinaryConnector` | Reads binary files |

### HTTP Connectors

| Connector | Description |
|-----------|-------------|
| `HttpConnector` | Fetches via HTTP/HTTPS |
| `RestConnector` | Calls REST APIs |

## Validation

Connectors support validation:

- **ConfigurationValidator** - Validate connector configuration
- **RequestValidator** - Validate execution requests
- **LifecycleValidator** - Validate state transitions
- **CapabilityValidator** - Validate connector definitions
- **ArtifactValidator** - Validate retrieved artifacts

## Processing Pipeline

```
External Source
      ↓
   Connector
(Retrieves raw data)
      ↓
 ConnectorArtifact
(Raw bytes/content)
      ↓
  Phase 5B
(Processing begins)
```

## Next Phase

**Phase 5B — Data Processing Foundation**

Processing responsibilities:

- Data normalization
- Schema mapping
- Data validation
- Format conversion
- Basic transformations
- Data enrichment
