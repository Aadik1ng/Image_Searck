import streamlit as st
import requests

# Base URL of the Flask API
API_BASE_URL = "http://localhost:5000"

st.title("Image Embedding API Tester")

st.markdown("This tool tests the **/add**, **/delete**, and **/search** endpoints.")

# ------------------------------
# Section: Add Image
# ------------------------------
st.header("Add Image")
uploaded_file_add = st.file_uploader("Choose an image to add", type=["jpg", "jpeg", "png"], key="add")
if uploaded_file_add is not None:
    if st.button("Add Image"):
        files = {"image": uploaded_file_add}
        response = requests.post(f"{API_BASE_URL}/add", files=files)
        if response.ok:
            st.success("Image added successfully!")
            st.json(response.json())
        else:
            st.error("Failed to add image.")
            st.json(response.json())

# ------------------------------
# Section: Delete Image
# ------------------------------
st.header("Delete Image")
uploaded_file_delete = st.file_uploader("Choose an image to delete", type=["jpg", "jpeg", "png"], key="delete")
if uploaded_file_delete is not None:
    if st.button("Delete Image"):
        files = {"image": uploaded_file_delete}
        response = requests.delete(f"{API_BASE_URL}/delete", files=files)
        if response.ok:
            st.success("Image deleted successfully!")
            st.json(response.json())
        else:
            st.error("Failed to delete image.")
            st.json(response.json())

# ------------------------------
# Section: Search Image
# ------------------------------
st.header("Search Image")
query = st.text_input("Enter search query (e.g., 'A smiling person')")
if st.button("Search"):
    if query:
        params = {"q": query}
        response = requests.get(f"{API_BASE_URL}/search", params=params)
        if response.ok:
            st.success("Search successful!")
            result = response.json()
            st.json(result)
            image_path = result.get("image_path")
            if image_path:
                st.markdown("### Matching Image")
                # Note: This will work if your Flask app serves the static images.
                st.image(image_path, caption="Found Image", use_column_width=True)
        else:
            st.error("Search failed.")
            st.json(response.json())
    else:
        st.warning("Please enter a search query.")
