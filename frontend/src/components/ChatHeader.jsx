const ChatHeader = ({ theme, toggleTheme }) => {
    return (
        <header className="sticky top-0 z-10 flex items-center justify-between h-14 px-4 border-b border-base-300 bg-base-100/80 backdrop-blur-md">
            {/* Left side */}
            <div className="flex items-center gap-3 flex-1">
                <button 
                    className="flex items-center justify-center w-9 h-9 rounded-lg hover:bg-base-200 active:bg-base-300 transition-colors"
                    aria-label="Menu"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-base-content" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                    </svg>
                </button>
                <h1 className="text-sm font-semibold text-base-content">
                    Medical Assistant
                </h1>
            </div>

            {/* Center - Model indicator */}
            {/* <div className="hidden md:flex items-center justify-center flex-1">
                <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-base-200/50 border border-base-300">
                    <div className="w-1.5 h-1.5 rounded-full bg-success"></div>
                    <span className="text-xs font-medium text-base-content">GPT-4</span>
                </div>
            </div> */}

            {/* Right side */}
            <div className="flex items-center gap-2 justify-end flex-1">
                <button 
                    type="button"
                    className="flex items-center justify-center w-9 h-9 rounded-lg hover:bg-base-200 active:bg-base-300 transition-colors cursor-pointer"
                    onClick={(e) => {
                        e.preventDefault()
                        e.stopPropagation()
                        toggleTheme()
                    }}
                    aria-label={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
                >
                    {theme === 'dark' ? (
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-base-content" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                        </svg>
                    ) : (
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-base-content" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                        </svg>
                    )}
                </button>
            </div>
        </header>
    )
}

export default ChatHeader
