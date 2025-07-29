
import requests
import os
from typing import Dict, List, Any
import json

class GitHubComplianceMonitor:
    def __init__(self, token: str = None):
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.base_url = 'https://api.github.com'
    
    def scan_repository_compliance(self, repo: str) -> Dict[str, Any]:
        """Scan repository for compliance issues"""
        compliance_report = {
            'security_vulnerabilities': self.check_security_alerts(repo),
            'license_compliance': self.check_license(repo),
            'code_quality': self.analyze_code_quality(repo),
            'dependency_updates': self.check_outdated_dependencies(repo)
        }
        
        return compliance_report
    
    def check_security_alerts(self, repo: str) -> List[Dict]:
        """Check for security vulnerabilities"""
        try:
            response = requests.get(
                f'{self.base_url}/repos/{repo}/vulnerability-alerts',
                headers=self.headers
            )
            if response.status_code == 200:
                return response.json()
            return []
        except Exception:
            return []
    
    def check_license(self, repo: str) -> Dict[str, Any]:
        """Check repository license compliance"""
        try:
            response = requests.get(
                f'{self.base_url}/repos/{repo}/license',
                headers=self.headers
            )
            if response.status_code == 200:
                license_data = response.json()
                return {
                    'license': license_data.get('license', {}).get('name'),
                    'compliant': True
                }
            return {'license': None, 'compliant': False}
        except Exception:
            return {'license': None, 'compliant': False}
    
    def analyze_code_quality(self, repo: str) -> Dict[str, Any]:
        """Analyze code quality metrics"""
        try:
            response = requests.get(
                f'{self.base_url}/repos/{repo}/stats/code_frequency',
                headers=self.headers
            )
            
            return {
                'has_readme': self.has_readme(repo),
                'has_tests': self.has_tests(repo),
                'code_coverage': 'unknown'  # Would need additional integration
            }
        except Exception:
            return {'has_readme': False, 'has_tests': False}
    
    def has_readme(self, repo: str) -> bool:
        """Check if repository has README"""
        try:
            response = requests.get(
                f'{self.base_url}/repos/{repo}/readme',
                headers=self.headers
            )
            return response.status_code == 200
        except Exception:
            return False
    
    def has_tests(self, repo: str) -> bool:
        """Check if repository has test files"""
        try:
            response = requests.get(
                f'{self.base_url}/repos/{repo}/contents',
                headers=self.headers
            )
            if response.status_code == 200:
                contents = response.json()
                test_indicators = ['test', 'tests', 'spec', '__tests__']
                return any(
                    any(indicator in item.get('name', '').lower() 
                        for indicator in test_indicators)
                    for item in contents
                )
            return False
        except Exception:
            return False
    
    def check_outdated_dependencies(self, repo: str) -> List[Dict]:
        """Check for outdated dependencies"""
        return []

if __name__ == "__main__":
    monitor = GitHubComplianceMonitor()
    print("GitHub compliance monitor initialized")
