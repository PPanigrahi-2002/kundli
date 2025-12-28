
import os
from config import Config

print(f"Environment GROQ_API_KEY: {os.getenv('GROQ_API_KEY')}")
print(f"Config GROQ_API_KEY: {Config.GROQ_API_KEY}")
try:
    Config.validate_config()
    print("Validation: SUCCESS")
except Exception as e:
    print(f"Validation: FAILED ({e})")
