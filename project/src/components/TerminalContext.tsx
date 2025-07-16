import React, { createContext, useContext, useRef, useState, useEffect } from 'react';

interface TerminalContextType {
  isOpen: boolean;
  logs: string[];
  openTerminal: () => void;
  closeTerminal: () => void;
  clearTerminal: () => void;
  appendLog: (line: string) => void;
}

const TerminalContext = createContext<TerminalContextType | undefined>(undefined);

export const TerminalProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [logs, setLogs] = useState<string[]>([]);
  const streamRef = useRef<EventSource | null>(null);

  const openTerminal = () => {
    setIsOpen(true);
  };

  const closeTerminal = () => {
    setIsOpen(false);
    if (streamRef.current) {
      streamRef.current.close();
      streamRef.current = null;
    }
  };

  const clearTerminal = () => {
    setLogs([]);
  };

  const appendLog = (line: string) => {
    setLogs((prev) => [...prev, line]);
  };

  useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current.close();
        streamRef.current = null;
      }
    };
  }, []);

  return (
    <TerminalContext.Provider
      value={{ isOpen, logs, openTerminal, closeTerminal, clearTerminal, appendLog }}
    >
      {children}
    </TerminalContext.Provider>
  );
};

export const useTerminal = (): TerminalContextType => {
  const context = useContext(TerminalContext);
  if (!context) throw new Error('useTerminal must be used within a TerminalProvider');
  return context;
};
