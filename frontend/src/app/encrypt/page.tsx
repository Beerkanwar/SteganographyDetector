'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import Dropzone from '@/components/Dropzone';
import { api, EncryptResponse } from '@/lib/api';
import { Lock, Download, Copy, CheckCircle2 } from 'lucide-react';

export default function EncryptPage() {
  const [file, setFile] = useState<File | null>(null);
  const [plaintext, setPlaintext] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<EncryptResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  const handleEncrypt = async () => {
    if (!file || !plaintext) return;
    setLoading(true);
    setError(null);
    try {
      const res = await api.encrypt(file, plaintext);
      setResult(res);
    } catch (err: any) {
      setError(err.message || 'Encryption failed');
    } finally {
      setLoading(false);
    }
  };

  const copyKey = () => {
    if (result?.key) {
      navigator.clipboard.writeText(result.key);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-3xl mx-auto space-y-8"
    >
      <div className="text-center space-y-2">
        <h1 className="text-4xl font-bold text-white">Encrypt & Hide</h1>
        <p className="text-zinc-400">Securely embed your secret message into an image.</p>
      </div>

      <div className="glass-card p-6 md:p-8 space-y-6">
        <div>
          <label className="block text-sm font-medium text-zinc-300 mb-2">1. Select Carrier Image</label>
          <Dropzone onFileSelect={setFile} selectedFile={file} />
        </div>

        <div>
          <label className="block text-sm font-medium text-zinc-300 mb-2">2. Secret Message</label>
          <textarea
            value={plaintext}
            onChange={(e) => setPlaintext(e.target.value)}
            placeholder="Enter the secret message to hide..."
            className="w-full h-32 px-4 py-3 bg-zinc-900/50 border border-zinc-700 rounded-xl text-white placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all resize-none"
          />
        </div>

        {error && (
          <div className="p-4 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm">
            {error}
          </div>
        )}

        <button
          onClick={handleEncrypt}
          disabled={!file || !plaintext || loading}
          className="w-full py-4 rounded-xl font-bold text-white bg-blue-600 hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center space-x-2"
        >
          {loading ? (
            <div className="w-6 h-6 border-2 border-white/20 border-t-white rounded-full animate-spin" />
          ) : (
            <>
              <Lock className="w-5 h-5" />
              <span>Encrypt & Embed Payload</span>
            </>
          )}
        </button>
      </div>

      {result && (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="glass-card p-6 md:p-8 space-y-6 border-emerald-500/30"
        >
          <div className="flex items-center space-x-3 text-emerald-400">
            <CheckCircle2 className="w-6 h-6" />
            <h2 className="text-xl font-bold">Successfully Embedded</h2>
          </div>

          <div className="grid grid-cols-2 gap-4 text-sm">
            <div className="p-4 rounded-lg bg-black/20">
              <p className="text-zinc-500 mb-1">Payload Size</p>
              <p className="font-mono text-white">{result.payload_size_bytes} Bytes</p>
            </div>
            <div className="p-4 rounded-lg bg-black/20">
              <p className="text-zinc-500 mb-1">Capacity Used</p>
              <p className="font-mono text-white">{result.utilization_percent.toFixed(2)}%</p>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-zinc-400 mb-2">Decryption Key (AES-256)</label>
            <div className="flex space-x-2">
              <input
                readOnly
                value={result.key}
                className="flex-1 px-4 py-3 bg-black/30 border border-zinc-700 rounded-lg text-emerald-400 font-mono text-sm focus:outline-none"
              />
              <button
                onClick={copyKey}
                className="px-4 py-2 bg-zinc-800 hover:bg-zinc-700 rounded-lg transition-colors flex items-center justify-center"
              >
                {copied ? <CheckCircle2 className="w-5 h-5 text-emerald-400" /> : <Copy className="w-5 h-5 text-zinc-300" />}
              </button>
            </div>
            <p className="text-xs text-red-400 mt-2 font-medium">⚠️ Save this key! It is not stored anywhere and cannot be recovered.</p>
          </div>

          <a
            href={`data:image/png;base64,${result.stego_image}`}
            download={`stego_${file?.name || 'image.png'}`}
            className="w-full py-4 rounded-xl font-bold text-white bg-zinc-800 hover:bg-zinc-700 transition-all flex items-center justify-center space-x-2"
          >
            <Download className="w-5 h-5" />
            <span>Download Stego Image</span>
          </a>
        </motion.div>
      )}
    </motion.div>
  );
}
