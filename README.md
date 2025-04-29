# Network Security Monitoring System

A comprehensive network security monitoring system that combines Suricata IDS with custom security rules and monitoring capabilities.

## Components

- **IDS System**: Suricata-based intrusion detection with custom rules
- **Security Gateway**: NGINX-based gateway for traffic management
- **Monitoring**: Prometheus metrics for security event monitoring
- **Testing Tools**: Scripts for simulating various attack patterns

## Features

- SQL Injection detection
- Cross-site Scripting (XSS) detection
- Directory traversal prevention
- Command injection detection
- Suspicious user agent monitoring
- Large POST request detection
- Brute force attack prevention
- Data exfiltration monitoring
- Cryptocurrency mining detection
- Malware communication pattern detection

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/network-security-lab.git
   cd network-security-lab
   ```

2. Build and start the containers:
   ```bash
   docker-compose build
   docker-compose up -d
   ```

3. Access the monitoring dashboard:
   - Gateway: http://localhost:8080
   - Prometheus metrics: http://localhost:9090

## Testing

Run the security testing suite:
```bash
python3 scripts/test_security.py
```

## Directory Structure

```
.
├── config/
│   ├── suricata.yaml
│   └── custom.rules
├── scripts/
│   ├── ids_monitor.py
│   └── test_security.py
├── Dockerfile.ids
├── Dockerfile.gateway
├── docker-compose.yml
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 