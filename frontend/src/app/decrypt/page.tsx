'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import Dropzone from '@/components/Dropzone';
import { api, DecryptResponse } from '@/lib/api';
import { Unlock, FileCode2, Copy, CheckCircle2 } from 'lucide-react';

export default function DecryptPage() {
  const [file, setFile] = useState<File | null>(null);
  const [key, setKey] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<DecryptResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  const handleDecrypt = async () => {
    if (!file || !key) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await api.decrypt(file, key);
      setResult(res);
    } catch (err: any) {
      setError(err.message || 'Decryption failed. Invalid key or image does not contain a payload.');
    } finally {
      setLoading(false);
    }
  };

  const copyPlaintext = () => {
    if (result?.plaintext) {
      navigator.clipboard.writeText(result.plaintext);
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
        <h1 className="text-4xl font-bold text-white">Decrypt Payload</h1>
        <p className="text-zinc-400">Extract and decrypt a hidden message using your AES-256 key.</p>
      </div>

      <div className="glass-card p-6 md:p-8 space-y-6">
        <div>
          <label className="block text-sm font-medium text-zinc-300 mb-2">1. Upload Stego Image</label>
          <Dropzone onFileSelect={setFile} selectedFile={file} accept="image/png" />
          <p className="text-xs text-zinc-500 mt-2">* Must be the exact PNG generated during encryption.</p>
        </div>

        <div>
          <label className="block text-sm font-medium text-zinc-300 mb-2">2. Decryption Key</label>
          <input
            type="text"
            value={key}
            onChange={(e) => setKey(e.target.value)}
            placeholder="Paste your base64 AES-256 key here..."
            className="w-full px-4 py-3 bg-zinc-900/50 border border-zinc-700 rounded-xl text-emerald-400 font-mono text-sm placeholder-zinc-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
          />
        </div>

        {error && (
          <div className="p-4 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm">
            {error}
          </div>
        )}

        <button
          onClick={handleDecrypt}
          disabled={!file || !key || loading}
          className="w-full py-4 rounded-xl font-bold text-white bg-blue-600 hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center space-x-2"
        >
          {loading ? (
            <div className="w-6 h-6 border-2 border-white/20 border-t-white rounded-full animate-spin" />
          ) : (
            <>
              <Unlock className="w-5 h-5" />
              <span>Extract & Decrypt</span>
            </>
          )}
        </button>
      </div>

      {result && (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="glass-card p-6 md:p-8 space-y-4 border-blue-500/30"
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3 text-blue-400">
              <FileCode2 className="w-6 h-6" />
              <h2 className="text-xl font-bold">Decrypted Message</h2>
            </div>
            <button
              onClick={copyPlaintext}
              className="flex items-center space-x-2 text-sm text-zinc-400 hover:text-white transition-colors"
            >
              {copied ? <CheckCircle2 className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
              <span>{copied ? 'Copied' : 'Copy'}</span>
            </button>
          </div>
          
          <div className="p-4 rounded-xl bg-black/40 border border-white/5 whitespace-pre-wrap text-zinc-300 font-mono text-sm">
            {result.plaintext}
          </div>
        </motion.div>
      )}
    </motion.div>
  );
}
