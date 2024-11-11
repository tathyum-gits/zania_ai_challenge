
# Zania AI Challenge

This project is an AI-powered question-answering bot designed to answer user questions based on the context extracted from a PDF document and post the responses directly to a specified Slack channel. It leverages OpenAI's language model for question-answering and utilizes LangChain for a Retrieval-Augmented Generation (RAG) setup.

## Project Structure

```
zania_ai_challenge/
├── src/
│   ├── pdf_parser.py          # Parses PDF documents
│   ├── qa_agent.py            # Question-answering agent using OpenAI
│   ├── slack_client.py        # Posts messages to Slack
│   └── app.py                 # Main application file
├── data/
│   └── handbook.pdf           # Example PDF document
├── log/
│   └── logger.log             # Log file for recording events
├── config.yaml                # Configuration file
├── requirements.txt           # List of dependencies
├── README.md                  # Project documentation
└── .env                       # Environment variables for API keys
```

## Requirements

- Python 3.7+
- OpenAI API key (for question-answering functionality)
- Slack API token (for posting messages to a Slack channel)

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/tathyum-gits/zania_ai_challenge
cd zania_ai_challenge
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Keys
Follow the steps in the **API Key Setup** section below to configure your API keys in the `.env` file.

### 4. Environment Variables Setup

Create a `.env` file and add your OpenAI and Slack API keys:
```env
OPENAI_API_KEY=your_openai_api_key
SLACK_API_TOKEN=your_slack_api_token
```

### 5. Configuring the `config.yaml` File

In the project root, configure the `config.yaml` file with the following options:

- `pdf_path`: Path to the PDF document to analyze.
- `questions`: List of questions you want the bot to answer.
- `slack_channel`: Slack channel where the bot will post answers.

#### Example `config.yaml`

```yaml
pdf_path: "data/handbook.pdf"  # Path to the PDF file
questions:
  - "What is the name of the company?"
  - "Who is the CEO of the company?"
  - "What is their vacation policy?"
  - "What is the termination policy?"
slack_channel: "#zania-ai-challenge"  # Slack channel to post answers
```

### 6. Usage

1. **Add Your PDF**: Place the PDF file you want to analyze in the `data/` folder for easy organization. Ensure `pdf_path` in `config.yaml` points to this file.

2. **Edit `config.yaml`**: Update the `pdf_path`, `questions`, and `slack_channel` fields with desired values.

3. **Run the Bot**:
    ```bash
    python app.py
    ```
   The application will read the `config.yaml` file, extract text from the PDF, answer the questions, and post answers to the specified Slack channel.

## API Key Setup

To use this bot, configure your OpenAI and Slack API keys:

- **OpenAI API Key**: Add your OpenAI API key to `.env`:
  ```env
  OPENAI_API_KEY=your_openai_api_key
  ```
  
- **Slack API Token**:
  - **Option 1**: Set up your own Slack App.
    - [Create a Slack app](https://api.slack.com/apps) and add the `chat:write` scope under OAuth & Permissions to allow message posting.
    - Install the app to your Slack workspace to retrieve the OAuth token.
    - Add the token to your `.env` file:
      ```env
      SLACK_API_TOKEN=your_slack_api_token
      ```

  - **Option 2**: Use Provided Test Credentials.
    - If setting up a new Slack app isn’t feasible, you may use our test credentials to verify functionality.
    - **Slack API Token**: `test_slack_api_key` (provided separately)

## Logging

This project uses logging to record important events and errors. Logs are written to both the console and a file named `logger.log` in the `log` directory.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
