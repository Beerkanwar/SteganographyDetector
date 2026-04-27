'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import Dropzone from '@/components/Dropzone';
import Gauge from '@/components/Gauge';
import { api, DetectResponse } from '@/lib/api';
import { Search } from 'lucide-react';

export default function DetectPage() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<DetectResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleDetect = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await api.detect(file);
      setResult(res);
    } catch (err: any) {
      setError(err.message || 'Detection failed. Ensure the ML model is trained and active.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-3xl mx-auto space-y-8"
    >
      <div className="text-center space-y-2">
        <h1 className="text-4xl font-bold text-white">Steganalysis Detection</h1>
        <p className="text-zinc-400">Analyze an image using our Deep Learning model to find hidden payloads.</p>
      </div>

      <div className="glass-card p-6 md:p-8 space-y-6">
        <div>
          <label className="block text-sm font-medium text-zinc-300 mb-2">Upload Suspicious Image</label>
          <Dropzone onFileSelect={(f) => { setFile(f); setResult(null); }} selectedFile={file} />
        </div>

        {error && (
          <div className="p-4 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm">
            {error}
          </div>
        )}

        <button
          onClick={handleDetect}
          disabled={!file || loading}
          className="w-full py-4 rounded-xl font-bold text-white bg-blue-600 hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center space-x-2"
        >
          {loading ? (
            <div className="w-6 h-6 border-2 border-white/20 border-t-white rounded-full animate-spin" />
          ) : (
            <>
              <Search className="w-5 h-5" />
              <span>Analyze Image</span>
            </>
          )}
        </button>
      </div>

      {result && (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="flex justify-center"
        >
          <Gauge value={result.label === 'stego' ? result.confidence : 100 - result.confidence} label={result.label} />
        </motion.div>
      )}
    </motion.div>
  );
}
