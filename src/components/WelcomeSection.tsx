interface WelcomeSectionProps {
  customCount: number
  totalCount: number
  displayCount: number
}

export default function WelcomeSection({ customCount, totalCount, displayCount }: WelcomeSectionProps) {
  const getGreeting = () => {
    const hour = new Date().getHours()
    if (hour < 6) return '夜深了'
    if (hour < 12) return '早上好'
    if (hour < 14) return '中午好'
    if (hour < 18) return '下午好'
    return '晚上好'
  }

  return (
    <div className="mb-6">
      <div className="flex items-center justify-center gap-3 mb-1">
        <span className="text-xl">👋</span>
        <h2 className="text-lg font-bold" style={{ fontFamily: 'var(--font-display)' }}>
          <span className="welcome-gradient">{getGreeting()}</span>
          <span className="opacity-60 ml-1">今天需要什么工具？</span>
        </h2>
      </div>
      <p className="text-[12px] opacity-35 text-center flex items-center justify-center gap-1.5">
        <span className="inline-flex items-center gap-1">
          <span className="w-1.5 h-1.5 rounded-full bg-[var(--color-online)]" />
          当前展示 <span className="font-semibold opacity-80">{displayCount}</span> 个
        </span>
        <span className="opacity-30">·</span>
        <span>共 {totalCount} 个可用</span>
      </p>
      {customCount > 0 && (
        <div className="flex items-center justify-center gap-2 mt-2">
          <span className="inline-flex items-center gap-1.5 text-[11px] px-3 py-1 rounded-lg font-medium"
            style={{
              background: 'linear-gradient(135deg, rgba(99,102,241,0.08), rgba(139,92,246,0.05))',
              color: '#6366F1'
            }}
          >
            ✨ {customCount} 个自定义
          </span>
        </div>
      )}
    </div>
  )
}
