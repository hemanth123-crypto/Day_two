import { BookOpen, Brain, Compass, History, Home, ShieldCheck, Sparkles } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';

export default function Navbar() {
  const location = useLocation();

  const navItems = [
    { name: 'Home', path: '/', icon: Home },
    { name: 'Discover', path: '/results', icon: Sparkles },
    { name: 'Skill Gap', path: '/skills', icon: Brain },
    { name: 'Learning Path', path: '/learning-path', icon: Compass },
    { name: 'Evaluation', path: '/evaluation', icon: ShieldCheck },
    { name: 'Courses', path: '/explorer', icon: BookOpen },
    { name: 'Dashboard', path: '/dashboard', icon: History },
  ];

  return (
    <nav className="sticky top-0 z-50 border-b border-white/10 bg-slate-950/80 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-3.5">
        <Link to="/" className="flex items-center gap-3 group">
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-to-tr from-cyan-500 to-violet-600 shadow-[0_0_20px_rgba(34,211,238,0.4)] transition group-hover:scale-105">
            <Sparkles size={20} className="text-white" />
          </div>
          <div>
            <span className="text-xs font-bold uppercase tracking-widest text-cyan-400">Coursera Intelligence</span>
            <h1 className="text-lg font-black tracking-tight text-white">Course Finder</h1>
          </div>
        </Link>

        <div className="hidden md:flex items-center gap-1 rounded-full border border-slate-800 bg-slate-900/60 p-1.5 shadow-inner">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-2 rounded-full px-4 py-1.5 text-xs font-medium transition ${
                  isActive
                    ? 'bg-gradient-to-r from-cyan-500/20 to-violet-500/20 text-cyan-200 border border-cyan-400/30 shadow-[0_0_12px_rgba(34,211,238,0.2)]'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                }`}
              >
                <Icon size={14} />
                {item.name}
              </Link>
            );
          })}
        </div>

        <div className="flex items-center gap-3">
          <span className="hidden sm:inline-flex items-center gap-1.5 rounded-full border border-emerald-500/30 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-300">
            <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" />
            FAISS + AI Active
          </span>
        </div>
      </div>
    </nav>
  );
}
