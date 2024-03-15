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
    prompt = "この画像は何を表している?50文字以内で説明して。"

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


def get_ad_category(
    image_path: str, image_info: dict[str, str], category_list: list[str]
) -> dict[str, str]:
    """広告の情報から、広告カテゴリを取得する
    args:
        image_info: dict[str, str]
        ex)
        {
            "タイトル": "タイトル",
            "CTAテキスト": "CTAテキスト",
            "画像説明": "GPT-4-Visionで検知した画像説明文",
        }

    return dict[str, str]:
        ex)
        {
            "image_path": "path/to/image",
            "category": "分類カテゴリ",
        }
    """
    prompt = f"""
    出力はJSON形式で返すようにしてください。

    [質問内容]
    「タイトル・CTAテキスト・画像説明」の入力から、商品カテゴリに分類してください。
    商品カテゴリは、カテゴリリストから1つ選択してください。もしどのカテゴリにも分類できない場合は、「その他」に分類してください。

    [入力]
    タイトル:{image_info["タイトル"]}
    CTAテキスト:{image_info["CTAテキスト"]}
    画像説明:{image_info["画像説明"]}

    [出力形式JSON]
    {{
        "image_path": {image_path},
        "category": カテゴリリストから1つ選択,
    }}

    [カテゴリリスト]
    {category_list}
    """
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        temperature=0.0,
        messages=[
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
    )
    return response.choices[0].message.content


application_json = {
    "タイトル": "「究極の可愛さ！フルーツパラダイス」",
    "CTAテキスト": "「今すぐ遊んでみよう！」",
    "画像説明": detect_gpt_4_vision(
        encode_image("data/ad_image/application.png"), "png"
    ),
}

category_list = [
    "有料道路",
    "美容",
    "コスメ",
    "衣服",
    "スポーツ用品",
    "コンビニ",
    "電化製品",
    "ペット",
    "小児科",
    "保育園" "カード返済",
    "固定電話",
    "携帯電話",
    "インターネット",
    "WEBサービス",
    "ゲーム",
    "飲食",
]

book_json = {
    "タイトル": "「今宵のお楽しみ」",
    "CTAテキスト": "キャンペーンをチェック！",
    "画像説明": detect_gpt_4_vision(encode_image("data/ad_image/book.png"), "png"),
}

chocolate_json = {
    "タイトル": "「感性を刺激する、上質なチョコレート体験」",
    "CTAテキスト": "今すぐ味わう",
    "画像説明": detect_gpt_4_vision(
        encode_image("data/ad_image/chocolate.jpg"), "jpeg"
    ),
}

hatomugi_json = {
    "タイトル": "「肌悩みに革命を！独自成分で実現するクリアスキン」",
    "CTAテキスト": "限定価格で購入する",
    "画像説明": detect_gpt_4_vision(encode_image("data/ad_image/hatomugi.png"), "png"),
}


res = get_ad_category("data/ad_image/hatomugi.png", hatomugi_json, category_list)

print(res)
