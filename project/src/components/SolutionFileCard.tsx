// import React, { useRef, useState } from 'react';
// import { ChevronDown, ChevronRight, FileText, Clock, TrendingUp, Wrench, TrendingDown } from 'lucide-react';
// import { SolutionStatus } from '../types/monitoring';
// import { StatusBadge } from './StatusBadge';
// import { SolutionCard } from './solutionCard';
// import { useTerminal } from '../components/TerminalContext';


// interface SolutionCardProps {
//   file: SolutionStatus;
//   onTriggerFix?: (filePath: string, errorIndex: number) => void;
// }



// export const FileCard: React.FC<SolutionCardProps> = ({ file, onTriggerFix }) => {
//   const [isExpanded, setIsExpanded] = useState(false);
//   const { isOpen: showTerminal, openTerminal, closeTerminal, clearTerminal, appendLog } = useTerminal();
//   const eventSourceRef = useRef<EventSource | null>(null);


//   const getBuildStatusColor = (status?: string) => {
//     switch (status) {
//       case 'success': return 'text-green-400';
//       case 'failed': return 'text-red-400';
//       case 'running': return 'text-yellow-400';
//       case 'pending': return 'text-blue-400';
//       default: return 'text-gray-400';
//     }
//   };


//   const getBuildStatusIcon = (status?: string) => {
//     switch (status) {
//       case 'success':
//         return <TrendingUp className="h-4 w-4 text-green-500" />;

//       case 'failed':
//         return <TrendingDown className="h-4 w-4 text-red-500" />;
//     }
//   };

//   const getPipelineStageColor = (stage?: string) => {
//     switch (stage) {
//       case 'build': return 'bg-blue-500/20 text-blue-300';
//       case 'test': return 'bg-purple-500/20 text-purple-300';
//       case 'deploy': return 'bg-green-500/20 text-green-300';
//       case 'post-deploy': return 'bg-cyan-500/20 text-cyan-300';
//       default: return 'bg-gray-500/20 text-gray-300';
//     }
//   };

//   const toggleTerminalAndStreamLogs = (e: React.MouseEvent) => {
//       e.stopPropagation();
  
//       if (!isExpanded) setIsExpanded(true);
  
//       if (!showTerminal) {
//         openTerminal();
//         clearTerminal();
  
//         // Use the first error's err_id to stream logs
       
  
       
//       } else {
//         closeTerminal();
//         eventSourceRef.current?.close();
//         eventSourceRef.current = null;
//       }
//     };


//   return (
//     <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 overflow-hidden hover:border-slate-600/50 transition-colors">
//       <div 
//         className="p-4 cursor-pointer hover:bg-slate-700/20 transition-colors"
//         onClick={() => setIsExpanded(!isExpanded)}
//       >
//         <div className="flex items-center justify-between">
//           <div className="flex items-center space-x-3">
//             <div className="flex items-center space-x-2">
//               {file.errors.length > 0 ? (
//                 isExpanded ? <ChevronDown className="h-4 w-4 text-gray-400" /> : <ChevronRight className="h-4 w-4 text-gray-400" />
//               ) : (
//                 <FileText className="h-4 w-4 text-gray-400" />
//               )}
//             </div>
//             <div className="flex-1">
//               <div className="flex items-center space-x-2 mb-1">
//                 <h3 className="font-medium text-white text-sm">{file.file}</h3>
//                 {file.pipeline_stage && (
//                   <span className={`px-2 py-1 text-xs rounded-full ${getPipelineStageColor(file.pipeline_stage)}`}>
//                     {file.pipeline_stage}
//                   </span>
//                 )}
//               </div>
//               <div className="flex items-center space-x-4 text-xs text-gray-400">
//                 <div className="flex items-center space-x-1">
//                   <Clock className="h-3 w-3" />
//                   <span>Last checked: {new Date(file.last_checked).toLocaleString()}</span>
//                 </div>
//                 {file.build_status && (
//                   <div className="flex items-center space-x-1">
//                     <span>{getBuildStatusIcon(file.build_status)}</span>
//                     <span className={getBuildStatusColor(file.build_status)}>
//                       Github Push: {file.build_status}
//                     </span>
//                   </div>
//                 )}
                
//                 {file.last_fix_attempt && (
//                   <div className="flex items-center space-x-1">
//                     <Wrench className="h-3 w-3" />
//                     <span>Last fix: {new Date(file.last_fix_attempt).toLocaleString()}</span>
//                   </div>
//                 )}
//               </div>
//             </div>
//           </div>

//           <button
//               onClick={toggleTerminalAndStreamLogs}
//               className="px-4 py-1 bg-slate-600 hover:bg-slate-700 text-white text-xs rounded"
//             >
//               {showTerminal ? 'Hide Terminal' : 'Give Fix'}
//             </button>
//           <StatusBadge 
//             status={file.status} 
//             errorCount={file.error_count}
            
//           />
//         </div>
//       </div>

//       {isExpanded && file.errors.length > 0 && (
//         <div className="border-t border-slate-700/50 p-4 space-y-4 bg-slate-900/20">
//           <div className="flex items-center justify-between text-sm">
//             <span className="text-gray-300">
//               {file.errors.length} issue{file.errors.length !== 1 ? 's' : ''} detected
//             </span>
            
//           </div>
//           {file.solutions.map((solution, index) => (
//             <SolutionCard
//               key={solution.id}
//               solution={solution}
//               onTriggerExecute={() => onTriggerFix?.(file.file, index)}
              
//             />
//           ))}

//         </div>
//       )}
//     </div>
//   );
// };


import React, { useRef, useState } from 'react';
import { ChevronDown, ChevronRight, FileText, Clock, TrendingUp, Wrench, TrendingDown } from 'lucide-react';
import { SolutionStatus } from '../types/monitoring';
import { StatusBadge } from './StatusBadge';
import { SolutionCard } from './solutionCard';
import { useTerminal } from '../components/TerminalContext';

interface SolutionCardProps {
  file: SolutionStatus;
  onTriggerFix?: (filePath: string, errorIndex: number) => void;
}

export const FileCard: React.FC<SolutionCardProps> = ({ file, onTriggerFix }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [activeSolutionId, setActiveSolutionId] = useState<string | null>(null);

  const { isOpen: showTerminal, openTerminal, closeTerminal, clearTerminal, appendLog } = useTerminal();
  const eventSourceRef = useRef<EventSource | null>(null);

  const getBuildStatusColor = (status?: string) => {
    switch (status) {
      case 'success': return 'text-green-400';
      case 'failed': return 'text-red-400';
      case 'running': return 'text-yellow-400';
      case 'pending': return 'text-blue-400';
      default: return 'text-gray-400';
    }
  };

  const getBuildStatusIcon = (status?: string) => {
    switch (status) {
      case 'success':
        return <TrendingUp className="h-4 w-4 text-green-500" />;
      case 'failed':
        return <TrendingDown className="h-4 w-4 text-red-500" />;
      default:
        return null;
    }
  };

  const getPipelineStageColor = (stage?: string) => {
    switch (stage) {
      case 'build': return 'bg-blue-500/20 text-blue-300';
      case 'test': return 'bg-purple-500/20 text-purple-300';
      case 'deploy': return 'bg-green-500/20 text-green-300';
      case 'post-deploy': return 'bg-cyan-500/20 text-cyan-300';
      default: return 'bg-gray-500/20 text-gray-300';
    }
  };

  const toggleTerminalAndStreamLogs = (e: React.MouseEvent) => {
    e.stopPropagation();
    setIsExpanded(true);

    if (showTerminal) {
      // Close terminal and stop streaming logs
      closeTerminal();
      eventSourceRef.current?.close();
      eventSourceRef.current = null;
      setActiveSolutionId(null);
    } else {
      // If no solution selected yet, do nothing on this generic toggle
      // We want terminal only opened per solution now
      openTerminal();
    }
  };

  const handleExecuteSolution = (solutionId: string) => {
    setIsExpanded(true);
    setActiveSolutionId(solutionId);

    openTerminal();
    clearTerminal();

    // Close existing connection if any
    eventSourceRef.current?.close();

    // Open new EventSource stream for logs of the selected solution
    eventSourceRef.current = new EventSource(`${import.meta.env.VITE_API_BASE_URL}/solution/${solutionId}/stream/logs`);

    eventSourceRef.current.onmessage = (event) => {
      appendLog(event.data);
    };

    eventSourceRef.current.onerror = () => {
      appendLog('\n--- Script finished running ---');
      eventSourceRef.current?.close();
      eventSourceRef.current = null;
    };

    // Scroll to the solution card
    setTimeout(() => {
      document.getElementById(`solution-${solutionId}`)?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }, 100);
  };

  return (
    <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 overflow-hidden hover:border-slate-600/50 transition-colors">
      <div
        className="p-4 cursor-pointer hover:bg-slate-700/20 transition-colors"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-2">
              {file.errors.length > 0 ? (
                isExpanded ? <ChevronDown className="h-4 w-4 text-gray-400" /> : <ChevronRight className="h-4 w-4 text-gray-400" />
              ) : (
                <FileText className="h-4 w-4 text-gray-400" />
              )}
            </div>
            <div className="flex-1">
              <div className="flex items-center space-x-2 mb-1">
                <h3 className="font-medium text-white text-sm">{file.file}</h3>
                {file.pipeline_stage && (
                  <span className={`px-2 py-1 text-xs rounded-full ${getPipelineStageColor(file.pipeline_stage)}`}>
                    {file.pipeline_stage}
                  </span>
                )}
              </div>
              <div className="flex items-center space-x-4 text-xs text-gray-400">
                <div className="flex items-center space-x-1">
                  <Clock className="h-3 w-3" />
                  <span>Last checked: {new Date(file.last_checked).toLocaleString()}</span>
                </div>
                {file.build_status && (
                  <div className="flex items-center space-x-1">
                    <span>{getBuildStatusIcon(file.build_status)}</span>
                    <span className={getBuildStatusColor(file.build_status)}>
                      Github Push: {file.build_status}
                    </span>
                  </div>
                )}
                {file.last_fix_attempt && (
                  <div className="flex items-center space-x-1">
                    <Wrench className="h-3 w-3" />
                    <span>Last fix: {new Date(file.last_fix_attempt).toLocaleString()}</span>
                  </div>
                )}
              </div>
            </div>
          </div>

          <button
            onClick={toggleTerminalAndStreamLogs}
            className="px-4 py-1 bg-slate-600 hover:bg-slate-700 text-white text-xs rounded"
          >
            {showTerminal ? 'Hide Terminal' : 'Give Fix'}
          </button>
          <StatusBadge
            status={file.status}
            errorCount={file.error_count}
          />
        </div>
      </div>

      {isExpanded && file.errors.length > 0 && (
        <div className="border-t border-slate-700/50 p-4 space-y-4 bg-slate-900/20">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-300">
              {file.errors.length} issue{file.errors.length !== 1 ? 's' : ''} detected
            </span>
          </div>

          {file.solutions.map((solution, index) => (
            <div key={solution.id} id={`solution-${solution.id}`}>
              <SolutionCard
                solution={solution}
                onTriggerExecute={() => handleExecuteSolution(solution.id)}
              />
              
              {/* Render Terminal below the active solution */}
              {showTerminal && activeSolutionId === solution.id && (
                <div className="bg-black p-4 rounded-lg border border-slate-700 text-green-400 text-xs font-mono whitespace-pre-wrap max-h-64 overflow-auto mt-2">
                  {/* The terminal output should come from your TerminalContext appendLog */}
                  {/* If you have a Terminal component you can place it here */}
                  Terminal is open and streaming logs for this solution...
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
