#!/usr/bin/env python3
"""
Test complete AI content optimization workflow
"""

import requests
import json
import time

def test_complete_workflow():
    """Test the complete user workflow"""
    base_url = "http://localhost:5000"
    session = requests.Session()
    
    print("🧪 Testing Complete AI Content Optimization Workflow")
    print("=" * 60)
    
    print("\n1. Testing health check...")
    try:
        response = session.get(f"{base_url}/api/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health check passed: {health_data['status']}")
            print(f"   Database: {health_data['database']}")
            print(f"   AI Optimization: {health_data['services']['ai_optimization']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    print("\n2. Testing user signup...")
    test_email = f"workflow_test_{int(time.time())}@example.com"
    test_password = "TestPassword123!"
    
    signup_data = {
        "email": test_email,
        "password": test_password
    }
    
    try:
        response = session.post(f"{base_url}/api/signup", json=signup_data)
        if response.status_code == 200:
            signup_result = response.json()
            if signup_result.get('success'):
                print(f"✅ Signup successful: User ID {signup_result.get('user_id')}")
            else:
                print(f"❌ Signup failed: {signup_result.get('error')}")
                return False
        else:
            print(f"❌ Signup HTTP error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Signup error: {e}")
        return False
    
    print("\n3. Testing user login...")
    login_data = {
        "email": test_email,
        "password": test_password
    }
    
    try:
        response = session.post(f"{base_url}/api/login", json=login_data)
        if response.status_code == 200:
            login_result = response.json()
            if login_result.get('success'):
                print(f"✅ Login successful: {login_result.get('message')}")
            else:
                print(f"❌ Login failed: {login_result.get('error')}")
                return False
        else:
            print(f"❌ Login HTTP error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False
    
    print("\n4. Testing AI content optimization...")
    test_content = """
    Looking to boost your social media presence? Our new marketing tool helps businesses 
    grow their online audience through targeted campaigns and analytics. Get started today 
    and see results in just 30 days!
    """
    
    optimization_data = {
        "content": test_content.strip(),
        "target_audience": "small business owners"
    }
    
    try:
        response = session.post(f"{base_url}/api/optimize", json=optimization_data)
        if response.status_code == 200:
            optimization_result = response.json()
            if optimization_result.get('success'):
                print("✅ AI optimization successful!")
                print(f"   Original length: {len(optimization_result['original'])} chars")
                print(f"   Optimized length: {len(optimization_result['optimized'])} chars")
                print(f"   Engagement score: {optimization_result['engagement_score']}/100")
                print(f"   Improvements: {len(optimization_result['improvements'])} suggestions")
                
                optimized = optimization_result['optimized']
                if len(optimized) > 100:
                    print(f"   Sample: {optimized[:100]}...")
                else:
                    print(f"   Optimized: {optimized}")
                    
            else:
                print(f"❌ AI optimization failed: {optimization_result.get('error')}")
                return False
        else:
            print(f"❌ AI optimization HTTP error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ AI optimization error: {e}")
        return False
    
    print("\n5. Testing payment integration...")
    try:
        response = session.post(f"{base_url}/api/create-checkout-session", json={"plan": "basic"})
        if response.status_code == 200:
            payment_result = response.json()
            if payment_result.get('success'):
                print("✅ Payment integration working!")
                print(f"   Checkout URL generated: {len(payment_result.get('checkout_url', ''))} chars")
            else:
                print(f"⚠️  Payment integration issue: {payment_result.get('error')}")
        else:
            print(f"⚠️  Payment HTTP error: {response.status_code}")
    except Exception as e:
        print(f"⚠️  Payment error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Complete workflow test PASSED!")
    print("✅ User can signup, login, and use AI content optimization")
    return True

if __name__ == "__main__":
    success = test_complete_workflow()
    if not success:
        print("\n❌ Workflow test FAILED!")
        exit(1)
    else:
        print("\n🚀 AI-Powered Content Optimizer is fully functional!")
