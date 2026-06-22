# Acne Analyzer

## Decscription

This web app allows users to upload an image file (jpg, jpeg, or png) which is passed
to OpenAI's GPT-4o Vision API to analyze the user's uploaded photo of their face and
generate skincare recommendations based on the type and severity of the acne.

## Why?

I built this app because I have struggled with rather severe acne since 7th grade and
wanted to see how well AI can recommend and diagnose my acne compared to my dermatologist. I see this project as a first-stepping-stone to eventually building a full fledged AI-driven app to help people understand and treat their acne.

## Tech Stack

Backend --> Python and Flask
AI --> OpenAI API (GPT-4o Vision)
Frontend --> HTML, CSS, JavaScript
Libraries --> Pillow, python-dotenv, Werkzeug, Markdown

## How to Run

1. Clone the repository

2. Install dependencies

   pip install -r requirements.txt

3. Set up environment variables

   Create a new '.env' file in the root directory and add OpenAI API key

4. Run the app

```bash
    python app.py
```

5. Open your browser and go to:

   http://127.0.0.1:5000
