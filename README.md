Ollama Chat is a privacy-focused, speed-optimized command-line interface (CLI) tool that integrates with an AI model, capable of performing tasks like summarizing websites, answering questions, and handling conversations. It uses a combination of web scraping and AI to provide insightful and accurate responses. Currently, the /scrape feature allows the AI to inject website knowledge into its memory upon receiving a URL in the prompt. This feature is in progress but demonstrates how the AI can effectively process and summarize web pages.

Key Features

AI Model Integration: Ollama Chat integrates with OpenAI-like models for natural language understanding, capable of generating responses to prompts.

Website Scraping: When a URL is provided, the program scrapes the website, extracts relevant information, and injects the knowledge into the AI's memory. The AI can then summarize the content and answer any questions about it.

Memory System: The AI can remember the last prompt and response, making it context-aware for follow-up questions.

Logging System: Keeps logs of all operations to help trace actions and identify potential errors.

Speed and Privacy: Designed for both speed and privacy, this tool doesn’t store any sensitive information externally. Everything happens locally, ensuring user data isn’t shared unless explicitly done so by the user.

How to Use

Run the Script:

Simply run the Python script: python Internetscraping.py

Interact with the AI:

Ask questions or provide prompts for the AI to respond to.

If you want the AI to scrape a website and summarize it, simply enter a URL in the prompt, such as:What is https://getpocket.com/explore/item/the-science-behind-why-some-of-us-are-shy?utm_source=firefox-newtab-en-us about?
The AI will scrape the page and respond with a summary of the content.
Commands:

/model: Change the AI model being used.

/memory: View the current memory of the AI.

/scrape: Scrape a website by entering a URL.

Exit: Type "exit" to end the session.

Required Packages

Before running the program, make sure the following Python packages are installed:

os: For interacting with the operating system (creating directories, file operations).

json: To handle configuration files and memory data.

logging: For logging events and errors.

subprocess: To run external commands (such as running the AI model through a terminal).

requests: To send HTTP requests for website scraping.

beautifulsoup4: To parse and extract data from HTML documents.

termcolor: For adding color to terminal outputs (makes the UI more readable).

You can install the necessary dependencies by running:pip install requests beautifulsoup4 termcolor
Configuration

The script expects a config.json file containing the following configurations:

openAICompatible: The AI model setup, including the API key and model names.

log_file: The location where log files are saved.

Sample config.json format:{
  "ollama-chat": {
    "openAICompatible": {
      "baseUrl": "http://localhost:11434",
      "apiKey": "your-api-key-here",
      "models": ["gpt-oss:20b", "deepseek-r1:32b"]
    },
    "log_file": "ollama-chat/logs/process_log.txt"
  }
}
Notes:
Privacy: The program is built with privacy in mind and doesn’t store or send data externally unless you explicitly provide it. All operations run locally on your machine.

Speed Optimization: Designed to be fast and efficient, the program optimizes scraping and model queries for quicker response times.

Future Work

The /scrape feature is still in development, and additional improvements are expected in future versions. Currently, it only works when a valid URL is provided within a prompt, allowing the AI to scrape and store knowledge about the website in its memory.

Conclusion

Ollama Chat is a simple but powerful tool that showcases AI integration with web scraping. It offers a unique way to interact with AI models while focusing on privacy, speed, and convenience. Perfect for anyone who wants a quick and easy way to extract knowledge from the web using an AI-powered CLI tool.
