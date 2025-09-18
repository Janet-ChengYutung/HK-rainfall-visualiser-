import React from 'react';

const RainArt: React.FC = () => {
  return (
    <div style={{padding:20}}>
      <h2>RainArt placeholder</h2>
      <p>If you see this, the component compiled successfully.</p>
    </div>
  );
};

export default RainArt;
// Created by 21st.dev
import React, { useState, useEffect } from 'react';

const RainArt: React.FC = () => {
  const [frame, setFrame] = useState(0);

  // Hong Kong rain data (15.2,8.7,45.3,78.9,156.4,234.7,298.5,267.3,189.6,67.8,23.4,12.1)
  const rainData = [15.2, 8.7, 45.3, 78.9, 156.4, 234.7, 298.5, 267.3, 189.6, 67.8, 23.4, 12.1];

  useEffect(() => {
    const interval = setInterval(() => {
      setFrame(prev => prev + 1);
    }, 30);
    return () => clearInterval(interval);
  }, []);

  const generateFluidPattern = (data: number[], time: number) => {
    const maxVal = Math.max(...data);
    const grid: string[] = [];
    
    for (let y = 0; y < 40; y++) {
      let row = '';
      for (let x = 0; x < 120; x++) {
        import React from 'react';

        const RainArt: React.FC = () => {
          return (
            <div style={{padding:20}}>
              <h2>RainArt placeholder</h2>
              <p>If you see this, the component compiled successfully.</p>
            </div>
          );
        };

        export default RainArt;
    const bgTime = frame * 0.02;
    const bgGrid = [];
    for (let y = 0; y < 60; y++) {
      let row = '';
      for (let x = 0; x < 200; x++) {
        const wave = Math.sin(x * 0.05 + y * 0.03 + bgTime) * Math.cos(x * 0.03 + y * 0.07 - bgTime * 0.5);
        const intensity = (wave + 1) / 2;
        if (intensity > 0.7) row += '∘';
        else if (intensity > 0.5) row += '·';
        else row += ' ';
      }
      bgGrid.push(row);
    }
    return bgGrid;
  };

  const bgPattern = backgroundPattern();

  return (
    <div className="min-h-screen relative overflow-hidden flex items-center justify-center p-4">
      <div 
        className="absolute inset-0 opacity-10 text-blue-300/20 font-mono text-xs leading-none whitespace-pre select-none pointer-events-none"
        style={{ transform: `translate(${-frame * 0.5}px, ${-frame * 0.2}px)` }}
      >
        {bgPattern.map((line, i) => (
          <div key={i}>{line}</div>
        ))}
      </div>
      <div className="absolute inset-0 bg-gradient-to-br from-blue-950 via-blue-800 to-cyan-400"></div>
      <div className="relative z-10">
        <div className="absolute inset-0 bg-cyan-400/10 blur-3xl rounded-full"></div>
        <div className="relative bg-blue-900/50 backdrop-blur-sm border border-cyan-400/20 rounded-2xl p-8 overflow-hidden">
          <div className="font-mono text-xs leading-none whitespace-pre select-none">
            {pattern.map((line, i) => (
              <div 
                key={i} 
                className="transition-all duration-75"
                style={{
                  background: `linear-gradient(90deg, 
                    rgba(30, 58, 138, ${0.1 + (i / 40) * 0.3}) 0%, 
                    rgba(59, 130, 246, ${0.2 + (i / 40) * 0.2}) 50%, 
                    rgba(34, 211, 238, ${0.1 + (i / 40) * 0.3}) 100%)`,
                  color: i < 3 ? '#ffffff' : 
                         i < 6 ? '#e0e7ff' : 
                         i < 10 ? '#c7d2fe' :
                         i < 15 ? '#a5b4fc' :
                         i < 20 ? '#818cf8' :
                         i < 25 ? '#6366f1' :
                         i < 30 ? '#4f46e5' :
                         i < 35 ? '#3b82f6' : '#22d3ee'
                }}
              >
                {line}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default RainArt;
