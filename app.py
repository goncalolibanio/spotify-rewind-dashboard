import os
import glob
import json
import uuid
import warnings
warnings.filterwarnings('ignore')

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
             
        # Generate Data & Figures
        eras_data = eras(df)
        gv_data = general_view(df)
        habits_data = listening_habits(df)
        insights_data = get_insights(df)
        
        # Structure the payload
        response_data = {
            'success': True,
            'kpis': {
                'total_min': gv_data['total_min'],
                'unique_songs': gv_data['unique_songs'],
                'top_artist': gv_data['top_artist'],
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
        
        # Cache the processed response
        DATA_CACHE[session_id] = response_data
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
