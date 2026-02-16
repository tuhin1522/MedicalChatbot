const ChatMessage = ({ message, theme }) => {
    const isBot = message.sender === 'bot'
    const isError = message.isError
    const hasSources = isBot && message.sources && message.sources.length > 0
    const hasDisclaimer = isBot && message.disclaimer
    
    return (
        <div className={`py-8 ${isBot ? 'bg-base-200/30' : 'bg-base-100'} message-animation20`}>
            <div className="chat-container">
                <div className={`flex ${isBot ? 'justify-start' : 'justify-end'}`}>
                    <div className={`max-w-[100%] ${isBot ? 'text-left' : 'text-right'}`}>
                        <div className={`inline-block text-left px-4 py-3 rounded-2xl ${
                            isBot 
                                ? 'bg-transparent' 
                                : theme === 'dark' 
                                    ? 'bg-primary text-white' 
                                    : 'bg-primary text-base-content'
                        }`}>
                            {isError ? (
                                <div className="flex items-center gap-2 text-sm">
                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                    <span>{message.text}</span>
                                </div>
                            ) : (
                                <>
                                    <p className={`text-[15px] leading-7 whitespace-pre-wrap break-words ${
                                        isBot ? 'text-base-content' : theme === 'dark' ? 'text-white' : 'text-base-content'
                                    }`}>
                                        {message.text}
                                    </p>
                                    
                                    {/* Response Time */}
                                    {isBot && message.response_time && (
                                        <p className="mt-2 text-xs text-base-content/40">
                                            Response time: {message.response_time.toFixed(2)}s
                                        </p>
                                    )}
                                </>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default ChatMessage
