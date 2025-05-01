import os
import openai
from openai import OpenAI
from dotenv import load_dotenv
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI()

@csrf_exempt
def gpt_request(request):
    if request.method == "POST":
        client = OpenAI()
        try:
            data = json.loads(request.body)
            user_message = data.get("message")
            #user_name = data.get("name")
            #DB에서user_name 비교해서 description 가져오기
            print(user_message)

            if not user_message:
                return JsonResponse({"error": "No message provided"}, status=400)

            response = client.chat.completions.create(
                model="gpt-4.1-nano",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant., 코드의 최적화를 목적으로 분석하고 개선해야할 점을 알려줘, 한글로 해줘 중요한 부분만 300자 이내로 설명해줘"},
                    {"role": "user", "content": user_message }
                ],
                temperature=0.7,
                max_tokens=300,
                top_p=1.0,
            )
            


            reply = response.choices[0].message.content.strip()


            #여기서 DB에 reply 저장

            return JsonResponse({"reply": reply}, status=200)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)