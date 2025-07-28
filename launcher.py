import subprocess
import sys
import os

def print_banner():
    banner = """
    🛰️  AI SATELLITE ORBIT SIMULATOR  🛰️
    ======================================
    
    Educational Physics Simulation Tool
    Real-time Orbital Mechanics with AI Analysis
    
    Choose your simulation mode:
    """
    print(banner)

def print_options():
    options = """
    1. 🎮 Full Interactive Simulation (Recommended)
       - Real-time pygame visualization
       - Keyboard controls for parameters
       - Live physics calculations
       - AI orbit classification
    
    2. 🖥️  GUI Control Panel + Visualization
       - User-friendly interface
       - Sliders for easy parameter adjustment
       - Detailed AI analysis panel
       - Separate visualization window
    
    3. ℹ️  Show Project Information
       - About this project
       - Educational objectives
       - Technical details
    
    4. 🚪 Exit
    """
    print(options)

def run_main_simulation():
    try:
        print("\n🚀 Starting Full Interactive Simulation...")
        print("Controls:")
        print("  Enter: Start/Stop simulation")
        print("  ↑/↓: Adjust altitude")
        print("  ←/→: Adjust mass")
        print("  Space: Clear trail")
        print("  +/-: Simulation speed")
        print("\nLaunching simulation window...")
        
        subprocess.run([sys.executable, "main.py"])
    except Exception as e:
        print(f"Error running simulation: {e}")
        input("Press Enter to continue...")

def run_gui_simulation():
    try:
        print("\n🖥️  Starting GUI Control Panel...")
        print("Features:")
        print("  - Interactive parameter sliders")
        print("  - Real-time calculations")
        print("  - AI analysis panel")
        print("  - Visual simulation window")
        print("\nLaunching GUI...")
        
        subprocess.run([sys.executable, "satellite_gui.py"])
    except Exception as e:
        print(f"Error running GUI: {e}")
        input("Press Enter to continue...")

def show_project_info():
    info = """
    🛰️ AI SATELLITE ORBIT SIMULATOR
    ================================
    
    📋 PROJECT OVERVIEW:
    An interactive educational tool that demonstrates orbital mechanics
    through real-time physics calculations and AI-powered analysis.
    
    🎯 EDUCATIONAL OBJECTIVES:
    • Understand orbital mechanics (velocity, period, force)
    • Experience AI in scientific simulation
    • Explore space technology concepts
    • Engage with STEM through interactive learning
    
    🧮 PHYSICS CALCULATIONS:
    • Orbital Velocity: v = √(GM/r)
    • Orbital Period: T = 2π√(r³/GM)
    • Centripetal Force: F = mv²/r
    
    🤖 AI FEATURES:
    • Smart orbit classification (LEO/MEO/GEO/HEO)
    • Mission suitability analysis
    • Energy requirement calculations
    • Stability assessments
    
    📊 SUPPORTED ORBIT TYPES:
    • LEO (Low Earth Orbit): 160-2,000 km
    • MEO (Medium Earth Orbit): 2,000-35,786 km
    • GEO (Geostationary Orbit): ~35,786 km
    • HEO (High Earth Orbit): >35,786 km
    
    💡 TECHNICAL FEATURES:
    • Real-time visualization with pygame
    • Interactive parameter adjustment
    • AI-powered orbit analysis
    • Educational physics display
    • Smooth animation and effects
    
    Created for Impact Revolution - Inspiring future space scientists! 🌟
    """
    print(info)
    input("\nPress Enter to return to main menu...")

def main():
    while True:
        # Clear screen (Windows)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print_banner()
        print_options()
        
        try:
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == '1':
                run_main_simulation()
            elif choice == '2':
                run_gui_simulation()
            elif choice == '3':
                show_project_info()
            elif choice == '4':
                print("\n🚀 Thank you for using AI Satellite Orbit Simulator!")
                print("Keep exploring the cosmos! 🌌")
                break
            else:
                print("\n❌ Invalid choice. Please enter 1, 2, 3, or 4.")
                input("Press Enter to continue...")
        
        except KeyboardInterrupt:
            print("\n\n🚀 Thank you for using AI Satellite Orbit Simulator!")
            print("Keep exploring the cosmos! 🌌")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
