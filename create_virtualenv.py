import sys
import subprocess

def main():
    # Check if Python version is 3.6 or higher
    if sys.version_info < (3, 6):
        print("Python 3.6 or higher is required.")
        return

    # Set up the virtual environment
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("Virtual environment 'venv' created.")
    except subprocess.CalledProcessError:
        print("Error: Could not create the virtual environment.")
        return

if __name__ == "__main__":
    main()
