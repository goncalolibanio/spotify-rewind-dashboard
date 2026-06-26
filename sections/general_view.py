import pandas as pd
import plotly.express as px
from data_processing import apply_spotify_style

def general_view(df_filtered):
    #Insights
    total_min = round(df_filtered['ms_played'].sum() / 60000)
    artist_count = df_filtered['master_metadata_album_artist_name'].value_counts()
    top_artist = artist_count.index[0] if not artist_count.empty else 'N/A'
    unique_songs = df_filtered['master_metadata_track_name'].nunique()

    # Calculate Top Artist Duration
    top_artist_ms = 0
    if top_artist != 'N/A':
        top_artist_ms = df_filtered[df_filtered['master_metadata_album_artist_name'] == top_artist]['ms_played'].sum()
    top_artist_min = round(top_artist_ms / 60000)
    
    if top_artist_min < 60:
        top_artist_time = f"{top_artist_min} min"
    else:
        hours = round(top_artist_min / 60, 1)
        if hours.is_integer():
            top_artist_time = f"{int(hours)} hours"
        else:
            top_artist_time = f"{hours} hours"

    #Monthly Evolution
    monthly_df = df_filtered.groupby('mes')['ms_played'].sum().reset_index()
    monthly_df['minutes'] = round(monthly_df['ms_played'] / 60000, 2)
    monthly_df = monthly_df.sort_values('mes')

    fig = px.line(
        monthly_df,
        x = 'mes',
        y = 'minutes',
        labels={'mes': 'Month', 'minutes': 'Minutes Listened'}
    )

    fig.update_traces(
        line_color = '#1DB954',
        line_width = 4,
        marker = dict(size=8, color="#ffffff", symbol='circle')
    )

    fig = apply_spotify_style(fig)

    return {
        'total_min': f"{total_min:.2f}",
        'top_artist': top_artist,
        'top_artist_time': top_artist_time,
        'unique_songs': unique_songs,
        'fig_general': fig
    }