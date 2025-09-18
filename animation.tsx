import React from 'react';

interface AnimationProps {
  width?: number;
  height?: number;
}

const Animation: React.FC<AnimationProps> = ({ width = 1280, height = 720 }) => {
  return (
    <div 
      style={{
        width: `${width}px`,
        height: `${height}px`,
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* Animated background elements */}
      <div
        style={{
          position: 'absolute',
          width: '100%',
          height: '100%',
          background: 'radial-gradient(circle at 30% 30%, rgba(255,255,255,0.1) 0%, transparent 50%)',
          animation: 'pulse 3s ease-in-out infinite',
        }}
      />
      
      {/* Floating particles */}
      {[...Array(10)].map((_, i) => (
        <div
          key={i}
          style={{
            position: 'absolute',
            width: `${Math.random() * 20 + 10}px`,
            height: `${Math.random() * 20 + 10}px`,
            background: 'rgba(255,255,255,0.3)',
            borderRadius: '50%',
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 100}%`,
            animation: `float ${3 + Math.random() * 4}s ease-in-out infinite`,
            animationDelay: `${Math.random() * 2}s`,
          }}
        />
      ))}
      
      {/* Central title area */}
      <div
        style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          textAlign: 'center',
          color: 'white',
          fontFamily: 'Arial, sans-serif',
        }}
      >
        <h1 style={{ fontSize: '48px', margin: '0', textShadow: '2px 2px 4px rgba(0,0,0,0.5)' }}>
          HK Rainfall Visualiser
        </h1>
        <p style={{ fontSize: '24px', margin: '20px 0', textShadow: '1px 1px 2px rgba(0,0,0,0.5)' }}>
          Beautiful Weather Data
        </p>
      </div>
      
      <style jsx>{`
        @keyframes pulse {
          0%, 100% { opacity: 0.3; }
          50% { opacity: 0.7; }
        }
        
        @keyframes float {
          0%, 100% { transform: translateY(0px) rotate(0deg); }
          50% { transform: translateY(-20px) rotate(180deg); }
        }
      `}</style>
    </div>
  );
};

export default Animation;