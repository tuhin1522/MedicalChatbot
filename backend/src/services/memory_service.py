from typing import Dict, Optional
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from ..core import config, logger


class SessionMemoryManager:
    """Manages separate conversation memories for different sessions"""
    
    def __init__(self):
        self._memories: Dict[str, ConversationBufferWindowMemory] = {}
        self._default_session = "default"
        logger.info("Session memory manager initialized")
    
    def get_memory(self, session_id: Optional[str] = None) -> ConversationBufferWindowMemory:
        """
        Get or create memory for a specific session
        
        Args:
            session_id: Unique session identifier (None uses default session)
            
        Returns:
            ConversationBufferWindowMemory: Memory instance for the session
        """
        session_key = session_id or self._default_session
        
        if session_key not in self._memories:
            self._memories[session_key] = ConversationBufferWindowMemory(
                k=config.MEMORY_WINDOW_SIZE,
                memory_key="chat_history",
                return_messages=True,
                output_key="answer"
            )
            logger.info(f"Created new memory for session: {session_key}")
        
        return self._memories[session_key]
    
    def clear_memory(self, session_id: Optional[str] = None):
        """
        Clear memory for a specific session or all sessions
        
        Args:
            session_id: Session to clear (None clears all sessions)
        """
        if session_id:
            if session_id in self._memories:
                self._memories[session_id].clear()
                logger.info(f"Cleared memory for session: {session_id}")
        else:
            # Clear all memories
            for mem in self._memories.values():
                mem.clear()
            self._memories.clear()
            logger.info("Cleared all session memories")
    
    def get_session_count(self) -> int:
        """Get number of active sessions"""
        return len(self._memories)


# Global session memory manager
memory_manager = SessionMemoryManager()

# For backward compatibility - default memory (deprecated, use memory_manager instead)
memory = memory_manager.get_memory()

logger.info(f"Conversation window memory initialized with k={config.MEMORY_WINDOW_SIZE}")