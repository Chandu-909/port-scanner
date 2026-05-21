"""
Core port scanning functionality.
"""

import socket
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import List, Set, Dict, Optional
from utils import get_service_name


class PortScanner:
    """Multi-threaded port scanner."""

    def __init__(
        self,
        host: str,
        ports: List[int],
        threads: int = 100,
        timeout: float = 1.0,
        verbose: bool = False,
        banner_grab: bool = False
    ):
        """
        Initialize port scanner.

        Args:
            host: Target host IP or hostname
            ports: List of ports to scan
            threads: Number of worker threads
            timeout: Socket timeout in seconds
            verbose: Enable verbose output
            banner_grab: Attempt to grab service banners
        """
        self.host = host
        self.ports = ports
        self.threads = threads
        self.timeout = timeout
        self.verbose = verbose
        self.banner_grab = banner_grab
        self.results: Dict[int, Dict[str, str]] = {}
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None

    def _scan_port(self, port: int) -> tuple:
        """
        Scan a single port.

        Args:
            port: Port number to scan

        Returns:
            Tuple of (port, is_open, service, banner)
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                result = sock.connect_ex((self.host, port))

                if result == 0:
                    service = get_service_name(port)
                    banner = ""

                    # Attempt banner grabbing if enabled
                    if self.banner_grab:
                        banner = self._grab_banner(port)

                    if self.verbose:
                        print(f"✅ Port {port} is OPEN ({service})")

                    return (port, True, service, banner)
                else:
                    if self.verbose:
                        print(f"❌ Port {port} is closed")
                    return (port, False, "", "")

        except socket.gaierror:
            print(f"❌ Hostname {self.host} could not be resolved")
            return (port, False, "", "")
        except socket.error as e:
            if self.verbose:
                print(f"⚠️  Error scanning port {port}: {str(e)}")
            return (port, False, "", "")
        except Exception as e:
            if self.verbose:
                print(f"⚠️  Unexpected error on port {port}: {str(e)}")
            return (port, False, "", "")

    def _grab_banner(self, port: int, banner_timeout: float = 2.0) -> str:
        """
        Attempt to grab service banner from open port.

        Args:
            port: Open port number
            banner_timeout: Timeout for banner grabbing

        Returns:
            Service banner string or empty string if failed
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(banner_timeout)
                sock.connect((self.host, port))
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                return banner[:100] if banner else ""  # Limit to 100 chars
        except Exception:
            return ""

    def scan(self) -> List[int]:
        """
        Perform the port scan.

        Returns:
            List of open ports
        """
        self.start_time = datetime.now()
        open_ports: List[int] = []

        print("🔄 Scanning in progress...\n")

        # Use ThreadPoolExecutor for concurrent scanning
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            # Submit all port scan tasks
            futures = {
                executor.submit(self._scan_port, port): port
                for port in self.ports
            }

            # Collect results as they complete
            completed = 0
            total = len(self.ports)

            for future in as_completed(futures):
                completed += 1
                port, is_open, service, banner = future.result()

                if is_open:
                    open_ports.append(port)
                    self.results[port] = {
                        "status": "open",
                        "service": service,
                        "banner": banner
                    }

                # Print progress every 100 ports
                if completed % 100 == 0 or completed == total:
                    progress = (completed / total) * 100
                    print(f"📈 Progress: {completed}/{total} ({progress:.1f}%)")

        self.end_time = datetime.now()
        open_ports.sort()
        return open_ports

    def print_results(self, open_ports: List[int]) -> None:
        """
        Print scan results in a formatted table.

        Args:
            open_ports: List of open ports
        """
        duration = (self.end_time - self.start_time).total_seconds()

        print("\n" + "=" * 70)
        print("SCAN RESULTS")
        print("=" * 70)

        if open_ports:
            print(f"\n{'PORT':<10}{'STATUS':<12}{'SERVICE':<20}{'BANNER':<30}")
            print("-" * 70)

            for port in open_ports:
                result = self.results.get(port, {})
                status = result.get("status", "unknown")
                service = result.get("service", "Unknown")
                banner = result.get("banner", "")

                # Truncate banner for display
                banner_display = (banner[:25] + "...") if len(banner) > 25 else banner

                print(f"{port:<10}{status:<12}{service:<20}{banner_display:<30}")

            print("-" * 70)
            print(f"\n✅ Found {len(open_ports)} open port(s)")
        else:
            print("\n⚠️  No open ports found")

        print(f"⏱️  Scan duration: {duration:.2f} seconds")
        print("=" * 70 + "\n")

    def save_results(self, open_ports: List[int], filename: str) -> None:
        """
        Save scan results to a JSON file.

        Args:
            open_ports: List of open ports
            filename: Output filename
        """
        output = {
            "host": self.host,
            "scan_time": self.start_time.isoformat() if self.start_time else None,
            "duration_seconds": (self.end_time - self.start_time).total_seconds() if (self.start_time and self.end_time) else 0,
            "ports_scanned": len(self.ports),
            "open_ports": open_ports,
            "details": self.results
        }

        try:
            with open(filename, 'w') as f:
                json.dump(output, f, indent=2)
        except IOError as e:
            print(f"❌ Failed to save results: {e}")