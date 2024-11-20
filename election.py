import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Define party color scheme
PARTY_COLORS = {
    'Janasena Party': '#FF0000',  # Red
    'Telugu Desam': '#FFD700',    # Yellow
    'Yuvajana Sramika Rythu Congress Party': '#0000FF',  # Blue
    'Bharatiya Janata Party': '#FFA500'  # Orange
}

# Set page configuration
st.set_page_config(
    page_title="AP Elections 2024",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stPlotlyChart {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 1rem;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-container {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .stDataFrame {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 1rem;
        padding: 1rem;
    }
    .css-1d391kg {
        padding-top: 1rem;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
    }
    .st-emotion-cache-16idsys p {
        font-size: 1.2rem;
    }
    .custom-header {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    file_path = "AP_2024-2.csv"
    return pd.read_csv(file_path)

# Load data
data = load_data()

# Header Section
st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='font-size: 3rem; font-weight: bold; margin-bottom: 1rem;'>
            🗳️ Andhra Pradesh Elections 2024
        </h1>
        <p style='font-size: 1.2rem; color: #cccccc;'>
            Comprehensive Analysis & Visualization Dashboard
        </p>
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/2/2b/India_Andhra_Pradesh_locator_map.svg", width=200)
    
    # Party selection with colored boxes
    st.markdown("### 🎫 Select Party")
    selected_party = st.selectbox(
        "",
        options=list(PARTY_COLORS.keys()),
        key='party_select'
    )
    
    # Show party color indicator
    st.markdown(f"""
        <div style='background-color: {PARTY_COLORS[selected_party]}; 
                    padding: 1rem; 
                    border-radius: 0.5rem; 
                    margin: 1rem 0;
                    color: black;
                    text-align: center;
                    font-weight: bold;'>
            {selected_party}
        </div>
    """, unsafe_allow_html=True)
    
    # Constituency selection
    st.markdown("### 🏛️ Select Constituency")
    constituencies = sorted(data['Constituency'].unique())
    selected_constituency = st.selectbox("", constituencies, key='constituency_select')
    
    # Time info
    st.markdown("---")
    st.markdown(f"Last updated: {datetime.now().strftime('%B %d, %Y %H:%M')}")

# Main content area with tabs
tab1, tab2, tab3 = st.tabs(["📊 Party Analysis", "🏛️ Constituency Details", "📈 Overall Trends"])

# Tab 1: Party Analysis
with tab1:
    party_data = data[data['Party'] == selected_party].copy()
    
    # Key metrics row
    met1, met2, met3, met4 = st.columns(4)
    with met1:
        st.metric("Total Constituencies", len(party_data['Constituency'].unique()))
    with met2:
        st.metric("Total Votes", f"{party_data['Total Votes'].sum():,}")
    with met3:
        st.metric("Average Votes", f"{int(party_data['Total Votes'].mean()):,}")
    with met4:
        st.metric("Highest Votes", f"{int(party_data['Total Votes'].max()):,}")
    
    # Main charts
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Votes Distribution
        fig_votes = px.bar(
            party_data.sort_values('Total Votes', ascending=False),
            x='Constituency',
            y='Total Votes',
            color='Candidate',
            title='Constituency-wise Vote Distribution',
            template='plotly_dark',
            color_discrete_sequence=[PARTY_COLORS[selected_party]]
        )
        fig_votes.update_layout(
            height=500,
            xaxis_tickangle=-45,
            showlegend=True,
            legend_title="Candidates"
        )
        st.plotly_chart(fig_votes, use_container_width=True)
    
    with col2:
        # Vote Distribution Box Plot
        fig_box = go.Figure()
        fig_box.add_trace(go.Box(
            y=party_data['Total Votes'],
            name='Votes',
            marker_color=PARTY_COLORS[selected_party],
            boxpoints='all',
            jitter=0.3,
            pointpos=-1.8
        ))
        fig_box.update_layout(
            title='Vote Distribution Statistics',
            template='plotly_dark',
            height=500,
            showlegend=False
        )
        st.plotly_chart(fig_box, use_container_width=True)

# Tab 2: Constituency Details
with tab2:
    const_data = data[data['Constituency'] == selected_constituency].copy()
    
    # Constituency metrics
    st.subheader(f"📍 {selected_constituency} Constituency")
    
    met1, met2, met3 = st.columns(3)
    with met1:
        st.metric("Total Candidates", len(const_data))
    with met2:
        st.metric("Total Votes Cast", f"{const_data['Total Votes'].sum():,}")
    with met3:
        st.metric("Leading Party", const_data.loc[const_data['Total Votes'].idxmax(), 'Party'])
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Vote share pie chart
        fig_pie = px.pie(
            const_data,
            values='Total Votes',
            names='Party',
            title='Vote Share Distribution',
            template='plotly_dark',
            color='Party',
            color_discrete_map=PARTY_COLORS,
            hole=0.4
        )
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Results table
        st.subheader("Detailed Results")
        styled_data = const_data[['Candidate', 'Party', 'Total Votes']].sort_values('Total Votes', ascending=False)
        st.dataframe(
            styled_data.style.background_gradient(cmap='viridis', subset=['Total Votes']),
            height=400
        )
        
        # Download button
        csv = const_data.to_csv(index=False)
        st.download_button(
            "📥 Download Constituency Data",
            csv,
            f"{selected_constituency}_results.csv",
            "text/csv",
            key='download_button'
        )

# Tab 3: Overall Trends
with tab3:
    # Overall vote share analysis
    party_totals = data.groupby('Party')['Total Votes'].agg(['sum', 'mean', 'count']).reset_index()
    party_totals.columns = ['Party', 'Total Votes', 'Average Votes', 'Constituencies']
    party_totals['Vote Share (%)'] = (party_totals['Total Votes'] / party_totals['Total Votes'].sum() * 100).round(2)
    
    # Overall metrics
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Total Constituencies", len(data['Constituency'].unique()))
    with m2:
        st.metric("Total Votes Cast", f"{data['Total Votes'].sum():,}")
    with m3:
        st.metric("Total Candidates", len(data['Candidate'].unique()))
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Party-wise vote share
        fig_total = px.bar(
            party_totals.sort_values('Total Votes', ascending=True),
            y='Party',
            x='Total Votes',
            title='Total Votes by Party',
            template='plotly_dark',
            orientation='h',
            color='Party',
            color_discrete_map=PARTY_COLORS
        )
        fig_total.update_layout(height=500)
        st.plotly_chart(fig_total, use_container_width=True)
    
    with col2:
        # Summary table
        st.subheader("Vote Share Summary")
        summary_df = party_totals[['Party', 'Vote Share (%)', 'Constituencies']]
        st.dataframe(
            summary_df.sort_values('Vote Share (%)', ascending=False),
            height=500
        )

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 1rem;'>
        <p>Data Source: Election Commission of India</p>
        <p>Dashboard created with Streamlit</p>
    </div>
""", unsafe_allow_html=True)