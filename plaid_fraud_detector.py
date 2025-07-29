
import requests
import os
from typing import Dict, List, Any
import json
from datetime import datetime, timedelta

class PlaidFraudDetector:
    def __init__(self, client_id: str = None, secret: str = None):
        self.client_id = client_id or os.getenv('PLAID_CLIENT_ID')
        self.secret = secret or os.getenv('PLAID_SECRET')
        self.base_url = 'https://production.plaid.com'
        
    def analyze_transaction_patterns(self, access_token: str, days: int = 30) -> Dict[str, Any]:
        """Analyze transaction patterns for fraud detection"""
        transactions = self.get_transactions(access_token, days)
        
        fraud_indicators = {
            'unusual_amounts': self.detect_unusual_amounts(transactions),
            'suspicious_merchants': self.detect_suspicious_merchants(transactions),
            'velocity_anomalies': self.detect_velocity_anomalies(transactions),
            'location_anomalies': self.detect_location_anomalies(transactions),
            'risk_score': 0
        }
        
        risk_factors = sum([
            len(fraud_indicators['unusual_amounts']) * 2,
            len(fraud_indicators['suspicious_merchants']) * 3,
            len(fraud_indicators['velocity_anomalies']) * 4,
            len(fraud_indicators['location_anomalies']) * 2
        ])
        
        fraud_indicators['risk_score'] = min(100, risk_factors * 5)
        fraud_indicators['alert_level'] = self.get_alert_level(fraud_indicators['risk_score'])
        
        return fraud_indicators
    
    def get_transactions(self, access_token: str, days: int) -> List[Dict]:
        """Fetch recent transactions from Plaid"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        payload = {
            'client_id': self.client_id,
            'secret': self.secret,
            'access_token': access_token,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        }
        
        try:
            response = requests.post(
                f'{self.base_url}/transactions/get',
                json=payload
            )
            if response.status_code == 200:
                return response.json().get('transactions', [])
        except Exception:
            pass
        
        return []
    
    def detect_unusual_amounts(self, transactions: List[Dict]) -> List[Dict]:
        """Detect transactions with unusual amounts"""
        if not transactions:
            return []
        
        amounts = [abs(t.get('amount', 0)) for t in transactions]
        avg_amount = sum(amounts) / len(amounts)
        
        unusual = []
        for transaction in transactions:
            amount = abs(transaction.get('amount', 0))
            if amount > avg_amount * 3:  # 3x average
                unusual.append({
                    'transaction_id': transaction.get('transaction_id'),
                    'amount': amount,
                    'merchant': transaction.get('merchant_name'),
                    'reason': f'Amount ${amount:.2f} is {amount/avg_amount:.1f}x average'
                })
        
        return unusual
    
    def detect_suspicious_merchants(self, transactions: List[Dict]) -> List[Dict]:
        """Detect transactions with suspicious merchant patterns"""
        suspicious_keywords = ['cash advance', 'atm', 'wire transfer', 'money order']
        suspicious = []
        
        for transaction in transactions:
            merchant = transaction.get('merchant_name', '').lower()
            if any(keyword in merchant for keyword in suspicious_keywords):
                suspicious.append({
                    'transaction_id': transaction.get('transaction_id'),
                    'merchant': transaction.get('merchant_name'),
                    'amount': transaction.get('amount'),
                    'reason': 'Suspicious merchant category'
                })
        
        return suspicious
    
    def detect_velocity_anomalies(self, transactions: List[Dict]) -> List[Dict]:
        """Detect rapid-fire transactions (velocity fraud)"""
        if len(transactions) < 2:
            return []
        
        sorted_transactions = sorted(transactions, key=lambda x: x.get('date', ''))
        anomalies = []
        
        for i in range(1, len(sorted_transactions)):
            current = sorted_transactions[i]
            previous = sorted_transactions[i-1]
            
            if current.get('date') == previous.get('date'):
                anomalies.append({
                    'transaction_ids': [current.get('transaction_id'), previous.get('transaction_id')],
                    'reason': 'Multiple transactions on same date',
                    'total_amount': abs(current.get('amount', 0)) + abs(previous.get('amount', 0))
                })
        
        return anomalies
    
    def detect_location_anomalies(self, transactions: List[Dict]) -> List[Dict]:
        """Detect geographically impossible transactions"""
        locations = {}
        anomalies = []
        
        for transaction in transactions:
            location = transaction.get('location', {})
            if location:
                city = location.get('city')
                if city and city not in locations:
                    locations[city] = transaction
                elif city and city in locations:
                    anomalies.append({
                        'transaction_id': transaction.get('transaction_id'),
                        'location': city,
                        'reason': 'Multiple geographic locations'
                    })
        
        return anomalies
    
    def get_alert_level(self, risk_score: int) -> str:
        """Get alert level based on risk score"""
        if risk_score >= 80:
            return 'HIGH'
        elif risk_score >= 50:
            return 'MEDIUM'
        elif risk_score >= 20:
            return 'LOW'
        else:
            return 'NONE'

if __name__ == "__main__":
    detector = PlaidFraudDetector()
    print("Plaid fraud detection system initialized")
