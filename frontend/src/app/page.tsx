'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import { Shield, Lock, Eye } from 'lucide-react';

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] text-center space-y-12">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7 }}
        className="max-w-3xl space-y-6"
      >
        <div className="flex justify-center mb-6">
          <div className="p-4 rounded-2xl bg-blue-500/10 border border-blue-500/20">
            <Shield className="w-16 h-16 text-blue-500" />
          </div>
        </div>
        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white to-zinc-400">
          Invisibly Secure.
        </h1>
        <p className="text-xl text-zinc-400 max-w-2xl mx-auto leading-relaxed">
          Hide military-grade AES-256 encrypted messages inside ordinary images. 
          Analyze suspicious images using our advanced Deep Learning steganalysis engine.
        </p>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7, delay: 0.2 }}
        className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-4xl"
      >
        <Link href="/encrypt">
          <div className="glass-card p-8 hover:bg-white/5 transition-colors group cursor-pointer h-full flex flex-col items-center text-center">
            <Lock className="w-12 h-12 text-blue-400 mb-4 group-hover:scale-110 transition-transform" />
            <h3 className="text-2xl font-bold text-white mb-2">Encrypt & Hide</h3>
            <p className="text-zinc-400">Embed a secret payload securely into any PNG or JPG using LSB matching and AES-GCM.</p>
          </div>
        </Link>
        
        <Link href="/detect">
          <div className="glass-card p-8 hover:bg-white/5 transition-colors group cursor-pointer h-full flex flex-col items-center text-center">
            <Eye className="w-12 h-12 text-emerald-400 mb-4 group-hover:scale-110 transition-transform" />
            <h3 className="text-2xl font-bold text-white mb-2">Detect Payloads</h3>
            <p className="text-zinc-400">Run images through an EfficientNetV2 neural network trained on the COCO dataset to detect hidden data.</p>
          </div>
        </Link>
      </motion.div>
    </div>
  );
}
