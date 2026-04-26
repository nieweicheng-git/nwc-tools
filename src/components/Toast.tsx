import { useEffect, useState } from 'react'

interface ToastProps {
  message: string
  visible: boolean
  onClose: () => void
}

export default function Toast({ message, visible, onClose }: ToastProps) {
  const [show, setShow] = useState(false)

  useEffect(() => {
    if (visible) {
      setShow(true)
      const timer = setTimeout(() => {
        setShow(false)
        setTimeout(onClose, 300)
      }, 2000)
      return () => clearTimeout(timer)
    }
  }, [visible, onClose])

  if (!visible && !show) return null

  return (
    <div className={`toast-container ${show && visible ? 'toast-enter' : 'toast-exit'}`}>
      <div className="toast-content">
        <span className="mr-2">✅</span>
        <span className="text-sm font-medium">{message}</span>
      </div>
    </div>
  )
}
