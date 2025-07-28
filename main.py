"""
AI SATELLITE ORBIT SIMULATOR
============================
An interactive physics simulation tool that demonstrates orbital mechanics
using AI-powered classification and real-time visualization.

Features:
- Real-time orbital physics calculations
- Visual satellite orbit simulation
- AI-based orbit classification (LEO/MEO/GEO)
- Interactive user interface
- Educational physics display
"""

import pygame
import numpy as np
import math
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time

class SatelliteOrbitSimulator:
    def __init__(self):
        # Physics constants
        self.EARTH_RADIUS = 6371000  # meters
        self.EARTH_MASS = 5.972e24   # kg
        self.G = 6.67430e-11         # gravitational constant
        
        # Initialize Pygame first to get display info
        pygame.init()
        info = pygame.display.Info()
        
        # Adaptive display constants based on screen size
        self.WINDOW_WIDTH = min(info.current_w - 100, 1400)
        self.WINDOW_HEIGHT = min(info.current_h - 100, 900)
        self.EARTH_DISPLAY_RADIUS = max(40, min(100, self.WINDOW_WIDTH // 20))
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLUE = (100, 149, 237)
        self.GREEN = (34, 139, 34)
        self.RED = (220, 20, 60)
        self.YELLOW = (255, 215, 0)
        self.GRAY = (128, 128, 128)
        self.LIGHT_BLUE = (173, 216, 230)
        
        # Simulation variables
        self.satellite_mass = 1000  # kg
        self.altitude = 400000      # meters (400 km default)
        self.simulation_running = False
        self.simulation_speed = 1.0
        
        # Calculated values
        self.orbital_velocity = 0
        self.orbital_period = 0
        self.centripetal_force = 0
        self.orbit_type = ""
        
        # Animation variables
        self.satellite_angle = 0
        self.satellite_x = 0
        self.satellite_y = 0
        self.trail_points = []
        
        # Create display
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("AI Satellite Orbit Simulator")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, max(20, self.WINDOW_WIDTH // 60))
        self.title_font = pygame.font.Font(None, max(24, self.WINDOW_WIDTH // 40))
        
        # Earth center position
        self.earth_x = self.WINDOW_WIDTH // 3
        self.earth_y = self.WINDOW_HEIGHT // 2
        
    def calculate_orbital_physics(self):
        """Calculate orbital mechanics using real physics equations"""
        # Distance from Earth's center
        orbital_radius = self.EARTH_RADIUS + self.altitude
        
        # Orbital velocity: v = sqrt(GM/r)
        self.orbital_velocity = math.sqrt(self.G * self.EARTH_MASS / orbital_radius)
        
        # Orbital period: T = 2π * sqrt(r³/GM)
        self.orbital_period = 2 * math.pi * math.sqrt(orbital_radius**3 / (self.G * self.EARTH_MASS))
        
        # Centripetal force: F = mv²/r
        self.centripetal_force = (self.satellite_mass * self.orbital_velocity**2) / orbital_radius
        
        # AI-based orbit classification
        self.orbit_type = self.classify_orbit_ai()
        
    def classify_orbit_ai(self):
        """AI logic to classify orbit type based on altitude"""
        altitude_km = self.altitude / 1000
        
        # AI classification rules
        if altitude_km < 2000:
            if altitude_km < 160:
                return "VERY LOW ORBIT (Unstable)"
            elif altitude_km <= 2000:
                return "LEO (Low Earth Orbit)"
        elif altitude_km <= 35786:
            if altitude_km >= 2000 and altitude_km <= 35786:
                return "MEO (Medium Earth Orbit)"
        else:
            if abs(altitude_km - 35786) < 100:
                return "GEO (Geostationary Orbit)"
            else:
                return "HEO (High Earth Orbit)"
        
        return "UNDEFINED ORBIT"
    
    def get_display_radius(self):
        """Calculate display radius for the orbit with adaptive scaling"""
        altitude_km = self.altitude / 1000
        
        # Calculate available space for orbit
        available_width = self.WINDOW_WIDTH - self.earth_x - 350  # Leave space for info panel
        available_height = self.WINDOW_HEIGHT - 100  # Leave margin
        available_radius = min(available_width, available_height // 2) - self.EARTH_DISPLAY_RADIUS - 20
        
        # Adaptive scaling based on altitude
        if altitude_km <= 1000:
            # Linear scaling for low altitudes
            scale_factor = available_radius / 1000
            display_radius = self.EARTH_DISPLAY_RADIUS + (altitude_km * scale_factor)
        else:
            # Logarithmic scaling for high altitudes
            log_altitude = math.log10(altitude_km)
            max_log = math.log10(100000)  # Maximum reasonable altitude
            normalized_log = min(log_altitude / max_log, 1.0)
            display_radius = self.EARTH_DISPLAY_RADIUS + (available_radius * normalized_log)
        
        # Ensure minimum and maximum bounds
        min_radius = self.EARTH_DISPLAY_RADIUS + 15
        max_radius = self.EARTH_DISPLAY_RADIUS + available_radius
        
        return max(min_radius, min(display_radius, max_radius))
    
    def update_satellite_position(self):
        """Update satellite position for animation with realistic orbital speed"""
        if not self.simulation_running:
            return
            
        # Calculate angular velocity (rad/s) based on real orbital period
        if self.orbital_period > 0:
            real_angular_velocity = (2 * math.pi) / self.orbital_period
            
            # Scale for visual appeal (speed up animation)
            visual_speed_multiplier = 50 * self.simulation_speed
            angular_velocity = real_angular_velocity * visual_speed_multiplier
            
            # Update angle
            self.satellite_angle += angular_velocity * 0.016  # ~60 FPS timing
            
            # Keep angle in range [0, 2π]
            if self.satellite_angle >= 2 * math.pi:
                self.satellite_angle -= 2 * math.pi
            
            # Calculate satellite position
            display_radius = self.get_display_radius()
            self.satellite_x = self.earth_x + display_radius * math.cos(self.satellite_angle)
            self.satellite_y = self.earth_y + display_radius * math.sin(self.satellite_angle)
            
            # Add to trail
            self.trail_points.append((int(self.satellite_x), int(self.satellite_y)))
            
            # Adaptive trail length based on orbit size
            max_trail_length = max(100, min(400, int(display_radius * 3)))
            if len(self.trail_points) > max_trail_length:
                self.trail_points.pop(0)
    
    def draw_earth(self):
        """Draw Earth with realistic appearance"""
        # Draw Earth
        pygame.draw.circle(self.screen, self.BLUE, 
                          (int(self.earth_x), int(self.earth_y)), 
                          self.EARTH_DISPLAY_RADIUS)
        
        # Draw continents (simplified)
        pygame.draw.circle(self.screen, self.GREEN, 
                          (int(self.earth_x - 20), int(self.earth_y - 10)), 15)
        pygame.draw.circle(self.screen, self.GREEN, 
                          (int(self.earth_x + 25), int(self.earth_y + 20)), 12)
        pygame.draw.circle(self.screen, self.GREEN, 
                          (int(self.earth_x - 10), int(self.earth_y + 30)), 10)
        
        # Draw Earth outline
        pygame.draw.circle(self.screen, self.WHITE, 
                          (int(self.earth_x), int(self.earth_y)), 
                          self.EARTH_DISPLAY_RADIUS, 2)
    
    def draw_orbit_path(self):
        """Draw the orbital path"""
        display_radius = self.get_display_radius()
        pygame.draw.circle(self.screen, self.GRAY, 
                          (int(self.earth_x), int(self.earth_y)), 
                          int(display_radius), 1)
    
    def draw_satellite(self):
        """Draw the satellite with adaptive sizing"""
        if self.simulation_running:
            # Draw satellite trail with fade effect
            if len(self.trail_points) > 1:
                for i in range(1, len(self.trail_points)):
                    alpha = i / len(self.trail_points)
                    color = (int(255 * alpha), int(200 * alpha), 0)
                    trail_size = max(1, int(3 * alpha))
                    if i < len(self.trail_points):
                        pygame.draw.circle(self.screen, color, self.trail_points[i], trail_size)
            
            # Adaptive satellite size based on display radius
            display_radius = self.get_display_radius()
            satellite_size = max(4, min(10, int(display_radius / 20)))
            
            # Draw satellite
            pygame.draw.circle(self.screen, self.RED, 
                              (int(self.satellite_x), int(self.satellite_y)), satellite_size + 2)
            pygame.draw.circle(self.screen, self.YELLOW, 
                              (int(self.satellite_x), int(self.satellite_y)), satellite_size)
            
            # Draw velocity vector (adaptive length)
            vector_length = min(40, display_radius / 4)
            vector_x = self.satellite_x + vector_length * math.cos(self.satellite_angle + math.pi/2)
            vector_y = self.satellite_y + vector_length * math.sin(self.satellite_angle + math.pi/2)
            pygame.draw.line(self.screen, self.WHITE, 
                           (self.satellite_x, self.satellite_y), 
                           (vector_x, vector_y), 2)
    
    def draw_info_panel(self):
        """Draw information panel with calculated values"""
        panel_x = self.WINDOW_WIDTH - 350
        panel_y = 50
        panel_width = 320
        panel_height = min(450, self.WINDOW_HEIGHT - 100)
        
        # Draw panel background
        pygame.draw.rect(self.screen, (30, 30, 30), 
                        (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(self.screen, self.WHITE, 
                        (panel_x, panel_y, panel_width, panel_height), 2)
        
        # Title
        title = self.title_font.render("Orbital Parameters", True, self.WHITE)
        self.screen.blit(title, (panel_x + 10, panel_y + 10))
        
        # Display values
        y_offset = 50
        display_radius = self.get_display_radius()
        scale_ratio = display_radius / self.EARTH_DISPLAY_RADIUS
        
        info_texts = [
            f"Satellite Mass: {self.satellite_mass:,.0f} kg",
            f"Altitude: {self.altitude/1000:,.1f} km",
            f"Orbital Velocity: {self.orbital_velocity:,.0f} m/s",
            f"Orbital Period: {self.orbital_period/3600:.2f} hours",
            f"Centripetal Force: {self.centripetal_force:,.0f} N",
            f"Orbit Type: {self.orbit_type}",
            "",
            f"Display Scale: {scale_ratio:.1f}x",
            f"Earth Radius: {self.EARTH_DISPLAY_RADIUS}px",
            f"Orbit Radius: {display_radius:.0f}px",
            "",
            "AI Analysis:",
            self.get_ai_analysis()
        ]
        
        for i, text in enumerate(info_texts):
            if text and (panel_y + y_offset + i * 22) < (panel_y + panel_height - 20):
                color = self.LIGHT_BLUE if ":" in text else self.WHITE
                if "Display Scale" in text or "Radius" in text:
                    color = self.GRAY
                rendered_text = self.font.render(text, True, color)
                self.screen.blit(rendered_text, (panel_x + 10, panel_y + y_offset + i * 22))
    
    def get_ai_analysis(self):
        """Generate AI-style analysis of the orbit"""
        altitude_km = self.altitude / 1000
        
        if altitude_km < 160:
            return "⚠️ Orbit too low - atmospheric drag"
        elif altitude_km <= 400:
            return "✅ Ideal for Earth observation"
        elif altitude_km <= 1000:
            return "🛰️ Good for communications"
        elif altitude_km <= 20000:
            return "🌐 Navigation satellite range"
        elif abs(altitude_km - 35786) < 100:
            return "🌍 Perfect geostationary orbit!"
        else:
            return "🚀 Deep space trajectory"
    
    def draw_controls_info(self):
        """Draw control instructions"""
        controls = [
            "Controls:",
            "Enter: Start/Stop simulation",
            "↑/↓: Adjust altitude",
            "←/→: Adjust mass",
            "Space: Reset trail",
            "+/-: Simulation speed"
        ]
        
        for i, control in enumerate(controls):
            color = self.YELLOW if i == 0 else self.WHITE
            text = self.font.render(control, True, color)
            self.screen.blit(text, (20, 20 + i * 25))
    
    def handle_input(self):
        """Handle keyboard input for parameter adjustment"""
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP]:
            self.altitude += 1000  # Increase altitude by 1 km
            self.altitude = min(self.altitude, 100000000)  # Max 100,000 km
            self.calculate_orbital_physics()
        
        if keys[pygame.K_DOWN]:
            self.altitude -= 1000  # Decrease altitude by 1 km
            self.altitude = max(self.altitude, 150000)  # Min 150 km
            self.calculate_orbital_physics()
        
        if keys[pygame.K_RIGHT]:
            self.satellite_mass += 100  # Increase mass by 100 kg
            self.satellite_mass = min(self.satellite_mass, 100000)  # Max 100 tons
            self.calculate_orbital_physics()
        
        if keys[pygame.K_LEFT]:
            self.satellite_mass -= 100  # Decrease mass by 100 kg
            self.satellite_mass = max(self.satellite_mass, 100)  # Min 100 kg
            self.calculate_orbital_physics()
        
        if keys[pygame.K_PLUS] or keys[pygame.K_EQUALS]:
            self.simulation_speed = min(self.simulation_speed * 1.1, 10.0)
        
        if keys[pygame.K_MINUS]:
            self.simulation_speed = max(self.simulation_speed * 0.9, 0.1)
    
    def run_simulation(self):
        """Main simulation loop"""
        # Initial calculations
        self.calculate_orbital_physics()
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.simulation_running = not self.simulation_running
                        if self.simulation_running:
                            self.satellite_angle = 0
                            self.trail_points = []
                    
                    elif event.key == pygame.K_SPACE:
                        self.trail_points = []
            
            # Handle continuous input
            self.handle_input()
            
            # Update physics
            self.update_satellite_position()
            
            # Clear screen
            self.screen.fill(self.BLACK)
            
            # Draw everything
            self.draw_earth()
            self.draw_orbit_path()
            self.draw_satellite()
            self.draw_info_panel()
            self.draw_controls_info()
            
            # Draw simulation status
            status = "RUNNING" if self.simulation_running else "PAUSED"
            status_color = self.GREEN if self.simulation_running else self.RED
            status_text = self.font.render(f"Simulation: {status}", True, status_color)
            self.screen.blit(status_text, (20, self.WINDOW_HEIGHT - 100))
            
            speed_text = self.font.render(f"Speed: {self.simulation_speed:.1f}x", True, self.WHITE)
            self.screen.blit(speed_text, (20, self.WINDOW_HEIGHT - 75))
            
            # Update display
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()

def main():
    """Main function to run the AI Satellite Orbit Simulator"""
    print("🛰️ AI SATELLITE ORBIT SIMULATOR 🛰️")
    print("=" * 50)
    print("Starting the interactive orbital physics simulation...")
    print("Features:")
    print("• Real-time orbital mechanics calculations")
    print("• AI-powered orbit classification")
    print("• Interactive satellite visualization")
    print("• Educational physics display")
    print("=" * 50)
    
    try:
        simulator = SatelliteOrbitSimulator()
        simulator.run_simulation()
    except Exception as e:
        print(f"Error running simulation: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()