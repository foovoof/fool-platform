"""
threat_intelligence/models/enums.py

Threat Intelligence Enums.
"""
from __future__ import annotations

from enum import Enum


class ThreatEntityType(Enum):
    """Types of threat entities."""
    INDICATOR = "indicator"
    THREAT_ACTOR = "threat_actor"
    CAMPAIGN = "campaign"
    MALWARE = "malware"
    TOOL = "tool"
    INFRASTRUCTURE = "infrastructure"
    VULNERABILITY = "vulnerability"
    IDENTITY = "identity"
    VICTIM = "victim"
    TARGET = "target"
    EVIDENCE = "evidence"
    REPORT = "report"
    FINDING = "finding"
    RELATIONSHIP = "relationship"


class IndicatorType(Enum):
    """Types of indicators."""
    IPV4_ADDRESS = "ipv4_addr"
    IPV6_ADDRESS = "ipv6_addr"
    DOMAIN_NAME = "domain_name"
    URL = "url"
    EMAIL_ADDRESS = "email_addr"
    FILE_HASH_MD5 = "file_hash_md5"
    FILE_HASH_SHA1 = "file_hash_sha1"
    FILE_HASH_SHA256 = "file_hash_sha256"
    FILE_NAME = "file_name"
    FILE_PATH = "file_path"
    REGISTRY_KEY = "registry_key"
    MUTEX = "mutex"
    HOSTNAME = "hostname"
    EMAIL_SUBJECT = "email_subject"
    EMAIL_BODY = "email_body"
    USER_AGENT = "user_agent"
    BTC_ADDRESS = "btc_address"
    XMR_ADDRESS = "xmr_address"
    CUSTOM = "custom"


class ThreatActorType(Enum):
    """Types of threat actors."""
    NATION_STATE = "nation_state"
    STATE_SPONSORED = "state_sponsored"
    ORGANIZED_CRIME = "organized_crime"
    HACKTIVIST = "hacktivist"
    INSIDER_THREAT = "insider_threat"
    SCRIPT_KIDDIE = "script_kiddie"
    UNKNOWN = "unknown"


class MalwareType(Enum):
    """Types of malware."""
    VIRUS = "virus"
    WORM = "worm"
    TROJAN = "trojan"
    RANSOMWARE = "ransomware"
    SPYWARE = "spyware"
    ADWARE = "adware"
    BOT = "bot"
    ROOTKIT = "rootkit"
    KEYLOGGER = "keylogger"
    DROPPER = "dropper"
    BACKDOOR = "backdoor"
    CRYPTO_MINER = "crypto_miner"
    WIPER = "wiper"
    INFECTION_VECTOR = "infection_vector"


class MalwareFamily(Enum):
    """Malware family classifications."""
    APT = "apt"
    CRIMEWARE = "crimeware"
    RANSOMWARE_GROUP = "ransomware_group"
    BOTNET = "botnet"
    TARGETED = "targeted"
    OPPORTUNISTIC = "opportunistic"


class CampaignStatus(Enum):
    """Campaign status."""
    PLANNED = "planned"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    UNKNOWN = "unknown"


class IndicatorStatus(Enum):
    """Indicator status."""
    OBSERVED = "observed"
    EXPECTED = "expected"
    DEPLOYED = "deployed"
    REVOKED = "revoked"
    EXPIRED = "expired"


class ConfidenceLevel(Enum):
    """Confidence levels."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NONE = "none"


class SourceReliability(Enum):
    """Source reliability ratings."""
    A = "a"
    B = "b"
    C = "c"
    D = "d"
    E = "e"
    F = "f"


class InformationReliability(Enum):
    """Information reliability ratings."""
    CONFIRMED = "confirmed"
    LIKELY = "likely"
    POSSIBLE = "possible"
    DOUBTFUL = "doubtful"
    UNLIKELY = "unlikely"
    UNKNOWN = "unknown"


class ThreatLevel(Enum):
    """Threat levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFORMATIONAL = "informational"
    NONE = "none"


class ReportType(Enum):
    """Types of reports."""
    EXECUTIVE = "executive"
    TECHNICAL = "technical"
    TACTICAL = "tactical"
    STRATEGIC = "strategic"
    FLASH = "flash"
    PERIODIC = "periodic"
    AD_HOC = "ad_hoc"


class ReportStatus(Enum):
    """Report status."""
    DRAFT = "draft"
    REVIEW = "review"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class EvidenceType(Enum):
    """Types of evidence."""
    DIRECT = "direct"
    CIRCUMSTANTIAL = "circumstantial"
    CORROBORATING = "corroborating"
    INCONSISTENT = "inconsistent"


class FindingType(Enum):
    """Types of findings."""
    THREAT_ACTOR = "threat_actor"
    CAMPAIGN = "campaign"
    MALWARE = "malware"
    INFRASTRUCTURE = "infrastructure"
    VULNERABILITY = "vulnerability"
    TECHNIQUE = "technique"
    TTP = "ttp"
    TREND = "trend"
    CORRELATION = "correlation"


class LifecycleStatus(Enum):
    """Lifecycle statuses."""
    NEW = "new"
    IN_PROGRESS = "in_progress"
    STABLE = "stable"
    DEGRADED = "degraded"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"
