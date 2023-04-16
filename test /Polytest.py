import unittest
from unittest.mock import MagicMock
from bot import Bot, QuoteBot
from loguru import logger


class TestBot(unittest.TestCase):

    def setUp(self):
        with open('.telegramToken') as f:
            _token = f.read()
        # create a mock updater object
        self.updater = MagicMock()

        # create a bot object with the mock updater
        self.bot = QuoteBot(_token)
        self.bot.updater = self.updater

    def test_send_text(self):
        # create a mock update object
        update = MagicMock()

        # call send_text method
        self.bot.send_text(update, 'Hello, world!')

        # assert that reply_text method was called with the expected arguments
        update.message.reply_text.assert_called_once_with('Hello, world!', quote=False)

    def test_send_text2(self):
        # create a mock update object
        update = MagicMock()
        # call send_text method
        self.bot.send_text(update, "Don't quote me please")

        # assert that reply_text method was called with the expected arguments
        update.message.reply_text.assert_called_once_with("Don't quote me please", quote=False)

    def test_message_handler(self):
        # create a mock update object
        update = MagicMock()

        # create a mock context object
        context = MagicMock()

        # call _message_handler method
        self.bot._message_handler(update, context)

        mock_send_text = MagicMock()
        self.bot.send_text = mock_send_text

        # Call the message handler
        self.bot._message_handler(update, context)

        # Assert that the send_text method was called once with the expected arguments
        mock_send_text.assert_called_once_with(update, f'Your original message: {update.message.text}', quote=True)

        # assert that send_text method was called with the expected arguments
        # self.bot.send_text.assert_called_once_with(update, f'Your original message: {update.message.text}')

    def test_start(self):
        # call start method
        self.bot.start()

        # assert that start_polling method was called
        self.updater.start_polling.assert_called_once()

        # assert that logger.info method was called with the expected arguments
        # logger.info.assert_called_once_with(f'{self.bot.__class__.__name__} is up and listening to new messages....')

        # assert that idle method was called
        self.updater.idle.assert_called_once()


if __name__ == '__main__':
    unittest.main()