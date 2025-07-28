import pygame
import numpy as np
import math
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time

class SatelliteOrbitSimulator:
    def __init__(self):
        self.EARTH_RADIUS = 6371000
        self.EARTH_MASS = 5.972e24
        self.G = 6.67430e-11
        
        pygame.init()
        info = pygame.display.Info()
        
        self.WINDOW_WIDTH = min(info.current_w - 100, 1400)
        self.WINDOW_HEIGHT = min(info.current_h - 100, 900)
        self.EARTH_DISPLAY_RADIUS = max(40, min(100, self.WINDOW_WIDTH // 20))
        
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLUE = (100, 149, 237)
        self.GREEN = (34, 139, 34)
        self.RED = (220, 20, 60)
        self.YELLOW = (255, 215, 0)
        self.GRAY = (128, 128, 128)
        self.LIGHT_BLUE = (173, 216, 230)
        
        self.satellite_mass = 1000
        self.altitude = 400000
        
        self.orbital_velocity = 0
        self.orbital_period = 0
        self.centripetal_force = 0
        self.orbit_type = ""
        
        self.satellite_angle = 0
        self.trail_points = []
        self.is_paused = False
        self.running = True
        
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("AI Satellite Orbit Simulator")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, max(24, self.WINDOW_WIDTH // 60))
        
        self.earth_x = self.WINDOW_WIDTH // 4
        self.earth_y = self.WINDOW_HEIGHT // 2
        
    def calculate_orbital_parameters(self):
        orbital_radius = self.EARTH_RADIUS + self.altitude
        self.orbital_velocity = math.sqrt(self.G * self.EARTH_MASS / orbital_radius)
        self.orbital_period = 2 * math.pi * math.sqrt(orbital_radius**3 / (self.G * self.EARTH_MASS))
        self.centripetal_force = (self.satellite_mass * self.orbital_velocity**2) / orbital_radius
        self.orbit_type = self.classify_orbit(self.altitude / 1000)
    
    def classify_orbit(self, altitude_km):
        if altitude_km < 160:
            return "VERY LOW (Unstable)"
        elif altitude_km <= 2000:
            return "LEO (Low Earth Orbit)"
        elif altitude_km <= 35786:
            return "MEO (Medium Earth Orbit)"
        elif abs(altitude_km - 35786) < 100:
            return "GEO (Geostationary)"
        else:
            return "HEO (High Earth Orbit)"
    
    def calculate_display_radius(self):
        available_width = self.WINDOW_WIDTH - self.earth_x - 350
        available_height = self.WINDOW_HEIGHT - 100
        max_display_radius = min(available_width, available_height) // 2
        
        altitude_km = self.altitude / 1000
        if altitude_km <= 2000:
            scale_factor = max_display_radius / 2000
            display_radius = self.EARTH_DISPLAY_RADIUS + (altitude_km * scale_factor)
        else:
            log_altitude = math.log10(altitude_km)
            max_log = math.log10(100000)
            normalized_log = log_altitude / max_log
            display_radius = self.EARTH_DISPLAY_RADIUS + (max_display_radius * normalized_log)
        
        return max(self.EARTH_DISPLAY_RADIUS + 20, 
                  min(display_radius, self.EARTH_DISPLAY_RADIUS + max_display_radius))
    
    def update_satellite_position(self):
        if not self.is_paused:
            display_radius = self.calculate_display_radius()
            orbital_radius = self.EARTH_RADIUS + self.altitude
            angular_velocity = math.sqrt(self.G * self.EARTH_MASS / orbital_radius**3)
            
            if self.orbital_period > 0:
                angular_velocity *= 50
            
            self.satellite_angle += angular_velocity * 0.016
            
            if self.satellite_angle >= 2 * math.pi:
                self.satellite_angle -= 2 * math.pi
            
            sat_x = self.earth_x + display_radius * math.cos(self.satellite_angle)
            sat_y = self.earth_y + display_radius * math.sin(self.satellite_angle)
            
            self.trail_points.append((int(sat_x), int(sat_y)))
            
            trail_length = max(50, min(200, int(display_radius)))
            if len(self.trail_points) > trail_length:
                self.trail_points.pop(0)
            
            return sat_x, sat_y, display_radius
        return None, None, self.calculate_display_radius()
    
    def draw_earth(self):
        pygame.draw.circle(self.screen, self.BLUE, 
                          (self.earth_x, self.earth_y), self.EARTH_DISPLAY_RADIUS)
        
        continent_scale = self.EARTH_DISPLAY_RADIUS / 60
        pygame.draw.circle(self.screen, self.GREEN, 
                          (int(self.earth_x - 15 * continent_scale), 
                           int(self.earth_y - 10 * continent_scale)), 
                          max(3, int(8 * continent_scale)))
        pygame.draw.circle(self.screen, self.GREEN, 
                          (int(self.earth_x + 20 * continent_scale), 
                           int(self.earth_y + 15 * continent_scale)), 
                          max(2, int(6 * continent_scale)))
        
        pygame.draw.circle(self.screen, self.WHITE, 
                          (self.earth_x, self.earth_y), self.EARTH_DISPLAY_RADIUS, 2)
    
    def draw_orbit_and_satellite(self, sat_x, sat_y, display_radius):
        pygame.draw.circle(self.screen, self.GRAY, 
                          (self.earth_x, self.earth_y), int(display_radius), 1)
        
        if sat_x is not None and sat_y is not None:
            for i, point in enumerate(self.trail_points):
                if i > 0:
                    alpha = i / len(self.trail_points)
                    color = (int(255 * alpha), int(200 * alpha), 0)
                    trail_size = max(1, int(3 * alpha))
                    pygame.draw.circle(self.screen, color, point, trail_size)
            
            sat_size = max(3, min(8, int(display_radius / 50)))
            pygame.draw.circle(self.screen, self.RED, (int(sat_x), int(sat_y)), sat_size + 1)
            pygame.draw.circle(self.screen, self.YELLOW, (int(sat_x), int(sat_y)), sat_size)
            
            vector_length = min(30, display_radius / 10)
            vector_x = sat_x + vector_length * math.cos(self.satellite_angle + math.pi/2)
            vector_y = sat_y + vector_length * math.sin(self.satellite_angle + math.pi/2)
            pygame.draw.line(self.screen, self.WHITE, 
                           (sat_x, sat_y), (vector_x, vector_y), 2)
    
    def draw_info_panel(self):
        panel_x = self.WINDOW_WIDTH - 340
        panel_y = 10
        panel_width = 330
        panel_height = self.WINDOW_HEIGHT - 20
        
        panel_surface = pygame.Surface((panel_width, panel_height))
        panel_surface.set_alpha(200)
        panel_surface.fill(self.BLACK)
        self.screen.blit(panel_surface, (panel_x, panel_y))
        
        title = self.font.render("🛰️ SATELLITE SIMULATOR", True, self.WHITE)
        self.screen.blit(title, (panel_x + 10, panel_y + 10))
        
        info_texts = [
            f"Mass: {self.satellite_mass:,.0f} kg",
            f"Altitude: {self.altitude/1000:,.1f} km",
            f"Velocity: {self.orbital_velocity:,.0f} m/s",
            f"Period: {self.orbital_period/3600:.2f} hours",
            f"Force: {self.centripetal_force:,.0f} N",
            f"Type: {self.orbit_type}",
            "",
            "CONTROLS:",
            "↑/↓ - Adjust Altitude",
            "+/- - Adjust Mass", 
            "SPACE - Pause/Resume",
            "R - Reset Position",
            "ESC - Exit"
        ]
        
        for i, text in enumerate(info_texts):
            color = self.WHITE if i < 6 else self.GRAY
            if text == "CONTROLS:":
                color = self.YELLOW
            
            rendered = self.font.render(text, True, color)
            self.screen.blit(rendered, (panel_x + 15, panel_y + 50 + i * 25))
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP]:
            self.altitude += 1000
            self.altitude = min(self.altitude, 100000000)
            self.calculate_orbital_parameters()
        
        if keys[pygame.K_DOWN]:
            self.altitude -= 1000
            self.altitude = max(self.altitude, 150000)
            self.calculate_orbital_parameters()
        
        if keys[pygame.K_EQUALS] or keys[pygame.K_PLUS]:
            self.satellite_mass += 100
            self.satellite_mass = min(self.satellite_mass, 100000)
            self.calculate_orbital_parameters()
        
        if keys[pygame.K_MINUS]:
            self.satellite_mass -= 100
            self.satellite_mass = max(self.satellite_mass, 100)
            self.calculate_orbital_parameters()
    
    def run(self):
        self.calculate_orbital_parameters()
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_SPACE:
                        self.is_paused = not self.is_paused
                    elif event.key == pygame.K_r:
                        self.satellite_angle = 0
                        self.trail_points = []
            
            self.handle_input()
            
            sat_x, sat_y, display_radius = self.update_satellite_position()
            
            self.screen.fill(self.BLACK)
            
            self.draw_earth()
            self.draw_orbit_and_satellite(sat_x, sat_y, display_radius)
            self.draw_info_panel()
            
            status_text = "PAUSED" if self.is_paused else "RUNNING"
            status_color = self.RED if self.is_paused else self.GREEN
            status_surface = self.font.render(status_text, True, status_color)
            self.screen.blit(status_surface, (10, 10))
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()

def main():
    simulator = SatelliteOrbitSimulator()
    simulator.run()

if __name__ == "__main__":
    main()
