import { useState, useRef, useEffect } from 'react'
import ChatHeader from './ChatHeader'
import ChatMessage from './ChatMessage'
import ChatInput from './ChatInput'

const ChatInterface = () => {
    const [messages, setMessages] = useState([])
    const [isTyping, setIsTyping] = useState(false)
    const [theme, setTheme] = useState('light')
    const messagesEndRef = useRef(null)

    // Apply theme to document
    useEffect(() => {
        document.documentElement.setAttribute('data-theme', theme)
    }, [theme])

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

    const toggleTheme = () => {
        const newTheme = theme === 'light' ? 'dark' : 'light'
        console.log('Toggling theme from', theme, 'to', newTheme)
        setTheme(newTheme)
    }

    return (
        <div className="flex flex-col h-screen bg-base-100">
            {/* Chat Header */}
            <ChatHeader theme={theme} toggleTheme={toggleTheme} />

            {/* Messages Container */}
            <div className="flex-1 overflow-y-auto">
                <div className="chat-container py-6">
                    {messages.length === 0 && (
                        <div className="flex flex-col items-center justify-center min-h-[calc(100vh-180px)] px-4 space-y-8 py-12">
                            {/* Welcome Section */}
                            <div className="text-center space-y-4 max-w-2xl">
                                <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary/10 mb-4">
                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                                    </svg>
                                </div>
                                <h2 className="text-3xl font-semibold text-base-content">
                                    How can I help you today?
                                </h2>
                                <p className="text-base text-base-content/60 max-w-md">
                                    I'm your AI medical assistant. Ask me about symptoms, conditions, treatments, or general health information.
                                </p>
                            </div>
                        </div>
                    )}

                    {/* Messages */}
                    {messages.map((message) => (
                        <ChatMessage key={message.id} message={message} theme={theme} />
                    ))}

                    {/* Typing Indicator */}
                    {isTyping && (
                        <div className="message-animation py-8 border-b border-base-300">
                            <div className="chat-container flex items-start space-x-4">
                                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary flex items-center justify-center">
                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                                    </svg>
                                </div>
                                <div className="flex-1 pt-1">
                                    <div className="flex space-x-1 py-2">
                                        <div className="w-2 h-2 bg-base-content/40 rounded-full typing-indicator"></div>
                                        <div className="w-2 h-2 bg-base-content/40 rounded-full typing-indicator" style={{ animationDelay: '0.2s' }}></div>
                                        <div className="w-2 h-2 bg-base-content/40 rounded-full typing-indicator" style={{ animationDelay: '0.4s' }}></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}

                    <div ref={messagesEndRef} />
                </div>
            </div>

            {/* Input Area */}
            <ChatInput onSendMessage={handleSendMessage} disabled={isTyping} theme={theme} />
        </div>
    )
}

export default ChatInterface
