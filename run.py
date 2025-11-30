"""
Quick start script for the Analytics Backend
"""
import subprocess
import sys
import os

def main():
    """Run the FastAPI server"""
    print("Starting Analytics Backend API...")
    print("Server will be available at http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "app.main:app",
            "--reload",
            "--host", "0.0.0.0",
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n\nServer stopped.")

if __name__ == "__main__":
    main()

