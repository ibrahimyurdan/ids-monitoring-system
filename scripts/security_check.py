#!/usr/bin/env python3

import time
import logging
import subprocess
from prometheus_client import start_http_server, Counter, Gauge

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/nginx/security_check.log'),
        logging.StreamHandler()
    ]
)

# Prometheus metrics
BLOCKED_REQUESTS = Counter('blocked_requests_total', 'Total blocked requests', ['reason'])
ACTIVE_BANS = Gauge('active_bans', 'Number of currently banned IPs')
REQUEST_RATE = Gauge('request_rate', 'Current request rate per second')

class SecurityCheck:
    def __init__(self):
        self.banned_ips = set()
        
    def check_fail2ban_status(self):
        """Check fail2ban status and update metrics"""
        try:
            result = subprocess.run(['fail2ban-client', 'status'], 
                                 capture_output=True, text=True)
            
            # Parse output and update metrics
            if result.stdout:
                banned_count = result.stdout.count('Banned IP list:')
                ACTIVE_BANS.set(banned_count)
                
        except Exception as e:
            logging.error(f"Error checking fail2ban status: {e}")
            
    def monitor_nginx_logs(self):
        """Monitor nginx access logs for suspicious activity"""
        try:
            result = subprocess.run(['tail', '-n', '1', '/var/log/nginx/access.log'],
                                 capture_output=True, text=True)
            
            if '404' in result.stdout:
                BLOCKED_REQUESTS.labels(reason='not_found').inc()
            elif '403' in result.stdout:
                BLOCKED_REQUESTS.labels(reason='forbidden').inc()
                
        except Exception as e:
            logging.error(f"Error monitoring nginx logs: {e}")
            
    def check_request_rate(self):
        """Monitor request rate"""
        try:
            result = subprocess.run(['grep', '-c', '"GET\|POST"', '/var/log/nginx/access.log'],
                                 capture_output=True, text=True)
            
            if result.stdout:
                requests = int(result.stdout.strip())
                REQUEST_RATE.set(requests)
                
        except Exception as e:
            logging.error(f"Error checking request rate: {e}")

def main():
    # Start Prometheus metrics server
    start_http_server(8080)
    logging.info("Started Prometheus metrics server on port 8080")
    
    # Initialize security check
    checker = SecurityCheck()
    logging.info("Security check initialized")
    
    # Main monitoring loop
    while True:
        checker.check_fail2ban_status()
        checker.monitor_nginx_logs()
        checker.check_request_rate()
        time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    main() 