

import openai

import dotenv
dotenv.load_dotenv()

openai_client = openai.OpenAI()


def generate_image(prompt):
    response = openai_client.images.generate(
        model="dall-e-3",
        prompt=prompt,
    )
    return response.data[0].url




if __name__ == "__main__":
    print(generate_image("A painting of a cat in the style of Picasso"))