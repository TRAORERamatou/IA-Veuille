import os
import time

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# use gemini modal
model = genai.GenerativeModel("gemini-1.5-flash-latest")

def summarize_text(text: str, max_tokens: int = 200) -> str:
    if not text or len(text.strip()) < 30:
        return "Insufficient text for summary."

    prompt = f"Please provide a concise summary in English (between 10 and 20 sentences) of the following content:\n{text}"

    try:
        # Wait between requests to avoid exceeding quota
        time.sleep(4)
        response = model.generate_content(prompt)
        print(" summary:", response.text[:100], "...")
        return response.text.strip()
    except Exception as e:
        # Explicit handling of quota errors (429)
        err_text = str(e)
        if "429" in err_text:
            time.sleep(15)
            try:
                response = model.generate_content(prompt)
                print("Summary (2nd attempt)) :", response.text[:100], "...")
                return response.text.strip()
            except Exception as e2:
                print("Failed again:", e2)
                return "Summary unavailable"
        print(" Gemini error:", e)
        return "Summary unavailable"
