import streamlit as st

st.set_page_config(
    page_title="AI Quantity Takeoff",
    page_icon="🏗️"
)

st.title("🏗️ AI Quantity Takeoff Assistant")

st.write(
    "Capture or upload a floor plan image from your mobile phone."
)


uploaded_file = st.camera_input(
    "Take a photo of your floor plan"
)


if uploaded_file:

    st.success("Floor plan captured successfully!")

    st.image(
        uploaded_file,
        caption="Captured Floor Plan",
        use_container_width=True
    )


    if st.button("Analyze Drawing"):

        st.info(
            "AI analysis will be connected in the next step."
        )
