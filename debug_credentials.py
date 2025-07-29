#!/usr/bin/env python3
"""
Debug credential loading mechanism
"""

import sys
sys.path.append('/tmp/test_skill_output')

from credential_manager import CredentialManager

def debug_credentials():
    """Debug credential loading"""
    print("🔍 Debugging Credential Loading Mechanism")
    print("=" * 50)
    
    manager = CredentialManager()
    
    print("\n1. Testing get_deployment_credentials()...")
    credentials = manager.get_deployment_credentials()
    print(f"   Found {len(credentials)} credentials:")
    for key, value in credentials.items():
        masked_value = value[:8] + "..." if len(value) > 8 else "***"
        print(f"   ✅ {key}: {masked_value}")
    
    print("\n2. Testing load_credentials() (encrypted file)...")
    stored_creds = manager.load_credentials()
    print(f"   Found {len(stored_creds)} stored credentials")
    
    print("\n3. Testing environment variables...")
    import os
    env_keys = ['RAILWAY_TOKEN', 'VERCEL_TOKEN', 'GITHUB_TOKEN', 'OPENAI_API_KEY']
    for key in env_keys:
        value = os.getenv(key, '')
        if value:
            masked_value = value[:8] + "..." if len(value) > 8 else "***"
            print(f"   ✅ {key}: {masked_value}")
        else:
            print(f"   ❌ {key}: Not set")
    
    print("\n4. Testing provided credentials (hardcoded)...")
    provided_credentials = {
        'RAILWAY_TOKEN': '2e8e81e5-cb08-4ae9-8fe8-4fa94e942a62',
        'VERCEL_TOKEN': 'ZEo01Ou1koSSDWyFw0w9LGjX',
        'GITHUB_APP_ID': '1693043',
        'GODADDY_API_KEY': 'h2K7cZMm5MPB_6Daj9vMhKLqpx3c7ijGDgM',
        'GODADDY_SECRET': 'HqmPSzSHSgbboFYuWJK3NU'
    }
    
    for key, value in provided_credentials.items():
        masked_value = value[:8] + "..." if len(value) > 8 else "***"
        print(f"   ✅ {key}: {masked_value}")
    
    print("\n" + "=" * 50)
    if credentials:
        print("✅ Credential loading mechanism is working")
        return True
    else:
        print("❌ Credential loading mechanism is broken")
        return False

if __name__ == "__main__":
    success = debug_credentials()
    if not success:
        print("\n🔧 Need to fix credential loading mechanism")
        exit(1)
    else:
        print("\n🚀 Credentials ready for autonomous deployment")
