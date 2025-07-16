import React from 'react';
import { BarChart3, Monitor, Wrench, Hammer, Bot } from 'lucide-react';
// import { PageType } from '../hooks/useNavigation';

export type PageType = 
  | 'dashboard'
  | 'monitor'
  | 'solutions'
  | 'fix'
  | 'agents'
  | 'process flow';


interface NavigationProps {
  currentPage: PageType;
  onNavigate: (page: PageType) => void;
  isCollapsed: boolean;
}

export const Navigation: React.FC<NavigationProps> = ({ currentPage, onNavigate, isCollapsed }) => {
  const navItems = [
    { id: 'dashboard' as PageType, label: 'Dashboard', icon: BarChart3 },
    { id: 'monitor' as PageType, label: 'Monitor', icon: Monitor},
    { id: 'solutions' as PageType, label: 'Solutions', icon: Wrench},
    { id: 'fix' as PageType, label: 'Fix', icon: Hammer},
    { id: 'agents' as PageType, label: 'Agents', icon: Bot },
    { id: 'process flow' as PageType, label:'CI/CD Flow', icon: Bot},

  ];

  return (
    <nav className="space-y-2">
      {navItems.map((item) => {
        const Icon = item.icon;
        const isActive = currentPage === item.id;
        
        return (
          <button
            key={item.id}
            onClick={() => onNavigate(item.id)}
            className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-all duration-200 text-left group ${
              isActive
                ? 'bg-cyan-600 text-white shadow-lg'
                : 'text-gray-300 hover:text-white hover:bg-slate-700/50'
            }`}
            title={isCollapsed ? item.label : undefined}
          >
            <Icon className="h-5 w-5 flex-shrink-0" />
            {!isCollapsed && (
              <div className="flex-1 min-w-0">
                <div className="font-medium">{item.label}</div> 
                <div className={`text-xs ${isActive ? 'text-cyan-100' : 'text-gray-400 group-hover:text-gray-300'}`}>
                </div>
              </div>
            )}
          </button>
        );
      })}
    </nav>
  );
};