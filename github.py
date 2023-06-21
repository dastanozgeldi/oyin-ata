import json
import base64
import requests


class GitHub:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def create_repo(self, name: str, description: str):
        """Creates a GitHub repo"""
        data = {"name": name, "description": description}
        response = requests.post(
            "https://api.github.com/user/repos",
            headers=self.headers,
            data=json.dumps(data),
        )
        # print(r.status_code, r.content)

        print(f"✅ {response.status_code} - Repo created successfully.")

    def upload_file(
        self, user: str, repo: str, path: str, content: str, commit_message: str
    ):
        """Uploads static website to GitHub repo"""
        encoded_content = base64.b64encode(content.encode()).decode()
        upload_url = f"https://api.github.com/repos/{user}/{repo}/contents/{path}"
        data = {"message": commit_message, "content": encoded_content}

        response = requests.put(upload_url, headers=self.headers, data=json.dumps(data))

        if response.status_code == 201:
            print("✅ 201 - File uploaded successfully.")
        else:
            print(f"❌ {response.status_code} - Error uploading file:", response.content)

    def deploy(self, user: str, repo: str, branch: str):
        """Deploys the static website to GitHub Pages"""
        deploy_url = f"https://api.github.com/repos/{user}/{repo}/pages"
        data = {"source": {"branch": branch}}

        response = requests.post(
            deploy_url, headers=self.headers, data=json.dumps(data)
        )
        # print(response.json())
        print(f"✅ {response.status_code} - Changes sent to GitHub Pages successfully.")
        print(f"Check in a minute: https://{user}.github.io/{repo}/")
