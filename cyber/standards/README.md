# Cyber Standards Integration

## Phase 6D

This is the **Cyber Standards Integration Foundation** - Phase 6D of the FOOL Platform architecture.

## IMPORTANT: What This IS

This phase implements **interoperability** with industry cybersecurity standards:

✅ STIX 2.x (Structured Threat Information Expression)  
✅ MITRE ATT&CK Framework  
✅ CVE (Common Vulnerabilities and Exposures)  
✅ CWE (Common Weakness Enumeration)  
✅ CAPEC (Common Attack Pattern Enumeration and Classification)  
✅ Sigma Detection Rules  
✅ YARA Malware Detection Rules  
✅ OpenIOC (Open Indicators of Compromise)

## IMPORTANT: What This Is NOT

This phase does **NOT** implement:

- ❌ Threat Intelligence workflows
- ❌ Threat Hunting
- ❌ Detection execution
- ❌ Sigma execution
- ❌ YARA execution
- ❌ STIX import/export pipelines
- ❌ External feeds
- ❌ MISP integration
- ❌ TAXII
- ❌ AI
- ❌ LLM
- ❌ External services

**Interoperability only. No execution.**

## Architectural Principle

```
External Standards
        ↓
Standard Adapters
        ↓
FOOL Canonical Domain
        ↓
Knowledge Graph
        ↓
Inference
        ↓
Correlation
        ↓
Threat Intelligence
```

**FOOL remains the canonical internal model. External standards never become the source of truth.**

## Module Structure

```
cyber/standards/
├── __init__.py
├── models.py
├── registry.py
├── services.py
├── events.py
├── stix/
│   ├── __init__.py
│   ├── enums.py
│   ├── validators.py
│   ├── mappers.py
│   └── serializers.py
├── attack/
│   ├── __init__.py
│   ├── validators.py
│   ├── mappers.py
│   └── serializers.py
├── cve/
│   ├── __init__.py
│   ├── validators.py
│   ├── mappers.py
│   └── serializers.py
├── cwe/
│   ├── __init__.py
│   ├── validators.py
│   ├── mappers.py
│   └── serializers.py
├── capec/
│   ├── __init__.py
│   ├── validators.py
│   ├── mappers.py
│   └── serializers.py
├── sigma/
│   ├── __init__.py
│   ├── validators.py
│   ├── mappers.py
│   └── serializers.py
├── yara/
│   ├── __init__.py
│   ├── validators.py
│   ├── mappers.py
│   └── serializers.py
├── openioc/
│   ├── __init__.py
│   ├── validators.py
│   ├── mappers.py
│   └── serializers.py
└── tests/
    ├── __init__.py
    └── test_cyber_standards.py
```

## Supported Standards

### STIX 2.x

| Feature | Support |
|---------|---------|
| Object Types | indicator, malware, threat-actor, attack-pattern, vulnerability, etc. |
| Versions | 2.0, 2.1 |
| Relationships | uses, targets, delivers, etc. |
| Bundles | Yes |

### MITRE ATT&CK

| Feature | Support |
|---------|---------|
| Techniques | T{id} format |
| Groups | G{id} format |
| Software | S{id} format |
| Mitigations | M{id} format |
| Versions | 8.0 - 13.0 |

### CVE

| Feature | Support |
|---------|---------|
| Format | CVE-{year}-{id} |
| Versions | 4.0, 5.0 |
| CVSS | Score and severity |

### CWE

| Feature | Support |
|---------|---------|
| Format | CWE-{id} |
| Weaknesses | All CWE entries |

### CAPEC

| Feature | Support |
|---------|---------|
| Format | CAPEC-{id} |
| Attack Patterns | All CAPEC entries |

### Sigma

| Feature | Support |
|---------|---------|
| Metadata | title, description, level, status |
| Detection | detection section |
| Logsource | logsource mapping |

### YARA

| Feature | Support |
|---------|---------|
| Metadata | meta section |
| Strings | string definitions |
| Condition | rule condition |

### OpenIOC

| Feature | Support |
|---------|---------|
| Format | IOC XML/JSON |
| Indicators | All indicator types |

## Usage

### Validation

```python
from cyber.standards import ValidationService, StandardType

service = ValidationService()

# Validate STIX object
result = service.validate(StandardType.STIX, stix_object)
if result.is_valid:
    print("Valid STIX object")
else:
    for error in result.errors:
        print(f"Error: {error}")
```

### Mapping

```python
from cyber.standards import MappingService, StandardType

service = MappingService()

# Map STIX to FOOL domain
result = service.to_fool_domain(StandardType.STIX, stix_object)
if result.success:
    fool_object = result.mapped_object
    print(f"Mapped to: {result.target_type}")

# Map ATT&CK to FOOL domain
result = service.to_fool_domain(StandardType.ATTACK, technique)
```

### Serialization

```python
from cyber.standards import SerializationService, StandardType

service = SerializationService()

# Serialize to JSON
json_str = service.serialize(StandardType.CVE, cve_object)

# Deserialize from JSON
cve_object = service.deserialize(StandardType.CVE, json_str)
```

### Registry

```python
from cyber.standards import CyberStandardRegistry, StandardType

registry = CyberStandardRegistry()

# List supported standards
standards = registry.list_standards()
for std in standards:
    print(f"{std.name} {std.version}")

# Check support
if registry.supports_standard(StandardType.STIX):
    print("STIX is supported")

if registry.supports_version(StandardType.STIX, "2.1"):
    print("STIX 2.1 is supported")
```

### Events

```python
from cyber.standards import CyberStandardEventEmitter

emitter = CyberStandardEventEmitter()

# Emit events
emitter.emit_loaded("stix", "2.1")
emitter.emit_validated("stix", True)
emitter.emit_mapping_created("stix", "src-1", "tgt-1")

# Get events
events = emitter.get_events()
```

## Architecture Boundaries

### Allowed Dependencies

- ✅ `standards` - Standard definitions
- ✅ `contracts` - Domain contracts
- ✅ `domain` - Domain models
- ✅ `knowledge` - Knowledge graph
- ✅ `cyber/domain` - Cyber domain concepts
- ✅ `platform/events` - Event bus
- ✅ `python standard library` - Standard library only

### Forbidden Dependencies

- ❌ `intelligence` - Intelligence runtime
- ❌ `ai` - AI/ML components
- ❌ `applications` - Application layer
- ❌ `connectors` - Data connectors
- ❌ `processing` - Data processing
- ❌ `external feeds` - External data feeds
- ❌ `detection engines` - Rule execution engines
- ❌ `networks` - Network access

## Key Principles

1. **FOOL is authoritative** - Internal model is the source of truth
2. **Standards are interoperability layers** - Not the primary domain model
3. **Deterministic mappings** - All mappings are deterministic
4. **Observable events** - Optional events for all operations
5. **No execution** - No rule execution, detection, or intelligence workflows
6. **No external feeds** - No network access, no external services

## Next Phase

**Phase 6E — Threat Intelligence Services**

This will implement:
- Threat intelligence workflows
- IOC management
- Threat actor profiles
- Campaign tracking
