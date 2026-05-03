export default function SourceCard({ source }) {
  return (
    <div className="inline-flex items-center space-x-2 px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded-md text-xs">
      <svg className="w-3 h-3 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <span className="text-gray-700 dark:text-gray-300 font-medium">{source.name}</span>
      {source.page && (
        <span className="text-gray-500 dark:text-gray-400">
          • Page {source.page}
        </span>
      )}
      {source.section && (
        <span className="text-gray-500 dark:text-gray-400">
          • {source.section}
        </span>
      )}
    </div>
  )
}
