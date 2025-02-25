# streamlit_app.py
import streamlit as st
import requests
import json
import os

# Set the API endpoint
API_URL = "http://127.0.0.1:5000"  # Adjust if your Flask app runs on a different URL

# Title of the app
st.title("Image Search with CLIP")

# Upload Image Section
st.header("Upload Image")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Save the uploaded file to the static/images directory
    image_path = os.path.join("static/images", uploaded_file.name)
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    st.success("Image uploaded successfully!")

# Search Section
st.header("Search Images")
query = st.text_input("Enter your search query:")
top_k = st.number_input("Number of top results to display:", min_value=1, max_value=20, value=5)

if st.button("Search"):
    if query:
        # Make a request to the search API
        response = requests.post(f"{API_URL}/search", json={"query": query, "top_k": top_k})
        if response.status_code == 200:
            results = response.json()
            if results:
                st.subheader("Search Results:")
                for result in results:
                    st.image(result["path"], caption=f"Similarity: {result['similarity']:.2f}", use_column_width=True)
            else:
                st.warning("No results found.")
        else:
            st.error("Error occurred while searching.")

# Add Embedding Section
st.header("Add New Embedding")
input_type = st.selectbox("Select input type:", ["image", "text"])
data = st.text_input("Enter image path or text query:")

if st.button("Add Embedding"):
    if input_type == "image" and uploaded_file is not None:
        # Use the uploaded image path
        data = image_path
    elif input_type == "text" and data:
        pass
    else:
        st.error("Please provide valid input.")

    # Make a request to add the embedding
    response = requests.post(f"{API_URL}/add", json={"input_type": input_type, "data": data})
    if response.status_code == 200:
        st.success("Embedding added successfully!")
    else:
        st.error("Error occurred while adding embedding.")

# Delete Embedding Section
st.header("Delete Embedding")
delete_input_type = st.selectbox("Select input type to delete:", ["image", "text"])
delete_data = st.text_input("Enter image path or text query to delete:")

if st.button("Delete Embedding"):
    # Make a request to delete the embedding
    response = requests.post(f"{API_URL}/delete", json={"input_type": delete_input_type, "data": delete_data})
    if response.status_code == 200:
        st.success("Embedding deleted successfully!")
    else:
        st.error("Error occurred while deleting embedding.")