import { Award, BrainCircuit, Check, Info, Sparkles, TrendingUp } from 'lucide-react';
import { Course } from '../types';

type Props = {
  course: Course;
  targetCareer?: string | null;
};

export default function RecommendationExplanation({ course, targetCareer }: Props) {
  const finalScorePct = Math.round((course.final_score || 0) * 100);
  const semanticPct = Math.round((course.semantic_norm || course.semantic_score || 0) * 100);
  const skillPct = Math.round((course.skill_norm || course.skill_score || 0) * 100);
  const difficultyPct = Math.round((course.difficulty_norm || course.difficulty_score || 0) * 100);
  const ratingPct = Math.round((course.rating_norm || course.rating_score || 0) * 100);

  return (
    <div className="rounded-2xl border border-cyan-500/20 bg-gradient-to-br from-slate-900 via-slate-900/90 to-cyan-950/20 p-5 shadow-lg backdrop-blur-xl">
      <div className="mb-3 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-cyan-500/10 text-cyan-400">
            <Sparkles size={16} />
          </div>
          <span className="text-xs font-semibold uppercase tracking-wider text-cyan-300">
            Why This Course?
          </span>
        </div>
        <div className="flex items-center gap-1.5 rounded-full border border-cyan-400/30 bg-cyan-500/10 px-3 py-1 text-xs font-bold text-cyan-200">
          <TrendingUp size={12} />
          {finalScorePct}% Match Score
        </div>
      </div>

      <p className="text-xs text-slate-200 leading-relaxed">
        {course.explanation ||
          `This course aligns closely with your objective${
            targetCareer ? ` in ${targetCareer}` : ''
          } and provides verified instruction from ${course.organization || 'top partners'}.`}
      </p>

      {/* Multi-factor Score Breakdown */}
      <div className="mt-4 grid grid-cols-2 gap-2 sm:grid-cols-4 text-center">
        <div className="rounded-xl border border-slate-800 bg-slate-950/60 p-2">
          <span className="block text-[10px] uppercase tracking-wider text-slate-400">Semantic</span>
          <span className="text-xs font-bold text-cyan-300">{semanticPct}%</span>
        </div>
        <div className="rounded-xl border border-slate-800 bg-slate-950/60 p-2">
          <span className="block text-[10px] uppercase tracking-wider text-slate-400">Skill Gap</span>
          <span className="text-xs font-bold text-violet-300">{skillPct}%</span>
        </div>
        <div className="rounded-xl border border-slate-800 bg-slate-950/60 p-2">
          <span className="block text-[10px] uppercase tracking-wider text-slate-400">Difficulty</span>
          <span className="text-xs font-bold text-emerald-300">{difficultyPct}%</span>
        </div>
        <div className="rounded-xl border border-slate-800 bg-slate-950/60 p-2">
          <span className="block text-[10px] uppercase tracking-wider text-slate-400">Rating</span>
          <span className="text-xs font-bold text-amber-300">{ratingPct}%</span>
        </div>
      </div>

      {/* Matched Skills */}
      {course.matched_skills && course.matched_skills.length > 0 && (
        <div className="mt-3.5 flex flex-wrap items-center gap-1.5 pt-2 border-t border-slate-800">
          <span className="text-[10px] uppercase tracking-wider text-slate-400 mr-1">Directly Covers:</span>
          {course.matched_skills.map((skill) => (
            <span
              key={skill}
              className="inline-flex items-center gap-1 rounded-md border border-cyan-500/30 bg-cyan-500/10 px-2 py-0.5 text-[10px] font-medium text-cyan-200"
            >
              <Check size={10} className="text-cyan-400" />
              {skill}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}
