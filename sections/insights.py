import pandas as pd

def get_insights(df_filtered):
    if df_filtered.empty:
        return {
            "binge_day": "N/A",
            "binge_hours": 0,
            "binge_artist": "N/A",
            "ghost_songs": 0,
            "listener_profile": "N/A"
        }
    
    df_filtered['date_only'] = df_filtered['ts'].dt.date
    day_records = df_filtered.groupby('date_only')['ms_played'].sum()

    if not day_records.empty:
        max_day = day_records.idxmax()
        max_hours = round(day_records.max() / 3600000, 1) # ms to hr
        
        top_day_df = df_filtered[df_filtered['date_only'] == max_day]
        day_artists = top_day_df['master_metadata_album_artist_name'].value_counts()
        binge_artist = day_artists.index[0] if not day_artists.empty else "N/A"
        binge_day_str = max_day.strftime('%B %d, %Y') # Formato: "December 14, 2024"
    else:
        binge_day_str, max_hours, binge_artist = "N/A", 0, "N/A"

    ghost_songs = df_filtered[df_filtered['hora'].between(0, 5)].shape[0]

    ending_counts = df_filtered['reason_end'].value_counts()
    total_ends = ending_counts.sum()
    skips = ending_counts.get('fwdbtn', 0)
    skip_percentage = (skips / total_ends) * 100 if total_ends > 0 else 0
    
    if skip_percentage < 15:
        listener_profile = "The Devoted Listener"
    elif skip_percentage <= 40:
        listener_profile = "The Balanced Curator"
    else:
        listener_profile = "The Impatient DJ"
        
    return {
        "binge_day": binge_day_str,
        "binge_hours": max_hours,
        "binge_artist": binge_artist,
        "ghost_songs": f"{ghost_songs:,}",
        "listener_profile": listener_profile
    }