import os
import openai

# OpenAI API 키 초기화
openai.api_key = os.getenv("OPENAI_API_KEY")

# client 객체 생성
client = openai

# 만약 다른 모듈들이 client에 의존한다면, 추가 import 없이 client 객체만 노출합니다.