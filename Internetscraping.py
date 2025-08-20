import os
import json
import logging
import subprocess
import requests
from bs4 import BeautifulSoup
from termcolor import colored

# Setup logging for file operations and error logging
logging.basicConfig(level=logging.INFO)

def load_config(config_file='config.json'):
    """Load configuration from the JSON file."""
    with open(config_file, 'r') as file:
        return json.load(file)

def create_directories(directories):
    """Create directories based on the config."""
    for dir_name, path in directories.items():
        if not os.path.exists(path):
            print(f"Creating directory: {path}")
            os.makedirs(path, exist_ok=True)

def log_operation(log_file, message):
    """Log the operation to a log file."""
    with open(log_file, 'a') as log:
        log.write(message + '\n')
    logging.info(message)

def log_error(error_message):
    """Log error messages to a log file."""
    with open('error_log.txt', 'a') as file:
        file.write(f"ERROR: {error_message}\n")

def connect_to_ai(config):
    """Connect to the AI service using the config."""
    base_url = config["ollama-chat"]["openAICompatible"]["baseUrl"]
    api_key = config["ollama-chat"]["openAICompatible"]["apiKey"]
    models = config["ollama-chat"]["openAICompatible"]["models"]

    # Prepare the headers for API requests
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    # Set up the AI service
    ai_service = {
        "base_url": base_url,
        "headers": headers,
        "models": models
    }

    return ai_service

def run_ollama_query(model, prompt):
    """Run a query on Ollama model via subprocess."""
    command = f"ollama run {model} \"{prompt}\""
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        
        # Filter out everything before the actual response
        if "Thinking..." in result.stdout:
            final_output = result.stdout.split("...done thinking.")[-1].strip()
        else:
            final_output = result.stdout.strip()
        
        return final_output
    except Exception as e:
        log_error(f"Error running Ollama query: {str(e)}")
        raise Exception(f"Error running Ollama query: {str(e)}")

def scrape_website(url):
    """Scrape the website content using BeautifulSoup."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise error if the request failed
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract text content, remove unwanted tags (like scripts, styles)
        text_content = soup.get_text(separator=" ", strip=True)
        return text_content[:1500]  # Limit the amount of text returned (to avoid too much data)
    
    except requests.RequestException as e:
        log_error(f"Error scraping website: {str(e)}")
        print(colored(f"Error scraping website: {str(e)}", "red"))
        return None

def update_memory(memory_file, memory):
    """Update the memory file with the latest conversation."""
    with open(memory_file, 'w') as file:
        json.dump(memory, file, indent=4)

def main():
    # Load the configuration
    config = load_config('config.json')

    # Define directories to create (this part can be customized as needed)
    directories = {
        "input_dir": "ollama-chat/input",
        "output_dir": "ollama-chat/output",
        "logs_dir": "ollama-chat/logs"
    }
    
    # Perform filesystem operations if necessary
    create_directories(directories)

    # Log the directory creation
    log_file = config['ollama-chat'].get("log_file", "ollama-chat/logs/process_log.txt")
    log_operation(log_file, "Directories created successfully.")

    # Connect to the AI service
    ai_service = connect_to_ai(config)

    # Initialize memory (this could be loaded from a file, but here we use an empty dictionary initially)
    memory_file = 'conversation_memory.json'
    memory = {}
    
    try:
        while True:
            prompt = input(colored(f"👤: Enter a prompt (or type 'exit' to quit, '/model' to change model, '/memory' to view memory, '/scrape' to scrape a website): ", "yellow"))
            
            # Handle exit
            if prompt.lower() == 'exit':
                print(colored("Goodbye! 👋", "red"))
                break

            # Handle model change
            if prompt.lower() == '/model':
                print(f"Available models: {', '.join(ai_service['models'])}")
                selected_model = input("Choose a model from the available options: ")
                if selected_model not in ai_service["models"]:
                    print(f"Model '{selected_model}' is not available. Please select a valid model.")
                    continue

            # Handle memory view
            elif prompt.lower() == '/memory':
                print(colored(f"Memory: {json.dumps(memory, indent=2)}", "cyan"))

            # Handle web scraping
            elif prompt.lower() == '/scrape':
                url = input(colored("Enter the URL to scrape: ", "cyan"))
                scraped_content = scrape_website(url)
                if scraped_content:
                    print(colored(f"Scraped content: {scraped_content[:500]}...", "green"))
                    memory['scraped_content'] = scraped_content
                    continue

            # Handle normal conversation or queries
            else:
                if memory.get("last_prompt"):
                    print(colored(f"👤 Last prompt: {memory['last_prompt']}", "magenta"))
                else:
                    print(colored("No previous memory available.", "red"))

                # Run query with selected model
                selected_model = ai_service["models"][0]  # Default to the first model if not changed
                try:
                    ai_response = run_ollama_query(selected_model, prompt)
                    print(colored(f"🤖 {selected_model} says: {ai_response}", "green"))
                    
                    # Update memory with the conversation
                    memory["last_prompt"] = prompt
                    memory["last_response"] = ai_response

                    # Log AI response
                    log_operation(log_file, f"Model: {selected_model}, Response: {ai_response}")
                    update_memory(memory_file, memory)
                except Exception as e:
                    print(f"Error querying {selected_model}: {str(e)}")
                    log_error(f"Error querying {selected_model}: {str(e)}")

    except KeyboardInterrupt:
        print("\nProcess interrupted. Exiting gracefully...")
        exit(0)

if __name__ == '__main__':
    main()
