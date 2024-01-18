import DataExtracting as DE
import DataProcessing as DP
import DataVisualisation as DV

import pandas as pd
import streamlit as st

### ---------- Sampling - Already Done ---------- ###
# def extract_sample()
  # # read full file
  # df_2020 = DE.read_data("full_2020.csv")
  # df_2019 = DE.read_data("full_2019.csv")

  # # extract sample
  # sample_2019 = DE.extract_sample(df_2019, 0.03)
  # sample_2020 = DE.extract_sample(df_2020, 0.05)

  # # extract columns
  # cols = ['id_mutation', 'date_mutation', 'nature_mutation','valeur_fonciere',
  #         'code_departement', 'type_local', 'surface_terrain', 'longitude', 'latitude']
  # extract_2019 = DE.extract_columns(sample_2019, cols)
  # extract_2020 = DE.extract_columns(sample_2020, cols)

  # # save
  # cleaned_2019 = extract_2019.copy()
  # cleaned_2020 = extract_2020.copy()
  # DE.save_data(cleaned_2019, "cleaned_extracted_sample_2019.csv")
  # DE.save_data(cleaned_2019, "cleaned_extracted_sample_2020.csv")
### --------------- End Sampling --------------- ###

@st.cache
def preparing():
  # read
  df_2020 = DE.read_data("cleaned_extracted_sample_2020.csv")
  df_2019 = DE.read_data("cleaned_extracted_sample_2019.csv")

  # clean
  DP.cleaning(df_2019)
  DP.cleaning(df_2020)

  # enrich
  DP.enriching(df_2019)
  DP.enriching(df_2020)

  # return
  return df_2019, df_2020

def see_used_data():
  st.write('Choose year:')
  # choose year
  year_2019 = st.checkbox('2019', value=True)
  year_2020 = st.checkbox('2020', value=False)
  # dropdown
  dropdown = st.expander('Click to see used data')
  with dropdown:
    if year_2019 and year_2020:
      st.dataframe(data = pd.concat([df_2019, df_2020]))
    elif year_2019:
      st.dataframe(data = df_2019)
    elif year_2020:
      st.dataframe(data = df_2020)

def visual_nature_mutation():
  # year radio
  year = st.radio("Which year", ('2019', '2020'), key = 'nature_mutation')
  # dataviz
  if year == '2019':
    DV.pie_nature_mutation(df_2019, "2019")
    DV.scatter_price_m2_by_nature_mutation(df_2019, "2019")
  elif year == '2020':
    DV.pie_nature_mutation(df_2020, "2020")
    DV.scatter_price_m2_by_nature_mutation(df_2020, "2020")

def visual_type_local():
  # year radio
  year = st.radio("Which year", ('2019', '2020'), key = 'type_local')
  # dataviz
  if year == '2019':
    DV.pie_type_local(df_2019, "2019")
    DV.scatter_price_m2_by_type_local(df_2019, "2019")
  elif year == '2020':
    DV.pie_type_local(df_2020, "2020")
    DV.scatter_price_m2_by_type_local(df_2020, "2020")

def visual_month():
  # month slider
  start, end = st.select_slider('Select month range',
                                options = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                                value = ('Jan', 'Dec'))
  # selected data
  dict_month = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
  mask1 = df_2019['month_mutation'] <= dict_month[end]
  mask2 = df_2019['month_mutation'] >= dict_month[start]
  mask3 = df_2020['month_mutation'] <= dict_month[end]
  mask4 = df_2020['month_mutation'] >= dict_month[start]
  selected_2019 = df_2019[mask1 & mask2]
  selected_2020 = df_2020[mask3 & mask4]
  # dataviz hist
  DV.hist_nb_mutations_by_month(selected_2019, selected_2020)
  # dataviz line
  DV.line_price_m2_by_month(selected_2019, selected_2020)

def visual_department():
  # dataviz
  DV.bar_nb_mutations_by_department(df_2019, df_2020)
  DV.scater_price_m2_by_department(df_2019, df_2020)

def visual_map():
  # department text input
  department = st.text_input('Enter ONE department code', placeholder = 'Ex: 75')
  # Department Code Reference
  department_code_ref = df_2019[['code_departement', 'nom_commune']]
  dropdown = st.expander('Department Code Reference')
  with dropdown:
      st.dataframe(data = department_code_ref)
  # building type multiselect
  building_type = st.multiselect('Choose building type',
                                  ['Maison', 'Appartement'], # choices
                                  ['Maison', 'Appartement']) # default
  # price slider
  # max_price = max(df_2019.prix_m2_terrain.max().item(), df_2020.prix_m2_terrain.max().item())
  start, end = st.slider('Select price range',
                          0.0, 60000.0, # range
                          (0.0, 60000.0), # default
                          step = 100.0)
  # masks
  mask1 = df_2019['prix_m2_terrain'] >= start
  mask2 = df_2019['prix_m2_terrain'] <= end
  mask3 = df_2019['type_local'] == 'Maison'
  mask4 = df_2019['type_local'] == 'Appartement'
  mask5 = df_2019['code_departement'] == department

  mask6 = df_2020['prix_m2_terrain'] >= start
  mask7 = df_2020['prix_m2_terrain'] <= end
  mask8 = df_2020['type_local'] == 'Maison'
  mask9 = df_2020['type_local'] == 'Appartement'
  mask10 = df_2019['code_departement'] == department

  # selected data
  selected_2019 = df_2019.copy()
  selected_2020 = df_2020.copy()

  # validate department
  if department == '':
    pass
  elif department in df_2019.code_departement.unique().tolist() or department in df_2020.code_departement.unique().tolist():
    selected_2019 = selected_2019[mask5]
    selected_2020 = selected_2020[mask10]
  else:
    st.error('Department not found! Please try again!',  icon = "🚨")

  # validate building type
  if building_type == 'Maison' :
    selected_2019 = selected_2019[mask3]
    selected_2020 = selected_2020[mask8]
  elif building_type == 'Appartement':
    selected_2019 = selected_2019[mask4]
    selected_2020 = selected_2020[mask9]
  else:
    selected_2019 = selected_2019[mask3 | mask4]
    selected_2020 = selected_2020[mask8 | mask9]
  
  # selected data
  selected_2019 = selected_2019[mask1 & mask2]
  selected_2020 = selected_2020[mask6 & mask7]

  location_2019 = selected_2019[['longitude', 'latitude']]
  location_2020 = selected_2020[['longitude', 'latitude']]
  locations = pd.concat([location_2019, location_2020])

  # dataviz
  DV.map(locations)

# ------------------------------------ #
# --------------- Main --------------- #
# ------------------------------------ #

if __name__ == '__main__':
  # prepare
  df_2019, df_2020 = preparing()
  
  # title and header
  st.title('Estate Value Analytics of 2019 et 2020')

  # dropdown used data
  st.subheader('Used Data')
  see_used_data()

  # mutation nature - count and price per square meter
  st.subheader('Mutation Nature - Count and Price per Square Meter')
  visual_nature_mutation()

  # bulding type - count and price per square meter
  st.subheader('Building Type - Count and Price per Square Meter')
  visual_type_local()

  # month analysis
  st.subheader('Number of Mutations by Month')
  visual_month()

  # department - count and price per square meter
  st.subheader('Department - Count and Price per Square Meter')
  visual_department()

  # map
  st.subheader('Map - Multi-filter')
  visual_map()