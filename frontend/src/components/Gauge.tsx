'use client';

import { motion } from 'framer-motion';

interface GaugeProps {
  value: number; // 0 to 100
  label: string;
}

export default function Gauge({ value, label }: GaugeProps) {
  // Determine color based on risk (0=clean/green, 100=stego/red)
  const isDanger = value > 50;
  const colorClass = isDanger ? 'text-red-500' : 'text-emerald-500';
  const strokeClass = isDanger ? 'stroke-red-500' : 'stroke-emerald-500';
  const bgClass = isDanger ? 'bg-red-500/10' : 'bg-emerald-500/10';

  const circumference = 2 * Math.PI * 45; // radius 45
  const strokeDashoffset = circumference - (value / 100) * circumference;

  return (
    <div className="flex flex-col items-center justify-center p-6 glass-card">
      <div className="relative w-48 h-48 flex items-center justify-center">
        {/* Background Circle */}
        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
          <circle
            cx="50"
            cy="50"
            r="45"
            fill="none"
            stroke="currentColor"
            strokeWidth="8"
            className="text-zinc-800"
          />
          {/* Animated Progress Circle */}
          <motion.circle
            cx="50"
            cy="50"
            r="45"
            fill="none"
            strokeWidth="8"
            strokeLinecap="round"
            className={strokeClass}
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset }}
            transition={{ duration: 1.5, ease: "easeOut" }}
          />
        </svg>
        
        {/* Center Text */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <motion.span 
            initial={{ opacity: 0, scale: 0.5 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.5 }}
            className={`text-4xl font-bold ${colorClass}`}
          >
            {value.toFixed(1)}%
          </motion.span>
          <span className="text-xs text-zinc-400 mt-1 uppercase tracking-wider">Confidence</span>
        </div>
      </div>
      
      <div className={`mt-6 px-4 py-2 rounded-full ${bgClass} border border-white/5`}>
        <span className={`text-sm font-semibold uppercase tracking-wider ${colorClass}`}>
          {label === 'stego' ? 'Payload Detected' : 'Clean Image'}
        </span>
      </div>
    </div>
  );
}
