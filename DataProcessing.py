import pandas as pd

def cleaning(df):
  df['date_mutation'] = pd.to_datetime(df['date_mutation'])
  df['nombre_pieces_principales'] = df['nombre_pieces_principales'].fillna(-1).astype(int)
  df[['valeur_fonciere', 'surface_terrain', 'longitude', 'latitude']] = df[['valeur_fonciere', 'surface_terrain', 'longitude', 'latitude']].fillna(-1)

  df['type_local'] = df['type_local'].astype(str)
  df['type_local'].mask(df['type_local'] == 'nan', "-1", inplace=True)

def enriching(df):
  df['prix_m2_terrain'] = df['valeur_fonciere']/df['surface_terrain']
  df['prix_m2_terrain'].mask(df['prix_m2_terrain'] < 0, -1, inplace=True)

  df['month_mutation'] = df['date_mutation'].map(get_month)

def get_month(dt):
  return dt.month