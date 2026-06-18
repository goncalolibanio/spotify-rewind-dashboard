import pandas as pd
import plotly.express as px
from data_processing import apply_spotify_style

def listening_habits(df_filtered):
    days_map = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 
    3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'
    }
    df_filtered['day_name'] = df_filtered['dia_num'].map(days_map)

    heatmap_df = df_filtered.groupby(['day_name', 'hora']).size().reset_index(name='count')
    
    fig_rhythm = px.density_heatmap(
        heatmap_df, 
        x='hora', 
        y='day_name', 
        z='count',  # A cor vai depender da contagem
        category_orders={'day_name': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']},
        labels={'hora': 'Hour of the Day', 'day_name': 'Day of the Week', 'count': 'Songs Listened'},
        color_continuous_scale=['#181818', '#1DB954', '#00f2fe']
    )
    
    fig_rhythm = apply_spotify_style(fig_rhythm)
    
    fig_rhythm.update_layout(
        coloraxis_colorbar=dict(
            title="Songs Listened",
            orientation="h",      
            yanchor="top",
            y=-0.22,              
            xanchor="center",
            x=0.5
        ),
        margin=dict(t=20, b=80, l=80, r=40),
        autosize=True,
        xaxis=dict(tickmode='linear', tick0=0, dtick=1)
        )

    fig_rhythm.update_xaxes(
        tickmode='linear',
        tick0=0,
        dtick=1,            
        range=[-0.5, 23.5], 
        fixedrange=True     
    )

    fig_rhythm.update_yaxes(fixedrange=True)

    #DONUT CHART
    ending_counts = df_filtered['reason_end'].value_counts().reset_index()
    ending_counts.columns = ['reason', 'count']
    
    total_ends = ending_counts['count'].sum()
    skips = ending_counts[ending_counts['reason'] == 'fwdbtn']['count'].sum()
    skip_percentage = round((skips / total_ends) * 100) if total_ends > 0 else 0

    display_labels = {
        'fwdbtn': 'Skipped',
        'trackdone': 'Completed',
        'backbtn': 'Previous'
    }

    ending_counts['reason'] = ending_counts['reason'].map(lambda x: display_labels.get(x, 'Others'))

    ending_counts = ending_counts.groupby('reason')['count'].sum().reset_index()
    ending_counts = ending_counts.sort_values(by='count', ascending=False)

    fig_pie = px.pie(
        ending_counts, 
        values='count', 
        names='reason', 
        hole=0.6,
        color_discrete_sequence=['#1DB954', '#fe8c00', '#388bfd', '#666666'] # Cinza para "Others"
    )

    fig_pie = apply_spotify_style(fig_pie)
    fig_pie.update_traces(textposition='inside', textinfo='percent')

    fig_pie.update_layout(
        margin=dict(t=30, b=30, l=30, r=100), 
        height=280,
        legend=dict(
            orientation="v",        
            yanchor="middle",
            y=0.5,                  
            xanchor="left",
            x=1.02                  
        ),
        autosize=True
    )
    

    return {
        "fig_rhythm_heat": fig_rhythm,
        "fig_rhythm_end": fig_pie,
        "skip_percentage": skip_percentage
    }