#!/usr/bin/env python3
"""
ArogyaJal Predictive Maintenance - Zero Dependency Launcher
Uses ONLY Python standard library - NO pip installs needed!
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

def print_banner():
    """Print welcome banner."""
    print("\n" + "="*60)
    print("🚀 ArogyaJal Predictive Maintenance System")
    print("="*60)
    print("✨ ZERO dependencies • NO pip installs • Works offline")
    print("="*60 + "\n")

def check_files():
    """Check if required files exist."""
    required_files = ['index.html', 'data/pump_data.csv']
    missing = []

    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)

    if missing:
        print("❌ Missing required files:")
        for file in missing:
            print(f"   - {file}")
        print("\n💡 Please ensure all files are in the correct location")
        return False

    print("✅ All required files found")
    return True

def start_server(port=8000):
    """Start HTTP server using Python standard library."""
    try:
        # Change to script directory
        os.chdir(Path(__file__).parent)

        # Check files
        if not check_files():
            input("\nPress Enter to exit...")
            return

        # Custom handler to suppress logs
        class QuietHandler(http.server.SimpleHTTPRequestHandler):
            def log_message(self, format, *args):
                pass  # Suppress default logging

        # Create server
        with socketserver.TCPServer(("", port), QuietHandler) as httpd:
            url = f"http://localhost:{port}/index.html"

            print(f"🌐 Server started successfully!")
            print(f"📱 Opening browser at: {url}")
            print(f"🛑 Press Ctrl+C to stop the server\n")
            print("-" * 60)
            print("💡 TIP: If browser doesn't open automatically,")
            print(f"   copy this URL: {url}")
            print("-" * 60 + "\n")

            # Try to open browser
            try:
                webbrowser.open(url)
                print("✅ Browser opened automatically\n")
            except:
                print("⚠️  Please open the URL manually in your browser\n")

            # Start serving
            print("🎯 Server running... Ready for predictions!")
            print("=" * 60 + "\n")

            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n\n" + "=" * 60)
                print("👋 Server stopped by user")
                print("=" * 60)
                print("\n✅ Thank you for using ArogyaJal!")
                print("💡 Run this script again anytime to restart\n")

    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {port} is already in use")
            print(f"💡 Try a different port or close the other application")
            print(f"   To use different port: python run_app.py 8080")
        else:
            print(f"❌ Error starting server: {e}")

        input("\nPress Enter to exit...")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        input("\nPress Enter to exit...")

def main():
    """Main function."""
    print_banner()

    # Check Python version
    if sys.version_info < (3, 0):
        print("❌ Python 3+ is required")
        print("💡 Please upgrade Python and try again")
        input("\nPress Enter to exit...")
        return

    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

    # Get port from command line or use default
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"⚠️  Invalid port number, using default: {port}")

    # Start server
    start_server(port)

if __name__ == "__main__":
    main()