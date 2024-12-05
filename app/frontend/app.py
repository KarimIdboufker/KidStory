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

# Main app
def main():
    # Load styles and set title
    load_css("assets/style.css")
    st.title("Custom Comic Generator")

    # State to manage pages
    if "current_page" not in st.session_state:
        st.session_state.current_page = 0

    # Dropdown menus for user input
    characters = st.multiselect("Choose characters:", ["Nael", "Naim", "Venom", "Maui", "Tyranosaurus Rex", "Godzilla"], default=["Nael", "Naim"])
    setting = st.selectbox("Choose the setting:", ["Space", "Castle", "Forest", "Beach", "London"])
    action = st.selectbox("Choose the action:", ["Battle", "Treasure Hunt", "Adventure", "Science experiment"])
    ending = st.selectbox("Choose the ending:", ["Funny", "Victory", "Discovery", "Enigma"])

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
                if "pages" in story_data and story_data["pages"]:
                    image_payload = {"story_paragraphs": [page["text"] for page in story_data["pages"]]}
                    image_response = requests.post(f"{BACKEND_URL}/generate_images", json=image_payload)
                    if image_response.status_code != 200:
                        st.error(f"Error generating images: {image_response.text}")
                        return
                    image_data = image_response.json()
                else:
                    st.error("No story pages received from the server")
                    return

                # Save story and images in session state
                if story_data["status"] == "success" and image_data["status"] == "success":
                    st.session_state.pages = [{"text": page["text"], "image": image_data["images"][i]}
                                              for i, page in enumerate(story_data["pages"])]
                    st.session_state.current_page = 0  # Reset to the first page
                else:
                    st.error("Error in response from server")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the server: {str(e)}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    elif generate_button:  # Only show warning if button was clicked but no characters selected
        st.warning("Please select at least one character")

    # Display the current page
    if "pages" in st.session_state:
        current_page = st.session_state.current_page
        pages = st.session_state.pages

        # Show image
        img_bytes = base64.b64decode(pages[current_page]["image"])
        img = Image.open(BytesIO(img_bytes))
        st.image(img, use_container_width=True)

        # Show story text in comic-style box
        st.markdown(
            f"""
            <div style="background-color: white; padding: 20px; border-radius: 10px; border: 2px solid black; text-align: center;">
                <p style="font-family: 'Comic Sans MS', cursive, sans-serif; font-size: 20px; color: black;">
                    {pages[current_page]["text"]}
                </p>
            </div>
            """, unsafe_allow_html=True
        )

        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("Previous", key="prev_button") and current_page > 0:
                st.session_state.current_page -= 1
        with col3:
            if st.button("Next", key="next_button") and current_page < len(pages) - 1:
                st.session_state.current_page += 1

if __name__ == "__main__":
    main()
