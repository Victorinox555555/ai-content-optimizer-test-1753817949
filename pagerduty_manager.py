
import requests
import os
from typing import Dict, List, Any
import json

class PagerDutyManager:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('PAGERDUTY_API_KEY')
        self.headers = {
            'Authorization': f'Token token={self.api_key}',
            'Accept': 'application/vnd.pagerduty+json;version=2',
            'Content-Type': 'application/json'
        }
        self.base_url = 'https://api.pagerduty.com'
    
    def create_incident(self, title: str, service_id: str, urgency: str = 'high') -> Dict[str, Any]:
        """Create a new incident"""
        payload = {
            'incident': {
                'type': 'incident',
                'title': title,
                'service': {
                    'id': service_id,
                    'type': 'service_reference'
                },
                'urgency': urgency
            }
        }
        
        try:
            response = requests.post(
                f'{self.base_url}/incidents',
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': str(e)}
    
    def get_incidents(self, status: str = 'open') -> List[Dict]:
        """Get incidents by status"""
        params = {'statuses[]': status}
        
        try:
            response = requests.get(
                f'{self.base_url}/incidents',
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            return response.json().get('incidents', [])
        except Exception as e:
            return []
    
    def resolve_incident(self, incident_id: str) -> Dict[str, Any]:
        """Resolve an incident"""
        payload = {
            'incident': {
                'type': 'incident',
                'status': 'resolved'
            }
        }
        
        try:
            response = requests.put(
                f'{self.base_url}/incidents/{incident_id}',
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': str(e)}

if __name__ == "__main__":
    manager = PagerDutyManager()
    print("PagerDuty incident manager initialized")
