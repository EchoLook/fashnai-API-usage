import os
import time
import json
import requests
import streamlit as st
from dotenv import load_dotenv
import base64
import io
from PIL import Image

# Load environment variables
load_dotenv()

# Get API key from environment variable
API_KEY = os.getenv("FASHN_API_KEY")
if not API_KEY:
    st.warning("FASHN_API_KEY not set. API calls will fail.")
    API_KEY = "dummy_key"

# API endpoints
RUN_ENDPOINT = "https://api.fashn.ai/v1/run"
STATUS_ENDPOINT = "https://api.fashn.ai/v1/status/"

def encode_image_to_base64(image):
    """Convert an image to base64 string."""
    if isinstance(image, str):
        # Assuming it's a file path
        with open(image, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    else:
        # Assuming it's a PIL image or bytes
        if isinstance(image, Image.Image):
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            encoded_string = base64.b64encode(buffered.getvalue()).decode("utf-8")
        else:
            # Assuming it's bytes
            encoded_string = base64.b64encode(image).decode("utf-8")
    
    return f"data:image/jpeg;base64,{encoded_string}"

def try_on_clothes(model_image, garment_image, category="auto"):
    """
    Process virtual try-on using Fashn.ai API.
    
    Args:
        model_image: Image of the model
        garment_image: Image of the garment
        category: Category of clothing ('auto', 'tops', 'bottoms', 'one-pieces')
        
    Returns:
        Result image or status message
    """
    # Show processing message
    with st.spinner("Processing your request..."):
        # Prepare API request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        
        # Convert images to base64
        model_base64 = encode_image_to_base64(model_image)
        garment_base64 = encode_image_to_base64(garment_image)
        
        # Prepare request payload
        payload = {
            "model_image": model_base64,
            "garment_image": garment_base64,
            "category": category
        }
        
        # Submit job to API
        try:
            response = requests.post(RUN_ENDPOINT, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            
            if "error" in result and result["error"]:
                return None, f"Error: {result['error']}"
            
            job_id = result["id"]
            
            # Create a progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Poll for results
            max_attempts = 40  # Maximum 40 seconds wait time with 1 second polling
            for attempt in range(max_attempts):
                # Update progress
                progress = min(0.95, attempt / max_attempts)
                progress_bar.progress(progress)
                status_text.text(f"Processing... ({attempt + 1}/{max_attempts}s)")
                
                # Sleep for a second
                time.sleep(1)
                
                # Check status
                status_response = requests.get(
                    f"{STATUS_ENDPOINT}{job_id}", 
                    headers={"Authorization": f"Bearer {API_KEY}"}
                )
                status_data = status_response.json()
                
                if status_data["status"] == "completed":
                    # Download the result image
                    output_url = status_data["output"][0]
                    result_image = requests.get(output_url).content
                    
                    # Save the result image
                    result_path = f"images/results/result_{int(time.time())}.jpg"
                    os.makedirs(os.path.dirname(result_path), exist_ok=True)
                    with open(result_path, "wb") as f:
                        f.write(result_image)
                    
                    # Complete the progress bar
                    progress_bar.progress(1.0)
                    status_text.empty()
                    
                    return Image.open(result_path), "Processing completed successfully!"
                
                elif status_data["status"] == "failed":
                    status_text.empty()
                    progress_bar.empty()
                    return None, f"Processing failed: {status_data.get('error', 'Unknown error')}"
            
            status_text.empty()
            progress_bar.empty()
            return None, "Processing timed out. Check status manually with job ID."
        
        except requests.exceptions.RequestException as e:
            return None, f"API request error: {str(e)}"

# Set up the Streamlit page
st.set_page_config(page_title="Virtual Try-On App", layout="wide")
st.title("Virtual Try-On App")
st.write("Upload a picture of a person and a clothing item to see how the clothing would look on the person.")

# Create two columns for inputs and outputs
col1, col2 = st.columns(2)

with col1:
    st.subheader("Upload Images")
    
    # Tabs for different input methods for the model image
    model_tab1, model_tab2 = st.tabs(["📁 Upload Person Image", "📷 Take Photo"])
    
    with model_tab1:
        model_image_upload = st.file_uploader("Upload Person Image", type=["jpg", "jpeg", "png"], key="model_upload")
    
    with model_tab2:
        st.write("Take a photo of yourself with the camera")
        model_image_camera = st.camera_input("Take a picture", key="model_camera")
    
    # Get the model image from either the upload or camera
    model_image = model_image_upload if model_image_upload is not None else model_image_camera
    
    # Tabs for different input methods for the garment image
    garment_tab1, garment_tab2 = st.tabs(["📁 Upload Garment Image", "📷 Take Photo"])
    
    with garment_tab1:
        garment_image_upload = st.file_uploader("Upload Clothing Item Image", type=["jpg", "jpeg", "png"], key="garment_upload")
    
    with garment_tab2:
        st.write("Take a photo of the clothing item with the camera")
        garment_image_camera = st.camera_input("Take a picture", key="garment_camera")
    
    # Get the garment image from either the upload or camera
    garment_image = garment_image_upload if garment_image_upload is not None else garment_image_camera
    
    # Display selected images
    cols_preview = st.columns(2)
    with cols_preview[0]:
        if model_image is not None:
            st.write("Selected person image:")
            st.image(model_image, width=150)
    
    with cols_preview[1]:
        if garment_image is not None:
            st.write("Selected garment image:")
            st.image(garment_image, width=150)
    
    # Category selection
    category = st.selectbox("Clothing Category", ["auto", "tops", "bottoms", "one-pieces"])
    
    # Submit button
    submit_button = st.button("Generate Try-On")

# Initialize session state to store results
if "result_image" not in st.session_state:
    st.session_state.result_image = None
if "result_message" not in st.session_state:
    st.session_state.result_message = ""

# Process images when the button is clicked
if submit_button:
    if model_image is not None and garment_image is not None:
        # Read image data
        model_bytes = model_image.getvalue()
        garment_bytes = garment_image.getvalue()
        
        # Process the images
        result_image, result_message = try_on_clothes(model_bytes, garment_bytes, category)
        
        # Store results in session state
        st.session_state.result_image = result_image
        st.session_state.result_message = result_message
    else:
        st.error("Please provide both a person image and a clothing item image.")

# Display the results
with col2:
    st.subheader("Results")
    
    # Display result message
    if st.session_state.result_message:
        if st.session_state.result_message.startswith("Error") or st.session_state.result_message.startswith("Processing failed"):
            st.error(st.session_state.result_message)
        elif st.session_state.result_message.startswith("Processing completed"):
            st.success(st.session_state.result_message)
        else:
            st.info(st.session_state.result_message)
    
    # Display result image
    if st.session_state.result_image is not None:
        st.image(st.session_state.result_image, caption="Try-On Result", use_column_width=True)
        
        # Add download button for the result
        if st.session_state.result_image:
            # Convert the PIL image to bytes
            buf = io.BytesIO()
            st.session_state.result_image.save(buf, format="JPEG")
            byte_im = buf.getvalue()
            
            st.download_button(
                label="Download Result",
                data=byte_im,
                file_name=f"virtual_tryon_result_{int(time.time())}.jpg",
                mime="image/jpeg"
            )
    
    # Show placeholder when no result is available
    if st.session_state.result_image is None and not st.session_state.result_message:
        st.info("Your try-on result will appear here.")

# Display sample images
st.markdown("---")
st.subheader("How it works")
st.write("""
1. Upload a photo of a person or take one with your camera
2. Upload a photo of a clothing item or take one with your camera
3. Select the appropriate category (or leave as "auto")
4. Click "Generate Try-On" and wait for the results
5. Processing may take up to 40 seconds
6. Download your result if you like it!
""")

# Footer
st.markdown("---")
st.caption("Powered by Fashn.ai API - Visit https://docs.fashn.ai/fashn-api/endpoints for more information") 