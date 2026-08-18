import streamlit as st

st.set_page_config(
    page_title="AI Quantity Takeoff",
    page_icon="🏗️"
)

st.title("🏗️ AI Quantity Takeoff Assistant")

st.write(
    "Upload an architectural floor plan and get AI-based quantity estimation."
)

uploaded_file = st.file_uploader(
    "Upload Floor Plan (PDF/Image)",
    type=["png", "jpg", "jpeg", "pdf"]
)

if uploaded_file:

    st.success("Floor plan uploaded successfully!")

    if uploaded_file.type != "application/pdf":
        st.image(uploaded_file, caption="Uploaded Floor Plan")

    if st.button("Analyze Drawing"):

        st.subheader("Quantity Takeoff Result")

        data = {
            "Item": [
                "Floor Area",
                "Floor Tile",
                "Wall Paint",
                "Brickwork"
            ],
            "Estimated Quantity": [
                "120 m²",
                "126 m²",
                "350 m²",
                "30 m³"
            ]
        }

        st.table(data)

        st.info(
            "Note: This is a prototype. AI vision and automatic measurement will be integrated next."
        )
