# GenAI for Business - Course Sandbox

Welcome to the sandbox repository for the "Technical Foundations of Generative AI for Business" course. This repository provides a ready-to-use development environment in GitHub Codespaces, so you can start learning and experimenting with generative AI without worrying about local setup.

## Getting Started

To get started, you need to create your own repository from this template.

1.  **Create a new repository:** Click the "Use this template" button at the top of this page and select "Create a new repository."
2.  **Name your repository:** Give your new repository a name, for example, `genai-business-course`.
3.  **Launch the Codespace:** Once your repository is created, click the "<> Code" button, select the "Codespaces" tab, and click "Create codespace on main." This will launch a new development environment in your browser.

## Using the Codespace

Your Codespace comes with all the tools you need for this course:

*   **Python 3.13**
*   **uv:** A fast Python package installer and resolver.
*   **Gemini CLI:** A command-line interface for the Gemini API.
*   **Pre-configured secrets:** The Codespace is configured to use your `GEMINI_API_KEY` and `GOOGLE_API_KEY` secrets. You will need to add these to your GitHub account. See this documentation page: [Managing your account-specific secrets for GitHub Codespaces](https://docs.github.com/en/codespaces/managing-your-codespaces/managing-your-account-specific-secrets-for-github-codespaces)

> [!WARNING]
> Handle API keys with extreme caution. DO NOT COMMIT API KEYS TO GITHUB ALONG WITH YOUR CODE. 

### Gemini CLI

The Gemini CLI is a powerful tool for interacting with the Gemini API from the command line. To use it, you need to make sure that the `GEMINI_API_KEY` environment variable is set in your Codespace secrets.

Before using the Gemini CLI, make sure you are in the project directory:

```bash
cd /workspaces/chatbox
```

To start the Gemini CLI, you can simply run the following command:

```bash
gemini
```

This will start the Gemini CLI in interactive mode. You can then type your prompts directly into the terminal. To exit, press `Ctrl+C` twice.

### Terminal

You can open a new terminal in your Codespace by going to the "Terminal" menu and selecting "New Terminal" or pressing `CTRL` + `SHIFT` + `C`.

### Running the Example App

This repository includes a simple Streamlit application in `app.py`. To run it for the first time, open a terminal and enter the following command:

```bash
# Make sure you're in the project root directory
cd /workspaces/chatbox
# Create virtual environment and install dependencies
uv sync
# Run the app
uv run -- streamlit run app.py --server.enableCORS false --server.enableXsrfProtection false
```

> [!CAUTION]
>  The flags `--server.enableCORS false` and `--server.enableXsrfProtection false` are used to disable two security features in the Streamlit server. This is sometimes necessary to ensure the application runs correctly within the GitHub Codespaces environment. While this is safe to do in a development environment like Codespaces, you would typically not disable these features in a production application."

## Questions

If you have any questions, please reach out to your instructor.
