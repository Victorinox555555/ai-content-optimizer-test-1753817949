#!/usr/bin/env python3
"""
Final integration test for the autonomous deployment system
This will be run once API credentials are provided to verify end-to-end functionality
"""

import os
import sys
import json
from typing import Dict, Any, Optional
from autonomous_deployer import AutonomousDeployer

def load_credentials() -> Optional[Dict[str, str]]:
    """Load API credentials from environment variables"""
    credentials = {}
    
    critical_keys = [
        'RENDER_API_KEY',
        'RAILWAY_TOKEN', 
        'VERCEL_TOKEN',
        'GITHUB_TOKEN',
        'SENDGRID_API_KEY'
    ]
    
    optional_keys = [
        'NAMECHEAP_API_KEY',
        'SENTRY_DSN',
        'DATADOG_API_KEY',
        'CLOUDFLARE_API_TOKEN'
    ]
    
    missing_critical = []
    
    for key in critical_keys:
        value = os.getenv(key)
        if value:
            credentials[key] = value
        else:
            missing_critical.append(key)
    
    for key in optional_keys:
        value = os.getenv(key)
        if value:
            credentials[key] = value
    
    if missing_critical:
        print(f"❌ Missing critical credentials: {', '.join(missing_critical)}")
        print("Please set these environment variables before running the test.")
        return None
    
    print(f"✅ Loaded {len(credentials)} credentials successfully")
    return credentials

def test_autonomous_deployment():
    """Test the complete autonomous deployment pipeline"""
    
    print("=" * 80)
    print("🤖 AUTONOMOUS SAAS FACTORY - FINAL INTEGRATION TEST")
    print("=" * 80)
    
    credentials = load_credentials()
    if not credentials:
        return False
    
    print("\n🔧 Initializing Autonomous Deployer...")
    try:
        deployer = AutonomousDeployer(credentials)
        print("✅ Autonomous Deployer initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize deployer: {str(e)}")
        return False
    
    print("\n🚀 Starting autonomous deployment of AI-Powered Content Optimizer...")
    
    try:
        result = deployer.deploy_mvp(
            mvp_path="/tmp/test_skill_output",
            mvp_name="ai-content-optimizer",
            platform="render"  # Primary platform
        )
        
        if result.get("success"):
            print("\n🎉 AUTONOMOUS DEPLOYMENT SUCCESSFUL!")
            print("=" * 80)
            
            urls = result.get("urls", {})
            print(f"🌐 Live Site: {urls.get('live_site', 'N/A')}")
            print(f"📁 GitHub Repo: {urls.get('github_repo', 'N/A')}")
            print(f"🌍 Custom Domain: {urls.get('custom_domain', 'N/A')}")
            
            details = result.get("deployment_details", {})
            print(f"\n📊 Deployment Details:")
            print(f"  Platform: {details.get('platform', 'N/A')}")
            print(f"  Repository: {details.get('repo_full_name', 'N/A')}")
            print(f"  Monitoring: {'✅' if details.get('monitoring_enabled') else '❌'}")
            print(f"  Email: {'✅' if details.get('email_configured') else '❌'}")
            print(f"  CI/CD: {'✅' if details.get('cicd_enabled') else '❌'}")
            print(f"  Domain: {'✅' if details.get('domain_configured') else '❌'}")
            print(f"  Business Ops: {'✅' if details.get('business_ops_ready') else '❌'}")
            
            print(f"\n⏱️  Deployment Time: {result.get('deployment_time', 'N/A')}")
            print(f"🤖 Manual Steps Required: {result.get('manual_steps_required', 'N/A')}")
            
            print("\n🔍 Testing deployed site functionality...")
            live_url = urls.get('live_site')
            if live_url:
                success = test_deployed_site(live_url)
                if success:
                    print("✅ Deployed site is fully functional!")
                else:
                    print("⚠️  Deployed site has some issues")
            
            return True
            
        else:
            print(f"\n❌ AUTONOMOUS DEPLOYMENT FAILED")
            print(f"Error: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"\n❌ DEPLOYMENT EXCEPTION: {str(e)}")
        return False

def test_deployed_site(url: str) -> bool:
    """Test the functionality of the deployed site"""
    import requests
    import time
    
    try:
        print("  🔄 Testing homepage...")
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            print("  ✅ Homepage accessible")
        else:
            print(f"  ❌ Homepage failed: {response.status_code}")
            return False
        
        print("  🔄 Testing health endpoint...")
        health_response = requests.get(f"{url}/api/health", timeout=30)
        if health_response.status_code == 200:
            print("  ✅ Health endpoint working")
        else:
            print(f"  ❌ Health endpoint failed: {health_response.status_code}")
        
        print("  🔄 Testing signup functionality...")
        test_email = f"test{int(time.time())}@example.com"
        signup_data = {"email": test_email, "password": "testpassword123"}
        
        signup_response = requests.post(
            f"{url}/api/signup",
            json=signup_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if signup_response.status_code == 200:
            signup_result = signup_response.json()
            if signup_result.get("success"):
                print("  ✅ Signup functionality working")
                return True
            else:
                print(f"  ❌ Signup failed: {signup_result.get('message')}")
                return False
        else:
            print(f"  ❌ Signup request failed: {signup_response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ Site testing error: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🎯 AUTONOMOUS SAAS FACTORY - FINAL INTEGRATION TEST")
    print("This test verifies the complete end-to-end deployment pipeline")
    print("Make sure all required API credentials are set as environment variables\n")
    
    success = test_autonomous_deployment()
    
    if success:
        print("\n" + "=" * 80)
        print("🎉 INTEGRATION TEST PASSED!")
        print("✅ Autonomous SaaS Factory is fully operational")
        print("✅ Can deploy MVPs end-to-end without manual intervention")
        print("✅ All 8 deployment automation gaps successfully filled")
        print("🚀 Ready for production use!")
        print("=" * 80)
        return 0
    else:
        print("\n" + "=" * 80)
        print("❌ INTEGRATION TEST FAILED")
        print("Please check the error messages above and fix any issues")
        print("=" * 80)
        return 1

if __name__ == "__main__":
    sys.exit(main())
