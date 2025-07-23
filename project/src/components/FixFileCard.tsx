// import React, { useState } from 'react';
// import { ChevronDown, ChevronRight, FileText, Clock, TrendingUp, Wrench, X } from 'lucide-react';
// import { FileStatusFix } from '../types/monitoring';
// import { StatusBadge } from './StatusBadge';
// import { FixErrorCard } from './FixErrorCard';

// interface FixFileCardProps {
//     file: FileStatusFix;
//     onTriggerFix?: (filePath: string, fixIndex: number) => void;
// }

// export const FixFileCard: React.FC<FixFileCardProps> = ({ file, onTriggerFix }) => {
//     const [isExpanded, setIsExpanded] = useState(false);
//     const [showTerminal, setShowTerminal] = useState(false);
//     const [terminalContent, setTerminalContent] = useState<string[]>([]);
//     const [isProcessing, setIsProcessing] = useState(false);

//     const getUptimeColor = (uptime?: number) => {
//         if (!uptime) return 'text-gray-400';
//         if (uptime >= 99) return 'text-green-400';
//         if (uptime >= 95) return 'text-yellow-400';
//         return 'text-red-400';
//     };

//     const getBuildStatusColor = (status?: string) => {
//         switch (status) {
//             case 'success': return 'text-green-400';
//             case 'failed': return 'text-red-400';
//             case 'running': return 'text-yellow-400';
//             case 'pending': return 'text-blue-400';
//             default: return 'text-gray-400';
//         }
//     };

//     const getBuildStatusIcon = (status?: string) => {
//         switch (status) {
//             case 'success': return '✅';
//             case 'failed': return '❌';
//             case 'running': return '🔄';
//             case 'pending': return '⏳';
//             default: return '❓';
//         }
//     };

//     const getPipelineStageColor = (stage?: string) => {
//         switch (stage) {
//             case 'build': return 'bg-blue-500/20 text-blue-300';
//             case 'test': return 'bg-purple-500/20 text-purple-300';
//             case 'deploy': return 'bg-green-500/20 text-green-300';
//             case 'post-deploy': return 'bg-cyan-500/20 text-cyan-300';
//             default: return 'bg-gray-500/20 text-gray-300';
//         }
//     };

//     const handleTriggerFix = (errorIndex: number) => {
//         setShowTerminal(true);
//         setIsProcessing(true);
//         setTerminalContent([]);

//         // Scroll to the file card
//         setTimeout(() => {
//             const element = document.getElementById(`file-card-${file.file.replace(/[^a-zA-Z0-9]/g, '-')}`);
//             if (element) {
//                 element.scrollIntoView({ behavior: 'smooth', block: 'center' });
//             }
//         }, 100);

//         // Simulate Git push process
//         const gitCommands = [
//             '$ git add .',
//             '$ git commit -m "Fix: Resolve ' + file.errors[errorIndex]?.error_type + ' error in ' + file.file + '"',
//             '[main ' + Math.random().toString(36).substr(2, 7) + '] Fix: Resolve ' + file.errors[errorIndex]?.error_type + ' error in ' + file.file,
//             ' 1 file changed, ' + Math.floor(Math.random() * 10 + 1) + ' insertions(+), ' + Math.floor(Math.random() * 5 + 1) + ' deletions(-)',
//             '$ git push origin main',
//             'Enumerating objects: ' + Math.floor(Math.random() * 10 + 5) + ', done.',
//             'Counting objects: 100% (' + Math.floor(Math.random() * 10 + 5) + '/' + Math.floor(Math.random() * 10 + 5) + '), done.',
//             'Delta compression using up to 8 threads',
//             'Compressing objects: 100% (' + Math.floor(Math.random() * 5 + 3) + '/' + Math.floor(Math.random() * 5 + 3) + '), done.',
//             'Writing objects: 100% (' + Math.floor(Math.random() * 10 + 5) + '/' + Math.floor(Math.random() * 10 + 5) + '), ' + Math.floor(Math.random() * 1000 + 500) + ' bytes | ' + Math.floor(Math.random() * 100 + 50) + '.00 KiB/s, done.',
//             'Total ' + Math.floor(Math.random() * 10 + 5) + ' (delta ' + Math.floor(Math.random() * 3 + 1) + '), reused 0 (delta 0), pack-reused 0',
//             'remote: Resolving deltas: 100% (' + Math.floor(Math.random() * 3 + 1) + '/' + Math.floor(Math.random() * 3 + 1) + '), done.',
//             'To https://github.com/user/repo.git',
//             '   ' + Math.random().toString(36).substr(2, 7) + '..' + Math.random().toString(36).substr(2, 7) + '  main -> main',
//             '',
//             '✅ Successfully pushed fix to GitHub!',
//             '🚀 CI/CD pipeline triggered automatically',
//             '📦 Build and deployment in progress...'
//         ];

//         let commandIndex = 0;
//         const interval = setInterval(() => {
//             if (commandIndex < gitCommands.length) {
//                 setTerminalContent(prev => [...prev, gitCommands[commandIndex]]);
//                 commandIndex++;
//             } else {
//                 setIsProcessing(false);
//                 clearInterval(interval);

//                 // Call the original trigger fix if provided
//                 if (onTriggerFix) {
//                     onTriggerFix(file.file, errorIndex);
//                 }
//             }
//         }, 800);
//     };

//     const handleCloseTerminal = () => {
//         setShowTerminal(false);
//         setTerminalContent([]);
//         setIsProcessing(false);
//     };

//     return (
//         <div
//             id={`file-card-${file.file.replace(/[^a-zA-Z0-9]/g, '-')}`}
//             className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 overflow-hidden hover:border-slate-600/50 transition-colors"
//         >
//             <div
//                 className="p-4 cursor-pointer hover:bg-slate-700/20 transition-colors"
//                 onClick={() => setIsExpanded(!isExpanded)}
//             >
//                 <div className="flex items-center justify-between">
//                     <div className="flex items-center space-x-3">
//                         <div className="flex items-center space-x-2">
//                             {file.errors.length > 0 ? (
//                                 isExpanded ? <ChevronDown className="h-4 w-4 text-gray-400" /> : <ChevronRight className="h-4 w-4 text-gray-400" />
//                             ) : (
//                                 <FileText className="h-4 w-4 text-gray-400" />
//                             )}
//                         </div>
//                         <div className="flex-1">
//                             <div className="flex items-center space-x-2 mb-1">
//                                 <h3 className="font-medium text-white text-sm">{file.file}</h3>
//                                 {file.pipeline_stage && (
//                                     <span className={`px-2 py-1 text-xs rounded-full ${getPipelineStageColor(file.pipeline_stage)}`}>
//                                         {file.pipeline_stage}
//                                     </span>
//                                 )}
//                             </div>
//                             <div className="flex items-center space-x-4 text-xs text-gray-400">
//                                 <div className="flex items-center space-x-1">
//                                     <Clock className="h-3 w-3" />
//                                     <span>Last checked: {new Date(file.last_checked).toLocaleString()}</span>
//                                 </div>
//                                 {file.build_status && (
//                                     <div className="flex items-center space-x-1">
//                                         <span>{getBuildStatusIcon(file.build_status)}</span>
//                                         <span className={getBuildStatusColor(file.build_status)}>
//                                             Build: {file.build_status}
//                                         </span>
//                                     </div>
//                                 )}
//                                 {file.uptime_percentage && (
//                                     <div className="flex items-center space-x-1">
//                                         <TrendingUp className="h-3 w-3" />
//                                         <span className={getUptimeColor(file.uptime_percentage)}>
//                                             {file.uptime_percentage}% uptime
//                                         </span>
//                                     </div>
//                                 )}
//                                 {file.last_fix_attempt && (
//                                     <div className="flex items-center space-x-1">
//                                         <Wrench className="h-3 w-3" />
//                                         <span>Last fix: {new Date(file.last_fix_attempt).toLocaleString()}</span>
//                                     </div>
//                                 )}
//                             </div>
//                         </div>
//                     </div>
//                     <StatusBadge
//                         status={file.status as "fixed" | "healthy" | "detected" | "warning" | "critical" | "fixing" | "unknown"}
//                         errorCount={file.error_count}
//                         criticalCount={file.critical_count}
//                     />
//                 </div>
//             </div>

//             {isExpanded && file.errors.length > 0 && (
//                 <div className="border-t border-slate-700/50 p-4 space-y-4 bg-slate-900/20">
//                     <div className="flex items-center justify-between text-sm">
//                         <span className="text-gray-300">
//                             {file.errors.length} issue{file.errors.length !== 1 ? 's' : ''} detected
//                         </span>

//                     </div>
//                     {file.errors.map((fix, index) => (
//                         <FixErrorCard
//                             key={index}
//                             fix={fix}
//                             fixIndex={index}
//                             onTriggerFix={handleTriggerFix}
//                         />
//                     ))}


//                 </div>
//             )}

//             {/* Terminal Section */}
//             {showTerminal && (
//                 <div className="border-t border-slate-700/50 p-4 bg-slate-900/30">
//                     <div className="bg-black rounded-lg border border-gray-600 overflow-hidden">
//                         {/* Terminal Header */}
//                         <div className="bg-gray-800 px-4 py-2 flex items-center justify-between border-b border-gray-600">
//                             <div className="flex items-center space-x-2">
//                                 <div className="w-3 h-3 bg-red-500 rounded-full"></div>
//                                 <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
//                                 <div className="w-3 h-3 bg-green-500 rounded-full"></div>
//                                 <span className="text-gray-300 text-sm ml-2">Git Push Terminal - {file.file}</span>
//                             </div>
//                             <button
//                                 onClick={handleCloseTerminal}
//                                 className="text-gray-400 hover:text-white transition-colors"
//                             >
//                                 <X className="h-4 w-4" />
//                             </button>
//                         </div>

//                         {/* Terminal Content */}
//                         <div className="p-4 h-64 overflow-y-auto font-mono text-sm">
//                             {terminalContent.length === 0 ? (
//                                 <div className="text-green-400">
//                                     $ Initializing Git push process...
//                                     <br />
//                                     <span className="animate-pulse">$ Preparing commit...</span>
//                                 </div>
//                             ) : (
//                                 <div className="space-y-1">
//                                     {terminalContent.map((line, index) => (
//                                         <div
//                                             key={index}
//                                             className={`${typeof line === 'string' && line.includes('✅') ? 'text-green-400 font-bold' :
//                                                     typeof line === 'string' && line.includes('🚀') ? 'text-blue-400 font-bold' :
//                                                         typeof line === 'string' && line.includes('📦') ? 'text-purple-400 font-bold' :
//                                                             typeof line === 'string' && line.includes('$') ? 'text-cyan-400' :
//                                                                 typeof line === 'string' && line.includes('To https://') ? 'text-yellow-400' :
//                                                                     typeof line === 'string' && line.includes('->') ? 'text-green-400' :
//                                                                         typeof line === 'string' && line.includes('remote:') ? 'text-blue-400' :
//                                                                             'text-gray-300'
//                                                 }`}
//                                         >
//                                             {line}
//                                         </div>

//                                     ))}
//                                     {isProcessing && (
//                                         <div className="text-cyan-400 animate-pulse">$ Processing...</div>
//                                     )}
//                                 </div>
//                             )}
//                         </div>
//                     </div>
//                 </div>
//             )}
//         </div>
//     );
// };

import React, { useState, useRef } from 'react';
import { ChevronDown, ChevronRight, FileText, Clock, TrendingUp, Wrench, X } from 'lucide-react';
import { FileStatusFix } from '../types/monitoring';
import { StatusBadge } from './StatusBadge';
import { FixErrorCard } from './FixErrorCard';
import { streamGithubPushLogs } from '../api/push';

interface FixFileCardProps {
    file: FileStatusFix;
    onTriggerFix?: (filePath: string, fixIndex: number) => void;
}

export const FixFileCard: React.FC<FixFileCardProps> = ({ file, onTriggerFix }) => {
    const [isExpanded, setIsExpanded] = useState(false);
    const [showTerminal, setShowTerminal] = useState(false);
    const [terminalContent, setTerminalContent] = useState<string[]>([]);
    const [isProcessing, setIsProcessing] = useState(false);
    
    const eventSourceRef = useRef<EventSource | null>(null);
    const terminalRef = useRef<HTMLDivElement>(null);

    const getUptimeColor = (uptime?: number) => {
        if (!uptime) return 'text-gray-400';
        if (uptime >= 99) return 'text-green-400';
        if (uptime >= 95) return 'text-yellow-400';
        return 'text-red-400';
    };

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
            case 'success': return '✅';
            case 'failed': return '❌';
            case 'running': return '🔄';
            case 'pending': return '⏳';
            default: return '❓';
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

    const getLogLineColor = (message: string): string => {
        if (message.includes('✅') || message.includes('🎉')) {
            return 'text-green-400 font-bold';
        }
        if (message.includes('🚀')) {
            return 'text-blue-400 font-bold';
        }
        if (message.includes('📦') || message.includes('💾') || message.includes('🔄')) {
            return 'text-purple-400 font-bold';
        }
        if (message.includes('❌')) {
            return 'text-red-400 font-bold';
        }
        if (message.includes('⚠️')) {
            return 'text-yellow-400 font-bold';
        }
        if (message.includes('🔧')) {
            return 'text-cyan-400';
        }
        if (message.includes('✍️')) {
            return 'text-green-300';
        }
        return 'text-gray-300';
    };

    const handleTriggerFix = (errorIndex: number) => {
        setShowTerminal(true);
        setIsProcessing(true);
        setTerminalContent([]);

        // Scroll to the file card
        setTimeout(() => {
            const element = document.getElementById(`file-card-${file.file.replace(/[^a-zA-Z0-9]/g, '-')}`);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }, 100);

        // Start streaming logs
        eventSourceRef.current = streamGithubPushLogs(
            (data: string) => {
                setTerminalContent(prev => [...prev, data]);
                
                // Auto-scroll to bottom
                setTimeout(() => {
                    if (terminalRef.current) {
                        terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
                    }
                }, 50);

                // Check if process completed
                if (data.includes('All logs updated successfully') || data.includes('GitHub push failed')) {
                    setIsProcessing(false);
                }
            },
            (error) => {
                console.error('Stream error:', error);
                // setTerminalContent(prev => [...prev, '❌ Connection error occurred']);
                setIsProcessing(false);
            }
        );

        // Call the original trigger fix if provided
        if (onTriggerFix) {
            onTriggerFix(file.file, errorIndex);
        }
    };

    const handleCloseTerminal = () => {
        // Close the event source
        if (eventSourceRef.current) {
            eventSourceRef.current.close();
            eventSourceRef.current = null;
        }
        
        setShowTerminal(false);
        setTerminalContent([]);
        setIsProcessing(false);
    };

    return (
        <div
            id={`file-card-${file.file.replace(/[^a-zA-Z0-9]/g, '-')}`}
            className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 overflow-hidden hover:border-slate-600/50 transition-colors"
        >
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
                                            Build: {file.build_status}
                                        </span>
                                    </div>
                                )}
                                {file.uptime_percentage && (
                                    <div className="flex items-center space-x-1">
                                        <TrendingUp className="h-3 w-3" />
                                        <span className={getUptimeColor(file.uptime_percentage)}>
                                            {file.uptime_percentage}% uptime
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
                    <StatusBadge
                        status={file.status as "fixed" | "healthy" | "detected" | "warning" | "critical" | "fixing" | "unknown"}
                        errorCount={file.error_count}
                        criticalCount={file.critical_count}
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
                    {file.errors.map((fix, index) => (
                        <FixErrorCard
                            key={index}
                            fix={fix}
                            fixIndex={index}
                            onTriggerFix={handleTriggerFix}
                        />
                    ))}
                </div>
            )}

            {/* Terminal Section with Live Streaming */}
            {showTerminal && (
                <div className="border-t border-slate-700/50 p-4 bg-slate-900/30">
                    <div className="bg-black rounded-lg border border-gray-600 overflow-hidden">
                        {/* Terminal Header */}
                        <div className="bg-gray-800 px-4 py-2 flex items-center justify-between border-b border-gray-600">
                            <div className="flex items-center space-x-2">
                                <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                                <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                                <span className="text-gray-300 text-sm ml-2">Git Push Terminal - {file.file}</span>
                                {isProcessing && (
                                    <div className="flex items-center space-x-1 ml-2">
                                        <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
                                        <span className="text-blue-400 text-xs">Live</span>
                                    </div>
                                )}
                            </div>
                            <button
                                onClick={handleCloseTerminal}
                                className="text-gray-400 hover:text-white transition-colors"
                            >
                                <X className="h-4 w-4" />
                            </button>
                        </div>

                        {/* Terminal Content */}
                        <div 
                            ref={terminalRef}
                            className="p-4 h-64 overflow-y-auto font-mono text-sm bg-black"
                        >
                            {terminalContent.length === 0 ? (
                                <div className="text-green-400">
                                    $ Connecting to Git push stream...
                                    <br />
                                    <span className="animate-pulse">$ Waiting for logs...</span>
                                </div>
                            ) : (
                                <div className="space-y-1">
                                    {terminalContent.map((line, index) => (
                                        <div
                                            key={index}
                                            className={getLogLineColor(line)}
                                        >
                                            {line}
                                        </div>
                                    ))}
                                    {isProcessing && (
                                        <div className="text-cyan-400 animate-pulse">$ Processing...</div>
                                    )}
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};