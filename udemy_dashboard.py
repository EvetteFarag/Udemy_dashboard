import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="Udemy Dashboard",
                    page_icon=None,
                    layout="wide",
                    initial_sidebar_state="expanded")

df = pd.read_csv(r"C:\\Users\\hp\Desktop\\tips\\udemy_project\\udemy model.csv")

st.sidebar.header("Udemy Dashboard")
st.sidebar.write("")

st.sidebar.write("Educational Dashboard Using Udemy Dataset")
st.sidebar.write("")

#st.sidebar.image("Udemy.jpg")
st.sidebar.write("")

st.sidebar.write("Filter your data :")

year_filter = st.sidebar.selectbox("year",[None,2014, 2015 ,2016 ,2017])
month_filter= st.sidebar.selectbox("month",df["month"].unique())
price_filter = st.sidebar.selectbox("Price_category", df["Price_category"].unique())

st.sidebar.write("")
st.sidebar.markdown("Made with :heart_eyes: by [Evette Farag](www.linkedin.com/in/evette-farag-7505151b6)")




#row1

a1 , a2 , a3  = st.columns([3,3,3])

with a1:
    a1.metric("No. of courses" ,df["course_id"].value_counts().sum())
with a2:
    # Calculate total profit
    sum_profit = df["Profit"].sum()
    # Format the number
    formatted_number = f"{sum_profit:,.2f}"
    # Format the number with dots instead of commas
    formatted_number = f"{sum_profit:,}".replace(",", ".")
    # Display the formatted number
    a2=st.metric("Total Profit", formatted_number)

with a3:
    # Calculate total of No. of subscribers
    sum_num_subscribers= df['num_subscribers'].sum()
    # Format the number
    formatted_number= f"{sum_num_subscribers:,.2f}"
    # Format the number with dots instead of commas
    formatted_number = f"{sum_num_subscribers:,}".replace(",", ".")
    # Display the formatted number
    a3=st.metric("total of No. of subscribers", formatted_number)

# Add space before the charts
st.markdown("   ")  # Or st.markdown("                                 /><                                        />" for more space)



#row2 
# Create columns
b1, b2 = st.columns(2)

# Chart 1 (subjects vs. no. of subscribers by year)
with b1:
    filtered_df = df[df["year"] == year_filter]
    grouped_df = filtered_df.groupby("subject")["num_subscribers"].sum()
    # Create the figure with a sequential color palette
    fig = px.bar(data_frame=grouped_df.reset_index(), x="subject", y="num_subscribers",
                 color="subject", color_continuous_scale=px.colors.sequential.Viridis)
    # Update the layout to position the title in the center
    fig.update_layout(
    title="subjects vs. no. of subscribers by year",
    title_x=0.2,  # Center horizontally
    title_y=0.9,  # Adjust vertically as needed
    xaxis=dict(showgrid=False),  # Remove x-axis gridlines
    yaxis=dict(showgrid=False),  # Remove y-axis gridlines
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Chart 2 (subjects vs. no. of subscribers by month)
with b2:
    filtered_month = df[df["month"] == month_filter]
    grouped_df = filtered_month.groupby("subject")["num_subscribers"].sum()
    fig = px.bar(data_frame=grouped_df.reset_index(), x="subject", y="num_subscribers",
                 color="subject", color_continuous_scale=px.colors.sequential.Viridis)
    # Update the layout to position the title in the center
    fig.update_layout(
    title="subjects vs. no. of subscribers by month",
    title_x=0.2,  # Center horizontally
    title_y=0.9,  # Adjust vertically as needed
    xaxis=dict(showgrid=False),  # Remove x-axis gridlines
    yaxis=dict(showgrid=False),  # Remove y-axis gridlines
    )
    st.plotly_chart(fig, use_container_width=True)



#row3
r1 = st.columns(1)

# Create the pie chart
fig1 = px.pie(data_frame=df, names="is_paid")
# Update the layout to position the title in the center
fig1.update_layout(
    title="NO. of paid/unpaid coursesr",
    title_x=0.6,  # Center horizontally
    title_y=0.9  # Adjust vertically as needed
    )
# Update text position
fig1.update_traces(textposition='auto')  # Automatically position text
textfont=dict(
            family="Cambria",  # You can choose any font family
            size=14,         # Adjust the size of the text
            color="white",   # Set text color
            bold=True        # Make the text bold
)
# Display the chart
st.plotly_chart(fig1, use_container_width=True)



#row4
e1 = st.columns(1)
fig2=px.bar(df,x='subject',y='Profit',
            color="Price_category",
            color_continuous_scale=px.colors.sequential.Viridis,
)


# Update the layout to position the title in the center
fig2.update_layout(

    title="In each year what is the total profit by each subject regarding price category",
    title_x=0.2,  # Center horizontally
    title_y=0.9,  # Adjust vertically as needed
    xaxis=dict(showgrid=False),  # Remove x-axis gridlines
    yaxis=dict(showgrid=False),  # Remove y-axis gridlines
)

# Display the chart
st.plotly_chart(fig2, use_container_width=True)



#row5
m1 = st.columns(1)[0]  # Extract the first (and only) column from the list 
with m1:
    # Filter the dataframe
    filtered_price = df[df["Price_category"] == price_filter]
    
    # Group by both subject and Price_category to retain the column
    grouped_df = filtered_price.groupby(["subject", "Price_category"])["num_subscribers"].sum().reset_index()

    # Calculate the percentage for each category
    total_subscribers = grouped_df["num_subscribers"].sum()
    grouped_df["percentage"] = (grouped_df["num_subscribers"] / total_subscribers) * 100

    # Create a text column for showing both value and percentage, separated by a line break
    grouped_df["text"] = grouped_df.apply(
        lambda row: f'{row["num_subscribers"]:,}<br>({row["percentage"]:.2f}%)', axis=1
    )
    
    # Plot with the retained Price_category column and add text for value and percentage
    fig3 = px.bar(
        data_frame=grouped_df,
        x='subject',
        y='num_subscribers',
        color='Price_category',  # Color by Price_category
        text='text',  # Show the text with value and percentage
        color_discrete_sequence=px.colors.qualitative.Vivid  # Choose any color sequence
    )
    
    # Update the layout to adjust title position and text position on bars
    fig3.update_layout(
        title="How Many Subscribers in Each Subject Regarding Price Category",
        title_x=0.2,  # Center horizontally
        title_y=0.9, # Adjust vertically as needed
        xaxis=dict(showgrid=False),  # Remove x-axis gridlines
        yaxis=dict(showgrid=False),  # Remove y-axis gridlines
    )
    
    # Update text position
    fig3.update_traces(textposition='auto')  # Automatically position text
    textfont=dict(
            family="Cambria",  # You can choose any font family
            size=14,         # Adjust the size of the text
            color="white",   # Set text color
            bold=True        # Make the text bold
    )


    # Display the chart
    st.plotly_chart(fig3, use_container_width=True)



#row6

n1 = st.columns(1)[0] # Extract the first (and only) column from the list 
with n1:
    fig5=px.bar(df,x='subject',y='Profit',
            color="Duration_Category",
            color_continuous_scale=px.colors.sequential.Viridis,
)
# Update the layout to position the title in the center
fig5.update_layout(

    title="In each year what is the total profit by each subject regarding duration category",
    title_x=0.2,  # Center horizontally
    title_y=0.9,  # Adjust vertically as needed
    xaxis=dict(showgrid=False),  # Remove x-axis gridlines
    yaxis=dict(showgrid=False),  # Remove y-axis gridlines
)
 # Display the chart
st.plotly_chart(fig5, use_container_width=True)











