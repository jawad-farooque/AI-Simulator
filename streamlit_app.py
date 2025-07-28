"""
🛰️ AI Satellite Orbit Simulator - Streamlit Web Application
===========================================================
Professional web interface for the AI Satellite Orbit Simulator
with interactive visualizations and real-time physics calculations.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import math
import pandas as pd
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="🛰️ AI Satellite Orbit Simulator",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        color: #f0f0f0;
        font-size: 1.2rem;
        margin: 0;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    
    .ai-analysis {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    .physics-section {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    .orbit-type-leo {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1rem;
        border-radius: 8px;
        color: #333;
    }
    
    .orbit-type-meo {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1rem;
        border-radius: 8px;
        color: #333;
    }
    
    .orbit-type-geo {
        background: linear-gradient(135deg, #a8e6cf 0%, #dcedc8 100%);
        padding: 1rem;
        border-radius: 8px;
        color: #333;
    }
    
    .orbit-type-heo {
        background: linear-gradient(135deg, #ffd3a5 0%, #fd9853 100%);
        padding: 1rem;
        border-radius: 8px;
        color: #333;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .stSelectbox label, .stSlider label, .stNumberInput label {
        font-weight: 600;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

class SatelliteOrbitCalculator:
    """Professional satellite orbit calculation engine"""
    
    def __init__(self):
        # Physics constants
        self.EARTH_RADIUS = 6371  # km
        self.EARTH_MASS = 5.972e24  # kg
        self.G = 6.67430e-11  # m³/kg⋅s²
        
    def calculate_orbital_parameters(self, mass_kg, altitude_km):
        """Calculate all orbital parameters"""
        # Convert to meters for calculations
        altitude_m = altitude_km * 1000
        orbital_radius_m = (self.EARTH_RADIUS * 1000) + altitude_m
        
        # Orbital velocity (m/s)
        orbital_velocity = math.sqrt(self.G * self.EARTH_MASS / orbital_radius_m)
        
        # Orbital period (seconds)
        orbital_period = 2 * math.pi * math.sqrt(orbital_radius_m**3 / (self.G * self.EARTH_MASS))
        
        # Centripetal force (N)
        centripetal_force = (mass_kg * orbital_velocity**2) / orbital_radius_m
        
        # Orbital energy (J)
        orbital_energy = -self.G * self.EARTH_MASS * mass_kg / (2 * orbital_radius_m)
        
        # Angular velocity (rad/s)
        angular_velocity = orbital_velocity / orbital_radius_m
        
        return {
            'velocity_ms': orbital_velocity,
            'velocity_kms': orbital_velocity / 1000,
            'period_seconds': orbital_period,
            'period_minutes': orbital_period / 60,
            'period_hours': orbital_period / 3600,
            'centripetal_force': centripetal_force,
            'orbital_energy': orbital_energy,
            'angular_velocity': angular_velocity,
            'orbital_radius_km': orbital_radius_m / 1000
        }
    
    def classify_orbit_ai(self, altitude_km):
        """AI-powered orbit classification"""
        if altitude_km < 160:
            return {
                'type': 'VERY LOW ORBIT',
                'category': 'Unstable',
                'color': '#ff4444',
                'description': 'Severe atmospheric drag - Mission not viable',
                'suitability': 'Critical Risk Zone',
                'maintenance': 'Extreme',
                'css_class': 'orbit-type-leo'
            }
        elif altitude_km <= 2000:
            return {
                'type': 'LEO',
                'category': 'Low Earth Orbit',
                'color': '#4CAF50',
                'description': 'Ideal for Earth observation and ISS operations',
                'suitability': 'Excellent for imaging missions',
                'maintenance': 'Moderate',
                'css_class': 'orbit-type-leo'
            }
        elif altitude_km <= 35786:
            return {
                'type': 'MEO',
                'category': 'Medium Earth Orbit',
                'color': '#FF9800',
                'description': 'Perfect for navigation satellites (GPS)',
                'suitability': 'Optimal for global coverage',
                'maintenance': 'Low',
                'css_class': 'orbit-type-meo'
            }
        elif abs(altitude_km - 35786) < 100:
            return {
                'type': 'GEO',
                'category': 'Geostationary Orbit',
                'color': '#2196F3',
                'description': 'Fixed position over Earth - Perfect for communications',
                'suitability': 'Ideal for weather & communication satellites',
                'maintenance': 'Very Low',
                'css_class': 'orbit-type-geo'
            }
        else:
            return {
                'type': 'HEO',
                'category': 'High Earth Orbit',
                'color': '#9C27B0',
                'description': 'Deep space missions and specialized applications',
                'suitability': 'Scientific & exploration missions',
                'maintenance': 'Minimal',
                'css_class': 'orbit-type-heo'
            }
    
    def generate_ai_analysis(self, mass_kg, altitude_km, orbit_params, orbit_classification):
        """Generate comprehensive AI analysis"""
        velocity_kms = orbit_params['velocity_kms']
        period_hours = orbit_params['period_hours']
        
        analysis = f"""
        **🤖 AI MISSION ANALYSIS**
        
        **Mission Profile Assessment:**
        - **Satellite Mass:** {mass_kg:,.0f} kg
        - **Orbital Altitude:** {altitude_km:,.0f} km
        - **Required Velocity:** {velocity_kms:.2f} km/s
        - **Orbital Period:** {period_hours:.2f} hours
        
        **Mission Suitability:** {orbit_classification['suitability']}
        
        **Energy Requirements:**
        - **Launch ΔV:** ~{velocity_kms:.1f} km/s
        - **Maintenance:** {orbit_classification['maintenance']}
        
        **AI Recommendations:**
        """
        
        if altitude_km < 200:
            analysis += """
            ⚠️ **HIGH RISK**: Atmospheric drag will cause rapid orbital decay
            - Expect frequent orbital corrections
            - Mission duration severely limited
            - High fuel consumption required
            """
        elif altitude_km <= 600:
            analysis += """
            ✅ **EXCELLENT CHOICE**: Perfect for Earth observation
            - High resolution imaging possible
            - Good ground station communication
            - Reasonable launch costs
            """
        elif altitude_km <= 1500:
            analysis += """
            🛰️ **GOOD OPTION**: Suitable for communication missions
            - Regional coverage achievable
            - Stable orbital environment
            - Moderate power requirements
            """
        elif altitude_km <= 20000:
            analysis += """
            🌐 **OPTIMAL**: Navigation satellite altitude
            - Global coverage possible
            - Long orbital periods
            - Excellent for GPS constellation
            """
        elif abs(altitude_km - 35786) < 500:
            analysis += """
            🌍 **PERFECT**: Geostationary orbit achieved!
            - Fixed position over Earth
            - 24-hour orbital period
            - Ideal for weather monitoring and communications
            """
        else:
            analysis += """
            🚀 **SPECIALIZED**: Deep space trajectory
            - Very high energy requirements
            - Limited Earth communication windows
            - Suitable for scientific exploration
            """
        
        return analysis

def create_3d_orbit_visualization(altitude_km, orbit_classification):
    """Create beautiful 3D orbit visualization"""
    
    # Create Earth sphere
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 50)
    earth_radius = 6371
    
    x_earth = earth_radius * np.outer(np.cos(u), np.sin(v))
    y_earth = earth_radius * np.outer(np.sin(u), np.sin(v))
    z_earth = earth_radius * np.outer(np.ones(np.size(u)), np.cos(v))
    
    # Create orbital path
    orbital_radius = earth_radius + altitude_km
    theta = np.linspace(0, 2 * np.pi, 100)
    x_orbit = orbital_radius * np.cos(theta)
    y_orbit = orbital_radius * np.sin(theta)
    z_orbit = np.zeros_like(theta)
    
    # Create satellite position (animated)
    current_time = time.time()
    satellite_angle = (current_time % 10) / 10 * 2 * np.pi  # 10 second rotation
    sat_x = orbital_radius * np.cos(satellite_angle)
    sat_y = orbital_radius * np.sin(satellite_angle)
    sat_z = 0
    
    # Create 3D plot
    fig = go.Figure()
    
    # Add Earth
    fig.add_trace(go.Surface(
        x=x_earth, y=y_earth, z=z_earth,
        colorscale='Blues',
        showscale=False,
        name='Earth',
        hovertemplate='Earth<extra></extra>'
    ))
    
    # Add orbital path
    fig.add_trace(go.Scatter3d(
        x=x_orbit, y=y_orbit, z=z_orbit,
        mode='lines',
        line=dict(color=orbit_classification['color'], width=8),
        name=f'{orbit_classification["type"]} Orbit',
        hovertemplate=f'Altitude: {altitude_km} km<extra></extra>'
    ))
    
    # Add satellite
    fig.add_trace(go.Scatter3d(
        x=[sat_x], y=[sat_y], z=[sat_z],
        mode='markers',
        marker=dict(
            size=15,
            color='red',
            symbol='diamond'
        ),
        name='Satellite',
        hovertemplate=f'Satellite Position<br>Altitude: {altitude_km} km<extra></extra>'
    ))
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=f"🛰️ {orbit_classification['type']} - {altitude_km:,.0f} km Altitude",
            x=0.5,
            font=dict(size=20, color='white')
        ),
        scene=dict(
            xaxis_title="X (km)",
            yaxis_title="Y (km)",
            zaxis_title="Z (km)",
            bgcolor='black',
            xaxis=dict(backgroundcolor='black', gridcolor='gray'),
            yaxis=dict(backgroundcolor='black', gridcolor='gray'),
            zaxis=dict(backgroundcolor='black', gridcolor='gray'),
            aspectmode='cube'
        ),
        paper_bgcolor='black',
        plot_bgcolor='black',
        font=dict(color='white'),
        height=600,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    return fig

def create_orbital_comparison_chart():
    """Create comparison chart of different orbits"""
    
    orbit_data = {
        'Orbit Type': ['LEO', 'MEO', 'GEO', 'HEO'],
        'Altitude (km)': [400, 20200, 35786, 50000],
        'Velocity (km/s)': [7.67, 3.87, 3.07, 2.65],
        'Period (hours)': [1.5, 12, 24, 36],
        'Use Cases': ['Earth Observation', 'Navigation (GPS)', 'Communications', 'Deep Space']
    }
    
    df = pd.DataFrame(orbit_data)
    
    fig = go.Figure()
    
    # Add altitude bars
    fig.add_trace(go.Bar(
        x=df['Orbit Type'],
        y=df['Altitude (km)'],
        name='Altitude (km)',
        marker_color=['#4CAF50', '#FF9800', '#2196F3', '#9C27B0'],
        text=df['Altitude (km)'],
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>Altitude: %{y} km<br>Use: %{customdata}<extra></extra>',
        customdata=df['Use Cases']
    ))
    
    fig.update_layout(
        title='🚀 Orbital Altitude Comparison',
        xaxis_title='Orbit Types',
        yaxis_title='Altitude (km)',
        template='plotly_dark',
        height=400,
        showlegend=False
    )
    
    return fig

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🛰️ AI Satellite Orbit Simulator</h1>
        <p>Interactive Orbital Physics Simulation with AI-Powered Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize calculator
    calc = SatelliteOrbitCalculator()
    
    # Sidebar controls
    st.sidebar.markdown("## 🎛️ Mission Parameters")
    
    # Satellite mass input
    st.sidebar.markdown("### 🛰️ Satellite Configuration")
    mass_kg = st.sidebar.slider(
        "Satellite Mass (kg)",
        min_value=100,
        max_value=50000,
        value=1000,
        step=100,
        help="Mass of the satellite in kilograms"
    )
    
    # Altitude input
    altitude_km = st.sidebar.slider(
        "Orbital Altitude (km)",
        min_value=150,
        max_value=50000,
        value=400,
        step=50,
        help="Height above Earth's surface in kilometers"
    )
    
    # Quick preset buttons
    st.sidebar.markdown("### 🚀 Quick Presets")
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("🌍 ISS Orbit"):
            altitude_km = 408
            mass_kg = 420000
    
    with col2:
        if st.button("🛰️ GPS Orbit"):
            altitude_km = 20200
            mass_kg = 2000
    
    col3, col4 = st.sidebar.columns(2)
    with col3:
        if st.button("📡 GEO Orbit"):
            altitude_km = 35786
            mass_kg = 5000
    
    with col4:
        if st.button("🔭 Hubble"):
            altitude_km = 547
            mass_kg = 11110
    
    # Calculate orbital parameters
    orbit_params = calc.calculate_orbital_parameters(mass_kg, altitude_km)
    orbit_classification = calc.classify_orbit_ai(altitude_km)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 3D Visualization
        st.markdown("## 🌍 Real-Time Orbital Visualization")
        orbit_fig = create_3d_orbit_visualization(altitude_km, orbit_classification)
        st.plotly_chart(orbit_fig, use_container_width=True)
        
        # Orbital comparison
        st.markdown("## 📊 Orbital Types Comparison")
        comparison_fig = create_orbital_comparison_chart()
        st.plotly_chart(comparison_fig, use_container_width=True)
    
    with col2:
        # Orbit classification
        st.markdown(f"""
        <div class="{orbit_classification['css_class']}">
            <h3>🎯 Orbit Classification</h3>
            <h2 style="color: {orbit_classification['color']};">{orbit_classification['type']}</h2>
            <p><strong>{orbit_classification['category']}</strong></p>
            <p>{orbit_classification['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Key metrics
        st.markdown("## 📊 Orbital Parameters")
        
        st.metric(
            label="🚀 Orbital Velocity",
            value=f"{orbit_params['velocity_kms']:.2f} km/s",
            delta=f"{orbit_params['velocity_ms']:,.0f} m/s"
        )
        
        st.metric(
            label="⏰ Orbital Period",
            value=f"{orbit_params['period_hours']:.2f} hours",
            delta=f"{orbit_params['period_minutes']:.1f} minutes"
        )
        
        st.metric(
            label="💪 Centripetal Force",
            value=f"{orbit_params['centripetal_force']:,.0f} N",
            delta=f"{orbit_params['centripetal_force']/9.81:.0f} kg⋅g"
        )
        
        st.metric(
            label="🌐 Orbital Radius",
            value=f"{orbit_params['orbital_radius_km']:,.0f} km",
            delta=f"{altitude_km:,} km above Earth"
        )
    
    # AI Analysis Section
    st.markdown("""
    <div class="ai-analysis">
        <h2>🤖 AI Mission Analysis</h2>
    </div>
    """, unsafe_allow_html=True)
    
    ai_analysis = calc.generate_ai_analysis(mass_kg, altitude_km, orbit_params, orbit_classification)
    st.markdown(ai_analysis)
    
    # Physics formulas section
    st.markdown("""
    <div class="physics-section">
        <h2>🧮 Physics Calculations</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Orbital Velocity**
        ```
        v = √(GM/r)
        ```
        Where:
        - G = 6.674×10⁻¹¹ m³/kg⋅s²
        - M = 5.972×10²⁴ kg (Earth)
        - r = orbital radius
        """)
    
    with col2:
        st.markdown("""
        **Orbital Period**
        ```
        T = 2π√(r³/GM)
        ```
        Where:
        - r = orbital radius
        - G = gravitational constant
        - M = Earth's mass
        """)
    
    with col3:
        st.markdown("""
        **Centripetal Force**
        ```
        F = mv²/r
        ```
        Where:
        - m = satellite mass
        - v = orbital velocity
        - r = orbital radius
        """)
    
    # Mission planning section
    st.markdown("## 🎯 Mission Planning Assistant")
    
    mission_type = st.selectbox(
        "Select Mission Type",
        ["Earth Observation", "Communications", "Navigation", "Weather Monitoring", "Scientific Research", "Space Station"]
    )
    
    # Provide mission-specific recommendations
    recommendations = {
        "Earth Observation": "Recommended: LEO (400-800 km) for high-resolution imaging",
        "Communications": "Recommended: GEO (35,786 km) for fixed coverage area",
        "Navigation": "Recommended: MEO (20,000 km) for global coverage",
        "Weather Monitoring": "Recommended: GEO (35,786 km) for continuous monitoring",
        "Scientific Research": "Varies by mission - LEO for Earth studies, HEO for space research",
        "Space Station": "Recommended: LEO (400-500 km) for crew safety and accessibility"
    }
    
    st.info(f"💡 **Mission Recommendation:** {recommendations[mission_type]}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;">
        <h3>🌟 Created for Impact Revolution</h3>
        <p>Inspiring the next generation of space scientists and AI developers!</p>
        <p><em>Interactive Physics • AI Analysis • Real-time Visualization</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
