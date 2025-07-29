import requests
import os
import json
import time
from typing import Dict, Any, Optional, List

class RenderDeployment:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.render.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def create_service(self, repo_url: str, env_vars: Dict[str, str], service_name: str) -> Dict[str, Any]:
        """Create a new web service on Render"""
        try:
            payload = {
                "type": "web_service",
                "name": service_name,
                "repo": repo_url,
                "branch": "main",
                "buildCommand": "pip install -r requirements.txt",
                "startCommand": "gunicorn main:app --bind 0.0.0.0:$PORT",
                "envVars": [
                    {"key": k, "value": v} for k, v in env_vars.items()
                ],
                "plan": "free",
                "region": "oregon"
            }
            
            response = requests.post(
                f"{self.base_url}/services",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 201:
                service_data = response.json()
                return {
                    "success": True,
                    "service_id": service_data.get("id"),
                    "url": service_data.get("serviceDetails", {}).get("url"),
                    "status": "deploying"
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to create service: {response.text}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Exception creating Render service: {str(e)}"
            }
    
    def get_service_status(self, service_id: str) -> Dict[str, Any]:
        """Get deployment status of a service"""
        try:
            response = requests.get(
                f"{self.base_url}/services/{service_id}",
                headers=self.headers
            )
            
            if response.status_code == 200:
                service_data = response.json()
                return {
                    "success": True,
                    "status": service_data.get("serviceDetails", {}).get("status"),
                    "url": service_data.get("serviceDetails", {}).get("url")
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to get service status: {response.text}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Exception getting service status: {str(e)}"
            }

class RailwayDeployment:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://backboard.railway.app/graphql"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    def deploy_project(self, repo_url: str, env_vars: Dict[str, str], project_name: str) -> Dict[str, Any]:
        """Deploy project to Railway using GraphQL API"""
        try:
            create_project_mutation = """
            mutation projectCreate($input: ProjectCreateInput!) {
                projectCreate(input: $input) {
                    id
                    name
                }
            }
            """
            
            variables = {
                "input": {
                    "name": project_name,
                    "description": f"Autonomous deployment of {project_name}",
                    "isPublic": False
                }
            }
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json={"query": create_project_mutation, "variables": variables}
            )
            
            if response.status_code == 200:
                data = response.json()
                if "errors" not in data:
                    project_id = data["data"]["projectCreate"]["id"]
                    
                    service_result = self._create_service(project_id, repo_url, env_vars)
                    if service_result["success"]:
                        return {
                            "success": True,
                            "project_id": project_id,
                            "service_id": service_result["service_id"],
                            "url": service_result.get("url"),
                            "status": "deploying"
                        }
                    else:
                        return service_result
                else:
                    return {
                        "success": False,
                        "error": f"GraphQL errors: {data['errors']}"
                    }
            else:
                return {
                    "success": False,
                    "error": f"Failed to create Railway project: {response.text}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Exception creating Railway project: {str(e)}"
            }
    
    def _create_service(self, project_id: str, repo_url: str, env_vars: Dict[str, str]) -> Dict[str, Any]:
        """Create a service within a Railway project"""
        try:
            create_service_mutation = """
            mutation serviceCreate($input: ServiceCreateInput!) {
                serviceCreate(input: $input) {
                    id
                    name
                }
            }
            """
            
            variables = {
                "input": {
                    "projectId": project_id,
                    "name": "web-service",
                    "source": {
                        "repo": repo_url,
                        "branch": "main"
                    }
                }
            }
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json={"query": create_service_mutation, "variables": variables}
            )
            
            if response.status_code == 200:
                data = response.json()
                if "errors" not in data:
                    service_id = data["data"]["serviceCreate"]["id"]
                    
                    env_result = self._set_environment_variables(service_id, env_vars)
                    if env_result["success"]:
                        return {
                            "success": True,
                            "service_id": service_id,
                            "url": f"https://{service_id}.railway.app"
                        }
                    else:
                        return env_result
                else:
                    return {
                        "success": False,
                        "error": f"GraphQL errors: {data['errors']}"
                    }
            else:
                return {
                    "success": False,
                    "error": f"Failed to create Railway service: {response.text}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Exception creating Railway service: {str(e)}"
            }
    
    def _set_environment_variables(self, service_id: str, env_vars: Dict[str, str]) -> Dict[str, Any]:
        """Set environment variables for a Railway service"""
        try:
            for key, value in env_vars.items():
                set_var_mutation = """
                mutation variableUpsert($input: VariableUpsertInput!) {
                    variableUpsert(input: $input) {
                        id
                    }
                }
                """
                
                variables = {
                    "input": {
                        "serviceId": service_id,
                        "name": key,
                        "value": value
                    }
                }
                
                response = requests.post(
                    self.base_url,
                    headers=self.headers,
                    json={"query": set_var_mutation, "variables": variables}
                )
                
                if response.status_code != 200:
                    return {
                        "success": False,
                        "error": f"Failed to set environment variable {key}: {response.text}"
                    }
            
            return {"success": True}
        except Exception as e:
            return {
                "success": False,
                "error": f"Exception setting environment variables: {str(e)}"
            }

class VercelDeployment:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://api.vercel.com/v2"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    def create_deployment(self, repo_url: str, env_vars: Dict[str, str], project_name: str) -> Dict[str, Any]:
        """Create a deployment on Vercel"""
        try:
            project_result = self._create_project(project_name, repo_url)
            if not project_result["success"]:
                return project_result
            
            project_id = project_result["project_id"]
            
            env_result = self._set_environment_variables(project_id, env_vars)
            if not env_result["success"]:
                return env_result
            
            deploy_result = self._trigger_deployment(project_id)
            if deploy_result["success"]:
                return {
                    "success": True,
                    "project_id": project_id,
                    "deployment_id": deploy_result["deployment_id"],
                    "url": deploy_result["url"],
                    "status": "deploying"
                }
            else:
                return deploy_result
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Exception creating Vercel deployment: {str(e)}"
            }
    
    def _create_project(self, name: str, repo_url: str) -> Dict[str, Any]:
        """Create a new project on Vercel"""
        try:
            payload = {
                "name": name,
                "gitRepository": {
                    "repo": repo_url,
                    "type": "github"
                },
                "framework": "other"
            }
            
            response = requests.post(
                f"{self.base_url}/projects",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                project_data = response.json()
                return {
                    "success": True,
                    "project_id": project_data.get("id")
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to create Vercel project: {response.text}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Exception creating Vercel project: {str(e)}"
            }
    
    def _set_environment_variables(self, project_id: str, env_vars: Dict[str, str]) -> Dict[str, Any]:
        """Set environment variables for a Vercel project"""
        try:
            for key, value in env_vars.items():
                payload = {
                    "key": key,
                    "value": value,
                    "target": ["production", "preview", "development"]
                }
                
                response = requests.post(
                    f"{self.base_url}/projects/{project_id}/env",
                    headers=self.headers,
                    json=payload
                )
                
                if response.status_code != 200:
                    return {
                        "success": False,
                        "error": f"Failed to set environment variable {key}: {response.text}"
                    }
            
            return {"success": True}
        except Exception as e:
            return {
                "success": False,
                "error": f"Exception setting Vercel environment variables: {str(e)}"
            }
    
    def _trigger_deployment(self, project_id: str) -> Dict[str, Any]:
        """Trigger a new deployment for a Vercel project"""
        try:
            response = requests.post(
                f"{self.base_url}/projects/{project_id}/deployments",
                headers=self.headers,
                json={"target": "production"}
            )
            
            if response.status_code == 200:
                deployment_data = response.json()
                return {
                    "success": True,
                    "deployment_id": deployment_data.get("id"),
                    "url": deployment_data.get("url")
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to trigger Vercel deployment: {response.text}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Exception triggering Vercel deployment: {str(e)}"
            }
