import streamlit as st
import json
import os


# ---------------------------------
# Page Configuration
# ---------------------------------

st.set_page_config(
    page_title="AI Quantity Takeoff",
    page_icon="🏗️",
    layout="centered"
)


# ---------------------------------
# Title
# ---------------------------------

st.title("🏗️ AI Quantity Takeoff Assistant")

st.write(
    "LLM-based architectural drawing interpretation and quantity estimation"
)


# ---------------------------------
# Function to load JSON
# ---------------------------------

def load_json(filename):

    if not os.path.exists(filename):
        st.error(f"Missing file: {filename}")
        st.stop()

    with open(filename, "r") as file:
        return json.load(file)



# ---------------------------------
# Load Data
# ---------------------------------

building_model = load_json(
    "Plan_001_Building_Model.json"
)

assumptions = load_json(
    "Construction_Assumptions.json"
)

quantity = load_json(
    "Quantity_Takeoff_Result.json"
)



# ---------------------------------
# Building Information
# ---------------------------------

st.header("🏢 Building Information")


info = building_model["building_information"]


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "Project",
        info["project_name"]
    )


with col2:

    st.metric(
        "Location",
        info["location"]
    )


st.write(
    "Unit System:",
    info["unit_system"]
)

st.write(
    "Drawing:",
    info["sheet_referenced"]
)



# ---------------------------------
# Area Information
# ---------------------------------

st.header("📐 Area Information")


floor = building_model["floor_information"]


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "Gross Footprint",
        f'{floor["gross_footprint_area_sqft"]} sqft'
    )


with col2:

    st.metric(
        "Interior Area",
        f'{floor["total_dimensioned_interior_area_sqft"]} sqft'
    )



# ---------------------------------
# Room Information
# ---------------------------------

st.header("🚪 Room Information")


rooms = building_model["rooms"]


for room in rooms:

    with st.expander(
        f"{room['name']} - {room['unit']}"
    ):

        st.write(
            f"""
            **Length:** {room['length_ft']} ft

            **Width:** {room['width_ft']} ft

            **Area:** {room['area_sqft']} sqft
            """
        )



# ---------------------------------
# Quantity Takeoff Results
# ---------------------------------

st.header("📊 Quantity Takeoff Result")



# Floor Finish

st.subheader("🟫 Floor Finish")

floor_finish = quantity["floor_finish_takeoff"]


st.write(
    f"""
    Base Floor Area:
    {floor_finish['base_interior_floor_area_sqft']} sqft


    Wastage:
    {floor_finish['wastage_factor_percent']} %


    Required Tile Quantity:
    {floor_finish['total_tile_quantity_required_sqft']} sqft
    """
)



# Brick Masonry

st.subheader("🧱 Brick Masonry")


brick = quantity["brick_masonry_takeoff"]


st.write(
    f"""
    External Wall Volume:

    {brick['external_walls']['net_volume_cuft']} cubic ft


    Internal Wall Volume:

    {brick['internal_walls']['net_volume_cuft']} cubic ft


    Total Brickwork:

    {brick['totals']['total_net_volume_cuft']} cubic ft
    """
)



# Painting

st.subheader("🎨 Painting Quantity")


paint = quantity["wall_painting_takeoff"]


st.write(
    f"""
    External Painting Area:

    {paint['external_painting_surface_one_face_sqft']['net_area_sqft']} sqft


    Internal Painting Area:

    {paint['internal_painting_surface_sqft']['total_net_internal_painting_area_sqft']} sqft
    """
)



# ---------------------------------
# Openings
# ---------------------------------

st.header("🚪 Doors and Windows")


openings = quantity["openings_summary"]


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "Doors",
        openings["doors"]["count"]
    )


with col2:

    st.metric(
        "Windows",
        openings["windows"]["count"]
    )



# ---------------------------------
# Structural Information
# ---------------------------------

st.header("🏗️ Structural Elements")


structure = building_model["structural_elements"]


st.write(
    f"""
    Columns:
    {structure['columns']['count']}


    Staircase:
    {structure['staircase']['type']}


    Lift:
    {structure['lift']['area_sqft']} sqft
    """
)



# ---------------------------------
# Assumptions
# ---------------------------------

st.header("⚙️ Construction Assumptions")


st.json(assumptions)



# ---------------------------------
# Research Prototype Note
# ---------------------------------

st.divider()

st.caption(
    "Prototype: Mobile floor plan capture → LLM interpretation → Structured building model → Quantity takeoff"
)
