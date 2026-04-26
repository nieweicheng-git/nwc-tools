export default function Footer() {
  return (
    <footer className="pb-10 pt-8">
      <div className="max-w-[1200px] mx-auto text-center px-6">
        <div className="h-px bg-gradient-to-r from-transparent via-[var(--color-accent)]/10 to-transparent mb-6" />
        <div className="flex items-center justify-center gap-2 mb-2">
          <span className="text-[14px]">🧰</span>
          <span className="text-sm font-semibold opacity-25" style={{ fontFamily: 'var(--font-display)' }}>
            小工具百宝箱
          </span>
        </div>
        <p className="text-[11px] opacity-20">
          © 2025 Toolbox Hub · 你可以完全自定义你的工具列表
        </p>
      </div>
    </footer>
  )
}
