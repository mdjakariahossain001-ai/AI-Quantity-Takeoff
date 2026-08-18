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
    "Capture a floor plan using mobile camera and generate AI-based quantity estimation."
)


# ---------------------------------
# Mobile Camera / Upload Section
# ---------------------------------

st.header("📷 Capture Floor Plan")


camera_image = st.camera_input(
    "Take a photo of your floor plan"
)


uploaded_file = st.file_uploader(
    "Or upload Floor Plan PDF/Image",
    type=["png", "jpg", "jpeg", "pdf"]
)



if camera_image:

    st.success("Floor plan captured successfully!")

    st.image(
        camera_image,
        caption="Captured Floor Plan",
        use_container_width=True
    )


elif uploaded_file:

    st.success("Floor plan uploaded successfully!")

    if uploaded_file.type != "application/pdf":

        st.image(
            uploaded_file,
            caption="Uploaded Floor Plan",
            use_container_width=True
        )



st.divider()



# ---------------------------------
# Load JSON Files
# ---------------------------------

def load_json(filename):

    if not os.path.exists(filename):

        st.error(
            f"{filename} not found"
        )

        st.stop()


    with open(filename, "r") as file:

        return json.load(file)



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
            Length: {room['length_ft']} ft

            Width: {room['width_ft']} ft

            Area: {room['area_sqft']} sqft
            """
        )



# ---------------------------------
# Quantity Results
# ---------------------------------

st.header("📊 Quantity Takeoff Result")



# Floor

st.subheader("🟫 Floor Finish")


floor_result = quantity["floor_finish_takeoff"]


st.write(
    f"""
    Floor Area:

    {floor_result['base_interior_floor_area_sqft']} sqft


    Wastage:

    {floor_result['wastage_factor_percent']} %


    Required Tile:

    {floor_result['total_tile_quantity_required_sqft']} sqft
    """
)



# Brick

st.subheader("🧱 Brick Masonry")


brick = quantity["brick_masonry_takeoff"]


st.write(
    f"""
    External Wall:

    {brick['external_walls']['net_volume_cuft']} cubic ft


    Internal Wall:

    {brick['internal_walls']['net_volume_cuft']} cubic ft


    Total Brickwork:

    {brick['totals']['total_net_volume_cuft']} cubic ft
    """
)



# Painting

st.subheader("🎨 Painting")


paint = quantity["wall_painting_takeoff"]


st.write(
    f"""
    External Painting:

    {paint['external_painting_surface_one_face_sqft']['net_area_sqft']} sqft


    Internal Painting:

    {paint['internal_painting_surface_sqft']['total_net_internal_painting_area_sqft']} sqft
    """
)



# ---------------------------------
# Doors Windows
# ---------------------------------

st.header("🚪 Openings")


opening = quantity["openings_summary"]


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "Doors",
        opening["doors"]["count"]
    )


with col2:

    st.metric(
        "Windows",
        opening["windows"]["count"]
    )



# ---------------------------------
# Assumptions
# ---------------------------------

st.header("⚙️ Construction Assumptions")


st.json(
    assumptions
)



st.divider()


st.caption(
    "Prototype workflow: Mobile Capture → LLM Interpretation → Building Model → Quantity Takeoff"
)
