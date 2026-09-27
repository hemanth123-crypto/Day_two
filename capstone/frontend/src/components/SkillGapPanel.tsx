import { BookOpen, CheckCircle2, ChevronRight, HelpCircle, Sparkles, Target, XCircle } from 'lucide-react';
import { useState } from 'react';
import { Course } from '../types';

type Props = {
  currentSkills: string[];
  missingSkills: string[];
  requiredSkills: string[];
  coverage: number;
  targetCareer?: string;
  missingSkillsCourses?: Record<string, Course[]>;
  onSelectCourse?: (course: Course) => void;
};

export default function SkillGapPanel({
  currentSkills,
  missingSkills,
  requiredSkills,
  coverage,
  targetCareer,
  missingSkillsCourses = {},
  onSelectCourse,
}: Props) {
  const [activeMissingSkill, setActiveMissingSkill] = useState<string | null>(
    missingSkills.length > 0 ? missingSkills[0] : null
  );

  return (
    <div className="rounded-3xl border border-white/10 bg-slate-900/80 p-6 shadow-2xl backdrop-blur-xl">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between mb-6">
        <div>
          <span className="text-xs font-semibold uppercase tracking-wider text-cyan-400">
            Intelligent Gap Analysis
          </span>
          <h3 className="mt-1 text-2xl font-bold text-white">
            Skill Competency for {targetCareer || 'Target Career'}
          </h3>
        </div>
        <div className="inline-flex items-center gap-2 rounded-2xl border border-emerald-400/30 bg-emerald-500/10 px-4 py-2 text-sm font-bold text-emerald-300 shadow-[0_0_20px_rgba(52,211,153,0.15)]">
          <Sparkles size={16} />
          {Math.round(coverage)}% Readiness
        </div>
      </div>

      {/* Coverage Progress Bar */}
      <div className="mb-6 rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
        <div className="flex items-center justify-between text-xs text-slate-300 mb-2">
          <span>Career Skill Coverage</span>
          <span className="font-bold text-cyan-300">
            {requiredSkills.length - missingSkills.length} of {requiredSkills.length || currentSkills.length} skills mastered
          </span>
        </div>
        <div className="h-3 w-full overflow-hidden rounded-full bg-slate-800">
          <div
            className="h-full rounded-full bg-gradient-to-r from-cyan-400 via-sky-400 to-emerald-400 transition-all duration-700 shadow-[0_0_16px_rgba(34,211,238,0.5)]"
            style={{ width: `${Math.max(coverage, 5)}%` }}
          />
        </div>
      </div>

      {/* 2-Column: Current Skills vs Missing Skills */}
      <div className="grid gap-5 md:grid-cols-2">
        {/* Current Skills */}
        <div className="rounded-2xl border border-emerald-500/20 bg-emerald-950/10 p-5">
          <div className="mb-3 flex items-center gap-2">
            <CheckCircle2 size={16} className="text-emerald-400" />
            <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-300">
              Your Current Competencies ({currentSkills.length})
            </h4>
          </div>
          {currentSkills.length > 0 ? (
            <div className="flex flex-wrap gap-2">
              {currentSkills.map((skill) => (
                <span
                  key={skill}
                  className="rounded-xl border border-emerald-500/30 bg-emerald-500/15 px-3 py-1 text-xs font-medium text-emerald-200"
                >
                  ✓ {skill}
                </span>
              ))}
            </div>
          ) : (
            <p className="text-xs text-slate-400">
              No current skills were detected from your query.
            </p>
          )}
        </div>

        {/* Missing Skills */}
        <div className="rounded-2xl border border-amber-500/20 bg-amber-950/10 p-5">
          <div className="mb-3 flex items-center gap-2">
            <XCircle size={16} className="text-amber-400" />
            <h4 className="text-xs font-bold uppercase tracking-wider text-amber-300">
              Identified Skill Gaps ({missingSkills.length})
            </h4>
          </div>
          {missingSkills.length > 0 ? (
            <div className="flex flex-wrap gap-2">
              {missingSkills.map((skill) => {
                const isActive = activeMissingSkill === skill;
                return (
                  <button
                    key={skill}
                    type="button"
                    onClick={() => setActiveMissingSkill(skill)}
                    className={`rounded-xl px-3 py-1 text-xs font-medium transition flex items-center gap-1 ${
                      isActive
                        ? 'border border-amber-400 bg-amber-500/25 text-amber-200 shadow-md ring-1 ring-amber-400/50'
                        : 'border border-amber-500/30 bg-amber-500/10 text-amber-300 hover:bg-amber-500/20'
                    }`}
                  >
                    • {skill}
                  </button>
                );
              })}
            </div>
          ) : (
            <p className="text-xs text-emerald-300">
              Outstanding! You already cover all core skills required for this career target.
            </p>
          )}
        </div>
      </div>

      {/* Recommended Courses to Close Selected Missing Skill Gap */}
      {activeMissingSkill && missingSkillsCourses[activeMissingSkill] && missingSkillsCourses[activeMissingSkill].length > 0 && (
        <div className="mt-6 rounded-2xl border border-cyan-500/30 bg-gradient-to-r from-slate-950 via-slate-900 to-slate-950 p-5">
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-cyan-300 mb-3">
            <Target size={14} />
            <span>Recommended Course to bridge gap: {activeMissingSkill}</span>
          </div>
          <div className="grid gap-3 sm:grid-cols-2">
            {missingSkillsCourses[activeMissingSkill].map((course) => (
              <div
                key={course.course_id}
                onClick={() => onSelectCourse && onSelectCourse(course)}
                className="cursor-pointer rounded-xl border border-slate-700 bg-slate-900/90 p-4 transition hover:border-cyan-400 hover:bg-slate-800"
              >
                <div className="flex items-start justify-between gap-2">
                  <h5 className="text-sm font-semibold text-white truncate">{course.course_name}</h5>
                  <span className="rounded-full bg-slate-800 px-2 py-0.5 text-[10px] text-cyan-300">
                    {course.difficulty}
                  </span>
                </div>
                <p className="mt-1 text-xs text-slate-400">
                  {course.organization || 'Coursera Partner'} • Rating: {course.rating || 'N/A'}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
