import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import AppContent from './AppContent';
import { TerminalProvider } from './components/TerminalContext';
import { AuthProvider } from './components/AuthProvider';
import { LoginPage } from './pages/LoginPage';

function App() {
  return (
    <AuthProvider>
      <TerminalProvider>
        <Router>
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/:page" element={<AppContent />} />
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
            <Route path="/loginpage" element={<LoginPage />} />
          </Routes>
        </Router>
      </TerminalProvider>
    </AuthProvider>
  );
}

export default App;
