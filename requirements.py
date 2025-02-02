import subprocess
import sys
import os

def install_requirements():
    # Python package requirements
    python_packages = [
        'tkinter',  # Usually comes with Python
        'pathlib',
        'ctypes'
    ]

    # Node.js packages
    node_packages = [
        'electron-fiddle',
        'asar',
        'source-map-explorer',
        'electron-devtools-installer',
        'electron-debug',
        'devtron'
    ]

    print("Installing Python packages...")
    for package in python_packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except:
            print(f"Note: {package} installation skipped (might be built-in)")

    print("\nChecking for Node.js...")
    try:
        subprocess.check_call(["node", "--version"])
    except:
        print("Node.js not found! Please install from https://nodejs.org/")
        input("Press Enter to exit...")
        sys.exit(1)

    print("\nInstalling Node.js packages globally...")
    for package in node_packages:
        try:
            subprocess.check_call(["npm", "install", "-g", package])
        except Exception as e:
            print(f"Error installing {package}: {str(e)}")

    print("\nSetup complete! You can now run Exe-Decompiler.")

if __name__ == "__main__":
    install_requirements()