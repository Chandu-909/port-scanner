"""
Utility functions for port scanner.
"""

import socket
import re
from typing import List


# Common service ports
COMMON_PORTS = {
    20: "FTP-DATA",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    465: "SMTP-SSL",
    587: "SMTP-TLS",
    993: "IMAP-SSL",
    995: "POP3-SSL",
    1433: "MSSQL",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    5900: "VNC",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
    9200: "Elasticsearch",
    27017: "MongoDB",
    6379: "Redis",
}


def print_banner() -> None:
    """Print ASCII banner."""
    banner = """
    ╔═══════════════════════════════════════════════════╗
    ║         🔍 PYTHON PORT SCANNER v1.0.0             ║
    ║      Fast Multi-threaded Network Scanner          ║
    ╚═══════════════════════════════════════════════════╝
    """
    print(banner)


def validate_ip(host: str) -> str:
    """
    Validate and resolve hostname to IP address.

    Args:
        host: IP address or hostname

    Returns:
        IP address string

    Raises:
        ValueError: If host is invalid
    """
    try:
        # Try to resolve hostname to IP
        ip_address = socket.gethostbyname(host)
        return ip_address
    except socket.gaierror:
        raise ValueError(f"Could not resolve hostname: {host}")
    except Exception as e:
        raise ValueError(f"Invalid host: {e}")


def validate_port_range(port_string: str) -> List[int]:
    """
    Parse and validate port specification.

    Examples:
        "80" -> [80]
        "80-100" -> [80, 81, ..., 100]
        "80,443,8080" -> [80, 443, 8080]
        "80,443-445,8080" -> [80, 443, 444, 445, 8080]

    Args:
        port_string: Port specification string

    Returns:
        List of port numbers

    Raises:
        ValueError: If port specification is invalid
    """
    ports: List[int] = []

    try:
        # Split by comma for multiple port groups
        groups = port_string.split(',')

        for group in groups:
            group = group.strip()

            if '-' in group:
                # Port range (e.g., "80-443")
                parts = group.split('-')
                if len(parts) != 2:
                    raise ValueError(f"Invalid port range: {group}")

                try:
                    start_port = int(parts[0].strip())
                    end_port = int(parts[1].strip())
                except ValueError:
                    raise ValueError(f"Invalid port numbers in range: {group}")

                if not (1 <= start_port <= 65535 and 1 <= end_port <= 65535):
                    raise ValueError(f"Port numbers must be between 1 and 65535: {group}")

                if start_port > end_port:
                    raise ValueError(f"Invalid range: start port ({start_port}) > end port ({end_port})")

                ports.extend(range(start_port, end_port + 1))
            else:
                # Single port
                try:
                    port = int(group)
                except ValueError:
                    raise ValueError(f"Invalid port number: {group}")

                if not (1 <= port <= 65535):
                    raise ValueError(f"Port number must be between 1 and 65535: {port}")

                ports.append(port)

        if not ports:
            raise ValueError("No valid ports specified")

        # Remove duplicates and sort
        return sorted(list(set(ports)))

    except ValueError as e:
        raise ValueError(f"Invalid port specification: {str(e)}")


def get_service_name(port: int) -> str:
    """
    Get service name for a port number.

    Args:
        port: Port number

    Returns:
        Service name or "Unknown"
    """
    if port in COMMON_PORTS:
        return COMMON_PORTS[port]

    try:
        service = socket.getservbyport(port)
        return service.upper()
    except OSError:
        return "Unknown"