import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# def pie_nature_mutation(df, year):
#   count_nature_mutation = pd.DataFrame(df['nature_mutation'].value_counts()).reset_index()
#   fig = px.pie(count_nature_mutation, values='nature_mutation', names='index',
#               title='Nature of Mutation Counts - ' + year,
#               labels={'index':'Nature','nature_mutation':'Count'},
#               color_discrete_sequence=px.colors.sequential.RdBu)
#   st.plotly_chart(fig)

def pie_nature_mutation(df, year):
  count_nature_mutation = df['nature_mutation'].value_counts().reset_index()
  count_nature_mutation.columns = ['index', 'nature_mutation']  # Rename columns
  fig = px.pie(count_nature_mutation, values='nature_mutation', names='index',
              title='Nature of Mutation Counts - ' + year,
              labels={'index':'Nature', 'nature_mutation':'Count'},
              color_discrete_sequence=px.colors.sequential.RdBu)
  st.plotly_chart(fig)

def scatter_price_m2_by_nature_mutation(df, year):
  # mean prix_m2_terrain by nature_mutation
  mask = df['prix_m2_terrain'] >= 0
  mean_price = df[mask].groupby(['nature_mutation']).prix_m2_terrain.mean().to_frame().reset_index()

  # scatter
  fig = go.Figure()
  fig.add_trace(go.Scatter(x = mean_price.nature_mutation,
                          y = mean_price.prix_m2_terrain,
                          mode = 'lines+markers', name = 'lines+markers',
                          line_color = '#8C0C18'))
  fig.update_layout(title_text = 'Average Full-land Price per Square Meter by Nature of Mutation - ' + year,
                    xaxis_title = 'Nature',
                    yaxis_title = 'Price in EUR')
  st.plotly_chart(fig)

# def pie_type_local(df, year):
#   count_type_local = pd.DataFrame(df['type_local'].value_counts()).reset_index()
#   count_type_local['index'].replace(['-1'], 'Unknown', inplace=True)
#   fig = px.pie(count_type_local, values='type_local', names='index',
#               title='Building Type Counts - ' + year,
#               labels={'index':'Type','type_local':'Count'},
#               color_discrete_sequence=px.colors.sequential.Viridis)
#   st.plotly_chart(fig)

def pie_type_local(df, year):
    count_type_local = df['type_local'].value_counts().reset_index()
    count_type_local.columns = ['index', 'type_local']
    count_type_local['index'].replace(['-1'], 'Unknown', inplace=True)
    fig = px.pie(count_type_local, values='type_local', names='index',
                 title='Building Type Counts - ' + year,
                 labels={'index': 'Type', 'type_local': 'Count'},
                 color_discrete_sequence=px.colors.sequential.Viridis)
    st.plotly_chart(fig)

def scatter_price_m2_by_type_local(df, year):
  # mean prix_m2_terrain by type_local 2019
  mask = df['prix_m2_terrain'] >= 0
  mean_price = df[mask].groupby(['type_local']).prix_m2_terrain.mean()
  mean_price = mean_price.to_frame().reset_index()
  mean_price['type_local'].replace(['-1'], 'Unknown', inplace=True)

  # scatter - prix_m2_terrain by nature_mutation 2019
  fig = go.Figure()
  fig.add_trace(go.Scatter(x = mean_price.type_local,
                          y = mean_price.prix_m2_terrain,
                          mode = 'lines+markers', name = 'lines+markers',
                          line_color = '#2F9FAF'))
  fig.update_layout(title_text = 'Average Full-land Price per Square Meter by Building Type - ' + year,
                    xaxis_title = 'Type',
                    yaxis_title = 'Price in EUR')
  st.plotly_chart(fig)

def hist_nb_mutations_by_month(df1, df2):
  fig = go.Figure()
  fig.add_trace(go.Histogram(x = df1['month_mutation'], name = '2019', marker_color = 'lightsalmon'))
  fig.add_trace(go.Histogram(x = df2['month_mutation'], name = '2020', marker_color = 'rebeccapurple'))
  fig.update_layout(title_text = 'Mutation Count per Month', 
                    xaxis_title = 'Month',
                    yaxis_title = 'Number of Mutations')
  st.plotly_chart(fig)

def line_price_m2_by_month(df1, df2):
  # mean prix_m2_terrain by month_mutation
  mean_price_2019 = df1.groupby(['month_mutation']).prix_m2_terrain.mean().to_frame().reset_index()
  mean_price_2020 = df2.groupby(['month_mutation']).prix_m2_terrain.mean().to_frame().reset_index()
  mean_price = pd.merge(mean_price_2019, mean_price_2020,
                        on = 'month_mutation',
                        suffixes = ('_2019','_2020'))

  # line - prix_m2_terrain by month_mutation
  st.line_chart(data = mean_price,
                x = 'month_mutation', y = None,
                use_container_width = True)
    
def bar_nb_mutations_by_department(df1, df2):
  # count id_mutation by code_departement
  count_mutations_2019 = df1.groupby(['code_departement']).id_mutation.size().to_frame().reset_index()
  count_mutations_2020 = df2.groupby(['code_departement']).id_mutation.size().to_frame().reset_index()

  # bar - count id_mutation by code_departement
  fig = go.Figure(data = [
                  go.Bar(name = '2019',
                        x = count_mutations_2019['code_departement'],
                        y = count_mutations_2019['id_mutation']),
                  go.Bar(name = '2020',
                        x = count_mutations_2020['code_departement'],
                        y = count_mutations_2020['id_mutation'])])
  fig.update_layout(title_text = 'Mutation Count by Department', 
                    xaxis_title = 'Department',
                    yaxis_title = 'Number of Mutations')
  st.plotly_chart(fig)

def scater_price_m2_by_department(df1, df2):
  # prix_m2_terrain by code_departement
  price_2019 = df1[['code_departement', 'prix_m2_terrain']]
  price_2020 = df2[['code_departement', 'prix_m2_terrain']]
  price = pd.concat([price_2019, price_2020])
  mask = price['prix_m2_terrain'] >= 0
  mean_price = price[mask].groupby(['code_departement']).prix_m2_terrain.mean().to_frame().reset_index()

  # scatter - prix_m2_terrain by code_departement
  fig = go.Figure()
  fig.add_trace(go.Scatter(x = mean_price.code_departement,
                          y = mean_price.prix_m2_terrain,
                          mode = 'lines+markers', name = 'lines+markers',
                          line_color = '#4AD0E3'))
  fig.update_layout(title_text = 'Average Full-land Price per Square Meter by Department',
                    xaxis_title = 'Department',
                    yaxis_title = 'Price in EUR')
  st.plotly_chart(fig)

def map(df):
  st.map(df, zoom = 2, use_container_width = True)