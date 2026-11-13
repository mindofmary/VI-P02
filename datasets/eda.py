import pandas as pd

def clean_data(df):

    # Change column type to string for columns: 'track_id', 'track_name' and 5 other columns
    df = df.astype({'track_id': 'string', 'track_name': 'string', 'artist_name': 'string', 'artist_genres': 'string', 'album_id': 'string', 'album_name': 'string', 'album_type': 'string'})

    # Change column type to int64 for columns: 'track_number', 'track_popularity' and 3 other columns
    df = df.astype({'track_number': 'int64', 'track_popularity': 'int64', 'artist_popularity': 'int64', 'artist_followers': 'int64', 'album_total_tracks': 'int64'})

    # Change column type to bool for column: 'explicit'
    df = df.astype({'explicit': 'bool'})

    # Change column type to datetime64[ns] for column: 'album_release_date'
    df = df.astype({'album_release_date': 'datetime64[ns]'})

    # Create release_decade from album_release_date
    df['release_decade'] = (df['album_release_date'].dt.year // 10) * 10

    # Define the function to classify music era
    def classify_music_era(row):
        if row['album_release_date'].year <= 1999:
            return 'vinyl/CD'
        elif 2000 <= row['album_release_date'].year <= 2012:
            return 'downloads'
        elif 2013 <= row['album_release_date'].year <= 2019:
            return 'streaming'
        else:
            return 'short-form'
    # Apply the classification and assign to df
    df['music_era'] = df.apply(classify_music_era, axis=1)
    
    # Classify track duration into categories
    df['duration_category'] = pd.cut(
        df['track_duration_min'],
        bins=[-float('inf'), 1.5, 2.5, 4, float('inf')],
        labels=['interlude', 'short', 'default', 'long']
    )
    # interlude - less than 1,5 min
    # short - between 1,5 and 2,5 min
    # default - between 2,5 and 4 min
    # long - more than 4 min
    return df

# Loaded variable 'df' from URI: c:\Users\maria\OneDrive - dei.uc.pt\Universidade\Mestrado 2025-2027\2º ano 2026-2027\Visualização de Informação\VI-P02\datasets\spotify_data clean.csv
df = pd.read_csv(r'c:\Users\maria\OneDrive - dei.uc.pt\Universidade\Mestrado 2025-2027\2º ano 2026-2027\Visualização de Informação\VI-P02\datasets\spotify_data clean.csv')

df_clean = clean_data(df.copy())
df_clean.head()