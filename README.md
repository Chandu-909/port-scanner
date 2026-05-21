# 🔍 Python Port Scanner

A fast, multi-threaded network port scanner built with Python. Perfect for network diagnostics, security testing, and learning network programming concepts.

## ✨ Features

- ⚡ **Multi-threaded scanning** - Scan multiple ports simultaneously
- 🎯 **Flexible port specification** - Single ports, ranges, or combinations
- 📊 **Service detection** - Identify common services running on ports
- 🚩 **Banner grabbing** - Optional banner grabbing for service identification
- 💾 **JSON export** - Save scan results for later analysis
- 🎨 **Clean output** - Human-readable results with progress tracking
- 🛡️ **Error handling** - Graceful handling of network errors
- ⚙️ **Customizable** - Adjustable threads, timeout, and port ranges

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Chandu-909/port-scanner.git
cd port-scanner

# (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (optional)
pip install -r requirements.txt
```

### Basic Usage

```bash
# Scan default ports (1-1024) on localhost
python main.py 127.0.0.1

# Scan specific port range
python main.py 192.168.1.1 -p 1-10000

# Scan specific ports
python main.py example.com -p 80,443,8080

# Scan with custom threads and timeout
python main.py 127.0.0.1 -t 200 --timeout 2.0

# Enable banner grabbing
python main.py 127.0.0.1 --banner

# Save results to file
python main.py 127.0.0.1 -o results.json

# Verbose output
python main.py 127.0.0.1 -v
```

## 📖 Usage Examples

### Example 1: Scan localhost for common ports
```bash
python main.py 127.0.0.1
```

### Example 2: Scan a network with custom thread count
```bash
python main.py 192.168.1.100 -p 1-1000 -t 150
```

### Example 3: Scan specific ports on a remote host
```bash
python main.py 8.8.8.8 -p 80,443,53 --banner
```

### Example 4: Full scan with output to file
```bash
python main.py example.com -p 1-65535 -t 500 --timeout 1.5 -o full_scan.json
```

## 🎮 Command Line Options

```
positional arguments:
  host                  Target host IP address or hostname

optional arguments:
  -h, --help           Show help message
  -p, --ports          Port range to scan (default: 1-1024)
                       Examples: 80, 80-443, 80,443,8080
  -t, --threads        Number of threads (default: 100, max: 1000)
  --timeout            Socket timeout in seconds (default: 1.0)
  -o, --output         Save results to JSON file
  -v, --verbose        Enable verbose output
  --banner             Attempt banner grabbing on open ports
```

## 📊 Output Example

```
🔍 PYTHON PORT SCANNER v1.0.0

🎯 Target: 127.0.0.1
📊 Ports: 1024 to scan
⚙️  Threads: 100
⏱️  Timeout: 1.0s

🔄 Scanning in progress...

📈 Progress: 100/1024 (9.8%)
📈 Progress: 200/1024 (19.5%)
...

======================================================================
SCAN RESULTS
======================================================================

PORT      STATUS      SERVICE             BANNER
----------------------------------------------------------------------
22        open        SSH
80        open        HTTP
443       open        HTTPS
3306      open        MySQL
----------------------------------------------------------------------

✅ Found 4 open port(s)
⏱️  Scan duration: 12.34 seconds
======================================================================
```

## 🔧 Project Structure

```
port-scanner/
├── main.py              # Entry point with CLI
├── scanner.py           # Core scanning logic
├── utils.py             # Helper functions
├── requirements.txt     # Dependencies
├── README.md           # This file
└── LICENSE             # MIT License
```

## 📚 How It Works

1. **Argument Parsing** - `main.py` parses command-line arguments
2. **Input Validation** - `utils.py` validates IP addresses and port ranges
3. **Concurrent Scanning** - `scanner.py` uses `ThreadPoolExecutor` for fast parallel scanning
4. **Service Detection** - Common ports are mapped to service names
5. **Results Compilation** - Open ports and banners are collected and displayed
6. **Export** - Results can be saved to JSON format

## 🎯 Use Cases

- 🔐 **Security Testing** - Identify open ports on authorized systems
- 🌐 **Network Diagnostics** - Discover available services on your network
- 📚 **Learning** - Understand Python networking and concurrency
- 🔍 **Troubleshooting** - Find unexpectedly open ports
- 📋 **Network Inventory** - Document services running on hosts

## ⚠️ Important Disclaimer

**LEGAL NOTICE:**
- ✅ **DO** only scan networks and hosts you own or have explicit written permission to scan
- ❌ **DO NOT** use this tool for unauthorized scanning
- ⚖️ Unauthorized port scanning may be illegal in your jurisdiction
- 📜 The author assumes no liability for unauthorized use

This tool is intended for **educational purposes** and **authorized security testing only**.

## 🚀 Performance Tips

- **Increase threads** for faster scanning (e.g., `-t 500`)
- **Reduce timeout** for faster responses (e.g., `--timeout 0.5`)
- **Target specific ports** instead of full ranges when possible
- **Run from a machine close to the target** for better performance

## 🐛 Troubleshooting

### "Hostname could not be resolved"
```bash
# Make sure the hostname/IP is correct and reachable
python main.py 8.8.8.8  # Try with IP instead of hostname
```

### Scan is very slow
```bash
# Increase thread count and reduce timeout
python main.py 127.0.0.1 -t 300 --timeout 0.5
```

### Permission denied on some ports
```bash
# On Linux/Mac, you may need root privileges for ports < 1024
sudo python main.py 127.0.0.1 -p 1-1024
```

## 📝 Examples

Check the `examples/` directory for more advanced usage patterns.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Created by [Chandu-909](https://github.com/Chandu-909)

## 🙏 Acknowledgments

- Inspired by Nmap and other network scanning tools
- Built with Python standard library
- Community feedback and suggestions

## 📞 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Stay ethical. Only scan networks you own or have permission to scan.** 🔒