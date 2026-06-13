import pandas as pd
import plotly.express as px
from data_processing import apply_spotify_style
import base64
import requests

SPOTIFY_CLIENT_ID = ""
SPOTIFY_CLIENT_SECRET = ""

def get_spotify_artist_imagem(artist_name):
    if not SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_ID == "O_TEU_CLIENT_ID":
        return None
    
    try:
        auth_url = "https://accounts.spotify.com/api/token"
        auth_bytes = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode("utf-8")
        auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")
        
        auth_headers = {"Authorization": f"Basic {auth_base64}"}
        auth_data = {"grant_type": "client_credentials"}
        
        token_response = requests.post(auth_url, headers=auth_headers, data=auth_data, timeout=5)
        access_token = token_response.json().get("access_token")
        
        if not access_token:
            return None
        
        search_url = "https://api.spotify.com/v1/search"
        search_headers = {"Authorization": f"Bearer {access_token}"}
        search_params = {"q": artist_name, "type": "artist", "limit": 1}
        
        search_response = requests.get(search_url, headers=search_headers, params=search_params, timeout=5)
        search_data = search_response.json()
        
        artists_found = search_data.get("artists", {}).get("items", [])
        if artists_found:
            images = artists_found[0].get("images", [])
            if images:
                # Retorna a primeira imagem (que é sempre a de maior resolução)
                return images[0].get("url")
                
    except Exception as e:
        print(f"[API Spotify] Erro ao procurar imagem para {artist_name}: {e}")
        
    return None

def eras(df_filtered):
    artist_counts = df_filtered['master_metadata_album_artist_name'].value_counts()

    top_artist_name = artist_counts.index[0] if not artist_counts.empty else 'N/A'
    top_artist_image_url = get_spotify_artist_imagem(top_artist_name)

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

    fig.update_layout(
        # Dá 130 píxeis de espaço para os nomes das bandas não baterem na parede
        margin=dict(t=20, b=40, l=130, r=20),
        autosize=True
    )

    fig.update_traces(marker_color='#DD2A7B') # Pink/Magenta palette for the Eras vibe
    fig = apply_spotify_style(fig)

    chart_html = fig.to_html(full_html=False, include_plotlyjs='cdn', config={'responsive': True})

    return {
        "chart_eras": chart_html,
        "top_artists_table": artist_counts.head(10).to_dict(),
        "top_artist_image": top_artist_image_url
    }
    