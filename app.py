import os
import glob
import json
import uuid
import warnings
warnings.filterwarnings('ignore')

# Exclude system paths, virtual environments, library directories, and uploads from the reloader.
# This prevents Werkzeug/Watchdog from triggering restart loops on Windows when standard library files are accessed.
exclude_patterns = [
    '*uploads*',
    '*.venv*',
    '*venv*',
    '*site-packages*',
    '*lib*',
    '*Lib*',
    '*python*',
    '*Python*'
]
separator = ';' if os.name == 'nt' else ':'
os.environ.setdefault('FLASK_RUN_EXCLUDE_PATTERNS', separator.join(exclude_patterns))
os.environ.setdefault('WERKZEUG_RUN_EXCLUDE_PATTERNS', separator.join(exclude_patterns))

from flask import Flask, render_template, request, jsonify, session
from data_processing import load_spotify_data
from sections.eras import eras
from sections.general_view import general_view
from sections.habits import listening_habits
from sections.insights import get_insights

app = Flask(__name__)
app.secret_key = 'spotify_rewind_dashboard_secret_key_prod_fallback'

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# In-memory cache for processed data payloads: session_id -> response_data
DATA_CACHE = {}

@app.route('/')
def index():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template('index.html')

@app.route('/api/session-data', methods=['GET'])
def get_session_data():
    session_id = session.get('session_id')

    if session_id and session_id in DATA_CACHE:
        return jsonify(DATA_CACHE[session_id])
    
    return jsonify({'cached': False}), 200

def process_dataframe_to_payload(df):
    # Generate Data & Figures
    eras_data = eras(df)
    gv_data = general_view(df)
    habits_data = listening_habits(df)
    insights_data = get_insights(df)
    
    return {
        'kpis': {
            'total_min': gv_data['total_min'],
            'unique_songs': gv_data['unique_songs'],
            'top_artist': gv_data['top_artist'],
            'top_artist_time': gv_data['top_artist_time'],
            'skip_percentage': habits_data['skip_percentage'],
            'binge_day': insights_data['binge_day'],
            'binge_hours': insights_data['binge_hours'],
            'binge_artist': insights_data['binge_artist'],
            'ghost_songs': insights_data['ghost_songs'],
            'listener_profile': insights_data['listener_profile'],
        },
        'charts': {
            'eras': json.loads(eras_data['fig_eras'].to_json()),
            'general': json.loads(gv_data['fig_general'].to_json()),
            'rhythm_heat': json.loads(habits_data['fig_rhythm_heat'].to_json()),
            'rhythm_end': json.loads(habits_data['fig_rhythm_end'].to_json())
        }
    }

@app.route('/api/upload', methods=['POST'])
def upload():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    session_id = session['session_id']

    files = request.files.getlist('files')
    if not files:
        return jsonify({'error': 'No files uploaded'}), 400

    user_upload_folder = os.path.join(UPLOAD_FOLDER, session_id)
    os.makedirs(user_upload_folder, exist_ok=True)

    # Clear existing files in user's upload directory
    for file in glob.glob(os.path.join(user_upload_folder, "*.json")):
        try:
            os.remove(file)
        except Exception:
            pass
            
    # Save new files
    for file in files:
        if file.filename.endswith('.json'):
            file.save(os.path.join(user_upload_folder, file.filename))
            
    try:
        df = load_spotify_data(user_upload_folder)
        if df.empty:
             return jsonify({'error': 'No valid Spotify streaming data found in uploaded files'}), 400
             
        # Extract available unique years sorted
        available_years = sorted([str(y) for y in df['ano'].dropna().unique()])
        
        # Build lifetime view
        lifetime_payload = process_dataframe_to_payload(df)
        
        # Build year-by-year views
        by_year_payloads = {}
        for yr in available_years:
            df_year = df[df['ano'] == yr]
            if not df_year.empty:
                try:
                    by_year_payloads[yr] = process_dataframe_to_payload(df_year)
                except Exception:
                    # Fallback if a specific year has too little data for specific sub-charts
                    pass

        response_data = {
            'success': True,
            'years': available_years,
            'lifetime': lifetime_payload,
            'by_year': by_year_payloads
        }
        
        # Cache the processed response
        DATA_CACHE[session_id] = response_data
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clear', methods=['POST'])
def clear():
    session_id = session.get('session_id')
    if session_id:
        # Clear cache
        DATA_CACHE.pop(session_id, None)
        
        # Clear files in user's upload directory
        user_upload_folder = os.path.join(UPLOAD_FOLDER, session_id)
        if os.path.exists(user_upload_folder):
            import shutil
            try:
                shutil.rmtree(user_upload_folder)
            except Exception:
                pass
                
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(
        debug=True,
        port=5000,
        exclude_patterns=[
            '*uploads*',
            '*.venv*',
            '*venv*',
            '*site-packages*',
            '*lib*',
            '*Lib*',
            '*python*',
            '*Python*'
        ]
    )

