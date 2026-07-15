# Data Connectors Foundation

## Phase 5A

This is the **Data Connectors Foundation** - Phase 5A of the FOOL Platform architecture.

## IMPORTANT: What This IS

This phase implements the **Data Acquisition Layer** that:

✅ Retrieves data from external sources  
✅ Converts data into standardized connector artifacts  
✅ Integrates with platform events  
✅ Supports policy evaluation  
✅ Provides validation  
✅ Maintains execution records  

## IMPORTANT: What This Is NOT

This phase does **NOT** implement:

- ❌ Intelligence
- ❌ Knowledge Resolution
- ❌ Inference
- ❌ AI/LLM
- ❌ Data Normalization
- ❌ Threat Intelligence
- ❌ IOC Extraction
- ❌ Parsing Intelligence
- ❌ Investigation
- ❌ Analytics

**Connectors retrieve data only. Processing begins in Phase 5B.**

## Architecture Position

```
Standards
    ↓
Contracts
    ↓
Domain
    ↓
Knowledge
    ↓
Inference
    ↓
Intelligence
    ↓
Connectors   ← THIS PHASE
    ↓
Processing
    ↓
Cyber Intelligence
    ↓
AI Augmentation
    ↓
Applications
```

## Key Principles

1. **Connectors retrieve data** - They do not understand data
2. **Connectors do not transform data** - They only provide access
3. **Connectors do not create intelligence** - Pure data retrieval
4. **Deterministic execution** - All operations are deterministic
5. **Observable** - Events for all operations
6. **Reusable** - Infrastructure-independent

## Dependency Rules

Connectors may depend only on:

- ✅ standards
- ✅ contracts
- ✅ platform/kernel
- ✅ platform/events
- ✅ platform/policies
- ✅ platform/configuration
- ✅ Python Standard Library

Connectors MUST NOT depend on:

- ❌ knowledge
- ❌ inference
- ❌ intelligence
- ❌ cyber
- ❌ ai
- ❌ applications

## Connector Contracts

| Contract | Purpose |
|----------|---------|
| `ConnectorDefinition` | Defines a connector |
| `ConnectorRequest` | Request for connector operation |
| `ConnectorResult` | Result of connector execution |
| `ConnectorArtifact` | Raw data retrieved by connector |
| `ConnectorConfiguration` | Connector configuration |
| `ConnectorExecutionRecord` | Audit/replay record |

## Connector Types

### File Connectors

| Connector | Purpose |
|-----------|---------|
| `FileConnector` | Reads files from filesystem |
| `DirectoryConnector` | Lists directory contents |
| `ZipConnector` | Extracts files from ZIP archives |
| `TarConnector` | Extracts files from TAR archives |

### Format Connectors

| Connector | Purpose |
|-----------|---------|
| `JsonConnector` | Reads JSON files |
| `CsvConnector` | Reads CSV files |
| `TextConnector` | Reads text files |
| `BinaryConnector` | Reads binary files |

### HTTP Connectors

| Connector | Purpose |
|-----------|---------|
| `HttpConnector` | Fetches data via HTTP/HTTPS |
| `RestConnector` | Calls REST APIs |

## Components

### Base (`connectors/base/`)

- `connector.py` - BaseConnector
- `runtime.py` - ConnectorRuntime
- `lifecycle.py` - Lifecycle management
- `policies.py` - Policy evaluation
- `events.py` - Event emission
- `validation.py` - Validation
- `exceptions.py` - Exceptions
- `models.py` - Contracts

### Registry (`connectors/registry/`)

- `__init__.py` - ConnectorRegistryLoader

## Usage

```python
from connectors import ConnectorRuntime, FileConnector, ConnectorRequest

# Create runtime
runtime = ConnectorRuntime()

# Create and register connector
connector = FileConnector()
connector.initialize()
connector.start()
runtime.register(connector)

# Execute request
request = ConnectorRequest(
    connector_id=connector.connector_id,
    source="/path/to/file.txt",
)

result = runtime.execute(request)

if result.is_successful():
    for artifact in result.artifacts:
        print(f"Retrieved: {artifact.name}")
        print(f"Size: {artifact.size}")
```

## Lifecycle

```
PENDING → INITIALIZED → STARTING → RUNNING
                              ↓         ↓
                           FAILED   STOPPING → STOPPED
```

## Events

| Event | Description |
|-------|-------------|
| `connector.initialized` | Connector initialized |
| `connector.started` | Connector started |
| `connector.completed` | Operation completed |
| `connector.failed` | Operation failed |
| `connector.validated` | Request validated |
| `connector.stopped` | Connector stopped |

## Policies

Policies control connector operations:

- `ALLOW` - Permit operation
- `DENY` - Block operation
- `WARN` - Allow with warning

## Next Phase

**Phase 5B — Data Processing Foundation**

This will implement:
- Data normalization
- Schema mapping
- Data validation
- Format conversion
- Basic transformations
