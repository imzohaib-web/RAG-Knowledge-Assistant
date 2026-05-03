import { useState } from 'react'

export default function TopBar({
  title,
  currentModel,
  settings,
  onSaveSettings,
  onResetSettings,
  settingsLoading,
  onClearChat,
  onExportChat,
  onMenuToggle,
}) {
  const [showSettings, setShowSettings] = useState(false)
  const [draft, setDraft] = useState(settings)

  const save = () => {
    onSaveSettings(draft)
    setShowSettings(false)
  }

  return (
    <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-4 lg:px-6 py-4">
      <div className="flex items-center justify-between">
      <div className="flex items-center space-x-3">
        {/* Mobile menu button */}
        <button
          onClick={onMenuToggle}
          className="lg:hidden p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
        >
          <svg className="w-5 h-5 text-gray-500 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
        
        <h1 className="text-lg font-semibold text-gray-800 dark:text-white">{title}</h1>
        <div className="hidden sm:flex items-center space-x-2 px-3 py-1 bg-green-100 dark:bg-green-900 rounded-full">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-xs text-green-700 dark:text-green-300">Using private data</span>
        </div>
        <div className="text-xs text-gray-500 dark:text-gray-400">Model: {currentModel}</div>
      </div>
      
      <div className="flex items-center space-x-2">
        <button onClick={onClearChat} className="text-sm px-3 py-1 rounded bg-gray-100 dark:bg-gray-700">Clear Chat</button>
        <button onClick={onExportChat} className="text-sm px-3 py-1 rounded bg-gray-100 dark:bg-gray-700">Export Chat</button>
        <button onClick={() => { setDraft(settings); setShowSettings(!showSettings) }} className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
          <svg className="w-5 h-5 text-gray-500 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        </button>
      </div>
      </div>
      {showSettings && (
        <div className="mt-3 p-3 rounded border border-gray-200 dark:border-gray-700 grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
          <label>Chunk Size: {draft.chunkSize}
            <input type="range" min="200" max="1000" value={draft.chunkSize} onChange={(e) => setDraft({ ...draft, chunkSize: Number(e.target.value) })} className="w-full" />
          </label>
          <label>Chunk Overlap: {draft.chunkOverlap}
            <input type="range" min="0" max="200" value={draft.chunkOverlap} onChange={(e) => setDraft({ ...draft, chunkOverlap: Number(e.target.value) })} className="w-full" />
          </label>
          <label>Top K Results: {draft.topK}
            <input type="range" min="1" max="10" value={draft.topK} onChange={(e) => setDraft({ ...draft, topK: Number(e.target.value) })} className="w-full" />
          </label>
          <label>Temperature: {draft.temperature.toFixed(1)}
            <input type="range" min="0" max="1" step="0.1" value={draft.temperature} onChange={(e) => setDraft({ ...draft, temperature: Number(e.target.value) })} className="w-full" />
            <div className="text-xs text-gray-500">More Focused → More Creative</div>
          </label>
          <label className="md:col-span-2">Model
            <select value={draft.model} onChange={(e) => setDraft({ ...draft, model: e.target.value })} className="w-full mt-1 p-2 rounded border dark:bg-gray-800">
              <option value="llama3-8b-8192">llama3-8b-8192 (Fast)</option>
              <option value="llama3-70b-8192">llama3-70b-8192 (Better)</option>
              <option value="mixtral-8x7b-32768">mixtral-8x7b-32768 (Detailed)</option>
            </select>
          </label>
          <div className="md:col-span-2 flex gap-2">
            <button onClick={save} disabled={settingsLoading} className="px-3 py-2 rounded bg-blue-600 text-white disabled:opacity-60">{settingsLoading ? 'Saving...' : 'Save Settings'}</button>
            <button onClick={() => { onResetSettings(); setShowSettings(false) }} className="px-3 py-2 rounded bg-gray-200 dark:bg-gray-700">Reset to Defaults</button>
          </div>
        </div>
      )}
    </div>
  )
}
