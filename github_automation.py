import requests
import base64
import json
from typing import Dict, Any, List

class GitHubAutomation:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        }
    
    def create_repository(self, name: str, description: str, private: bool = False) -> Dict[str, Any]:
        """Create a new GitHub repository"""
        try:
            import time
            unique_name = f"{name}-{int(time.time())}"
            
            payload = {
                "name": unique_name,
                "description": description,
                "private": private,
                "auto_init": True,
                "gitignore_template": "Python"
            }
            
            response = requests.post(
                f"{self.base_url}/user/repos",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 201:
                repo_data = response.json()
                return {
                    "success": True,
                    "repo_id": repo_data.get("id"),
                    "repo_url": repo_data.get("html_url"),
                    "clone_url": repo_data.get("clone_url"),
                    "ssh_url": repo_data.get("ssh_url"),
                    "full_name": repo_data.get("full_name")
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to create repository: {response.text}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Exception creating GitHub repository: {str(e)}"
            }
    
    def upload_files(self, repo_full_name: str, files: Dict[str, str], commit_message: str = "Initial commit") -> Dict[str, Any]:
        """Upload multiple files to a GitHub repository"""
        try:
            success_files = []
            failed_files = []
            
            for file_path, content in files.items():
                result = self._upload_single_file(repo_full_name, file_path, content, commit_message)
                if result["success"]:
                    success_files.append(file_path)
                else:
                    failed_files.append({"file": file_path, "error": result["error"]})
            
            return {
                "success": len(failed_files) == 0,
                "uploaded_files": success_files,
                "failed_files": failed_files,
                "total_files": len(files)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Exception uploading files: {str(e)}"
            }
    
    def _upload_single_file(self, repo_full_name: str, file_path: str, content: str, commit_message: str) -> Dict[str, Any]:
        """Upload a single file to GitHub repository"""
        try:
            encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
            
            payload = {
                "message": commit_message,
                "content": encoded_content,
                "branch": "main"
            }
            
            response = requests.put(
                f"{self.base_url}/repos/{repo_full_name}/contents/{file_path}",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code in [200, 201]:
                return {"success": True}
            else:
                return {
                    "success": False,
                    "error": f"Failed to upload {file_path}: {response.text}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Exception uploading {file_path}: {str(e)}"
            }
    
    def setup_environment_variables(self, repo_full_name: str, env_vars: Dict[str, str]) -> Dict[str, Any]:
        """Set up GitHub secrets for repository"""
        try:
            public_key = self._get_repository_public_key(repo_full_name)
            if not public_key["success"]:
                return public_key
            
            success_vars = []
            failed_vars = []
            
            for key, value in env_vars.items():
                result = self._create_secret(repo_full_name, key, value, public_key["key"], public_key["key_id"])
                if result["success"]:
                    success_vars.append(key)
                else:
                    failed_vars.append({"key": key, "error": result["error"]})
            
            return {
                "success": len(failed_vars) == 0,
                "created_secrets": success_vars,
                "failed_secrets": failed_vars,
                "total_secrets": len(env_vars)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Exception setting up environment variables: {str(e)}"
            }
    
    def _get_repository_public_key(self, repo_full_name: str) -> Dict[str, Any]:
        """Get repository public key for encrypting secrets"""
        try:
            response = requests.get(
                f"{self.base_url}/repos/{repo_full_name}/actions/secrets/public-key",
                headers=self.headers
            )
            
            if response.status_code == 200:
                key_data = response.json()
                return {
                    "success": True,
                    "key": key_data.get("key"),
                    "key_id": key_data.get("key_id")
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to get public key: {response.text}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Exception getting public key: {str(e)}"
            }
    
    def _create_secret(self, repo_full_name: str, secret_name: str, secret_value: str, public_key: str, key_id: str) -> Dict[str, Any]:
        """Create an encrypted secret in GitHub repository"""
        try:
            from cryptography.hazmat.primitives import serialization
            from cryptography.hazmat.primitives.asymmetric import padding
            from cryptography.hazmat.primitives import hashes
            
            public_key_obj = serialization.load_pem_public_key(
                f"-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----".encode()
            )
            
            encrypted_value = public_key_obj.encrypt(
                secret_value.encode('utf-8'),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            
            encrypted_value_b64 = base64.b64encode(encrypted_value).decode('utf-8')
            
            payload = {
                "encrypted_value": encrypted_value_b64,
                "key_id": key_id
            }
            
            response = requests.put(
                f"{self.base_url}/repos/{repo_full_name}/actions/secrets/{secret_name}",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code in [200, 201, 204]:
                return {"success": True}
            else:
                return {
                    "success": False,
                    "error": f"Failed to create secret {secret_name}: {response.text}"
                }
        except ImportError:
            return {
                "success": False,
                "error": "cryptography library not available for secret encryption"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Exception creating secret {secret_name}: {str(e)}"
            }
    
    def create_github_actions_workflow(self, repo_full_name: str, workflow_name: str, workflow_content: str) -> Dict[str, Any]:
        """Create a GitHub Actions workflow file"""
        try:
            workflow_path = f".github/workflows/{workflow_name}.yml"
            result = self._upload_single_file(
                repo_full_name, 
                workflow_path, 
                workflow_content, 
                f"Add {workflow_name} workflow"
            )
            
            if result["success"]:
                return {
                    "success": True,
                    "workflow_path": workflow_path,
                    "message": f"GitHub Actions workflow '{workflow_name}' created successfully"
                }
            else:
                return result
        except Exception as e:
            return {
                "success": False,
                "error": f"Exception creating GitHub Actions workflow: {str(e)}"
            }
    
    def get_repository_info(self, repo_full_name: str) -> Dict[str, Any]:
        """Get information about a repository"""
        try:
            response = requests.get(
                f"{self.base_url}/repos/{repo_full_name}",
                headers=self.headers
            )
            
            if response.status_code == 200:
                repo_data = response.json()
                return {
                    "success": True,
                    "name": repo_data.get("name"),
                    "full_name": repo_data.get("full_name"),
                    "description": repo_data.get("description"),
                    "html_url": repo_data.get("html_url"),
                    "clone_url": repo_data.get("clone_url"),
                    "default_branch": repo_data.get("default_branch"),
                    "private": repo_data.get("private"),
                    "created_at": repo_data.get("created_at"),
                    "updated_at": repo_data.get("updated_at")
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to get repository info: {response.text}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Exception getting repository info: {str(e)}"
            }
