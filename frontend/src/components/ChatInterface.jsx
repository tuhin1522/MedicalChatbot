import { useState, useRef, useEffect } from 'react'
import ChatHeader from './ChatHeader'
import ChatMessage from './ChatMessage'
import ChatInput from './ChatInput'
import chatbotIcon from '../assets/chatbot.png'

const ChatInterface = () => {
    const [messages, setMessages] = useState([])
    const [isTyping, setIsTyping] = useState(false)
    const [darkMode, setDarkMode] = useState(false)
    const messagesEndRef = useRef(null)

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }

    useEffect(() => {
        scrollToBottom()
    }, [messages])

    const handleSendMessage = async (messageText) => {
        if (!messageText.trim()) return

        // Add user message
        const userMessage = {
            id: Date.now(),
            text: messageText,
            sender: 'user',
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
        setMessages(prev => [...prev, userMessage])
        setIsTyping(true)

        try {
            // Send message to FastAPI backend
            const formData = new FormData()
            formData.append('msg', messageText)

            const response = await fetch('http://localhost:8000/get', {
                method: 'POST',
                body: formData
            })

            const botResponse = await response.text()

            // Add bot message
            const botMessage = {
                id: Date.now() + 1,
                text: botResponse,
                sender: 'bot',
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            }
            setMessages(prev => [...prev, botMessage])
        } catch (error) {
            console.error('Error sending message:', error)
            const errorMessage = {
                id: Date.now() + 1,
                text: 'I apologize, but I\'m currently unable to process your request. This could be due to a connectivity issue. Please ensure the backend server is running and try again. If the problem persists, please consult with a healthcare professional directly.',
                sender: 'bot',
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
                isError: true
            }
            setMessages(prev => [...prev, errorMessage])
        } finally {
            setIsTyping(false)
        }
    }

    return (
        <div className={`flex items-center justify-center min-h-screen p-4 transition-colors duration-300 ${darkMode ? 'bg-gray-900' : 'bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50'}`}>
            <div className={`w-full max-w-4xl h-[85vh] flex flex-col rounded-3xl shadow-2xl overflow-hidden transition-colors duration-300 ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
                {/* Chat Header */}
                <ChatHeader darkMode={darkMode} setDarkMode={setDarkMode} />

                {/* Messages Container */}
                <div className={`flex-1 overflow-y-auto px-6 py-4 space-y-4 transition-colors duration-300 ${darkMode ? 'bg-gradient-to-b from-gray-800 to-gray-900' : 'bg-gradient-to-b from-gray-50 to-white'}`} role="log" aria-live="polite" aria-label="Chat messages">
                    {messages.length === 0 && (
                        <div className="flex flex-col items-center justify-center h-full text-center px-4">
                            <div className={`rounded-full p-6 mb-6 shadow-lg transition-colors duration-300 ${darkMode ? 'bg-gradient-to-br from-indigo-900 to-purple-900' : 'bg-gradient-to-br from-indigo-100 to-purple-100'}`}>
                                <img
                                    src={chatbotIcon}
                                    alt="Medical Chatbot"
                                    className="w-24 h-24 object-cover"
                                />
                            </div>
                            <h3 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-3">
                                Welcome to Your Medical Assistant
                            </h3>
                            <p className={`max-w-md text-lg mb-4 transition-colors duration-300 ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                                Ask me anything about medical conditions, symptoms, treatments, or general health advice. I'm here to help!
                            </p>
                            <div className={`text-xs px-4 py-2 rounded-lg mb-6 max-w-xl transition-colors duration-300 ${darkMode ? 'bg-yellow-900/30 text-yellow-200 border border-yellow-700' : 'bg-yellow-50 text-yellow-800 border border-yellow-200'}`} role="alert">
                                <strong className="font-semibold">⚕️ Medical Disclaimer:</strong> This AI assistant provides general health information only. Always consult qualified healthcare professionals for medical advice, diagnosis, or treatment.
                            </div>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-2xl">
                                <div className={`p-4 rounded-xl shadow-sm transition-all duration-300 text-left hover:shadow-md ${darkMode ? 'bg-gray-700 border border-gray-600' : 'bg-white border border-gray-100'}`}>
                                    <div className="text-indigo-500 font-semibold mb-1 text-base">💊 Medications</div>
                                    <div className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Ask about drug interactions and side effects</div>
                                </div>
                                <div className={`p-4 rounded-xl shadow-sm transition-all duration-300 text-left hover:shadow-md ${darkMode ? 'bg-gray-700 border border-gray-600' : 'bg-white border border-gray-100'}`}>
                                    <div className="text-indigo-500 font-semibold mb-1 text-base">🩺 Symptoms</div>
                                    <div className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Understand various medical symptoms</div>
                                </div>
                                <div className={`p-4 rounded-xl shadow-sm transition-all duration-300 text-left hover:shadow-md ${darkMode ? 'bg-gray-700 border border-gray-600' : 'bg-white border border-gray-100'}`}>
                                    <div className="text-indigo-500 font-semibold mb-1 text-base">🏥 Conditions</div>
                                    <div className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Learn about different health conditions</div>
                                </div>
                                <div className={`p-4 rounded-xl shadow-sm transition-all duration-300 text-left hover:shadow-md ${darkMode ? 'bg-gray-700 border border-gray-600' : 'bg-white border border-gray-100'}`}>
                                    <div className="text-indigo-500 font-semibold mb-1 text-base">💡 Advice</div>
                                    <div className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Get general health and wellness tips</div>
                                </div>
                            </div>
                        </div>
                    )}

                    {messages.map((message) => (
                        <ChatMessage key={message.id} message={message} darkMode={darkMode} />
                    ))}

                    {isTyping && (
                        <div className="flex items-start space-x-3 message-animation" role="status" aria-live="polite">
                            <div className="flex-shrink-0">
                                <img
                                    src={chatbotIcon}
                                    alt="Chatbot typing"
                                    className={`w-10 h-10 rounded-full object-cover shadow-md p-1 transition-colors duration-300 ${darkMode ? 'bg-gradient-to-br from-indigo-900 to-purple-900' : 'bg-gradient-to-br from-indigo-100 to-purple-100'}`}
                                />
                            </div>
                            <div className={`rounded-2xl rounded-tl-none px-6 py-3 shadow-md transition-colors duration-300 ${darkMode ? 'bg-gray-700 border border-gray-600' : 'bg-white border border-gray-100'}`}>
                                <div className="flex space-x-2">
                                    <div className="w-2 h-2 bg-indigo-400 rounded-full typing-indicator"></div>
                                    <div className="w-2 h-2 bg-indigo-400 rounded-full typing-indicator" style={{ animationDelay: '0.2s' }}></div>
                                    <div className="w-2 h-2 bg-indigo-400 rounded-full typing-indicator" style={{ animationDelay: '0.4s' }}></div>
                                </div>
                                <span className="sr-only">Assistant is typing...</span>
                            </div>
                        </div>
                    )}

                    <div ref={messagesEndRef} />
                </div>

                {/* Input Area */}
                <ChatInput onSendMessage={handleSendMessage} disabled={isTyping} darkMode={darkMode} />
            </div>
        </div>
    )
}

export default ChatInterface
