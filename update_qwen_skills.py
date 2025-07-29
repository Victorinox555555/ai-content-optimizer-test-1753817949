#!/usr/bin/env python3
"""
Update QWEN-GPT-AGI skills to use autonomous deployment system
"""

import os
import sys

def update_deploy_vercel_skill():
    """Update deploy_vercel.py to use autonomous deployment"""
    skill_path = "/home/ubuntu/QWEN-GPT-AGI/skills/deploy_vercel.py"
    
    updated_content = '''
def deploy_vercel(context):
    """Deploy to Vercel using autonomous deployment system"""
    import sys
    sys.path.append('/tmp/test_skill_output')
    
    from autonomous_deployer import AutonomousDeployer
    
    work_dir = context.get('work_dir', '/tmp/test_skill_output')
    
    credentials = {
        'VERCEL_TOKEN': context.get('secrets', {}).get('VERCEL_TOKEN'),
        'GITHUB_TOKEN': context.get('secrets', {}).get('GITHUB_TOKEN'),
        'OPENAI_API_KEY': context.get('secrets', {}).get('OPENAI_API_KEY'),
        'STRIPE_SECRET_KEY': context.get('secrets', {}).get('STRIPE_SECRET_KEY'),
        'FLASK_SECRET_KEY': context.get('secrets', {}).get('FLASK_SECRET_KEY')
    }
    
    deployer = AutonomousDeployer(credentials)
    
    mvp_name = context.get('idea', {}).get('name', 'autonomous-mvp')
    
    result = deployer.deploy_mvp(
        mvp_path=work_dir,
        mvp_name=mvp_name,
        platform='vercel'
    )
    
    if result["success"]:
        return f"✅ Autonomous deployment complete! Live URL: {result['urls'].get('live_site', 'Deploying...')}"
    else:
        return f"❌ Deployment failed: {result.get('error', 'Unknown error')}"
'''
    
    with open(skill_path, 'w') as f:
        f.write(updated_content)
    
    print(f"✅ Updated {skill_path}")

def update_deploy_render_skill():
    """Create deploy_render.py skill"""
    skill_path = "/home/ubuntu/QWEN-GPT-AGI/skills/deploy_render.py"
    
    content = '''
def deploy_render(context):
    """Deploy to Render using autonomous deployment system"""
    import sys
    sys.path.append('/tmp/test_skill_output')
    
    from autonomous_deployer import AutonomousDeployer
    
    work_dir = context.get('work_dir', '/tmp/test_skill_output')
    
    credentials = {
        'RENDER_API_KEY': context.get('secrets', {}).get('RENDER_API_KEY'),
        'GITHUB_TOKEN': context.get('secrets', {}).get('GITHUB_TOKEN'),
        'OPENAI_API_KEY': context.get('secrets', {}).get('OPENAI_API_KEY'),
        'STRIPE_SECRET_KEY': context.get('secrets', {}).get('STRIPE_SECRET_KEY'),
        'FLASK_SECRET_KEY': context.get('secrets', {}).get('FLASK_SECRET_KEY')
    }
    
    deployer = AutonomousDeployer(credentials)
    
    mvp_name = context.get('idea', {}).get('name', 'autonomous-mvp')
    
    result = deployer.deploy_mvp(
        mvp_path=work_dir,
        mvp_name=mvp_name,
        platform='render'
    )
    
    if result["success"]:
        return f"✅ Autonomous deployment complete! Live URL: {result['urls'].get('live_site', 'Deploying...')}"
    else:
        return f"❌ Deployment failed: {result.get('error', 'Unknown error')}"
'''
    
    with open(skill_path, 'w') as f:
        f.write(content)
    
    print(f"✅ Created {skill_path}")

def update_deploy_railway_skill():
    """Create deploy_railway.py skill"""
    skill_path = "/home/ubuntu/QWEN-GPT-AGI/skills/deploy_railway.py"
    
    content = '''
def deploy_railway(context):
    """Deploy to Railway using autonomous deployment system"""
    import sys
    sys.path.append('/tmp/test_skill_output')
    
    from autonomous_deployer import AutonomousDeployer
    
    work_dir = context.get('work_dir', '/tmp/test_skill_output')
    
    credentials = {
        'RAILWAY_TOKEN': context.get('secrets', {}).get('RAILWAY_TOKEN'),
        'GITHUB_TOKEN': context.get('secrets', {}).get('GITHUB_TOKEN'),
        'OPENAI_API_KEY': context.get('secrets', {}).get('OPENAI_API_KEY'),
        'STRIPE_SECRET_KEY': context.get('secrets', {}).get('STRIPE_SECRET_KEY'),
        'FLASK_SECRET_KEY': context.get('secrets', {}).get('FLASK_SECRET_KEY')
    }
    
    deployer = AutonomousDeployer(credentials)
    
    mvp_name = context.get('idea', {}).get('name', 'autonomous-mvp')
    
    result = deployer.deploy_mvp(
        mvp_path=work_dir,
        mvp_name=mvp_name,
        platform='railway'
    )
    
    if result["success"]:
        return f"✅ Autonomous deployment complete! Live URL: {result['urls'].get('live_site', 'Deploying...')}"
    else:
        return f"❌ Deployment failed: {result.get('error', 'Unknown error')}"
'''
    
    with open(skill_path, 'w') as f:
        f.write(content)
    
    print(f"✅ Created {skill_path}")

if __name__ == "__main__":
    print("🔄 Updating QWEN-GPT-AGI skills for autonomous deployment...")
    
    update_deploy_vercel_skill()
    update_deploy_render_skill()
    update_deploy_railway_skill()
    
    print("✅ All deployment skills updated!")
