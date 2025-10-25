import streamlit as st
from PIL import Image

from story_generator import generate_story_from_images, narrate_story


st.title("AI Story Generator from images")
st.markdown("Upload an 1 to 10 images and let the AI generate a story for you!")

# Sidebar for file upload
with st.sidebar:
    st.header("Controls")
    uploaded_files = st.file_uploader(
       "Upload Images", type=["png", "jpg", "jpeg"],
        accept_multiple_files=True
   )
    
    #selecting an story style
    story_style= st.selectbox(
        "Choose a story style",
        ("Comedy", "Thriller", "Fairy Tale", "Sci-Fi", "Mystery", "Adventure", "Morale")
    )
    paragraph_count = st.slider(
        "Story length (paragraphs)", min_value=3, max_value=6, value=4
    )
    generate_button =st.button("Generate Story", type="primary")

    # MAIN LOGIC
if generate_button:
    if not uploaded_files: # This line was causing the error
        st.warning("Please upload atlest 1 image.")
    elif len(uploaded_files)>10:
        st.warning("Please upload an maximum of 10 images.")
    else:
        with st.spinner("The AI is writing  and narrating your story..... This may take few moments."):
            try:
                pil_images= [Image.open(uploaded_file) for uploaded_file in  uploaded_files]
                st.subheader("Your visual Inspiration:")
                image_columns= st.columns(len(pil_images))

                for i ,image in enumerate(pil_images):
                    with image_columns[i]:
                        st.image(image, use_container_width=True)

                generate_story= generate_story_from_images(
                    pil_images, story_style, paragraph_count
                )
                if "Error" in generate_story or "failed" in generate_story or"API key" in generate_story:
                    st.error(generate_story)
                else:
                    st.subheader(f"Your {story_style} story: ")
                    st.success(generate_story)


                st.subheader("Listen to your Story:")
                audio_file= narrate_story(generate_story)
                if isinstance(audio_file, str):
                    st.error(audio_file)
                elif audio_file:
                    audio_bytes = audio_file.getvalue()
                    st.audio(audio_bytes,format="audio/mp3")
                    st.download_button(
                        "Download narration",
                        data=audio_bytes,
                        file_name="storyspark-story.mp3",
                        mime="audio/mpeg",
                    )

            except Exception as e:
                st.error(f"An application  error occurred {e}")
