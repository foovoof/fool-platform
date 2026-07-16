# Cyber Standards Integration Architecture

## Overview

Cyber Standards Integration provides interoperability with industry cybersecurity standards while maintaining FOOL's internal canonical domain model.

### Key Responsibilities

1. **Standard Support** - Support multiple industry standards
2. **Validation** - Validate objects against standard schemas
3. **Mapping** - Map between standards and FOOL domain
4. **Serialization** - JSON serialization/deserialization
5. **Registry** - Maintain supported standards registry

### What Cyber Standards Does NOT Do

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
│  Knowledge Graph                                           │
│      ↓                                                     │
│  Inference                                                 │
│      ↓                                                     │
│  Cyber Domain                                              │
│      ↓                                                     │
│  Cyber Knowledge Mapping                                   │
│      ↓                                                     │
│  CYBER STANDARDS INTEGRATION ← THIS LAYER                 │
│      ↓                                                     │
│  Threat Intelligence Services                               │
│      ↓                                                     │
│  AI Augmentation                                           │
│      ↓                                                     │
│  Applications                                              │
└─────────────────────────────────────────────────────────────┘
```

## Dependency Rules

### Allowed Dependencies

Cyber Standards may depend on:

- ✅ `standards` - Standard definitions
- ✅ `contracts` - Domain contracts
- ✅ `domain` - Domain models
- ✅ `knowledge` - Knowledge graph
- ✅ `cyber/domain` - Cyber domain concepts
- ✅ `platform/events` - Event bus
- ✅ `python standard library` - Standard library only

### Forbidden Dependencies

Cyber Standards MUST NOT depend on:

- ❌ `intelligence` - Intelligence runtime
- ❌ `ai` - AI/ML components
- ❌ `applications` - Application layer
- ❌ `connectors` - Data connectors
- ❌ `processing` - Data processing
- ❌ `external feeds` - External data feeds
- ❌ `detection engines` - Rule execution engines

## Supported Standards

| Standard | Version | Purpose |
|----------|---------|---------|
| STIX 2.x | 2.0, 2.1 | Structured Threat Information Expression |
| MITRE ATT&CK | 8.0 - 13.0 | Attack techniques and tactics |
| CVE | 4.0, 5.0 | Common Vulnerabilities and Exposures |
| CWE | 4.x | Common Weakness Enumeration |
| CAPEC | 3.x | Attack Pattern Enumeration |
| Sigma | 0.1 | Detection Rule Format |
| YARA | 3.0, 4.0 | Malware Detection Rules |
| OpenIOC | 1.0 | Open Indicators of Compromise |

## Canonical Domain

FOOL maintains its own canonical internal model:

| FOOL Type | Description |
|-----------|-------------|
| `indicator` | Observable indicators |
| `technique` | Attack techniques |
| `malware` | Malware instances |
| `threat_actor` | Threat actors |
| `campaign` | Attack campaigns |
| `infrastructure` | Infrastructure |
| `vulnerability` | Vulnerabilities |
| `tool` | Attack tools |
| `course_of_action` | Mitigation measures |

## Mapping Philosophy

### FOOL Domain → Standard

Maps FOOL internal concepts to standard representations:

```
malware → STIX malware object
       → ATT&CK software
       → YARA rule metadata
```

### Standard → FOOL Domain

Maps standard objects to FOOL internal concepts:

```
STIX indicator → FOOL indicator
ATT&CK technique → FOOL technique
CVE → FOOL vulnerability
```

### Mapping Rules

1. **Deterministic** - Same input always produces same output
2. **Lossless** - Preserve all relevant information
3. **Reversible** - Mapping is bidirectional where possible
4. **No interpretation** - No intelligence, only translation

## Module Structure

### Models (`cyber/standards/models.py`)

| Model | Purpose |
|-------|---------|
| `StandardType` | Enum of supported standards |
| `StandardMetadata` | Metadata for standards |
| `StandardValidationResult` | Validation results |
| `StandardMappingResult` | Mapping results |
| `StixObject` | STIX object model |
| `AttackObject` | ATT&CK object model |
| `CveObject` | CVE object model |
| `CweObject` | CWE object model |
| `CapecObject` | CAPEC object model |
| `SigmaRule` | Sigma rule metadata |
| `YaraRule` | YARA rule metadata |
| `OpenIOCObject` | OpenIOC object model |

### Registry (`cyber/standards/registry.py`)

| Method | Purpose |
|--------|---------|
| `register_standard()` | Register a standard |
| `get_standard()` | Get standard info |
| `list_standards()` | List all standards |
| `register_mapping()` | Register a mapping |
| `get_mapping()` | Get mapping info |
| `supports_standard()` | Check standard support |
| `supports_version()` | Check version support |

### Services (`cyber/standards/services.py`)

| Service | Purpose |
|---------|---------|
| `StandardIntegrationService` | Coordinates integration |
| `ValidationService` | Coordinates validation |
| `MappingService` | Coordinates mapping |
| `SerializationService` | Coordinates serialization |

### Events (`cyber/standards/events.py`)

| Event | Description |
|-------|-------------|
| `cyber.standard.loaded` | Standard loaded |
| `cyber.standard.validated` | Object validated |
| `cyber.mapping.created` | Mapping created |
| `cyber.mapping.failed` | Mapping failed |

## Standard Modules

### STIX Module

**Path**: `cyber/standards/stix/`

| Component | Purpose |
|-----------|---------|
| `enums.py` | STIX object types, relationship types |
| `validators.py` | STIX object validation |
| `mappers.py` | STIX ↔ FOOL mapping |
| `serializers.py` | JSON serialization |

### ATT&CK Module

**Path**: `cyber/standards/attack/`

| Component | Purpose |
|-----------|---------|
| `validators.py` | ATT&CK object validation |
| `mappers.py` | ATT&CK ↔ FOOL mapping |
| `serializers.py` | JSON serialization |

### CVE Module

**Path**: `cyber/standards/cve/`

| Component | Purpose |
|-----------|---------|
| `validators.py` | CVE validation |
| `mappers.py` | CVE ↔ FOOL mapping |
| `serializers.py` | JSON serialization |

### Other Modules

| Module | Path |
|--------|------|
| CWE | `cyber/standards/cwe/` |
| CAPEC | `cyber/standards/capec/` |
| Sigma | `cyber/standards/sigma/` |
| YARA | `cyber/standards/yara/` |
| OpenIOC | `cyber/standards/openioc/` |

## Usage Examples

### Validation Example

```python
from cyber.standards import ValidationService, StandardType

service = ValidationService()

# Validate STIX indicator
stix_indicator = {
    "type": "indicator",
    "id": "indicator--c410e480-e42b-47d1-9476-85307c12bcbf",
    "created": "2024-01-01T00:00:00Z",
    "modified": "2024-01-01T00:00:00Z",
    "pattern": "[ipv4-addr:value = '1.2.3.4']",
}

result = service.validate(StandardType.STIX, stix_indicator)
if result.is_valid:
    print("Valid STIX indicator")
```

### Mapping Example

```python
from cyber.standards import MappingService, StandardType

service = MappingService()

# Map STIX malware to FOOL domain
stix_malware = {
    "type": "malware",
    "id": "malware--c410e480-e42b-47d1-9476-85307c12bcbf",
    "name": "Emotet",
    "description": "Banking trojan",
}

result = service.to_fool_domain(StandardType.STIX, stix_malware)
if result.success:
    fool_object = result.mapped_object
    print(f"Type: {fool_object['type']}")  # "malware"
    print(f"Name: {fool_object['name']}")  # "Emotet"
```

### Registry Example

```python
from cyber.standards import CyberStandardRegistry, StandardType

registry = CyberStandardRegistry()

# List all supported standards
for std in registry.list_standards():
    print(f"{std.name} {std.version}")

# Check support
if registry.supports_standard(StandardType.STIX):
    print("STIX is supported")

if registry.supports_version(StandardType.ATTACK, "13.0"):
    print("ATT&CK v13.0 is supported")
```

## Versioning

Standards evolve over time. FOOL supports multiple versions:

| Standard | Supported Versions |
|----------|-------------------|
| STIX | 2.0, 2.1 |
| ATT&CK | 8.0, 9.0, 10.0, 11.0, 12.0, 13.0 |
| CVE | 4.0, 5.0 |
| CWE | 4.x |
| CAPEC | 3.x |
| Sigma | 0.1 |
| YARA | 3.0, 4.0 |
| OpenIOC | 1.0 |

## Event Integration

Events are optional and do not fail if the event bus is unavailable:

```python
from cyber.standards import CyberStandardEventEmitter

emitter = CyberStandardEventEmitter()

# Emit events
emitter.emit_loaded("stix", "2.1")
emitter.emit_validated("stix", True)
emitter.emit_mapping_created("stix", "src-1", "tgt-1")
emitter.emit_mapping_failed("cve", "CVE-2024-1234", "Invalid format")
```

## Guiding Principle

> FOOL owns the internal language. Industry standards are interoperability layers. Never allow an external standard to become the canonical domain model.

## Next Phase

**Phase 6E — Threat Intelligence Services**

This will implement:
- Threat intelligence workflows
- IOC management
- Threat actor profiles
- Campaign tracking
