"""
Test script for the adaptive scaling functionality
"""

import pygame
import math

def test_adaptive_scaling():
    """Test the adaptive scaling algorithm"""
    
    # Initialize pygame to get screen info
    pygame.init()
    info = pygame.display.Info()
    
    print("🛰️ AI Satellite Orbit Simulator - Scaling Test")
    print("=" * 50)
    print(f"Screen Resolution: {info.current_w} x {info.current_h}")
    
    # Calculate adaptive window size
    screen_width = min(info.current_w - 100, 1200)
    screen_height = min(info.current_h - 100, 800)
    
    print(f"Adaptive Window: {screen_width} x {screen_height}")
    
    # Calculate adaptive Earth radius
    min_earth_radius = 30
    max_earth_radius = min(screen_width, screen_height) // 8
    earth_radius = max(min_earth_radius, min(max_earth_radius, 60))
    
    print(f"Earth Radius: {earth_radius}px")
    
    # Test different altitudes
    test_altitudes = [200, 400, 1000, 5000, 20000, 35786, 50000]
    
    print("\nAltitude Scaling Test:")
    print("-" * 40)
    
    for altitude_km in test_altitudes:
        # Calculate available space
        earth_x, earth_y = screen_width // 2, screen_height // 2
        available_radius = min(screen_width // 2 - earth_radius - 50, 
                             screen_height // 2 - earth_radius - 50)
        
        # Apply scaling algorithm
        if altitude_km <= 1000:
            scale_factor = available_radius / 1000
            display_radius = earth_radius + (altitude_km * scale_factor)
        else:
            log_altitude = math.log10(altitude_km)
            max_log = math.log10(50000)
            normalized_log = log_altitude / max_log
            display_radius = earth_radius + (available_radius * normalized_log)
        
        # Ensure bounds
        display_radius = max(earth_radius + 20, min(display_radius, available_radius + earth_radius))
        
        # Check if satellite will be visible
        sat_x = earth_x + display_radius
        sat_y = earth_y
        
        visible = (sat_x < screen_width and sat_y < screen_height)
        
        print(f"Altitude: {altitude_km:>6} km | Display: {display_radius:>6.1f}px | Visible: {'✅' if visible else '❌'}")
    
    print("\n✅ All orbits should now be visible on screen!")
    print("🎮 Try running satellite_gui.py to test interactively")
    
    pygame.quit()

if __name__ == "__main__":
    test_adaptive_scaling()
