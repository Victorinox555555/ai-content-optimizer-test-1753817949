import requests
import json
from typing import Dict, Any, List, Optional

class EmailIntegration:
    def __init__(self, credentials: Dict[str, str]):
        self.credentials = credentials
        self.services = {}
        
        if credentials.get('SENDGRID_API_KEY'):
            self.services['sendgrid'] = SendGridIntegration(credentials['SENDGRID_API_KEY'])
        
        if credentials.get('MAILGUN_API_KEY') and credentials.get('MAILGUN_DOMAIN'):
            self.services['mailgun'] = MailgunIntegration(
                credentials['MAILGUN_API_KEY'],
                credentials['MAILGUN_DOMAIN']
            )
        
        if credentials.get('SES_ACCESS_KEY') and credentials.get('SES_SECRET_KEY'):
            self.services['ses'] = SESIntegration(
                credentials['SES_ACCESS_KEY'],
                credentials['SES_SECRET_KEY'],
                credentials.get('SES_REGION', 'us-east-1')
            )
    
    def setup_email_service(self, app_name: str, from_email: str) -> Dict[str, Any]:
        """Set up email service for the application"""
        results = {}
        
        for service_name, service in self.services.items():
            try:
                result = service.setup_email_service(app_name, from_email)
                results[service_name] = result
            except Exception as e:
                results[service_name] = {
                    "success": False,
                    "error": f"Failed to setup {service_name}: {str(e)}"
                }
        
        return {
            "success": len([r for r in results.values() if r.get("success")]) > 0,
            "services": results,
            "total_services": len(self.services),
            "recommended_service": self._get_recommended_service(results)
        }
    
    def _get_recommended_service(self, results: Dict[str, Any]) -> str:
        """Get the recommended email service based on setup results"""
        successful_services = [name for name, result in results.items() if result.get("success")]
        
        if "sendgrid" in successful_services:
            return "sendgrid"
        elif "mailgun" in successful_services:
            return "mailgun"
        elif "ses" in successful_services:
            return "ses"
        else:
            return "none"

class SendGridIntegration:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.sendgrid.com/v3"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def setup_email_service(self, app_name: str, from_email: str) -> Dict[str, Any]:
        """Set up SendGrid email service"""
        try:
            verify_result = self._verify_api_key()
            if not verify_result["success"]:
                return verify_result
            
            sender_result = self._create_sender_identity(from_email, app_name)
            
            templates = self._generate_email_templates(app_name)
            
            return {
                "success": True,
                "service": "SendGrid",
                "sender_identity": sender_result,
                "templates": templates,
                "integration_code": self._generate_sendgrid_code(from_email)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"SendGrid setup failed: {str(e)}"
            }
    
    def _verify_api_key(self) -> Dict[str, Any]:
        """Verify SendGrid API key"""
        try:
            response = requests.get(
                f"{self.base_url}/user/account",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return {"success": True, "message": "API key verified"}
            else:
                return {
                    "success": False,
                    "error": f"API key verification failed: {response.text}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"API key verification error: {str(e)}"
            }
    
    def _create_sender_identity(self, from_email: str, app_name: str) -> Dict[str, Any]:
        """Create sender identity in SendGrid"""
        try:
            payload = {
                "nickname": f"{app_name} Sender",
                "from": {
                    "email": from_email,
                    "name": app_name
                },
                "reply_to": {
                    "email": from_email,
                    "name": app_name
                },
                "address": "123 Main St",
                "city": "San Francisco",
                "state": "CA",
                "zip": "94105",
                "country": "US"
            }
            
            response = requests.post(
                f"{self.base_url}/verified_senders",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code in [200, 201]:
                return {
                    "success": True,
                    "message": "Sender identity created",
                    "from_email": from_email
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to create sender identity: {response.text}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Sender identity creation error: {str(e)}"
            }
    
    def _generate_email_templates(self, app_name: str) -> Dict[str, str]:
        """Generate email templates"""
        return {
            "welcome": f"""
Subject: Welcome to {app_name}!

Hello {{{{name}}}},

Welcome to {app_name}! We're excited to have you on board.

Your account has been successfully created and you can now start using our service.

Best regards,
The {app_name} Team
""",
            "password_reset": f"""
Subject: Password Reset Request - {app_name}

Hello {{{{name}}}},

You requested a password reset for your {app_name} account.

Click the link below to reset your password:
{{{{reset_link}}}}

If you didn't request this, please ignore this email.

Best regards,
The {app_name} Team
""",
            "subscription_confirmation": f"""
Subject: Subscription Confirmed - {app_name}

Hello {{{{name}}}},

Thank you for subscribing to {app_name}!

Your subscription details:
- Plan: {{{{plan_name}}}}
- Amount: ${{{{amount}}}}
- Next billing date: {{{{next_billing_date}}}}

Best regards,
The {app_name} Team
"""
        }
    
    def _generate_sendgrid_code(self, from_email: str) -> str:
        """Generate Python code for SendGrid integration"""
        return f"""
import sendgrid
from sendgrid.helpers.mail import Mail

sg = sendgrid.SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))

def send_email(to_email, subject, content, from_email='{from_email}'):
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=content
    )
    
    try:
        response = sg.send(message)
        return {{"success": True, "status_code": response.status_code}}
    except Exception as e:
        return {{"success": False, "error": str(e)}}

def send_welcome_email(user_email, user_name):
    subject = "Welcome to {app_name}!"
    content = f"Hello {{user_name}}, welcome to our service!"
    return send_email(user_email, subject, content)
"""

class MailgunIntegration:
    def __init__(self, api_key: str, domain: str):
        self.api_key = api_key
        self.domain = domain
        self.base_url = f"https://api.mailgun.net/v3/{domain}"
    
    def setup_email_service(self, app_name: str, from_email: str) -> Dict[str, Any]:
        """Set up Mailgun email service"""
        try:
            verify_result = self._verify_domain()
            if not verify_result["success"]:
                return verify_result
            
            templates = self._generate_email_templates(app_name)
            
            return {
                "success": True,
                "service": "Mailgun",
                "domain": self.domain,
                "templates": templates,
                "integration_code": self._generate_mailgun_code(from_email)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Mailgun setup failed: {str(e)}"
            }
    
    def _verify_domain(self) -> Dict[str, Any]:
        """Verify Mailgun domain"""
        try:
            response = requests.get(
                f"https://api.mailgun.net/v3/domains/{self.domain}",
                auth=("api", self.api_key)
            )
            
            if response.status_code == 200:
                return {"success": True, "message": "Domain verified"}
            else:
                return {
                    "success": False,
                    "error": f"Domain verification failed: {response.text}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Domain verification error: {str(e)}"
            }
    
    def _generate_email_templates(self, app_name: str) -> Dict[str, str]:
        """Generate email templates for Mailgun"""
        return {
            "welcome": f"Welcome to {app_name}! Your account is ready.",
            "password_reset": f"Reset your {app_name} password using this link: {{{{reset_link}}}}",
            "subscription_confirmation": f"Your {app_name} subscription is confirmed!"
        }
    
    def _generate_mailgun_code(self, from_email: str) -> str:
        """Generate Python code for Mailgun integration"""
        return f"""
import requests

def send_email_mailgun(to_email, subject, content, from_email='{from_email}'):
    return requests.post(
        f"https://api.mailgun.net/v3/{{os.getenv('MAILGUN_DOMAIN')}}/messages",
        auth=("api", os.getenv('MAILGUN_API_KEY')),
        data={{
            "from": from_email,
            "to": to_email,
            "subject": subject,
            "html": content
        }}
    )
"""

class SESIntegration:
    def __init__(self, access_key: str, secret_key: str, region: str):
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
    
    def setup_email_service(self, app_name: str, from_email: str) -> Dict[str, Any]:
        """Set up AWS SES email service"""
        try:
            return {
                "success": True,
                "service": "AWS SES",
                "region": self.region,
                "integration_code": self._generate_ses_code(from_email)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"SES setup failed: {str(e)}"
            }
    
    def _generate_ses_code(self, from_email: str) -> str:
        """Generate Python code for SES integration"""
        return f"""
import boto3
from botocore.exceptions import ClientError

ses_client = boto3.client(
    'ses',
    region_name='{self.region}',
    aws_access_key_id=os.getenv('SES_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('SES_SECRET_KEY')
)

def send_email_ses(to_email, subject, content, from_email='{from_email}'):
    try:
        response = ses_client.send_email(
            Source=from_email,
            Destination={{'ToAddresses': [to_email]}},
            Message={{
                'Subject': {{'Data': subject}},
                'Body': {{'Html': {{'Data': content}}}}
            }}
        )
        return {{"success": True, "message_id": response['MessageId']}}
    except ClientError as e:
        return {{"success": False, "error": str(e)}}
"""
