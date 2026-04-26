import { useState, useMemo, useCallback, useEffect } from 'react'
import { useTheme } from './hooks/useTheme'
import { categories } from './data/categories'
import Header from './components/Header'
import CategoryTabs from './components/CategoryTabs'
import WelcomeSection from './components/WelcomeSection'
import ToolCard from './components/ToolCard'
import EmptyState from './components/EmptyState'
import Footer from './components/Footer'
import ConfirmDialog from './components/ConfirmDialog'
import AddToolModal from './components/AddToolModal'
import Toast from './components/Toast'
import type { Tool } from './data/tools'

type SourceFilter = 'all' | 'self' | 'third_party'

export default function App() {
  const { theme, toggleTheme } = useTheme()
  const [tools, setTools] = useState<Tool[]>([])
  const [activeCategory, setActiveCategory] = useState('recommend')
  const [searchQuery, setSearchQuery] = useState('')
  const [sourceFilter, setSourceFilter] = useState<SourceFilter>('self')
  const [confirmOpen, setConfirmOpen] = useState(false)
  const [confirmAction, setConfirmAction] = useState<{ title: string; message: string; onConfirm: () => void } | null>(null)
  const [addModalOpen, setAddModalOpen] = useState(false)
  const [toastVisible, setToastVisible] = useState(false)
  const [toastMessage, setToastMessage] = useState('')
  const [loading, setLoading] = useState(true)

  const fetchTools = useCallback(async () => {
    try {
      const res = await fetch('/api/v1/tools/list')
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const json = await res.json()
      if (json.code === 200) {
        setTools(json.data)
      }
    } catch {
      setTools([])
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { fetchTools() }, [fetchTools])

  const filteredTools = useMemo(() => {
    let result = tools

    if (sourceFilter !== 'all') {
      result = result.filter(t => t.source === sourceFilter)
    }

    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase().trim()
      result = result.filter(t =>
        t.name.toLowerCase().includes(q) ||
        t.description.toLowerCase().includes(q) ||
        t.tags.some(tag => tag.toLowerCase().includes(q))
      )
    } else if (activeCategory !== 'recommend') {
      result = result.filter(t => t.category === activeCategory)
    }

    return result
  }, [activeCategory, searchQuery, tools, sourceFilter])

  const customCount = useMemo(() =>
    tools.filter(t => t.toolType === 'file' || t.id > 999999).length,
    [tools]
  )

  const handleCategoryChange = useCallback((id: string) => {
    setActiveCategory(id)
    setSearchQuery('')
    setSourceFilter('all')
  }, [])

  const handleSearch = useCallback((query: string) => {
    setSearchQuery(query)
  }, [])

  const handleSourceFilterChange = useCallback((filter: SourceFilter) => {
    setSourceFilter(filter)
  }, [])

  const handleDeleteTool = useCallback((id: number) => {
    setConfirmAction({
      title: '删除工具',
      message: '确定要永久删除这个工具吗？删除后无法恢复。',
      onConfirm: async () => {
        try {
          const res = await fetch(`/api/v1/tools/delete/${id}`, { method: 'DELETE' })
          if (!res.ok) throw new Error(`HTTP ${res.status}`)
          const json = await res.json()
          if (json.code === 200) {
            setTools(prev => prev.filter(t => t.id !== id))
          } else {
            setToastMessage(json.message || '删除失败')
            setToastVisible(true)
          }
        } catch {
          setToastMessage('删除失败，请检查网络')
          setToastVisible(true)
        }
        setConfirmOpen(false)
        setConfirmAction(null)
      }
    })
    setConfirmOpen(true)
  }, [])

  const handleAddUrlTool = useCallback(async (tool: Tool) => {
    try {
      const res = await fetch('/api/v1/tools/add-url', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: tool.name,
          description: tool.description,
          icon: tool.icon,
          usageType: tool.usageType,
          source: tool.source,
          url: tool.url,
          category: tool.category,
          tags: tool.tags,
        }),
      })
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const json = await res.json()
      if (json.code === 200) {
        await fetchTools()
        setAddModalOpen(false)
        setToastMessage('添加成功')
        setToastVisible(true)
      } else {
        setToastMessage(json.message || '添加失败')
        setToastVisible(true)
      }
    } catch {
      setToastMessage('网络错误，请稍后重试')
      setToastVisible(true)
    }
  }, [fetchTools])

  const handleFileUpload = useCallback(async (formData: FormData, onProgress: (pct: number) => void): Promise<Tool | null> => {
    return new Promise((resolve) => {
      const xhr = new XMLHttpRequest()
      xhr.open('POST', '/api/v1/tools/upload')

      xhr.upload.onprogress = (e) => {
        if (e.lengthComputable) {
          onProgress(Math.round((e.loaded / e.total) * 100))
        }
      }

      xhr.onload = () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          try {
            const json = JSON.parse(xhr.responseText)
            if (json.code === 200) {
              fetchTools()
              setToastMessage('上传成功')
              setToastVisible(true)
              resolve(json.data)
            } else {
              setToastMessage(json.message || '上传失败')
              setToastVisible(true)
              resolve(null)
            }
          } catch {
            setToastMessage('服务器响应解析失败')
            setToastVisible(true)
            resolve(null)
          }
        } else {
          setToastMessage('上传失败')
          setToastVisible(true)
          resolve(null)
        }
      }

      xhr.onerror = () => {
        setToastMessage('网络连接失败')
        setToastVisible(true)
        resolve(null)
      }

      xhr.send(formData)
    })
  }, [fetchTools])

  const handleAddTool = useCallback((tool: Tool) => {
    if (tool.toolType === 'file') return
    handleAddUrlTool(tool)
  }, [handleAddUrlTool])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="text-4xl mb-4">🧰</div>
          <p className="text-sm opacity-40">加载中...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="relative min-h-screen flex flex-col">
      <div className="relative z-10 flex flex-col min-h-screen">
        <Header
          onSearch={handleSearch}
          searchQuery={searchQuery}
          theme={theme}
          onToggleTheme={toggleTheme}
        />
        <CategoryTabs
          categories={categories}
          activeCategory={activeCategory}
          onCategoryChange={handleCategoryChange}
          onAddTool={() => setAddModalOpen(true)}
          sourceFilter={sourceFilter}
          onSourceFilterChange={handleSourceFilterChange}
        />

        <div className="page-container flex-1">
          <WelcomeSection
            customCount={customCount}
            totalCount={tools.length}
            displayCount={filteredTools.length}
          />
          {searchQuery.trim() && (
            <div className="mb-4 text-[13px] opacity-40 text-center">
              搜索 "<span className="font-medium opacity-80">{searchQuery}</span>" 找到 <span className="font-semibold opacity-70">{filteredTools.length}</span> 个工具
            </div>
          )}
          {filteredTools.length > 0 ? (
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 sm:gap-5 lg:gap-6 xl:gap-7">
              {filteredTools.map((tool, index) => (
                <ToolCard key={tool.id} tool={tool} index={index} onDelete={handleDeleteTool} />
              ))}
            </div>
          ) : (
            <EmptyState />
          )}
        </div>
        <Footer />
      </div>

      <ConfirmDialog
        open={confirmOpen}
        title={confirmAction?.title || ''}
        message={confirmAction?.message || ''}
        onConfirm={confirmAction?.onConfirm || (() => {})}
        onCancel={() => { setConfirmOpen(false); setConfirmAction(null) }}
      />

      <AddToolModal
        open={addModalOpen}
        onClose={() => setAddModalOpen(false)}
        onSubmit={handleAddTool}
        onFileUpload={handleFileUpload}
      />

      <Toast
        message={toastMessage}
        visible={toastVisible}
        onClose={() => setToastVisible(false)}
      />
    </div>
  )
}
