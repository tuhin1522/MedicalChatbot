import { useState, useRef, useEffect } from 'react'

const ChatInput = ({ onSendMessage, disabled, theme }) => {
    const [input, setInput] = useState('')
    const textareaRef = useRef(null)

    const handleSubmit = (e) => {
        e.preventDefault()
        if (input.trim() && !disabled) {
            onSendMessage(input)
            setInput('')
            // Reset textarea height
            if (textareaRef.current) {
                textareaRef.current.style.height = 'auto'
            }
        }
    }

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            handleSubmit(e)
        }
    }

    const handleInput = (e) => {
        setInput(e.target.value)
        // Auto-resize textarea
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto'
            textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 200) + 'px'
        }
    }

    return (
        <div className="sticky bottom-12 bg-base-100 pt-4 pb-8 mb-6">
            <div className="chat-container">
                <form onSubmit={handleSubmit} className="relative">
                    <div className="relative flex items-center bg-base-200/50 border-2 border-base-300 rounded-2xl shadow-sm hover:shadow-md transition-all duration-200 focus-within:border-primary/50 focus-within:shadow-lg">
                        <textarea
                            ref={textareaRef}
                            value={input}
                            onChange={handleInput}
                            onKeyPress={handleKeyPress}
                            placeholder="Message Medical Assistant..."
                            disabled={disabled}
                            rows="1"
                            className="w-full pl-5 pr-14 py-4 leading-6 bg-transparent  resize-none focus:outline-none text-[15px] text-base-content placeholder:text-base-content/50 placeholder:pl-0 disabled:cursor-not-allowed"
                            style={{
                                minHeight: '56px',
                                maxHeight: '200px',
                            }}
                            aria-label="Message input"
                        />

                        <button
                            type="submit"
                            disabled={disabled || !input.trim()}
                            className={`absolute right-3 bottom-3 w-10 h-10 rounded-full flex items-center justify-center transition-all duration-200 ${
                                disabled || !input.trim() 
                                    ? 'bg-base-300 text-base-content/30 cursor-not-allowed' 
                                    : 'bg-primary hover:bg-primary-focus text-white shadow-md hover:shadow-lg hover:scale-105 active:scale-95'
                            }`}
                            aria-label="Send message"
                            title="Send message (Enter)"
                        >
                            <svg
                                className="w-5 h-5"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                                aria-hidden="true"
                                strokeWidth={2.5}
                            >
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    d="M5 12h14M12 5l7 7-7 7"
                                />
                            </svg>
                        </button>
                    </div>

                    <p className="text-xs text-center mt-3 text-base-content/50">
                        Medical advice can be inaccurate. Always verify important health information.
                    </p>
                </form>
            </div>
        </div>
    )
}

export default ChatInput
