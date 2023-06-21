import os
from dotenv import load_dotenv
from code_generation import CodeGeneration

from github import GitHub


def main():
    load_dotenv()

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GITHUB_PERSONAL_ACCESS_TOKEN = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")

    user = "dastanozgeldi"
    repo = "yerassyl_portfolio_page"

    github = GitHub(GITHUB_PERSONAL_ACCESS_TOKEN)
    github.create_repo(
        repo,
        "😸 All this was done with the power of GitHub API and OpenAI API.",
    )

    code_generation = CodeGeneration(OPENAI_API_KEY)
    html_content = code_generation.generate_html_game(
        "I want to build a basic html portfolio. I'm Yerassyl, 15 yo react developer specializing in Next.js, currently building full stack apps in fintech field. Add some styles to the page in dark mode, center the content both horizontally and vertically and give a width of around 60ch."
    )

    github.upload_file(
        user,
        repo,
        "index.html",
        html_content,
        "upload test commit",
    )

    github.deploy(user, repo, "main")


if __name__ == "__main__":
    main()
