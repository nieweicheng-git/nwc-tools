export default function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center py-28 animate-fade-in-up">
      <div className="text-5xl mb-4">🔍</div>
      <h3 className="text-lg font-semibold mb-2 opacity-50" style={{ fontFamily: 'var(--font-display)' }}>
        暂无工具
      </h3>
      <p className="text-sm opacity-30">换个关键词试试吧</p>
    </div>
  )
}
