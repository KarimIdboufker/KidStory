import streamlit as st
import requests

# Load the custom styles
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Main app
def main():
    # Load styles and set title
    load_css("assets/style.css")
    st.title("Custom Comic Generator")

    # Dropdown menus for user input
    characters = st.multiselect("Choose characters:", ["Knight", "Dragon", "Princess", "Wizard"])
    setting = st.selectbox("Choose the setting:", ["Castle", "Forest", "Village"])
    action = st.selectbox("Choose the action:", ["Battle", "Treasure Hunt", "Magic Spell"])
    ending = st.selectbox("Choose the ending:", ["Victory", "Friendship", "Discovery"])

    # Submit button
    if st.button("Generate Comic"):
        with st.spinner("Generating your comic..."):
            # Request story
            story_payload = {"characters": characters, "setting": setting, "action": action, "ending": ending}
            story_response = requests.post("http://backend:8000/generate_story", json=story_payload).json()

            # Request images
            image_payload = {"characters": characters, "setting": setting, "action": action, "ending": ending}
            image_response = requests.post("http://backend:8000/generate_images", json=image_payload).json()

            # Display story and images
            for page in story_response["pages"]:
                st.image(image_response["images"][page["index"]], use_column_width=True)
                st.markdown(f"### {page['text']}")

if __name__ == "__main__":
    main()
