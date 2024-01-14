import os
import base64
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
client = OpenAI()


def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def detect_gpt_4_vision(base64_image: str, image_type: str) -> str:
    prompt = "この画像は何を表している?「アニメの画像」「アプリの画像」のどちらかで回答してください。"

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/{image_type};base64,{base64_image}",
                            # 高解像度を求める場合は、detail: highを指定する
                        },
                    },
                ],
            }
        ],
        max_tokens=1000,
    )
    return response.choices[0].message.content


base64_image = encode_image("data/ad_image/application.png")
print(detect_gpt_4_vision(base64_image, "png"))
