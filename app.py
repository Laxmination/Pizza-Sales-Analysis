import streamlit as st
import pandas as pd
from style import headerStyle, kpiStyle
import plotly.express as px

@st.cache_data
def load_data(path:str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


# Clean data and Feature engineering
@st.cache_data
def clean_data(df:pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["order_date"] = pd.to_datetime(df["order_date"], format="mixed")
    df["order_time"] = pd.to_datetime(df["order_time"], format="mixed").dt.time

    # Feature engineering
    df["Order_Day"] = df["order_date"].dt.day_name()
    df["Order_Month"] = df["order_date"].dt.month_name()
    df["month_num"] = df["order_date"].dt.month
    df["Order_Hour"] = pd.to_datetime(df["order_time"], format="%H:%M:%S").dt.hour

    # Categorical ordering so plots sort correctly
    weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday"]
    df["Order_Day"] = pd.Categorical(df["Order_Day"], categories=weekdays, ordered=True)

    months = ["January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"]
    df["Order_Month"] = pd.Categorical(df["Order_Month"], categories=months, ordered=True)

    return df

# Read data using functions
df_raw = load_data('pizza_sales.csv')
df = clean_data(df_raw)

# Page Configuration
st.set_page_config(
    page_title='Pizza Sales Dashboard',
    page_icon=':pizza:',
    layout='wide',
    initial_sidebar_state='auto'
)

st.title('Pizza Sales Dashboard')
# st.header(':yellow[KPI]')


# Sidebar
st.sidebar.header('Filter Data')


# Get Unique Categories
categories =sorted(df['pizza_category'].unique())

#implement unique categories into dropdown for selection
categories_data = st.sidebar.multiselect(
    'Pizza Category',
    options=categories,
    default=categories
)

# Get unique Sizes
sizes = sorted(df['pizza_size'].unique())
# Implement unique Sizes into dropdown for selection
sizes_data = st.sidebar.multiselect(
    'Pizza Size',
    options=sizes,
    default=sizes
)



# Filter Data
filtered = df[
    df["pizza_category"].isin((categories_data))
    &(df['pizza_size'].isin(sizes_data))
]

if filtered.empty:
    st.warning('No Data selected')
    st.stop()

# KPI
st.markdown(headerStyle('KPI'), unsafe_allow_html=True)

total_revenue = filtered['total_price'].sum()
total_pizza_sold = filtered['quantity'].sum()
total_orders = filtered['order_id'].nunique()
average_order_value = total_revenue/ total_orders
average_pizza_per_order = total_pizza_sold / total_orders


kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.markdown(kpiStyle('Total Revenue', f'${total_revenue:,.2f}'), unsafe_allow_html=True)

with kpi2:
    st.markdown(kpiStyle('Total Pizza Sold', f'${total_pizza_sold:,.2f}'), unsafe_allow_html=True)

with kpi3:
    st.markdown(kpiStyle('Total Orders', f'{total_orders}'), unsafe_allow_html=True)

with kpi4:
    st.markdown(kpiStyle('Average Order Value', f'{average_order_value:,.2f}'), unsafe_allow_html=True)

with kpi5:
    st.markdown(kpiStyle('Average Pizza/Order', f'{average_pizza_per_order:,.2f}'), unsafe_allow_html=True)


# st.metric(':red[Total Revenue]', f'${total_revenue:,.2f}')
# st.metric('Total Pizza Sold', f'${total_pizza_sold:,.2f}')
# st.metric('Total Orders', f'${total_orders:,.2f}')


st.markdown(headerStyle('Analysis'), unsafe_allow_html=True)

st.markdown(headerStyle('Raw Data'), unsafe_allow_html=True)

st.divider()

# Tabs for Visualization
tab_overview, tab_time, tab_top_bottom, raw_data = st.tabs(
    ['Overview', 'Time Analysis', 'Top/Bottom Sales', 'Raw Data']
)

with tab_overview:
    left, right = st.columns(2)
    
    with left:
        cat_sales_pct = df.groupby('pizza_category')['total_price'].sum().reset_index()
        
        fig = px.pie(
            cat_sales_pct,
            names='pizza_category',
            values ='total_price',
            hole=0.5,
            labels={'pizza_category':'Pizza Category', 'total_price':'Revenue($)'},
            color_discrete_sequence=px.colors.sequential.ice
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    with right:
        size_cat_pct = df.groupby(['pizza_size', 'pizza_category'])['total_price'].sum().reset_index()
        
        fig = px.bar(
            size_cat_pct,
            x='pizza_size',
            y='total_price',
            color='pizza_category',
            barmode='group',
            labels={'pizza_size':'Pizza Size', 'pizza_category':'Pizza Category', 'total_price':'Revenue($)'},
            color_discrete_sequence=px.colors.sequential.Plasma
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        
        
with tab_time:
    left, right = st.columns(2)
    
    with left:
        day_sales = filtered.groupby('Order_Day', observed=False)['total_price'].sum().reset_index()
        
        fig = px.line(
            day_sales,
            x= 'Order_Day',
            y='total_price',
            markers='o'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        with right:
            hour_sales = filtered.groupby('Order_Hour')['total_price'].sum().reset_index()
            st.subheader('sales by order hour')
                    
            fig = px.bar(
                hour_sales,
                x= 'Order_Hour',
                y='total_price',
                color_continuous_scale='blues',
                labels={'Order Hour':'Hour', 'total_price':'Revenue($)'}
            )
            
            fig.update_layout(coloraxis_showscale=False)
            fig.update_xaxes(dtick=1)
            
            
            st.plotly_chart(fig, use_container_width=True)
            
    # Monthly Sales
    monthly_sales = df.groupby('Order_Month').agg(
        Total_Price =('total_price', 'sum'),
        Total_Orders = ('order_id', 'nunique')
    ).reset_index()
    
    st.subheader('Sales by Order Month')
    
    fig = px.line(
        monthly_sales,
        x='Order_Month',
        y='Total_Price',
        markers=True
    )
    
    fig.add_bar(
        x=monthly_sales['Order_Month'],
        y=monthly_sales['Total_Orders'],
        name='Orders',
        yaxis='y2',
        opacity=0.60
    )
    
    fig.update_layout(
        yaxis1=dict(title='Total Price'),
        yaxis2=dict(title='Orders', overlaying='y', side='right'),
        legend=dict(orientation='h', y=1.1),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    
    
with tab_top_bottom:
    left, right = st.columns(2)
    
    top_n =st.slider('How many pizza you want to show?', min_value=3, max_value=10, value=5)
    
    with left:
        st.subheader(f'Top {top_n} Best Selling Pizza')
        
        top_5 = filtered.groupby('pizza_name').agg(
            Total_Revenue =('total_price', 'sum'),
            Total_Orders =('order_id', 'sum'),
            Total_Quantity =('quantity', 'sum')
        ).reset_index().rename(
            columns={'pizza_name':'Pizza Name', 'Total_Revenue':'Revenue($)'}
        ).sort_values(ascending=False, by='Revenue($)', ignore_index=True).head(top_n)
        
        fig=px.bar(
            top_5,
            x='Revenue($)',
            y='Pizza Name',
            orientation='h',
            color='Revenue($)',
            color_continuous_scale='blues'
        )
        
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
        
        
    with right:
        st.subheader(f'Bottom {top_n} least selling pizza')
        bottom_5 =filtered.groupby('pizza_name').agg(
            Total_Revenue =('total_price', 'sum')
        ).reset_index().rename(
            columns={'pizza_name': 'Pizza Name'}
        ).sort_values(ascending=True, by='Total_Revenue', ignore_index=True).head(top_n)
        
        fig = px.bar(
            bottom_5,
            x= 'Total_Revenue',
            y='Pizza Name',
            orientation='h',
            color='Total_Revenue',
            color_continuous_scale='blues'
        )
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
        
    st.divider()
    st.subheader('Tree Map')
    tree=(
        filtered.groupby(['pizza_category','pizza_size', 'pizza_name'])['total_price'].sum().reset_index()
    )
    
    fig =px.treemap(
        tree,
        path=['pizza_category', 'pizza_size', 'pizza_name'],
        values='total_price',
        color='total_price',
        color_continuous_scale='RdBu'
    )
    
    st.plotly_chart(fig)
with raw_data:
    st.write('Data')