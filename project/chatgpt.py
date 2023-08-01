import openai
import numpy as np
import os

chat_gpt_key = ""
openai.api_key = os.getenv("CHAT_GPT_KEY", chat_gpt_key)


def ask_chatgpt(string1, string2, model="gpt-3.5-turbo"):
    """
    Write the question 'Do the following strings convey similar information? "phrase 1" and "phrase 2". Please answer with only yes or no.' to chatgpt.
    Returns boolean if the answer is 'yes'.
    """

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
    """
    Calculate the distance of the vectors representing the strings using openai.
    Returns if the distance is lower than the given threshold.
    """

    embedding1 = openai.Embedding.create(input=string1, model=model)["data"][0][
        "embedding"
    ]

    embedding2 = openai.Embedding.create(
        input=string2, model="text-similarity-davinci-001"
    )["data"][0]["embedding"]

    dist = np.linalg.norm(np.array(embedding1) - np.array(embedding2))
    return dist <= threshold
