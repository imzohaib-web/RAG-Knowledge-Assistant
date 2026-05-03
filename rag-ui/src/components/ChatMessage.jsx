import SourceCard from './SourceCard'

export default function ChatMessage({ message }) {
  const isUser = message.type === 'user'
  const isSystem = message.type === 'system'
  
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
        {!isUser && message.sources && message.sources.length > 0 && (
          <div className="mt-2">
            <div className="text-xs text-gray-500 dark:text-gray-400 mb-1">Sources:</div>
            <div className="space-y-1">
              {message.sources.map((source, index) => (
                <SourceCard key={index} source={source} />
              ))}
            </div>
          </div>
        )}
        
        {/* Timestamp */}
        <div className="mt-1 text-xs text-gray-400 dark:text-gray-500">
          {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </div>
      </div>
    </div>
  )
}
