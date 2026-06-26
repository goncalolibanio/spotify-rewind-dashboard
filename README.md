# 🎵📊 Personal Spotify Rewinder (Wrapped)

An interactive web dashboard built with **Flask** and **Pandas** to visualize and analyze the complete streaming history of a Spotify user using the JSON data files extracted from their account.

The HTML, CSS & JAVASCRIPT was done with AI, for visualization purposes.

---

## 📸 Preview Demo
This is a preview of the first dashboard, with my personal data.

![Spotify Rewinder Dashboard Preview](dashboard_preview.png)

---

## ✨ Main Features

### 🚀 Web Architecture & Performance
* **Dynamic Filters:** Filter between the available years in your data (specific year vs. Lifetime Listening). The graphs and insights update instantly in the background via **AJAX (Fetch API)** without needing to refresh the page.
* **Data Caching:** Data processed by Pandas is temporarily stored in the server's memory using a unique session ID (`uuid`), eliminating the need to re-upload files if the user changes tabs or refreshes the page.
* **Fluid & Responsive Interface:** Flexible grid built with pure CSS that adapts seamlessly to any screen size, from wide desktops to mobile devices.
* **Loading Overlay:** A premium animated spinner with a *glassmorphism* blur effect that provides visual feedback while the server handles data aggregations or external API requests.

### 📈 Insights & Statistics

* **General View:**
  * **Primary KPIs:** Total streaming time (minutes), Number 1 Artist, and Unique Song counter.
  * Line chart tracking the monthly evolution of your streaming time.
  * **Listener Profile:** An algorithmic behavioral classification based on your skipping habits (*The Devoted Listener*, *The Balanced Curator*, or *The Impatient DJ*).
  * **Binge Record Day:** Automatically identifies the exact calendar day with the highest streaming spike, showing total hours spent and the featured artist.
  * **Late Night Tracks:** Total counter for songs played during the early morning hours (00:00 AM - 06:00 AM).

* **Daily Habits:**
  * **Weekly Bubble Punchcard:** A scatter plot crossing days of the week with the 24 hours of the day to pinpoint your exact listening routines and intensity peaks.
  * **Clean Donut Chart:** Displays song ending reasons with an intelligent auto-grouping mechanism (*Completed*, *Skipped*, *Others*) to avoid visual clutter from rare system codes.

* **Music Eras:**
  * Horizontal bar chart highlighting your Top 10 Artists.
  * Detailed ranking table showcasing exact play counts.

---

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **Data Crunching:** Pandas
* **Data Visualization:** Plotly Express / Plotly Graph Objects (Interactive native HTML charts)
* **Frontend:** HTML, CSS JAVASCRIPT

---

## 🚀 How to Run the Project Locally

### 1. Prerequisites
Make sure you have Python 3 installed on your machine.

### 2. Clone the Repository

### 3. Setup a .venv Environment (Recommended)
```bash
#Windows:
python -m venv .venv
venv\Scripts\activate

#Mac/Linux:
python3 -m venv .venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run this in terminal
```bash
python app.py
```

## Project Structure
```
spotify-rewind-dashboard/
│
├── app.py                  # Main Flask server and API endpoints
├── data_processing.py      # Core Pandas pipeline for data cleaning and formatting
├── requirements.txt        # Python dependencies list
├── .gitignore              # Git ignore configuration
│
├── sections/               # Isolated Python modules containing business logic
│   ├── general_view.py     # General KPIs and timeline evolution
│   ├── habits.py           # Punchcard scatter plot and Donut charts
│   ├── eras.py             # Top 10 artists and Spotify API integrations
│   └── insights.py         # Analytics (records, profiles, night tracks)
│
├── static/
│   ├── styles.css          # Complete CSS UI architecture and visual effects
│   └── script.js           # Interactive UI, AJAX (Fetch API), and Plotly integration
│
└── templates/
    └── index.html          # Structural HTML layout for the dashboard engine
```

## 📄License
This project is licensed under the MIT License - feel free to clone, modify and share it!

Developed by Gonçalo Libânio
