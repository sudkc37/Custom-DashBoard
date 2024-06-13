import pandas as pd 
import plotly.express as pl
import os
import streamlit as st


st.set_page_config(page_title="DASHBOARD: Sales Report ", page_icon=":chart_with_upwards_trend:", layout="wide")
st.title(" :chart_with_upwards_trend: DASHBOARD: Sales Report")
st.markdown('<style>div.block-container{padding-to:1rem;}</style>', unsafe_allow_html=True)

column1, column2 = st.columns((2))

with column1:
    df = st.file_uploader("Files: Upload a File", type=(["csv","xlsx","xls"]))
    if df is not None:
        filename = df.name
        st.write(f"Uploaded file: {filename}")
        file_extension = filename.split('.')[-1]
        if file_extension=='csv':
            df = pd.read_csv(df)
        if file_extension in ['xls','xlsx']:
            df = pd.read_excel(df)
        else:
            st.error(f"Unsupperted file format: {file_extension}")
    




state_mapping = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
    'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
    'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
    'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
    'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}

df['State_code'] = df['State'].replace(state_mapping)


range_columns = st.sidebar.selectbox("Select Range columns: ", df.columns)
df[range_columns] = pd.to_datetime(df[range_columns])
start_date = pd.to_datetime(df[range_columns]).min()
end_date = pd.to_datetime(df[range_columns]).max()


with column2:
    start = pd.to_datetime(st.date_input("Start Date", start_date))
with column2:
    end = pd.to_datetime(st.date_input("End Date", end_date))

df = df[(df[range_columns] >= start) & (df[range_columns] <= end)].copy()



st.sidebar.header("Select Columns:")
selected_columns = st.sidebar.multiselect("Select columns to filter by: ", df.columns, max_selections=4)
st.sidebar.header("Choose Filters: ")
selected_filters = {}

selected_filters[0] = st.sidebar.multiselect(f"Select {selected_columns[0]} ", df[selected_columns[0]].unique())
if not selected_filters[0]:
    df1 = df.copy()
else:
    df1 = df[df[selected_columns[0]].isin(selected_filters[0])]

selected_filters[1] = st.sidebar.multiselect(f"Select {selected_columns[1]} ", df1[selected_columns[1]].unique())
if not selected_columns[1]:
    df2 = df1.copy()
else:
    df2 = df1[df1[selected_columns[1]].isin(selected_filters[1])]

selected_filters[2] = st.sidebar.multiselect(f"Select {selected_columns[2]} ", df2[selected_columns[2]].unique())
if not selected_filters[2]:
    df3 = df2.copy()
else:
    df3 = df2[df2[selected_columns[2]].isin(selected_filters[2])]

selected_filters[3] = st.sidebar.multiselect(f"Select {selected_columns[3]} ", df3[selected_columns[3]].unique())
if not selected_filters[3]:
    df4 = df3.copy()
else:
    df4 = df3[df3[selected_columns[3]].isin(selected_filters[3])]



sales_category = df4.groupby(by=['Category'], as_index = False)["Sales"].sum()

with column1:
    fig = pl.bar(sales_category, x="Category", y = "Sales", template="seaborn", title='Category wise sales')
    st.plotly_chart(fig, use_container_width=True)

with column2:
    fig = pl.pie(df4, values ='Sales', names='Region', hole=0.5, title='Region wise sales')
    fig.update_traces(text= df4['Region'], textposition ='outside')
    st.plotly_chart(fig, use_container_width=True)



aggregate_sales_state = df3.groupby('State_code').agg({
    'Sales':'sum',
    'Quantity':'sum',
    'Profit':'sum'
}).round().reset_index()

with column2:
    fig = pl.choropleth(aggregate_sales_state, 
                    locations='State_code',
                    locationmode= "USA-states",
                    color='Sales', 
                    scope ='usa',
                    hover_data=['Sales','Quantity','Profit'],
                    title='Sales by Filtered States')
    fig.update_layout(mapbox_style='open-street-map')
    st.plotly_chart(fig, use_container_width=True)


profit_category = df4.groupby(by=['Category'], as_index = False)["Profit"].sum()
with column1:
    fig = pl.bar(profit_category, x="Category", y = "Profit", template="seaborn", title='Category wise Profit')
    st.plotly_chart(fig, use_container_width=True)


sales_segment = df4.groupby(by=['Segment'], as_index = False)["Sales"].sum()
with column1:
    fig = pl.pie(df4, values ='Sales', names='Segment', hole=0.5, title='Segment wise sales')
    fig.update_traces(text= df4['Segment'], textposition ='outside')
    st.plotly_chart(fig, use_container_width=True)

profit_segment = df4.groupby(by=['Segment'], as_index = False)["Profit"].sum()
with column2:
    fig = pl.bar(profit_segment, x="Segment", y = "Profit", template="seaborn", title='Segment wise Profit')
    st.plotly_chart(fig, use_container_width=True)

fig = pl.scatter(df4, x='Sales', y='Profit', size='Quantity', title='Sales Vs Profit for filtered data')
st.plotly_chart(fig, use_container_width=True)

fig = pl.scatter(df, x='Sales', y='Profit', size='Quantity', title='Sales Vs Profit for Entire Dataset')
st.plotly_chart(fig, use_container_width=True)


aggregate = df.groupby('State_code').agg({
    'Sales':'sum',
    'Quantity':'sum',
    'Profit':'sum'
}).round().reset_index()

aggregate_df = pd.DataFrame(aggregate)

fig = pl.choropleth(aggregate_df, 
                    locations='State_code',
                    locationmode= "USA-states",
                    color='Sales', 
                    scope ='usa',
                    hover_data=['Sales','Quantity','Profit'],
                    title='Summary Report by State')
fig.update_layout(mapbox_style='open-street-map')
st.plotly_chart(fig, use_container_width=True)                       

st.header("Filtered DataFrame:")
st.write(df4)