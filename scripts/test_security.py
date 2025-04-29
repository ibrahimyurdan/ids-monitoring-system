#!/usr/bin/env python3

import requests
import time
import random
import logging
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecurityTester:
    def __init__(self, target_url="http://localhost:8080"):
        self.target_url = target_url
        self.attack_patterns = {
            'sql_injection': [
                "' OR '1'='1",
                "UNION SELECT * FROM users",
                "'; DROP TABLE users--",
            ],
            'xss': [
                "<script>alert('xss')</script>",
                "<img src=x onerror=alert('xss')>",
                "javascript:alert('xss')",
            ],
            'directory_traversal': [
                "../../../etc/passwd",
                "..\\..\\windows\\system32",
                "....//....//etc/hosts",
            ],
            'command_injection': [
                "; cat /etc/passwd",
                "| ls -la",
                "`whoami`",
            ],
            'large_request': [
                "A" * 1000000,  # 1MB of data
            ]
        }

    def simulate_normal_traffic(self):
        """Simulate normal web traffic"""
        try:
            endpoints = ['/', '/api', '/about', '/contact']
            endpoint = random.choice(endpoints)
            response = requests.get(f"{self.target_url}{endpoint}")
            logger.info(f"Normal traffic - Status: {response.status_code}")
        except Exception as e:
            logger.error(f"Error in normal traffic simulation: {e}")

    def simulate_attack(self, attack_type):
        """Simulate various types of attacks"""
        try:
            if attack_type not in self.attack_patterns:
                logger.error(f"Unknown attack type: {attack_type}")
                return

            patterns = self.attack_patterns[attack_type]
            pattern = random.choice(patterns)
            
            # Simulate different types of requests
            if attack_type == 'large_request':
                response = requests.post(self.target_url, data={'payload': pattern})
            else:
                response = requests.get(f"{self.target_url}?q={pattern}")
                
            logger.info(f"Attack simulation ({attack_type}) - Status: {response.status_code}")
            
        except Exception as e:
            logger.error(f"Error in attack simulation: {e}")

    def run_security_test(self, duration=300):
        """Run security tests for specified duration"""
        logger.info("Starting security testing...")
        
        end_time = time.time() + duration
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            while time.time() < end_time:
                # 80% normal traffic, 20% attack traffic
                if random.random() < 0.8:
                    executor.submit(self.simulate_normal_traffic)
                else:
                    attack_type = random.choice(list(self.attack_patterns.keys()))
                    executor.submit(self.simulate_attack, attack_type)
                    
                time.sleep(random.uniform(0.1, 0.5))

def main():
    tester = SecurityTester()
    
    # Run tests for 5 minutes
    logger.info("Starting security testing suite")
    tester.run_security_test(duration=300)
    logger.info("Security testing completed")

if __name__ == "__main__":
    main() 