import { useState } from 'react'
import Sidebar from './components/Sidebar'
import TopBar from './components/TopBar'
import ChatWindow from './components/ChatWindow'
import InputBox from './components/InputBox'
import { apiService } from './services/api'

function App() {
  const [messages, setMessages] = useState([])
  const [isTyping, setIsTyping] = useState(false)
  const [currentChatTitle, setCurrentChatTitle] = useState('New Chat')
  const [uploadedFiles, setUploadedFiles] = useState([])
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)

  const handleSendMessage = async (message) => {
    setMessages(prev => [...prev, { id: Date.now(), type: 'user', text: message }])
    setIsTyping(true)
    
    try {
      const response = await apiService.sendMessage(message)
      
      const aiResponse = {
        id: Date.now() + 1,
        type: 'ai',
        text: response.answer,
        sources: response.sources.map(source => ({ 
          name: 'Uploaded Document', 
          page: source.replace('Page ', '') 
        }))
      }
      setMessages(prev => [...prev, aiResponse])
    } catch (error) {
      const errorResponse = {
        id: Date.now() + 1,
        type: 'ai',
        text: `Error: ${error.message}. Please make sure the backend is running and you have uploaded documents.`,
        sources: []
      }
      setMessages(prev => [...prev, errorResponse])
    } finally {
      setIsTyping(false)
    }
  }

  const handleFileUpload = async (files) => {
    // Filter for PDF files only
    const pdfFiles = files.filter(file => file.type === 'application/pdf')
    
    if (pdfFiles.length === 0) {
      alert('Only PDF files are supported. Please select PDF files.')
      return
    }

    try {
      for (const file of pdfFiles) {
        const response = await apiService.uploadPDF(file)
        console.log(`Successfully uploaded ${file.name}:`, response)
        
        // Add to uploaded files list with success status
        setUploadedFiles(prev => [...prev, { 
          ...file, 
          status: 'success',
          chunksCreated: response.chunks_created 
        }])
      }
      
      setIsSidebarOpen(false) // Close sidebar on mobile after file upload
      
      // Show success message
      const successMessage = {
        id: Date.now(),
        type: 'system',
        text: `Successfully uploaded ${pdfFiles.length} PDF file(s). You can now ask questions about the content.`,
        sources: []
      }
      setMessages(prev => [...prev, successMessage])
      
    } catch (error) {
      console.error('Error uploading files:', error)
      
      // Show error message
      const errorMessage = {
        id: Date.now(),
        type: 'system',
        text: `Error uploading files: ${error.message}. Please make sure the backend is running.`,
        sources: []
      }
      setMessages(prev => [...prev, errorMessage])
    }
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
