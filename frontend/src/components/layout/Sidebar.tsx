import {
  BarChart3,
  BriefcaseBusiness,
  FileText,
  LayoutDashboard,
  Settings,
  Users,
  GitCompare,
  ClipboardCheck,
} from 'lucide-react'
import { NavLink } from 'react-router-dom'
import type { ComponentType } from 'react'

type NavItem = {
  label: string
  path: string
  icon: ComponentType<{ size?: number; strokeWidth?: number }>
}

const workspaceItems: NavItem[] = [
  { label: 'Dashboard', path: '/', icon: LayoutDashboard },
  { label: 'Jobs', path: '/jobs', icon: BriefcaseBusiness },
  { label: 'Candidates', path: '/candidates', icon: Users },
  { label: 'Matches', path: '/matches', icon: GitCompare },
  { label: 'Evaluate', path: '/evaluate', icon: ClipboardCheck },
]

const insightItems: NavItem[] = [
  { label: 'Analytics', path: '/analytics', icon: BarChart3 },
  { label: 'Reports', path: '/reports', icon: FileText },
]

export default function Sidebar() {
  return (
    <aside className="flex h-screen w-[248px] shrink-0 flex-col bg-[#172033] text-white">
      <div className="flex items-center gap-3 border-b border-white/10 px-5 py-5">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-white text-sm font-bold text-[#172033]">
          M
        </div>

        <div>
          <div className="text-[15px] font-semibold tracking-tight">
            MeritMatch
          </div>

          <div className="text-[11px] text-slate-400">
            Candidate Intelligence
          </div>
        </div>
      </div>

      <nav className="flex-1 px-3 py-6">
        <div className="mb-3 px-3 text-[10px] font-semibold uppercase tracking-[0.16em] text-slate-500">
          Workspace
        </div>

        <div className="space-y-1">
          {workspaceItems.map((item) => {
            const Icon = item.icon

            return (
              <NavLink
                key={item.label}
                to={item.path}
                end={item.path === '/'}
                className={({ isActive }) =>
                  `flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-left text-[13px] transition ${
                    isActive
                      ? 'bg-white text-[#172033] shadow-sm'
                      : 'text-slate-300 hover:bg-white/5 hover:text-white'
                  }`
                }
              >
                <Icon size={17} strokeWidth={1.8} />
                <span>{item.label}</span>
              </NavLink>
            )
          })}
        </div>

        <div className="mb-3 mt-8 px-3 text-[10px] font-semibold uppercase tracking-[0.16em] text-slate-500">
          Insights
        </div>

        <div className="space-y-1">
          {insightItems.map((item) => {
            const Icon = item.icon

            return (
              <NavLink
                key={item.label}
                to={item.path}
                className={({ isActive }) =>
                  `flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-left text-[13px] transition ${
                    isActive
                      ? 'bg-white text-[#172033] shadow-sm'
                      : 'text-slate-300 hover:bg-white/5 hover:text-white'
                  }`
                }
              >
                <Icon size={17} strokeWidth={1.8} />
                <span>{item.label}</span>
              </NavLink>
            )
          })}
        </div>

        <div className="mb-3 mt-8 px-3 text-[10px] font-semibold uppercase tracking-[0.16em] text-slate-500">
          System
        </div>

        <NavLink
          to="/settings"
          className={({ isActive }) =>
            `flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-left text-[13px] transition ${
              isActive
                ? 'bg-white text-[#172033] shadow-sm'
                : 'text-slate-300 hover:bg-white/5 hover:text-white'
            }`
          }
        >
          <Settings size={17} strokeWidth={1.8} />
          <span>Settings</span>
        </NavLink>
      </nav>

      <div className="border-t border-white/10 px-5 py-4 text-[11px] text-slate-500">
        MeritMatch v0.1 · Development
      </div>
    </aside>
  )
}
