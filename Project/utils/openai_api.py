import os
from decouple import config
from openai import OpenAI

# 환경 변수에서 API 키 로드
api_key = config('OPENAI_API_KEY')

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=api_key)

# 예제 프롬프트로 대화 생성
def generate_dialogue(prompt, model="gpt-4o", max_tokens=150, temperature=0.7, top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0):
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
    )
    return response

# 프롬프트 예제
prompt = "Create a dialogue between two Americans at a restaurant."
dialogue = generate_dialogue(prompt)

# 결과를 대화 형식으로 출력
for choice in dialogue.choices:
    message_content = choice.message.content.strip()
    messages = message_content.split('\n\n')
    for message in messages:
        print(message)
        print("\n")

# 사용된 토큰 수 출력
total_tokens = dialogue.usage.total_tokens
print(f"Total tokens used: {total_tokens}")
