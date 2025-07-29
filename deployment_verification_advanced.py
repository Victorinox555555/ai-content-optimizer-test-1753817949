#!/usr/bin/env python3
"""
Advanced Deployment Verification System
Comprehensive testing suite for autonomous deployment validation
"""

import requests
import json
import time
import os
from typing import Dict, List, Any, Optional
from urllib.parse import urljoin
import subprocess

class AdvancedDeploymentVerifier:
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.test_results = []
    
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test result"""
        result = {
            'test': test_name,
            'success': success,
            'details': details,
            'timestamp': time.time()
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {details}")
    
    def test_ssl_certificate(self) -> bool:
        """Verify SSL certificate is valid"""
        try:
            response = self.session.get(self.base_url, timeout=self.timeout, verify=True)
            self.log_test("SSL Certificate", True, "Valid SSL certificate")
            return True
        except requests.exceptions.SSLError as e:
            self.log_test("SSL Certificate", False, f"SSL Error: {str(e)}")
            return False
        except Exception as e:
            self.log_test("SSL Certificate", False, f"Connection Error: {str(e)}")
            return False
    
    def test_security_headers(self) -> bool:
        """Verify security headers are present"""
        try:
            response = self.session.get(self.base_url, timeout=self.timeout)
            headers = response.headers
            
            required_headers = {
                'X-Content-Type-Options': 'nosniff',
                'X-Frame-Options': 'DENY',
                'X-XSS-Protection': '1; mode=block',
                'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'
            }
            
            missing_headers = []
            for header, expected_value in required_headers.items():
                if header not in headers:
                    missing_headers.append(header)
                elif expected_value and headers[header] != expected_value:
                    missing_headers.append(f"{header} (incorrect value)")
            
            if missing_headers:
                self.log_test("Security Headers", False, f"Missing: {', '.join(missing_headers)}")
                return False
            else:
                self.log_test("Security Headers", True, "All security headers present")
                return True
                
        except Exception as e:
            self.log_test("Security Headers", False, f"Error: {str(e)}")
            return False
    
    def test_performance_metrics(self) -> bool:
        """Test page load performance"""
        try:
            start_time = time.time()
            response = self.session.get(self.base_url, timeout=self.timeout)
            load_time = time.time() - start_time
            
            if load_time < 3.0:  # Under 3 seconds is good
                self.log_test("Performance", True, f"Page loaded in {load_time:.2f}s")
                return True
            else:
                self.log_test("Performance", False, f"Slow load time: {load_time:.2f}s")
                return False
                
        except Exception as e:
            self.log_test("Performance", False, f"Error: {str(e)}")
            return False
    
    def test_api_endpoints(self) -> bool:
        """Test all API endpoints"""
        endpoints = [
            ('/api/health', 'GET', 200),
            ('/api/signup', 'POST', [400, 409]),  # Bad request or conflict expected without data
            ('/api/login', 'POST', [400, 401]),   # Bad request or unauthorized expected
            ('/api/create-checkout-session', 'POST', [400, 500])  # Bad request expected without data
        ]
        
        all_passed = True
        for endpoint, method, expected_codes in endpoints:
            try:
                url = urljoin(self.base_url, endpoint)
                if method == 'GET':
                    response = self.session.get(url, timeout=self.timeout)
                else:
                    response = self.session.post(url, json={}, timeout=self.timeout)
                
                if isinstance(expected_codes, list):
                    success = response.status_code in expected_codes
                else:
                    success = response.status_code == expected_codes
                
                if success:
                    self.log_test(f"API {endpoint}", True, f"Status: {response.status_code}")
                else:
                    self.log_test(f"API {endpoint}", False, f"Unexpected status: {response.status_code}")
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"API {endpoint}", False, f"Error: {str(e)}")
                all_passed = False
        
        return all_passed
    
    def test_database_connectivity(self) -> bool:
        """Test database connectivity through health endpoint"""
        try:
            url = urljoin(self.base_url, '/api/health')
            response = self.session.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                db_status = data.get('database', 'unknown')
                
                if db_status == 'connected':
                    self.log_test("Database Connectivity", True, "Database connected")
                    return True
                else:
                    self.log_test("Database Connectivity", False, f"Database status: {db_status}")
                    return False
            else:
                self.log_test("Database Connectivity", False, f"Health check failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Database Connectivity", False, f"Error: {str(e)}")
            return False
    
    def test_user_registration_flow(self) -> bool:
        """Test complete user registration flow"""
        try:
            signup_url = urljoin(self.base_url, '/api/signup')
            test_user = {
                'email': f'test_{int(time.time())}@example.com',
                'password': 'TestPassword123!'
            }
            
            response = self.session.post(signup_url, json=test_user, timeout=self.timeout)
            
            if response.status_code in [200, 201]:
                data = response.json()
                if data.get('success'):
                    self.log_test("User Registration", True, f"User created with ID: {data.get('user_id')}")
                    return True
                else:
                    self.log_test("User Registration", False, f"Signup failed: {data.get('error', 'Unknown error')}")
                    return False
            else:
                self.log_test("User Registration", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("User Registration", False, f"Error: {str(e)}")
            return False
    
    def test_payment_integration(self) -> bool:
        """Test payment system integration"""
        try:
            checkout_url = urljoin(self.base_url, '/api/create-checkout-session')
            response = self.session.post(checkout_url, json={'plan': 'basic'}, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('checkout_url'):
                    self.log_test("Payment Integration", True, "Stripe checkout session created")
                    return True
                else:
                    self.log_test("Payment Integration", False, f"Checkout failed: {data.get('error')}")
                    return False
            else:
                self.log_test("Payment Integration", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Payment Integration", False, f"Error: {str(e)}")
            return False
    
    def test_responsive_design(self) -> bool:
        """Test responsive design by checking viewport meta tag"""
        try:
            response = self.session.get(self.base_url, timeout=self.timeout)
            html_content = response.text
            
            if 'viewport' in html_content and 'width=device-width' in html_content:
                self.log_test("Responsive Design", True, "Viewport meta tag present")
                return True
            else:
                self.log_test("Responsive Design", False, "Missing viewport meta tag")
                return False
                
        except Exception as e:
            self.log_test("Responsive Design", False, f"Error: {str(e)}")
            return False
    
    def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run all verification tests"""
        print(f"\n🔍 Running Comprehensive Deployment Verification")
        print(f"Target URL: {self.base_url}")
        print("=" * 60)
        
        tests = [
            self.test_ssl_certificate,
            self.test_security_headers,
            self.test_performance_metrics,
            self.test_api_endpoints,
            self.test_database_connectivity,
            self.test_user_registration_flow,
            self.test_payment_integration,
            self.test_responsive_design
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
        
        print("=" * 60)
        print(f"📊 Test Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        report = {
            'url': self.base_url,
            'timestamp': time.time(),
            'total_tests': total,
            'passed_tests': passed,
            'success_rate': passed / total,
            'overall_status': 'PASS' if passed == total else 'PARTIAL' if passed > total * 0.7 else 'FAIL',
            'detailed_results': self.test_results
        }
        
        return report
    
    def generate_report_file(self, report: Dict[str, Any], filename: str = "deployment_verification_report.json"):
        """Generate detailed report file"""
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"📄 Detailed report saved to: {filename}")

def main():
    """Main verification function"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python deployment_verification_advanced.py <base_url>")
        sys.exit(1)
    
    base_url = sys.argv[1]
    verifier = AdvancedDeploymentVerifier(base_url)
    
    report = verifier.run_comprehensive_test()
    verifier.generate_report_file(report)
    
    if report['overall_status'] == 'PASS':
        print("\n🎉 All tests passed! Deployment is fully verified.")
        sys.exit(0)
    elif report['overall_status'] == 'PARTIAL':
        print(f"\n⚠️  Partial success: {report['passed_tests']}/{report['total_tests']} tests passed.")
        sys.exit(1)
    else:
        print(f"\n❌ Deployment verification failed: {report['passed_tests']}/{report['total_tests']} tests passed.")
        sys.exit(2)

if __name__ == "__main__":
    main()
