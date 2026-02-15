import time
import uuid
from datetime import datetime
from ..core import config, logger
from .rag_service import conversational_qa

def conversational_chat():
    """
    Conversational chatbot with memory - FIXES follow-up question problem!
    
    DEPENDENCIES: config, logger, conversational_qa
    Features:
    - Remembers conversation history
    - Reformulates follow-up questions
    - Maintains topic continuity
    - Full logging and error handling
    """
    # Verify dependencies
    try:
        _ = (config, logger, conversational_qa)
    except NameError as e:
        print(f"❌ ERROR: Missing dependency - {e}")
        print("Please ensure you've run the required cells first!")
        return
    
    session_id = str(uuid.uuid4())[:8]
    conversation_count = 0
    
    logger.info(f"Starting conversational chat session: {session_id}")
    
    print("=" * 80)
    print("🏥 Medical Chatbot - Conversational Mode (WITH MEMORY)")
    print("=" * 80)
    print(f"Session ID: {session_id}")
    print(f"Model: {config.LLM_MODEL}")
    print("\nCommands:")
    print("   • 'exit/quit/bye' - End conversation")
    print("   • 'history' - Show conversation summary")
    print("   • 'memory' - View current memory state")
    print("   • 'reset' - Clear conversation memory (fresh start)")
    print("   • 'clear' - Clear screen")
    print("   • 'export' - Export conversation to file")
    print("=" * 80)
    
    while True:
        try:
            user_query = input("\n🧑 You: ").strip()
            
            # Handle commands
            if user_query.lower() in ['exit', 'quit', 'bye', 'q']:
                print(f"\n👋 Conversation ended. Total queries: {conversation_count}")
                logger.info(f"Conversational session {session_id} ended. Total queries: {conversation_count}")
                break
            
            if user_query.lower() == 'history':
                # Show memory summary
                memory_vars = conversational_qa.memory.load_memory_variables({})
                chat_history = memory_vars.get('chat_history', [])
                
                if chat_history:
                    print("\n📜 Conversation Summary:")
                    print("=" * 60)
                    for i in range(0, len(chat_history), 2):
                        q_num = i // 2 + 1
                        if i < len(chat_history):
                            print(f"\n[{q_num}] Q: {chat_history[i].content[:80]}...")
                        if i + 1 < len(chat_history):
                            print(f"    A: {chat_history[i+1].content[:80]}...")
                    print("=" * 60)
                else:
                    print("\n📜 No conversation history yet.")
                continue
            
            if user_query.lower() == 'memory':
                # Show raw memory
                memory_vars = conversational_qa.memory.load_memory_variables({})
                chat_history = memory_vars.get('chat_history', [])
                print(f"\n🧠 Memory State:")
                print(f"   Messages in memory: {len(chat_history)}")
                print(f"   Queries processed: {conversation_count}")
                continue
            
            if user_query.lower() == 'clear':
                print("\n" * 50)
                continue
            
            if user_query.lower() == 'reset':
                # Clear conversation memory
                conversational_qa.memory.clear()
                conversation_count = 0
                print("\n🔄 Memory cleared! Starting fresh conversation.")
                logger.info(f"Memory reset in session {session_id}")
                continue
            
            if user_query.lower() == 'export':
                if conversation_count > 0:
                    filename = f"chat_conversational_{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                    try:
                        memory_vars = conversational_qa.memory.load_memory_variables({})
                        chat_history = memory_vars.get('chat_history', [])
                        
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(f"Medical Chatbot - Conversational Chat History\n")
                            f.write(f"Session ID: {session_id}\n")
                            f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                            f.write("=" * 80 + "\n\n")
                            
                            for i in range(0, len(chat_history), 2):
                                q_num = i // 2 + 1
                                if i < len(chat_history):
                                    f.write(f"\n[Query {q_num}]\n")
                                    f.write(f"Q: {chat_history[i].content}\n\n")
                                if i + 1 < len(chat_history):
                                    f.write(f"A: {chat_history[i+1].content}\n\n")
                                f.write("-" * 80 + "\n")
                        
                        print(f"✅ Conversation exported to: {filename}")
                        logger.info(f"Chat history exported to {filename}")
                    except Exception as e:
                        print(f"❌ Error exporting: {e}")
                        logger.error(f"Failed to export chat history: {e}")
                else:
                    print("📜 No conversation to export yet.")
                continue
            
            if not user_query:
                continue
            
            # Log and display user input clearly
            print(f"\n{'='*80}")
            print(f"🧑 You: {user_query}")
            print(f"{'='*80}")
            logger.info(f"USER INPUT #{conversation_count + 1}: {user_query}")
            
            # Process query with conversation memory
            start_time = time.time()
            
            logger.info(f"Processing query #{conversation_count + 1} in session {session_id}: {user_query[:100]}")
            
            try:
                # Use conversational_qa which automatically handles memory
                result = conversational_qa({"question": user_query})
                answer = result["answer"]
                
                end_time = time.time()
                response_time = end_time - start_time
                
                # Log query processing details
                logger.info(f"Response generated in {response_time:.2f}s")
                logger.info(f"Retrieved {len(result.get('source_documents', []))} documents")
                
                # Display response with clear formatting
                print(f"\n{'='*80}")
                print(f"🤖 Assistant:")
                print(f"{'='*80}")
                print(answer)
                print(f"{'='*80}")
                
                conversation_count += 1
                
                # Show sources
                if result.get("source_documents"):
                    sources = [doc.metadata.get("source", "Unknown").split("/")[-1] 
                              for doc in result["source_documents"]]
                    unique_sources = list(dict.fromkeys(sources))  # Remove duplicates
                    print(f"Sources: {', '.join(unique_sources)}")
                
                print(f"Response Time: {response_time:.2f}s | Query #{conversation_count}")
                logger.info(f"OUTPUT ANSWER: {answer[:100]}...")
                print()
                
                logger.info(f"Query #{conversation_count} processed successfully in {response_time:.2f}s")
                
            except Exception as e:
                error_msg = str(e)
                print(f"\n❌ Error: {error_msg}")
                logger.error(f"Query processing error in session {session_id}: {error_msg}", exc_info=True)
                print("Please try rephrasing your question or type 'exit' to quit.")
            
        except KeyboardInterrupt:
            print(f"\n\nSession {session_id} interrupted. Goodbye!")
            logger.info(f"Conversational session {session_id} interrupted")
            break
        except Exception as e:
            logger.error(f"Unexpected error in session {session_id}: {e}", exc_info=True)
            print(f"\n❌ Unexpected error: {e}")
            print("Please try again or type 'exit' to quit.")
    
    # Final summary
    if conversation_count > 0:
        print(f"\nSession Summary:")
        print(f"   Total queries: {conversation_count}")
        print(f"   Session ID: {session_id}")
        
        # Check memory state
        memory_vars = conversational_qa.memory.load_memory_variables({})
        chat_history = memory_vars.get('chat_history', [])
        print(f"   Messages in memory: {len(chat_history)}")