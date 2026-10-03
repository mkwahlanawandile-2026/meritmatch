type StatusBadgeProps = {
  status: 'Qualified' | 'Review' | 'Not Qualified'
}

export default function StatusBadge({ status }: StatusBadgeProps) {
  const styles = {
    Qualified: 'border-[#DCEFE3] bg-[#F4FBF7] text-[#28734B]',
    Review: 'border-[#F3E6C8] bg-[#FFF9ED] text-[#A56A00]',
    'Not Qualified': 'border-[#F3D6D3] bg-[#FFF6F5] text-[#B42318]',
  }

  return (
    <span
      className={`inline-flex rounded-full border px-2.5 py-1 text-[11px] font-medium ${styles[status]}`}
    >
      {status}
    </span>
  )
}
