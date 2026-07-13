# Translator 9000

A stylish Streamlit translation app for Spanish and English input, with Mandarin, French, and Japanese output.

## Run locally

1. Install the project dependencies:

   ```powershell
   uv sync
   ```

2. Add your OpenAI key. Create `.streamlit/secrets.toml` with:

   ```toml
   OPENAI_API_KEY = "your-api-key"
   ```

   Alternatively, set an `OPENAI_API_KEY` environment variable.

3. Start the app:

   ```powershell
   uv run streamlit run streamlit_app.py
   ```

The app uses the `gpt-3.5-turbo-0125` model from the original example. Change the `model` value in `streamlit_app.py` if your account uses a different model.
