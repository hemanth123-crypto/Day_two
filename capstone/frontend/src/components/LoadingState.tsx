import { Loader2, Sparkles } from 'lucide-react';

type Props = {
  message?: string;
  submessage?: string;
};

export default function LoadingState({
  message = "Discovering the best courses for you...",
  submessage = "Analyzing semantic vectors, calculating skill gaps & structuring your learning path...",
}: Props) {
  return (
    <div className="flex flex-col items-center justify-center py-16 text-center">
      <div className="relative mb-6">
        <div className="h-16 w-16 rounded-3xl bg-gradient-to-tr from-cyan-500 to-violet-600 blur-xl opacity-60 animate-pulse" />
        <div className="absolute inset-0 flex items-center justify-center rounded-3xl border border-white/20 bg-slate-900/90 shadow-2xl backdrop-blur-xl">
          <Loader2 size={28} className="animate-spin text-cyan-400" />
        </div>
      </div>
      <h3 className="text-xl font-bold text-white">{message}</h3>
      <p className="mt-2 max-w-md text-sm text-slate-400">{submessage}</p>

      {/* Shimmer skeleton preview */}
      <div className="mt-8 grid w-full max-w-4xl gap-4 md:grid-cols-3">
        {[1, 2, 3].map((i) => (
          <div
            key={i}
            className="animate-pulse rounded-2xl border border-slate-800 bg-slate-900/40 p-5 text-left"
          >
            <div className="h-3 w-20 rounded-full bg-slate-800 mb-3" />
            <div className="h-5 w-40 rounded-full bg-slate-700 mb-4" />
            <div className="h-14 rounded-xl bg-slate-800/60 mb-4" />
            <div className="flex gap-2">
              <div className="h-4 w-12 rounded-full bg-slate-800" />
              <div className="h-4 w-16 rounded-full bg-slate-800" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
