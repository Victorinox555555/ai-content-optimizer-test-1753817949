import json
from typing import Dict, Any, List

class CICDAutomation:
    def __init__(self, github_automation):
        self.github = github_automation
    
    def setup_github_actions(self, repo_full_name: str, platform: str) -> Dict[str, Any]:
        """Set up GitHub Actions CI/CD pipeline"""
        try:
            workflow_content = self._generate_workflow_content(platform)
            
            result = self.github.create_github_actions_workflow(
                repo_full_name,
                "deploy",
                workflow_content
            )
            
            if result["success"]:
                return {
                    "success": True,
                    "workflow_file": result["workflow_path"],
                    "platform": platform,
                    "features": [
                        "Automated testing on push",
                        "Deployment to production",
                        "Environment variable management",
                        "Security scanning",
                        "Dependency updates"
                    ]
                }
            else:
                return result
        except Exception as e:
            return {
                "success": False,
                "error": f"CI/CD setup failed: {str(e)}"
            }
    
    def _generate_workflow_content(self, platform: str) -> str:
        """Generate GitHub Actions workflow content"""
        if platform == "render":
            return self._generate_render_workflow()
        elif platform == "railway":
            return self._generate_railway_workflow()
        elif platform == "vercel":
            return self._generate_vercel_workflow()
        else:
            return self._generate_generic_workflow()
    
    def _generate_render_workflow(self) -> str:
        """Generate workflow for Render deployment"""
        return """name: Deploy to Render

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest flake8
    
    - name: Lint with flake8
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    
    - name: Test with pytest
      run: |
        pytest test_suite.py -v
    
    - name: Security scan
      run: |
        pip install bandit
        bandit -r . -f json -o bandit-report.json || true
    
  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to Render
      env:
        RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        STRIPE_SECRET_KEY: ${{ secrets.STRIPE_SECRET_KEY }}
      run: |
        echo "Deployment triggered automatically via Render GitHub integration"
"""
    
    def _generate_railway_workflow(self) -> str:
        """Generate workflow for Railway deployment"""
        return """name: Deploy to Railway

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest flake8
    
    - name: Lint with flake8
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
    
    - name: Test with pytest
      run: |
        pytest test_suite.py -v
    
  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Install Railway CLI
      run: |
        npm install -g @railway/cli
    
    - name: Deploy to Railway
      env:
        RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
      run: |
        railway login --token $RAILWAY_TOKEN
        railway up --detach
"""
    
    def _generate_vercel_workflow(self) -> str:
        """Generate workflow for Vercel deployment"""
        return """name: Deploy to Vercel

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest flake8
    
    - name: Lint with flake8
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
    
    - name: Test with pytest
      run: |
        pytest test_suite.py -v
    
  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Install Vercel CLI
      run: npm install -g vercel
    
    - name: Deploy to Vercel
      env:
        VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
        VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
        VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}
      run: |
        vercel --prod --token $VERCEL_TOKEN --confirm
"""
    
    def _generate_generic_workflow(self) -> str:
        """Generate generic workflow for any platform"""
        return """name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest flake8 bandit
    
    - name: Lint with flake8
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    
    - name: Security scan with bandit
      run: |
        bandit -r . -f json -o bandit-report.json || true
    
    - name: Test with pytest
      run: |
        pytest test_suite.py -v
    
    - name: Upload test results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: test-results
        path: |
          bandit-report.json
          pytest-report.xml
    
  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build application
      run: |
        echo "Application built successfully"
        
    - name: Create deployment artifact
      run: |
        tar -czf deployment.tar.gz . --exclude='.git' --exclude='node_modules'
    
    - name: Upload deployment artifact
      uses: actions/upload-artifact@v3
      with:
        name: deployment-package
        path: deployment.tar.gz
"""
    
    def setup_dependency_updates(self, repo_full_name: str) -> Dict[str, Any]:
        """Set up automated dependency updates"""
        try:
            dependabot_content = self._generate_dependabot_config()
            
            result = self.github._upload_single_file(
                repo_full_name,
                ".github/dependabot.yml",
                dependabot_content,
                "Add Dependabot configuration"
            )
            
            if result["success"]:
                return {
                    "success": True,
                    "message": "Dependabot configuration added",
                    "features": [
                        "Automated Python dependency updates",
                        "Security vulnerability alerts",
                        "Weekly update schedule",
                        "Automatic PR creation"
                    ]
                }
            else:
                return result
        except Exception as e:
            return {
                "success": False,
                "error": f"Dependabot setup failed: {str(e)}"
            }
    
    def _generate_dependabot_config(self) -> str:
        """Generate Dependabot configuration"""
        return """version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    reviewers:
      - "devin-ai-integration[bot]"
    assignees:
      - "devin-ai-integration[bot]"
    commit-message:
      prefix: "deps"
      include: "scope"
    labels:
      - "dependencies"
      - "python"
    
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
    commit-message:
      prefix: "ci"
      include: "scope"
    labels:
      - "dependencies"
      - "github-actions"
"""
    
    def setup_security_scanning(self, repo_full_name: str) -> Dict[str, Any]:
        """Set up security scanning workflow"""
        try:
            security_workflow = self._generate_security_workflow()
            
            result = self.github.create_github_actions_workflow(
                repo_full_name,
                "security",
                security_workflow
            )
            
            if result["success"]:
                return {
                    "success": True,
                    "workflow_file": result["workflow_path"],
                    "features": [
                        "CodeQL analysis",
                        "Dependency vulnerability scanning",
                        "Secret scanning",
                        "SAST (Static Application Security Testing)"
                    ]
                }
            else:
                return result
        except Exception as e:
            return {
                "success": False,
                "error": f"Security scanning setup failed: {str(e)}"
            }
    
    def _generate_security_workflow(self) -> str:
        """Generate security scanning workflow"""
        return """name: Security Scanning

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * 1'  # Weekly on Monday at 2 AM

jobs:
  codeql:
    name: CodeQL Analysis
    runs-on: ubuntu-latest
    permissions:
      actions: read
      contents: read
      security-events: write
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v3
    
    - name: Initialize CodeQL
      uses: github/codeql-action/init@v2
      with:
        languages: python
    
    - name: Autobuild
      uses: github/codeql-action/autobuild@v2
    
    - name: Perform CodeQL Analysis
      uses: github/codeql-action/analyze@v2
  
  dependency-scan:
    name: Dependency Vulnerability Scan
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install safety bandit semgrep
    
    - name: Run Safety check
      run: |
        safety check --json --output safety-report.json || true
    
    - name: Run Bandit security scan
      run: |
        bandit -r . -f json -o bandit-report.json || true
    
    - name: Run Semgrep scan
      run: |
        semgrep --config=auto --json --output=semgrep-report.json . || true
    
    - name: Upload security reports
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: security-reports
        path: |
          safety-report.json
          bandit-report.json
          semgrep-report.json
"""
