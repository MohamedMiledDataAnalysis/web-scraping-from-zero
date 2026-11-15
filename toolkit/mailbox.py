"""A test mailbox on your own computer, for the email alerts of Chapter 22.

It receives emails on localhost, port 1025, prints them and saves them in
output/mailbox/. Nothing ever leaves your computer.
"""
import logging
from pathlib import Path

from aiosmtpd.controller import Controller

logging.getLogger("mail.log").setLevel(logging.WARNING)   # keep the SMTP chatter quiet

BOX = Path("output/mailbox")


class _Handler:
    def __init__(self, quiet=False):
        self.quiet = quiet
        self.count = 0

    async def handle_DATA(self, server, session, envelope):
        BOX.mkdir(parents=True, exist_ok=True)
        self.count += 1
        text = envelope.content.decode("utf-8", errors="replace")
        (BOX / f"message_{self.count:03d}.eml").write_text(text, encoding="utf-8")
        if not self.quiet:
            subject = next((l for l in text.splitlines() if l.startswith("Subject:")), "")
            print(f"[mailbox] message {self.count} to {', '.join(envelope.rcpt_tos)}: {subject}")
        return "250 Message accepted"


def start_test_mailbox(port=1025, quiet=False):
    """Start the mailbox in the background; call .stop() on the result at the end."""
    controller = Controller(_Handler(quiet), hostname="127.0.0.1", port=port)
    controller.start()
    return controller
