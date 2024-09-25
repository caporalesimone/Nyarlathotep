""" This script is used to create an executable file from the agent.py scripP """

import os
import subprocess
import re
import shutil

def update_version_file(file_path) -> str:
    """ Update the version in the versions.py file """	

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    version_pattern = re.compile(r'CLIENT_SW_VERSION\s*=\s*"(.*?)"')
    new_lines = []
    for line in lines:
        match = version_pattern.match(line)
        if match:
            version = match.group(1)

            version_parts = version.split('.')
            version_parts[-1] = str(int(version_parts[-1]) + 1)
            new_version = '.'.join(version_parts)
            new_lines.append(f'CLIENT_SW_VERSION = "{new_version}"\n')
        else:
            new_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)

    return new_version

def main():
    """ Main function to create the executable file """	

    current_dir = os.path.dirname(os.path.abspath(__file__))

    versions_file_path = os.path.join(current_dir, "versions.py")
    version = update_version_file(versions_file_path)

    output_folder = f"output_{version}"
    output_path = os.path.join(current_dir, output_folder)

    os.makedirs(output_path, exist_ok=True)

    script_path = os.path.join(current_dir, "agent.py")
    command = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--console",
        script_path
    ]

    result = subprocess.run(command, capture_output=True, text=True, cwd=output_path, check=False)

    print("Output:", result.stdout)
    print("Error:", result.stderr)

    # Copy resources to the dist folder
    resources_dir = os.path.join(current_dir, "resources")
    output_dist_dir = os.path.join(output_path, "dist")

    # Copy nssm.exe
    nssm_exe_src = os.path.join(resources_dir, "nssm", "nssm.exe")
    shutil.copy2(nssm_exe_src, output_dist_dir)

    # Copy all .bat files
    bat_file_src = os.path.join(resources_dir, "install_agent_as_service.bat")
    shutil.copy2(bat_file_src, output_dist_dir)
    bat_file_src = os.path.join(resources_dir, "remove_agent_service.bat")
    shutil.copy2(bat_file_src, output_dist_dir)

    # Rename the output folder agent with the version
    os.rename(os.path.join(output_path, "dist"),
              os.path.join(output_path, f"Agent_{version}"))

if __name__ == "__main__":
    main()
