import { useNavigate, useParams } from 'react-router-dom';
import { Shield, Menu, X, ChevronLeft, ChevronRight } from 'lucide-react';

import { Navigation } from './components/Navigation';
import { DashboardPage } from './pages/DashboardPage';
import { MonitorPage } from './pages/MonitorPage';
import { SolutionsPage } from './pages/SolutionsPage';
import { FixPage } from './pages/FixPage';
import { AgentsPage } from './pages/AgentsPage';
import { ProcessFlowMap } from './pages/ProcessFlowMap'; // Adjust import if needed

import { useMonitoring } from './hooks/useMonitoring';
import { useSidebar } from './hooks/useSidebar';

type PageType = 'dashboard' | 'monitor' | 'solutions' | 'fix' | 'agents' | 'process flow';

function AppContent() {
  const { page } = useParams<{ page: string }>();
  const navigate = useNavigate();

  // Get currentPage from URL param or default to 'dashboard'
  const currentPage = (page && ['dashboard', 'monitor', 'solutions', 'fix', 'agents', 'process flow'].includes(page)
    ? (page as PageType)
    : 'dashboard');

  const { connectionStatus, lastRefresh } = useMonitoring(3000);
  const {
    isCollapsed,
    isMobileOpen,
    isMobile,
    toggleCollapse,
    toggleMobile,
    closeMobile,
  } = useSidebar();

  const sidebarWidth = isMobile ? 0 : (isCollapsed ? 80 : 320);

  const renderCurrentPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <DashboardPage />;
      case 'monitor':
        return <MonitorPage />;
      case 'solutions':
        return <SolutionsPage />;
      case 'fix':
        return <FixPage />;
      case 'agents':
        return <AgentsPage />;
      case 'process flow':
        return <ProcessFlowMap />;
      default:
        return <DashboardPage />;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex">
      {/* Mobile Sidebar Overlay */}
      {isMobileOpen && (
        <div
          className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 lg:hidden"
          onClick={closeMobile}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          fixed top-0 left-0 h-screen bg-slate-900/95 backdrop-blur-sm border-r border-slate-700/50 
          transform transition-all duration-300 ease-in-out z-50
          ${isMobile
            ? `w-80 ${isMobileOpen ? 'translate-x-0' : '-translate-x-full'}`
            : `${isCollapsed ? 'w-20' : 'w-80'}`
          }
        `}
      >
        <div className="flex flex-col h-full">
          {/* Sidebar Header */}
          <div className="p-6 border-b border-slate-700/50 flex-shrink-0">
            <div className="flex items-center justify-between">
              <div className={`flex items-center space-x-3 ${isCollapsed && !isMobile ? 'justify-center' : ''}`}>
                <Shield className="h-8 w-8 text-cyan-400 flex-shrink-0" />
                {(!isCollapsed || isMobile) && (
                  <div>
                    <h1 className="text-xl font-bold text-white">DevOps Center</h1>
                  </div>
                )}
              </div>

              {/* Mobile close button */}
              {isMobile && (
                <button
                  onClick={closeMobile}
                  className="p-2 text-gray-400 hover:text-white hover:bg-slate-700 rounded-lg transition-colors"
                >
                  <X className="h-5 w-5" />
                </button>
              )}

              {/* Desktop collapse button */}
              
            </div>
          </div>

          {/* Navigation */}
          <div className="flex-1 p-4 overflow-y-auto">
            <div className="mb-6">
              {(!isCollapsed || isMobile) && (
                <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">
                  Navigation
                </h2>
              )}
              <Navigation
                currentPage={currentPage}
                onNavigate={(page) => {
                  navigate(`/${page}`);
                  if (isMobile) closeMobile();
                }}
                isCollapsed={isCollapsed && !isMobile}
              />
            </div>
          </div>

          {/* Sidebar Footer */}
          <div className={`p-6 border-t border-slate-700/50 flex-shrink-0`}>
            <div className={`flex items-center ${isCollapsed && !isMobile ? 'justify-center' : 'justify-between'}`}>
              {(!isCollapsed || isMobile) && (
                <div className="text-xs text-gray-500">
                  <div>DevOps Control Center</div>
                  <div>Version 2.0</div>
                </div>
              )}
              
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content - Adjusted for sidebar */}
      <div
        className="flex-1 flex flex-col min-w-0 transition-all duration-300 ease-in-out"
        style={{
          marginLeft: isMobile ? 0 : `${sidebarWidth}px`
        }}
      >
        {/* Top Header */}
        <header className="bg-slate-900/80 backdrop-blur-sm border-b border-slate-700/50 sticky top-0 z-30 flex-shrink-0">
          <div className="px-4 sm:px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <button
                  onClick={toggleMobile}
                  className="lg:hidden p-2 text-gray-400 hover:text-white hover:bg-slate-700 rounded-lg transition-colors"
                >
                  <Menu className="h-5 w-5" />
                </button>
                <div className="flex flex-row items-center space-x-2">
                  {!isMobile && (
                    <button
                      onClick={toggleCollapse}
                      className="p-2 text-gray-400 hover:text-white hover:bg-slate-700 rounded-lg transition-colors"
                    >
                      {isCollapsed ? <ChevronRight className="h-5 w-5" /> : <ChevronLeft className="h-5 w-5" />}
                    </button>
                  )}
                  <h1 className="text-2xl font-bold text-white capitalize">{currentPage}</h1>
                </div>
              </div>

              
            </div>
          </div>
        </header>

        {/* Main Content Area */}
        <main className="flex-1 px-4 sm:px-6 py-4 sm:py-8 overflow-auto">
          {renderCurrentPage()}
        </main>

        {/* Footer */}
        <footer className="border-t border-slate-700/50 bg-slate-900/50 backdrop-blur-sm flex-shrink-0">
          <div className="px-4 sm:px-6 py-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between text-sm text-gray-500 gap-2">
              <div>
                <span className="hidden sm:inline">CI/CD DevOps Control Center • Real-time pipeline monitoring and automation</span>
                <span className="sm:hidden">DevOps Control Center</span>
              </div>
              <div className="flex items-center space-x-4">
                <span>Status: {connectionStatus}</span>
                <span className="hidden sm:inline">•</span>
                <span>Sync: {lastRefresh.toLocaleTimeString()}</span>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
}

export default AppContent;
