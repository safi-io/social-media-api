from fastapi import HTTPException
from google import genai
from google.genai import types


def get_gemini_response(prompt: str, system_instructions: str, extra_details: str) -> str:
    client = genai.Client()
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=f"{system_instructions}, and specific information is {extra_details}",
            )
        )
        return response.text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error calling Gemini API: {e}")
