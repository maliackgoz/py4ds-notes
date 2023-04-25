import dash
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objs as go
import numpy as np
import pandas as pd

paragraph_intro = "The use of Big Data in the video game industry has become increasingly important in recent years. With the rise of digital distribution and online gaming, companies have access to vast amounts of data on player behavior and preferences. By analyzing this data, companies can gain insights into player engagement, identify trends, and develop targeted marketing strategies. Additionally, data analysis can be used to inform game design decisions, leading to more engaging and successful games. This has resulted in a shift towards a data-driven approach to game development and marketing. In this context, the use of Big Data has the potential to revolutionize the video game industry and shape the future of gaming."
paragraph1 = "I had trouble finding a free dataset for Türkiye, so I decided to focus my project on analyzing global, Europe, North America, and Japan sales, using a dataset I already had. I may explore Türkiye in the future, but for now, not having access to the right dataset could hinder my project's success. If companies face similar issues, they may need to create their own datasets for specific needs."
paragraph2 = "If I had access to a Türkiye dataset, I planned to analyze the correlation between the country's economy and the popularity of certain video games globally, but not in Türkiye. For example, I wanted to explore why the Zelda series, popular globally, is not as popular in Türkiye due to limited Nintendo console users."
paragraph3 = "The dataset I selected combines sales and scores, allowing me to conduct regionalized analyses, important for my project's goals. This saves me time from merging separate datasets, making it beneficial to my project."

paragraph4 = "Firstly, we can see what the most popular games are for some regions that have global sales greater than 10 million. (You can change between regions by using the dropdown.)"
paragraph5 = "We can see that, except from Japan and Other countries, Wii Sports is the most sold game. So, why is that? Let's take a look."
paragraph6 = "In Japan, Pokémon has a massive following and has been a cultural phenomenon for over two decades. This popularity is likely due to the franchise's origins in Japan and its ability to appeal to a wide audience, including children and adults. In contrast, Wii Sports may not have had the same cultural relevance in Japan, despite its success in other regions."
paragraph7 = "As for the Other countries (such as Middle East), Grand Theft Auto (GTA) is popular because of its open-world gameplay and its ability to allow players to experience a world that they may not be able to in real life. Additionally, the series' gritty and mature themes, which include crime and violence, may appeal to some audiences in the region. Wii Sports, on the other hand, may not have the same level of appeal due to its family-friendly nature and lack of mature themes."

paragraph8 = "Furthermore, let's take a look at the most popular games, which have global sales greater than $25 million. (You can change between regions by using the dropdown.)"

df = pd.read_csv("Assignments\Assignment2\Video_Games_Sales_as_at_22_Dec_2016.csv")

# create a new dataframe with sales data grouped by game and region
sales_df = df.groupby(["Name"])[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]].sum().reset_index()

# create a mask for rows where Global_Sales is lower than 10 (millions)
mask = sales_df['Global_Sales'] < 10

# drop rows where mask is True
sales_df = sales_df.drop(sales_df[mask].index).reset_index()
sales_df = sales_df.drop("index", axis=1)

sales_df = sales_df.sort_values("Global_Sales", ascending=False).reset_index(drop=True)

# create a dictionary to map sales regions to column names
region_cols = {
    'NA': 'NA_Sales',
    'EU': 'EU_Sales',
    'JP': 'JP_Sales',
    'Other': 'Other_Sales',
    'Global': 'Global_Sales'
}

# create the first dropdown menu for the bar chart
dropdown1 = dcc.Dropdown(
    id='region-dropdown1',
    options=[{'label': region, 'value': region_cols[region]} for region in region_cols.keys()],
    value='EU_Sales'
)

# create the second dropdown menu for the pie chart
dropdown2 = dcc.Dropdown(
    id='region-dropdown2',
    options=[{'label': region, 'value': region_cols[region]} for region in region_cols.keys()],
    value='NA_Sales'
)

# create the initial plot with a bar trace for EU sales
fig1 = px.bar(
    sales_df,
    y='EU_Sales',
    x='Name',
    title="Most Sold Video Games until 2016 (larger than 10 millions) - Sales by Game",
    hover_data=[sales_df['Global_Sales']],
    labels={'EU_Sales': 'Sales (million)', 'Global_Sales': 'Global Sales (million)'},
)


# create a new dataframe with sales data grouped by game and region
sales_df2 = df.groupby(["Name"])[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]].sum().reset_index()

mask = sales_df2['Global_Sales'] < 20

# select rows where mask is True using loc
sales_df2 = sales_df2.loc[~mask].reset_index(drop=True)

sales_df2 = sales_df2.sort_values("Global_Sales", ascending=False).reset_index(drop=True)


# create the second plot with a pie chart
fig2 = px.pie(
    sales_df2,
    names='Name',
    values='EU_Sales',
    title="Most Sold Video Games until 2016 (larger than 20 millions) - Sales by Game",
    hover_data=[sales_df2['Global_Sales']],
    labels={'EU_Sales': 'Sales (million)', 'Global_Sales': 'Global Sales (million)'},
)

# Define the external stylesheet
external_stylesheets = ['https://fonts.googleapis.com/css?family=Roboto']

# create the layout for the dashboard
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Define the colors
colors = {
    'background': '#ffffff',
    "header": "#636efa",
    'text': '#0f1012'
}

# Define the layout
app.layout = html.Div(style={'backgroundColor': colors['background'],'fontFamily': 'Roboto'}, children=[
    html.H1("The Use of Big Data for Understanding the Video Game Market", style={'color': colors['header']}),
    html.P(paragraph_intro, style={'color': colors['text']}),
    html.H2("Finding the Dataset", style={'color': colors['header']}),
    html.P(paragraph1, style={'color': colors['text']}),
    html.P(paragraph2, style={'color': colors['text']}),
    html.P(paragraph3, style={'color': colors['text']}),
    html.H2("Most Popular (Sold) Games Until 2016", style={'color': colors['header']}),
    html.P(paragraph4, style={'color': colors['text']}),
    html.Div([
        html.Div([
            dcc.Graph(id='sales-graph', figure=fig1, style={'height': '400px'}),
            dropdown1
        ], className='six columns'),
        html.P(paragraph5, style={'color': colors['text']}),
        html.P(paragraph6, style={'color': colors['text']}),
        html.P(paragraph7, style={'color': colors['text']}),
        html.P(paragraph8, style={'color': colors['text']}),
        html.Div([
            dcc.Graph(id='pie-chart', figure=fig2),
            dropdown2
        ], className='six columns')
    ], className='row'),
])


# define the callback function for the first dropdown
@app.callback(
    dash.dependencies.Output('sales-graph', 'figure'),
    [dash.dependencies.Input('region-dropdown1', 'value')])
def update_sales_graph1(region):
    # update the bar chart with the selected region
    fig = px.bar(
        sales_df,
        y=region,
        x='Name',
        title="Most Sold Video Games until 2016 (larger than 10 millions) - Sales by Game",
        hover_data=[sales_df['Global_Sales']],
        labels={region: 'Sales (million)', 'Global_Sales': 'Global Sales (million)'},
    )
    return fig

# define the callback function for the second dropdown
@app.callback(
    dash.dependencies.Output('pie-chart', 'figure'),
    [dash.dependencies.Input('region-dropdown2', 'value')])
def update_sales_graph2(region):
    # update the pie chart with the selected region
    fig = px.pie(
        sales_df2,
        names='Name',
        values=region,
        title="Most Sold Video Games until 2016 (larger than 20 millions) - Sales by Game",
        hover_data=[sales_df2['Global_Sales']],
        labels={region: 'Sales (million)', 'Global_Sales': 'Global Sales (million)'},
    )
    return fig

# run the dashboard
if __name__ == '__main__':
    app.run_server(debug=True)