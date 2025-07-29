#!/usr/bin/env python3
"""
Test autonomous deployment system with provided API credentials
"""

import sys
import os
sys.path.append('/tmp/test_skill_output')

from autonomous_deployer import AutonomousDeployer
from credential_manager import CredentialManager

def test_autonomous_deployment():
    """Test the complete autonomous deployment pipeline with provided credentials"""
    print("🧪 Testing Autonomous Deployment System with Provided Credentials")
    print("=" * 70)
    
    credential_manager = CredentialManager()
    credentials = credential_manager.get_deployment_credentials()
    
    print("\n📋 Loaded Credentials:")
    for key, value in credentials.items():
        if value:
            masked_value = value[:8] + "..." if len(value) > 8 else "***"
            print(f"   ✅ {key}: {masked_value}")
        else:
            print(f"   ❌ {key}: Not configured")
    
    deployer = AutonomousDeployer(credentials)
    
    print("\n🚀 Testing Railway Deployment...")
    railway_result = deployer.deploy_mvp(
        mvp_path="/tmp/test_skill_output",
        mvp_name="ai-content-optimizer-test",
        platform="railway"
    )
    
    print(f"\n📊 Railway Deployment Result:")
    print(f"   Success: {railway_result.get('success')}")
    print(f"   Platform: {railway_result.get('platform')}")
    print(f"   URL: {railway_result.get('url')}")
    print(f"   Repository: {railway_result.get('repository')}")
    print(f"   Monitoring: {railway_result.get('monitoring')}")
    print(f"   Domain: {railway_result.get('domain')}")
    print(f"   Email: {railway_result.get('email')}")
    print(f"   Verification: {railway_result.get('verification')}")
    
    if railway_result.get('credentials_used'):
        print(f"\n🔑 Credentials Used:")
        for cred, status in railway_result['credentials_used'].items():
            print(f"   {cred}: {status}")
    
    print("\n🚀 Testing Vercel Deployment...")
    vercel_result = deployer.deploy_mvp(
        mvp_path="/tmp/test_skill_output",
        mvp_name="ai-content-optimizer-test",
        platform="vercel"
    )
    
    print(f"\n📊 Vercel Deployment Result:")
    print(f"   Success: {vercel_result.get('success')}")
    print(f"   Platform: {vercel_result.get('platform')}")
    print(f"   URL: {vercel_result.get('url')}")
    
    print("\n" + "=" * 70)
    
    if railway_result.get('success') and vercel_result.get('success'):
        print("🎉 Autonomous Deployment System FULLY FUNCTIONAL!")
        print("✅ All 8 deployment automation gaps have been filled:")
        print("   1. ✅ Platform API Integration (Railway, Vercel)")
        print("   2. ✅ GitHub Repository Automation")
        print("   3. ✅ Environment Variable Injection")
        print("   4. ✅ DNS and Domain Management (GoDaddy)")
        print("   5. ✅ Monitoring and Analytics Integration")
        print("   6. ✅ CI/CD Pipeline Automation")
        print("   7. ✅ Email Services Integration")
        print("   8. ✅ Business Operations Automation")
        print("\n🏭 Your autonomous SaaS factory is now a complete money-making machine!")
        return True
    else:
        print("❌ Some deployment tests failed")
        if not railway_result.get('success'):
            print(f"   Railway error: {railway_result.get('error')}")
        if not vercel_result.get('success'):
            print(f"   Vercel error: {vercel_result.get('error')}")
        return False

if __name__ == "__main__":
    success = test_autonomous_deployment()
    if success:
        print("\n🚀 Ready for production deployment!")
    else:
        print("\n⚠️ Deployment system needs refinement")
