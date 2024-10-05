import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_option_menu import option_menu  # Import the option menu
from scipy.stats import pearsonr  # For calculating correlation

# Set the title and description, and collapse the sidebar initially
st.set_page_config(page_title="Video Game Sales", layout="wide", initial_sidebar_state="collapsed")

# Load the dataset
@st.cache_data
def load_data():
    data = pd.read_csv("videogamesales.csv")
    return data

data = load_data()

# Mapping for the region select box (user-friendly name to dataset column name)
region_mapping = {
    "Global Sales": "Global_Sales",
    "NA Sales": "NA_Sales",
    "EU Sales": "EU_Sales",
    "JP Sales": "JP_Sales",
    "Other Sales": "Other_Sales"
}

with st.sidebar:
    
    selected = option_menu(
        menu_title="Liberty Walk",  # Title of the menu
        options=["Introduction & Statistics", "Sales by Platform", "Sales by Genre", "Sales Comparison", "Sales Over Time", "Histogram", "Box Plot", "Conclusion"],  
        icons=["grid"],  # Icons for each option
        menu_icon="cast",  # Icon of the menu
        default_index=0,  # Default selected option
        orientation="vertical"  # Show the menu in the sidebar (vertical orientation)
    )
    st.write("Team Members")
    image_path = "members.png" 
    st.image(image_path, use_column_width=True)
   
    


# Function to calculate and display metrics with dynamic insights
def show_metrics(selected_region):

    # Get the relevant sales column based on the selected region
    sales_data = data[region_mapping[selected_region]]
    
    # Calculate the metrics
    mean_sales = sales_data.mean()
    median_sales = sales_data.median()
    mode_sales = sales_data.mode().values[0]  # Most frequent value
    std_sales = sales_data.std()
    var_sales = sales_data.var()
    min_sales = sales_data.min()
    max_sales = sales_data.max()
    range_sales = max_sales - min_sales
    percentiles = np.percentile(sales_data, [25, 50, 75])

    # Skewness (asymmetry in the data distribution)
    skewness = sales_data.skew()

    # Interquartile Range (IQR) to detect potential outliers
    Q1 = np.percentile(sales_data, 25)
    Q3 = np.percentile(sales_data, 75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Identify potential outliers
    outliers = sales_data[(sales_data < lower_bound) | (sales_data > upper_bound)]

    # Display the metrics using Streamlit's metric component, arranged horizontally
    st.subheader(f"📈 {selected_region} Statistics")
    
    # First row
    col1, col2, col3 = st.columns(3)
    col1.metric("Mean", f"{mean_sales:.2f} M")
    col2.metric("Median", f"{median_sales:.2f} M")
    col3.metric("Mode", f"{mode_sales:.2f} M")
    
    # Second row
    col1, col2, col3 = st.columns(3)
    col1.metric("Standard Deviation", f"{std_sales:.2f} M")
    col2.metric("Variance", f"{var_sales:.2f} M")
    col3.metric("Range", f"{range_sales:.2f} M")
    
    # Third row
    col1, col2, col3 = st.columns(3)
    col1.metric("Min", f"{min_sales:.2f} M")
    col2.metric("Max", f"{max_sales:.2f} M")
    col3.metric("25th Percentile", f"{percentiles[0]:.2f} M")
    
    # Fourth row
    col1, col2, col3 = st.columns(3)
    col1.metric("50th Percentile (Median)", f"{percentiles[1]:.2f} M")
    col2.metric("75th Percentile", f"{percentiles[2]:.2f} M")

    # Dynamic Insights Section
    st.subheader("🔍 Insights")

    # 1. Spread Insights
    if std_sales > 1:
        st.write(f"The spread of sales in {selected_region} is quite wide with a standard deviation of {std_sales:.2f} million units, indicating significant variability across the data.")
    else:
        st.write(f"The sales in {selected_region} are relatively consistent, with a standard deviation of {std_sales:.2f} million units, suggesting limited variation.")

    # 2. Skewness Insights
    if skewness > 0:
        st.write(f"The distribution of sales in {selected_region} is positively skewed (skewness: {skewness:.2f}), meaning there are more low sales values and a few high-value outliers.")
    elif skewness < 0:
        st.write(f"The distribution of sales in {selected_region} is negatively skewed (skewness: {skewness:.2f}), indicating a concentration of higher sales with some lower-value outliers.")
    else:
        st.write(f"The sales in {selected_region} are symmetrically distributed, with a skewness close to 0.")

    # 3. Outliers Insights
    if not outliers.empty:
        st.write(f"There are **{len(outliers)} potential outliers** in the sales data for {selected_region}, suggesting a few games have sales far outside the normal range. These games either performed exceptionally well or poorly.")
    else:
        st.write(f"No significant outliers detected in the sales data for {selected_region}, indicating the majority of the sales fall within the expected range.")

    # 4. Percentiles Insights
    st.write(f"The interquartile range (IQR) for sales in {selected_region} is {IQR:.2f} million units. This shows the middle 50% of the games' sales are distributed across this range, giving an idea of the typical performance range for games.")



# Function to display introduction and dataset overview
def show_intro_and_overview():
    # Display the main title only in this section
    st.title("🎮 Video Game Sales")
    
    # Limit the width of the introduction using a container or columns
    intro_container = st.container()
    
    with intro_container:
        # Create a fixed width for the introduction text
        intro_col1, _ = st.columns([2, 1])  # 2:1 ratio to limit the width
        
        with intro_col1:
            # Introduction section
            st.header("Introduction")
            st.write("""
            The dataset provided contains information on video game sales across different regions (**North America, Europe, Japan, and other regions**), 
            as well as global sales figures. Each record in the dataset represents a video game, along with attributes such as the **platform**, **genre**, 
            **publisher**, **release year**, and corresponding **sales figures**. 

            The dataset's primary objective is to **track sales performance** and understand the **distribution and relationships** between sales data 
            across different regions. This Streamlit application presents a variety of visualizations to explore the sales data and trends.
            """)
    
    # Create two columns: one for the dataset and one for metrics
    col1, col2 = st.columns([2, 1])  # 3:1 ratio for dataset and metrics
    
    with col1:
        # Display dataset overview (Show all rows in a scrollable format)
        st.subheader("Dataset Overview")
        st.dataframe(data)  # Show all rows in a scrollable dataframe
        st.write("Dataset Source: [Video Game Sales Dataset](https://www.kaggle.com/datasets/sidtwr/videogames-sales-dataset?select=Video_Games_Sales_as_at_22_Dec_2016.csv&classId=09460dc7-d15d-4ba5-b6d3-785da7a59bae&assignmentId=67bb0923-5499-4710-92d1-a69d91fe07b2&submissionId=12339343-d9ce-f9bb-4a76-dc964765a9ff)")
    
    with col2:

        
        # Add selectbox for region selection beside the metrics
        region_selection = st.selectbox(
            "Choose a region for statistics:",
            ["Global Sales", "NA Sales", "EU Sales", "JP Sales", "Other Sales"]
        )
        
        # Show metrics (descriptive statistics)
        show_metrics(region_selection)

# Function to display the Sales Over Time Line Chart
def sales_over_time_chart():
    st.title("Sales Over Time")
    
    # Allow the user to select a region
    selected_region = st.selectbox("Select a region for sales over time:", list(region_mapping.keys()))
    
    # Ensure the data has the release year and selected region's sales
    if 'Year' not in data.columns or data['Year'].isnull().all():
        st.warning("No 'Year' data available in the dataset.")
        return
    
    # Filter out rows where Year or Sales data is missing
    filtered_data = data[['Year', region_mapping[selected_region]]].dropna()

    # Create the line chart using Plotly
    fig_line = px.line(
        filtered_data,
        x='Year',
        y=region_mapping[selected_region],
        labels={'Year': 'Year', region_mapping[selected_region]: 'Sales (in millions)'},
        title=f"Sales Over Time for {selected_region}"
    )

    # Display the line chart
    st.plotly_chart(fig_line, use_container_width=True)

    # Add a dynamic description based on sales trends
    sales_trend = filtered_data[region_mapping[selected_region]].diff().mean()

    # Dynamic trend description based on sales data
    if sales_trend > 0:
        st.write(f"""
        Sales in {selected_region} show an **increasing trend** over time, indicating growing market demand or rising popularity 
        of video games in this region. This upward trend suggests that the gaming industry is becoming more lucrative in {selected_region},
        and could be driven by various factors such as increased console adoption, broader access to games, or a shift in gaming preferences.
        This trend might also indicate expanding purchasing power or higher engagement from gamers in this region.
        """)
    elif sales_trend < 0:
        st.write(f"""
        Sales in {selected_region} show a **decreasing trend** over time, indicating a potential decline in the gaming market in this region.
        This could suggest that the gaming industry is maturing or even shrinking in {selected_region}, possibly due to market saturation, 
        reduced consumer interest, or competition from other entertainment sources. It's also possible that other regions are overtaking 
        {selected_region} in terms of gaming revenue, or that particular gaming platforms or genres are losing traction here.
        """)
    else:
        st.write(f"""
        Sales in {selected_region} have remained **relatively stable** over time, indicating consistent performance in the gaming market.
        This stability could suggest that while there may not be significant growth, there is also no major decline, pointing to a steady 
        and reliable consumer base in {selected_region}. This could indicate that gaming has become a regular form of entertainment here, 
        with consumers making predictable purchasing decisions over the years.
        """)


# Data preparation for pie chart
platform_sales = data.groupby('Platform')['Global_Sales'].sum().reset_index()

# Customized Pie Chart Function (Sales by Region)
def pie_chart():
    # Create a column layout with a limited width for the selectbox
    select_col, _ = st.columns([1, 3])  # 1:3 ratio to limit the width of the selectbox

    with select_col:
        # Add selectbox for region selection
        region_selection = st.selectbox(
            "Choose a region for the pie chart:",
            ["Global Sales", "NA Sales", "EU Sales", "JP Sales", "Other Sales"]
        )

    # Mapping for the region to the actual column name in the dataset
    region_mapping = {
        "Global Sales": "Global_Sales",
        "NA Sales": "NA_Sales",
        "EU Sales": "EU_Sales",
        "JP Sales": "JP_Sales",
        "Other Sales": "Other_Sales"
    }

    # Get the selected region's sales column
    selected_sales_column = region_mapping[region_selection]

    # Group the data by Platform for the selected region's sales
    region_sales = data.groupby('Platform')[selected_sales_column].sum().reset_index()

    # Display the pie chart title using st.title (this replaces the main title)
    st.title(f"{region_selection} Distribution by Platform")

    # Custom color palette (optional)
    custom_colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', 
                     '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']
    
    # Create the pie chart with customizations
    fig_pie = px.pie(region_sales, names='Platform', values=selected_sales_column,
                     color_discrete_sequence=custom_colors)  # Custom color sequence

    # Customize the appearance
    fig_pie.update_traces(textposition='inside', textinfo='percent+label', 
                          hoverinfo='label+percent+value', 
                          hole=0.4)  # Makes it a donut chart (hole=0.4)

    # Customize the layout: title, legend position, size, etc.
    fig_pie.update_layout(
        width=700,  # Adjust the width of the pie chart
        height=700,  # Adjust the height of the pie chart
        legend_title_text='Platform',  # Legend title
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)  # Position the legend below the chart
    )

    # Find the platform with the highest and lowest sales for the selected region
    top_platform = region_sales.loc[region_sales[selected_sales_column].idxmax()]
    lowest_platform = region_sales.loc[region_sales[selected_sales_column].idxmin()]

    # Create two columns: one for the pie chart and one for the description
    col1, col2 = st.columns([2, 1])  # 2:1 ratio for pie chart and description
    
    with col1:
        # Display the pie chart
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Display a brief bullet-point description beside the pie chart
        st.write(f"""
        - **{top_platform['Platform']}** is the leading platform with over **{top_platform[selected_sales_column]:.2f} million units** sold in this region.
        - The platform with the **lowest sales** in this region is **{lowest_platform['Platform']}**, with **{lowest_platform[selected_sales_column]:.2f} million units** sold.
        - Other platforms, such as the Nintendo DS, Xbox 360, and PS3, also contribute significantly, with sales ranging from moderate to high.
        - However, some platforms, such as the GBA and PSP, represent smaller portions of the market.
        - This chart highlights the clear dominance of **{top_platform['Platform']}**, showcasing its immense popularity in the {region_selection} region.
        """)

# Function for displaying a Histogram
def histogram_chart():
    st.title("Sales Distribution (Histogram)")

    # Allow the user to select a region
    selected_region = st.selectbox("Select a region for the histogram:", list(region_mapping.keys()))

    # Filter the relevant data for the selected region
    sales_data = data[region_mapping[selected_region]].dropna()

    # Create a histogram
    fig_histogram = px.histogram(
        sales_data,
        nbins=30,  # Number of bins
        labels={region_mapping[selected_region]: f"{selected_region} Sales"},
        title=f"{selected_region} Sales Distribution",
    )

    # Customize the layout for the histogram
    fig_histogram.update_layout(
        xaxis_title=f"{selected_region} Sales (in millions)",
        yaxis_title="Frequency",
        bargap=0.2
    )

    # Display the histogram
    st.plotly_chart(fig_histogram, use_container_width=True)

    # Calculate key statistics for dynamic explanation
    mean_sales = sales_data.mean()
    median_sales = sales_data.median()
    std_sales = sales_data.std()
    skewness = sales_data.skew()

    # Mean and Median explanation
    if mean_sales > median_sales:
        st.write(f"""
        The sales distribution in {selected_region} is **positively skewed**. 
        The mean sales ({mean_sales:.2f} million units) is higher than the median sales ({median_sales:.2f} million units), 
        indicating that while most games sell at or below the median value, there are some games with very high sales, pulling the average up.
        """)
    elif mean_sales < median_sales:
        st.write(f"""
        The sales distribution in {selected_region} is **negatively skewed**. 
        The mean sales ({mean_sales:.2f} million units) is lower than the median sales ({median_sales:.2f} million units), 
        suggesting that most games in this region sell at or above the median value, but there are some games with very low sales that pull the average down.
        """)
    else:
        st.write(f"""
        The sales distribution in {selected_region} is **symmetrical**, with the mean sales ({mean_sales:.2f} million units) 
        and median sales ({median_sales:.2f} million units) being roughly the same. This indicates a balanced distribution of sales 
        around the average, where most games perform similarly.
        """)

    # Spread (Standard Deviation) explanation
    st.write(f"""
    The standard deviation of sales is {std_sales:.2f} million units, indicating that the spread of sales values is {'high' if std_sales > 1 else 'low'}. 
    A higher spread suggests that there is a significant variation in how different games perform in {selected_region}. 
    Conversely, a lower spread would indicate that most games have similar sales figures, reflecting a more uniform market.
    """)

    # Skewness explanation
    if skewness > 0:
        st.write(f"The distribution is **positively skewed** with a skewness of {skewness:.2f}, meaning that there are a few games with extremely high sales.")
    elif skewness < 0:
        st.write(f"The distribution is **negatively skewed** with a skewness of {skewness:.2f}, meaning that there are a few games with very low sales compared to the rest.")
    else:
        st.write(f"The distribution has **no skew** with a skewness of {skewness:.2f}, indicating a relatively symmetrical distribution of sales.")

    # Final explanation based on the shape of the distribution
    st.write(f"""
    This histogram provides insights into how video games sell in {selected_region}. A positively skewed distribution with a high standard deviation 
    might suggest that a few top-performing games dominate the market, while most other games sell significantly less. 
    On the other hand, a lower standard deviation or a symmetrical distribution could indicate a more evenly distributed market where games perform consistently.
    """)


# Function for displaying a Box Plot
def box_plot_chart():
    st.title("Sales Comparison (Box Plot)")

    # Select multiple regions for comparison
    selected_regions = st.multiselect(
        "Select regions to compare:",
        list(region_mapping.keys()),
        default=["Global Sales", "NA Sales", "EU Sales"]  # Default selections
    )

    # Prepare the data for box plot by melting the DataFrame
    box_data = data[["Global_Sales", "NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]].dropna()
    melted_data = pd.melt(box_data, var_name="Region", value_name="Sales")

    # Create the box plot
    fig_box = px.box(
        melted_data[melted_data["Region"].isin([region_mapping[r] for r in selected_regions])],
        x="Region",
        y="Sales",
        title="Sales Comparison across Regions",
        labels={"Region": "Sales Region", "Sales": "Sales (in millions)"}
    )

    # Display the box plot
    st.plotly_chart(fig_box, use_container_width=True)

    # Dynamic description of the box plot
    st.subheader("Insights into Sales Comparison")

    # Loop over the selected regions to give insights for each one
    for region in selected_regions:
        region_sales = data[region_mapping[region]].dropna()
        median_sales = region_sales.median()
        iqr_sales = region_sales.quantile(0.75) - region_sales.quantile(0.25)  # Interquartile range
        min_sales = region_sales.min()
        max_sales = region_sales.max()
        outliers = len(region_sales[(region_sales < (region_sales.quantile(0.25) - 1.5 * iqr_sales)) | 
                                    (region_sales > (region_sales.quantile(0.75) + 1.5 * iqr_sales))])

        # Dynamic explanation for each region
        st.write(f"### {region} Sales Insights")
        st.write(f"""
        The median sales for {region} is **{median_sales:.2f} million units**, indicating that half of the games sold more than this amount, 
        while the other half sold less. The **interquartile range (IQR)**, which represents the middle 50% of sales, is **{iqr_sales:.2f} million units**, 
        suggesting that the sales data for most games are concentrated within this range.
        """)

        # Outliers explanation
        if outliers > 0:
            st.write(f"""
            There are **{outliers} outliers** in the {region} sales data. These are games that either significantly underperformed or overperformed 
            compared to the rest of the market. Outliers can be seen as points that fall outside the whiskers of the box plot, and their presence 
            suggests that a few games stand out with either very low or very high sales in this region.
            """)
        else:
            st.write(f"There are no significant outliers in the {region} sales data, indicating a relatively consistent distribution of sales across games.")

        # Spread explanation
        if iqr_sales > 1:
            st.write(f"""
            The spread of sales in {region} is quite **wide**, with an interquartile range of {iqr_sales:.2f} million units. This suggests that 
            games in this region have varied performance, with some selling significantly better than others.
            """)
        else:
            st.write(f"""
            The spread of sales in {region} is relatively **narrow**, with an interquartile range of {iqr_sales:.2f} million units. 
            This indicates that most games in {region} tend to perform similarly, with fewer extremes in sales.
            """)

        # Range explanation
        st.write(f"""
        The sales range in {region} extends from a minimum of {min_sales:.2f} million units to a maximum of {max_sales:.2f} million units, 
        showing the complete variation in game sales within this region.
        """)

    # Final comparison explanation
    st.write(f"""
    The box plot allows you to compare how video games perform in different regions based on their sales distribution. The relative height 
    of each box reflects the range of sales for the region, while the median line inside each box shows where the midpoint of sales lies. 
    Outliers, represented as individual points outside the whiskers, can help identify exceptional cases—either bestsellers or poor performers.
    """)



# Customized Scatter Chart Function for Region Comparison
def scatter_chart():
    st.title("Compare Two Regions")
    
    # Allow user to select two regions for comparison
    region_x = st.selectbox("Select X-axis Region:", list(region_mapping.keys()))
    
    # Filter out the selected X-axis region from Y-axis options
    remaining_regions = [region for region in region_mapping.keys() if region != region_x]
    region_y = st.selectbox("Select Y-axis Region:", remaining_regions)

    # Get the corresponding sales data for the selected regions
    x_data = data[region_mapping[region_x]]
    y_data = data[region_mapping[region_y]]

    # Create a scatter plot comparing the selected regions
    fig_scatter = px.scatter(
        data,
        x=x_data,
        y=y_data,
        labels={region_mapping[region_x]: region_x, region_mapping[region_y]: region_y},
        title=f"Scatter Plot: {region_x} vs {region_y}",
        trendline="ols"  # Add a trendline for better comparison
    )

    # Calculate the correlation between the two selected regions
    correlation, _ = pearsonr(x_data, y_data)

    # Display the scatter chart
    st.plotly_chart(fig_scatter, use_container_width=True)

    # Add a detailed dynamic description based on the correlation
    if correlation > 0.75:
        st.write(f"""
        The correlation between {region_x} and {region_y} is **strong** (Correlation: {correlation:.2f}). 
        This means that sales in these two regions tend to move in the same direction. 
        When sales are high in {region_x}, they are likely to be high in {region_y} as well, 
        suggesting that games that perform well in one region tend to perform similarly well in the other.
        The strong correlation could indicate similar gaming preferences or market conditions in these regions.
        """)
    elif correlation > 0.5:
        st.write(f"""
        The correlation between {region_x} and {region_y} is **moderate** (Correlation: {correlation:.2f}).
        While there is a noticeable relationship between the sales in these two regions, 
        it's not as strong as a high correlation. This suggests that while some games might perform similarly in both regions,
        there are also notable differences in the market or consumer preferences.
        The trendline indicates the general direction of this relationship, 
        but there could be more variation in the sales data for certain games.
        """)
    elif correlation > 0.3:
        st.write(f"""
        The correlation between {region_x} and {region_y} is **weak** (Correlation: {correlation:.2f}).
        This means that the sales performance in these two regions is only slightly related. 
        It's possible that while a few games might sell similarly in both regions, 
        there are major differences in how most games perform in {region_x} versus {region_y}.
        This could be due to differing tastes, market conditions, or other regional factors.
        The trendline gives a general idea of the relationship, but the scatter points are more dispersed.
        """)
    else:
        st.write(f"""
        There is **little to no correlation** between {region_x} and {region_y} (Correlation: {correlation:.2f}).
        Sales in these two regions do not follow a consistent pattern. 
        A game's performance in {region_x} does not reliably predict its performance in {region_y}, 
        which suggests that these markets have very different gaming preferences or market dynamics.
        The scatter plot shows a wide spread of data points, and the trendline is relatively flat, 
        indicating minimal relationship between sales in the two regions.
        """)



# Function to display the Regional Sales Breakdown by Genre (Stacked Bar Chart)
def regional_sales_by_genre_chart():
    st.title("Regional Sales Breakdown by Genre")

    # Add a short explanation or description for the chart
    st.write("""
    This chart provides a breakdown of video game sales by genre across different regions. 
    Each genre's total sales are stacked and color-coded based on the sales contribution from 
    North America, Europe, Japan, and other regions. The height of each bar represents the 
    total sales for the genre, while the color segments show the sales distribution across regions.
    """)

    # Filter the relevant columns (Genre and regional sales)
    sales_columns = ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]
    genre_sales = data.groupby('Genre')[sales_columns].sum().reset_index()

    # Melt the dataframe to have one column for sales regions and values for easier plotting
    melted_genre_sales = pd.melt(genre_sales, id_vars='Genre', value_vars=sales_columns, 
                                 var_name='Region', value_name='Sales')

    # Create the stacked bar chart
    fig_bar = px.bar(melted_genre_sales, 
                     x='Genre', 
                     y='Sales', 
                     color='Region', 
                     labels={'Sales': 'Sales (in millions)', 'Genre': 'Genre'},
                     barmode='stack')

    # Customize layout for better presentation
    fig_bar.update_layout(
        xaxis_title="Genre",
        yaxis_title="Sales (in millions)",
        legend_title="Region",
        width=800, 
        height=600
    )

    # Display the chart
    st.plotly_chart(fig_bar, use_container_width=True)


# Function to display general insights and takeaways in the Conclusion tab
def show_conclusion():
    st.title("Conclusion: Key Insights and Takeaways")
    
    st.subheader("General Sales Trends Across Regions")
    st.write("""
    - **Global Sales**: Video games tend to perform differently across regions, with some regions like **North America** and **Europe** showing stronger sales trends compared to regions like **Japan**.
    - **Platform Dominance**: Specific platforms such as the **Nintendo DS** and **PlayStation** have consistently performed well across multiple regions, while other platforms like the **Xbox** have seen more regional popularity.
    - **Genre Popularity**: Certain genres, such as **Action** and **Sports**, dominate global sales, but niche genres like **Role-Playing** tend to have strong followings in regions like Japan.
    """)

    st.subheader("Key Takeaways from Data Analysis")
    st.write("""
    - **Skewness in Sales**: The sales distributions across most regions tend to be **positively skewed**, indicating that while a majority of games sell below the median, a few blockbuster titles push the average sales higher.
    - **Outliers**: There are many **outliers** in the sales data, particularly for best-selling games, which have significantly outperformed the rest of the market.
    - **Region-Specific Preferences**: Each region exhibits unique preferences, with games performing well in one region not necessarily achieving similar success in another. For instance, **Role-Playing Games (RPGs)** are more popular in **Japan**, while **Sports** and **Action** games lead the charts in **North America**.
    """)

    st.subheader("Market Insights for Stakeholders")
    st.write("""
    - **Developers and Publishers**: Understanding these sales patterns is crucial for developers and publishers when considering game localization, marketing strategies, and which genres to focus on in different regions.
    - **Platform Holders**: Platform dominance varies by region, so platform holders like **Nintendo**, **Sony**, and **Microsoft** can use these insights to tailor their game offerings and expand their market share in underperforming regions.
    - **Investors**: Investors can use this data to identify growing trends in specific regions or genres, investing in studios or platforms that align with the strongest growth areas.
    """)

    st.subheader("Future Trends to Watch")
    st.write("""
    - The growing popularity of **digital distribution** and **subscription-based gaming services** may significantly impact future sales trends.
    - Regional preferences could shift as cloud gaming becomes more prevalent, reducing barriers to access for certain platforms.
    - The rise of **mobile gaming** and **cross-platform play** may also lead to new sales trends across different regions and platforms.
    """)

    st.subheader("Conclusion")
    st.write("""
    Overall, the data provides valuable insights into the global video game market, with clear regional trends and market dynamics. 
    By understanding the key takeaways from this analysis, industry stakeholders can make more informed decisions on game development, 
    distribution, and marketing strategies to maximize their success across different markets.
    """)


# Display logic for the app based on option selected
if selected == "Introduction & Statistics":
    show_intro_and_overview()
elif selected == "Sales by Platform":
    pie_chart()
elif selected == "Sales Comparison":
    scatter_chart()
elif selected == "Sales Over Time":
    sales_over_time_chart()
elif selected == "Histogram":
    histogram_chart()
elif selected == "Box Plot":
    box_plot_chart()
elif selected == "Sales by Genre":
    regional_sales_by_genre_chart()
elif selected == "Conclusion":
    show_conclusion()
