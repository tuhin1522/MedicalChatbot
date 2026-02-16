import logging
from datetime import datetime
from pathlib import Path
from .config import config

# Ensure log directory exists
log_dir = Path(config.LOG_DIR)
log_dir.mkdir(parents=True, exist_ok=True)

# Configure logging
log_file = log_dir / f'chatbot_{datetime.now().strftime("%Y%m%d")}.log'
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('MedicalChatbot')

# Test logging
logger.info("Medical Chatbot logging initialized")
logger.info(f"Log level: {config.LOG_LEVEL}")

print("Logging configured successfully!")