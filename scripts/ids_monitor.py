#!/usr/bin/env python3

import time
import json
import logging
import subprocess
from datetime import datetime
from prometheus_client import start_http_server, Counter, Gauge, Histogram
import yaml

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/suricata/ids_monitor.log'),
        logging.StreamHandler()
    ]
)

# Prometheus metrics
ALERT_COUNTER = Counter('suricata_alerts_total', 'Total number of Suricata alerts', ['category', 'severity'])
ALERT_SEVERITY = Gauge('alert_severity', 'Current alert severity level')
PACKET_COUNTER = Counter('packets_processed_total', 'Total number of packets processed')
ALERT_LATENCY = Histogram('alert_processing_seconds', 'Time spent processing alerts')

class IDSMonitor:
    def __init__(self):
        self.alert_categories = {
            'sql_injection': 0,
            'xss': 0,
            'directory_traversal': 0,
            'command_injection': 0,
            'brute_force': 0
        }
        
    def start_suricata(self):
        """Start Suricata IDS"""
        try:
            subprocess.Popen(['suricata', '-c', '/etc/suricata/suricata.yaml', '-i', 'eth0'])
            logging.info("Suricata started successfully")
        except Exception as e:
            logging.error(f"Failed to start Suricata: {e}")
            
    def parse_eve_json(self):
        """Parse Suricata eve.json file for alerts"""
        try:
            with open('/var/log/suricata/eve.json', 'r') as f:
                for line in f:
                    try:
                        event = json.loads(line)
                        if event.get('event_type') == 'alert':
                            self.process_alert(event)
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            logging.error(f"Error parsing eve.json: {e}")
            
    def process_alert(self, alert):
        """Process and categorize alerts"""
        with ALERT_LATENCY.time():
            try:
                signature = alert.get('alert', {}).get('signature', '')
                category = self.categorize_alert(signature)
                severity = alert.get('alert', {}).get('severity', 1)
                
                # Update Prometheus metrics
                ALERT_COUNTER.labels(category=category, severity=severity).inc()
                ALERT_SEVERITY.set(severity)
                
                # Log alert details
                logging.info(f"Alert detected - Category: {category}, Severity: {severity}")
                
                # Update alert categories
                if category in self.alert_categories:
                    self.alert_categories[category] += 1
                    
            except Exception as e:
                logging.error(f"Error processing alert: {e}")
                
    def categorize_alert(self, signature):
        """Categorize alerts based on signature"""
        signature = signature.lower()
        if 'sql' in signature:
            return 'sql_injection'
        elif 'xss' in signature or 'script' in signature:
            return 'xss'
        elif 'directory' in signature or '../' in signature:
            return 'directory_traversal'
        elif 'command' in signature:
            return 'command_injection'
        elif 'brute' in signature:
            return 'brute_force'
        return 'other'
        
    def monitor_traffic(self):
        """Monitor network traffic statistics"""
        try:
            result = subprocess.run(['tcpdump', '-i', 'eth0', '-c', '1', '-w', '/dev/null'],
                                 capture_output=True, text=True)
            PACKET_COUNTER.inc()
        except Exception as e:
            logging.error(f"Error monitoring traffic: {e}")

def main():
    # Start Prometheus metrics server
    start_http_server(9090)
    logging.info("Started Prometheus metrics server on port 9090")
    
    # Initialize IDS monitor
    monitor = IDSMonitor()
    monitor.start_suricata()
    logging.info("IDS monitoring system initialized")
    
    # Main monitoring loop
    while True:
        monitor.parse_eve_json()
        monitor.monitor_traffic()
        time.sleep(1)  # Check every second

if __name__ == "__main__":
    main() 