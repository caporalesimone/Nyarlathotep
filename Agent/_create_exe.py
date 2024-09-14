""" This script is used to create an executable file from the agent.py scripP """

import os
import subprocess
import re

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
        "--onedir",
        "--console",
        script_path
    ]

    result = subprocess.run(command, capture_output=True, text=True, cwd=output_path, check=False)

    print("Output:", result.stdout)
    print("Error:", result.stderr)

if __name__ == "__main__":
    main()
