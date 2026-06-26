# 🎵📊 Personal Spotify Rewinder (Wrapped)

An interactive web dashboard built with **Flask** and **Pandas** to visualize and analyze the complete streaming history of a Spotify user using the JSON data files extracted from their account. It supports both standard `StreamingHistory*.json` files (from the basic account data) and the extended `endsong.json` history files.

The HTML, CSS & JavaScript UI includes a dark theme with modern glow effects, smooth entrance animations, and responsive layouts.

---

## 📸 Preview Demo
This is a preview of the dashboard populated with listening history.

![Spotify Rewinder Dashboard Preview](dashboard_preview.png)

---

## ✨ Main Features

### 🚀 Web Architecture & Performance
* **Dynamic Filters:** Filter between lifetime listening history or a specific year. The graphs, KPIs, and insights update instantly in the background via **AJAX (Fetch API)** without requiring page reloads.
* **Session Caching:** Processed Pandas payloads are cached in-memory on the Flask server using a session UUID, avoiding reprocessing or requiring re-uploads when toggling filters or reloading.
* **Modern & Fluid Interface:** Responsive design built with vanilla CSS containing glow backdrops, a noise texture overlay, smooth scroll transitions, and element reveal animations using the `IntersectionObserver` API.
* **Inline Processing State:** Clear visual loading indicators (spinner and text updates) during file upload and parsing.

### 📈 Insights & Statistics

* **General View KPIs:**
  * **Total Listening Time:** Total accumulated minutes streamed.
  * **Top Artist:** Your #1 most-streamed artist, along with the total hours/minutes spent listening to them.
  * **Unique Songs:** Total number of distinct tracks discovered.
  * **Skip Rate:** The overall percentage of tracks you skipped.

* **Calculated Analytics:**
  * **Binge Day:** Automatically detects the single calendar day with the highest listening intensity, displaying the date, hours listened, and the artist you played most on that day.
  * **Ghost Songs:** Counts total plays during the late-night hours (between 00:00 and 05:59).
  * **Listener Profile:** A classification of your listening style based on skip rate:
    * *The Devoted Listener* (Skip rate < 15%)
    * *The Balanced Curator* (Skip rate 15% – 40%)
    * *The Impatient DJ* (Skip rate > 40%)

* **Visualizations (Plotly.js):**
  * **Monthly Evolution:** A line chart displaying listening minutes month-by-month.
  * **Top Artists:** A horizontal bar chart showcasing your Top 10 Artists and their play counts.
  * **Listening Habits Heatmap:** A 2D density heatmap mapping days of the week against hours of the day to pinpoint your peak listening routines.
  * **Song Completion Donut Chart:** A breakdown of track termination reasons (*Completed*, *Skipped*, *Previous*, or *Others*).

---

## 🛠️ Tech Stack

* **Backend:** Python 3, Flask
* **Data Processing:** Pandas
* **Data Visualization:** Plotly Express / Plotly.js (interactive client-side rendering)
* **Frontend:** HTML5, Vanilla CSS3 (custom variables, modern grids, animations), Vanilla JavaScript

---

## 🚀 How to Run the Project Locally

### 1. Prerequisites
Make sure you have Python 3 installed on your machine.

### 2. Clone the Repository
Clone this repository to your local machine.

### 3. Setup a Virtual Environment (Recommended)
```bash
# Windows:
python -m venv .venv
.venv\Scripts\activate

# Mac/Linux:
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Application
```bash
python app.py
```

---

## 📁 Project Structure

```
spotify-rewind-dashboard/
│
├── app.py                  # Main Flask server, API endpoints (upload, clear, cache)
├── data_processing.py      # Pandas logic for parsing and cleaning Spotify JSON formats
├── requirements.txt        # Python package dependencies
├── .gitignore              # Git ignore configuration
│
├── sections/               # Modular components for metric & chart payload generation
│   ├── __init__.py
│   ├── general_view.py     # Total minutes, unique songs, and monthly line chart
│   ├── habits.py           # Listening habits heatmap and completion donut chart
│   ├── eras.py             # Top 10 artists bar chart
│   └── insights.py         # Binge records, ghost songs, and listener profiles
│
├── static/                 # Frontend assets and styling
│   ├── assets/
│   │   └── favicon.svg     # SVG logo favicon
│   ├── styles.css          # CSS styles, theme colors, layout grids, animations
│   └── script.js           # AJAX handlers, DOM updates, and Plotly initialization
│
└── templates/
    └── index.html          # Main HTML structure and layout elements
```

---

## 📄 License
This project is licensed under the MIT License - feel free to clone, modify and share it!

Developed by Gonçalo Libânio

