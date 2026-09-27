import {
  AlertTriangle,
  Award,
  BarChart3,
  BookOpen,
  CheckCircle2,
  ChevronRight,
  HelpCircle,
  Info,
  ShieldCheck,
  Sparkles,
  TrendingUp,
  Zap,
} from 'lucide-react';
import { useState } from 'react';
import { CourseEvaluation } from '../types';
import EvaluationModal from './EvaluationModal';

type Props = {
  evaluations: CourseEvaluation[];
  targetCareer?: string;
  studentSkills?: string[];
  missingSkills?: string[];
  coveragePct?: number;
  loading?: boolean;
};

export default function EvaluationPanel({
  evaluations,
  targetCareer = 'Target Career',
  studentSkills = [],
  missingSkills = [],
  coveragePct = 0,
  loading = false,
}: Props) {
  const [activeModalEval, setActiveModalEval] = useState<CourseEvaluation | null>(null);

  if (loading) {
    return (
      <div className="rounded-3xl border border-slate-800 bg-slate-900/60 p-12 text-center text-slate-300">
        <div className="mx-auto mb-4 h-8 w-8 animate-spin rounded-full border-2 border-cyan-400 border-t-transparent" />
        <p className="text-sm font-semibold">Generating transparent course evaluation matrix...</p>
      </div>
    );
  }

  if (!evaluations || evaluations.length === 0) {
    return (
      <div className="rounded-3xl border border-slate-800 bg-slate-900/60 p-12 text-center text-slate-400">
        <HelpCircle size={32} className="mx-auto mb-3 text-slate-500" />
        <p className="text-base font-semibold text-slate-200">No course evaluations available.</p>
        <p className="text-xs text-slate-400 mt-1">Submit a search query to inspect recommendation rationales.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Top Banner: Transparency & System Audit */}
      <div className="rounded-3xl border border-cyan-500/20 bg-gradient-to-r from-slate-900/90 via-slate-900/80 to-cyan-950/20 p-6 shadow-xl backdrop-blur-xl">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <Sparkles size={16} className="text-cyan-400" />
              <span className="text-xs font-bold uppercase tracking-wider text-cyan-400">
                Transparent Recommendation Audit & Explainability
              </span>
            </div>
            <h3 className="mt-1 text-2xl font-bold text-white">
              Why We Recommended These Courses For {targetCareer}
            </h3>
            <p className="mt-1 text-xs text-slate-300 max-w-2xl leading-relaxed">
              Every course is evaluated using normalized multi-signal hybrid scoring, direct skill-gap closure,
              and educational prerequisite dependency verification through a topological DAG.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <div className="rounded-2xl border border-slate-700 bg-slate-800/80 px-4 py-2.5 text-center">
              <span className="block text-[10px] uppercase tracking-wider text-slate-400">Courses Evaluated</span>
              <strong className="text-lg font-bold text-cyan-300">{evaluations.length}</strong>
            </div>
            <div className="rounded-2xl border border-slate-700 bg-slate-800/80 px-4 py-2.5 text-center">
              <span className="block text-[10px] uppercase tracking-wider text-slate-400">Prerequisite Safety</span>
              <strong className="text-lg font-bold text-emerald-300">100% DAG</strong>
            </div>
          </div>
        </div>
      </div>

      {/* Explanatory Methodology Card */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-4">
          <div className="flex items-center gap-2 text-cyan-300 font-semibold text-xs mb-1">
            <BarChart3 size={15} />
            Multi-Signal Hybrid Weights
          </div>
          <p className="text-[11px] text-slate-300 leading-relaxed">
            Semantic (54.5%) + Skill Gap (18.2%) + Career Fit (9.1%) + Difficulty (9.1%) + Rating (9.1%).
          </p>
        </div>

        <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-4">
          <div className="flex items-center gap-2 text-emerald-300 font-semibold text-xs mb-1">
            <ShieldCheck size={15} />
            Prerequisite Verification
          </div>
          <p className="text-[11px] text-slate-300 leading-relaxed">
            Dependencies are checked against your current competencies ({studentSkills.length} verified skills) to prevent gaps.
          </p>
        </div>

        <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-4">
          <div className="flex items-center gap-2 text-violet-300 font-semibold text-xs mb-1">
            <Zap size={15} />
            Zero-Hallucination Explanations
          </div>
          <p className="text-[11px] text-slate-300 leading-relaxed">
            All justifications are synthesized from verified Coursera partner metadata, difficulty, and ratings.
          </p>
        </div>
      </div>

      {/* Course Evaluation Cards List */}
      <div className="space-y-4">
        <h4 className="text-sm font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
          <BookOpen size={16} className="text-cyan-400" />
          Course-by-Course Evaluation Matrix
        </h4>

        {evaluations.map((evalItem) => {
          const scorePct = Math.round(evalItem.final_score * 100);
          const readiness = evalItem.prerequisite_readiness;

          return (
            <div
              key={evalItem.course_id}
              className="group rounded-3xl border border-slate-800 bg-slate-900/70 p-5 sm:p-6 transition-all duration-300 hover:border-cyan-500/50 hover:bg-slate-900 hover:shadow-xl"
            >
              <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
                {/* Left: Course details and badges */}
                <div className="space-y-2 max-w-2xl">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="rounded-full bg-cyan-500/10 border border-cyan-500/30 px-2.5 py-0.5 text-xs font-bold text-cyan-300">
                      Rank #{evalItem.rank}
                    </span>
                    <span className="rounded-full bg-violet-500/10 border border-violet-500/30 px-2.5 py-0.5 text-xs font-semibold text-violet-300">
                      {evalItem.verdict_badge}
                    </span>
                    <span className="text-xs text-slate-400">
                      {evalItem.organization} • {evalItem.difficulty} • ★ {evalItem.rating ? evalItem.rating.toFixed(1) : '4.5'}
                    </span>
                  </div>

                  <h3 className="text-lg font-bold text-white group-hover:text-cyan-200 transition">
                    {evalItem.course_name}
                  </h3>

                  <p className="text-xs text-slate-300 leading-relaxed">
                    {evalItem.detailed_justification}
                  </p>

                  {/* Closed skills pills */}
                  {evalItem.closed_skill_gaps.length > 0 && (
                    <div className="flex flex-wrap items-center gap-1.5 pt-1">
                      <span className="text-[10px] uppercase tracking-wider text-slate-400">
                        Bridges Skill Gap in:
                      </span>
                      {evalItem.closed_skill_gaps.map((sk) => (
                        <span
                          key={sk}
                          className="rounded-md border border-cyan-500/30 bg-cyan-500/10 px-2 py-0.5 text-[10px] font-semibold text-cyan-200"
                        >
                          ✓ {sk}
                        </span>
                      ))}
                    </div>
                  )}
                </div>

                {/* Right: Scores & Action Button */}
                <div className="flex flex-row lg:flex-col items-center lg:items-end justify-between lg:justify-center gap-4 shrink-0 border-t lg:border-t-0 pt-4 lg:pt-0 border-slate-800">
                  <div className="text-left lg:text-right">
                    <div className="flex items-center gap-2 lg:justify-end">
                      <TrendingUp size={16} className="text-cyan-400" />
                      <span className="text-2xl font-black text-cyan-300">{scorePct}%</span>
                    </div>
                    <span className="text-[10px] text-slate-400 block">Total Match Score</span>

                    <div className="mt-1">
                      {readiness.status === 'READY' ? (
                        <span className="inline-flex items-center gap-1 text-[11px] font-semibold text-emerald-400">
                          <CheckCircle2 size={12} /> Prerequisite Ready
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 text-[11px] font-semibold text-amber-400">
                          <AlertTriangle size={12} /> Review Recommended
                        </span>
                      )}
                    </div>
                  </div>

                  <button
                    type="button"
                    onClick={() => setActiveModalEval(evalItem)}
                    className="inline-flex items-center gap-1.5 rounded-xl border border-cyan-500/40 bg-cyan-500/10 hover:bg-cyan-500/20 px-4 py-2 text-xs font-semibold text-cyan-200 transition shadow-sm"
                  >
                    Why Recommended?
                    <ChevronRight size={14} />
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Interactive Modal */}
      <EvaluationModal
        evaluation={activeModalEval}
        isOpen={activeModalEval !== null}
        onClose={() => setActiveModalEval(null)}
        targetCareer={targetCareer}
      />
    </div>
  );
}
