# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
from plotly.graph_objects import Layout

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

#options=[{'label': 'All Sites', 'value': 'ALL'},{'label': 'site1', 'value': 'site1'}, ...]
dropdown_opt = []
dropdown_opt.append({'label': 'All Sites', 'value': 'ALL'})
for ls in spacex_df['Launch Site'].unique():
    linha = dict()
    linha['label'] = ls
    linha['value'] = ls
    dropdown_opt.append(linha)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', options=dropdown_opt, value='ALL',
                                        placeholder='Select a Launch Site here', searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                       2500: '2500',5000: '5000',7500: '7500',10000: '10000'},
                                                value=[min_payload, max_payload]),


                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df = spacex_df.copy()
        names = 'Launch Site'
        title = 'Total Success Launchs by Site'
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]['class']
        names = 'class'
        title = 'Total Success Launchs for site {}'.format(entered_site)
    fig = px.pie(filtered_df, names=names, title=title)
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
                  Input(component_id="payload-slider", component_property="value")])
def plot_scatter(entered_site, entered_payload):
    if entered_site == 'ALL':
        filtered_df = spacex_df.copy()
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]

    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= entered_payload[0]) & 
                    (filtered_df['Payload Mass (kg)'] <= entered_payload[1])]
    fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class",color="Booster Version Category")
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()


"""
Which site has the largest successful launches?
KSC LC-39A
Which site has the highest launch success rate?
VAFB SLC-4E e KSC LC-39A
Which payload range(s) has the highest launch success rate?
Between 2k and 4k 
Which payload range(s) has the lowest launch success rate?
Between 6k and 10k
Which F9 Booster version (v1.0, v1.1, FT, B4, B5, etc.) has the highest launch success rate?
FT
"""
