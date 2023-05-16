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
paragraph4 = paragraphs[6].strip()
paragraph5 = paragraphs[8].strip()
paragraph6 = paragraphs[9].strip()
paragraph7 = paragraphs[10].strip()
paragraph8 = paragraphs[5].strip()
paragraph9 = paragraphs[7].strip()
paragraph10 = paragraphs[11].strip()
paragraph11 = paragraphs[12].strip()
paragraph12 = paragraphs[13].strip()

container1 = st.container()
# Render the header
container1.title("The Use of Data for Understanding the Video Game Market 🎮📈")
container1.write(paragraph_intro)
container1.write(paragraph_intro2)

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

total_sales = genre_sales.drop('Global_Sales', axis=1)
total_sales = total_sales.drop('Genre', axis=1)

# Create a new table with the sum of sales by column
total_sales = pd.DataFrame(total_sales.sum(), columns=['Total_Sales'])

# Define the dropdown options for regions
region_options = {
    'Global Sales': 'Global_Sales',
    'North America Sales': 'NA_Sales',
    'Europe Sales': 'EU_Sales',
    'Japan Sales': 'JP_Sales',
    'Other Sales': 'Other_Sales'
}

# Create the first dropdown menu for the bar chart
dropdown1 = st.selectbox('Select a region', list(region_options.keys()), index=0)

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
col1, col2 = st.columns((1.2, 1))

with col1:
    # Render the first plot with the bar chart
    st.plotly_chart(fig1, height=600)

with col2:
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write(paragraph2)
    st.write(paragraph3)
    st.write(paragraph8)
    st.write(paragraph4)

st.divider()

st.header("Most Sold Genres until 2016")
st.write(paragraph9)

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

with col5:
    st.plotly_chart(fig3)

col6, col7 = st.columns((5,1))

with col7:
    st.subheader("Total Game Sales by Region")
    st.dataframe(total_sales, width=400)

with col6:
    st.write(paragraph5)
    st.write(paragraph6)
    st.write(paragraph7)

st.divider()

st.header("Best Selling Publishers until 2016")
st.write(paragraph10)

publisher_sales = df.groupby(["Publisher"])[["Global_Sales"]].sum().reset_index()
publisher_sales = publisher_sales.sort_values("Global_Sales", ascending=False).reset_index(drop=True)
publisher_sales = publisher_sales.head(10)

# Create the funnel chart
fig4 = go.Figure(go.Funnel(
    y=publisher_sales["Publisher"],
    x=publisher_sales["Global_Sales"],
    text=publisher_sales["Global_Sales"],
    textinfo="value+percent initial",
    marker=dict(color="#FF00FF"),
    connector=dict(line=dict(color="white", width=2))
))

# Set the chart title and font settings
fig4.update_layout(
    title="Top 10 Publishers by Global Sales until 2016 (in million)"
)

# Customize the layout
fig4.update_layout(
    funnelmode="stack",
    hoverlabel=dict(font_size=12)
)

publisher_sales_regioned = df.groupby(["Publisher"])[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]].sum().reset_index()

publisher_sales_regioned = publisher_sales_regioned.sort_values("Global_Sales", ascending=False).reset_index(drop=True)
publisher_sales_regioned.drop(["Global_Sales"], axis=1, inplace=True)
publisher_sales_regioned = publisher_sales_regioned.head(20)

# Define the dropdown options for regions
region_options3 = {
    'North America Sales': 'NA_Sales',
    'Europe Sales': 'EU_Sales',
    'Other Sales': 'Other_Sales',
    'Japan Sales': 'JP_Sales'
}

col000, col0000 = st.columns((1, 1.1))

dropdown3 = col000.selectbox('Select a region', list(region_options3.keys()), index=3)

fig5 = px.bar(
    publisher_sales_regioned,
    y=region_options3[dropdown3],
    x='Publisher',
    title="Top 20 Publishers by Regional Sales until 2016 (in million)",
    color=region_options3[dropdown3],
    color_continuous_scale="Agsunset"
)

fig5.update_yaxes(title_text=dropdown3)

fig5.update_layout(height=600)

publishergame_sales = df.groupby(["Publisher", "Name"])[["Global_Sales"]].sum().reset_index()
publishergame_sales = publishergame_sales.sort_values("Global_Sales", ascending=False).reset_index(drop=True)

nintendo_sales = publishergame_sales.loc[publishergame_sales['Publisher'] == 'Nintendo']
nintendo_sales = nintendo_sales.head(10).drop(["Publisher"], axis=1)
nintendo_sales.index = range(1, len(nintendo_sales) + 1)

ea_sales = publishergame_sales.loc[publishergame_sales['Publisher'] == 'Electronic Arts']
ea_sales = ea_sales.head(10).drop(["Publisher"], axis=1)
ea_sales.index = range(1, len(ea_sales) + 1)

act_sales = publishergame_sales.loc[publishergame_sales['Publisher'] == 'Activision']
act_sales = act_sales.head(10).drop(["Publisher"], axis=1)
act_sales.index = range(1, len(act_sales) + 1)

sony_sales = publishergame_sales.loc[publishergame_sales['Publisher'] == 'Sony Computer Entertainment']
sony_sales = sony_sales.head(10).drop(["Publisher"], axis=1)
sony_sales.index = range(1, len(sony_sales) + 1)

ubi_sales = publishergame_sales.loc[publishergame_sales['Publisher'] == 'Ubisoft']
ubi_sales = ubi_sales.head(10).drop(["Publisher"], axis=1)
ubi_sales.index = range(1, len(ubi_sales) + 1)

t2_sales = publishergame_sales.loc[publishergame_sales['Publisher'] == 'Take-Two Interactive']
t2_sales = t2_sales.head(10).drop(["Publisher"], axis=1)
t2_sales.index = range(1, len(t2_sales) + 1)

with st.container():
    col8, col9 = st.columns(2)
    col9.plotly_chart(fig4)
    col8.plotly_chart(fig5)
    st.write(paragraph11)
    st.write(paragraph12)
    lcol1, lcol2, lcol3 = st.columns(3)
    lcol4, lcol5, lcol6 = st.columns(3)
    lcol1.write("Nintendo (in million)")
    lcol1.dataframe(nintendo_sales)
    lcol2.write("Electronic Arts (in million)")
    lcol2.dataframe(ea_sales)
    lcol3.write("Activision (in million)")
    lcol3.dataframe(act_sales)
    lcol4.write("Sony Computer Entertainment (in million)")
    lcol4.dataframe(sony_sales)
    lcol5.write("Ubisoft (in million)")
    lcol5.dataframe(ubi_sales)
    lcol6.write("Take-Two Interactive (in million)")
    lcol6.dataframe(t2_sales)

st.divider()
st.header("Content Writer")
st.write("Muhammed Ali Acikgoz: [Github](https://github.com/maliackgoz), [LinkedIn](https://www.linkedin.com/in/muhammedaliacikgoz)")