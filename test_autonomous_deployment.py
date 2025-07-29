#!/usr/bin/env python3
"""
Test script for autonomous deployment system
"""

import os
import sys
import json
from autonomous_deployer import AutonomousDeployer

def test_deployment_system():
    """Test the autonomous deployment system"""
    print("🚀 Testing Autonomous Deployment System")
    print("=" * 50)
    
    test_credentials = {
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY', 'test_key'),
        'STRIPE_SECRET_KEY': os.getenv('STRIPE_SECRET_KEY', 'test_key'),
        'FLASK_SECRET_KEY': os.getenv('FLASK_SECRET_KEY', 'test_key'),
        'GITHUB_TOKEN': os.getenv('GITHUB_TOKEN', 'test_token'),
        'RENDER_API_KEY': os.getenv('RENDER_API_KEY', 'test_key'),
        'RAILWAY_TOKEN': os.getenv('RAILWAY_TOKEN', 'test_token'),
        'VERCEL_TOKEN': os.getenv('VERCEL_TOKEN', 'test_token')
    }
    
    deployer = AutonomousDeployer(test_credentials)
    
    print(f"✅ Deployer initialized with {len(deployer.platforms)} platforms")
    print(f"📋 Available platforms: {deployer.list_available_platforms()}")
    
    print("\n🔍 Testing MVP validation...")
    mvp_path = "/tmp/test_skill_output"
    validation_result = deployer._validate_mvp_files(mvp_path)
    
    if validation_result["success"]:
        print(f"✅ MVP validation passed - {len(validation_result['present_files'])} files found")
    else:
        print(f"❌ MVP validation failed - missing files: {validation_result['missing_files']}")
    
    print("\n🔧 Testing environment variable preparation...")
    env_vars = deployer._prepare_environment_variables()
    print(f"✅ Prepared {len(env_vars)} environment variables")
    
    print("\n⚙️ Testing deployment configuration...")
    from deployment_config import DeploymentConfig
    
    config_manager = DeploymentConfig("test-mvp", "render")
    render_config = config_manager.generate_render_config(env_vars)
    print(f"✅ Generated Render configuration with {len(render_config['services'])} services")
    
    print("\n🔑 Required credentials for full automation:")
    required_creds = deployer.get_required_credentials()
    for category, creds in required_creds.items():
        print(f"  {category}: {', '.join(creds)}")
    
    print("\n🎯 Autonomous Deployment System Test Complete!")
    print("=" * 50)
    
    return {
        "validation_passed": validation_result["success"],
        "platforms_available": len(deployer.platforms),
        "env_vars_prepared": len(env_vars),
        "required_credentials": required_creds
    }

if __name__ == "__main__":
    result = test_deployment_system()
    print(f"\n📊 Test Results: {json.dumps(result, indent=2)}")
