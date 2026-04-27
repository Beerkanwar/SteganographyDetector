'use client';

import { motion } from 'framer-motion';
import { Database, ShieldAlert, Cpu } from 'lucide-react';

export default function DocsPage() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-4xl mx-auto space-y-12"
    >
      <div className="text-center space-y-4">
        <h1 className="text-4xl md:text-5xl font-bold text-white">How It Works</h1>
        <p className="text-zinc-400 max-w-2xl mx-auto text-lg">
          The technical architecture behind SteganoVault's encryption and detection engines.
        </p>
      </div>

      <div className="space-y-8">
        <section className="glass-card p-8 flex flex-col md:flex-row gap-8 items-start">
          <div className="p-4 rounded-2xl bg-blue-500/10 shrink-0">
            <ShieldAlert className="w-10 h-10 text-blue-400" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-white mb-3">1. Authenticated Encryption (AES-GCM)</h2>
            <p className="text-zinc-400 leading-relaxed mb-4">
              Before any data touches the image, the plaintext is compressed using <code className="text-blue-300">zlib</code> and then encrypted using <code className="text-blue-300">AES-256-GCM</code>. 
              This is an authenticated encryption mode. It not only ensures confidentiality but provides an authentication tag. 
              If the image is manipulated (e.g., compressed or resized), the decryption will explicitly fail rather than returning garbage data.
            </p>
          </div>
        </section>

        <section className="glass-card p-8 flex flex-col md:flex-row gap-8 items-start">
          <div className="p-4 rounded-2xl bg-emerald-500/10 shrink-0">
            <Database className="w-10 h-10 text-emerald-400" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-white mb-3">2. LSB Steganography Engine</h2>
            <p className="text-zinc-400 leading-relaxed mb-4">
              We use <code className="text-emerald-300">numpy</code> for ultra-fast bitwise manipulation. The system calculates the exact payload capacity of the carrier image. 
              It then prepends a 4-byte size header to the encrypted payload, converts it to a bit array, and overwrites the Least Significant Bit (LSB) of each pixel channel.
              Because the payload is encrypted (and therefore looks like high-entropy random noise), standard statistical histogram attacks are less effective.
            </p>
          </div>
        </section>

        <section className="glass-card p-8 flex flex-col md:flex-row gap-8 items-start">
          <div className="p-4 rounded-2xl bg-purple-500/10 shrink-0">
            <Cpu className="w-10 h-10 text-purple-400" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-white mb-3">3. Deep Learning Steganalysis</h2>
            <p className="text-zinc-400 leading-relaxed">
              To detect hidden payloads, we trained an <code className="text-purple-300">EfficientNetV2</code> neural network on the COCO 2017 dataset.
              The model does not look for shapes; it looks for high-frequency noise patterns introduced by LSB embedding.
              During training, clean images are dynamically injected with random payloads to force the network to learn the fundamental signature of steganography rather than dataset bias.
            </p>
          </div>
        </section>
      </div>
    </motion.div>
  );
}
