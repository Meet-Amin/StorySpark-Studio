import os
from io import BytesIO
from typing import List

from dotenv import load_dotenv
from gtts import gTTS
import google.generativeai as genai
from PIL import Image


load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set the GOOGLE_API_KEY environment variable.")

genai.configure(api_key=api_key)
MODEL = genai.GenerativeModel("gemini-2.0-flash-lite")


def create_advanced_prompt(style: str) -> str:
    base_prompt = f"""
    **Your Persona:** You are a friendly and engaging storyteller. Your goal is to tell a story that is fun and easy to read.
    **Your Main Goal:** Write a story in simple, clear, and modern English.
    **Your Task:** Create one single story that connects all the provided images in order.
    **Style Requirement:** The story must fit the '{style}' genre.
    **Core Instructions:**
    1.  **Tell One Single Story:** Connect all images into a narrative with a beginning, middle, and end.
    2.  **Use Every Image:** Include a key detail from each image.
    3.  **Creative Interpretation:** Infer the relationships between the images.
    4.  **Nationality**: Use only Indian Names,Characters, Places , Persona Etc.
    **Output Format:**
    -   **Title:** Start with a simple and clear title.
    -   **Length:** The story must be between 4 and 5 paragraphs.
    """

    style_instruction = ""
    if style == "Morale":
        style_instruction = "\n**Special Section:** After the story, you MUST add a section starting with the exact tag `[MORAL]:` followed by the single-sentence moral of the story."
    elif style == "Mystery":
        style_instruction = "\n**Special Section:** After the story, you MUST add a section starting with the exact tag `[SOLUTION]:` that reveals the culprit and the key clue."
    elif style == "Thriller":
        style_instruction = "\n**Special Section:** After the story, you MUST add a section starting with the exact tag `[TWIST]:` that reveals a final, shocking twist."

    return base_prompt + style_instruction


def _extract_story_text(response: genai.types.GenerateContentResponse) -> str:
    text = (getattr(response, "text", None) or "").strip()
    if text:
        return text

    parts: List[str] = []
    for candidate in getattr(response, "candidates", []) or []:
        content = getattr(candidate, "content", None)
        if not content:
            continue
        for part in getattr(content, "parts", []) or []:
            if getattr(part, "text", None):
                parts.append(part.text)
    return "\n".join(parts).strip()


def generate_story_from_images(images: List[Image.Image], style: str) -> str:
    if not images:
        raise ValueError("At least one image is required to generate a story.")

    contents = [img for img in images]
    contents.append(create_advanced_prompt(style))

    response = MODEL.generate_content(contents=contents)
    story = _extract_story_text(response)
    if not story:
        raise RuntimeError("The model returned an empty story.")
    return story


def narrate_story(story_text: str):
    try:
        tts = gTTS(text=story_text, lang="en", slow=False)
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        return audio_fp
    except Exception:
        return "An unexpected error occurred during the text-to-speech call."
