# AI Satellite Orbit Simulator

🛰️ **Professional AI-Powered Orbital Mechanics Desktop Simulation**

An interactive, educational desktop simulation tool that demonstrates orbital mechanics through real-time physics calculations and AI-powered orbit classification. This project bridges physics, artificial intelligence, and space technology to provide an engaging learning experience.

## 🌟 Features

### �️ Desktop Application with Real-Time Animation
- **Interactive GUI Control Panel**: Tkinter-based parameter adjustment interface
- **Real-Time Pygame Visualization**: Smooth satellite orbital animation
- **Adaptive Scaling**: Works on any screen size automatically
- **AI-Powered Analysis**: Smart orbit classification and mission recommendations
- **Physics Engine**: Accurate orbital calculations with advanced metrics
- **Visual Orbital Trail**: See the satellite's path in real-time

## 🎮 Quick Start

### 🖥️ Desktop Application (Recommended)
```bash
# Clone the repository
git clone https://github.com/jawad-farooque/AI-Simulator.git
cd AI-Simulator

# Install dependencies
pip install -r requirements.txt

# Run the GUI version with control panel and real-time animation
python satellite_gui.py

# Run the main pygame simulation (basic version)
python main.py

# Interactive launcher for all applications
python launcher.py
```

## �️ Application Features

### 🎯 **GUI Control Panel** (`satellite_gui.py`)
- **Parameter Sliders**: Adjust satellite mass (100-50,000 kg) and altitude (150-50,000 km)
- **Real-Time Calculations**: Orbital velocity, period, and centripetal force
- **AI Orbit Classification**: Automatic detection of LEO, MEO, GEO, HEO orbits
- **Mission Analysis**: Detailed AI-powered mission suitability assessment
- **Live Visualization**: Separate pygame window with smooth satellite animation

### 🚀 **Pygame Simulation** (`main.py`)
- **Real-Time Animation**: Watch satellites orbit Earth with realistic physics
- **Adaptive Scaling**: Automatically adjusts to any screen resolution
- **Visual Trail**: See the satellite's orbital path
- **Physics Display**: Live orbital parameters and metrics

## 📊 Educational Applications

- **Physics Education**: Real orbital mechanics calculations
- **Space Science**: Understanding satellite operations
- **AI Integration**: Smart classification and analysis
- **Interactive Learning**: Hands-on exploration of complex concepts

## 🛰️ Orbit Types Supported

| Orbit Type | Altitude Range | Use Cases |
|------------|---------------|-----------|
| **LEO** | 160-2,000 km | Earth observation, ISS |
| **MEO** | 2,000-35,786 km | Navigation (GPS) |
| **GEO** | ~35,786 km | Communications, Weather |
| **HEO** | >35,786 km | Deep space missions |

## 🧮 Physics Calculations

- **Orbital Velocity**: v = √(GM/r)
- **Orbital Period**: T = 2π√(r³/GM)
- **Centripetal Force**: F = mv²/r
- **Launch Requirements**: ΔV calculations
- **Ground Coverage**: Visibility analysis

## 🚀 Deployment

### Streamlit Cloud (Free)
1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select this repository
5. Choose `streamlit_app_pro.py` as main file
6. Deploy!

### Local Development
```bash
pip install -r requirements.txt
streamlit run streamlit_app_pro.py
```

## 📱 Screenshots

*Professional web interface with real-time 3D orbital visualization*

## 🎯 Mission Presets

- 🏠 **ISS**: International Space Station orbit
- 🔭 **Hubble**: Space telescope parameters
- 📡 **GPS**: Navigation satellite constellation
- 🌍 **GEO**: Geostationary communication satellites

## 🤖 AI Features

- **Smart Classification**: Automatic orbit type detection
- **Mission Analysis**: Risk assessment and recommendations
- **Cost Estimation**: Launch cost and mission duration
- **Real-time Feedback**: Instant parameter analysis

## 📋 Requirements

- Python 3.7+
- Streamlit
- Plotly
- NumPy
- Pandas
- Pygame (for desktop versions)

## 🔧 Technical Architecture

- **Physics Engine**: Real-time orbital mechanics
- **AI Classifier**: Rule-based orbit categorization
- **Visualization**: 3D interactive plots with Plotly
- **Web Framework**: Streamlit for professional UI
- **Desktop Framework**: Pygame for real-time simulation

## 📚 Educational Objectives

- Understanding orbital mechanics
- AI applications in space science
- Interactive physics learning
- Space mission planning
- STEM engagement

## 🌟 Created for Impact Revolution

*Inspiring the next generation of space scientists and AI developers!*

---

**© 2025 Impact Revolution | Professional Space Simulation Platform**
