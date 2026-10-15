import google.generativeai as genai
from backend.config import settings
import json

genai.configure(api_key=settings.GEMINI_API_KEY)

def analyze_medical_text(text: str):
    if not settings.GEMINI_API_KEY:
        print("WARNING: GEMINI_API_KEY is not set. Mocking AI response for development.")
        return {
            "summary": "[MOCK] Your report looks normal based on the text extracted.",
            "observations": [
                {"test": "Hemoglobin", "value": "13.5", "reference_range": "12-16", "status": "Normal"}
            ],
            "out_of_range_values": [],
            "simple_explanation_en": "[MOCK] This is a simple explanation in English.",
            "simple_explanation_ta": "[MOCK] இது ஒரு எளிய தமிழ் விளக்கம்.",
            "questions_for_doctor": ["What does this mean?", "Should I change my diet?"],
            "follow_up_notes": ["Consult your general physician for a formal diagnosis."]
        }

    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""
        You are a medical AI assistant. Analyze the following medical report text.
        Extract key information and return it STRICTLY as a JSON object with the following keys:
        - "summary": A brief, simple summary of the report.
        - "observations": A list of objects with "test", "value", "reference_range", "status" (e.g., Normal, High, Low).
        - "out_of_range_values": A list of objects with "test", "value", "status".
        - "simple_explanation_en": A simple explanation of the results for a layperson in English.
        - "simple_explanation_ta": A simple explanation of the results for a layperson in Tamil.
        - "questions_for_doctor": A list of questions the patient could ask their doctor.
        - "follow_up_notes": A list of general recommendations (e.g., "Consult your doctor").

        IMPORTANT RULES:
        * Do not diagnose.
        * Do not prescribe medication.
        * Do not invent values. Use only extracted report information.
        * Clearly distinguish abnormal values.
        * Explain uncertainty.
        * Recommend professional consultation when appropriate.

        Report Text:
        {text}
        """

        response = model.generate_content(prompt)
        response_text = response.text
        if response_text.startswith("```json"):
            response_text = response_text[7:-3]
        elif response_text.startswith("```"):
            response_text = response_text[3:-3]

        return json.loads(response_text)
    except Exception as e:
        print(f"Error calling AI API: {e}")
        return None
