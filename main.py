#!/usr/bin/env python3
"""
Port Scanner - A fast, multi-threaded network port scanning utility.
Author: Chandu-909
License: MIT
"""

import argparse
import sys
from scanner import PortScanner
from utils import validate_ip, validate_port_range, print_banner


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="🔍 Fast Multi-threaded Port Scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py 127.0.0.1
  python main.py 192.168.1.1 -p 1-1000
  python main.py google.com -p 80,443,8080 -t 200
  python main.py 127.0.0.1 --timeout 2 --output results.json
        """
    )

    parser.add_argument(
        "host",
        help="Target host IP address or hostname"
    )

    parser.add_argument(
        "-p", "--ports",
        default="1-1024",
        help="Port range to scan (default: 1-1024). Examples: 80, 80-443, 80,443,8080"
    )

    parser.add_argument(
        "-t", "--threads",
        type=int,
        default=100,
        help="Number of threads (default: 100, max: 1000)"
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=1.0,
        help="Socket timeout in seconds (default: 1.0)"
    )

    parser.add_argument(
        "-o", "--output",
        help="Save results to file (JSON format)"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    parser.add_argument(
        "--banner",
        action="store_true",
        help="Attempt banner grabbing on open ports"
    )

    return parser.parse_args()


def main():
    """Main function."""
    print_banner()

    args = parse_arguments()

    # Validate inputs
    try:
        host = validate_ip(args.host)
        ports = validate_port_range(args.ports)
        threads = min(max(1, args.threads), 1000)  # Clamp threads between 1-1000
        timeout = max(0.1, args.timeout)  # Minimum 0.1 seconds

    except ValueError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Create scanner instance
    scanner = PortScanner(
        host=host,
        ports=ports,
        threads=threads,
        timeout=timeout,
        verbose=args.verbose,
        banner_grab=args.banner
    )

    # Run scan
    try:
        print(f"\n🎯 Target: {args.host}")
        print(f"📊 Ports: {len(ports)} to scan")
        print(f"⚙️  Threads: {threads}")
        print(f"⏱️  Timeout: {timeout}s\n")

        open_ports = scanner.scan()

        # Display results
        scanner.print_results(open_ports)

        # Save to file if requested
        if args.output:
            scanner.save_results(open_ports, args.output)
            print(f"💾 Results saved to {args.output}")

        # Exit with status based on results
        sys.exit(0 if open_ports else 1)

    except KeyboardInterrupt:
        print("\n\n⚠️  Scan interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"❌ Error during scan: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()