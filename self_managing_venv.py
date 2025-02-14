"""
Self-Managing Virtual Environment Checks & Setup Script
*Just include at the very top (first thing) of any python script*
*all imports can be pushed up at the top before everything else*
"""

import os
import sys
import subprocess
import platform

VENV_FOLDER = "venv"  # Change this if using a different folder name
SYSTEM_INFO_FILE = os.path.join(VENV_FOLDER, "system_info.txt")  # Store system details

def get_system_info():
    """Returns a string representing the current system for compatibility checking."""
    return f"{platform.system()}-{platform.release()}-{sys.executable}"

def is_venv_compatible():
    """Checks if the existing virtual environment matches the system it was created on."""
    if not os.path.exists(VENV_FOLDER):
        return False  # No venv exists, so it's not compatible

    if not os.path.exists(SYSTEM_INFO_FILE):
        return False  # No system info file means we can't verify compatibility

    # Read stored system info
    with open(SYSTEM_INFO_FILE, "r") as f:
        stored_info = f.read().strip()

    # Compare with current system info
    return stored_info == get_system_info()

def delete_virtual_environment():
    """Deletes the existing virtual environment if it is incompatible."""
    if os.path.exists(VENV_FOLDER):
        print("🗑️ Removing incompatible virtual environment...")
        if sys.platform == "win32":
            subprocess.run(["rmdir", "/s", "/q", VENV_FOLDER], shell=True)  # Windows delete command
        else:
            subprocess.run(["rm", "-rf", VENV_FOLDER])  # macOS/Linux delete command
        print("✅ Virtual environment removed.")

def create_virtual_environment():
    """Creates a fresh virtual environment and stores system info for compatibility checks."""
    print("🔧 Creating a new virtual environment...")
    subprocess.run([sys.executable, "-m", "venv", VENV_FOLDER])
    
    # Store the system info for future compatibility checks
    with open(SYSTEM_INFO_FILE, "w") as f:
        f.write(get_system_info())

    print("✅ Virtual environment created.")

def install_dependencies():
    """Installs dependencies from requirements.txt only if they are missing."""
    requirements_file = "requirements.txt"
    pip_executable = os.path.join(VENV_FOLDER, "Scripts" if sys.platform == "win32" else "bin", "pip")

    if os.path.exists(requirements_file):
        print("📦 Installing dependencies from requirements.txt...")
        subprocess.run([pip_executable, "install", "-r", requirements_file])
        print("✅ Dependencies installed.")
    else:
        print("⚠️ No requirements.txt file found. Skipping dependency installation.")

def check_dependencies():
    """Checks if required modules are installed inside the virtual environment."""
    try:
        import psycopg2
        import serial
        print("✅ All required modules are installed.")
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}. Installing now...")
        install_dependencies()

# ✅ Manage Virtual Environment
if not is_venv_compatible():
    delete_virtual_environment()
    create_virtual_environment()

# ✅ Install dependencies and check modules
install_dependencies()
check_dependencies()

# 🚀 Now continue running the actual program
print("🚀 Starting Mitutoyo Measurement Logger...")
