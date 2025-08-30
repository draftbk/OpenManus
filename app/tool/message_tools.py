import requests
import json
from typing import Optional, List
from app.tool import BaseTool
from app.logger import logger


class DiscordWebhookTool(BaseTool):
    """Tool for sending messages via Discord webhook."""

    name: str = "send_discord_message"
    description: str = "Send a message to a Discord channel using a webhook URL."
    parameters: dict = {
        "type": "object",
        "properties": {
            "webhook_url": {
                "type": "string",
                "description": "Discord webhook URL",
            },
            "message": {
                "type": "string",
                "description": "Message content to send",
            },
            "username": {
                "type": "string",
                "description": "Custom username for the message (optional)",
                "default": "OpenManus Bot",
            },
            "avatar_url": {
                "type": "string",
                "description": "Avatar URL for the message (optional)",
            },
        },
        "required": ["webhook_url", "message"],
    }

    async def execute(
        self,
        webhook_url: str,
        message: str,
        username: str = "OpenManus Bot",
        avatar_url: Optional[str] = None,
    ) -> str:
        """
        Send a message to Discord using webhook.

        Args:
            webhook_url: Discord webhook URL
            message: Message content to send
            username: Custom username for the message
            avatar_url: Avatar URL for the message

        Returns:
            Success or error message
        """
        try:
            payload = {
                "content": message,
                "username": username,
            }

            if avatar_url:
                payload["avatar_url"] = avatar_url

            response = requests.post(webhook_url, json=payload, timeout=10)

            if response.status_code == 204:
                logger.info(f"Discord message sent successfully")
                return f"Discord message sent successfully!"
            else:
                error_msg = f"Failed to send Discord message. Status: {response.status_code}"
                logger.error(error_msg)
                return f"Error: {error_msg}"

        except requests.exceptions.RequestException as e:
            error_msg = f"Error sending Discord message: {e}"
            logger.error(error_msg)
            return f"Error: {error_msg}"
        except Exception as e:
            error_msg = f"Unexpected error: {e}"
            logger.error(error_msg)
            return f"Error: {error_msg}"


class SlackWebhookTool(BaseTool):
    """Tool for sending messages via Slack webhook."""

    name: str = "send_slack_message"
    description: str = "Send a message to a Slack channel using a webhook URL."
    parameters: dict = {
        "type": "object",
        "properties": {
            "webhook_url": {
                "type": "string",
                "description": "Slack webhook URL",
            },
            "message": {
                "type": "string",
                "description": "Message content to send",
            },
            "channel": {
                "type": "string",
                "description": "Channel name (optional, without #)",
            },
            "username": {
                "type": "string",
                "description": "Custom username for the message (optional)",
                "default": "OpenManus Bot",
            },
        },
        "required": ["webhook_url", "message"],
    }

    async def execute(
        self,
        webhook_url: str,
        message: str,
        channel: Optional[str] = None,
        username: str = "OpenManus Bot",
    ) -> str:
        """
        Send a message to Slack using webhook.

        Args:
            webhook_url: Slack webhook URL
            message: Message content to send
            channel: Channel name (optional)
            username: Custom username for the message

        Returns:
            Success or error message
        """
        try:
            payload = {
                "text": message,
                "username": username,
            }

            if channel:
                payload["channel"] = f"#{channel}"

            response = requests.post(webhook_url, json=payload, timeout=10)

            if response.status_code == 200 and response.text == "ok":
                logger.info(f"Slack message sent successfully")
                return f"Slack message sent successfully!"
            else:
                error_msg = f"Failed to send Slack message. Status: {response.status_code}, Response: {response.text}"
                logger.error(error_msg)
                return f"Error: {error_msg}"

        except requests.exceptions.RequestException as e:
            error_msg = f"Error sending Slack message: {e}"
            logger.error(error_msg)
            return f"Error: {error_msg}"
        except Exception as e:
            error_msg = f"Unexpected error: {e}"
            logger.error(error_msg)
            return f"Error: {error_msg}"


class TelegramBotTool(BaseTool):
    """Tool for sending messages via Telegram bot."""

    name: str = "send_telegram_message"
    description: str = "Send a message via Telegram bot."
    parameters: dict = {
        "type": "object",
        "properties": {
            "bot_token": {
                "type": "string",
                "description": "Telegram bot token",
            },
            "chat_id": {
                "type": "string",
                "description": "Chat ID or username (with @)",
            },
            "message": {
                "type": "string",
                "description": "Message content to send",
            },
        },
        "required": ["bot_token", "chat_id", "message"],
    }

    async def execute(
        self,
        bot_token: str,
        chat_id: str,
        message: str,
    ) -> str:
        """
        Send a message via Telegram bot.

        Args:
            bot_token: Telegram bot token
            chat_id: Chat ID or username
            message: Message content to send

        Returns:
            Success or error message
        """
        try:
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "HTML",
            }

            response = requests.post(url, json=payload, timeout=10)
            result = response.json()

            if result.get("ok"):
                logger.info(f"Telegram message sent successfully")
                return f"Telegram message sent successfully!"
            else:
                error_msg = f"Failed to send Telegram message: {result.get('description', 'Unknown error')}"
                logger.error(error_msg)
                return f"Error: {error_msg}"

        except requests.exceptions.RequestException as e:
            error_msg = f"Error sending Telegram message: {e}"
            logger.error(error_msg)
            return f"Error: {error_msg}"
        except Exception as e:
            error_msg = f"Unexpected error: {e}"
            logger.error(error_msg)
            return f"Error: {error_msg}"


class ConsoleMessageTool(BaseTool):
    """Tool for displaying messages in console (for testing)."""

    name: str = "send_console_message"
    description: str = "Display a message in the console (for testing purposes)."
    parameters: dict = {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "Message content to display",
            },
            "title": {
                "type": "string",
                "description": "Message title (optional)",
                "default": "OpenManus Message",
            },
        },
        "required": ["message"],
    }

    async def execute(
        self,
        message: str,
        title: str = "OpenManus Message",
    ) -> str:
        """
        Display a message in console.

        Args:
            message: Message content to display
            title: Message title

        Returns:
            Success message
        """
        print(f"\n{'='*50}")
        print(f"📧 {title}")
        print(f"{'='*50}")
        print(f"{message}")
        print(f"{'='*50}\n")

        logger.info(f"Console message displayed: {title}")
        return f"Message displayed in console: {title}"


class FileMessageTool(BaseTool):
    """Tool for saving messages to a file."""

    name: str = "save_message_to_file"
    description: str = "Save a message to a text file."
    parameters: dict = {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "Message content to save",
            },
            "filename": {
                "type": "string",
                "description": "Filename to save the message to",
                "default": "openmanus_message.txt",
            },
            "append": {
                "type": "boolean",
                "description": "Append to existing file (default: false)",
                "default": False,
            },
        },
        "required": ["message"],
    }

    async def execute(
        self,
        message: str,
        filename: str = "openmanus_message.txt",
        append: bool = False,
    ) -> str:
        """
        Save a message to a file.

        Args:
            message: Message content to save
            filename: Filename to save to
            append: Whether to append to existing file

        Returns:
            Success or error message
        """
        try:
            mode = "a" if append else "w"
            with open(filename, mode, encoding="utf-8") as f:
                f.write(f"{message}\n")

            logger.info(f"Message saved to file: {filename}")
            return f"Message saved to file: {filename}"

        except Exception as e:
            error_msg = f"Error saving message to file: {e}"
            logger.error(error_msg)
            return f"Error: {error_msg}"
