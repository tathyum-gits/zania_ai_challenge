import os
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from typing import Dict

class SlackClient:
    """A client for posting messages to a Slack channel."""

    def __init__(self, token: str = None):
        """
        Initializes the SlackClient with an API token.

        Args:
            token (str): The Slack API token. If None, it reads from the environment variable `SLACK_API_TOKEN`.
        """
        self.token = token or os.getenv("SLACK_API_TOKEN")
        if not self.token:
            raise ValueError("Slack API token is not set. Please set it as an environment variable or pass it directly.")
        
        self.client = WebClient(token=self.token)

    def post_answers(self, channel: str, answers: Dict[str, str]) -> None:
        """
        Posts a structured message with question-answer pairs to a Slack channel.

        Args:
            channel (str): The Slack channel to post the message to (e.g., '#general').
            answers (Dict[str, str]): A dictionary of questions and their corresponding answers.
        """
        try:
            # Format the message content with questions and answers
            message = self.format_message(answers)
            
            # Send message to the specified Slack channel
            response = self.client.chat_postMessage(
                channel=channel,
                text=message
            )
            logging.info("Message sent to Slack, timestamp: %s", response['ts'])
        
        except SlackApiError as e:
            error_message = e.response["error"]
            logging.error("Error posting to Slack: %s", error_message)
            raise RuntimeError(f"Failed to post message to Slack: {error_message}")
    
    def format_message(self, answers: Dict[str, str]) -> str:
        """
        Formats the answers in a user-friendly format for Slack.

        Args:
            answers (Dict[str, str]): A dictionary of questions and answers.

        Returns:
            str: A formatted string ready for posting to Slack.
        """
        message = "Here are the answers to your questions:\n"
        for question, answer in answers.items():
            message += f"*{question}*\n> {answer}\n\n"
        return message
