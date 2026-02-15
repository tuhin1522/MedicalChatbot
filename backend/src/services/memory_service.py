from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from ..core import config, logger

memory = ConversationBufferWindowMemory(
    k=config.MEMORY_WINDOW_SIZE,  # Limit to last N Q&A pairs
    memory_key="chat_history",
    return_messages=True,
    output_key="answer"
)

logger.info(f"Conversation window memory initialized with k={config.MEMORY_WINDOW_SIZE}")