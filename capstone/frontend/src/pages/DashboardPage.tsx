import { Clock, History, MessageSquare, Star, ThumbsUp, Trash2, TrendingUp, Zap } from 'lucide-react';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import { FeedbackStats } from '../types';

export default function DashboardPage() {
  const navigate = useNavigate();
  const [history, setHistory] = useState<any[]>([]);
  const [stats, setStats] = useState<FeedbackStats | null>(null);

  useEffect(() => {
    // Load local search history
    try {
      const stored = JSON.parse(localStorage.getItem('ucf_search_history') || '[]');
      setHistory(stored);
    } catch (e) {
      setHistory([]);
    }

    // Load feedback stats from API
    const loadStats = async () => {
      try {
        const response = await api.get('/feedback/stats');
        setStats(response.data);
      } catch (e) {
        // Fallback default
      }
    };
    loadStats();
  }, []);

  const clearHistory = () => {
    localStorage.removeItem('ucf_search_history');
    setHistory([]);
  };

  return (
    <div className="min-h-screen bg-slate-950 px-4 py-10 sm:px-8 text-slate-100">
      <div className="mx-auto max-w-6xl space-y-8">
        <div>
          <h1 className="text-3xl sm:text-4xl font-black text-white">System Dashboard & History</h1>
          <p className="mt-1 text-sm text-slate-400">
            Monitor search history, student recommendation satisfaction metrics, and live feedback statistics.
          </p>
        </div>

        {/* Feedback Performance Overview */}
        {stats && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="rounded-3xl border border-white/10 bg-slate-900/70 p-5 backdrop-blur-xl">
              <span className="block text-xs uppercase tracking-wider text-slate-400">Total Feedback</span>
              <span className="mt-1 block text-3xl font-black text-cyan-300">{stats.total_feedback}</span>
              <span className="text-[10px] text-slate-500">Stored in SQLite</span>
            </div>

            <div className="rounded-3xl border border-white/10 bg-slate-900/70 p-5 backdrop-blur-xl">
              <span className="block text-xs uppercase tracking-wider text-slate-400">Average Rating</span>
              <div className="mt-1 flex items-center gap-1.5 text-3xl font-black text-amber-300">
                <Star size={24} className="fill-amber-400 text-amber-400" />
                <span>{stats.average_rating || 5.0}</span>
              </div>
              <span className="text-[10px] text-slate-500">out of 5.0</span>
            </div>

            <div className="rounded-3xl border border-white/10 bg-slate-900/70 p-5 backdrop-blur-xl">
              <span className="block text-xs uppercase tracking-wider text-slate-400">Usefulness Rate</span>
              <div className="mt-1 flex items-center gap-1.5 text-3xl font-black text-emerald-300">
                <ThumbsUp size={22} className="text-emerald-400" />
                <span>{stats.usefulness_rate || 100}%</span>
              </div>
              <span className="text-[10px] text-slate-500">Positive student ratings</span>
            </div>

            <div className="rounded-3xl border border-white/10 bg-slate-900/70 p-5 backdrop-blur-xl">
              <span className="block text-xs uppercase tracking-wider text-slate-400">Vector Engine</span>
              <div className="mt-1 flex items-center gap-1.5 text-2xl font-black text-violet-300">
                <Zap size={20} className="text-violet-400" />
                <span>FAISS FlatIP</span>
              </div>
              <span className="text-[10px] text-slate-500">384-D Cosine Sim</span>
            </div>
          </div>
        )}

        <div className="grid gap-6 lg:grid-cols-2">
          {/* Recent Searches */}
          <div className="rounded-3xl border border-white/10 bg-slate-900/70 p-6 backdrop-blur-xl space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <History size={18} className="text-cyan-400" />
                <h3 className="text-base font-bold text-white">Recent Search Inquiries</h3>
              </div>
              {history.length > 0 && (
                <button
                  type="button"
                  onClick={clearHistory}
                  className="flex items-center gap-1 text-xs text-rose-400 hover:text-rose-300 transition"
                >
                  <Trash2 size={13} /> Clear
                </button>
              )}
            </div>

            {history.length === 0 ? (
              <p className="text-xs text-slate-500 py-6 text-center">
                No recent searches in this browser session. Enter a query from the Home page!
              </p>
            ) : (
              <div className="space-y-2.5 max-h-96 overflow-y-auto pr-1">
                {history.map((h, i) => (
                  <div
                    key={i}
                    onClick={() => navigate('/results', { state: { query: h.query } })}
                    className="group cursor-pointer rounded-2xl border border-slate-800 bg-slate-950/60 p-3.5 transition hover:border-cyan-400/50 hover:bg-slate-900"
                  >
                    <div className="flex items-start justify-between gap-2">
                      <p className="text-xs font-semibold text-white group-hover:text-cyan-200 transition">
                        "{h.query}"
                      </p>
                      <span className="rounded-full bg-slate-800 px-2 py-0.5 text-[10px] text-cyan-300 flex-shrink-0">
                        {h.career}
                      </span>
                    </div>
                    <span className="mt-1.5 block text-[10px] text-slate-500">
                      {new Date(h.timestamp).toLocaleDateString()} at{' '}
                      {new Date(h.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Recent Student Feedback */}
          <div className="rounded-3xl border border-white/10 bg-slate-900/70 p-6 backdrop-blur-xl space-y-4">
            <div className="flex items-center gap-2">
              <MessageSquare size={18} className="text-amber-400" />
              <h3 className="text-base font-bold text-white">Latest Recommendation Feedback</h3>
            </div>

            {stats?.recent_feedback && stats.recent_feedback.length > 0 ? (
              <div className="space-y-2.5 max-h-96 overflow-y-auto pr-1">
                {stats.recent_feedback.map((fb) => (
                  <div
                    key={fb.id}
                    className="rounded-2xl border border-slate-800 bg-slate-950/60 p-3.5"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-1 text-amber-300">
                        {[...Array(fb.rating)].map((_, idx) => (
                          <Star key={idx} size={13} className="fill-amber-400 text-amber-400" />
                        ))}
                      </div>
                      <span
                        className={`rounded-full px-2 py-0.5 text-[10px] font-semibold ${
                          fb.useful
                            ? 'bg-emerald-500/10 text-emerald-300 border border-emerald-500/30'
                            : 'bg-rose-500/10 text-rose-300 border border-rose-500/30'
                        }`}
                      >
                        {fb.useful ? 'Useful' : 'Not Useful'}
                      </span>
                    </div>
                    {fb.comment && (
                      <p className="mt-2 text-xs text-slate-300 italic">"{fb.comment}"</p>
                    )}
                    <span className="mt-2 block text-[10px] text-slate-500">
                      {fb.course_id ? `Course: ${fb.course_id}` : 'General Recommendation'} •{' '}
                      {fb.created_at ? new Date(fb.created_at).toLocaleDateString() : 'Just now'}
                    </span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-xs text-slate-500 py-6 text-center">
                No feedback received yet. Submit feedback on any recommended course!
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
