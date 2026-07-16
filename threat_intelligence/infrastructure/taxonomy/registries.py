"""
threat_intelligence/infrastructure/taxonomy/registries.py

Infrastructure Taxonomy Registries.
"""
from __future__ import annotations


class InfrastructureTypeRegistry:
    """Registry for infrastructure types."""
    
    _types: dict[str, str] = {
        "ip_address": "IP Address",
        "domain": "Domain",
        "subdomain": "Subdomain",
        "fqdn": "Fully Qualified Domain Name",
        "hostname": "Hostname",
        "url_endpoint": "URL Endpoint",
        "cloud_asset": "Cloud Asset",
        "server": "Server",
        "vps": "Virtual Private Server",
        "dedicated_host": "Dedicated Host",
        "cdn": "Content Delivery Network",
        "proxy": "Proxy Server",
        "vpn": "VPN Server",
        "tor_node": "Tor Node",
        "gateway": "Gateway",
        "load_balancer": "Load Balancer",
        "asn": "Autonomous System Number",
        "cidr": "CIDR Block",
        "certificate": "SSL/TLS Certificate",
        "name_server": "Name Server",
        "mail_server": "Mail Server",
        "container_endpoint": "Container Endpoint",
        "kubernetes_endpoint": "Kubernetes Endpoint",
        "custom": "Custom Infrastructure",
    }
    
    @classmethod
    def get_types(cls) -> dict[str, str]:
        """Get all infrastructure types."""
        return dict(cls._types)
    
    @classmethod
    def get_description(cls, infra_type: str) -> str:
        """Get description for type."""
        return cls._types.get(infra_type, "Unknown type")
    
    @classmethod
    def is_valid(cls, infra_type: str) -> bool:
        """Check if type is valid."""
        return infra_type in cls._types


class InfrastructureRoleRegistry:
    """Registry for infrastructure roles."""
    
    _roles: dict[str, str] = {
        "command_control": "Command and Control",
        "delivery": "Delivery Infrastructure",
        "exfiltration": "Data Exfiltration",
        "hosting": "Hosting Infrastructure",
        "scanning": "Scanning Infrastructure",
        "attack": "Attack Infrastructure",
        "phishing": "Phishing Infrastructure",
        "staging": "Staging Infrastructure",
        "infrastructure": "General Infrastructure",
        "support": "Support Infrastructure",
        "unknown": "Unknown Role",
    }
    
    @classmethod
    def get_roles(cls) -> dict[str, str]:
        """Get all roles."""
        return dict(cls._roles)
    
    @classmethod
    def get_description(cls, role: str) -> str:
        """Get description for role."""
        return cls._roles.get(role, "Unknown role")


class HostingTypeRegistry:
    """Registry for hosting types."""
    
    _types: dict[str, str] = {
        "cloud": "Cloud Hosting",
        "on_premise": "On-Premise",
        "colocation": "Colocation",
        "virtual": "Virtual Server",
        "dedicated": "Dedicated Server",
        "shared": "Shared Hosting",
        "residential": "Residential",
        "unknown": "Unknown Hosting",
    }
    
    @classmethod
    def get_types(cls) -> dict[str, str]:
        """Get all hosting types."""
        return dict(cls._types)


class ServiceTypeRegistry:
    """Registry for service types."""
    
    _types: dict[str, str] = {
        "http": "HTTP Service",
        "https": "HTTPS Service",
        "ssh": "SSH Service",
        "ftp": "FTP Service",
        "smtp": "SMTP Service",
        "dns": "DNS Service",
        "rdp": "RDP Service",
        "smb": "SMB Service",
        "database": "Database Service",
        "custom": "Custom Service",
    }
    
    @classmethod
    def get_types(cls) -> dict[str, str]:
        """Get all service types."""
        return dict(cls._types)


class ProtocolRegistry:
    """Registry for protocols."""
    
    _protocols: dict[str, str] = {
        "tcp": "TCP",
        "udp": "UDP",
        "icmp": "ICMP",
        "http": "HTTP",
        "https": "HTTPS",
        "dns": "DNS",
        "smtp": "SMTP",
        "ssh": "SSH",
        "ftp": "FTP",
        "custom": "Custom Protocol",
    }
    
    @classmethod
    def get_protocols(cls) -> dict[str, str]:
        """Get all protocols."""
        return dict(cls._protocols)


class RelationshipRegistry:
    """Registry for infrastructure relationships."""
    
    _relationships: dict[str, str] = {
        "hosts": "Hosts infrastructure",
        "resolves_to": "Resolves to another entity",
        "communicates_with": "Communicates with",
        "used_by": "Used by entity",
        "associated_with": "Associated with",
        "delivers": "Delivers malware/payload",
        "commands": "Issues commands",
        "exfiltrates": "Exfiltrates data",
        "supports": "Supports infrastructure",
        "part_of": "Part of larger infrastructure",
        "related_to": "Related to",
    }
    
    @classmethod
    def get_relationships(cls) -> dict[str, str]:
        """Get all relationship types."""
        return dict(cls._relationships)
    
    @classmethod
    def get_description(cls, rel_type: str) -> str:
        """Get description for relationship type."""
        return cls._relationships.get(rel_type, "Unknown relationship")
