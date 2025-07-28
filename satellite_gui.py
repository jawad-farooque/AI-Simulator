"""
Enhanced AI Satellite Orbit Simulator with GUI
==============================================
A more advanced version with tkinter GUI for parameter input
and pygame for real-time visualization.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pygame
import numpy as np
import math
import threading
import time

class SatelliteGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI Satellite Orbit Simulator - Control Panel")
        self.root.geometry("400x600")
        self.root.configure(bg='#2c3e50')
        
        # Variables
        self.mass_var = tk.DoubleVar(value=1000)
        self.altitude_var = tk.DoubleVar(value=400)
        self.simulation_running = False
        
        # Physics results
        self.orbital_velocity = tk.StringVar(value="0")
        self.orbital_period = tk.StringVar(value="0")
        self.centripetal_force = tk.StringVar(value="0")
        self.orbit_type = tk.StringVar(value="")
        
        self.create_widgets()
        self.simulator = None
        
    def create_widgets(self):
        """Create the GUI widgets"""
        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50')
        title_frame.pack(pady=10)
        
        title_label = tk.Label(title_frame, text="🛰️ AI SATELLITE ORBIT SIMULATOR", 
                              font=('Arial', 16, 'bold'), fg='#ecf0f1', bg='#2c3e50')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Interactive Orbital Physics Simulation", 
                                 font=('Arial', 10), fg='#bdc3c7', bg='#2c3e50')
        subtitle_label.pack()
        
        # Input Frame
        input_frame = tk.LabelFrame(self.root, text="Satellite Parameters", 
                                   font=('Arial', 12, 'bold'), fg='#ecf0f1', bg='#34495e')
        input_frame.pack(padx=20, pady=10, fill='x')
        
        # Mass input
        tk.Label(input_frame, text="Satellite Mass (kg):", fg='#ecf0f1', bg='#34495e').grid(row=0, column=0, sticky='w', padx=10, pady=5)
        mass_scale = tk.Scale(input_frame, from_=100, to=50000, orient='horizontal', 
                             variable=self.mass_var, bg='#34495e', fg='#ecf0f1',
                             command=self.update_calculations)
        mass_scale.grid(row=0, column=1, padx=10, pady=5, sticky='ew')
        
        mass_entry = tk.Entry(input_frame, textvariable=self.mass_var, width=10)
        mass_entry.grid(row=0, column=2, padx=10, pady=5)
        mass_entry.bind('<KeyRelease>', self.update_calculations)
        
        # Altitude input
        tk.Label(input_frame, text="Altitude (km):", fg='#ecf0f1', bg='#34495e').grid(row=1, column=0, sticky='w', padx=10, pady=5)
        altitude_scale = tk.Scale(input_frame, from_=150, to=50000, orient='horizontal', 
                                 variable=self.altitude_var, bg='#34495e', fg='#ecf0f1',
                                 command=self.update_calculations)
        altitude_scale.grid(row=1, column=1, padx=10, pady=5, sticky='ew')
        
        altitude_entry = tk.Entry(input_frame, textvariable=self.altitude_var, width=10)
        altitude_entry.grid(row=1, column=2, padx=10, pady=5)
        altitude_entry.bind('<KeyRelease>', self.update_calculations)
        
        input_frame.columnconfigure(1, weight=1)
        
        # Results Frame
        results_frame = tk.LabelFrame(self.root, text="Calculated Results", 
                                     font=('Arial', 12, 'bold'), fg='#ecf0f1', bg='#34495e')
        results_frame.pack(padx=20, pady=10, fill='x')
        
        # Results display
        tk.Label(results_frame, text="Orbital Velocity:", fg='#ecf0f1', bg='#34495e').grid(row=0, column=0, sticky='w', padx=10, pady=5)
        tk.Label(results_frame, textvariable=self.orbital_velocity, fg='#3498db', bg='#34495e', font=('Arial', 10, 'bold')).grid(row=0, column=1, sticky='w', padx=10, pady=5)
        
        tk.Label(results_frame, text="Orbital Period:", fg='#ecf0f1', bg='#34495e').grid(row=1, column=0, sticky='w', padx=10, pady=5)
        tk.Label(results_frame, textvariable=self.orbital_period, fg='#3498db', bg='#34495e', font=('Arial', 10, 'bold')).grid(row=1, column=1, sticky='w', padx=10, pady=5)
        
        tk.Label(results_frame, text="Centripetal Force:", fg='#ecf0f1', bg='#34495e').grid(row=2, column=0, sticky='w', padx=10, pady=5)
        tk.Label(results_frame, textvariable=self.centripetal_force, fg='#3498db', bg='#34495e', font=('Arial', 10, 'bold')).grid(row=2, column=1, sticky='w', padx=10, pady=5)
        
        tk.Label(results_frame, text="Orbit Type:", fg='#ecf0f1', bg='#34495e').grid(row=3, column=0, sticky='w', padx=10, pady=5)
        tk.Label(results_frame, textvariable=self.orbit_type, fg='#e74c3c', bg='#34495e', font=('Arial', 10, 'bold')).grid(row=3, column=1, sticky='w', padx=10, pady=5)
        
        # Control buttons
        control_frame = tk.Frame(self.root, bg='#2c3e50')
        control_frame.pack(pady=20)
        
        self.start_button = tk.Button(control_frame, text="🚀 Start Simulation", 
                                     command=self.start_simulation, bg='#27ae60', fg='white',
                                     font=('Arial', 12, 'bold'), padx=20, pady=10)
        self.start_button.pack(side='left', padx=10)
        
        self.stop_button = tk.Button(control_frame, text="⏹ Stop Simulation", 
                                    command=self.stop_simulation, bg='#e74c3c', fg='white',
                                    font=('Arial', 12, 'bold'), padx=20, pady=10, state='disabled')
        self.stop_button.pack(side='left', padx=10)
        
        # AI Analysis Frame
        ai_frame = tk.LabelFrame(self.root, text="AI Analysis", 
                                font=('Arial', 12, 'bold'), fg='#ecf0f1', bg='#34495e')
        ai_frame.pack(padx=20, pady=10, fill='both', expand=True)
        
        self.ai_text = tk.Text(ai_frame, height=8, bg='#2c3e50', fg='#ecf0f1', 
                              font=('Arial', 10), wrap='word')
        self.ai_text.pack(padx=10, pady=10, fill='both', expand=True)
        
        # Initial calculations
        self.update_calculations()
        
    def update_calculations(self, *args):
        """Update orbital calculations"""
        try:
            mass = float(self.mass_var.get())
            altitude_km = float(self.altitude_var.get())
            altitude_m = altitude_km * 1000
            
            # Physics constants
            EARTH_RADIUS = 6371000  # meters
            EARTH_MASS = 5.972e24   # kg
            G = 6.67430e-11         # gravitational constant
            
            # Calculations
            orbital_radius = EARTH_RADIUS + altitude_m
            orbital_velocity = math.sqrt(G * EARTH_MASS / orbital_radius)
            orbital_period = 2 * math.pi * math.sqrt(orbital_radius**3 / (G * EARTH_MASS))
            centripetal_force = (mass * orbital_velocity**2) / orbital_radius
            
            # Update display
            self.orbital_velocity.set(f"{orbital_velocity:,.0f} m/s")
            self.orbital_period.set(f"{orbital_period/3600:.2f} hours")
            self.centripetal_force.set(f"{centripetal_force:,.0f} N")
            
            # Classify orbit
            orbit_type = self.classify_orbit(altitude_km)
            self.orbit_type.set(orbit_type)
            
            # AI Analysis
            self.update_ai_analysis(mass, altitude_km, orbital_velocity, orbital_period)
            
        except ValueError:
            pass
    
    def classify_orbit(self, altitude_km):
        """AI-based orbit classification"""
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
    
    def update_ai_analysis(self, mass, altitude_km, velocity, period):
        """Generate AI analysis"""
        self.ai_text.delete(1.0, tk.END)
        
        analysis = f"""🤖 AI ORBITAL ANALYSIS
{'='*40}

📊 MISSION PROFILE:
• Satellite Mass: {mass:,.0f} kg
• Orbital Altitude: {altitude_km:,.0f} km
• Velocity Required: {velocity:,.0f} m/s
• Orbital Period: {period/3600:.2f} hours

🎯 MISSION SUITABILITY:
"""
        
        if altitude_km < 200:
            analysis += "⚠️  CRITICAL: Atmospheric drag zone\n• High fuel consumption required\n• Limited mission duration\n• Frequent orbital corrections needed"
        elif altitude_km <= 600:
            analysis += "✅ EXCELLENT: Earth observation zone\n• Perfect for imaging missions\n• Good ground resolution\n• Moderate power requirements"
        elif altitude_km <= 1500:
            analysis += "🛰️  GOOD: Communication satellite range\n• Suitable for regional coverage\n• Balanced orbit/ground link\n• Stable orbital environment"
        elif altitude_km <= 20000:
            analysis += "🌐 OPTIMAL: Navigation constellation\n• GPS/GLONASS altitude range\n• Global coverage possible\n• Long orbital periods"
        elif abs(altitude_km - 35786) < 500:
            analysis += "🌍 PERFECT: Geostationary orbit!\n• 24-hour orbital period\n• Fixed position over Earth\n• Ideal for weather/communication"
        else:
            analysis += "🚀 EXTREME: Deep space trajectory\n• Very high energy requirements\n• Limited Earth communication\n• Specialized mission profile"
        
        analysis += f"\n\n⚡ ENERGY ANALYSIS:\n• Launch ΔV: ~{velocity/1000:.1f} km/s\n• Orbital Energy: High efficiency\n• Station-keeping: "
        
        if altitude_km < 400:
            analysis += "High maintenance"
        elif altitude_km < 2000:
            analysis += "Moderate maintenance"
        else:
            analysis += "Low maintenance"
            
        self.ai_text.insert(tk.END, analysis)
    
    def start_simulation(self):
        """Start the pygame simulation in a separate thread"""
        if not self.simulation_running:
            self.simulation_running = True
            self.start_button.config(state='disabled')
            self.stop_button.config(state='normal')
            
            # Start pygame simulation in separate thread
            self.simulation_thread = threading.Thread(target=self.run_pygame_simulation)
            self.simulation_thread.daemon = True
            self.simulation_thread.start()
    
    def stop_simulation(self):
        """Stop the simulation"""
        self.simulation_running = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
    
    def run_pygame_simulation(self):
        """Run the pygame visualization"""
        # Initialize pygame
        pygame.init()
        
        # Get screen dimensions and create adaptive window
        info = pygame.display.Info()
        screen_width = min(info.current_w - 100, 1200)  # Leave some margin
        screen_height = min(info.current_h - 100, 800)
        
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("AI Satellite Orbit Visualization")
        clock = pygame.time.Clock()
        
        # Colors
        BLACK = (0, 0, 0)
        BLUE = (100, 149, 237)
        WHITE = (255, 255, 255)
        RED = (220, 20, 60)
        YELLOW = (255, 215, 0)
        GREEN = (34, 139, 34)
        GRAY = (128, 128, 128)
        LIGHT_GRAY = (200, 200, 200)
        
        # Animation variables
        angle = 0
        trail_points = []
        earth_x, earth_y = screen_width // 2, screen_height // 2
        
        # Adaptive sizing based on screen
        min_earth_radius = 30
        max_earth_radius = min(screen_width, screen_height) // 8
        earth_radius = max(min_earth_radius, min(max_earth_radius, 60))
        
        font = pygame.font.Font(None, max(16, min(24, screen_width // 50)))
        
        while self.simulation_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.simulation_running = False
            
            # Calculate display parameters with adaptive scaling
            altitude_km = self.altitude_var.get()
            
            # Adaptive scaling algorithm
            # Calculate available space for orbit (leaving margin for Earth and info)
            available_radius = min(screen_width // 2 - earth_radius - 50, 
                                 screen_height // 2 - earth_radius - 50)
            
            # Scale altitude to fit within available space
            # Use logarithmic scaling for very high altitudes
            if altitude_km <= 1000:
                # Linear scaling for low altitudes
                scale_factor = available_radius / 1000
                display_radius = earth_radius + (altitude_km * scale_factor)
            else:
                # Logarithmic scaling for high altitudes
                log_altitude = math.log10(altitude_km)
                max_log = math.log10(50000)  # Maximum altitude from slider
                normalized_log = log_altitude / max_log
                display_radius = earth_radius + (available_radius * normalized_log)
            
            # Ensure minimum and maximum display radius
            display_radius = max(earth_radius + 20, min(display_radius, available_radius + earth_radius))
            
            # Calculate realistic orbital speed based on altitude
            # Higher altitudes = slower orbital speed
            EARTH_RADIUS = 6371  # km
            orbital_radius_km = EARTH_RADIUS + altitude_km
            
            # Real orbital period calculation for animation speed
            G = 6.67430e-11  # m³/kg⋅s²
            EARTH_MASS = 5.972e24  # kg
            orbital_period_seconds = 2 * math.pi * math.sqrt((orbital_radius_km * 1000)**3 / (G * EARTH_MASS))
            
            # Convert to animation speed (faster for visualization)
            base_speed = 0.02  # Base animation speed
            speed_multiplier = math.sqrt(EARTH_RADIUS / orbital_radius_km)  # Real physics scaling
            animation_speed = base_speed * speed_multiplier * 10  # Speed up for visibility
            
            # Update satellite position
            angle += animation_speed
            if angle >= 2 * math.pi:
                angle -= 2 * math.pi
                
            sat_x = earth_x + display_radius * math.cos(angle)
            sat_y = earth_y + display_radius * math.sin(angle)
            
            # Add to trail with adaptive trail length based on orbit size
            trail_length = max(50, min(200, int(display_radius * 2)))
            trail_points.append((int(sat_x), int(sat_y)))
            if len(trail_points) > trail_length:
                trail_points.pop(0)
            
            # Clear screen
            screen.fill(BLACK)
            
            # Draw orbit path
            pygame.draw.circle(screen, GRAY, (earth_x, earth_y), int(display_radius), 2)
            
            # Draw Earth with adaptive details
            pygame.draw.circle(screen, BLUE, (earth_x, earth_y), earth_radius)
            
            # Draw continents (scale with Earth size)
            continent_scale = earth_radius / 60
            pygame.draw.circle(screen, GREEN, 
                             (int(earth_x - 15 * continent_scale), int(earth_y - 10 * continent_scale)), 
                             max(3, int(8 * continent_scale)))
            pygame.draw.circle(screen, GREEN, 
                             (int(earth_x + 20 * continent_scale), int(earth_y + 15 * continent_scale)), 
                             max(2, int(6 * continent_scale)))
            pygame.draw.circle(screen, GREEN, 
                             (int(earth_x - 10 * continent_scale), int(earth_y + 25 * continent_scale)), 
                             max(2, int(5 * continent_scale)))
            
            # Draw Earth outline
            pygame.draw.circle(screen, WHITE, (earth_x, earth_y), earth_radius, 2)
            
            # Draw satellite trail with fade effect
            for i, point in enumerate(trail_points):
                if i > 0:  # Skip first point to avoid errors
                    alpha = i / len(trail_points)
                    color = (int(255 * alpha), int(200 * alpha), 0)
                    trail_size = max(1, int(3 * alpha))
                    pygame.draw.circle(screen, color, point, trail_size)
            
            # Draw satellite with adaptive size
            sat_size = max(3, min(8, int(earth_radius / 10)))
            pygame.draw.circle(screen, RED, (int(sat_x), int(sat_y)), sat_size + 2)
            pygame.draw.circle(screen, YELLOW, (int(sat_x), int(sat_y)), sat_size)
            
            # Draw velocity vector
            vector_length = min(30, display_radius / 5)
            vector_x = sat_x + vector_length * math.cos(angle + math.pi/2)
            vector_y = sat_y + vector_length * math.sin(angle + math.pi/2)
            pygame.draw.line(screen, WHITE, (sat_x, sat_y), (vector_x, vector_y), 2)
            
            # Draw adaptive info panel
            info_panel_width = min(300, screen_width // 3)
            info_texts = [
                f"Altitude: {altitude_km:,.0f} km",
                f"Velocity: {self.orbital_velocity.get()}",
                f"Period: {self.orbital_period.get()}",
                f"Type: {self.orbit_type.get()}",
                f"Display Scale: {display_radius/earth_radius:.1f}x"
            ]
            
            # Draw semi-transparent background for info
            info_bg = pygame.Surface((info_panel_width, len(info_texts) * 30 + 20))
            info_bg.set_alpha(180)
            info_bg.fill((0, 0, 0))
            screen.blit(info_bg, (10, 10))
            
            # Draw info text
            for i, text in enumerate(info_texts):
                color = WHITE if i < 4 else LIGHT_GRAY
                rendered = font.render(text, True, color)
                screen.blit(rendered, (20, 20 + i * 25))
            
            # Draw scale reference
            scale_text = f"Earth Radius: {earth_radius}px | Orbit: {display_radius:.0f}px"
            scale_rendered = font.render(scale_text, True, GRAY)
            screen.blit(scale_rendered, (20, screen_height - 30))
            
            # Draw instructions
            instruction_text = "Close window to stop simulation"
            inst_rendered = font.render(instruction_text, True, LIGHT_GRAY)
            screen.blit(inst_rendered, (screen_width - 250, screen_height - 30))
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
    
    def run(self):
        """Run the GUI application"""
        self.root.mainloop()

def main():
    """Main function"""
    app = SatelliteGUI()
    app.run()

if __name__ == "__main__":
    main()
