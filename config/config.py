import anthropic
from dotenv import load_dotenv

# loading of env component for the anthropic key
load_dotenv()

# The model parameters
client = anthropic.Anthropic()
MODEL = "claude-haiku-4-5-20251001"

# the timing parameters
WINDOW_MINUTES = 30
TIME_KEYS = ("timestamp", "created", "ts", "posted_at", "fetched_at")

# The alert\prompt
alert = "[ALERT] PIX success_rate below 85% for 10m — provider=ProviderX region=BR. First error in payment-router-prod at 2026-08-11 14:12 UTC."

# the mock path
mockpath = "info_collector_output.mock.json"
