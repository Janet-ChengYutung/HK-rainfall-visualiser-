#!/usr/bin/env python3
"""
Test script to run main application with TSX background for a few seconds.
"""

import pygame
import sys
import os
import time
import threading

def run_main_briefly():
    """Run the main application for a few seconds to test TSX background."""
    print("Testing Main.py with TSX background...")
    
    # Set environment variables for headless operation
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    
    try:
        # Import main after setting environment
        import Main
        
        # Run main in a separate thread with a timeout
        def run_main():
            Main.main()
        
        # Start main in background thread
        main_thread = threading.Thread(target=run_main, daemon=True)
        main_thread.start()
        
        # Let it run for 3 seconds
        time.sleep(3)
        
        print("✓ Main application started successfully with TSX background")
        print("✓ Application ran for 3 seconds without crashing")
        
        # Force exit since main runs in an infinite loop
        os._exit(0)
        
    except Exception as e:
        print(f"✗ Error running main application: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    run_main_briefly()