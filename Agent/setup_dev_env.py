import os
import sys
import shutil
import argparse

virtual_env_folder = os.path.normpath('.venv')

def create_virtual_environment():
    if os.path.exists(virtual_env_folder):
        print("❌ A virtual environment already exists. Delete it before continue.")
        exit(1)
    
    os.system(sys.executable + ' -m venv ' + virtual_env_folder)
    if not os.path.exists(virtual_env_folder):
        print("❌ Failed to create the virtual envionment.")
        exit(1)
    print("✔️  Virtual environment created.")
    

def install_packages(pythonVenvExecutable):
    os.system(pythonVenvExecutable + ' -m pip install -r requirements.txt')
    print("✔️  Required packages installed.")


def clean_environment():
    if os.path.exists(virtual_env_folder):
        shutil.rmtree(virtual_env_folder)

if __name__ == "__main__":
    if sys.platform != "win32":
        pythonVenvExecutable = ".venv/bin/python"
    else:
        pythonVenvExecutable = ".venv\\Scripts\\python.exe"

    parser = argparse.ArgumentParser(description="Manage development environment.")
    parser.add_argument('command', choices=['create', 'clean'], help='"create" to set up the environment, "clean" to remove the environment and clean all the repo.')
    args = parser.parse_args()

    if args.command == 'create':
        create_virtual_environment()
        install_packages(pythonVenvExecutable)
        print("💯 Development environment is ready.")
    elif args.command == 'clean':
        clean_environment()
        print("💯 Development environment is deleted.")
