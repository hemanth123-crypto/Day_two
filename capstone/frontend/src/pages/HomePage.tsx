import { ArrowRight, BookOpen, Brain, CheckCircle2, ChevronRight, Compass, Database, Layers, ShieldCheck, Sparkles, Terminal } from 'lucide-react';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import SearchForm from '../components/SearchForm';

const sampleQueries = [
  {
    title: 'Data Science Foundations',
    query: 'I want to learn data science from the basics. Which courses should I start with?',
    tag: 'Beginner',
  },
  {
    title: 'Python to Machine Learning',
    query: 'I know Python and SQL. What courses should I take next to move into machine learning?',
    tag: 'Career Move',
  },
  {
    title: 'Cloud Prerequisite Path',
    query: 'I want to learn cloud computing but I do not know which prerequisite courses I need.',
    tag: 'Prerequisites',
  },
  {
    title: 'Data Analytics Progression',
    query: 'Can you suggest a learning path from beginner to advanced data analytics?',
    tag: 'Roadmap',
  },
  {
    title: 'Java to Software Engineer',
    query: 'I know Java and want to become a software developer.',
    tag: 'Development',
  },
  {
    title: 'Statistics Gap for Data Science',
    query: 'I know Python but I am weak in statistics. I want to become a data scientist.',
    tag: 'Skill Gap',
  },
];

export default function HomePage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const handleSearch = (query: string) => {
    setLoading(true);
    navigate('/results', { state: { query } });
  };

  return (
    <div className="relative min-h-[calc(100vh-65px)] overflow-hidden px-6 py-10 md:px-12 text-slate-100">
      {/* Background ambient lighting */}
      <div className="pointer-events-none absolute inset-0 overflow-hidden">
        <div className="absolute -left-20 top-10 h-96 w-96 rounded-full bg-cyan-500/15 blur-[120px]" />
        <div className="absolute right-4 top-16 h-96 w-96 rounded-full bg-violet-600/15 blur-[130px]" />
        <div className="absolute bottom-10 left-1/3 h-80 w-80 rounded-full bg-sky-500/10 blur-[100px]" />
      </div>

      <div className="relative mx-auto max-w-6xl space-y-12">
        {/* Hero Section */}
        <div className="text-center max-w-3xl mx-auto space-y-4">
          <div className="inline-flex items-center gap-2 rounded-full border border-cyan-400/30 bg-cyan-500/10 px-4 py-1.5 text-xs font-semibold text-cyan-200 shadow-[0_0_24px_rgba(34,211,238,0.25)] backdrop-blur-md">
            <Sparkles size={14} className="text-cyan-300 animate-spin" />
            AI-Powered Semantic Course Discovery
          </div>

          <h1 className="text-4xl sm:text-6xl font-black tracking-tight text-white leading-tight">
            Find Your Exact Path in{' '}
            <span className="bg-gradient-to-r from-cyan-400 via-sky-400 to-violet-400 bg-clip-text text-transparent">
              Higher Online Education
            </span>
          </h1>

          <p className="text-base sm:text-lg text-slate-300 leading-relaxed">
            Move beyond keywords. Describe your goals, current skills, and target career. Our FAISS semantic engine calculates your skill gaps, resolves course prerequisites, and curates a structured learning path from Coursera.
          </p>
        </div>

        {/* Central Search Form */}
        <div className="max-w-3xl mx-auto">
          <SearchForm onSubmit={handleSearch} loading={loading} />
        </div>

        {/* System Stats Bar */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto">
          <div className="rounded-2xl border border-white/10 bg-slate-900/60 p-4 text-center backdrop-blur-md">
            <span className="block text-2xl font-black text-cyan-300">884</span>
            <span className="text-xs uppercase tracking-wider text-slate-400">Coursera Courses</span>
          </div>
          <div className="rounded-2xl border border-white/10 bg-slate-900/60 p-4 text-center backdrop-blur-md">
            <span className="block text-2xl font-black text-violet-300">FAISS</span>
            <span className="text-xs uppercase tracking-wider text-slate-400">Vector Index (384-D)</span>
          </div>
          <div className="rounded-2xl border border-white/10 bg-slate-900/60 p-4 text-center backdrop-blur-md">
            <span className="block text-2xl font-black text-emerald-300">100%</span>
            <span className="text-xs uppercase tracking-wider text-slate-400">Skill Gap Resolution</span>
          </div>
          <div className="rounded-2xl border border-white/10 bg-slate-900/60 p-4 text-center backdrop-blur-md">
            <span className="block text-2xl font-black text-amber-300">Topological</span>
            <span className="text-xs uppercase tracking-wider text-slate-400">Prerequisite Engine</span>
          </div>
        </div>

        {/* Sample Real Prompts Grid */}
        <div className="space-y-4 max-w-5xl mx-auto">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xs font-bold uppercase tracking-widest text-cyan-400">Explore Representative Inquiries</h2>
              <p className="text-sm text-slate-300">Click any student query below to view real-time recommendations and learning paths:</p>
            </div>
          </div>

          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {sampleQueries.map((item, idx) => (
              <div
                key={idx}
                onClick={() => handleSearch(item.query)}
                className="group cursor-pointer rounded-2xl border border-slate-800 bg-slate-900/70 p-4 transition-all duration-300 hover:border-cyan-400/50 hover:bg-slate-800 hover:shadow-[0_10px_30px_rgba(34,211,238,0.12)] hover:-translate-y-0.5"
              >
                <div className="flex items-center justify-between gap-2 mb-2">
                  <span className="rounded-full bg-cyan-500/10 border border-cyan-400/20 px-2.5 py-0.5 text-[10px] font-semibold text-cyan-300">
                    {item.tag}
                  </span>
                  <ChevronRight size={14} className="text-slate-500 group-hover:text-cyan-300 group-hover:translate-x-0.5 transition" />
                </div>
                <h3 className="text-sm font-semibold text-white group-hover:text-cyan-100 transition line-clamp-1">
                  {item.title}
                </h3>
                <p className="mt-1 text-xs text-slate-400 line-clamp-2 leading-relaxed">
                  "{item.query}"
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* 4 Pillars Explanatory Cards */}
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4 max-w-6xl mx-auto pt-6 border-t border-slate-800">
          <div className="rounded-3xl border border-white/5 bg-slate-900/40 p-5 backdrop-blur-md">
            <div className="h-10 w-10 rounded-2xl bg-cyan-500/10 flex items-center justify-center text-cyan-400 mb-3 border border-cyan-500/20">
              <Sparkles size={20} />
            </div>
            <h3 className="text-sm font-bold text-white">Semantic Intent Search</h3>
            <p className="mt-1.5 text-xs leading-relaxed text-slate-400">
              Maps natural phrasing into 384-D dense vector space to find relevant courses beyond keywords.
            </p>
          </div>

          <div className="rounded-3xl border border-white/5 bg-slate-900/40 p-5 backdrop-blur-md">
            <div className="h-10 w-10 rounded-2xl bg-violet-500/10 flex items-center justify-center text-violet-400 mb-3 border border-violet-500/20">
              <Brain size={20} />
            </div>
            <h3 className="text-sm font-bold text-white">Skill Gap Analysis</h3>
            <p className="mt-1.5 text-xs leading-relaxed text-slate-400">
              Contrasts what you know against standard industry roles to calculate career readiness %.
            </p>
          </div>

          <div className="rounded-3xl border border-white/5 bg-slate-900/40 p-5 backdrop-blur-md">
            <div className="h-10 w-10 rounded-2xl bg-emerald-500/10 flex items-center justify-center text-emerald-400 mb-3 border border-emerald-500/20">
              <Compass size={20} />
            </div>
            <h3 className="text-sm font-bold text-white">Ordered Learning Path</h3>
            <p className="mt-1.5 text-xs leading-relaxed text-slate-400">
              Applies Kahn's topological sort on prerequisite DAGs to assemble a cycle-free curriculum.
            </p>
          </div>

          <div
            onClick={() => navigate('/evaluation')}
            className="group cursor-pointer rounded-3xl border border-cyan-500/20 bg-gradient-to-br from-slate-900/70 to-cyan-950/20 p-5 backdrop-blur-md transition hover:border-cyan-400/50 hover:shadow-lg hover:shadow-cyan-500/10"
          >
            <div className="h-10 w-10 rounded-2xl bg-cyan-500/15 flex items-center justify-center text-cyan-300 mb-3 border border-cyan-400/30 group-hover:scale-105 transition">
              <ShieldCheck size={20} />
            </div>
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-white group-hover:text-cyan-200 transition">System Evaluation</h3>
              <ArrowRight size={14} className="text-cyan-400 group-hover:translate-x-1 transition" />
            </div>
            <p className="mt-1.5 text-xs leading-relaxed text-slate-400">
              Inspect multi-factor mathematical scoring weights, IR benchmarks (P@3: 0.900), and rationale audit.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
