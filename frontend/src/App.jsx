"""
React App Component - Main Application Shell
"""

export default function App() {
  const [isDarkMode, setIsDarkMode] = React.useState(false);
  
  React.useEffect(() => {
    // Initialize app
    console.log('MCP Research Assistant initialized');
  }, []);
  
  return (
    <div className={isDarkMode ? 'dark' : ''}>
      <div className="min-h-screen bg-white dark:bg-gray-900 transition-colors">
        
        {/* Header */}
        <header className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-4 shadow-lg">
          <div className="max-w-7xl mx-auto flex justify-between items-center">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-white rounded-lg flex items-center justify-center">
                <span className="font-bold text-blue-600">🤖</span>
              </div>
              <h1 className="text-2xl font-bold">MCP Research Assistant</h1>
            </div>
            
            <div className="flex items-center gap-4">
              <button
                onClick={() => setIsDarkMode(!isDarkMode)}
                className="p-2 rounded-lg hover:bg-white/20 transition"
              >
                {isDarkMode ? '☀️' : '🌙'}
              </button>
            </div>
          </div>
        </header>

        {/* Main Layout */}
        <div className="flex h-screen">
          
          {/* Sidebar */}
          <aside className="w-64 bg-gray-50 dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 p-4 overflow-y-auto">
            <nav className="space-y-4">
              <div>
                <h3 className="text-sm font-semibold text-gray-600 dark:text-gray-400 mb-2">NAVIGATION</h3>
                <ul className="space-y-2">
                  <li>
                    <a href="/" className="block px-4 py-2 rounded-lg bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-200">
                      💬 Chat
                    </a>
                  </li>
                  <li>
                    <a href="/documents" className="block px-4 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition">
                      📄 Documents
                    </a>
                  </li>
                  <li>
                    <a href="/reports" className="block px-4 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition">
                      📊 Reports
                    </a>
                  </li>
                  <li>
                    <a href="/agents" className="block px-4 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition">
                      🤝 Agents
                    </a>
                  </li>
                </ul>
              </div>

              <div>
                <h3 className="text-sm font-semibold text-gray-600 dark:text-gray-400 mb-2">UPLOADED FILES</h3>
                <ul className="space-y-1 text-sm">
                  <li className="px-4 py-2 text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer">
                    📋 research.pdf
                  </li>
                  <li className="px-4 py-2 text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer">
                    📋 notes.docx
                  </li>
                </ul>
              </div>
            </nav>
          </aside>

          {/* Main Content */}
          <main className="flex-1 flex flex-col overflow-hidden">
            
            {/* Chat Area */}
            <div className="flex-1 overflow-y-auto p-6 bg-gray-50 dark:bg-gray-900">
              <div className="max-w-4xl mx-auto space-y-4">
                
                {/* Message - User */}
                <div className="flex justify-end">
                  <div className="bg-blue-600 text-white px-4 py-2 rounded-lg max-w-xs">
                    What are the key findings in this research paper?
                  </div>
                </div>

                {/* Message - Assistant */}
                <div className="flex justify-start">
                  <div className="bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white px-4 py-2 rounded-lg max-w-xs">
                    Based on the uploaded research paper, the key findings include...
                    <div className="text-xs mt-2 text-gray-600 dark:text-gray-400">
                      Agent: Research | Similarity: 0.95 | Sources: 3
                    </div>
                  </div>
                </div>

              </div>
            </div>

            {/* Input Area */}
            <div className="border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-4">
              <div className="max-w-4xl mx-auto flex gap-4">
                <button className="p-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition" title="Upload file">
                  📎
                </button>
                <button className="p-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition" title="Voice input">
                  🎤
                </button>
                <input 
                  type="text" 
                  placeholder="Ask a research question..." 
                  className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
                  Send
                </button>
              </div>
            </div>
          </main>

          {/* Right Panel - Agent Monitor */}
          <aside className="w-80 bg-gray-50 dark:bg-gray-800 border-l border-gray-200 dark:border-gray-700 p-4 overflow-y-auto">
            <h3 className="font-semibold text-gray-900 dark:text-white mb-4">🤝 Agent Status</h3>
            
            <div className="space-y-2">
              <div className="p-3 bg-white dark:bg-gray-700 rounded-lg border-l-4 border-green-500">
                <div className="text-sm font-semibold text-gray-900 dark:text-white">Coordinator</div>
                <div className="text-xs text-green-600 dark:text-green-400">● Active</div>
              </div>
              
              <div className="p-3 bg-white dark:bg-gray-700 rounded-lg border-l-4 border-blue-500">
                <div className="text-sm font-semibold text-gray-900 dark:text-white">Retrieval Agent</div>
                <div className="text-xs text-blue-600 dark:text-blue-400">⟳ Processing</div>
              </div>
              
              <div className="p-3 bg-white dark:bg-gray-700 rounded-lg border-l-4 border-gray-400">
                <div className="text-sm font-semibold text-gray-900 dark:text-white">Report Generator</div>
                <div className="text-xs text-gray-600 dark:text-gray-400">○ Ready</div>
              </div>
            </div>

            <h3 className="font-semibold text-gray-900 dark:text-white mt-6 mb-4">📈 Performance</h3>
            
            <div className="space-y-2">
              <div>
                <div className="text-xs text-gray-600 dark:text-gray-400 mb-1">Tokens Used</div>
                <div className="w-full bg-gray-300 dark:bg-gray-600 rounded-full h-2">
                  <div className="bg-blue-600 h-2 rounded-full" style={{width: '65%'}}></div>
                </div>
                <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">2,450 / 4,000</div>
              </div>
              
              <div>
                <div className="text-xs text-gray-600 dark:text-gray-400 mb-1">Documents Indexed</div>
                <div className="text-sm font-semibold text-gray-900 dark:text-white">12 documents</div>
              </div>
            </div>
          </aside>

        </div>
      </div>
    </div>
  );
}

import React from 'react';
