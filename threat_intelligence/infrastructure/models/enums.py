"""
threat_intelligence/infrastructure/models/enums.py

Infrastructure Enums.
"""
from __future__ import annotations

from enum import Enum


class InfrastructureType(Enum):
    """Infrastructure type."""
    IP_ADDRESS = "ip_address"
    DOMAIN = "domain"
    SUBDOMAIN = "subdomain"
    FQDN = "fqdn"
    HOSTNAME = "hostname"
    URL_ENDPOINT = "url_endpoint"
    CLOUD_ASSET = "cloud_asset"
    SERVER = "server"
    VPS = "vps"
    DEDICATED_HOST = "dedicated_host"
    CDN = "cdn"
    PROXY = "proxy"
    VPN = "vpn"
    TOR_NODE = "tor_node"
    GATEWAY = "gateway"
    LOAD_BALANCER = "load_balancer"
    ASN = "asn"
    CIDR = "cidr"
    CERTIFICATE = "certificate"
    NAME_SERVER = "name_server"
    MAIL_SERVER = "mail_server"
    CONTAINER_ENDPOINT = "container_endpoint"
    KUBERNETES_ENDPOINT = "kubernetes_endpoint"
    CUSTOM = "custom"


class InfrastructureRole(Enum):
    """Infrastructure role."""
    COMMAND_CONTROL = "command_control"
    DELIVERY = "delivery"
    EXFILTRATION = "exfiltration"
    HOSTING = "hosting"
    SCANNING = "scanning"
    ATTACK = "attack"
    PHISHING = "phishing"
    STAGING = "staging"
    INFRASTRUCTURE = "infrastructure"
    SUPPORT = "support"
    UNKNOWN = "unknown"


class HostingType(Enum):
    """Hosting type."""
    CLOUD = "cloud"
    ON_PREMISE = "on_premise"
    COLOCATION = "colocation"
    VIRTUAL = "virtual"
    DEDICATED = "dedicated"
    SHARED = "shared"
    RESIDENTIAL = "residential"
    UNKNOWN = "unknown"


class ServiceType(Enum):
    """Service type."""
    HTTP = "http"
    HTTPS = "https"
    SSH = "ssh"
    FTP = "ftp"
    SMTP = "smtp"
    DNS = "dns"
    RDP = "rdp"
    SMB = "smb"
    DATABASE = "database"
    CUSTOM = "custom"


class Protocol(Enum):
    """Protocol."""
    TCP = "tcp"
    UDP = "udp"
    ICMP = "icmp"
    HTTP = "http"
    HTTPS = "https"
    DNS = "dns"
    SMTP = "smtp"
    SSH = "ssh"
    FTP = "ftp"
    CUSTOM = "custom"


class InfrastructureStatus(Enum):
    """Infrastructure status."""
    DRAFT = "draft"
    OBSERVED = "observed"
    VALIDATED = "validated"
    PUBLISHED = "published"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    REVOKED = "revoked"
    ARCHIVED = "archived"


class AssertionStatus(Enum):
    """Assertion status."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    DISPUTED = "disputed"
    REFUTED = "refuted"
    UNVERIFIED = "unverified"


class AssertionType(Enum):
    """Assertion type."""
    HOSTING = "hosting"
    USAGE = "usage"
    RELATIONSHIP = "relationship"
    CAPABILITY = "capability"
    COMMUNICATION = "communication"
    DELIVERY = "delivery"
    ATTRIBUTION = "attribution"
    ASSOCIATION = "association"
