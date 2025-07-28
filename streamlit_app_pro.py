"""
🛰️ Enhanced AI Satellite Orbit Simulator - Professional Streamlit App
====================================================================
Advanced web application with animations, interactive features, and professional UI
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import math
import pandas as pd
from datetime import datetime
import time
import json

# Page configuration
st.set_page_config(
    page_title="🛰️ AI Satellite Orbit Simulator Pro",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main-title {
        font-family: 'Orbitron', monospace;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 4rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .subtitle {
        font-family: 'Inter', sans-serif;
        text-align: center;
        font-size: 1.5rem;
        color: #666;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
        background-size: 50px 50px;
        animation: float 20s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    
    .metric-container {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border: 1px solid #f0f0f0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
    }
    
    .metric-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }
    
    .orbit-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .orbit-leo { background: linear-gradient(45deg, #4CAF50, #8BC34A); color: white; }
    .orbit-meo { background: linear-gradient(45deg, #FF9800, #FFC107); color: white; }
    .orbit-geo { background: linear-gradient(45deg, #2196F3, #03DAC6); color: white; }
    .orbit-heo { background: linear-gradient(45deg, #9C27B0, #E91E63); color: white; }
    
    .ai-panel {
        background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%);
        border-radius: 15px;
        padding: 2rem;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 20px rgba(255, 107, 107, 0.3);
    }
    
    .physics-panel {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        border-radius: 15px;
        padding: 2rem;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 20px rgba(116, 185, 255, 0.3);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        border: none;
        border-radius: 25px;
        color: white;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    .mission-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .mission-card:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 18px rgba(0,0,0,0.15);
    }
    
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .danger { background-color: #ff4757; }
    .warning { background-color: #ffa502; }
    .success { background-color: #2ed573; }
    .info { background-color: #3742fa; }
</style>
""", unsafe_allow_html=True)

class AdvancedSatelliteCalculator:
    """Advanced satellite orbit calculation with enhanced features"""
    
    def __init__(self):
        self.EARTH_RADIUS = 6371  # km
        self.EARTH_MASS = 5.972e24  # kg
        self.G = 6.67430e-11  # m³/kg⋅s²
        
        # Real satellite data for comparison
        self.reference_satellites = {
            "ISS": {"altitude": 408, "mass": 420000, "purpose": "Space Station"},
            "Hubble": {"altitude": 547, "mass": 11110, "purpose": "Space Telescope"},
            "GPS": {"altitude": 20200, "mass": 2000, "purpose": "Navigation"},
            "Geostationary": {"altitude": 35786, "mass": 5000, "purpose": "Communication"},
            "Starlink": {"altitude": 550, "mass": 260, "purpose": "Internet Constellation"}
        }
    
    def calculate_comprehensive_parameters(self, mass_kg, altitude_km):
        """Calculate comprehensive orbital parameters"""
        altitude_m = altitude_km * 1000
        orbital_radius_m = (self.EARTH_RADIUS * 1000) + altitude_m
        
        # Basic calculations
        orbital_velocity = math.sqrt(self.G * self.EARTH_MASS / orbital_radius_m)
        orbital_period = 2 * math.pi * math.sqrt(orbital_radius_m**3 / (self.G * self.EARTH_MASS))
        centripetal_force = (mass_kg * orbital_velocity**2) / orbital_radius_m
        
        # Advanced calculations
        orbital_energy = -self.G * self.EARTH_MASS * mass_kg / (2 * orbital_radius_m)
        angular_velocity = orbital_velocity / orbital_radius_m
        escape_velocity = math.sqrt(2 * self.G * self.EARTH_MASS / orbital_radius_m)
        
        # Launch requirements
        surface_velocity = 465  # m/s (Earth's rotation at equator)
        delta_v_required = orbital_velocity - surface_velocity
        
        # Gravitational acceleration at altitude
        g_at_altitude = self.G * self.EARTH_MASS / (orbital_radius_m**2)
        
        return {
            'velocity_ms': orbital_velocity,
            'velocity_kms': orbital_velocity / 1000,
            'period_seconds': orbital_period,
            'period_minutes': orbital_period / 60,
            'period_hours': orbital_period / 3600,
            'period_days': orbital_period / (3600 * 24),
            'centripetal_force': centripetal_force,
            'orbital_energy': orbital_energy,
            'angular_velocity': angular_velocity,
            'orbital_radius_km': orbital_radius_m / 1000,
            'escape_velocity': escape_velocity / 1000,  # km/s
            'delta_v_required': delta_v_required / 1000,  # km/s
            'g_at_altitude': g_at_altitude,
            'altitude_km': altitude_km,
            'mass_kg': mass_kg
        }
    
    def get_orbit_classification(self, altitude_km):
        """Enhanced orbit classification with detailed analysis"""
        if altitude_km < 160:
            return {
                'type': 'VERY LOW',
                'full_name': 'Very Low Earth Orbit',
                'color': '#ff4757',
                'status': 'danger',
                'description': 'Extreme atmospheric drag - Mission not viable',
                'applications': ['Atmospheric research (brief)', 'Deorbiting missions'],
                'challenges': ['Severe atmospheric drag', 'Rapid orbital decay', 'High maintenance'],
                'advantages': ['High resolution imagery', 'Low latency'],
                'examples': ['Deorbiting spacecraft', 'Some research missions'],
                'css_class': 'orbit-leo'
            }
        elif altitude_km <= 2000:
            return {
                'type': 'LEO',
                'full_name': 'Low Earth Orbit',
                'color': '#2ed573',
                'status': 'success',
                'description': 'Optimal for Earth observation and human spaceflight',
                'applications': ['Earth observation', 'Human spaceflight', 'Small satellites'],
                'challenges': ['Atmospheric drag', 'Limited coverage time', 'Frequent handovers'],
                'advantages': ['High resolution', 'Low launch cost', 'Easy maintenance'],
                'examples': ['ISS', 'Starlink', 'Planet Labs', 'Most CubeSats'],
                'css_class': 'orbit-leo'
            }
        elif altitude_km <= 35786:
            return {
                'type': 'MEO',
                'full_name': 'Medium Earth Orbit',
                'color': '#ffa502',
                'status': 'warning',
                'description': 'Perfect for navigation and regional communication',
                'applications': ['Navigation (GPS)', 'Regional communication', 'Scientific missions'],
                'challenges': ['Radiation environment', 'Higher launch costs', 'Complex orbital mechanics'],
                'advantages': ['Global coverage', 'Good compromise altitude', 'Stable orbits'],
                'examples': ['GPS constellation', 'GLONASS', 'Galileo', 'O3b satellites'],
                'css_class': 'orbit-meo'
            }
        elif abs(altitude_km - 35786) < 100:
            return {
                'type': 'GEO',
                'full_name': 'Geostationary Earth Orbit',
                'color': '#3742fa',
                'status': 'info',
                'description': 'Fixed position relative to Earth - Perfect for communications',
                'applications': ['Communications', 'Weather monitoring', 'Broadcasting'],
                'challenges': ['High launch costs', 'Launch window constraints', 'Orbital slot competition'],
                'advantages': ['Fixed coverage area', 'No tracking required', 'Continuous service'],
                'examples': ['Weather satellites', 'TV broadcast', 'Military communications'],
                'css_class': 'orbit-geo'
            }
        else:
            return {
                'type': 'HEO',
                'full_name': 'High Earth Orbit',
                'color': '#8c7ae6',
                'status': 'info',
                'description': 'Deep space missions and specialized applications',
                'applications': ['Deep space missions', 'Lagrange point missions', 'Interplanetary'],
                'challenges': ['Extreme launch requirements', 'Long communication delays', 'Harsh environment'],
                'advantages': ['Unique vantage points', 'Minimal gravitational influence', 'Scientific value'],
                'examples': ['James Webb Space Telescope', 'Solar observatories', 'Interplanetary probes'],
                'css_class': 'orbit-heo'
            }
    
    def generate_mission_analysis(self, orbit_params, orbit_class):
        """Generate detailed mission analysis"""
        altitude = orbit_params['altitude_km']
        mass = orbit_params['mass_kg']
        velocity = orbit_params['velocity_kms']
        period = orbit_params['period_hours']
        
        # Risk assessment
        risk_factors = []
        if altitude < 200:
            risk_factors.append("⚠️ High atmospheric drag")
        if altitude > 30000:
            risk_factors.append("⚠️ High radiation environment")
        if mass > 10000:
            risk_factors.append("⚠️ Heavy payload - high launch cost")
        
        # Mission recommendations
        recommendations = []
        if 400 <= altitude <= 600:
            recommendations.append("✅ Excellent for Earth observation")
        if 500 <= altitude <= 1200:
            recommendations.append("✅ Good for satellite constellations")
        if abs(altitude - 35786) < 500:
            recommendations.append("✅ Perfect for geostationary applications")
        
        return {
            'risk_factors': risk_factors,
            'recommendations': recommendations,
            'launch_cost_estimate': self.estimate_launch_cost(mass, altitude),
            'mission_duration_estimate': self.estimate_mission_duration(altitude),
            'ground_coverage': self.calculate_ground_coverage(altitude)
        }
    
    def estimate_launch_cost(self, mass_kg, altitude_km):
        """Estimate launch cost based on mass and altitude"""
        base_cost_per_kg = 5000  # USD per kg to LEO
        altitude_multiplier = 1 + (altitude_km / 10000)  # Higher altitude = higher cost
        total_cost = mass_kg * base_cost_per_kg * altitude_multiplier
        return total_cost
    
    def estimate_mission_duration(self, altitude_km):
        """Estimate mission duration based on orbital decay"""
        if altitude_km < 300:
            return "Weeks to months"
        elif altitude_km < 600:
            return "5-15 years"
        elif altitude_km < 2000:
            return "Decades"
        else:
            return "Centuries+"
    
    def calculate_ground_coverage(self, altitude_km):
        """Calculate ground coverage area"""
        earth_radius = 6371  # km
        horizon_distance = math.sqrt(2 * earth_radius * altitude_km + altitude_km**2)
        coverage_area = math.pi * horizon_distance**2
        return coverage_area

def create_animated_3d_orbit(altitude_km, orbit_class, animation_speed=1.0):
    """Create animated 3D orbit visualization"""
    earth_radius = 6371
    orbital_radius = earth_radius + altitude_km
    
    # Create Earth
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(0, np.pi, 30)
    x_earth = earth_radius * np.outer(np.cos(u), np.sin(v))
    y_earth = earth_radius * np.outer(np.sin(u), np.sin(v))
    z_earth = earth_radius * np.outer(np.ones(np.size(u)), np.cos(v))
    
    # Create orbit path
    theta = np.linspace(0, 2 * np.pi, 100)
    x_orbit = orbital_radius * np.cos(theta)
    y_orbit = orbital_radius * np.sin(theta)
    z_orbit = np.zeros_like(theta)
    
    # Animated satellite position - continuous rotation when active
    import streamlit as st
    
    if st.session_state.get('animation_active', False):
        # Calculate elapsed time since animation started
        start_time = st.session_state.get('start_time', time.time())
        elapsed_time = time.time() - start_time
        
        # Scale the animation - complete one orbit in 20 seconds, adjusted by speed
        base_period = 20.0 / animation_speed  # seconds for one complete orbit
        rotation_speed = (2 * np.pi) / base_period
        
        sat_angle = (elapsed_time * rotation_speed) % (2 * np.pi)
    else:
        # Static position when not animating
        sat_angle = 0
    
    sat_x = orbital_radius * np.cos(sat_angle)
    sat_y = orbital_radius * np.sin(sat_angle)
    sat_z = 0
    
    # Create satellite trail - only show when animating
    trail_length = 15
    trail_angles = [sat_angle - i * 0.2 for i in range(trail_length)]
    trail_x = [orbital_radius * np.cos(angle) for angle in trail_angles]
    trail_y = [orbital_radius * np.sin(angle) for angle in trail_angles]
    trail_z = [0] * trail_length
    
    fig = go.Figure()
    
    # Earth with texture-like appearance
    fig.add_trace(go.Surface(
        x=x_earth, y=y_earth, z=z_earth,
        colorscale='Earth',
        showscale=False,
        name='Earth',
        opacity=0.9,
        hovertemplate='🌍 Earth<extra></extra>'
    ))
    
    # Orbital path
    fig.add_trace(go.Scatter3d(
        x=x_orbit, y=y_orbit, z=z_orbit,
        mode='lines',
        line=dict(color=orbit_class['color'], width=6, dash='dot'),
        name=f'{orbit_class["type"]} Orbit Path',
        hovertemplate=f'Orbital Path<br>Altitude: {altitude_km:,} km<extra></extra>'
    ))
    
    # Satellite trail - only show if animation is active
    if st.session_state.get('animation_active', False):
        fig.add_trace(go.Scatter3d(
            x=trail_x, y=trail_y, z=trail_z,
            mode='lines+markers',
            line=dict(color='orange', width=4),
            marker=dict(size=3, color='orange', opacity=0.7),
            name='Satellite Trail',
            hovertemplate='Satellite Trail<extra></extra>'
        ))
    
    # Active satellite
    satellite_color = 'red' if st.session_state.get('animation_active', False) else 'blue'
    satellite_size = 25 if st.session_state.get('animation_active', False) else 20
    
    fig.add_trace(go.Scatter3d(
        x=[sat_x], y=[sat_y], z=[sat_z],
        mode='markers',
        marker=dict(
            size=satellite_size,
            color=satellite_color,
            symbol='diamond',
            line=dict(width=2, color='yellow')
        ),
        name='🛰️ Satellite',
        hovertemplate=f'{"🚀 Orbiting" if st.session_state.get("animation_active", False) else "🛰️ Static"} Satellite<br>Position: ({sat_x:.0f}, {sat_y:.0f}, {sat_z:.0f})<br>Altitude: {altitude_km:,} km<br>Angle: {sat_angle:.2f} rad<extra></extra>'
    ))
    
    # Update layout with professional styling
    fig.update_layout(
        title=dict(
            text=f"🛰️ {orbit_class['full_name']} Visualization",
            x=0.5,
            font=dict(size=24, family="Orbitron, monospace")
        ),
        scene=dict(
            xaxis_title="X (km)",
            yaxis_title="Y (km)", 
            zaxis_title="Z (km)",
            bgcolor='rgba(0,0,0,0.9)',
            xaxis=dict(
                backgroundcolor='rgba(0,0,0,0)',
                gridcolor='rgba(255,255,255,0.2)',
                showbackground=True,
                zerolinecolor='rgba(255,255,255,0.4)'
            ),
            yaxis=dict(
                backgroundcolor='rgba(0,0,0,0)',
                gridcolor='rgba(255,255,255,0.2)',
                showbackground=True,
                zerolinecolor='rgba(255,255,255,0.4)'
            ),
            zaxis=dict(
                backgroundcolor='rgba(0,0,0,0)',
                gridcolor='rgba(255,255,255,0.2)',
                showbackground=True,
                zerolinecolor='rgba(255,255,255,0.4)'
            ),
            aspectmode='cube',
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        ),
        paper_bgcolor='rgba(0,0,0,0.9)',
        plot_bgcolor='rgba(0,0,0,0.9)',
        font=dict(color='white', family="Inter, sans-serif"),
        height=700,
        margin=dict(l=0, r=0, t=60, b=0)
    )
    
    return fig

def create_orbital_parameters_chart(orbit_params):
    """Create comprehensive orbital parameters visualization"""
    
    # Create subplots
    fig = go.Figure()
    
    # Parameters for radar chart
    parameters = ['Velocity (km/s)', 'Period (hours)', 'Altitude (1000 km)', 
                 'Force (1000 N)', 'Energy (MJ/kg)']
    
    values = [
        orbit_params['velocity_kms'],
        orbit_params['period_hours'],
        orbit_params['altitude_km'] / 1000,
        orbit_params['centripetal_force'] / 1000,
        abs(orbit_params['orbital_energy'] / orbit_params['mass_kg']) / 1e6
    ]
    
    # Normalize values for radar chart
    max_values = [15, 24, 50, 100, 50]  # Reasonable max values for scaling
    normalized_values = [min(v/m, 1) * 100 for v, m in zip(values, max_values)]
    
    fig.add_trace(go.Scatterpolar(
        r=normalized_values,
        theta=parameters,
        fill='toself',
        name='Orbital Parameters',
        line=dict(color='#667eea', width=3),
        fillcolor='rgba(102, 126, 234, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='rgba(255,255,255,0.3)',
                tickcolor='white'
            ),
            angularaxis=dict(
                gridcolor='rgba(255,255,255,0.3)',
                tickcolor='white'
            )
        ),
        title="📊 Orbital Parameters Overview",
        font=dict(color='white'),
        paper_bgcolor='rgba(0,0,0,0.9)',
        plot_bgcolor='rgba(0,0,0,0.9)',
        height=400
    )
    
    return fig

def main():
    """Enhanced main application"""
    
    # Initialize session state for animation
    if 'animation_active' not in st.session_state:
        st.session_state.animation_active = False
    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()
    if 'animation_counter' not in st.session_state:
        st.session_state.animation_counter = 0
    if 'altitude' not in st.session_state:
        st.session_state.altitude = 400
    if 'mass' not in st.session_state:
        st.session_state.mass = 1000
    
    # Hero section
    st.markdown("""
    <div class="hero-section">
        <h1 class="main-title">🛰️ AI SATELLITE ORBIT SIMULATOR</h1>
        <p class="subtitle">Professional Orbital Mechanics Analysis Platform</p>
        <p style="font-size: 1.1rem; margin-top: 1rem;">Real-time Physics • AI-Powered Analysis • Interactive 3D Visualization</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize calculator
    calc = AdvancedSatelliteCalculator()
    
    # Enhanced sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: linear-gradient(45deg, #667eea, #764ba2); border-radius: 15px; margin-bottom: 2rem;">
            <h2 style="color: white; margin: 0;">🎛️ Mission Control</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Mission presets
        st.markdown("### 🚀 Quick Mission Presets")
        
        preset_col1, preset_col2 = st.columns(2)
        
        if preset_col1.button("🏠 ISS", key="iss"):
            st.session_state.altitude = 408
            st.session_state.mass = 420000
        
        if preset_col2.button("🔭 Hubble", key="hubble"):
            st.session_state.altitude = 547
            st.session_state.mass = 11110
        
        if preset_col1.button("📡 GPS", key="gps"):
            st.session_state.altitude = 20200
            st.session_state.mass = 2000
        
        if preset_col2.button("🌍 GEO", key="geo"):
            st.session_state.altitude = 35786
            st.session_state.mass = 5000
        
        st.markdown("---")
        
        # Parameters
        st.markdown("### 🛰️ Satellite Configuration")
        
        mass_kg = st.slider(
            "Satellite Mass (kg)",
            min_value=1,
            max_value=500000,
            value=st.session_state.get('mass', 1000),
            step=100,
            format="%d",
            help="Total mass of the satellite including fuel and instruments"
        )
        
        altitude_km = st.slider(
            "Orbital Altitude (km)",
            min_value=150,
            max_value=50000,
            value=st.session_state.get('altitude', 400),
            step=10,
            format="%d",
            help="Height above Earth's surface"
        )
        
        # Advanced options
        with st.expander("⚙️ Advanced Options"):
            show_comparison = st.checkbox("Show satellite comparison", True)
            show_physics_details = st.checkbox("Show detailed physics", True)
            animation_speed = st.slider("Animation Speed", 0.5, 3.0, 1.0, 0.1, help="Adjust how fast the satellite moves")
            
        st.markdown("---")
    
    # Calculate parameters
    orbit_params = calc.calculate_comprehensive_parameters(mass_kg, altitude_km)
    orbit_class = calc.get_orbit_classification(altitude_km)
    mission_analysis = calc.generate_mission_analysis(orbit_params, orbit_class)
    
    # Auto-refresh for animation - simplified approach
    if st.session_state.get('animation_active', False):
        st.sidebar.success("🎬 Animation: RUNNING")
        st.sidebar.info("🔄 Satellite is orbiting continuously")
    else:
        st.sidebar.info("🎬 Animation: STOPPED")
        st.sidebar.warning("Click 'Start Animation' to begin")
    
    # Main content
    col1, col2 = st.columns([2.5, 1.5])
    
    with col1:
        # 3D Visualization
        st.markdown("## 🌍 Real-Time Orbital Visualization")
        
        # Animation controls in the main area
        anim_col1, anim_col2 = st.columns([1, 1])
        
        with anim_col1:
            if st.button("🚀 Start Animation", key="start_main", help="Start continuous satellite movement"):
                st.session_state.animation_active = True
                st.session_state.start_time = time.time()
                
        with anim_col2:
            if st.button("⏸️ Stop Animation", key="pause_main", help="Stop animation"):
                st.session_state.animation_active = False
                
        # Status display
        if st.session_state.get('animation_active', False):
            st.success("🎬 Satellite is orbiting continuously! Animation is running...")
            
            # Add auto-refresh for continuous animation
            st.markdown("""
            <script>
            setTimeout(function(){
                window.location.reload();
            }, 1000);
            </script>
            """, unsafe_allow_html=True)
            
        else:
            st.info("🛰️ Click 'Start Animation' to begin continuous orbital movement")
        
        # Create the orbital visualization
        orbit_fig = create_animated_3d_orbit(altitude_km, orbit_class, animation_speed)
        st.plotly_chart(orbit_fig, use_container_width=True, key="main_viz")
        
        # Orbital parameters radar chart
        if show_physics_details:
            st.markdown("## 📊 Orbital Parameters Analysis")
            params_fig = create_orbital_parameters_chart(orbit_params)
            st.plotly_chart(params_fig, use_container_width=True)
    
    with col2:
        # Status indicator
        status_color = {'danger': 'danger', 'warning': 'warning', 'success': 'success', 'info': 'info'}[orbit_class['status']]
        
        st.markdown(f"""
        <div class="{orbit_class['css_class']}" style="text-align: center; padding: 2rem; border-radius: 15px; margin-bottom: 2rem;">
            <div class="status-indicator {status_color}"></div>
            <h2 style="margin: 0.5rem 0; color: {orbit_class['color']};">{orbit_class['type']}</h2>
            <h4 style="margin: 0; opacity: 0.9;">{orbit_class['full_name']}</h4>
            <p style="margin: 1rem 0;">{orbit_class['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Key metrics with enhanced styling
        st.markdown("## 📊 Mission Parameters")
        
        # Primary metrics
        metric_col1, metric_col2 = st.columns(2)
        
        with metric_col1:
            st.metric(
                "🚀 Orbital Velocity",
                f"{orbit_params['velocity_kms']:.2f} km/s",
                f"{orbit_params['velocity_ms']:,.0f} m/s"
            )
            
            st.metric(
                "💪 Centripetal Force", 
                f"{orbit_params['centripetal_force']/1000:.1f} kN",
                f"{orbit_params['centripetal_force']:,.0f} N"
            )
        
        with metric_col2:
            st.metric(
                "⏰ Orbital Period",
                f"{orbit_params['period_hours']:.2f} h",
                f"{orbit_params['period_minutes']:.1f} min"
            )
            
            st.metric(
                "🌐 Orbital Radius",
                f"{orbit_params['orbital_radius_km']:,.0f} km",
                f"{altitude_km:,} km altitude"
            )
        
        # Additional metrics
        with st.expander("📈 Advanced Metrics"):
            st.metric("🚀 Escape Velocity", f"{orbit_params['escape_velocity']:.2f} km/s")
            st.metric("⚡ Launch ΔV Required", f"{orbit_params['delta_v_required']:.2f} km/s")
            st.metric("🌍 Surface Gravity", f"{orbit_params['g_at_altitude']:.2f} m/s²")
            st.metric("🎯 Ground Coverage", f"{mission_analysis['ground_coverage']:,.0f} km²")
        
        # Mission analysis
        st.markdown("## 🎯 Mission Analysis")
        
        # Risk assessment
        if mission_analysis['risk_factors']:
            st.markdown("**⚠️ Risk Factors:**")
            for risk in mission_analysis['risk_factors']:
                st.markdown(f"- {risk}")
        
        # Recommendations
        if mission_analysis['recommendations']:
            st.markdown("**✅ Recommendations:**")
            for rec in mission_analysis['recommendations']:
                st.markdown(f"- {rec}")
        
        # Cost and duration estimates
        st.markdown("**💰 Mission Estimates:**")
        st.info(f"Launch Cost: ${mission_analysis['launch_cost_estimate']:,.0f}")
        st.info(f"Mission Duration: {mission_analysis['mission_duration_estimate']}")
    
    # AI Analysis Section
    st.markdown("""
    <div class="ai-panel">
        <h2>🤖 AI-Powered Mission Intelligence</h2>
    </div>
    """, unsafe_allow_html=True)
    
    ai_col1, ai_col2, ai_col3 = st.columns(3)
    
    with ai_col1:
        st.markdown("### 🎯 Applications")
        for app in orbit_class['applications']:
            st.markdown(f"• {app}")
    
    with ai_col2:
        st.markdown("### ⚠️ Challenges")
        for challenge in orbit_class['challenges']:
            st.markdown(f"• {challenge}")
    
    with ai_col3:
        st.markdown("### ✅ Advantages")
        for advantage in orbit_class['advantages']:
            st.markdown(f"• {advantage}")
    
    # Real satellite comparison
    if show_comparison:
        st.markdown("## 🛰️ Real Satellite Comparison")
        
        comparison_data = []
        for name, data in calc.reference_satellites.items():
            comparison_data.append({
                'Satellite': name,
                'Altitude (km)': data['altitude'],
                'Mass (kg)': data['mass'],
                'Purpose': data['purpose'],
                'Your Mission': '✅' if abs(data['altitude'] - altitude_km) < 100 else '❌'
            })
        
        df = pd.DataFrame(comparison_data)
        st.dataframe(df, use_container_width=True)
    
    # Physics formulas section
    st.markdown("""
    <div class="physics-panel">
        <h2>🧮 Orbital Mechanics Equations</h2>
    </div>
    """, unsafe_allow_html=True)
    
    formula_col1, formula_col2, formula_col3 = st.columns(3)
    
    with formula_col1:
        st.markdown("""
        **Orbital Velocity**
        ```
        v = √(GM/r)
        ```
        **Current Value:**  
        `{:.2f} km/s`
        """.format(orbit_params['velocity_kms']))
    
    with formula_col2:
        st.markdown("""
        **Orbital Period**
        ```
        T = 2π√(r³/GM)
        ```
        **Current Value:**  
        `{:.2f} hours`
        """.format(orbit_params['period_hours']))
    
    with formula_col3:
        st.markdown("""
        **Centripetal Force**
        ```
        F = mv²/r
        ```
        **Current Value:**  
        `{:.0f} N`
        """.format(orbit_params['centripetal_force']))
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; color: white; margin: 2rem 0;">
        <h2 style="margin-bottom: 1rem;">🌟 Impact Revolution Space Technologies</h2>
        <p style="font-size: 1.2rem; margin-bottom: 1rem;">Inspiring the Next Generation of Space Scientists</p>
        <p style="opacity: 0.9;">Advanced Orbital Mechanics • AI-Powered Analysis • Real-time Visualization</p>
        <p style="margin-top: 2rem; font-size: 0.9rem; opacity: 0.8;">
            © 2025 Impact Revolution | Professional Space Simulation Platform
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
