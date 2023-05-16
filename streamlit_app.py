import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Render the Streamlit app first
st.set_page_config(
    page_title="The Use of Data for Understanding the Video Game Market",
    page_icon="🎮",
    layout="wide"
)

# Set the background color and font
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0E1117;
        font-family: 'Helvetica', 'Arial', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Read the paragraphs from a text file
file_path = "Sources/paragraphs.txt"

with open(file_path, "r") as file:
    paragraphs = file.readlines()

paragraph_intro = paragraphs[0].strip()
paragraph_intro2 = paragraphs[1].strip()
paragraph1 = paragraphs[2].strip()
paragraph2 = paragraphs[3].strip()
paragraph3 = paragraphs[4].strip()
paragraph4 = paragraphs[5].strip()
paragraph5 = paragraphs[6].strip()
paragraph6 = paragraphs[7].strip()
paragraph7 = paragraphs[8].strip()

container1 = st.container()
# Render the header
container1.title("The Use of Data for Understanding the Video Game Market 🎮📈")
container1.write(paragraph_intro)
container1.write(paragraph_intro2)

container2 = st.container()
# Render section: Most Popular Games
st.header("Most Sold Games until 2016")
st.write(paragraph1)
st.info("You can change between regions by using the dropdowns.")

# Load the dataset
df = pd.read_csv("Sources/Datasets/Video_Games_Sales_as_at_22_Dec_2016.csv")
# Create a new dataframe with sales data grouped by game and region
sales_df = df.groupby(["Name"])[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]].sum().reset_index()
# Filter the dataframe based on global sales
sales_df = sales_df[sales_df['Global_Sales'] >= 10]
# Sort the dataframe by global sales in descending order
sales_df = sales_df.sort_values("Global_Sales", ascending=False).reset_index(drop=True)

# Create a new dataframe with sales data grouped by genre and region
genre_sales = df.groupby(["Genre"])[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]].sum().reset_index()
genre_sales = genre_sales.sort_values("Global_Sales", ascending=False).reset_index(drop=True)

# Define the dropdown options for regions
region_options = {
    'Global Sales': 'Global_Sales',
    'North America Sales': 'NA_Sales',
    'Europe Sales': 'EU_Sales',
    'Japan Sales': 'JP_Sales',
    'Other Sales': 'Other_Sales'
}

# Create the first dropdown menu for the bar chart
dropdown1 = st.selectbox('Select a region', list(region_options.keys()), index=1)

# Create the initial bar chart with fading colors
fig1 = px.bar(
    sales_df,
    y=region_options[dropdown1],
    x='Name',
    title="Most Sold Video Games until 2016 (in million)",
    color=region_options[dropdown1],
    color_continuous_scale="Viridis"
)

# Update the y-axis label based on the selected region
fig1.update_yaxes(title_text=dropdown1)

fig1.update_layout(height=600)

# Create a layout for the plots
col1, col2, col3 = st.columns(3)

with col1:
    # Render the first plot with the bar chart
    st.plotly_chart(fig1, height=600)

with col3:
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write(paragraph2)
    st.write(paragraph3)
    st.write("Japan is embracing its own culture and cultural products. In that case, a game can be developed based on newly popularized concepts within their culture.")
    st.write(paragraph4)

st.divider()

st.header("Most Sold Genres until 2016")
st.write("Now, we will be searching for the most sold genres in different regions. There are two figures below. The one on the left is demonstrating which genres are most popular regionally, and the one on the right side is demonstrating [GDP per capita](https://www.worldometers.info/gdp/gdp-by-country/) for those regions.")

# Define the dropdown2 options for regions
region_options2 = {
    'North America Sales': 'NA_Sales',
    'Europe Sales': 'EU_Sales',
    'Japan Sales': 'JP_Sales',
    'Other Sales': 'Other_Sales'
}

col0, col00 = st.columns(2)

with col0:
    # Create the second dropdown menu for the bar chart
    dropdown2 = st.selectbox('Select a region', list(region_options2.keys()), index=2)


# Create the scatter plot with fading colors to demonstrate Genres
fig2 = px.scatter(
    genre_sales,
    x="Genre",
    y=region_options2[dropdown2],
    size="Global_Sales",
    title="Most Sold Video Game Genres until 2016 (in million)",
    color="Global_Sales"
)

# Update the scatter plot based on the selected region
fig2.update_traces(
    marker=dict(line=dict(width=0.5, color='darkgray')),
    hovertemplate='<b>Genre</b>: %{x}<br><b>Sales</b>: %{y:.2f} million<br><b>Global Sales</b>: %{marker.size:.2f} million<br><extra></extra>'
)

fig2.update_yaxes(title_text=dropdown2)

# Define the color scale for fading
fig2.update_layout(coloraxis=dict(colorscale='Bluered'))

gdp_df = pd.read_csv("Sources/Datasets/GDP_by_Country_2017.csv")
gdp_df = gdp_df.drop(["Index"], axis=1)
gdp_df = gdp_df[["Country", "GDP_pc"]].head(30)

# Set GPD_pc column to sort the df by it
gdp_df["GDP_pc"] = gdp_df["GDP_pc"].map(lambda x: x.lstrip('$'))
gdp_df["GDP_pc"] = gdp_df["GDP_pc"].str.replace(',', '')
gdp_df["GDP_pc"] = gdp_df["GDP_pc"].astype(float)

gdp_df = gdp_df.sort_values(by=["GDP_pc"], ascending=False).reset_index().drop(["index"], axis=1)

# Manual input of regions since the df did not have it
region = ["EU", "EU", "NA", "EU", "Others", "EU", "EU", "NA", "EU", "EU", "Others", "EU", "EU", "Japan", "EU", "Others", "EU", "Others", "Others", "EU", "Others", "Others", "Others", "NA", "Others", "Others", "Others", "Others", "Others", "Others"]
gdp_df["Region"] = region

# Sort the DataFrame by GDP per capita
gdp_df_sorted = gdp_df.sort_values('GDP_pc', ascending=False)

# Define a custom color palette for dark background
custom_colors = ['#58C9B9', '#FF5858', '#FFCA3A', '#9E66AB']

# Create the scatter plot
fig3 = px.scatter(
    gdp_df_sorted, x="Country", y="GDP_pc", color="Region", hover_name="Country",
    labels={"GDP_pc": "GDP per capita"}, title="GDP per Capita (current US$) by Country - 2017",
    category_orders={"Country": gdp_df_sorted['Country']},
    color_discrete_sequence=custom_colors
)

# Update marker size
fig3.update_traces(marker=dict(size=12))


# Create a layout for the plots
col4, col5 = st.columns(2)

with col4:
    # Display the scatter plot
    st.plotly_chart(fig2)
    st.write(paragraph5)

with col5:
    st.plotly_chart(fig3)
    st.write(paragraph6)
    
st.write(paragraph7)

st.divider()

st.header("Best Selling Studios until 2016")
st.write("Moreover, we will be searching for the best selling studios and their sales in different regions in the two figures below.")

studio_sales = df.groupby(["Publisher"])[["Global_Sales"]].sum().reset_index()
studio_sales = studio_sales.sort_values("Global_Sales", ascending=False).reset_index(drop=True)
studio_sales = studio_sales.head(10)

# Create the funnel chart
fig4 = go.Figure(go.Funnel(
    y=studio_sales["Publisher"],
    x=studio_sales["Global_Sales"],
    text=studio_sales["Global_Sales"],
    textinfo="value+percent initial",
    marker=dict(color="#FF00FF"),
    connector=dict(line=dict(color="white", width=2))
))

# Set the chart title and font settings
fig4.update_layout(
    title="Top 10 Studios by Global Sales (in million)"
)

# Customize the layout
fig4.update_layout(
    funnelmode="stack",
    hoverlabel=dict(font_size=12)
)

studio_sales_regioned = df.groupby(["Publisher"])[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]].sum().reset_index()

studio_sales_regioned = studio_sales_regioned.sort_values("Global_Sales", ascending=False).reset_index(drop=True)
studio_sales_regioned.drop(["Global_Sales"], axis=1, inplace=True)
studio_sales_regioned = studio_sales_regioned.head(20)

# Define the dropdown options for regions
region_options3 = {
    'North America Sales': 'NA_Sales',
    'Europe Sales': 'EU_Sales',
    'Japan Sales': 'JP_Sales',
    'Other Sales': 'Other_Sales'
}

st.plotly_chart(fig4)

dropdown3 = st.selectbox('Select a region', list(region_options3.keys()), index=3)

fig5 = px.bar(
    studio_sales_regioned,
    y=region_options3[dropdown3],
    x='Publisher',
    title="Top 20 Studios by Regional Sales (in million)",
    color=region_options3[dropdown3],
    color_continuous_scale="Agsunset"
)

fig5.update_yaxes(title_text=dropdown3)

fig5.update_layout(height=600)

st.plotly_chart(fig5)