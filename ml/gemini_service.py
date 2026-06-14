import google.generativeai as genai
from django.conf import settings
import json
import base64


class GeminiInjuryAnalyzer:

    def __init__(self):
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')

    # ──────────────────────────────────────────────────────
    #  التحليل الرئيسي: يقبل نصاً + قائمة صور (bytes)
    # ──────────────────────────────────────────────────────
    def analyze_injury(self, student_name, student_activity,
                       injury_description='', image_bytes_list=None):
        """
        Analyze injury from text description and/or medical report images.
        Returns JSON with full medical analysis.
        """

        prompt = f"""You are an expert sports medicine physician.

Student: {student_name}
Sport/Activity: {student_activity}
{"Patient description: " + injury_description if injury_description else ""}
{"Medical report images are attached." if image_bytes_list else ""}

Analyze the injury and return ONLY valid JSON (no markdown, no extra text):
{{
    "injury_type": "e.g. Ankle Sprain",
    "affected_body_part": "e.g. Right Ankle",
    "severity_percentage": 65,
    "severity_level": "mild | moderate | severe",
    "rest_days": 7,
    "rehab_exercises": [
        "Exercise 1 description",
        "Exercise 2 description",
        "Exercise 3 description"
    ],
    "nutrition_advice": "Detailed nutritional recommendations",
    "light_training_return_days": 5,
    "full_competition_return_days": 14,
    "emergency_warnings": [
        "Warning 1",
        "Warning 2"
    ],
    "academic_impact": {{
        "affects_study": true,
        "days_affected": 3,
        "notes": "Student may need to rest at home for 3 days"
    }},
    "recommendation_summary": "Overall medical recommendation in 2-3 sentences."
}}"""

        try:
            # بناء محتوى الطلب (نص + صور)
            content_parts = [prompt]

            if image_bytes_list:
                for img_bytes in image_bytes_list:
                    content_parts.append({
                        "mime_type": "image/jpeg",
                        "data": base64.b64encode(img_bytes).decode('utf-8')
                    })

            response = self.model.generate_content(content_parts)
            text = response.text.strip()

            # تنظيف Markdown إن وُجد
            if text.startswith('```json'):
                text = text[7:]
            if text.startswith('```'):
                text = text[3:]
            if text.endswith('```'):
                text = text[:-3]
            text = text.strip()

            result = json.loads(text)
            return {"success": True, "data": result}

        except json.JSONDecodeError as e:
            return {"success": False, "error": f"JSON parse error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ──────────────────────────────────────────────────────
    #  تقرير مجمّع لرئيس القسم
    # ──────────────────────────────────────────────────────
    def generate_report_for_chef(self, injuries_data):
        prompt = f"""Analyze this injury data from university student athletes:
{json.dumps(injuries_data, ensure_ascii=False, indent=2)}

Provide a concise department head report covering:
1. Total injuries summary
2. Top 3 injury-causing activities
3. Most common injury types
4. Prevention recommendations
5. Students needing urgent follow-up

Write in clear English, professional tone."""

        try:
            response = self.model.generate_content(prompt)
            return {"success": True, "report": response.text}
        except Exception as e:
            return {"success": False, "error": str(e)}


gemini_service = GeminiInjuryAnalyzer()