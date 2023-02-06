import logging

from classic.components import component

from simple_shop.application import interfaces


logger = logging.getLogger(__name__)


@component
class LogMailSender(interfaces.MailSender):
    """Simple sender for debugging"""

    level: int = logging.INFO

    def send(self, mail: str, title: str, text: str):
        logger.log(
            self.level,
            f'SendTo: {mail}\n'
            f'Title: {title}\n'
            f'Body: {text}\n'
        )
