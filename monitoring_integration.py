import requests
import json
from typing import Dict, Any, List, Optional

class MonitoringSetup:
    def __init__(self, credentials: Dict[str, str]):
        self.credentials = credentials
        self.services = {}
        
        if credentials.get('SENTRY_DSN'):
            self.services['sentry'] = SentryIntegration(credentials['SENTRY_DSN'])
        
        if credentials.get('DATADOG_API_KEY'):
            self.services['datadog'] = DatadogIntegration(
                credentials['DATADOG_API_KEY'],
                credentials.get('DATADOG_APP_KEY')
            )
        
        if credentials.get('NEW_RELIC_LICENSE_KEY'):
            self.services['newrelic'] = NewRelicIntegration(credentials['NEW_RELIC_LICENSE_KEY'])
    
    def setup_monitoring(self, app_name: str, deployment_url: str) -> Dict[str, Any]:
        """Set up monitoring for the deployed application"""
        results = {}
        
        for service_name, service in self.services.items():
            try:
                result = service.setup_monitoring(app_name, deployment_url)
                results[service_name] = result
            except Exception as e:
                results[service_name] = {
                    "success": False,
                    "error": f"Failed to setup {service_name}: {str(e)}"
                }
        
        return {
            "success": len([r for r in results.values() if r.get("success")]) > 0,
            "services": results,
            "total_services": len(self.services)
        }

class SentryIntegration:
    def __init__(self, dsn: str):
        self.dsn = dsn
        self.api_base = "https://sentry.io/api/0"
    
    def setup_monitoring(self, app_name: str, deployment_url: str) -> Dict[str, Any]:
        """Set up Sentry error tracking"""
        try:
            sentry_config = {
                "dsn": self.dsn,
                "environment": "production",
                "release": f"{app_name}@1.0.0",
                "traces_sample_rate": 0.1,
                "profiles_sample_rate": 0.1
            }
            
            return {
                "success": True,
                "service": "Sentry",
                "config": sentry_config,
                "integration_code": self._generate_sentry_code(sentry_config)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Sentry setup failed: {str(e)}"
            }
    
    def _generate_sentry_code(self, config: Dict[str, Any]) -> str:
        """Generate Python code for Sentry integration"""
        return f"""
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="{config['dsn']}",
    integrations=[FlaskIntegration()],
    traces_sample_rate={config['traces_sample_rate']},
    profiles_sample_rate={config['profiles_sample_rate']},
    environment="{config['environment']}",
    release="{config['release']}"
)
"""

class DatadogIntegration:
    def __init__(self, api_key: str, app_key: Optional[str] = None):
        self.api_key = api_key
        self.app_key = app_key
        self.api_base = "https://api.datadoghq.com/api/v1"
    
    def setup_monitoring(self, app_name: str, deployment_url: str) -> Dict[str, Any]:
        """Set up Datadog monitoring"""
        try:
            datadog_config = {
                "api_key": self.api_key,
                "app_key": self.app_key,
                "service_name": app_name,
                "env": "production"
            }
            
            return {
                "success": True,
                "service": "Datadog",
                "config": datadog_config,
                "integration_code": self._generate_datadog_code(datadog_config)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Datadog setup failed: {str(e)}"
            }
    
    def _generate_datadog_code(self, config: Dict[str, Any]) -> str:
        """Generate Python code for Datadog integration"""
        return f"""
from ddtrace import patch_all, config
from ddtrace.contrib.flask import get_current_span

patch_all()

config.flask['service_name'] = '{config['service_name']}'
config.flask['distributed_tracing_enabled'] = True
"""

class NewRelicIntegration:
    def __init__(self, license_key: str):
        self.license_key = license_key
        self.api_base = "https://api.newrelic.com/v2"
    
    def setup_monitoring(self, app_name: str, deployment_url: str) -> Dict[str, Any]:
        """Set up New Relic monitoring"""
        try:
            newrelic_config = {
                "license_key": self.license_key,
                "app_name": app_name,
                "monitor_mode": True,
                "log_level": "info"
            }
            
            return {
                "success": True,
                "service": "New Relic",
                "config": newrelic_config,
                "integration_code": self._generate_newrelic_code(newrelic_config)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"New Relic setup failed: {str(e)}"
            }
    
    def _generate_newrelic_code(self, config: Dict[str, Any]) -> str:
        """Generate Python code for New Relic integration"""
        return f"""
import newrelic.agent

newrelic.agent.initialize()

app = newrelic.agent.WSGIApplicationWrapper(app)
"""

class UptimeMonitoring:
    def __init__(self, credentials: Dict[str, str]):
        self.credentials = credentials
    
    def setup_uptime_monitoring(self, app_name: str, deployment_url: str) -> Dict[str, Any]:
        """Set up basic uptime monitoring"""
        try:
            monitors = []
            
            if self.credentials.get('PINGDOM_API_KEY'):
                pingdom_result = self._setup_pingdom(app_name, deployment_url)
                monitors.append(pingdom_result)
            
            if self.credentials.get('UPTIMEROBOT_API_KEY'):
                uptimerobot_result = self._setup_uptimerobot(app_name, deployment_url)
                monitors.append(uptimerobot_result)
            
            health_check = self._generate_health_check_code()
            monitors.append({
                "service": "Health Check Endpoint",
                "success": True,
                "code": health_check
            })
            
            return {
                "success": True,
                "monitors": monitors,
                "total_monitors": len(monitors)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Uptime monitoring setup failed: {str(e)}"
            }
    
    def _setup_pingdom(self, app_name: str, deployment_url: str) -> Dict[str, Any]:
        """Set up Pingdom monitoring"""
        return {
            "service": "Pingdom",
            "success": True,
            "message": "Pingdom monitor configuration ready",
            "url": deployment_url,
            "check_interval": 300
        }
    
    def _setup_uptimerobot(self, app_name: str, deployment_url: str) -> Dict[str, Any]:
        """Set up UptimeRobot monitoring"""
        return {
            "service": "UptimeRobot",
            "success": True,
            "message": "UptimeRobot monitor configuration ready",
            "url": deployment_url,
            "check_interval": 300
        }
    
    def _generate_health_check_code(self) -> str:
        """Generate health check endpoint code"""
        return """
@app.route('/health')
def health_check():
    try:
        conn = sqlite3.connect('users.db')
        conn.execute('SELECT 1')
        conn.close()
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0',
            'database': 'connected'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500
"""
