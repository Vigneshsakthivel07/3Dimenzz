import streamlit as st
import sys
from pathlib import Path

# Force Python to recognize the project root folder so 'core' can be imported
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd
from shapely.geometry import Polygon
from shapely.validation import make_valid

# Import custom modules
from core.geometry import build_fmb_polygon
from core.analytics import compare_polygons
from core.visuals import visualize_comparison
# 1. Page Configuration
st.set_page_config(page_title="FMB Copilot", layout="wide")
st.title("🗺️ FMB Survey Copilot - Live Testing")

# 2. Sidebar Layout for Inputs
with st.sidebar:
    st.header("Survey Measurements")
    st.write("Enter the paper FMB record data below.")
    
    g_line = st.number_input("G-Line Length (meters)", value=100.0)
    
    st.write("Offsets (Perpendicular measurements)")
    # Interactive table for the user to type in data
    default_data = pd.DataFrame({
        "Chainage": [20.0, 50.0, 80.0, 30.0, 70.0],
        "Offset": [15.0, 30.0, 10.0, 25.0, 20.0],
        "Side": ["left", "left", "left", "right", "right"]
    })
    
    edited_df = st.data_editor(default_data, num_rows="dynamic")
    generate_btn = st.button("Generate Map", type="primary")

# 3. Main Screen Layout for Output
if generate_btn:
    # Convert the interactive table into the format our math engine expects
    offsets = list(edited_df.itertuples(index=False, name=None))
    
    # Run our core engine
    fmb_polygon = build_fmb_polygon(g_line, offsets)
    
    # Mock GPS Data (We will connect real Bluetooth GPS here later)
    gps_polygon = make_valid(Polygon([
        (-1, 2), (19, 17), (52, 28), (81, 11), (102, 1), 
        (72, -18), (28, -26), (-1, 2)
    ]))
    
    # Split the screen: Map on the left, Data on the right
    col_map, col_data = st.columns([2, 1])
    
    with col_map:
        st.subheader("Boundary Overlay")
        fig = visualize_comparison(fmb_polygon, gps_polygon)
        st.pyplot(fig)
        
    with col_data:
        st.subheader("Dispute Analytics")
        metrics = compare_polygons(fmb_polygon, gps_polygon)
        
        # Display large metric cards for easy reading
        for key, value in metrics.items():
            st.metric(label=key, value=str(value))
            
        if metrics["Max Deviation (Hausdorff)"] > 2.0:
            st.error(f"⚠️ Warning: High boundary deviation detected ({metrics['Max Deviation (Hausdorff)']}m)")