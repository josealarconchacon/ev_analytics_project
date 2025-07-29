#!/usr/bin/env python3
"""
EV Analytics Dashboard Launcher
Run this script to start the interactive web dashboard
"""

import os
import sys
import subprocess

def main():
    """Launch the Streamlit dashboard"""
    print("🚗 Starting EV Analytics Dashboard...")
    print("📊 Loading data and launching web interface...")
    
    # Change to the src directory
    src_dir = os.path.join(os.path.dirname(__file__), 'src')
    os.chdir(src_dir)
    
    # Run streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "dashboard.py",
            "--server.port=8501",
            "--server.headless=true"
        ], check=True)
    except KeyboardInterrupt:
        print("\n Dashboard stopped by user")
    except subprocess.CalledProcessError as e:
        print(f" Error running dashboard: {e}")
        print(" Make sure you have installed the requirements: pip install -r requirements.txt")
    except FileNotFoundError:
        print(" Streamlit not found. Please install requirements: pip install -r requirements.txt")

if __name__ == "__main__":
    main() 