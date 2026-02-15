const ChatMessage = ({ message, theme }) => {
    const isBot = message.sender === 'bot'
    const isError = message.isError
    const hasSources = isBot && message.sources && message.sources.length > 0
    const hasDisclaimer = isBot && message.disclaimer
    
    return (
        <div className={`py-6 ${isBot ? 'bg-base-200/30' : 'bg-base-100'} message-animation20`}>
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
                                    
                                    {/* Confidence Badge */}
                                    {isBot && message.confidence && (
                                        <div className="mt-3 flex items-center gap-2">
                                            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                                                message.confidence === 'high' 
                                                    ? 'bg-success/20 text-success' 
                                                    : message.confidence === 'medium'
                                                    ? 'bg-warning/20 text-warning'
                                                    : 'bg-error/20 text-error'
                                            }`}>
                                                {message.confidence === 'high' && '✓ High Confidence'}
                                                {message.confidence === 'medium' && '● Medium Confidence'}
                                                {message.confidence === 'low' && '! Low Confidence'}
                                            </span>
                                            {message.confidence_score && (
                                                <span className="text-xs text-base-content/50">
                                                    {Math.round(message.confidence_score * 100)}%
                                                </span>
                                            )}
                                        </div>
                                    )}
                                    
                                    {/* Sources */}
                                    {hasSources && (
                                        <div className="mt-4 space-y-2">
                                            <p className="text-xs font-semibold text-base-content/70 uppercase tracking-wide">
                                                Sources ({message.sources.length})
                                            </p>
                                            <div className="space-y-2">
                                                {message.sources.map((source, idx) => (
                                                    <div 
                                                        key={idx} 
                                                        className="text-xs bg-base-100/50 rounded-lg p-3 border border-base-300"
                                                    >
                                                        <p className="text-base-content/80 leading-relaxed">
                                                            {source.content}
                                                        </p>
                                                        {source.page && (
                                                            <p className="mt-1.5 text-base-content/50 font-medium">
                                                                Page {source.page}
                                                            </p>
                                                        )}
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    )}
                                    
                                    {/* Disclaimer */}
                                    {hasDisclaimer && (
                                        <div className="mt-4 p-3 bg-warning/10 border border-warning/30 rounded-lg">
                                            <div className="flex items-start gap-2">
                                                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-warning flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                                                </svg>
                                                <p className="text-xs text-warning leading-relaxed">
                                                    {message.disclaimer}
                                                </p>
                                            </div>
                                        </div>
                                    )}
                                    
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
