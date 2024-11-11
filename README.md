This ai challenge project enables you to answer user questions based on context from a PDF document and post them directly to a Slack channel. 
It leverages OpenAI's language model for question-answering and uses LangChain for a Retrieval-Augmented Generation (RAG) setup.
It is capable of parsing PDF text, using GPT model to answer the questions based on provided pdf context, and seamlessly posting them to Slack.

Project Structure:

zania_ai_challenge/
├── src/
│   ├── pdf_parser.py
│   ├── qa_agent.py
│   ├── slack_client.py
│   └── app.py
├── data/
│   └── handbook.pdf
├── log/
│   └── logger.log
├── config.yaml
├── requirements.txt
├── README.md
└── .env

Requirements:

  Python 3.7+
  An OpenAI API key (for question-answering)
  A Slack API token (for posting messages)

Setup:

  Clone the repository:

    git clone https://github.com/tathyum-gits/zania_ai_challenge
    cd zania_ai_challenge

  Install dependencies:

    pip install -r requirements.txt

  Configure API Keys:

	Follow the instructions in the API Key Setup section below to add your API keys to the environment.

  Environment Variables Setup:

    Populate the .env file with your OpenAI and Slack API keys.

  Configuring the config.yaml File
    
    To run this code, configure the config.yaml file located in the project root. The file includes the following configuration options:

      pdf_path: The path to the PDF file you want to analyze. Place your PDF files in the data/ folder for easy access.
      questions: A list of questions you want the bot to answer.
      slack_channel: The Slack channel where the bot will post the answers.
      
      Example config.yaml

      pdf_path: "data/handbook.pdf"  # Path to the PDF file
      questions:
        - "What is the name of the company?"
        - "Who is the CEO of the company?"
        - "What is their vacation policy?"
        - "What is the termination policy?"
      slack_channel: "#zania-ai-challenge"  # Slack channel to post answers

  Usage
    
    Add your PDF file to the data/ folder:

		Place the PDF file you want to analyze in the data/ folder for easy organization. Make sure the pdf_path in config.yaml correctly points to this file.

    Edit the config.yaml File:

      Update the pdf_path, questions, and slack_channel fields in config.yaml with the desired values.

    Run the Bot:

      python app.py

    The app will read the config.yaml file, extract text from the specified PDF, answer the questions, and post the answers to the specified Slack channel.

  API Key Setup
  
    To run this bot, you’ll need to configure your OpenAI and Slack API keys.

      OpenAI API Key:

        Add OpenAI API key to your .env file as follows:

          OPENAI_API_KEY=your_openai_api_key
      
      Slack API Token:

        Option 1: Set up Your Own Slack App:
        
          Create a Slack app by following the instructions at Slack API page.
          Add the chat:write scope under OAuth & Permissions to allow the bot to post messages.
          Install the app to your Slack workspace to retrieve the OAuth token.
          Add the token to your .env file as follows:

          SLACK_API_TOKEN=your_slack_api_token

        Option 2: Use Provided Test Credentials:
        
          If setting up a new Slack app is not feasible, you may use our test credentials to verify the bot's functionality:
          
          Slack API Token: test_slack_api_key (provided seperately)
  Logging

      This project uses logging to record important events and errors. Logs are written to both the console and a file named logger.log in the log directory.

  