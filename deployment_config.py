import json
import yaml
from typing import Dict, Any

class DeploymentConfig:
    def __init__(self, mvp_name: str, platform: str):
        self.mvp_name = mvp_name
        self.platform = platform
        self.sanitized_name = mvp_name.lower().replace('_', '-').replace(' ', '-')
    
    def generate_render_config(self, env_vars: Dict[str, str] = None) -> Dict[str, Any]:
        """Generate render.yaml configuration dynamically"""
        config = {
            "services": [
                {
                    "type": "web",
                    "name": self.sanitized_name,
                    "env": "python",
                    "buildCommand": "pip install -r requirements.txt",
                    "startCommand": "gunicorn main:app --bind 0.0.0.0:$PORT",
                    "envVars": [
                        {"key": "FLASK_ENV", "value": "production"}
                    ]
                }
            ]
        }
        
        if env_vars:
            for key, value in env_vars.items():
                if key == "FLASK_SECRET_KEY":
                    config["services"][0]["envVars"].append({
                        "key": key,
                        "generateValue": True
                    })
                else:
                    config["services"][0]["envVars"].append({
                        "key": key,
                        "sync": False
                    })
        
        return config
    
    def generate_railway_config(self, env_vars: Dict[str, str] = None) -> Dict[str, Any]:
        """Generate railway.toml configuration dynamically"""
        config = {
            "build": {
                "builder": "nixpacks"
            },
            "deploy": {
                "healthcheckPath": "/",
                "healthcheckTimeout": 300,
                "restartPolicyType": "on_failure"
            },
            "services": [
                {
                    "name": self.sanitized_name,
                    "variables": {
                        "PORT": "8080",
                        "FLASK_ENV": "production"
                    }
                }
            ]
        }
        
        if env_vars:
            for key, value in env_vars.items():
                if key not in ["PORT", "FLASK_ENV"]:
                    config["services"][0]["variables"][key] = f"${{{key}}}"
        
        return config
    
    def generate_vercel_config(self, env_vars: Dict[str, str] = None) -> Dict[str, Any]:
        """Generate vercel.json configuration dynamically"""
        config = {
            "version": 2,
            "name": self.sanitized_name,
            "builds": [
                {
                    "src": "main.py",
                    "use": "@vercel/python"
                },
                {
                    "src": "static/**",
                    "use": "@vercel/static"
                }
            ],
            "routes": [
                {
                    "src": "/static/(.*)",
                    "dest": "/static/$1"
                },
                {
                    "src": "/(.*)",
                    "dest": "/main.py"
                }
            ],
            "env": {}
        }
        
        if env_vars:
            for key, value in env_vars.items():
                config["env"][f"@{key.lower()}"] = key
        
        return config
    
    def generate_heroku_config(self, env_vars: Dict[str, str] = None) -> Dict[str, Any]:
        """Generate Procfile and app.json for Heroku deployment"""
        procfile_content = "web: gunicorn main:app --bind 0.0.0.0:$PORT"
        
        app_json = {
            "name": self.sanitized_name,
            "description": f"Autonomous SaaS deployment: {self.mvp_name}",
            "repository": f"https://github.com/user/{self.sanitized_name}",
            "keywords": ["python", "flask", "saas", "autonomous"],
            "env": {
                "FLASK_ENV": {
                    "description": "Flask environment",
                    "value": "production"
                }
            },
            "formation": {
                "web": {
                    "quantity": 1,
                    "size": "free"
                }
            },
            "addons": [],
            "buildpacks": [
                {
                    "url": "heroku/python"
                }
            ]
        }
        
        if env_vars:
            for key, value in env_vars.items():
                if key not in ["FLASK_ENV"]:
                    app_json["env"][key] = {
                        "description": f"Environment variable for {key}",
                        "required": True
                    }
        
        return {
            "procfile": procfile_content,
            "app_json": app_json
        }
    
    def generate_dockerfile(self, env_vars: Dict[str, str] = None) -> str:
        """Generate Dockerfile for containerized deployment"""
        dockerfile_content = f"""FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_ENV=production
ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8000", "--workers", "2"]
"""
        return dockerfile_content
    
    def generate_docker_compose(self, env_vars: Dict[str, str] = None) -> str:
        """Generate docker-compose.yml for local development"""
        compose_content = f"""version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - FLASK_ENV=production
"""
        
        if env_vars:
            for key, value in env_vars.items():
                if key != "FLASK_ENV":
                    compose_content += f"      - {key}=${{{key}}}\n"
        
        compose_content += """    volumes:
      - .:/app
    restart: unless-stopped
"""
        
        return compose_content
    
    def save_config_files(self, output_dir: str, env_vars: Dict[str, str] = None) -> Dict[str, str]:
        """Save all configuration files to the specified directory"""
        import os
        import yaml
        
        os.makedirs(output_dir, exist_ok=True)
        saved_files = {}
        
        render_config = self.generate_render_config(env_vars)
        render_path = os.path.join(output_dir, "render.yaml")
        with open(render_path, 'w') as f:
            yaml.dump(render_config, f, default_flow_style=False)
        saved_files["render.yaml"] = render_path
        
        railway_config = self.generate_railway_config(env_vars)
        railway_path = os.path.join(output_dir, "railway.toml")
        with open(railway_path, 'w') as f:
            import toml
            toml.dump(railway_config, f)
        saved_files["railway.toml"] = railway_path
        
        vercel_config = self.generate_vercel_config(env_vars)
        vercel_path = os.path.join(output_dir, "vercel.json")
        with open(vercel_path, 'w') as f:
            json.dump(vercel_config, f, indent=2)
        saved_files["vercel.json"] = vercel_path
        
        heroku_config = self.generate_heroku_config(env_vars)
        procfile_path = os.path.join(output_dir, "Procfile")
        with open(procfile_path, 'w') as f:
            f.write(heroku_config["procfile"])
        saved_files["Procfile"] = procfile_path
        
        app_json_path = os.path.join(output_dir, "app.json")
        with open(app_json_path, 'w') as f:
            json.dump(heroku_config["app_json"], f, indent=2)
        saved_files["app.json"] = app_json_path
        
        dockerfile_content = self.generate_dockerfile(env_vars)
        dockerfile_path = os.path.join(output_dir, "Dockerfile")
        with open(dockerfile_path, 'w') as f:
            f.write(dockerfile_content)
        saved_files["Dockerfile"] = dockerfile_path
        
        compose_content = self.generate_docker_compose(env_vars)
        compose_path = os.path.join(output_dir, "docker-compose.yml")
        with open(compose_path, 'w') as f:
            f.write(compose_content)
        saved_files["docker-compose.yml"] = compose_path
        
        return saved_files
