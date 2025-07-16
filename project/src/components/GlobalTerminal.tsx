import React, { useEffect, useRef } from 'react';
import { useTerminal } from '../components/TerminalContext';

export const GlobalTerminal: React.FC = () => {
  const { logs, isOpen } = useTerminal();
  const scrollRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  if (!isOpen) return null;

  return (
    <div className="bg-black rounded-lg border border-gray-600 overflow-hidden resize-y min-h-[200px] max-h-[80vh]">
      <div className="bg-gray-800 px-4 py-2 flex items-center border-b border-gray-600">
        <span className="text-gray-300 text-sm">CI/CD Monitor Terminal</span>
      </div>
      <div
        ref={scrollRef}
        className="p-4 font-mono text-sm overflow-y-auto"
        style={{ height: 'calc(100% - 40px)' }}
      >
        {logs.length === 0 ? (
          <div className="text-green-400">
            $ Waiting for log entries...
          </div>
        ) : (
          <div className="space-y-1">
            {logs.map((line, index) => (
              <div key={index} className="text-gray-300">
                {line}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
