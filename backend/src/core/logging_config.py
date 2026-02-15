import logging
from datetime import datetime
from .config import config

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'chatbot_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('MedicalChatbot')

# Test logging
logger.info("Medical Chatbot logging initialized")
logger.info(f"Log level: {config.LOG_LEVEL}")

print("Logging configured successfully!")