import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3
import os
from load_data import load_csv
from create_db import create_db
from queries import (
    top_ev_makes, 
    ev_count_by_year, 
    ev_count_by_county, 
    avg_electric_range_by_make, 
    ev_per_city_within_specific_county, 
    ev_dist_by_type_and_cafv, 
    top_ev_models_by_range
)

# Page configuration
st.set_page_config(
    page_title="EV Analytics Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .chart-container {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load data only - no database connection"""
    try:
        # Load data - use relative path from src directory
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", "ev_data.csv")
        df = load_csv(data_path)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def get_db_connection():
    """Get a fresh database connection for each query"""
    try:
        db_path = os.path.join(os.path.dirname(__file__), "..", "db", "ev_data.db")
        return sqlite3.connect(db_path)
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return None

def main():
    # Header
    st.markdown('<h1 class="main-header">🚗 EV Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    with st.spinner("Loading EV data..."):
        df = load_data()
    
    if df is None:
        st.error("Failed to load data. Please check if ev_data.csv exists in the data/ folder.")
        return
    
    # Sidebar filters
    st.sidebar.header("Filters Data")
    
    # Year filter
    if df is not None:
        # Check for null values in Model Year column
        years = df['Model Year'].dropna().unique()
        years = sorted([int(year) for year in years if year is not None and pd.notna(year)])
        selected_years = st.sidebar.multiselect(
            "Select Years:",
            options=years,
            default=years[-5:] if len(years) >= 5 else years
        )
    else:
        selected_years = []
    
    # Make filter
    if df is not None:
        # Handle null values in Make column
        makes = df['Make'].dropna().unique()
        makes = sorted([str(make) for make in makes if make is not None])
    else:
        makes = []
    selected_makes = st.sidebar.multiselect(
        "Select Makes:",
        options=makes,
        default=makes[:10] if len(makes) >= 10 else makes
    )
    
    # County filter
    if df is not None:
        # Handle null values in County column
        counties = df['County'].dropna().unique()
        counties = sorted([str(county) for county in counties if county is not None])
    else:
        counties = []
    selected_counties = st.sidebar.multiselect(
        "Select Counties:",
        options=counties,
        default=counties[:5] if len(counties) >= 5 else counties
    )
    
    # Main content
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Overview", 
        "🏭 Manufacturers", 
        "🗺️ Geographic", 
        "🔋 Performance", 
        "📊 Detailed Analysis"
    ])
    
    with tab1:
        st.header("📈 EV Market Overview")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_evs = len(df) if df is not None else 0
            st.metric("Total EVs", f"{total_evs:,}")
        
        with col2:
            unique_makes = df['Make'].nunique() if df is not None else 0
            st.metric("Unique Makes", unique_makes)
        
        with col3:
            if df is not None:
                avg_range = df['Electric Range'].dropna().mean()
                avg_range = avg_range if pd.notna(avg_range) else 0
            else:
                avg_range = 0
            st.metric("Avg Range (miles)", f"{avg_range:.1f}")
        
        with col4:
            unique_counties = df['County'].nunique() if df is not None else 0
            st.metric("Counties", unique_counties)
        
        # EV Growth Over Years
        st.subheader("EV Growth Over Years")
        conn = get_db_connection()
        if conn:
            df_years = ev_count_by_year(conn)
            conn.close()
        else:
            df_years = pd.DataFrame()
        
        fig_years = px.line(
            df_years, 
            x="Year", 
            y="EV_Count",
            title="EV Count by Year",
            markers=True
        )
        fig_years.update_layout(
            xaxis_title="Year",
            yaxis_title="Number of EVs",
            height=400
        )
        st.plotly_chart(fig_years, use_container_width=True)
        
        # Top EV Makes
        st.subheader("Top EV Manufacturers")
        conn = get_db_connection()
        if conn:
            df_makes = top_ev_makes(conn)
            conn.close()
        else:
            df_makes = pd.DataFrame()
        
        fig_makes = px.bar(
            df_makes,
            x="Make",
            y="total",
            title="Top 5 EV Manufacturers",
            color="total",
            color_continuous_scale="Blues"
        )
        fig_makes.update_layout(
            xaxis_title="Manufacturer",
            yaxis_title="Number of EVs",
            height=400
        )
        st.plotly_chart(fig_makes, use_container_width=True)
    
    with tab2:
        st.header("🏭 Manufacturer Analysis")
        
        # Average Electric Range by Make
        st.subheader("Average Electric Range by Make")
        conn = get_db_connection()
        if conn:
            df_range = avg_electric_range_by_make(conn)
            conn.close()
        else:
            df_range = pd.DataFrame()
        
        fig_range = px.bar(
            df_range,
            x="Make",
            y="Avg_Range",
            title="Average Electric Range by Make (Top 10)",
            color="Avg_Range",
            color_continuous_scale="Greens"
        )
        fig_range.update_layout(
            xaxis_title="Manufacturer",
            yaxis_title="Average Range (miles)",
            height=500
        )
        st.plotly_chart(fig_range, use_container_width=True)
        
        # Top EV Models by Range
        st.subheader("Top EV Models by Range")
        conn = get_db_connection()
        if conn:
            df_models = top_ev_models_by_range(conn)
            conn.close()
        else:
            df_models = pd.DataFrame()
        
        fig_models = px.scatter(
            df_models,
            x="Avg_Range",
            y="Model_Count",
            size="Avg_Range",
            color="Make",
            hover_name="Model",
            title="EV Models by Range and Popularity",
            labels={"Avg_Range": "Average Range (miles)", "Model_Count": "Number of Vehicles"}
        )
        fig_models.update_layout(height=500)
        st.plotly_chart(fig_models, use_container_width=True)
    
    with tab3:
        st.header("🗺️ Geographic Distribution")
        
        # EV Count by County
        st.subheader("EV Count by County")
        conn = get_db_connection()
        if conn:
            df_county = ev_count_by_county(conn)
            conn.close()
        else:
            df_county = pd.DataFrame()
        
        fig_county = px.bar(
            df_county.head(20),
            x="County",
            y="EV_Count",
            title="EV Count by County (Top 20)",
            color="EV_Count",
            color_continuous_scale="Reds"
        )
        fig_county.update_layout(
            xaxis_title="County",
            yaxis_title="Number of EVs",
            height=500,
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_county, use_container_width=True)
        
        # EV Count by City within Specific Counties
        st.subheader("EV Count by City (King, Pierce, Snohomish, Spokane)")
        conn = get_db_connection()
        if conn:
            df_city = ev_per_city_within_specific_county(conn)
            conn.close()
        else:
            df_city = pd.DataFrame()
        
        fig_city = px.bar(
            df_city,
            x="City",
            y="Count",
            title="EV Count by City Within Specific Counties",
            color="Count",
            color_continuous_scale="Purples"
        )
        fig_city.update_layout(
            xaxis_title="City",
            yaxis_title="Number of EVs",
            height=500,
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_city, use_container_width=True)
    
    with tab4:
        st.header("🔋 Performance & Efficiency")
        
        # EV Distribution by Type and CAFV Eligibility
        st.subheader("EV Distribution by Type and CAFV Eligibility")
        conn = get_db_connection()
        if conn:
            df_dist = ev_dist_by_type_and_cafv(conn)
            conn.close()
        else:
            df_dist = pd.DataFrame()
        
        fig_dist = px.bar(
            df_dist,
            x="Electric Vehicle Type",
            y="Count",
            color="Clean Alternative Fuel Vehicle (CAFV) Eligibility",
            title="EV Distribution by Type and CAFV Eligibility",
            barmode="group"
        )
        fig_dist.update_layout(
            xaxis_title="Electric Vehicle Type",
            yaxis_title="Number of Vehicles",
            height=500
        )
        st.plotly_chart(fig_dist, use_container_width=True)
        
        # Range distribution histogram
        if df is not None:
            st.subheader("Electric Range Distribution")
            # Filter out null values and values <= 0
            range_data = df[(df['Electric Range'] > 0) & (df['Electric Range'].notna())]['Electric Range']
            
            if len(range_data) > 0:
                fig_hist = px.histogram(
                    x=range_data,
                    nbins=30,
                    title="Distribution of Electric Range",
                    labels={"x": "Electric Range (miles)", "y": "Number of Vehicles"}
                )
                fig_hist.update_layout(height=400)
                st.plotly_chart(fig_hist, use_container_width=True)
            else:
                st.warning("No valid range data available for histogram.")
    
    with tab5:
        st.header("📊 Detailed Analysis")
        
        # Data tables
        st.subheader("Raw Data Tables")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Top EV Makes**")
            conn = get_db_connection()
            if conn:
                st.dataframe(top_ev_makes(conn), use_container_width=True)
                conn.close()
            
            st.write("**EV Count by Year**")
            conn = get_db_connection()
            if conn:
                st.dataframe(ev_count_by_year(conn), use_container_width=True)
                conn.close()
        
        with col2:
            st.write("**Average Range by Make**")
            conn = get_db_connection()
            if conn:
                st.dataframe(avg_electric_range_by_make(conn), use_container_width=True)
                conn.close()
            
            st.write("**Top Models by Range**")
            conn = get_db_connection()
            if conn:
                st.dataframe(top_ev_models_by_range(conn), use_container_width=True)
                conn.close()
        
        # Download data
        st.subheader("📥 Download Data")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            conn = get_db_connection()
            if conn:
                csv_makes = top_ev_makes(conn).to_csv(index=False)
                st.download_button(
                    label="Download Top Makes",
                    data=csv_makes,
                    file_name="top_ev_makes.csv",
                    mime="text/csv"
                )
                conn.close()
        
        with col2:
            conn = get_db_connection()
            if conn:
                csv_years = ev_count_by_year(conn).to_csv(index=False)
                st.download_button(
                    label="Download Year Data",
                    data=csv_years,
                    file_name="ev_by_year.csv",
                    mime="text/csv"
                )
                conn.close()
        
        with col3:
            conn = get_db_connection()
            if conn:
                csv_range = avg_electric_range_by_make(conn).to_csv(index=False)
                st.download_button(
                    label="Download Range Data",
                    data=csv_range,
                    file_name="avg_range_by_make.csv",
                    mime="text/csv"
                )
                conn.close()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "🚗 EV Analytics Dashboard | Built with Streamlit and Plotly"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 