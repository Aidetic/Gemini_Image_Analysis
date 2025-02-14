import os
import tempfile
import streamlit as st
from ai_engine import analyze_car_images

# Initialize session state for refresh functionality
if "needs_rerun" not in st.session_state:
    st.session_state.needs_rerun = False

# Add refresh button at the top
if st.button("🔄 Start New Analysis"):
    # Clear all stored files and results
    st.session_state.needs_rerun = True
    st.rerun()  # Updated to use st.rerun() instead of experimental_rerun

if st.session_state.needs_rerun:
    # Reset the flag
    st.session_state.needs_rerun = False
    # The page will be clean at this point due to the rerun

st.title("Vehicle Image Analysis App")

st.write("Please upload exactly **4 images** of the vehicle for analysis.")

# Allow multiple file uploads
uploaded_files = st.file_uploader(
    "Upload 4 images",
    type=["png", "jpg", "jpeg", "webp"],
    accept_multiple_files=True,
    key="file_uploader",  # Added a key for better state management
)

# Check if files are uploaded
if uploaded_files:
    if len(uploaded_files) != 4:
        st.error("Error: You must upload exactly 4 images.")
    else:
        # Show the uploaded images in a grid
        cols = st.columns(4)
        for idx, uploaded_file in enumerate(uploaded_files):
            with cols[idx]:
                st.image(
                    uploaded_file, caption=f"Image {idx + 1}", use_container_width=True
                )

        if st.button("Analyze Vehicle"):
            # Show loading spinner
            with st.spinner("Analyzing images..."):
                image_paths = []
                try:
                    # Save each uploaded image to a temporary file
                    for uploaded_file in uploaded_files:
                        ext = os.path.splitext(uploaded_file.name)[1]
                        with tempfile.NamedTemporaryFile(
                            delete=False, suffix=ext
                        ) as tmp_file:
                            tmp_file.write(uploaded_file.getbuffer())
                            image_paths.append(tmp_file.name)

                    # Call the analysis function
                    result = analyze_car_images(image_paths)

                    # Display results in a nice format
                    st.subheader("Analysis Results")
                    st.write(result)

                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                finally:
                    # Clean up temporary files
                    for path in image_paths:
                        try:
                            os.unlink(path)
                        except:
                            pass
