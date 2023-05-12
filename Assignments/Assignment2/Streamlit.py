import streamlit as st
import pandas as pd
import plotly.express as px

# Render the Streamlit app first
st.set_page_config(
    page_title="The Use of Big Data for Understanding the Video Game Market",
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

file_path = "Assignments/Assignment2/paragraphs.txt"  # Replace with the actual file path

with open(file_path, "r") as file:
    paragraphs = file.readlines()

paragraph_intro = paragraphs[0].strip()
paragraph1 = paragraphs[1].strip()
paragraph2 = paragraphs[2].strip()
paragraph3 = paragraphs[3].strip()
paragraph4 = paragraphs[4].strip()
paragraph5 = paragraphs[5].strip()
paragraph6 = paragraphs[6].strip()
paragraph7 = paragraphs[7].strip()
paragraph8 = paragraphs[8].strip()
paragraph9 = paragraphs[9].strip()
paragraph10 = paragraphs[10].strip()


# Render the header with an emoji
st.title("The Use of Big Data for Understanding the Video Game Market 🎮📈")
st.write(paragraph_intro)
st.write("Let's dive into the data.")

# Render section: Most Popular (Sold) Games
st.header("Most Popular (Sold) Games")
st.write(paragraph4)
st.info("You can change between regions by using the dropdown.")

# Load the dataset
df = pd.read_csv("Assignments/Assignment2/Video_Games_Sales_as_at_22_Dec_2016.csv")

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
    title="Most Sold Video Games until 2016 (larger than 10 million) - Sales by Game",
    labels={region_options[dropdown1]: 'Sales (million)'},
    color=region_options[dropdown1],
    color_continuous_scale="Viridis"
)

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
    st.write(paragraph5)
    st.write(paragraph6)
    st.write("Japan is embracing its own culture and cultural products. In that case, a game can be developed based on newly popularized concepts within their culture.")
    st.write(paragraph7)

st.header("Most Popular (Sold) Genres")
st.write("Now, we will look for the most popular genres in different regions.")
st.info("You can change between regions by using the dropdown.")

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

fig2 = px.scatter(
    genre_sales,
    x="Genre",
    y=region_options2[dropdown2],
    size="Global_Sales",
    title="Most Sold Video Game Genres until 2016 - Sales by Genre",
    color="Global_Sales",
    labels={'y': 'Sales (million)'}
)

# Update the scatter plot based on the selected region
fig2.update_traces(
    marker=dict(line=dict(width=0.5, color='darkgray')),
    hovertemplate='<b>Genre</b>: %{x}<br><b>Sales</b>: %{y:.2f} million<br><b>Global Sales</b>: %{marker.size:.2f} million<br><extra></extra>'
)

# Define the color scale for fading
fig2.update_layout(coloraxis=dict(colorscale='Bluered'))

gdp_df = pd.read_csv("Assignments/Assignment2/GDP_by_Country_2017.csv")
gdp_df = gdp_df.drop(["Index"], axis=1)
gdp_df = gdp_df[["Country", "GDP_pc"]].head(30)

gdp_df["GDP_pc"] = gdp_df["GDP_pc"].map(lambda x: x.lstrip('$'))
gdp_df["GDP_pc"] = gdp_df["GDP_pc"].str.replace(',', '')
gdp_df["GDP_pc"] = gdp_df["GDP_pc"].astype(float)

gdp_df = gdp_df.sort_values(by=["GDP_pc"], ascending=False).reset_index().drop(["index"], axis=1)

region = ["EU", "EU", "NA", "EU", "Others", "EU", "EU", "Others", "EU", "EU", "Others", "EU", "EU", "Japan", "EU", "Others", "EU", "Others", "Others", "EU", "Others", "Others", "Others", "Others", "Others", "Others", "Others", "Others", "Others", "Others"]
gdp_df["Region"] = region


# Create scatter plot
fig3 = px.scatter(
    gdp_df, x="Country", y="GDP_pc", color="Region", hover_name="Country",
    labels={"GDP_pc": "GDP per capita"}, title="GDP per Capita by Country - 2017 (https://www.worldometers.info/gdp/gdp-by-country/)"
)

# Update color scale
fig3.update_traces(marker=dict(size=12))


# Create a layout for the plots
col4, col5 = st.columns(2)

with col4:
    # Display the scatter plot
    st.plotly_chart(fig2)
    st.write(paragraph8)

with col5:
    st.plotly_chart(fig3)
    st.write(paragraph9)
    
st.write(paragraph10)