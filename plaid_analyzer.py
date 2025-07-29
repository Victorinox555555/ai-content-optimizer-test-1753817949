
import plaid
from plaid.api import plaid_api
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from datetime import datetime, timedelta
import os

class PlaidExpenseAnalyzer:
    def __init__(self):
        configuration = plaid.Configuration(
            host=getattr(plaid.Environment, os.getenv('PLAID_ENV', 'sandbox')),
            api_key={
                'clientId': os.getenv('PLAID_CLIENT_ID'),
                'secret': os.getenv('PLAID_SECRET'),
            }
        )
        api_client = plaid.ApiClient(configuration)
        self.client = plaid_api.PlaidApi(api_client)
    
    def exchange_public_token(self, public_token: str) -> str:
        """Exchange public token for access token"""
        request = ItemPublicTokenExchangeRequest(
            public_token=public_token
        )
        response = self.client.item_public_token_exchange(request)
        return response['access_token']
    
    def get_accounts(self, access_token: str) -> list:
        """Get user accounts"""
        request = AccountsGetRequest(access_token=access_token)
        response = self.client.accounts_get(request)
        return response['accounts']
    
    def get_transactions(self, access_token: str, days: int = 30) -> list:
        """Get recent transactions"""
        start_date = datetime.now() - timedelta(days=days)
        end_date = datetime.now()
        
        request = TransactionsGetRequest(
            access_token=access_token,
            start_date=start_date.date(),
            end_date=end_date.date()
        )
        response = self.client.transactions_get(request)
        return response['transactions']
    
    def analyze_recurring_expenses(self, transactions: list) -> dict:
        """Identify recurring wasteful expenses"""
        recurring_patterns = {}
        
        for transaction in transactions:
            merchant = transaction.get('merchant_name', 'Unknown')
            amount = abs(transaction.get('amount', 0))
            category = transaction.get('category', ['Other'])[0]
            
            if merchant not in recurring_patterns:
                recurring_patterns[merchant] = {
                    'transactions': [],
                    'total_amount': 0,
                    'category': category
                }
            
            recurring_patterns[merchant]['transactions'].append(transaction)
            recurring_patterns[merchant]['total_amount'] += amount
        
        wasteful_expenses = []
        for merchant, data in recurring_patterns.items():
            if len(data['transactions']) >= 3:  # Recurring (3+ times)
                avg_amount = data['total_amount'] / len(data['transactions'])
                if avg_amount > 10:  # Above $10 threshold
                    wasteful_expenses.append({
                        'merchant': merchant,
                        'frequency': len(data['transactions']),
                        'total_spent': data['total_amount'],
                        'average_amount': avg_amount,
                        'category': data['category'],
                        'waste_score': self._calculate_waste_score(data)
                    })
        
        return {
            'recurring_expenses': sorted(wasteful_expenses, key=lambda x: x['waste_score'], reverse=True),
            'total_recurring_spend': sum(exp['total_spent'] for exp in wasteful_expenses),
            'potential_savings': sum(exp['total_spent'] * 0.3 for exp in wasteful_expenses)  # 30% potential savings
        }
    
    def _calculate_waste_score(self, expense_data: dict) -> float:
        """Calculate waste score based on frequency and amount"""
        frequency = len(expense_data['transactions'])
        total_amount = expense_data['total_amount']
        
        score = (frequency * 10) + (total_amount * 0.1)
        
        wasteful_categories = ['Entertainment', 'Food and Drink', 'Shops']
        if expense_data['category'] in wasteful_categories:
            score *= 1.5
        
        return min(100, score)

if __name__ == "__main__":
    analyzer = PlaidExpenseAnalyzer()
    print("Plaid expense analyzer initialized")
