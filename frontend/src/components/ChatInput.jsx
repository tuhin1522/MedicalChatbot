import { useState } from 'react'

const ChatInput = ({ onSendMessage, disabled, darkMode }) => {
    const [input, setInput] = useState('')

    const handleSubmit = (e) => {
        e.preventDefault()
        if (input.trim() && !disabled) {
            onSendMessage(input)
            setInput('')
        }
    }

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            handleSubmit(e)
        }
    }

    return (
        <div className={`border-t px-6 py-4 transition-colors duration-300 ${darkMode ? 'border-gray-700 bg-gray-800' : 'border-gray-200 bg-white'
            }`}>
            <form onSubmit={handleSubmit} className="flex items-end space-x-3">
                <div className="flex-1 relative">
                    <textarea
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={handleKeyPress}
                        placeholder="Type your medical question here..."
                        disabled={disabled}
                        rows="1"
                        className={`w-full px-5 py-3.5 pr-12 border-2 rounded-2xl focus:outline-none focus:ring-2 resize-none transition-all duration-200 disabled:cursor-not-allowed text-base ${darkMode
                                ? 'bg-gray-700 border-gray-600 text-gray-100 placeholder-gray-400 focus:border-indigo-400 focus:ring-indigo-500/30 disabled:bg-gray-800'
                                : 'bg-white border-gray-200 text-gray-800 placeholder-gray-400 focus:border-indigo-500 focus:ring-indigo-200 disabled:bg-gray-50'
                            }`}
                        style={{
                            minHeight: '52px',
                            maxHeight: '120px'
                        }}
                        onInput={(e) => {
                            e.target.style.height = '52px'
                            e.target.style.height = e.target.scrollHeight + 'px'
                        }}
                        aria-label="Message input"
                    />
                </div>

                <button
                    type="submit"
                    disabled={disabled || !input.trim()}
                    className="flex-shrink-0 bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white p-4 rounded-2xl transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                    aria-label="Send message"
                    title="Send message (Enter)"
                >
                    <svg
                        className="w-6 h-6"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                        aria-hidden="true"
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                        />
                    </svg>
                </button>
            </form>

            <p className={`text-xs mt-2.5 text-center transition-colors duration-300 ${darkMode ? 'text-gray-500' : 'text-gray-400'
                }`}>
                Press <kbd className={`px-1.5 py-0.5 rounded text-xs font-mono ${darkMode ? 'bg-gray-700 border border-gray-600' : 'bg-gray-100 border border-gray-300'
                    }`}>Enter</kbd> to send • <kbd className={`px-1.5 py-0.5 rounded text-xs font-mono ${darkMode ? 'bg-gray-700 border border-gray-600' : 'bg-gray-100 border border-gray-300'
                        }`}>Shift+Enter</kbd> for new line
            </p>
        </div>
    )
}

export default ChatInput
