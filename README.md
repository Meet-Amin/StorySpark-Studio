# StorySpark Studio

StorySpark Studio transforms your images into narrated adventures. Upload up to ten visual prompts, pick a genre, and let Gemini craft a cohesive tale while gTTS brings it to life as an audio story.

## Working Demo
Check out the live demo here: [StorySpark Studio](https://storysparkstudio.streamlit.app)

## Features
- Upload between 1 and 10 JPG/PNG images as visual prompts.
- Choose a genre such as Comedy, Thriller, Fairy Tale, Sci-Fi, Mystery, Adventure, or Morale.
- Gemini (`gemini-2.0-flash-lite`) stitches the visuals into a unified story with optional moral/twist sections.
- gTTS converts the story to speech so you can listen immediately in the browser.

## Prerequisites
- Python 3.11+ (matching the current virtual environment used in development).
- A Google AI Studio API key with access to the Gemini models.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:
```
GOOGLE_API_KEY=your_api_key_here
```

## Running the App
Use Streamlit’s runner so session state and widgets work correctly:
```bash
streamlit run app.py
```

Then open the local URL printed in the terminal (usually `http://localhost:8501`). Upload your images, pick a style, and click **Generate Story**. The story appears on the page along with the synthesis.

## Project Structure
```
app.py            # Streamlit UI and orchestration
story_generator.py# Gemini + prompt logic + gTTS narration helper
requirements.txt  # Python dependencies
.env              # Not checked in; holds GOOGLE_API_KEY
```

## Notes & Troubleshooting
- If you see `ValueError: API key not found`, confirm the `.env` file uses the exact key name `GOOGLE_API_KEY` with no quotes or spaces.
- Run `streamlit run app.py` instead of `python app.py`; otherwise you’ll get “missing ScriptRunContext” warnings and session state won’t work.
- The app currently targets `gemini-2.0-flash-lite`. To try a different model, update `MODEL = genai.GenerativeModel(...)` in `story_generator.py.