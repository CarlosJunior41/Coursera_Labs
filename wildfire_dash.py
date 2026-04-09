import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update
import datetime as dt
#Create app
app = dash.Dash('dash_wildfire')
# Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True
# Read the wildfire data into pandas dataframe
df =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv')
#Extract year and month from the date column
df['Month'] = pd.to_datetime(df['Date']).dt.month_name() #used for the names of the months
df['Year'] = pd.to_datetime(df['Date']).dt.year
#Layout Section of Dash
#Task 2.1 Add the Title to the Dashboard
app.layout = html.Div(children=[ html.H1('Australia Wildfire Dashboard', 
                                style={'textAlign': 'center', 'color': '#503D36', 'font-size': 30}),
                                html.Div([html.H2('Select Region:', style={'margin-right': '2em'}),
                                dcc.RadioItems(['NSW','QL','SA','TA','VI','WA'], 'NSW', id='region',inline=True)]),
                                html.Div([ html.H2('Select Year:', style={'margin-right': '2em'}),
                                dcc.Dropdown(df.Year.unique(), value = 2005,id='year') ]),   
                                html.Div([
                                        html.Div(dcc.Graph(id='plot1')),
                                        html.Div(dcc.Graph(id='plot2'))
                                ], style={'display': 'flex'}),])

                                                  
#Place to add @app.callback Decorator
@app.callback([Output(component_id='plot1', component_property='figure'),
               Output(component_id='plot2', component_property='figure')],
               [Input(component_id='region', component_property='value'),
                Input(component_id='year', component_property='value')])
   
#Place to define the callback function .
def reg_year_display(region,year):
    #data
    region_data = df[df['Region'] == region]
    y_r_data = region_data[region_data['Year']==year]
    #Plot one - Monthly Average Estimated Fire Area
    est_data = y_r_data.groupby('Month')['Estimated_fire_area'].mean().reset_index()
    plot1 = px.pie(est_data, values='Estimated_fire_area', names='Month', title="{} : Monthly Average Estimated Fire Area in year {}".format(region,year))
    #Plot two - Monthly Average Count of Pixels for Presumed Vegetation Fires
    veg_data = y_r_data.groupby('Month')['Count'].mean().reset_index()
    plot2 = px.bar(veg_data, x='Month', y='Count', title='{} : Average Count of Pixels for Presumed Vegetation Fires in year {}'.format(region,year))
    return [plot1, plot2]

if __name__ == '__main__':
    app.run()
