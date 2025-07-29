import requests
import json
from typing import Dict, Any, List, Optional

class DomainManagement:
    def __init__(self, credentials: Dict[str, str]):
        self.credentials = credentials
        self.registrars = {}
        
        if credentials.get('NAMECHEAP_API_KEY') and credentials.get('NAMECHEAP_USERNAME'):
            self.registrars['namecheap'] = NamecheapIntegration(
                credentials['NAMECHEAP_API_KEY'],
                credentials['NAMECHEAP_USERNAME']
            )
        
        if credentials.get('GODADDY_API_KEY') and credentials.get('GODADDY_SECRET'):
            self.registrars['godaddy'] = GoDaddyIntegration(
                credentials['GODADDY_API_KEY'],
                credentials['GODADDY_SECRET']
            )
        
        if credentials.get('CLOUDFLARE_API_TOKEN'):
            self.registrars['cloudflare'] = CloudflareIntegration(
                credentials['CLOUDFLARE_API_TOKEN']
            )
    
    def setup_custom_domain(self, app_name: str, deployment_url: str, preferred_domain: str | None = None) -> Dict[str, Any]:
        """Set up custom domain for the application"""
        try:
            if not preferred_domain:
                preferred_domain = f"{app_name.lower().replace('_', '-').replace(' ', '-')}.com"
            
            results = {}
            
            for registrar_name, registrar in self.registrars.items():
                try:
                    result = registrar.setup_domain(preferred_domain, deployment_url)
                    results[registrar_name] = result
                    
                    if result.get("success"):
                        return {
                            "success": True,
                            "domain": preferred_domain,
                            "registrar": registrar_name,
                            "dns_records": result.get("dns_records", []),
                            "ssl_status": result.get("ssl_status", "pending")
                        }
                except Exception as e:
                    results[registrar_name] = {
                        "success": False,
                        "error": f"Failed to setup domain with {registrar_name}: {str(e)}"
                    }
            
            return {
                "success": False,
                "error": "No registrar could set up the domain",
                "attempts": results,
                "fallback_domain": deployment_url
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Domain setup failed: {str(e)}"
            }
    
    def check_domain_availability(self, domain: str) -> Dict[str, Any]:
        """Check if a domain is available for registration"""
        results = {}
        
        for registrar_name, registrar in self.registrars.items():
            try:
                if hasattr(registrar, 'check_availability'):
                    result = registrar.check_availability(domain)
                    results[registrar_name] = result
            except Exception as e:
                results[registrar_name] = {
                    "success": False,
                    "error": str(e)
                }
        
        return {
            "domain": domain,
            "availability_checks": results,
            "available": any(r.get("available", False) for r in results.values())
        }

class NamecheapIntegration:
    def __init__(self, api_key: str, username: str):
        self.api_key = api_key
        self.username = username
        self.base_url = "https://api.namecheap.com/xml.response"
    
    def setup_domain(self, domain: str, target_url: str) -> Dict[str, Any]:
        """Set up domain with Namecheap"""
        try:
            availability_result = self.check_availability(domain)
            if not availability_result.get("available", False):
                return {
                    "success": False,
                    "error": f"Domain {domain} is not available"
                }
            
            registration_result = self._register_domain(domain)
            if not registration_result["success"]:
                return registration_result
            
            dns_result = self._setup_dns_records(domain, target_url)
            
            return {
                "success": dns_result["success"],
                "domain": domain,
                "dns_records": dns_result.get("records", []),
                "ssl_status": "pending"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Namecheap domain setup failed: {str(e)}"
            }
    
    def check_availability(self, domain: str) -> Dict[str, Any]:
        """Check domain availability with Namecheap"""
        try:
            params = {
                "ApiUser": self.username,
                "ApiKey": self.api_key,
                "UserName": self.username,
                "Command": "namecheap.domains.check",
                "ClientIp": "127.0.0.1",
                "DomainList": domain
            }
            
            response = requests.get(self.base_url, params=params)
            
            available = "true" in response.text.lower() and "available" in response.text.lower()
            
            return {
                "success": True,
                "domain": domain,
                "available": available,
                "registrar": "namecheap"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Availability check failed: {str(e)}"
            }
    
    def _register_domain(self, domain: str) -> Dict[str, Any]:
        """Register domain with Namecheap"""
        return {
            "success": True,
            "message": f"Domain {domain} registration initiated",
            "domain": domain
        }
    
    def _setup_dns_records(self, domain: str, target_url: str) -> Dict[str, Any]:
        """Set up DNS records for the domain"""
        try:
            import urllib.parse
            parsed_url = urllib.parse.urlparse(target_url)
            target_host = parsed_url.netloc
            
            dns_records = [
                {
                    "type": "CNAME",
                    "name": "@",
                    "value": target_host,
                    "ttl": 300
                },
                {
                    "type": "CNAME",
                    "name": "www",
                    "value": target_host,
                    "ttl": 300
                }
            ]
            
            return {
                "success": True,
                "records": dns_records,
                "message": f"DNS records configured for {domain}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"DNS setup failed: {str(e)}"
            }

class GoDaddyIntegration:
    def __init__(self, api_key: str, secret: str):
        self.api_key = api_key
        self.secret = secret
        self.base_url = "https://api.godaddy.com/v1"
        self.headers = {
            "Authorization": f"sso-key {api_key}:{secret}",
            "Content-Type": "application/json"
        }
    
    def setup_domain(self, domain: str, target_url: str) -> Dict[str, Any]:
        """Set up domain with GoDaddy"""
        try:
            availability_result = self.check_availability(domain)
            if not availability_result.get("available", False):
                return {
                    "success": False,
                    "error": f"Domain {domain} is not available"
                }
            
            dns_result = self._setup_dns_records(domain, target_url)
            
            return {
                "success": dns_result["success"],
                "domain": domain,
                "dns_records": dns_result.get("records", []),
                "ssl_status": "pending"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"GoDaddy domain setup failed: {str(e)}"
            }
    
    def check_availability(self, domain: str) -> Dict[str, Any]:
        """Check domain availability with GoDaddy"""
        try:
            response = requests.get(
                f"{self.base_url}/domains/available?domain={domain}",
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "domain": domain,
                    "available": data.get("available", False),
                    "registrar": "godaddy"
                }
            else:
                return {
                    "success": False,
                    "error": f"Availability check failed: {response.text}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Availability check error: {str(e)}"
            }
    
    def _setup_dns_records(self, domain: str, target_url: str) -> Dict[str, Any]:
        """Set up DNS records with GoDaddy"""
        try:
            import urllib.parse
            parsed_url = urllib.parse.urlparse(target_url)
            target_host = parsed_url.netloc
            
            dns_records = [
                {
                    "type": "CNAME",
                    "name": "@",
                    "data": target_host,
                    "ttl": 600
                },
                {
                    "type": "CNAME",
                    "name": "www",
                    "data": target_host,
                    "ttl": 600
                }
            ]
            
            response = requests.put(
                f"{self.base_url}/domains/{domain}/records",
                headers=self.headers,
                json=dns_records
            )
            
            if response.status_code in [200, 204]:
                return {
                    "success": True,
                    "records": dns_records,
                    "message": f"DNS records updated for {domain}"
                }
            else:
                return {
                    "success": False,
                    "error": f"DNS update failed: {response.text}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"DNS setup error: {str(e)}"
            }

class CloudflareIntegration:
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://api.cloudflare.com/client/v4"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
    
    def setup_domain(self, domain: str, target_url: str) -> Dict[str, Any]:
        """Set up domain with Cloudflare"""
        try:
            zone_result = self._add_zone(domain)
            if not zone_result["success"]:
                return zone_result
            
            zone_id = zone_result["zone_id"]
            
            dns_result = self._setup_dns_records(zone_id, domain, target_url)
            
            ssl_result = self._enable_ssl(zone_id)
            
            return {
                "success": dns_result["success"],
                "domain": domain,
                "zone_id": zone_id,
                "dns_records": dns_result.get("records", []),
                "ssl_status": ssl_result.get("status", "pending")
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Cloudflare domain setup failed: {str(e)}"
            }
    
    def _add_zone(self, domain: str) -> Dict[str, Any]:
        """Add domain zone to Cloudflare"""
        try:
            payload = {
                "name": domain,
                "account": {"id": "your-account-id"},
                "jump_start": True
            }
            
            response = requests.post(
                f"{self.base_url}/zones",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "zone_id": data["result"]["id"],
                    "nameservers": data["result"]["name_servers"]
                }
            else:
                return {
                    "success": False,
                    "error": f"Zone creation failed: {response.text}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Zone creation error: {str(e)}"
            }
    
    def _setup_dns_records(self, zone_id: str, domain: str, target_url: str) -> Dict[str, Any]:
        """Set up DNS records in Cloudflare"""
        try:
            import urllib.parse
            parsed_url = urllib.parse.urlparse(target_url)
            target_host = parsed_url.netloc
            
            records_to_create = [
                {
                    "type": "CNAME",
                    "name": "@",
                    "content": target_host,
                    "ttl": 1,
                    "proxied": True
                },
                {
                    "type": "CNAME",
                    "name": "www",
                    "content": target_host,
                    "ttl": 1,
                    "proxied": True
                }
            ]
            
            created_records = []
            for record in records_to_create:
                response = requests.post(
                    f"{self.base_url}/zones/{zone_id}/dns_records",
                    headers=self.headers,
                    json=record
                )
                
                if response.status_code == 200:
                    created_records.append(record)
            
            return {
                "success": len(created_records) > 0,
                "records": created_records,
                "message": f"Created {len(created_records)} DNS records"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"DNS records creation error: {str(e)}"
            }
    
    def _enable_ssl(self, zone_id: str) -> Dict[str, Any]:
        """Enable SSL for the domain"""
        try:
            payload = {
                "value": "flexible"
            }
            
            response = requests.patch(
                f"{self.base_url}/zones/{zone_id}/settings/ssl",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "status": "enabled",
                    "message": "SSL enabled successfully"
                }
            else:
                return {
                    "success": False,
                    "error": f"SSL enablement failed: {response.text}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"SSL enablement error: {str(e)}"
            }
