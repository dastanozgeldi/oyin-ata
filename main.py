import os
import telebot
from dotenv import load_dotenv

from github import GitHub
from code_generation import CodeGeneration

load_dotenv()

bot = telebot.TeleBot(os.getenv("TELEGRAM_API_TOKEN"))


def handle_game(
    user: str = "dastanozgeldi", repo: str = "my_new_game", prompt: str = None
):
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GITHUB_PERSONAL_ACCESS_TOKEN = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")

    github = GitHub(GITHUB_PERSONAL_ACCESS_TOKEN)
    github.create_repo(
        repo,
        "😸 All this was done with the power of GitHub API and OpenAI API.",
    )

    code_generation = CodeGeneration(OPENAI_API_KEY)
    # "I want to build a basic html game. I'm Yerassyl, 15 yo react developer specializing in Next.js, currently building full stack apps in fintech field. Add some styles to the page in dark mode, center the content both horizontally and vertically and give a width of around 60ch."
    html_content = code_generation.generate_html_game(prompt)

    github.upload_file(
        user,
        repo,
        "index.html",
        html_content,
        "upload test commit",
    )

    url = github.deploy(user, repo, "main")
    return url


@bot.message_handler(commands=["start"])
def url(message):
    bot.send_message(
        message.from_user.id,
        "Hey there! I'm your web game builder bot. To get started use this command: /newgame",
    )


@bot.message_handler(commands=["newgame"])
def handle_newgame(message):
    chat_id = message.chat.id

    # Send a message to ask for the repository name
    bot.send_message(chat_id, "Please enter the project name, for example: dastan_snake_game")

    # Register the next message handler to receive the repository name
    bot.register_next_step_handler(message, process_repository_name)


def process_repository_name(message):
    repository_name = '-'.join(message.text.split())
    print('>', message.from_user.username, ':', repository_name)

    chat_id = message.chat.id

    # Send a message to ask for the prompt
    bot.send_message(chat_id, "Please enter the prompt for website generation:")

    # Store the repository name in the user's context (can be a dictionary)
    user_context = {"repository_name": repository_name}

    # Register the next message handler to receive the prompt
    bot.register_next_step_handler(message, process_prompt, user_context)


def process_prompt(message, user_context):
    prompt = message.text
    print('>', message.from_user.username, ':', prompt)
    # Retrieve the repository name from the user's context
    repository_name = user_context["repository_name"]

    url = handle_game("dastanozgeldi", repository_name, prompt)

    # Generate game using the repository name and prompt
    # game_page = generate_game(repository_name, prompt)
    # game_page = "https://dosek.xyz/"

    # Send the generated game page to the user
    bot.send_message(message.chat.id, f"Here is your game:\n{url}")


bot.infinity_polling()
