import glob
import os
import pandas as pd


required_columns = {"ts", "ms_played", "master_metadata_track_name", "master_metadata_album_artist_name", "reason_end"}
upload_folder = 'uploads'

def load_spotify_data(folder_path=upload_folder):
    os.makedirs(folder_path, exist_ok=True)

    json_files = glob.glob(os.path.join(folder_path, "*.json"))

    if not json_files:
        return pd.DataFrame()
    
    frames = []
    for file in json_files:
        try:
            temp_df = pd.read_json(file)
            if temp_df.empty:
                continue

            # Standard format mapping
            standard_mapping = {
                "endTime": "ts",
                "artistName": "master_metadata_album_artist_name",
                "trackName": "master_metadata_track_name",
                "msPlayed": "ms_played"
            }
            
            # Check if it has standard columns
            has_standard = all(col in temp_df.columns for col in ["endTime", "artistName", "trackName", "msPlayed"])
            # Check if it has extended columns
            has_extended = any(col in temp_df.columns for col in {"ts", "ms_played", "master_metadata_track_name", "master_metadata_album_artist_name"})

            if has_standard:
                temp_df = temp_df.rename(columns=standard_mapping)
                if "reason_end" not in temp_df.columns:
                    temp_df["reason_end"] = "trackdone"
                frames.append(temp_df)

            elif has_extended:
                # Rename standard columns to extended format if there's a mix
                for old_col, new_col in standard_mapping.items():
                    if old_col in temp_df.columns and new_col not in temp_df.columns:
                        temp_df = temp_df.rename(columns={old_col: new_col})
                if "reason_end" not in temp_df.columns:
                    temp_df["reason_end"] = "trackdone"
                frames.append(temp_df)

        except Exception as e:
            print(f"Error reading file {file}: {e}")
            continue

    if not frames:
        return pd.DataFrame()
    
    df = pd.concat(frames, ignore_index=True)

    # Normalize missing columns to prevent KeyErrors later
    for col in required_columns:
        if col not in df.columns:
            df[col] = None

    if 'ts' in df.columns:
        df['ts'] = pd.to_datetime(df['ts'], errors='coerce')
        
        # Drop rows with invalid/missing timestamps
        df = df.dropna(subset=['ts'])
        if df.empty:
            return df

        try:
            # If the timestamp has no timezone info, localize it first to UTC
            if df['ts'].dt.tz is None:
                df['ts'] = df['ts'].dt.tz_localize('UTC')
            df['ts'] = df['ts'].dt.tz_convert('Europe/Lisbon')
            
        except Exception:
            try:
                df['ts'] = df['ts'].dt.tz_convert('Europe/Lisbon')
            except Exception:
                pass
            
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
        font_family='Inter, sans-serif',
        margin=dict(l=40, r=20, t=40, b=40)
    )

    fig.update_xaxes(showgrid=False, color='#b3b3b3')
    fig.update_yaxes(showgrid=True, gridcolor='#282828', color='#b3b3b3')
    
    return fig