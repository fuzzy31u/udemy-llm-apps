# udemy-llm-apps + my sample app

* Here is a sample app that I created while taking the Udemy course "ChatGPTのAPIで5つのアプリを作ってみよう！JSON生成、属性抽出、独自文書Q&A、SQL生成、AIエージェント" by しま (大嶋勇樹)
* My sample app is a simple chatbot that can post to X automatically based on the user's input with Google Calendar API and X API.

## How to use
This app is on th dev container, so you can run it on your local machine.

1. Clone this repository
2. Open the repository in VS Code
3. Open the dev container
4. Run the app
```bash
$ poetry run streamlit run home.py 
```
5. Access the app on your browser like `http://localhost:8501/post_x_with_calendar`

## Note
* This app is just a sample app and not for practical use.
* This app is running with [make](https://make.com/) and OpenAI's API so you need to set up the make automations.
* You need to write these secrets or make URLs in the `.streamlit/secrets.toml` file.
```toml
OPENAI_API_KEY = "your_openai_api_key"
MAKE_WEBHOOK_CALENDAR_URL = "your_make_webhook_calendar_url"
MAKE_WEBHOOK_CALENDAR_SEARCH_URL = "your_make_webhook_calendar_search_url"
MAKE_WEBHOOK_X_URL = "your_make_webhook_x_url"
```
