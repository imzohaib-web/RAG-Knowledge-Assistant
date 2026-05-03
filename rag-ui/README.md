# RAG-based AI Knowledge Assistant

A modern, minimal AI chat interface for a RAG-based AI Knowledge Assistant web application, inspired by Google Gemini and ChatGPT.

## Features

- **Clean, Minimal Interface**: Modern design with soft colors, rounded corners, and smooth transitions
- **Dark/Light Mode Ready**: Built with Tailwind CSS for easy theming
- **Responsive Design**: Mobile-first approach with collapsible sidebar
- **Chat Interface**: User and AI message display with typing indicators
- **File Upload**: Drag & drop support for PDF, TXT, and DOC files
- **Source Attribution**: Shows document sources for AI responses
- **Mock State Management**: Demonstrates full functionality without backend

## Tech Stack

- **React 19** with component-based architecture
- **Tailwind CSS** for styling
- **Vite** for development and building

## Components Architecture

- `App` - Main application container with state management
- `Sidebar` - Navigation panel with chat history and file management
- `TopBar` - Header with chat title and status indicators
- `ChatWindow` - Message display area with empty state
- `ChatMessage` - Individual message component with source cards
- `InputBox` - Message input with file upload functionality
- `SourceCard` - Document attribution display

## Getting Started

### Prerequisites
- Node.js (version 18 or higher)
- npm or yarn

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```

### Development

Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

### Building

Build for production:
```bash
npm run build
```

## Usage

1. **Start a New Chat**: Click "New Chat" in the sidebar
2. **Upload Documents**: Use the upload button or drag & drop files
3. **Ask Questions**: Type your message and press Enter
4. **View Sources**: AI responses include source document references
5. **Mobile Support**: Use the hamburger menu to toggle sidebar on mobile

## File Upload Support

- PDF files (.pdf)
- Text files (.txt)
- Word documents (.doc, .docx)

## Design Features

- **Smooth Transitions**: Hover effects and animations throughout
- **Custom Scrollbars**: Styled scrollbars for better aesthetics
- **Loading States**: Typing indicators and loading animations
- **Empty States**: Helpful guidance when no messages exist
- **Responsive Layout**: Adapts seamlessly from desktop to mobile

## Future Enhancements

- Connect to actual RAG backend
- Real-time document processing
- Advanced search functionality
- User authentication
- Settings and preferences
- Export chat history

## Development Notes

This is a frontend-only demonstration. The AI responses are mock data. To connect to a real RAG system, replace the mock response logic in `App.jsx` with actual API calls.
