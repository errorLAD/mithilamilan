import os
import subprocess
import sys

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(e)
        sys.exit(1)

def main():
    # Create Django project
    run_command("django-admin startproject reddit_clone .")
    
    # Create apps
    apps = ["users", "subreddits", "posts"]
    for app in apps:
        run_command(f"python manage.py startapp {app}")
    
    # Create necessary directories
    directories = [
        "static",
        "templates",
        "media",
        "templates/base",
        "templates/users",
        "templates/subreddits",
        "templates/posts"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("Project structure created successfully!")
    print("Next steps:")
    print("1. Create a virtual environment and install requirements")
    print("2. Run migrations")
    print("3. Create a superuser")
    print("4. Start the development server")

if __name__ == "__main__":
    main() 