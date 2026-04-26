import type { Category } from '../data/categories'

type SourceFilter = 'all' | 'self' | 'third_party'

interface CategoryTabsProps {
  categories: Category[]
  activeCategory: string
  onCategoryChange: (id: string) => void
  onAddTool: () => void
  sourceFilter: SourceFilter
  onSourceFilterChange: (filter: SourceFilter) => void
}

const sourceOptions: { value: SourceFilter; label: string }[] = [
  { value: 'self', label: '自研' },
  { value: 'third_party', label: '第三方' },
  { value: 'all', label: '全部' },
]

export default function CategoryTabs({ categories, activeCategory, onCategoryChange, onAddTool, sourceFilter, onSourceFilterChange }: CategoryTabsProps) {
  return (
    <div className="px-4 sm:px-6 lg:px-8 py-4">
      <div className="category-bar">
        <div className="category-bar-scroll">
          {categories.map(cat => (
            <button
              key={cat.id}
              onClick={() => onCategoryChange(cat.id)}
              className={`category-tag ${activeCategory === cat.id ? 'active' : ''}`}
            >
              <span>{cat.icon}</span>
              <span>{cat.name}</span>
            </button>
          ))}

          <div className="category-separator" />

          {sourceOptions.map(opt => (
            <button
              key={opt.value}
              onClick={() => onSourceFilterChange(opt.value)}
              className={`category-tag ${sourceFilter === opt.value ? 'active' : ''}`}
            >
              {opt.label}
            </button>
          ))}

          <div className="category-separator" />

          <button
            onClick={onAddTool}
            className="category-tag category-tag-add"
          >
            <span>➕</span>
            <span>添加工具</span>
          </button>
        </div>
      </div>
    </div>
  )
}
