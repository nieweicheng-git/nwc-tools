interface ConfirmDialogProps {
  open: boolean
  title: string
  message: string
  confirmText?: string
  cancelText?: string
  onConfirm: () => void
  onCancel: () => void
}

export default function ConfirmDialog({ open, title, message, confirmText = '确定', cancelText = '取消', onConfirm, onCancel }: ConfirmDialogProps) {
  if (!open) return null

  return (
    <div className="modal-overlay" onClick={onCancel}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <h3 className="text-lg font-bold mb-2 text-center" style={{ fontFamily: 'var(--font-display)' }}>{title}</h3>
        <p className="text-sm opacity-60 mb-6 leading-relaxed text-center">{message}</p>
        <div className="flex justify-center gap-4">
          <button onClick={onCancel} className="btn-cancel">
            {cancelText}
          </button>
          <button onClick={onConfirm} className="btn-danger">
            {confirmText}
          </button>
        </div>
      </div>
    </div>
  )
}
