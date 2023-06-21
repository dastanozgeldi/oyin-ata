import openai

BASE_PROMPT = """I'm going to send you a client's request for portfolio page and you need answer with code only, don't include questions and explanations. Here is the example.

Me: write a hello world page in html
You: 
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
</head>
<body>
  <h1>Hello World!</h1>
</body>
</html>

So here is the request:
{}"""


class CodeGeneration:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key

    def generate_html_game(self, prompt: str):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": BASE_PROMPT.format(prompt),
                }
            ],
        )
        response = completion.choices[0].message.content
        print(response)

        return response
