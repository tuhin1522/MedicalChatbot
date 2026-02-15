# Step 7: Import conversational components (with memory)
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from ..core.logging_config import logger

memory = ConversationBufferWindowMemory(
    k=4,  # 🔑 CRITICAL: Limit to last 4 Q&A pairs (8 messages)
    memory_key="chat_history",
    return_messages=True,
    output_key="answer"
)

print("✅ Conversational imports loaded!")
print("   - ConversationalRetrievalChain: Handles memory-aware retrieval")
print("   - ConversationBufferWindowMemory: Stores LAST 4 Q&A pairs (prevents overflow)")

logger.info("Conversation window memory initialized with k=4")
print("✅ Conversation Memory Created!")
print(f"   Type: ConversationBufferWindowMemory")
print(f"   Window Size: k=4 (last 4 Q&A pairs = 8 messages)")

print(f"   Purpose: Prevents memory overflow while maintaining context")
print(f"   This fixes the 12-message problem!")