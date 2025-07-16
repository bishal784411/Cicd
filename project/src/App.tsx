import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import AppContent from './AppContent';
import { TerminalProvider } from './components/TerminalContext'; // ✅ import your context provider

function App() {
  return (
    <TerminalProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/:page" element={<AppContent />} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </Router>
    </TerminalProvider>
  );
}

export default App;
