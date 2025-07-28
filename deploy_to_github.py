"""
Git deployment script for AI Satellite Orbit Simulator
=====================================================
This script helps you deploy the project to GitHub easily.
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            if result.stdout:
                print(f"Output: {result.stdout.strip()}")
        else:
            print(f"❌ Error in {description}")
            print(f"Error: {result.stderr.strip()}")
            return False
        return True
    except Exception as e:
        print(f"❌ Exception during {description}: {e}")
        return False

def setup_git():
    """Setup git configuration"""
    print("🛠️ Setting up Git configuration...")
    
    # Set git user (you may want to change these)
    run_command('git config user.name "jawad-farooque"', "Setting git username")
    run_command('git config user.email "jawad.farooque1@gmail.com"', "Setting git email")

def deploy_to_github():
    """Deploy the project to GitHub"""
    print("🚀 AI Satellite Orbit Simulator - GitHub Deployment")
    print("=" * 60)
    
    # Check if git is installed
    if not run_command("git --version", "Checking Git installation"):
        print("❌ Git is not installed. Please install Git first.")
        return False
    
    # Setup git configuration
    setup_git()
    
    # Initialize git repository if not already initialized
    if not os.path.exists('.git'):
        run_command("git init", "Initializing Git repository")
    
    # Add remote origin
    repo_url = "https://github.com/jawad-farooque/AI-Simulator.git"
    run_command(f"git remote remove origin", "Removing existing origin (if any)")
    run_command(f"git remote add origin {repo_url}", "Adding remote origin")
    
    # Copy the GitHub README
    try:
        import shutil
        shutil.copy("README_GITHUB.md", "README.md")
        print("✅ Updated README.md for GitHub")
    except Exception as e:
        print(f"⚠️ Warning: Could not update README.md: {e}")
    
    # Add all files
    run_command("git add .", "Adding all files to Git")
    
    # Commit changes
    commit_message = "🛰️ AI Satellite Orbit Simulator - Professional Web Application with 3D Visualization"
    run_command(f'git commit -m "{commit_message}"', "Committing changes")
    
    # Set upstream and push
    run_command("git branch -M main", "Setting main branch")
    run_command("git push -u origin main --force", "Pushing to GitHub")
    
    print("\n🎉 Deployment completed!")
    print(f"📂 Repository URL: {repo_url}")
    print("🌐 Deploy to Streamlit Cloud:")
    print("   1. Go to https://share.streamlit.io")
    print("   2. Connect your GitHub account")
    print("   3. Select 'jawad-farooque/AI-Simulator' repository")
    print("   4. Choose 'streamlit_app_pro.py' as the main file")
    print("   5. Click Deploy!")
    
    return True

def main():
    """Main deployment function"""
    try:
        # Change to project directory
        project_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(project_dir)
        print(f"📁 Working directory: {project_dir}")
        
        # Run deployment
        success = deploy_to_github()
        
        if success:
            print("\n✅ All done! Your AI Satellite Orbit Simulator is now on GitHub!")
        else:
            print("\n❌ Deployment failed. Please check the errors above.")
            
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    main()
