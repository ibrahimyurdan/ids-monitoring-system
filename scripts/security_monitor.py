#!/usr/bin/env python3

import time
import json
import logging
from datetime import datetime
from prometheus_client import start_http_server, Counter, Gauge
import pandas as pd
from sklearn.ensemble import IsolationForest

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/security/security_monitor.log'),
        logging.StreamHandler()
    ]
)

# Prometheus metrics
SECURITY_EVENTS = Counter('security_events_total', 'Total security events detected')
THREAT_LEVEL = Gauge('threat_level', 'Current threat level')
ANOMALY_SCORE = Gauge('anomaly_score', 'Current anomaly score')

class SecurityMonitor:
    def __init__(self):
        self.anomaly_detector = IsolationForest(contamination=0.1)
        self.events_history = []
        
    def analyze_logs(self):
        """Analyze security logs for potential threats"""
        try:
            # Simulate log analysis (replace with actual log parsing)
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            logging.info(f"Analyzing logs at {current_time}")
            
            # Example: Parse Suricata alerts
            with open('/var/log/suricata/fast.log', 'r') as f:
                alerts = f.readlines()
                for alert in alerts:
                    self.process_alert(alert)
                    
        except Exception as e:
            logging.error(f"Error analyzing logs: {e}")
    
    def process_alert(self, alert):
        """Process individual security alerts"""
        try:
            # Parse alert and update metrics
            SECURITY_EVENTS.inc()
            
            # Add to events history for anomaly detection
            event_data = self.parse_alert(alert)
            self.events_history.append(event_data)
            
            # Perform anomaly detection
            if len(self.events_history) > 100:
                self.detect_anomalies()
                
        except Exception as e:
            logging.error(f"Error processing alert: {e}")
    
    def detect_anomalies(self):
        """Perform anomaly detection on security events"""
        try:
            # Convert events to features
            df = pd.DataFrame(self.events_history)
            
            # Fit and predict
            scores = self.anomaly_detector.fit_predict(df)
            
            # Update anomaly score
            anomaly_ratio = (scores == -1).sum() / len(scores)
            ANOMALY_SCORE.set(anomaly_ratio)
            
            # Update threat level based on anomalies
            threat_level = min(anomaly_ratio * 10, 1.0)
            THREAT_LEVEL.set(threat_level)
            
            logging.info(f"Current threat level: {threat_level:.2f}")
            
        except Exception as e:
            logging.error(f"Error in anomaly detection: {e}")
    
    def parse_alert(self, alert):
        """Parse alert into structured data"""
        # Example parsing (customize based on your alert format)
        return {
            'timestamp': datetime.now().timestamp(),
            'severity': 1.0,  # Example feature
            'source_ip': '0.0.0.0',  # Example feature
        }

def main():
    # Start Prometheus metrics server
    start_http_server(9090)
    logging.info("Started Prometheus metrics server on port 9090")
    
    # Initialize security monitor
    monitor = SecurityMonitor()
    logging.info("Security monitoring system initialized")
    
    # Main monitoring loop
    while True:
        monitor.analyze_logs()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main() 