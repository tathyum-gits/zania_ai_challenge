import logging
import yaml
import os
from dotenv import load_dotenv
from qa_agent import QAModule
from pdf_parser import PDFParser
from slack_client import SlackClient

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("log\logger.log"),
        logging.StreamHandler()
    ]
)

def load_config(config_path="config.yaml"):
    with open(config_path, "r") as file:
        return yaml.safe_load(file)
    
def main(pdf_path: str, questions: list, slack_channel: str):
    """Main function to parse PDF, answer questions, and post results to Slack."""
    try:
        # Check if the PDF file exists
        if not os.path.isfile(pdf_path):
            logging.error("PDF file not found at path: %s", pdf_path)
            return
        
        # Parse the PDF
        logging.info("Parsing PDF from %s", pdf_path)
        parser = PDFParser(pdf_path)
        pdf_text = parser.parse()

        if not pdf_text:
            logging.warning("Parsed text from PDF is empty.")
            return

        # Answer sample questions based on contextual pdf
        logging.info("Answering sample questions")
        qa_agent = QAModule()
        answers = qa_agent.answer_questions(pdf_text, questions)

        # Post results to Slack
        logging.info("Posting results to Slack channel %s", slack_channel)
        slack_client = SlackClient()
        slack_client.post_answers(slack_channel, answers)
        logging.info("Successfully posted results to Slack")

    except Exception as e:
        logging.exception("An unexpected error occurred: %s", e)

if __name__ == "__main__":
    config = load_config()  # Load configuration from file
    
    pdf_path = config["pdf_path"]
    slack_channel = config["slack_channel"]
    questions = config["questions"]

    logging.info("Starting App")
    main(pdf_path, questions, slack_channel)
    logging.info("App finished execution")
