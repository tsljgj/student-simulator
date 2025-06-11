import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = "gpt-4o-mini"  # Using the current model name
    
    # File paths
    KC_MASTERY_FILE = "data/kc_mastery.json"
    PROMPTS_DIR = "prompts/"
    
    # Student simulation settings
    MAX_TOKENS = 150
    TEMPERATURE = 0.7
    
    @staticmethod
    def validate():
        """Validate that required configuration is present"""
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        os.makedirs("prompts", exist_ok=True)