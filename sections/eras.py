import pandas as pd
import plotly.express as px
from data_processing import apply_spotify_style

def eras(df_filtered: pd.DataFrame) -> dict:
    artist_counts = df_filtered['master_metadata_album_artist_name'].value_counts()
    top_artist_name = artist_counts.index[0] if not artist_counts.empty else '`N/A`'

    top_10_artists = artist_counts.head(10).reset_index()
    top_10_artists.columns = ['artist', 'plays']
    top_10_artists = top_10_artists.iloc[::-1] 

    fig = px.bar(
        top_10_artists, 
        x='plays', 
        y='artist', 
        orientation='h',
        labels={'plays': 'Total Plays', 'artist': 'Artist'}
    )

    fig.update_traces(marker_color='#DD2A7B') # Pink/Magenta palette for the Eras vibe
    
    fig = apply_spotify_style(fig)

    fig.update_layout(
        # Gives 130 pixels of space so band names don't hit the wall
        margin=dict(t=20, b=40, l=130, r=20),
        autosize=True
    )

    return {
        "fig_eras": fig,
        "top_artists_table": artist_counts.head(10).to_dict(),
        "top_artist": top_artist_name 
    }