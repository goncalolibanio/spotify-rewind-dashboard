import glob
import os
import pandas as pd


required_columns = {"ts", "ms_played", "master_metadata_track_name", "master_metadata_album_artist_name", "reason_end"}
upload_folder = 'uploads'

def load_spotify_data():
    os.makedirs(upload_folder, exist_ok=True)

    json_files = glob.glob(os.path.join(upload_folder, "*.json"))

    if not json_files:
        return pd.DataFrame()
    
    frames = []
    for file in json_files:
        try:
            temp_df = pd.read_json(file)

            if any(col in temp_df.columns for col in required_columns):
                frames.append(temp_df)

        except Exception as e:
            print(f"Error reading file {file}: {e}")
            continue

    if not frames:
        return pd.DataFrame()
    
    df = pd.concat(frames, ignore_index=True)

    if 'ts' in df.columns:
        df['ts'] = pd.to_datetime(df['ts'])

        try:
            df['ts'] = df['ts'].dt.tz_localize('UTC').dt.tz_convert('Europe/Lisbon')
        except TypeError:
            df['ts'] = df['ts'].dt.tz_convert('Europe/Lisbon')
            
        df['ano'] = df['ts'].dt.year.astype(str)
        df['hora'] = df['ts'].dt.hour
        df['dia_num'] = df['ts'].dt.dayofweek
        df['mes'] = df['ts'].dt.strftime("%Y-%m")

    return df


def apply_spotify_style(fig):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#ffffff',
        font_family='Montserrat',
        margin=dict(l=40, r=20, t=40, b=40)
    )

    fig.update_xaxes(showgrid=False, color='#b3b3b3')
    fig.update_yaxes(showgrid=True, gridcolor='#282828', color='#b3b3b3')
    
    return fig