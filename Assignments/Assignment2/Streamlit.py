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

paragraph_intro = "The use of Big Data in the video game industry has become increasingly important in recent years. With the rise of digital distribution and online gaming, companies have access to vast amounts of data on player behavior and preferences. By analyzing this data, companies can gain insights into player engagement, identify trends, and develop targeted marketing strategies. Additionally, data analysis can be used to inform game design decisions, leading to more engaging and successful games. This has resulted in a shift towards a data-driven approach to game development and marketing. In this context, the use of Big Data has the potential to revolutionize the video game industry and shape the future of gaming."

paragraph1 = "I had trouble finding a free dataset for Türkiye, so I decided to focus my project on analyzing global, Europe, North America, and Japan sales, using a dataset I already had. I may explore Türkiye in the future, but for now, not having access to the right dataset could hinder my project's success. If companies face similar issues, they may need to create their own datasets for specific needs."
paragraph2 = "If I had access to a Türkiye dataset, I planned to analyze the correlation between the country's economy and the popularity of certain video games globally, but not in Türkiye. For example, I wanted to explore why the Zelda series, popular globally, is not as popular in Türkiye due to limited Nintendo console users."
paragraph3 = "The dataset I selected combines sales and scores, allowing me to conduct regionalized analyses, important for my project's goals. This saves me time from merging separate datasets, making it beneficial to my project."

paragraph4 = "Firstly, we can see what the most popular games are for some regions that have global sales greater than 10 million. (You can change between regions by using the dropdown.)"

paragraph5 = "We can see that, except from Japan and Other countries, Wii Sports is the most sold game. So, why is that? Let's take a look."
paragraph6 = "In Japan, Pokémon has a massive following and has been a cultural phenomenon for over two decades. This popularity is likely due to the franchise's origins in Japan and its ability to appeal to a wide audience, including children and adults. In contrast, Wii Sports may not have had the same cultural relevance in Japan, despite its success in other regions."
paragraph7 = "As for the Other countries (such as Middle East), Grand Theft Auto (GTA) is popular because of its open-world gameplay and its ability to allow players to experience a world that they may not be able to in real life. Additionally, the series' gritty and mature themes, which include crime and violence, may appeal to some audiences in the region."


# Render the header with an emoji
st.title("The Use of Big Data for Understanding the Video Game Market 🎮📈")
st.write(paragraph_intro)
st.write("Let's dive into the data.")

# Render section: Most Popular (Sold) Games Until 2016
st.header("Most Popular (Sold) Games Until 2016")
st.write(paragraph4)

# Load the dataset
df = pd.read_csv("Assignments/Assignment2/Video_Games_Sales_as_at_22_Dec_2016.csv")

# Create a new dataframe with sales data grouped by game and region
sales_df = df.groupby(["Name"])[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]].sum().reset_index()

# Filter the dataframe based on global sales
sales_df = sales_df[sales_df['Global_Sales'] >= 10]

# Sort the dataframe by global sales in descending order
sales_df = sales_df.sort_values("Global_Sales", ascending=False).reset_index(drop=True)

# Define the dropdown options for regions
region_options = {
    'Global Sales': 'Global_Sales',
    'NA Sales': 'NA_Sales',
    'EU Sales': 'EU_Sales',
    'JP Sales': 'JP_Sales',
    'Other Sales': 'Other_Sales'
}

# Create the first dropdown menu for the bar chart
dropdown1 = st.selectbox('Select a region', list(region_options.keys()), index=1)

# Create the initial bar chart
fig1 = px.bar(
    sales_df,
    y=region_options[dropdown1],
    x='Name',
    title="Most Sold Video Games until 2016 (larger than 10 million) - Sales by Game",
    labels={region_options[dropdown1]: 'Sales (million)', 'Global_Sales': 'Global Sales (million)'}
)

# Create a layout for the plots
col1, col2, col3 = st.columns(3)

with col1:
    # Render the first plot with the bar chart
    st.plotly_chart(fig1)

with col3:
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write(paragraph5)
    st.write(paragraph6)
    st.write("Japan is embracing its own culture. In that case, a game can be developed based on newly popularized concepts within their culture.")

st.write(paragraph7)