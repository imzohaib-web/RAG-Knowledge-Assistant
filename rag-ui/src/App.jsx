import { useEffect, useMemo, useState } from 'react'
import Sidebar from './components/Sidebar'
import TopBar from './components/TopBar'
import ChatWindow from './components/ChatWindow'
import InputBox from './components/InputBox'
import { apiService } from './services/api'

const DEFAULT_SETTINGS = {
  chunkSize: 500,
  chunkOverlap: 50,
  topK: 3,
  model: 'llama3-70b-8192',
  temperature: 0.3,
}

const SETTINGS_KEY = 'rag_settings'
const CHAT_KEY = 'rag_conversations'

function App() {
  const [conversations, setConversations] = useState(() => {
    const raw = localStorage.getItem(CHAT_KEY)
    return raw ? JSON.parse(raw) : []
  })
  const [activeConversationId, setActiveConversationId] = useState(null)
  const [isTyping, setIsTyping] = useState(false)
  const [pdfInfo, setPdfInfo] = useState({ filename: null, chunks_created: 0, total_pages: 0 })
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)
  const [actionLoading, setActionLoading] = useState({})
  const [errorText, setErrorText] = useState('')
  const [settings, setSettings] = useState(() => {
    const raw = localStorage.getItem(SETTINGS_KEY)
    return raw ? JSON.parse(raw) : DEFAULT_SETTINGS
  })

  const activeConversation = useMemo(
    () => conversations.find((c) => c.id === activeConversationId) || null,
    [conversations, activeConversationId]
  )
  const messages = activeConversation?.messages || []

  useEffect(() => {
    localStorage.setItem(CHAT_KEY, JSON.stringify(conversations))
  }, [conversations])

  useEffect(() => {
    localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings))
  }, [settings])

  useEffect(() => {
    if (conversations.length === 0) {
      handleNewChat()
    } else if (!activeConversationId) {
      setActiveConversationId(conversations[0].id)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const updateActiveConversation = (updater) => {
    setConversations((prev) =>
      prev.map((conversation) =>
        conversation.id === activeConversationId ? updater(conversation) : conversation
      )
    )
  }

  const setButtonLoading = (key, value) => {
    setActionLoading((prev) => ({ ...prev, [key]: value }))
  }

  const handleSendMessage = async (message) => {
    if (!activeConversationId) return
    setErrorText('')
    const userMessage = {
      id: `u-${Date.now()}`,
      type: 'user',
      text: message,
      timestamp: new Date().toISOString(),
    }
    updateActiveConversation((conversation) => {
      const title = conversation.messages.length === 0 ? message.slice(0, 40) : conversation.title
      return {
        ...conversation,
        title,
        updatedAt: new Date().toISOString(),
        messages: [...conversation.messages, userMessage],
      }
    })
    setIsTyping(true)

    try {
      const response = await apiService.sendMessage({
        question: message,
        conversation_id: activeConversationId,
        top_k: settings.topK,
        model: settings.model,
        temperature: settings.temperature,
      })

      const aiResponse = {
        id: `a-${Date.now()}`,
        type: 'ai',
        text: response.answer,
        sources: response.sources.map((source) => ({
          name: pdfInfo.filename || 'Uploaded Document',
          page: source.replace('Page ', ''),
        })),
        sourceChunks: response.source_chunks || [],
        modelUsed: response.model_used,
        chunksUsed: response.chunks_used || 0,
        timestamp: new Date().toISOString(),
      }

      updateActiveConversation((conversation) => ({
        ...conversation,
        updatedAt: new Date().toISOString(),
        messages: [...conversation.messages, aiResponse],
      }))
    } catch (error) {
      setErrorText(error.message)
      const errorResponse = {
        id: `e-${Date.now()}`,
        type: 'ai',
        text: `Error: ${error.message}. Please make sure the backend is running and a PDF is uploaded.`,
        sources: [],
        timestamp: new Date().toISOString(),
      }
      updateActiveConversation((conversation) => ({
        ...conversation,
        updatedAt: new Date().toISOString(),
        messages: [...conversation.messages, errorResponse],
      }))
    } finally {
      setIsTyping(false)
    }
  }

  const handleFileUpload = async (files) => {
    // Filter for PDF files only
    const pdfFiles = files.filter(file => file.type === 'application/pdf')
    
    if (pdfFiles.length === 0) {
      setErrorText('Only PDF files are supported. Please select a PDF file.')
      return
    }

    setButtonLoading('upload', true)
    try {
      const file = pdfFiles[0]
      const response = await apiService.uploadPDF(file)
      setPdfInfo({
        filename: response.filename,
        chunks_created: response.chunks_created,
        total_pages: response.total_pages,
      })
      setIsSidebarOpen(false) // Close sidebar on mobile after file upload

      const successMessage = {
        id: `s-${Date.now()}`,
        type: 'system',
        text: `${response.message}`,
        sources: [],
        timestamp: new Date().toISOString(),
      }
      updateActiveConversation((conversation) => ({
        ...conversation,
        updatedAt: new Date().toISOString(),
        messages: [...conversation.messages, successMessage],
      }))
    } catch (error) {
      setErrorText(`Error uploading files: ${error.message}`)
    } finally {
      setButtonLoading('upload', false)
    }
  }

  const handleNewChat = () => {
    const id = `conv-${Date.now()}`
    const now = new Date().toISOString()
    setConversations((prev) => [
      {
        id,
        title: 'New Chat',
        createdAt: now,
        updatedAt: now,
        messages: [],
      },
      ...prev,
    ])
    setActiveConversationId(id)
    setErrorText('')
    setIsSidebarOpen(false) // Close sidebar on mobile after new chat
  }

  const handleSelectConversation = (id) => {
    setActiveConversationId(id)
    setIsSidebarOpen(false)
  }

  const handleDeleteConversation = async (id) => {
    if (!window.confirm('Delete this conversation?')) return
    setButtonLoading(`delete-${id}`, true)
    try {
      await apiService.deleteHistory(id)
    } catch (error) {
      setErrorText(error.message)
    } finally {
      setButtonLoading(`delete-${id}`, false)
    }
    setConversations((prev) => prev.filter((conversation) => conversation.id !== id))
    if (activeConversationId === id) {
      const remaining = conversations.filter((conversation) => conversation.id !== id)
      if (remaining.length > 0) setActiveConversationId(remaining[0].id)
      else handleNewChat()
    }
  }

  const handleClearCurrentChat = () => {
    updateActiveConversation((conversation) => ({ ...conversation, messages: [] }))
  }

  const handleExportCurrentChat = () => {
    if (!activeConversation) return
    const content = activeConversation.messages
      .map((m) => `${m.type.toUpperCase()}: ${m.text}`)
      .join('\n\n')
    const blob = new Blob([content], { type: 'text/plain' })
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = `${activeConversation.title || 'chat'}.txt`
    link.click()
    URL.revokeObjectURL(link.href)
  }

  const handleSaveSettings = async (nextSettings) => {
    setButtonLoading('save-settings', true)
    setSettings(nextSettings)
    try {
      await apiService.saveSettings({
        chunk_size: nextSettings.chunkSize,
        chunk_overlap: nextSettings.chunkOverlap,
        top_k: nextSettings.topK,
        model: nextSettings.model,
        temperature: nextSettings.temperature,
      })
    } catch (error) {
      setErrorText(error.message)
    } finally {
      setButtonLoading('save-settings', false)
    }
  }

  const handleResetSettings = () => {
    handleSaveSettings(DEFAULT_SETTINGS)
  }

  const handleFeedback = async (message, rating) => {
    try {
      await apiService.saveFeedback({
        conversation_id: activeConversationId,
        message_id: message.id,
        rating,
        answer: message.text,
        timestamp: new Date().toISOString(),
      })
    } catch (error) {
      setErrorText(error.message)
    }
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
        conversations={conversations}
        activeConversationId={activeConversationId}
        onSelectConversation={handleSelectConversation}
        onDeleteConversation={handleDeleteConversation}
        deleteLoading={actionLoading}
        pdfInfo={pdfInfo}
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
      />
      
      <div className="flex-1 flex flex-col lg:ml-0 relative">
        <TopBar 
          title={activeConversation?.title || 'New Chat'}
          currentModel={settings.model}
          settings={settings}
          onSaveSettings={handleSaveSettings}
          onResetSettings={handleResetSettings}
          settingsLoading={actionLoading['save-settings']}
          onClearChat={handleClearCurrentChat}
          onExportChat={handleExportCurrentChat}
          onMenuToggle={() => setIsSidebarOpen(!isSidebarOpen)}
        />
        {errorText && (
          <div className="px-4 py-2 bg-red-100 text-red-700 text-sm border-b border-red-200">{errorText}</div>
        )}
        <ChatWindow 
          messages={messages}
          isTyping={isTyping}
          onFeedback={handleFeedback}
        />
        <InputBox 
          onSendMessage={handleSendMessage}
          onFileUpload={handleFileUpload}
          disabled={isTyping || actionLoading.upload}
          isUploading={actionLoading.upload}
        />
      </div>
    </div>
  )
}

export default App
