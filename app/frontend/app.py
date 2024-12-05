import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image

# Load the custom styles
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Backend URL configuration
BACKEND_URL = "http://localhost:8000"

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Main app
def main():
    add_bg_from_local('assets/your_image.jpg')
    # Load styles and set title
    load_css("assets/style.css")
    st.title("Custom Comic Generator")

    # Dropdown menus for user input
    characters = st.multiselect("Choose characters:", ["Nael","Naim","Knight", "Dragon", "Princess", "Wizard"], default=["Knight"])
    setting = st.selectbox("Choose the setting:", ["Space","Castle", "Forest", "Village"])
    action = st.selectbox("Choose the action:", ["Battle", "Treasure Hunt", "Adventure", "learning experience"])
    ending = st.selectbox("Choose the ending:", ["Victory", "Friendship", "Discovery", "Enigma"])

    # Submit button
    generate_button = st.button("Generate Comic", key="generate_button")
    
    if generate_button and characters:  # Ensure at least one character is selected
        with st.spinner("Generating your comic..."):
            try:
                # Request story
                story_payload = {"characters": characters, "setting": setting, "action": action, "ending": ending}
                story_response = requests.post(f"{BACKEND_URL}/generate_story", json=story_payload)
                if story_response.status_code != 200:
                    st.error(f"Error generating story: {story_response.text}")
                    return
                story_data = story_response.json()

                # Request images
                image_payload = story_payload  # Use the same payload
                image_response = requests.post(f"{BACKEND_URL}/generate_images", json=image_payload)
                if image_response.status_code != 200:
                    st.error(f"Error generating images: {image_response.text}")
                    return
                image_data = image_response.json()

                # Display story and images
                if story_data["status"] == "success" and image_data["status"] == "success":
                    for i, page in enumerate(story_data["pages"]):
                        if i < len(image_data["images"]):
                            # Convert base64 string back to image
                            img_bytes = base64.b64decode(image_data["images"][i])
                            img = Image.open(BytesIO(img_bytes))
                            st.image(img, use_container_width=True)
                        st.markdown(f"### {page['text']}")
                else:
                    st.error("Error in response from server")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the server: {str(e)}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    elif generate_button:  # Only show warning if button was clicked but no characters selected
        st.warning("Please select at least one character")

if __name__ == "__main__":
    main()
