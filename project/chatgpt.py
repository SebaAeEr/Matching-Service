import openai
import numpy as np
import os


# model = whisper.load_model("medium.en")
# result = model.transcribe("currentVM.wav")
# print(result["text"])

openai.api_key = os.getenv(
    "CHAT_GPT_KEY", "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"
)


def ask_chatgpt(string1, string2, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": 'Do the following strings convey similar information? "'
                + string1
                + '" and "'
                + string2
                + '". Please answer with only yes or no.',
            },
        ],
    )

    print(response.choices[0].message)
    return "yes" in response.choices[0].message["content"].lower()


def embedding_chatgpt(
    string1, string2, model="text-similarity-davinci-001", threshold=0.1
):
    embedding1 = openai.Embedding.create(input=string1, model=model)["data"][0][
        "embedding"
    ]

    embedding2 = openai.Embedding.create(
        input=string2, model="text-similarity-davinci-001"
    )["data"][0]["embedding"]

    dist = np.linalg.norm(np.array(embedding1) - np.array(embedding2))
    return dist <= threshold


# ask_chatgpt("Hello I am Sebastian.", "Hello my name is Sebastian.")
# embedding_chatgpt("Hello I am Sebastian.", "Hello my name is Sebastian.")
