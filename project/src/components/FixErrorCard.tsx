import React from 'react';
import { AlertTriangle, Clock, Brain, Wrench, CheckCircle, GitBranch, Hash } from 'lucide-react';
import { FixEntry } from '../types/monitoring';

interface FixErrorCardProps {
    fix: FixEntry;
    onTriggerFix?: (fixIndex: number) => void;
    fixIndex: number;
}

export const FixErrorCard: React.FC<FixErrorCardProps> = ({ fix, onTriggerFix, fixIndex }) => {
    const getSeverityColor = (severity: string) => {
        switch (severity) {
            case 'critical': return 'border-red-500/50 bg-red-500/10';
            case 'high': return 'border-orange-500/50 bg-orange-500/10';
            case 'medium': return 'border-yellow-500/50 bg-yellow-500/10';
            case 'low':
            default:
                return 'border-blue-500/50 bg-blue-500/10';
        }
    };

    const getTypeIcon = (type: string) => {
        switch (type) {
            case 'DOCKERFILE': return '🐳';
            case 'NETWORK': return '🌐';
            case 'BUILD': return '🔨';
            case 'DEPLOYMENT': return '🚀';
            case 'SECURITY': return '🔒';
            case 'PERFORMANCE': return '⚡';
            case 'CONFIG': return '⚙️';
            case 'TEST': return '🧪';
            default: return '📄';
        }
    };

    const getSeverityBadge = (severity: string) => {
        const colors = {
            critical: 'bg-red-500/20 text-red-300 border-red-500/30',
            high: 'bg-orange-500/20 text-orange-300 border-orange-500/30',
            medium: 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30',
            low: 'bg-blue-500/20 text-blue-300 border-blue-500/30'
        };
        return colors[severity as keyof typeof colors] || colors.low;
    };


    return (
        <div className={`rounded-lg border p-4 ${getSeverityColor(fix.status)}`}>
            <div className="flex items-start justify-between mb-3">
                <div className="flex items-center space-x-3">
                    <span className="text-lg">{getTypeIcon(fix.error_type)}</span>
                    <div>
                        <div className="flex items-center space-x-2">
                            <span className="font-medium text-white">{fix.error_type} Error</span>
                            <span
                                className={`px-2 py-1 text-xs rounded-full border ${getSeverityBadge(
                                    fix.ai_analysis?.[0]?.risk_level || 'low'
                                )}`}
                            >
                                {fix.ai_analysis?.[0]?.risk_level || 'Unknown'}
                            </span>
                            <span
                                className={`px-2 py-1 text-xs rounded-full border ${getSeverityBadge("medium")}`}
                            >
                                {fix.fix_id}
                            </span>

                            <span
                                className={`px-2 py-1 text-xs rounded-full border ${getSeverityBadge("high")}`}
                            >
                                {fix.solution_id}
                            </span>
                            <span
                               className={`px-2 py-1 text-xs rounded-full border ${getSeverityBadge("medium")}`}
                            >
                                {fix.err_id}
                            </span>
                        </div>
                        <div className="flex items-center space-x-3 mt-1">
                            {fix.commit_hash && (
                                <div className="flex items-center space-x-1 text-xs text-gray-400">
                                    <Hash className="h-3 w-3" />
                                    <span>{fix.commit_hash}</span>
                                </div>
                            )}
                            {fix.branch && (
                                <div className="flex items-center space-x-1 text-xs text-gray-400">
                                    <GitBranch className="h-3 w-3" />
                                    <span>{fix.branch}</span>
                                </div>
                            )}
                        </div>
                    </div>
                </div>

                <div className="flex items-center space-x-2">
                    <div className="flex items-center space-x-1 text-xs text-gray-400">
                        <Clock className="h-3 w-3" />
                        <span>{new Date(fix.timestamp).toLocaleTimeString()}</span>
                    </div>

                    {fix.auto_fixable && onTriggerFix ? (
                        <button
                            onClick={() => onTriggerFix(fixIndex)}
                            className="flex items-center space-x-1 px-2 py-1 bg-green-600 hover:bg-green-700 text-white text-xs rounded transition-colors"
                        >
                            <GitBranch className="h-3 w-3" />
                            <span>Push to GitHub</span>
                        </button>
                    ) : null}
                </div>
            </div>

            <div className="space-y-3">
                <div>
                    <div className="flex items-center space-x-2 mb-2">
                        <AlertTriangle className="h-4 w-4 text-red-400" />
                        <span className="text-sm font-medium text-gray-300">Error Details</span>
                    </div>
                    <div className="bg-slate-900/60 rounded p-3 font-mono text-sm text-red-300 border border-red-500/20">
                        {Array.isArray(fix.ai_analysis) && fix.ai_analysis[0]?.related_error
                            ? fix.ai_analysis[0].related_error
                            : fix.err_id}
                    </div>
                </div>

                {fix.ai_analysis && fix.ai_analysis.length > 0 && (

                    <div>
                        <div className="flex items-center space-x-2 mb-2">
                            <Brain className="h-4 w-4 text-purple-400" />
                            <span className="text-sm font-medium text-gray-300">AI Analysis</span>
                        </div>

                        {Array.isArray(fix.ai_analysis) && fix.ai_analysis.length > 0 && (
                            <div className="space-y-3">
                                {fix.ai_analysis.map((a, i) => (
                                    <div key={i} className="bg-gray-800/50 border border-gray-700 rounded-lg p-4 space-y-3">
                                        {/* Header with Decision and Risk Level */}
                                        <div className="flex items-center justify-between">
                                            <div className="flex items-center space-x-2">
                                                <span className="text-sm font-medium text-gray-300">Decision:</span>
                                                <span className="text-sm font-semibold text-white">{a.decision}</span>
                                            </div>
                                            <div className={`px-2 py-1 rounded text-xs font-medium ${a.risk_level === 'Low' ? 'bg-green-500/20 text-green-400' :
                                                    a.risk_level === 'Medium' ? 'bg-yellow-500/20 text-yellow-400' :
                                                        a.risk_level === 'High' ? 'bg-red-500/20 text-red-400' :
                                                            'bg-gray-500/20 text-gray-400'
                                                }`}>
                                                {a.risk_level} Risk
                                            </div>
                                        </div>

                                        {/* Confidence */}
                                        <div className="flex items-center space-x-2">
                                            <span className="text-sm font-medium text-gray-300">Confidence:</span>
                                            <span className={`text-sm font-semibold ${a.confidence >= 80 ? 'text-green-400' :
                                                    a.confidence >= 60 ? 'text-yellow-400' :
                                                        'text-red-400'
                                                }`}>
                                                {a.confidence}%
                                            </span>
                                        </div>

                                        {/* Reasoning */}
                                        <div className="space-y-1">
                                            <span className="text-sm font-medium text-gray-300">Reasoning:</span>
                                            <p className="text-sm text-gray-400 bg-gray-900/50 p-2 rounded border-l-2 border-blue-500/50">
                                                {a.reasoning}
                                            </p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                )}

                {fix.recommendations && (
                    <div>
                        <div className="flex items-center space-x-2 mb-2">
                            <Wrench className="h-4 w-4 text-green-400" />
                            <span className="text-sm font-medium text-gray-300">Recommended Fix</span>
                        </div>
                        <div className="bg-green-500/10 border border-green-500/20 rounded p-3 text-sm text-green-200">
                            {fix.recommendations}
                        </div>
                    </div>
                )}

                {fix.fix_applied && fix.applied_at && (
                    <div className="bg-emerald-500/10 border border-emerald-500/20 rounded p-2 text-xs text-emerald-300">
                        ✅ Fix applied automatically at {new Date(fix.applied_at).toLocaleString()}
                    </div>
                )}
            </div>
        </div>
    );
};
