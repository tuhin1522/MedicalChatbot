import chatbotIcon from '../assets/chatbot.png'

const ChatHeader = ({ darkMode, setDarkMode }) => {
    return (
        <div className={`px-6 py-5 shadow-lg transition-colors duration-300 ${darkMode ? 'bg-gradient-to-r from-gray-800 via-gray-900 to-black' : 'bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600'}`}>
            <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                    <div className="relative">
                        <img 
                            src={chatbotIcon} 
                            alt="Medical Chatbot" 
                            className="w-14 h-14 rounded-full border-3 border-white shadow-lg object-cover bg-white p-1"
                        />
                        <div className="absolute bottom-0 right-0 w-4 h-4 bg-green-400 rounded-full border-2 border-white" aria-label="Online status"></div>
                    </div>
                    <div className="flex-1">
                        <h1 className="text-2xl font-bold text-white">Medical Assistant</h1>
                        <p className="text-blue-100 text-sm flex items-center">
                            <span className="inline-block w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse" aria-hidden="true"></span>
                            <span className="text-base">Always here to help</span>
                        </p>
                    </div>
                </div>
                
                {/* Dark Mode Toggle */}
                <button
                    onClick={() => setDarkMode(!darkMode)}
                    className="p-3 rounded-xl bg-white/10 hover:bg-white/20 transition-all duration-300 backdrop-blur-sm border border-white/20 group"
                    aria-label={darkMode ? 'Switch to light mode' : 'Switch to dark mode'}
                    title={darkMode ? 'Light mode' : 'Dark mode'}
                >
                    {darkMode ? (
                        <svg className="w-6 h-6 text-yellow-300 group-hover:text-yellow-200 transition-colors" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clipRule="evenodd" />
                        </svg>
                    ) : (
                        <svg className="w-6 h-6 text-white group-hover:text-indigo-100 transition-colors" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
                        </svg>
                    )}
                </button>
            </div>
        </div>
    )
}

export default ChatHeader
