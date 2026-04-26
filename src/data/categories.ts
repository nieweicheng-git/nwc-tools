export interface Category {
  id: string
  name: string
  icon: string
  sortOrder: number
}

export const categories: Category[] = [
  { id: 'recommend', name: '推荐', icon: '✨', sortOrder: 0 },
  { id: 'dev', name: '开发工具', icon: '🛠', sortOrder: 1 },
  { id: 'design', name: '设计工具', icon: '🎨', sortOrder: 2 },
  { id: 'office', name: '办公工具', icon: '📊', sortOrder: 3 },
  { id: 'system', name: '系统工具', icon: '🔧', sortOrder: 4 },
  { id: 'entertainment', name: '娱乐工具', icon: '🎮', sortOrder: 5 }
]
