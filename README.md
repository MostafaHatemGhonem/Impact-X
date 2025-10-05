# 🌠 Meteor Madness

An interactive desktop application that simulates asteroid impacts on Earth using real NASA data. Visualize the devastating effects of near-Earth objects and explore "what if" scenarios with scientifically-based calculations.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.12-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## ✨ Features

- **Real NASA Data**: Fetch actual near-Earth asteroids from NASA's JPL SBDB API
- **Two Simulation Modes**:
  - **Destroy Earth**: Create catastrophic impact scenarios
  - **Save Earth**: Explore successful deflection missions
- **Impact Calculations**: 
  - Mass and kinetic energy
  - Crater dimensions
  - Earthquake magnitude (Richter scale)
  - Tsunami height for ocean impacts
  - Multiple damage radii zones (total destruction, severe, moderate, window breakage)
- **Interactive Maps**: Visualize impact zones with multi-layer folium maps
- **Land/Ocean Detection**: Automatic geocoding to determine impact location type
- **Modern UI**: 
  - Fixed navigation logo
  - Space-themed interface with smooth animations
  - Typing effects throughout
  - Responsive design

## 📋 Prerequisites

- Python 3.12+
- Node.js and npm (for TypeScript compilation)
- Virtual environment (recommended)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/MostafaHatemGhonem/Meteor-Madness.git
cd Meteor-Madness
```

### 2. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```txt
bottle==0.12.25
requests==2.31.0
python-dotenv==1.0.0
folium==0.15.1
pywebview==4.4.1
qtpy==2.4.1
PyQt5==5.15.10
PyQtWebEngine==5.15.6
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```env
OPENCAGE_API_KEY=your_opencage_api_key_here
```

Get your free API key from [OpenCage Geocoding API](https://opencagedata.com/)

### 5. Set Up Required Assets

#### **Download Videos**

Create the `web/assit/videos/` folder and add these videos:

| File Name | Purpose | Where to Get |
|-----------|---------|--------------|
| `Earth_wAtmos_spin_02_2160p30.mp4` | Page 2 Earth animation | [NASA SVS](https://svs.gsfc.nasa.gov/) or [Pixabay](https://pixabay.com/videos/search/earth/) |
| `Earth - 28049.mp4` | Save Earth card video | [Pexels](https://www.pexels.com/search/videos/earth/) |
| `Earth.mp4` | Destroy Earth card video | [Pexels](https://www.pexels.com/search/videos/earth/) |
| `Earth destroyed.mp4` | Simulation animation | [Pixabay](https://pixabay.com/videos/search/explosion/) or create custom |
| `planet-star.gif` | Loading spinner | [NASA Images](https://images.nasa.gov/) or [Giphy](https://giphy.com/) |

**Video Specifications:**
- Format: MP4 (H.264 codec recommended)
- Resolution: 1080p minimum, 4K for main Earth video
- Duration: 5-30 seconds (looping animations)
- File size: Keep under 10MB each for performance

#### **Download Images**

Create the `web/assit/Images/` folder and add:

| File Name | Purpose | Where to Get |
|-----------|---------|--------------|
| `Meteor.png` | Flying meteor animation | [NASA](https://www.nasa.gov/) or create with transparent background |
| `starsScreen.png` | Starfield background | [Unsplash Space](https://unsplash.com/s/photos/stars) (make tileable) |

**Image Specifications:**
- `Meteor.png`: 150x150px, transparent PNG with glow effect
- `starsScreen.png`: 512x512px minimum, seamless tileable pattern

#### **Download Font**

1. Visit [Google Fonts - Montserrat](https://fonts.google.com/specimen/Montserrat)
2. Download the **Black (900)** weight
3. Place `Montserrat-Black.ttf` in `web/assit/Font/Montserrat/static/`

**Alternative:** Use the font from GitHub: [Montserrat Repository](https://github.com/JulietaUla/Montserrat)

### 6. Compile TypeScript

```bash
cd web
npm install -g typescript  # If not already installed
tsc
```

## 📁 Project Structure

```
Meteor-Madness/
├── src/
│   ├── app.py              # Backend API handler with type hints
│   ├── calculations.py     # Impact physics calculations
│   ├── simulation.py       # Map generation with error handling
│   └── run.py             # Application entry point
├── web/
│   ├── index.html          # Main HTML structure
│   ├── style.css           # Modern styling with fixed logo
│   ├── script.ts           # TypeScript source with DOMContentLoaded
│   ├── tsconfig.json       # TypeScript configuration
│   ├── assit/              # Assets folder
│   │   ├── Images/         # Images and icons
│   │   │   ├── Meteor.png          # Flying meteor animation
│   │   │   └── starsScreen.png     # Background starfield
│   │   ├── videos/         # Video assets
│   │   │   ├── Earth_wAtmos_spin_02_2160p30.mp4  # Page 2 Earth
│   │   │   ├── Earth - 28049.mp4   # Save Earth option
│   │   │   ├── Earth.mp4           # Destroy Earth option
│   │   │   ├── Earth destroyed.mp4 # Simulation animation
│   │   │   └── planet-star.gif     # Loading spinner
│   │   └── Font/
│   │       └── Montserrat/
│   │           └── static/
│   │               └── Montserrat-Black.ttf
│   └── dist/
│       └── script.js       # Compiled JavaScript
├── .env                    # Environment variables
├── requirements.txt        # Python dependencies
└── README.md
```

## 🎮 Usage

### Running the Application

```bash
python src/main.py
```

The application will open in a desktop window (1200x800) powered by pywebview.

### Navigation

The application features multiple pages accessible through smooth scrolling:

1. **Page One**: Welcome screen with typing animation
2. **Page Two**: Earth visualization and introduction
3. **Page Three**: Choose between "Destroy Earth" or "Save Earth" modes

### Destroy Earth Mode

Two options available:

#### 1. Add Your Asteroid
- Enter custom parameters:
  - Diameter (km)
  - Velocity (km/s)
  - Impact location (latitude/longitude)
- Generates immediate simulation with detailed results

#### 2. Choose Your Asteroid
- Select from real near-Earth asteroids fetched from NASA
- Data includes:
  - Asteroid designation
  - Absolute magnitude (H)
  - Relative velocity
- Automatically calculates diameter from magnitude
- Enter impact location coordinates

### Save Earth Mode

Explore 5 successful deflection scenarios:

1. **Deflection Mission Success**: DART-style kinetic impactor
2. **Nuclear Disruption**: Fragmentation strategy
3. **Gravity Tractor**: Long-term deflection
4. **Last-Minute Evacuation**: Emergency response
5. **Kinetic Impactor**: High-speed collision

Each scenario shows:
- Original threat parameters
- Actual minimal impact
- Success message
- Interactive map of saved location

### Understanding Results

**Mass & Energy:**
- Total mass in kilograms
- Kinetic energy in joules
- TNT equivalent in megatons

**Impact Effects:**
- Crater diameter and depth (or tsunami height for ocean)
- Earthquake magnitude (Richter scale)
- Ocean vs. land impact detection

**Damage Zones (Interactive Map):**
- Total Destruction (dark red)
- Severe Damage (red)
- Moderate Damage (orange)
- Window Breakage (yellow)

## 🔬 Science Behind the Calculations

### Diameter from Absolute Magnitude
```python
D = 1329 / √(albedo) × 10^(-0.2 × H) km
```
Using albedo = 0.15 for C-type asteroids

### Mass Calculation
```python
Volume = (4/3) × π × r³
Mass = Density × Volume
```
Using C-type asteroid density: 2600 kg/m³

### Kinetic Energy
```python
E = ½ × mass × velocity²
```

### Crater Diameter
```python
D = 1.161 × (E / 10¹⁵)^0.294 km
Depth = 0.2 × D
```

### Tsunami Height (Ocean Impacts)
```python
H = 0.8 × √E / (ocean_depth)^0.75 meters
```
Assuming average ocean depth: 4000m

### Earthquake Magnitude
```python
M = 0.67 × log₁₀(E) - 5.87
```

### Damage Radii
Based on NASA's Earth Impact Effects Program:
- Total Destruction: 0.042 × (Mt)^(1/3) km
- Severe Damage: 0.084 × (Mt)^(1/3) km
- Moderate Damage: 0.17 × (Mt)^(1/3) km
- Window Breakage: 0.34 × (Mt)^(1/3) km

## 🛠️ Troubleshooting

### Assets Missing

**Symptoms**: Blank videos, missing background, font not loading

**Check**:
```bash
# Verify all assets exist
ls web/assit/videos/
ls web/assit/Images/
ls web/assit/Font/Montserrat/static/
```

**Solution**: Download all required assets (see Installation step 5)

### Map Not Displaying

**Issue**: "Error generating map: '>' not supported between instances of 'dict' and 'int'"

**Solution**: The updated `simulation.py` includes type checking and proper dict handling. Ensure you're using the latest version.

### PyWebview GUI Issues (Linux)

**Symptoms**: "You must have either QT or GTK installed"

**Solution**:
```bash
pip install qtpy PyQt5 PyQtWebEngine
```

Alternative:
```bash
pip install PySide6 qtpy
```

### GStreamer Warnings

**Symptoms**: WebKit warnings about missing AAC codec or WebVTT encoder

**Impact**: Videos may play without audio

**Solution** (Optional):
```bash
# Ubuntu/Debian
sudo apt-get install gstreamer1.0-plugins-bad gstreamer1-plugins-ugly

# Fedora
sudo dnf install gstreamer1-plugins-bad-free gstreamer1-plugins-ugly

# Arch
sudo pacman -S gst-plugins-bad gst-plugins-ugly
```

### TypeScript Compilation Errors

```bash
cd web
tsc --watch  # Watch mode for development
```

Check `tsconfig.json` for proper configuration.

### Logo Position Issues

The logo should remain fixed at the top. If it scrolls, check that `style.css` includes:
```css
.logo {
  position: fixed;
  top: 0;
  z-index: 1000;
}
```

### API Rate Limits

- **OpenCage**: 2,500 requests/day (free tier)
- **NASA API**: No authentication required, reasonable rate limits

## 🎨 Customization

### Styling

Edit `web/style.css` to customize:

**Color Scheme**:
```css
:root {
  --maincolor: #fff;
  --accentColor: #00d4ff;
  --dangerColor: #ff3366;
}
```

**Logo Position**: Already fixed at top with backdrop blur

**Animations**: Modify keyframes for custom effects

### Physics Parameters

Modify `src/calculations.py`:
```python
density = 2600  # C-type asteroid (kg/m³)
albedo = 0.15   # Reflectivity
```

### Scenario Messages

Edit scenarios in `web/script.ts`:
```typescript
const saveScenarios = [
  {
    id: 1,
    name: "Your Scenario",
    description: "Description",
    diameter: "0.05",
    velocity: "10",
    message: "Success message"
  }
]
```

## 📊 API Reference

### Backend Methods

#### `Api.get_asteroid_list() -> str`

Fetches near-Earth asteroids from NASA JPL API.

**Returns**:
```json
[
  {
    "name": "2024 AB",
    "h": 22.5,
    "v_inf": 15.3
  }
]
```

**Error Response**:
```json
{
  "error": "Error message"
}
```

#### `Api.run_simulation(...) -> str`

**Parameters**:
- `asteroid_name` (Optional[str]): Asteroid designation
- `diameter` (Optional[str]): Diameter in km
- `velocity` (Optional[str]): Velocity in km/s
- `lat` (Optional[str]): Latitude (-90 to 90)
- `long` (Optional[str]): Longitude (-180 to 180)
- `h_value` (Optional[str]): Absolute magnitude
- `v_inf_value` (Optional[str]): Velocity for real asteroids

**Returns**:
```json
{
  "mass_kg": 1234567890.5,
  "energy_joules": 9.876543210e15,
  "megatons_tnt": 123.45,
  "crater_diameter_km": 5.67,
  "crater_depth_km": 1.13,
  "earthquake_magnitude": 6.8,
  "tsunami_height_m": 45.2,
  "is_ocean_impact": true,
  "damage_radii_km": {
    "total_destruction_km": 2.1,
    "severe_damage_km": 4.2,
    "moderate_damage_km": 8.5,
    "window_breakage_km": 17.0
  },
  "map_html": "<div>...</div>",
  "impact_location": {
    "latitude": 40.7128,
    "longitude": -74.0060
  }
}
```

#### `Api.check_land_or_water(lat: float, lon: float) -> Dict`

Determines if coordinates are on land or in ocean using OpenCage API.

**Returns**:
```json
{
  "is_ocean": false
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Add type hints to all Python functions
- Use TypeScript for frontend code
- Add error handling for all API calls
- Test on multiple platforms (Linux, Windows, macOS)
- Follow existing code style

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **NASA JPL**: Near-Earth object data via SBDB Close-Approach API
- **OpenCage**: Geocoding API for land/ocean detection
- **Folium**: Interactive map generation
- **PyWebview**: Cross-platform desktop application framework
- **Earth Impact Effects Program**: Damage radius calculations

## 📧 Contact

**Infinity Explorers EG**

Project Link: [https://github.com/yourusername/Meteor-Madness](https://github.com/yourusername/Meteor-Madness)

## ⚠️ Disclaimer

This application is for educational and entertainment purposes only. The calculations are simplified approximations and should not be used for actual risk assessment or scientific research. Real asteroid impact predictions require complex models accounting for numerous variables including:

- Atmospheric entry effects
- Asteroid composition and structure
- Impact angle
- Local geology
- Atmospheric conditions
- Ground slope and properties

For accurate impact predictions, consult professional planetary defense organizations.

## 🔮 Future Enhancements

- [ ] 3D impact visualization using Three.js
- [ ] Real-time population impact estimates
- [ ] Historical impact database (Tunguska, Chelyabinsk, etc.)
- [ ] Multiple asteroid comparison mode
- [ ] PDF export of simulation reports
- [ ] Social sharing features
- [ ] Mobile app version (React Native)
- [ ] Multi-language support (i18n)
- [ ] Night mode toggle
- [ ] Sound effects and audio narration
- [ ] Time-lapse impact progression
- [ ] Integration with real-time NEO tracking

## 🐛 Known Issues

- GStreamer warnings on Linux (cosmetic, doesn't affect functionality)
- Map rendering may be slow for very large damage radii
- Some browsers may block autoplay videos
- Videos without audio due to missing AAC codec (visual-only experience still works)

## 📦 Asset Sources

### Free Resources for Missing Assets

**Earth & Space Videos:**
- [NASA Scientific Visualization Studio](https://svs.gsfc.nasa.gov/) - High-quality Earth animations
- [Pixabay](https://pixabay.com/videos/) - Free stock videos
- [Pexels](https://www.pexels.com/videos/) - Free HD videos
- [Videezy](https://www.videezy.com/) - Free space footage

**Images:**
- [NASA Image Gallery](https://images.nasa.gov/) - Official space images
- [Unsplash](https://unsplash.com/) - High-resolution photos
- [ESA/Hubble](https://www.spacetelescope.org/images/) - Space telescope images

**Fonts:**
- [Google Fonts](https://fonts.google.com/specimen/Montserrat) - Montserrat font family
- [GitHub Montserrat](https://github.com/JulietaUla/Montserrat) - Direct font files

### Creating Custom Assets

**Meteor.png:**
1. Use GIMP/Photoshop
2. Create 150x150px canvas
3. Draw/import meteor shape
4. Add outer glow effect (cyan/orange)
5. Export as transparent PNG

**starsScreen.png:**
1. Create 512x512px black canvas
2. Add white dots of varying sizes
3. Apply slight gaussian blur
4. Test tiling to ensure seamless edges
5. Export as PNG

## 📚 Resources

- [NASA NEO Program](https://cneos.jpl.nasa.gov/)
- [Earth Impact Effects Calculator](https://impact.ese.ic.ac.uk/ImpactEarth/)
- [Planetary Defense Conference](https://www.hou.usra.edu/meetings/pdc2021/)

---

**Made with 💫 by Infinity Explorers EG**

*Exploring the cosmos, one simulation at a time.*
