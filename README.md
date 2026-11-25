# Slovakia Districts Quiz

An interactive geography quiz to test your knowledge of Slovakia's 79 districts (*okresy*), available as both a terminal game and a Streamlit web application.

## Features
- **Two Game Modes:** Free-text input (with Unicode NFD normalization to handle Slovak diacritics and hyphens) or 4-option multiple choice.
- **Dynamic Map Rendering:** Multi-layer choropleth maps highlighting correct guesses, mistakes, and the active target district.
- **Auto-Zoom:** Automatically zooms in on small urban districts (e.g., Bratislava I–V, Košice I–IV) based on polygon area thresholds.
- **Progress & Recovery:** Tracks score, provides first-letter hints, and allows replaying missed districts.

## Tech Stack
- **Python 3**
- **GeoPandas & Matplotlib:** Spatial data processing and map rendering (`EPSG:3395` projection).
- **Streamlit:** Interactive web interface.

## Installation & Usage

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd slovakia_quiz
