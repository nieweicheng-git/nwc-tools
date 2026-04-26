import { useState, useEffect, useRef } from 'react'

interface HeaderProps {
  onSearch: (query: string) => void
  searchQuery: string
  theme: 'light' | 'dark'
  onToggleTheme: () => void
}

export default function Header({ onSearch, searchQuery, theme, onToggleTheme }: HeaderProps) {
  const [localQuery, setLocalQuery] = useState(searchQuery)
  const debounceRef = useRef<ReturnType<typeof setTimeout>>(null)
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    setLocalQuery(searchQuery)
  }, [searchQuery])

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 100)
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value
    setLocalQuery(value)
    if (debounceRef.current) clearTimeout(debounceRef.current)
    debounceRef.current = setTimeout(() => onSearch(value), 300)
  }

  const handleClear = () => {
    setLocalQuery('')
    onSearch('')
  }

  return (
    <header className="px-4 sm:px-6 lg:px-8 pt-4 pb-2 sticky top-0 z-50 transition-all duration-300">
      <div className={`glass-nav ${scrolled ? 'scrolled' : ''}`}>
        <div className="flex items-center justify-between gap-4 w-full">
          <div
            className="flex items-center gap-2.5 shrink-0 cursor-pointer"
            onClick={() => { handleClear(); onSearch('') }}
          >
            <span className="text-[22px]">🧰</span>
            <h1 className="text-lg font-bold" style={{ fontFamily: 'var(--font-display)' }}>
              <span className="welcome-gradient">小工具百宝箱</span>
            </h1>
          </div>

          <div className="glass-search relative">
            <div className="absolute left-4 top-1/2 -translate-y-1/2">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="opacity-30">
                <circle cx="11" cy="11" r="8" />
                <path d="m21 21-4.3-4.3" />
              </svg>
            </div>
            <input
              type="text"
              value={localQuery}
              onChange={handleInputChange}
              placeholder="搜索工具..."
              className="w-full h-full pl-10 pr-9 text-sm bg-transparent outline-none placeholder:opacity-40 text-center"
              style={{ fontFamily: 'var(--font-body)' }}
            />
            {localQuery && (
              <button
                onClick={handleClear}
                className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 rounded-full flex items-center justify-center opacity-30 hover:opacity-60 transition-opacity cursor-pointer"
              >
                <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
                  <path d="M18 6 6 18M6 6l12 12" />
                </svg>
              </button>
            )}
          </div>

          <button onClick={onToggleTheme} className="theme-toggle" aria-label="切换主题">
            <div className="theme-toggle-knob">
              {theme === 'light' ? '☀️' : '🌙'}
            </div>
          </button>
        </div>
      </div>
    </header>
  )
}
