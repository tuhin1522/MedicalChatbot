import chatbotIcon from '../assets/chatbot.png'
import userIcon from '../assets/user.png'

const ChatMessage = ({ message, darkMode }) => {
    const isBot = message.sender === 'bot'
    const isError = message.isError
    
    return (
        <div 
            className={`flex items-start space-x-3 message-animation ${isBot ? '' : 'flex-row-reverse space-x-reverse'}`}
            role="article"
            aria-label={`${isBot ? 'Assistant' : 'User'} message at ${message.timestamp}`}
        >
            {/* Avatar */}
            <div className="flex-shrink-0">
                <img 
                    src={isBot ? chatbotIcon : userIcon} 
                    alt={isBot ? 'Medical Assistant' : 'You'}
                    className={`w-10 h-10 rounded-full object-cover shadow-md transition-all duration-300 ${
                        isBot 
                            ? darkMode 
                                ? 'bg-gradient-to-br from-indigo-900 to-purple-900 p-1' 
                                : 'bg-gradient-to-br from-indigo-100 to-purple-100 p-1'
                            : darkMode
                                ? 'bg-gradient-to-br from-blue-800 to-cyan-800 p-1'
                                : 'bg-gradient-to-br from-blue-100 to-cyan-100 p-1'
                    }`}
                />
            </div>

            {/* Message Bubble */}
            <div className={`flex flex-col max-w-[75%] ${isBot ? 'items-start' : 'items-end'}`}>
                {/* Message Label for Accessibility */}
                <span className={`text-xs font-medium mb-1 px-2 transition-colors duration-300 ${
                    darkMode ? 'text-gray-400' : 'text-gray-500'
                }`}>
                    {isBot ? 'Medical Assistant' : 'You'}
                </span>
                
                <div 
                    className={`rounded-2xl px-5 py-3.5 shadow-md transition-all duration-300 text-base leading-relaxed ${
                        isBot 
                            ? isError
                                ? darkMode
                                    ? 'bg-red-900/40 text-red-200 border border-red-700 rounded-tl-none'
                                    : 'bg-red-50 text-red-800 border border-red-200 rounded-tl-none'
                                : darkMode
                                    ? 'bg-gray-700 text-gray-100 rounded-tl-none border border-gray-600'
                                    : 'bg-white text-gray-800 rounded-tl-none border border-gray-200'
                            : 'bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-tr-none shadow-lg'
                    }`}
                >
                    <p className="whitespace-pre-wrap break-words">{message.text}</p>
                    
                    {/* Medical Disclaimer for Bot Messages */}
                    {isBot && !isError && message.text.length > 100 && (
                        <div className={`mt-3 pt-3 border-t text-xs italic transition-colors duration-300 ${
                            darkMode ? 'border-gray-600 text-gray-400' : 'border-gray-200 text-gray-500'
                        }`}>
                            <span className="inline-flex items-center">
                                <svg className="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                                </svg>
                                This information is for educational purposes. Consult a healthcare provider.
                            </span>
                        </div>
                    )}
                </div>
                
                <span className={`text-xs mt-1.5 px-2 transition-colors duration-300 ${
                    darkMode ? 'text-gray-500' : 'text-gray-400'
                } ${isBot ? 'text-left' : 'text-right'}`}>
                    {message.timestamp}
                </span>
            </div>
        </div>
    )
}

export default ChatMessage
