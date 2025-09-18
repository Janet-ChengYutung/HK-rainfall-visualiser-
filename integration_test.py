#!/usr/bin/env python3
"""
Integration test to verify TSX background functionality end-to-end.
"""

import pygame
import sys
import os
import tempfile
import shutil

def test_tsx_integration():
    """Test the complete TSX background integration."""
    print("Running TSX Background Integration Test...")
    
    # Set headless mode
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    
    success_count = 0
    total_tests = 4
    
    try:
        # Test 1: Import modules
        print("\n1. Testing module imports...")
        try:
            from tsx_background_renderer import TSXBackgroundRenderer, create_tsx_background
            import Main
            print("✓ All modules imported successfully")
            success_count += 1
        except Exception as e:
            print(f"✗ Module import failed: {e}")
        
        # Test 2: Parse TSX file
        print("\n2. Testing TSX file parsing...")
        try:
            renderer = TSXBackgroundRenderer()
            styles = renderer.parse_tsx_file("animation.tsx")
            if styles and any(styles.values()):
                print("✓ TSX file parsed successfully")
                print(f"  - Found {len(styles.get('gradients', []))} gradients")
                print(f"  - Found {len(styles.get('particles', []))} particle groups")
                print(f"  - Found {len(styles.get('text_elements', []))} text elements")
                success_count += 1
            else:
                print("✗ TSX parsing returned empty results")
        except Exception as e:
            print(f"✗ TSX parsing failed: {e}")
        
        # Test 3: Render background
        print("\n3. Testing background rendering...")
        try:
            pygame.init()
            screen = pygame.display.set_mode((800, 600), pygame.HIDDEN)
            
            background = create_tsx_background("animation.tsx", 800, 600)
            if background and background.get_size() == (800, 600):
                print("✓ Background rendered successfully")
                print(f"  - Size: {background.get_size()}")
                success_count += 1
            else:
                print("✗ Background rendering failed")
        except Exception as e:
            print(f"✗ Background rendering failed: {e}")
        
        # Test 4: Main.py integration
        print("\n4. Testing Main.py integration...")
        try:
            # Check if Main.py has the TSX imports and configuration
            with open("Main.py", 'r') as f:
                main_content = f.read()
            
            has_import = "from tsx_background_renderer import create_tsx_background" in main_content
            has_config = "TSX_BACKGROUND_PATH" in main_content
            has_rendering = "tsx_background_surface" in main_content
            
            if has_import and has_config and has_rendering:
                print("✓ Main.py integration complete")
                print("  - TSX import: ✓")
                print("  - Configuration: ✓") 
                print("  - Rendering logic: ✓")
                success_count += 1
            else:
                print("✗ Main.py integration incomplete")
                print(f"  - TSX import: {'✓' if has_import else '✗'}")
                print(f"  - Configuration: {'✓' if has_config else '✗'}")
                print(f"  - Rendering logic: {'✓' if has_rendering else '✗'}")
        except Exception as e:
            print(f"✗ Main.py integration check failed: {e}")
        
        # Results
        print(f"\n=== Integration Test Results ===")
        print(f"Passed: {success_count}/{total_tests} tests")
        print(f"Success Rate: {(success_count/total_tests)*100:.1f}%")
        
        if success_count == total_tests:
            print("🎉 All tests passed! TSX background integration is working correctly.")
            return True
        else:
            print("⚠️  Some tests failed. Check the output above for details.")
            return False
        
    except Exception as e:
        print(f"✗ Integration test failed with error: {e}")
        return False
    
    finally:
        try:
            pygame.quit()
        except:
            pass

if __name__ == "__main__":
    success = test_tsx_integration()
    sys.exit(0 if success else 1)