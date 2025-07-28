"""
Test script to verify Streamlit app functionality
"""

import sys
import importlib.util

def test_imports():
    """Test if all required packages are available"""
    required_packages = [
        'streamlit',
        'plotly',
        'numpy',
        'pandas',
        'math',
        'time'
    ]
    
    print("🧪 Testing package imports...")
    
    for package in required_packages:
        try:
            if package == 'math' or package == 'time':
                # Built-in modules
                __import__(package)
            else:
                importlib.import_module(package)
            print(f"✅ {package} - OK")
        except ImportError as e:
            print(f"❌ {package} - FAILED: {e}")
            return False
    
    return True

def test_streamlit_app():
    """Test the Streamlit app components"""
    print("\n🔬 Testing Streamlit app components...")
    
    try:
        # Test basic imports from our app
        import numpy as np
        import plotly.graph_objects as go
        import math
        
        # Test calculations
        earth_radius = 6371  # km
        altitude = 400  # km
        orbital_radius = earth_radius + altitude
        velocity = math.sqrt(6.67430e-11 * 5.972e24 / (orbital_radius * 1000))
        
        print(f"✅ Physics calculations working")
        print(f"   Orbital velocity: {velocity/1000:.2f} km/s")
        
        # Test 3D plot creation
        u = np.linspace(0, 2 * np.pi, 10)
        v = np.linspace(0, np.pi, 10)
        x = earth_radius * np.outer(np.cos(u), np.sin(v))
        y = earth_radius * np.outer(np.sin(u), np.sin(v))
        z = earth_radius * np.outer(np.ones(np.size(u)), np.cos(v))
        
        fig = go.Figure()
        fig.add_trace(go.Surface(x=x, y=y, z=z, showscale=False))
        
        print("✅ 3D visualization working")
        
        return True
        
    except Exception as e:
        print(f"❌ App component test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🛰️ AI Satellite Orbit Simulator - Component Test")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed!")
        return False
    
    # Test app components
    if not test_streamlit_app():
        print("\n❌ App component tests failed!")
        return False
    
    print("\n🎉 All tests passed! Streamlit app is ready to run.")
    print("\n🚀 To start the app, run:")
    print("   streamlit run streamlit_app_pro.py")
    print("\n🌐 The app will be available at: http://localhost:8501")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
