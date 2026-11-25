import pandas as pd



def clean_data(df):
    # verificar tipos e converter colunas para tipos apropriados
    df = df.astype({'track_id': 'string', 'track_name': 'string', 'artist_name': 'string', 'artist_genres': 'string', 'album_id': 'string', 'album_name': 'string', 'album_type': 'string'})
    df = df.astype({'track_number': 'int64', 'track_popularity': 'int64', 'artist_popularity': 'int64', 'artist_followers': 'int64', 'album_total_tracks': 'int64'})
    df = df.astype({'explicit': 'bool'})
    df = df.astype({'album_release_date': 'datetime64[ns]'})

    #nova variável release_decade
    df['release_decade'] = (df['album_release_date'].dt.year // 10) * 10

    #classificar música por era
    def classify_music_era(row):
        if row['album_release_date'].year <= 1980:
            return 'vinyl'
        elif 1981 <= row['album_release_date'].year <= 1999:
            return 'cassette'
        elif 2000 <= row['album_release_date'].year <= 2012:
            return 'CD'
        elif 2013 <= row['album_release_date'].year <= 2019:
            return 'downloads'
        else:
            return 'streaming'

    df['music_era'] = df.apply(classify_music_era, axis=1)
    
    #categorias de duração das músicas
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

#resultados
df= pd.read_csv('datasets/spotify_data clean.csv')
df_clean = clean_data(df.copy())
df_clean.head()