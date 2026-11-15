"""Start the test mailbox of Chapter 22:  python run_mailbox.py

Emails sent to localhost port 1025 are printed here and saved in
output/mailbox/. Press Ctrl+C to stop.
"""
import time

from toolkit.mailbox import start_test_mailbox

box = start_test_mailbox()
print("Test mailbox running on localhost:1025. Press Ctrl+C to stop.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    box.stop()
