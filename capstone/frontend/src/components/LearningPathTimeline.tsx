import { ArrowRight, BookOpen, CheckCircle, ChevronRight, Compass, GitCommit, Layers, Star } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Course, LearningPathStep } from '../types';

type Props = {
  steps: LearningPathStep[];
  onSelectCourse?: (step: LearningPathStep) => void;
};

export default function LearningPathTimeline({ steps, onSelectCourse }: Props) {
  if (!steps || steps.length === 0) {
    return (
      <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-8 text-center text-slate-400">
        No learning path sequence generated for this query.
      </div>
    );
  }

  const getDifficultyColor = (diff: string) => {
    const lower = diff.toLowerCase();
    if (lower.includes('begin')) return 'border-emerald-500/40 bg-emerald-500/10 text-emerald-300';
    if (lower.includes('intermed')) return 'border-cyan-500/40 bg-cyan-500/10 text-cyan-300';
    return 'border-violet-500/40 bg-violet-500/10 text-violet-300';
  };

  return (
    <div className="relative space-y-6 before:absolute before:bottom-6 before:left-6 before:top-6 before:w-0.5 before:bg-gradient-to-b before:from-cyan-400 before:via-sky-500 before:to-violet-600">
      {steps.map((step) => {
        return (
          <div
            key={step.order}
            className="group relative flex items-start gap-5 rounded-3xl border border-white/10 bg-slate-900/80 p-6 shadow-xl backdrop-blur-xl transition hover:border-cyan-400/50 hover:bg-slate-900"
          >
            {/* Step Number Badge */}
            <div className="relative z-10 flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-2xl bg-gradient-to-tr from-cyan-400 via-sky-500 to-violet-600 font-black text-slate-950 shadow-[0_0_20px_rgba(34,211,238,0.4)]">
              {step.order}
            </div>

            <div className="flex-1 min-w-0">
              <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <span className="text-[11px] font-bold uppercase tracking-wider text-cyan-400">
                    {step.organization || 'University Curriculum'}
                  </span>
                  <h4 className="text-xl font-bold text-white group-hover:text-cyan-200 transition">
                    {step.course}
                  </h4>
                </div>
                <div className="flex items-center gap-2">
                  <span
                    className={`rounded-full border px-3 py-1 text-xs font-semibold uppercase tracking-wider ${getDifficultyColor(
                      step.difficulty
                    )}`}
                  >
                    {step.difficulty}
                  </span>
                  {step.rating && (
                    <span className="flex items-center gap-1 rounded-full bg-slate-800 px-2.5 py-1 text-xs text-amber-300">
                      <Star size={12} className="fill-amber-400 text-amber-400" />
                      {step.rating}
                    </span>
                  )}
                </div>
              </div>

              {/* Educational Rationale */}
              <p className="mt-3 text-xs leading-relaxed text-slate-300">
                {step.reason}
              </p>

              {/* Skills & Prerequisites Footer */}
              <div className="mt-4 flex flex-wrap items-center justify-between gap-3 border-t border-slate-800 pt-3">
                <div className="flex flex-wrap items-center gap-1.5">
                  <span className="text-[10px] uppercase tracking-wider text-slate-400">Skills Acquired:</span>
                  {step.skills.map((skill) => (
                    <span
                      key={skill}
                      className="rounded-lg bg-slate-800/90 px-2 py-0.5 text-[11px] text-slate-200"
                    >
                      {skill}
                    </span>
                  ))}
                </div>

                {step.prerequisites && step.prerequisites.length > 0 && (
                  <div className="flex items-center gap-1 text-[11px] text-slate-400">
                    <span className="font-semibold text-slate-300">Prerequisites:</span>
                    <span>{step.prerequisites.join(', ')}</span>
                  </div>
                )}

                {step.course_id && step.course_id.startsWith('course_') && (
                  <Link
                    to={`/course/${step.course_id}`}
                    className="inline-flex items-center gap-1 text-xs font-semibold text-cyan-400 hover:text-cyan-300 transition"
                  >
                    Course details <ChevronRight size={14} />
                  </Link>
                )}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
