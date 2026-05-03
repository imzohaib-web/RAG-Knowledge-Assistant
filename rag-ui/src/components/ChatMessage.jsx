import SourceCard from './SourceCard'

export default function ChatMessage({ message, onFeedback }) {
  const isUser = message.type === 'user'
  const isSystem = message.type === 'system'
  const timestamp = message.timestamp ? new Date(message.timestamp) : new Date()
  
  return (
    <div className={`flex items-start space-x-3 ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
      {/* Avatar */}
      {!isSystem && (
        <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
          isUser 
            ? 'bg-blue-500' 
            : 'bg-gradient-to-r from-blue-500 to-purple-600'
        }`}>
          <span className="text-white font-bold text-sm">
            {isUser ? 'U' : 'AI'}
          </span>
        </div>
      )}
      
      {/* Message Content */}
      <div className={`max-w-3xl ${isUser ? 'items-end' : 'items-start'} ${isSystem ? 'w-full' : ''}`}>
        <div className={`rounded-lg p-4 shadow-sm ${
          isUser 
            ? 'bg-blue-500 text-white' 
            : isSystem
              ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-800 dark:text-blue-200 border border-blue-200 dark:border-blue-800'
              : 'bg-white dark:bg-gray-800 text-gray-800 dark:text-white'
        }`}>
          <p className="whitespace-pre-wrap">{message.text}</p>
        </div>
        
        {/* Source Attribution for AI messages */}
        {!isUser && !isSystem && (
          <div className="mt-2 flex flex-wrap gap-2">
            <button
              onClick={() => navigator.clipboard.writeText(message.text)}
              className="text-xs px-2 py-1 rounded bg-gray-100 dark:bg-gray-700"
            >
              Copy Answer
            </button>
            <button onClick={() => onFeedback?.(message, 'up')} className="text-xs px-2 py-1 rounded bg-gray-100 dark:bg-gray-700">Thumbs Up</button>
            <button onClick={() => onFeedback?.(message, 'down')} className="text-xs px-2 py-1 rounded bg-gray-100 dark:bg-gray-700">Thumbs Down</button>
            <details className="text-xs px-2 py-1 rounded bg-gray-100 dark:bg-gray-700">
              <summary className="cursor-pointer">Show Source</summary>
              <div className="mt-2 space-y-2">
                {(message.sourceChunks || []).map((chunk) => (
                  <div key={`${message.id}-${chunk.chunk_id}`} className="p-2 bg-white dark:bg-gray-800 rounded border border-gray-200 dark:border-gray-700">
                    <div className="text-[11px] text-gray-500 mb-1">Page {chunk.page_number}</div>
                    <div className="text-xs whitespace-pre-wrap">{chunk.text}</div>
                  </div>
                ))}
              </div>
            </details>
          </div>
        )}
        {!isUser && message.sources && message.sources.length > 0 && (
          <div className="mt-2">
            <div className="text-xs text-gray-500 dark:text-gray-400 mb-1">Sources:</div>
            <div className="space-y-1">
              {message.sources.map((source, index) => (
                <SourceCard key={index} source={source} />
              ))}
            </div>
            {message.chunksUsed > 0 && (
              <div className="text-xs text-gray-500 mt-1">Chunks used: {message.chunksUsed}</div>
            )}
          </div>
        )}
        
        {/* Timestamp */}
        <div className="mt-1 text-xs text-gray-400 dark:text-gray-500">
          {timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </div>
      </div>
    </div>
  )
}
