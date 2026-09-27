import {
  AlertTriangle,
  Award,
  BookOpen,
  CheckCircle2,
  ExternalLink,
  HelpCircle,
  Info,
  ShieldCheck,
  Sparkles,
  TrendingUp,
  X,
  Zap,
} from 'lucide-react';
import { CourseEvaluation } from '../types';

type Props = {
  evaluation: CourseEvaluation | null;
  isOpen: boolean;
  onClose: () => void;
  targetCareer?: string | null;
};

export default function EvaluationModal({
  evaluation,
  isOpen,
  onClose,
  targetCareer,
}: Props) {
  if (!isOpen || !evaluation) return null;

  const scorePct = Math.round(evaluation.final_score * 100);
  const readiness = evaluation.prerequisite_readiness;

  const getReadinessBadge = () => {
    switch (readiness.status) {
      case 'READY':
        return (
          <span className="inline-flex items-center gap-1.5 rounded-full border border-emerald-500/30 bg-emerald-500/10 px-3 py-1 text-xs font-semibold text-emerald-300">
            <CheckCircle2 size={13} className="text-emerald-400" />
            100% Prerequisite Ready
          </span>
        );
      case 'MOSTLY_READY':
        return (
          <span className="inline-flex items-center gap-1.5 rounded-full border border-cyan-500/30 bg-cyan-500/10 px-3 py-1 text-xs font-semibold text-cyan-300">
            <Info size={13} className="text-cyan-400" />
            Mostly Ready ({Math.round(readiness.readiness_score * 100)}%)
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1.5 rounded-full border border-amber-500/30 bg-amber-500/10 px-3 py-1 text-xs font-semibold text-amber-300">
            <AlertTriangle size={13} className="text-amber-400" />
            Prior Milestones Recommended
          </span>
        );
    }
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-fade-in"
      onClick={onClose}
    >
      <div
        className="relative w-full max-w-3xl max-h-[90vh] overflow-y-auto rounded-3xl border border-slate-700/80 bg-gradient-to-b from-slate-900 via-slate-900 to-slate-950 p-6 sm:p-8 shadow-2xl text-slate-100"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Close Button */}
        <button
          type="button"
          onClick={onClose}
          className="absolute right-5 top-5 rounded-full p-2 text-slate-400 hover:bg-slate-800 hover:text-white transition"
          aria-label="Close"
        >
          <X size={18} />
        </button>

        {/* Header */}
        <div className="flex items-start gap-4 mb-6 pr-8">
          <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 shadow-inner">
            <Sparkles size={24} />
          </div>
          <div>
            <div className="flex flex-wrap items-center gap-2 mb-1">
              <span className="text-[11px] font-bold uppercase tracking-wider text-cyan-400">
                Evaluation & Recommendation Rationale
              </span>
              <span className="rounded-full bg-slate-800 border border-slate-700 px-2 py-0.5 text-[10px] text-slate-300">
                Rank #{evaluation.rank}
              </span>
              <span className="rounded-full bg-violet-500/10 border border-violet-500/30 px-2.5 py-0.5 text-[10px] font-semibold text-violet-300">
                {evaluation.verdict_badge}
              </span>
            </div>
            <h2 className="text-xl sm:text-2xl font-bold text-white leading-tight">
              {evaluation.course_name}
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              Offered by <strong className="text-slate-200">{evaluation.organization}</strong> • {evaluation.difficulty} Level • ★ {evaluation.rating ? evaluation.rating.toFixed(1) : '4.5'}
            </p>
          </div>
        </div>

        {/* Match Score Banner */}
        <div className="mb-6 rounded-2xl border border-cyan-500/30 bg-gradient-to-r from-cyan-950/40 via-slate-900 to-violet-950/30 p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-1.5 text-xs font-semibold text-cyan-300 uppercase tracking-wider">
              <TrendingUp size={14} /> Overall Match Alignment
            </div>
            <p className="text-sm font-semibold text-white mt-0.5">
              {evaluation.verdict}
            </p>
          </div>
          <div className="flex items-center gap-3">
            <div className="text-right">
              <span className="text-2xl font-black text-cyan-300">{scorePct}%</span>
              <span className="block text-[10px] text-slate-400">Hybrid Match</span>
            </div>
            <div className="h-10 w-px bg-slate-700/60" />
            <div>{getReadinessBadge()}</div>
          </div>
        </div>

        {/* Narrative Justification */}
        <div className="mb-6 rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
          <h4 className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-slate-300 mb-2">
            <BookOpen size={14} className="text-cyan-400" />
            Why This Course Was Recommended To You
          </h4>
          <p className="text-xs sm:text-sm text-slate-200 leading-relaxed">
            {evaluation.detailed_justification}
          </p>
        </div>

        {/* Prerequisite Readiness Assessment */}
        <div className="mb-6 rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
          <div className="flex items-center justify-between mb-3">
            <h4 className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-slate-300">
              <ShieldCheck size={14} className="text-emerald-400" />
              Prerequisite Readiness Analysis
            </h4>
            <span className="text-xs font-semibold text-slate-400">
              Status: <strong className={readiness.status === 'READY' ? 'text-emerald-300' : 'text-amber-300'}>{readiness.status}</strong>
            </span>
          </div>

          <p className="text-xs text-slate-300 mb-3 leading-relaxed">
            {readiness.guidance}
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
            <div className="rounded-xl border border-emerald-500/20 bg-emerald-950/20 p-3">
              <span className="block text-[10px] font-bold uppercase tracking-wider text-emerald-400 mb-1">
                Satisfied By Your Current Skills
              </span>
              {readiness.satisfied_prerequisites.length > 0 ? (
                <div className="flex flex-wrap gap-1.5 mt-1">
                  {readiness.satisfied_prerequisites.map((p) => (
                    <span key={p} className="rounded bg-emerald-500/20 px-2 py-0.5 text-[11px] text-emerald-200 font-medium">
                      ✓ {p}
                    </span>
                  ))}
                </div>
              ) : (
                <span className="text-slate-400 italic text-[11px]">No formal prerequisites required.</span>
              )}
            </div>

            <div className="rounded-xl border border-amber-500/20 bg-amber-950/20 p-3">
              <span className="block text-[10px] font-bold uppercase tracking-wider text-amber-400 mb-1">
                Helpful Prerequisites To Review
              </span>
              {readiness.missing_prerequisites.length > 0 ? (
                <div className="flex flex-wrap gap-1.5 mt-1">
                  {readiness.missing_prerequisites.map((p) => (
                    <span key={p} className="rounded bg-amber-500/20 px-2 py-0.5 text-[11px] text-amber-200 font-medium">
                      • {p}
                    </span>
                  ))}
                </div>
              ) : (
                <span className="text-emerald-400 italic text-[11px]">None! You are ready to start.</span>
              )}
            </div>
          </div>
        </div>

        {/* 5-Factor Score Decomposition */}
        <div className="mb-6 rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
          <div className="flex items-center justify-between mb-4">
            <h4 className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-slate-300">
              <Zap size={14} className="text-amber-400" />
              Hybrid Scoring Decomposition
            </h4>
            <span className="text-[10px] text-slate-400">
              Formula: ∑ (Weight × Normalized Subscore)
            </span>
          </div>

          <div className="space-y-3">
            {Object.entries(evaluation.factors).map(([key, factor]) => {
              const pct = Math.round(factor.normalized_score * 100);
              const contribPct = factor.percentage_of_final;

              return (
                <div key={key} className="space-y-1">
                  <div className="flex items-center justify-between text-xs">
                    <div className="flex items-center gap-2">
                      <span className="font-semibold text-slate-200">{factor.name}</span>
                      <span className="text-[10px] text-slate-400">
                        (Weight: {(factor.weight * 100).toFixed(0)}%)
                      </span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-bold text-cyan-300">{pct}%</span>
                      <span className="text-[10px] font-medium text-slate-400">
                        (+{factor.points_contributed.toFixed(3)} pts / {contribPct}% of total)
                      </span>
                    </div>
                  </div>
                  <div className="h-1.5 w-full rounded-full bg-slate-800 overflow-hidden">
                    <div
                      className={`h-full rounded-full ${
                        key === 'semantic'
                          ? 'bg-cyan-400'
                          : key === 'skill_gap'
                          ? 'bg-violet-400'
                          : key === 'career_fit'
                          ? 'bg-blue-400'
                          : key === 'difficulty_fit'
                          ? 'bg-emerald-400'
                          : 'bg-amber-400'
                      }`}
                      style={{ width: `${Math.max(pct, 5)}%` }}
                    />
                  </div>
                  <p className="text-[11px] text-slate-400 leading-normal">
                    {factor.explanation}
                  </p>
                </div>
              );
            })}
          </div>
        </div>

        {/* Strengths & Considerations */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
          <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
            <h5 className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-emerald-400 mb-2">
              <CheckCircle2 size={13} />
              Key Educational Strengths
            </h5>
            <ul className="space-y-1.5 text-xs text-slate-300">
              {evaluation.key_strengths.map((str, idx) => (
                <li key={idx} className="flex items-start gap-1.5">
                  <span className="text-emerald-400 font-bold">•</span>
                  <span>{str}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
            <h5 className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-amber-400 mb-2">
              <AlertTriangle size={13} />
              Learning Considerations
            </h5>
            <ul className="space-y-1.5 text-xs text-slate-300">
              {evaluation.considerations.length > 0 ? (
                evaluation.considerations.map((con, idx) => (
                  <li key={idx} className="flex items-start gap-1.5">
                    <span className="text-amber-400 font-bold">•</span>
                    <span>{con}</span>
                  </li>
                ))
              ) : (
                <li className="text-slate-400 italic">No special caveats. Course is directly accessible.</li>
              )}
            </ul>
          </div>
        </div>

        {/* Footer Actions */}
        <div className="flex items-center justify-between border-t border-slate-800 pt-4">
          <span className="text-xs text-slate-400">
            Intelligent Course Finder Evaluation System
          </span>
          <button
            type="button"
            onClick={onClose}
            className="rounded-xl bg-slate-800 hover:bg-slate-700 px-5 py-2 text-xs font-semibold text-white transition"
          >
            Close Rationale
          </button>
        </div>
      </div>
    </div>
  );
}
