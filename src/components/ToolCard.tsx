import type { Tool } from '../data/tools'

interface ToolCardProps {
  tool: Tool
  index: number
  onDelete: (id: number) => void
}

const API_BASE = ''

export default function ToolCard({ tool, index, onDelete }: ToolCardProps) {
  const isOnline = tool.usageType === 'online'
  const isSelf = tool.source === 'self'
  const isFile = tool.toolType === 'file'

  const handleClick = () => {
    if (isFile && tool.fileId) {
      const a = document.createElement('a')
      a.href = `${API_BASE}/api/v1/tools/download/${tool.fileId}`
      a.download = tool.fileName || ''
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
    } else if (tool.url && !tool.url.startsWith('#')) {
      window.open(tool.url, '_blank', 'noopener,noreferrer')
    }
  }

  return (
    <div
      className="tool-card glass-card animate-fade-in-up group relative"
      style={{ animationDelay: `${index * 50}ms` }}
      onClick={handleClick}
    >
      <span className={`source-tag absolute top-4 right-4 ${isSelf ? 'source-self' : 'source-third'}`}>
        {isSelf ? '自研' : '第三方'}
      </span>

      <div className="text-[32px] mb-3 mt-1">{tool.icon}</div>

      <h3 className="font-bold text-base mb-2 w-full" style={{ fontFamily: 'var(--font-display)' }}>
        {tool.name}
      </h3>

      <p className="text-sm leading-relaxed opacity-50 mb-3 w-full line-clamp-2">
        {tool.description}
      </p>

      <div className="flex items-center justify-center gap-1.5 flex-wrap mb-4 w-full">
        <span
          className={`inline-flex items-center gap-1 text-[11px] font-medium px-2.5 py-1 rounded-lg
            ${isOnline && !isFile
              ? 'text-[var(--color-online)] bg-[var(--color-online-bg)]'
              : 'text-[var(--color-download)] bg-[var(--color-download-bg)]'
            }`}
        >
          <span className={`w-1.5 h-1.5 rounded-full ${isOnline && !isFile ? 'bg-[var(--color-online)]' : 'bg-[var(--color-download)]'}`} />
          {isFile ? '文件下载' : isOnline ? '在线使用' : '下载安装'}
        </span>
        {tool.fileName && (
          <span className="text-[11px] px-2 py-1 rounded-lg bg-black/[0.03] dark:bg-white/[0.04] opacity-40 font-medium">
            {tool.fileName.length > 12 ? tool.fileName.slice(0, 10) + '…' : tool.fileName}
          </span>
        )}
        {tool.tags.slice(0, 3).map(tag => (
          <span key={tag} className="text-[11px] px-2 py-1 rounded-lg bg-black/[0.03] dark:bg-white/[0.04] opacity-40 font-medium">
            {tag}
          </span>
        ))}
      </div>

      <div className="mt-auto w-full flex items-center justify-center relative">
        <span className="text-sm font-medium bg-gradient-to-r from-[#6366F1] to-[#8B5CF6] bg-clip-text text-transparent">
          {isFile ? '下载 →' : isOnline ? '使用 →' : '下载 →'}
        </span>
        <button
          onClick={(e) => { e.stopPropagation(); onDelete(tool.id) }}
          className="delete-btn opacity-0 group-hover:opacity-100 absolute right-0"
          title="删除此工具"
        >
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
            <path d="M3 6h18M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" />
          </svg>
        </button>
      </div>
    </div>
  )
}
