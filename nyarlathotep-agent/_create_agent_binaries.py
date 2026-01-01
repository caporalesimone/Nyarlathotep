"""
This script creates executable binaries for the agent for the current OS.
The version is read from versions.py CLIENT_SW_VERSION (no auto-increment).
- On Windows: generates nyarlathotep-agent-win-x.y.zip
- On Linux:   generates nyarlathotep-agent-linux-x.y.zip

This script should be run on both Windows and Linux systems to generate both binaries.
(Typically done via GitHub Actions with matrix strategy)
"""

import os
import platform
import subprocess
import re
import shutil
import zipfile
from pathlib import Path


def get_version(versions_file_path: str) -> str:
    """Extract CLIENT_SW_VERSION from versions.py"""
    with open(versions_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    match = re.search(r'CLIENT_SW_VERSION\s*=\s*"(.*?)"', content)
    if match:
        return match.group(1)
    raise ValueError("Could not find CLIENT_SW_VERSION in versions.py")


def get_os_name() -> str:
    """Determine current OS (Windows or Linux)"""
    system = platform.system()
    if system == "Windows":
        return "win"
    elif system in ("Linux", "Darwin"):  # Darwin for macOS
        return "linux"
    else:
        raise ValueError(f"Unsupported OS: {system}")


def create_binary(current_dir: str, version: str, output_path: str, os_name: str) -> str:
    """Create executable with PyInstaller for the current OS"""
    print(f"\n{'='*60}")
    print(f"Creating {os_name.upper()} binary for version {version}...")
    print(f"System: {platform.system()}")
    print(f"{'='*60}")
    
    script_path = os.path.join(current_dir, "agent.py")
    build_path = os.path.join(output_path, f"build_{os_name}")
    os.makedirs(build_path, exist_ok=True)
    
    command = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--console",
        "--specpath", build_path,
        "--distpath", os.path.join(build_path, "dist"),
        "--workpath", os.path.join(build_path, "build"),
        f"--name=Agent_{version}",
        script_path
    ]
    
    result = subprocess.run(command, capture_output=True, text=True, cwd=current_dir, check=False)
    
    if result.returncode != 0:
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        raise RuntimeError(f"PyInstaller failed for {os_name.upper()} binary")
    
    dist_dir = os.path.join(build_path, "dist")
    
    # Copy platform-specific resources for Windows
    if os_name == "win":
        resources_dir = os.path.join(current_dir, "resources")
        
        # Copy nssm.exe
        nssm_exe_src = os.path.join(resources_dir, "nssm", "nssm.exe")
        if os.path.exists(nssm_exe_src):
            shutil.copy2(nssm_exe_src, dist_dir)
            print(f"Copied: nssm.exe")
        
        # Copy batch files
        for bat_file in ["install_agent_as_service.bat", "remove_agent_service.bat"]:
            bat_src = os.path.join(resources_dir, bat_file)
            if os.path.exists(bat_src):
                shutil.copy2(bat_src, dist_dir)
                print(f"Copied: {bat_file}")
    
    # Rename dist folder to Agent_version
    agent_folder = os.path.join(build_path, f"Agent_{version}")
    try:
        shutil.move(dist_dir, agent_folder)
        print(f"Renamed dist to: Agent_{version}")
    except Exception as e:
        print(f"Warning: Could not rename folder with shutil.move: {e}")
        # Fallback: just return the dist_dir as is
        agent_folder = dist_dir
    
    return agent_folder


def create_zip(source_dir: str, zip_name: str, output_path: str) -> str:
    """Create a zip file from a directory"""
    zip_path = os.path.join(output_path, f"{zip_name}.zip")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, arcname)
    
    print(f"Created: {zip_path}")
    return zip_path


def main():
    """Main function to create agent binary for current OS"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    versions_file_path = os.path.join(current_dir, "versions.py")
    
    # Get version from versions.py (no auto-increment)
    version = get_version(versions_file_path)
    os_name = get_os_name()
    
    print(f"\nAgent version: {version}")
    print(f"Target OS: {os_name.upper()}")
    
    # Create output directory
    output_path = os.path.join(current_dir, f"output_{version}")
    os.makedirs(output_path, exist_ok=True)
    
    try:
        # Create binary for current OS
        dist_dir = create_binary(current_dir, version, output_path, os_name)
        
        # Create zip file
        zip_name = f"nyarlathotep-agent-{os_name}-{version}"
        zip_path = create_zip(dist_dir, zip_name, output_path)
        
        print(f"\n{'='*60}")
        print(f"SUCCESS: Created {os_name.upper()} agent binary")
        print(f"{'='*60}")
        print(f"Version: {version}")
        print(f"Output:  {zip_path}")
        print(f"\nOutput directory: {output_path}")
        
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"ERROR: {str(e)}")
        print(f"{'='*60}")
        raise


if __name__ == "__main__":
    main()

