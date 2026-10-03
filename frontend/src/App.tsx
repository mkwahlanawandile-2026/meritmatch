import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import Sidebar from './components/layout/Sidebar'
import Topbar from './components/layout/Topbar'
import Dashboard from './pages/Dashboard'
import Jobs from './pages/Jobs'
import Candidates from './pages/Candidates'
import Matches from './pages/Matches'
import Analytics from './pages/Analytics'
import Reports from './pages/Reports'
import Settings from './pages/Settings'
import Evaluate from './pages/Evaluate'

function App() {
  return (
    <BrowserRouter>
      <div className="flex min-h-screen bg-[#F7F8FA]">
        <Sidebar />

        <div className="flex min-w-0 flex-1 flex-col">
          <Topbar />

          <Routes>
            <Route path="/" element={<Dashboard />} />

            <Route path="/jobs" element={<Jobs />} />

            <Route
              path="/candidates"
              element={<Candidates />}
            />

            <Route
              path="/matches"
              element={<Matches />}
            />

            <Route
              path="/analytics"
              element={<Analytics />}
            />

            <Route
              path="/reports"
              element={<Reports />}
            />

            <Route
              path="/settings"
              element={<Settings />}
            />

            <Route
              path="/evaluate"
              element={<Evaluate />}
            />

            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  )
}

export default App