'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Shield, Lock, Unlock, Eye, FileText } from 'lucide-react';
import { motion } from 'framer-motion';

const navItems = [
  { path: '/encrypt', label: 'Encrypt', icon: Lock },
  { path: '/decrypt', label: 'Decrypt', icon: Unlock },
  { path: '/detect', label: 'Detect', icon: Eye },
  { path: '/docs', label: 'Docs', icon: FileText },
];

export default function Navbar() {
  const pathname = usePathname();

  return (
    <nav className="fixed top-0 w-full z-50 glass border-b border-white/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="flex items-center space-x-2 text-white hover:text-blue-400 transition-colors">
            <Shield className="w-8 h-8 text-blue-500" />
            <span className="font-bold text-xl tracking-tight">SteganoVault</span>
          </Link>
          
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-4">
              {navItems.map((item) => {
                const isActive = pathname === item.path;
                const Icon = item.icon;
                
                return (
                  <Link
                    key={item.path}
                    href={item.path}
                    className={`relative px-4 py-2 rounded-md text-sm font-medium transition-colors flex items-center space-x-2
                      ${isActive ? 'text-white' : 'text-zinc-400 hover:text-white hover:bg-white/5'}`}
                  >
                    <Icon className="w-4 h-4" />
                    <span>{item.label}</span>
                    {isActive && (
                      <motion.div
                        layoutId="navbar-active"
                        className="absolute inset-0 bg-white/10 rounded-md -z-10"
                        transition={{ type: "spring", stiffness: 380, damping: 30 }}
                      />
                    )}
                  </Link>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}
