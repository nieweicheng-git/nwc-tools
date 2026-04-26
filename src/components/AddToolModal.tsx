import { useState, useRef, useCallback } from 'react'
import type { Tool } from '../data/tools'
import { categories } from '../data/categories'

interface AddToolModalProps {
  open: boolean
  onClose: () => void
  onSubmit: (tool: Tool) => void
  onFileUpload: (formData: FormData, onProgress: (pct: number) => void) => Promise<Tool | null>
}

const EMOJI_OPTIONS = ['🔧', '💻', '🎨', '📊', '📝', '🖼️', '🔍', '⚡', '🚀', '🎮', '📱', '🌐', '📄', '🎯', '💡', '🔑', '📦', '🛡️', '🔔', '🗂️']

type AddMode = 'url' | 'file'

export default function AddToolModal({ open, onClose, onSubmit, onFileUpload }: AddToolModalProps) {
  const [mode, setMode] = useState<AddMode>('url')
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [url, setUrl] = useState('')
  const [usageType, setUsageType] = useState<'online' | 'download'>('online')
  const [source, setSource] = useState<'self' | 'third_party'>('third_party')
  const [category, setCategory] = useState('dev')
  const [icon, setIcon] = useState('🔧')
  const [tagsInput, setTagsInput] = useState('')
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [showEmojiPicker, setShowEmojiPicker] = useState(false)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [uploading, setUploading] = useState(false)
  const [dragOver, setDragOver] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const validate = (): boolean => {
    const e: Record<string, string> = {}
    if (!name.trim()) e.name = '工具名称不能为空'
    else if (name.trim().length > 20) e.name = '最多20个字符'
    if (!description.trim()) e.description = '工具描述不能为空'
    else if (description.trim().length > 50) e.description = '最多50个字符'
    if (mode === 'url') {
      if (!url.trim()) e.url = '工具链接不能为空'
      else if (!/^https?:\/\/.+/.test(url.trim())) e.url = '请输入合法的链接（http/https开头）'
    } else {
      if (!selectedFile) e.file = '请选择要上传的文件'
    }
    setErrors(e)
    return Object.keys(e).length === 0
  }

  const handleSubmit = async () => {
    if (!validate()) return

    if (mode === 'file' && selectedFile) {
      setUploading(true)
      setUploadProgress(0)
      const formData = new FormData()
      formData.append('file', selectedFile)
      formData.append('name', name.trim())
      formData.append('description', description.trim())
      formData.append('icon', icon)
      formData.append('category', category)
      formData.append('tags', tagsInput)

      const result = await onFileUpload(formData, (pct) => setUploadProgress(pct))
      setUploading(false)
      if (result) {
        onSubmit(result)
        resetForm()
      }
      return
    }

    const tags = tagsInput.split(/[,，]/).map(t => t.trim()).filter(Boolean).slice(0, 3).map(t => t.slice(0, 4))
    const tool: Tool = {
      id: Date.now(),
      name: name.trim(),
      description: description.trim(),
      icon,
      usageType,
      source,
      toolType: 'url',
      url: url.trim(),
      category,
      tags,
    }
    onSubmit(tool)
    resetForm()
  }

  const handleFileSelect = (file: File) => {
    setSelectedFile(file)
    if (!name.trim()) {
      const baseName = file.name.replace(/\.[^.]+$/, '')
      setName(baseName.slice(0, 20))
    }
    setErrors(prev => { const { file: _, ...rest } = prev; return rest })
  }

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setDragOver(false)
    const file = e.dataTransfer.files[0]
    if (file) handleFileSelect(file)
  }, [])

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setDragOver(true)
  }, [])

  const handleDragLeave = useCallback(() => {
    setDragOver(false)
  }, [])

  const resetForm = () => {
    setName('')
    setDescription('')
    setUrl('')
    setUsageType('online')
    setSource('third_party')
    setCategory('dev')
    setIcon('🔧')
    setTagsInput('')
    setErrors({})
    setShowEmojiPicker(false)
    setSelectedFile(null)
    setUploadProgress(0)
    setUploading(false)
    setDragOver(false)
    setMode('url')
  }

  const handleClose = () => {
    resetForm()
    onClose()
  }

  if (!open) return null

  return (
    <div className="modal-overlay" onClick={handleClose}>
      <div className="modal-content modal-lg" onClick={e => e.stopPropagation()}>
        <h3 className="text-xl font-bold mb-5 text-center" style={{ fontFamily: 'var(--font-display)' }}>添加新工具</h3>

        <div className="flex justify-center gap-2 mb-5">
          <button
            onClick={() => setMode('url')}
            className={`category-tag ${mode === 'url' ? 'active' : ''}`}
            style={{ minWidth: '100px' }}
          >
            🔗 URL链接
          </button>
          <button
            onClick={() => setMode('file')}
            className={`category-tag ${mode === 'file' ? 'active' : ''}`}
            style={{ minWidth: '100px' }}
          >
            📁 文件上传
          </button>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-xs font-medium opacity-50 mb-1.5 text-center">工具名称 <span className="text-[#EF4444]">*</span></label>
            <input value={name} onChange={e => setName(e.target.value)} placeholder="例如：在线图片压缩" maxLength={20} className="form-input" />
            {errors.name && <p className="text-xs text-[#EF4444] mt-1 text-center">{errors.name}</p>}
          </div>

          <div>
            <label className="block text-xs font-medium opacity-50 mb-1.5 text-center">工具描述 <span className="text-[#EF4444]">*</span></label>
            <input value={description} onChange={e => setDescription(e.target.value)} placeholder="一句话说明工具用途" maxLength={50} className="form-input" />
            {errors.description && <p className="text-xs text-[#EF4444] mt-1 text-center">{errors.description}</p>}
          </div>

          {mode === 'url' ? (
            <div>
              <label className="block text-xs font-medium opacity-50 mb-1.5 text-center">工具链接 <span className="text-[#EF4444]">*</span></label>
              <input value={url} onChange={e => setUrl(e.target.value)} placeholder="https://example.com" className="form-input" />
              {errors.url && <p className="text-xs text-[#EF4444] mt-1 text-center">{errors.url}</p>}
            </div>
          ) : (
            <div>
              <label className="block text-xs font-medium opacity-50 mb-1.5 text-center">上传文件 <span className="text-[#EF4444]">*</span></label>
              <div
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onClick={() => fileInputRef.current?.click()}
                className={`form-input cursor-pointer flex flex-col items-center justify-center gap-1 h-auto min-h-[80px] py-3 transition-all
                  ${dragOver ? 'border-[#6366F1] bg-[rgba(99,102,241,0.05)]' : ''}
                  ${selectedFile ? 'border-green-400' : ''}`}
              >
                <input ref={fileInputRef} type="file" className="hidden" onChange={e => { if (e.target.files?.[0]) handleFileSelect(e.target.files[0]) }} />
                {selectedFile ? (
                  <>
                    <span className="text-sm font-medium opacity-70">📎 {selectedFile.name}</span>
                    <span className="text-xs opacity-40">{(selectedFile.size / 1024).toFixed(1)} KB</span>
                  </>
                ) : (
                  <>
                    <span className="text-sm opacity-50">点击选择文件，或者拖放文件到这里</span>
                    <span className="text-xs opacity-30">支持所有类型，最大100MB</span>
                  </>
                )}
              </div>
              {errors.file && <p className="text-xs text-[#EF4444] mt-1 text-center">{errors.file}</p>}
              {uploading && (
                <div className="mt-2">
                  <div className="w-full h-2 rounded-full bg-black/5 dark:bg-white/5 overflow-hidden">
                    <div
                      className="h-full rounded-full bg-gradient-to-r from-[#6366F1] to-[#8B5CF6] transition-all duration-300"
                      style={{ width: `${uploadProgress}%` }}
                    />
                  </div>
                  <p className="text-xs opacity-40 text-center mt-1">上传中 {uploadProgress}%</p>
                </div>
              )}
            </div>
          )}

          {mode === 'url' && (
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-medium opacity-50 mb-1.5 text-center">使用类型</label>
                <select value={usageType} onChange={e => setUsageType(e.target.value as 'online' | 'download')} className="form-select">
                  <option value="online">在线使用</option>
                  <option value="download">下载安装</option>
                </select>
              </div>
              <div>
                <label className="block text-xs font-medium opacity-50 mb-1.5 text-center">工具来源</label>
                <select value={source} onChange={e => setSource(e.target.value as 'self' | 'third_party')} className="form-select">
                  <option value="third_party">第三方工具</option>
                  <option value="self">自研工具</option>
                </select>
              </div>
            </div>
          )}

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium opacity-50 mb-1.5 text-center">分类</label>
              <select value={category} onChange={e => setCategory(e.target.value)} className="form-select">
                {categories.filter(c => c.id !== 'recommend').map(c => (
                  <option key={c.id} value={c.id}>{c.icon} {c.name}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-xs font-medium opacity-50 mb-1.5 text-center">图标</label>
              <div className="relative">
                <button type="button" onClick={() => setShowEmojiPicker(!showEmojiPicker)} className="form-input flex items-center justify-center gap-2 cursor-pointer w-full">
                  <span className="text-xl">{icon}</span>
                  <span className="text-xs opacity-40">点击选择</span>
                </button>
                {showEmojiPicker && (
                  <div className="absolute top-full left-0 mt-1 p-2 rounded-xl bg-white dark:bg-[#2A2A35] shadow-lg border border-black/5 dark:border-white/5 z-50 grid grid-cols-5 gap-1">
                    {EMOJI_OPTIONS.map(e => (
                      <button key={e} type="button" onClick={() => { setIcon(e); setShowEmojiPicker(false) }} className="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-black/5 dark:hover:bg-white/5 text-lg cursor-pointer">
                        {e}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium opacity-50 mb-1.5 text-center">标签</label>
            <input value={tagsInput} onChange={e => setTagsInput(e.target.value)} placeholder="逗号分隔，最多3个" className="form-input" />
          </div>
        </div>

        <div className="flex justify-center gap-4 mt-6 pt-4 border-t border-black/5 dark:border-white/5">
          <button onClick={handleClose} className="btn-cancel" disabled={uploading}>取消</button>
          <button onClick={handleSubmit} className="btn-primary" disabled={uploading}>
            {uploading ? `上传中 ${uploadProgress}%` : '提交'}
          </button>
        </div>
      </div>
    </div>
  )
}
