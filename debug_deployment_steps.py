#!/usr/bin/env python3
"""
Debug each step of the autonomous deployment pipeline
"""

import sys
sys.path.append('/tmp/test_skill_output')

from autonomous_deployer import AutonomousDeployer
from credential_manager import CredentialManager

def debug_deployment_steps():
    """Debug each step of the deployment pipeline individually"""
    print("🔍 Debugging Autonomous Deployment Pipeline Steps")
    print("=" * 60)
    
    credential_manager = CredentialManager()
    credentials = credential_manager.get_deployment_credentials()
    
    print(f"\n📋 Loaded {len(credentials)} credentials")
    
    deployer = AutonomousDeployer(credentials)
    mvp_path = "/tmp/test_skill_output"
    mvp_name = "ai-content-optimizer-debug"
    
    print("\n🔍 Step 1: Validating MVP files...")
    validation_result = deployer._validate_mvp_files(mvp_path)
    print(f"   Success: {validation_result.get('success')}")
    print(f"   Present files: {len(validation_result.get('present_files', []))}")
    print(f"   Missing files: {validation_result.get('missing_files', [])}")
    if validation_result.get('error'):
        print(f"   Error: {validation_result['error']}")
    
    print("\n🔍 Step 2: Testing GitHub repository creation...")
    try:
        repo_result = deployer._create_and_populate_repository(mvp_path, mvp_name)
        print(f"   Success: {repo_result.get('success')}")
        print(f"   Repo URL: {repo_result.get('repo_url')}")
        print(f"   Full name: {repo_result.get('full_name')}")
        if repo_result.get('error'):
            print(f"   Error: {repo_result['error']}")
    except Exception as e:
        print(f"   Exception: {str(e)}")
        repo_result = {"success": False, "error": str(e)}
    
    print("\n🔍 Step 3: Preparing environment variables...")
    try:
        env_vars = deployer._prepare_environment_variables()
        print(f"   Environment variables prepared: {len(env_vars)}")
        for key in env_vars.keys():
            print(f"   - {key}")
    except Exception as e:
        print(f"   Exception: {str(e)}")
        env_vars = {}
    
    print("\n🔍 Step 4: Testing Railway platform deployment...")
    try:
        railway_result = deployer._deploy_to_platform("railway", repo_result, env_vars, mvp_name)
        print(f"   Success: {railway_result.get('success')}")
        print(f"   URL: {railway_result.get('url')}")
        if railway_result.get('error'):
            print(f"   Error: {railway_result['error']}")
    except Exception as e:
        print(f"   Exception: {str(e)}")
    
    print("\n🔍 Step 5: Testing Vercel platform deployment...")
    try:
        vercel_result = deployer._deploy_to_platform("vercel", repo_result, env_vars, mvp_name)
        print(f"   Success: {vercel_result.get('success')}")
        print(f"   URL: {vercel_result.get('url')}")
        if vercel_result.get('error'):
            print(f"   Error: {vercel_result['error']}")
    except Exception as e:
        print(f"   Exception: {str(e)}")
    
    print("\n🔍 Step 6: Testing monitoring setup...")
    try:
        monitoring_result = deployer._setup_monitoring("https://example.com")
        print(f"   Success: {monitoring_result.get('success')}")
        print(f"   Services: {monitoring_result.get('services', [])}")
        if monitoring_result.get('error'):
            print(f"   Error: {monitoring_result['error']}")
    except Exception as e:
        print(f"   Exception: {str(e)}")
    
    print("\n" + "=" * 60)
    print("🔍 Deployment pipeline debugging complete")

if __name__ == "__main__":
    debug_deployment_steps()
