import { useState } from 'react'

export default function Sidebar({
  onNewChat,
  conversations,
  activeConversationId,
  onSelectConversation,
  onDeleteConversation,
  deleteLoading,
  pdfInfo,
  isOpen,
}) {
  const [isCollapsed, setIsCollapsed] = useState(false)

  return (
    <div className={`${isCollapsed ? 'w-16' : 'w-64'} lg:w-64 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col transition-all duration-300 ease-in-out fixed lg:relative h-full z-20 ${isCollapsed ? 'lg:w-16' : ''} ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}`}>
      {/* Logo and App Name */}
      <div className="p-4 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-between">
          {!isCollapsed && (
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">AI</span>
              </div>
              <span className="font-semibold text-gray-800 dark:text-white">Knowledge Assistant</span>
            </div>
          )}
          <button
            onClick={() => setIsCollapsed(!isCollapsed)}
            className="p-1 rounded hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
          >
            <svg className="w-5 h-5 text-gray-500 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>
      </div>

      {/* Navigation Buttons */}
      <div className="flex-1 p-4 space-y-2">
        <button
          onClick={onNewChat}
          className="w-full flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors text-gray-700 dark:text-gray-200"
        >
          <svg className="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          {!isCollapsed && <span>New Chat</span>}
        </button>

        {/* History Section */}
        {!isCollapsed && (
          <div className="mt-6">
            <h3 className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-3">History</h3>
            <div className="space-y-1">
              {conversations.map((chat) => (
                <div key={chat.id} className={`group rounded-lg ${activeConversationId === chat.id ? 'bg-blue-100 dark:bg-blue-900/30' : 'hover:bg-gray-100 dark:hover:bg-gray-700'}`}>
                  <button
                    onClick={() => onSelectConversation(chat.id)}
                    className="w-full text-left px-3 py-2 transition-colors text-sm text-gray-600 dark:text-gray-300"
                  >
                    <div className="truncate font-medium">{chat.title || 'New Chat'}</div>
                    <div className="text-xs text-gray-400">{new Date(chat.updatedAt).toLocaleString()}</div>
                  </button>
                  <button
                    onClick={() => onDeleteConversation(chat.id)}
                    disabled={deleteLoading?.[`delete-${chat.id}`]}
                    className="ml-3 mb-2 text-xs text-red-500 hover:text-red-600 disabled:opacity-50"
                  >
                    {deleteLoading?.[`delete-${chat.id}`] ? 'Deleting...' : 'Delete History'}
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Uploaded File */}
        {!isCollapsed && pdfInfo?.filename && (
          <div className="mt-6">
            <h3 className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-3">PDF Status</h3>
            <div className="px-3 py-2 rounded-lg bg-gray-50 dark:bg-gray-700 text-sm text-gray-600 dark:text-gray-300">
              <div className="truncate font-medium">{pdfInfo.filename}</div>
              <div className="text-xs mt-1">Pages: {pdfInfo.total_pages} • Chunks: {pdfInfo.chunks_created}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
