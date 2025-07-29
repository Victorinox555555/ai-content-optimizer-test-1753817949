#!/usr/bin/env python3
"""
Test signup functionality on the live deployment
"""

import requests
import json
import time

def test_live_signup():
    """Test signup on the current live deployment"""
    base_url = "https://user:6da87935548a338a30206f4808731bac@chat-privacy-checker-tunnel-96gq9os6.devinapps.com"
    
    print("🔄 Testing live signup functionality...")
    
    test_email = f"test{int(time.time())}@example.com"
    test_password = "testpassword123"
    
    signup_data = {
        "email": test_email,
        "password": test_password
    }
    
    try:
        print(f"📧 Testing signup with email: {test_email}")
        signup_response = requests.post(
            f"{base_url}/api/signup",
            json=signup_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"📊 Signup response status: {signup_response.status_code}")
        print(f"📊 Signup response: {signup_response.text}")
        
        if signup_response.status_code == 200:
            signup_result = signup_response.json()
            if signup_result.get("success"):
                print("✅ SIGNUP SUCCESSFUL!")
                
                print("🔄 Testing login...")
                login_response = requests.post(
                    f"{base_url}/api/login",
                    json=signup_data,
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )
                
                if login_response.status_code == 200:
                    login_result = login_response.json()
                    if login_result.get("success"):
                        print("✅ LOGIN SUCCESSFUL!")
                        print("🎉 COMPLETE AUTHENTICATION FLOW WORKING!")
                        return True
                    else:
                        print(f"❌ Login failed: {login_result.get('message')}")
                        return False
                else:
                    print(f"❌ Login request failed with status {login_response.status_code}")
                    return False
            else:
                print(f"❌ Signup failed: {signup_result.get('message')}")
                return False
        else:
            print(f"❌ Signup request failed with status {signup_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing signup: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_live_signup()
    if success:
        print("\n🎉 LIVE DEPLOYMENT SIGNUP IS WORKING!")
        print("✅ Users can successfully create accounts and log in")
        print("✅ Ready for production use")
    else:
        print("\n❌ SIGNUP FUNCTIONALITY NEEDS DEBUGGING")
