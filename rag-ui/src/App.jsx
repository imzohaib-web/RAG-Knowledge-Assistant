import { useState } from 'react'
import Sidebar from './components/Sidebar'
import TopBar from './components/TopBar'
import ChatWindow from './components/ChatWindow'
import InputBox from './components/InputBox'

function App() {
  const [messages, setMessages] = useState([])
  const [isTyping, setIsTyping] = useState(false)
  const [currentChatTitle, setCurrentChatTitle] = useState('New Chat')
  const [uploadedFiles, setUploadedFiles] = useState([])
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)

  const handleSendMessage = (message) => {
    setMessages(prev => [...prev, { id: Date.now(), type: 'user', text: message }])
    setIsTyping(true)
    
    // Simulate AI response
    setTimeout(() => {
      const aiResponse = {
        id: Date.now() + 1,
        type: 'ai',
        text: 'This is a sample AI response. In a real implementation, this would be connected to your RAG system backend.',
        sources: [
          { name: 'Document 1.pdf', page: 3 },
          { name: 'Knowledge Base.txt', section: 'Introduction' }
        ]
      }
      setMessages(prev => [...prev, aiResponse])
      setIsTyping(false)
    }, 1500)
  }

  const handleFileUpload = (files) => {
    setUploadedFiles(prev => [...prev, ...files])
    setIsSidebarOpen(false) // Close sidebar on mobile after file upload
  }

  const handleNewChat = () => {
    setMessages([])
    setCurrentChatTitle('New Chat')
    setIsSidebarOpen(false) // Close sidebar on mobile after new chat
  }

  return (
    <div className="flex h-screen bg-gray-50 dark:bg-gray-900 relative">
      {/* Mobile overlay */}
      {isSidebarOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-10 lg:hidden"
          onClick={() => setIsSidebarOpen(false)}
        />
      )}
      
      <Sidebar 
        onNewChat={handleNewChat}
        uploadedFiles={uploadedFiles}
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
      />
      
      <div className="flex-1 flex flex-col lg:ml-0 relative">
        <TopBar 
          title={currentChatTitle}
          onMenuToggle={() => setIsSidebarOpen(!isSidebarOpen)}
        />
        <ChatWindow 
          messages={messages}
          isTyping={isTyping}
        />
        <InputBox 
          onSendMessage={handleSendMessage}
          onFileUpload={handleFileUpload}
          disabled={isTyping}
        />
      </div>
    </div>
  )
}

export default App
