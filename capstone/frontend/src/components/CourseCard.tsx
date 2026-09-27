import { ArrowRight, BookOpen, Sparkles, Star } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Course } from '../types';

type Props = {
  course: Course;
  isSelected?: boolean;
  onSelect?: () => void;
  onExplain?: (course: Course) => void;
};

export default function CourseCard({ course, isSelected = false, onSelect, onExplain }: Props) {
  const skills = course.skills ? course.skills.split(';').map((skill) => skill.trim()).filter(Boolean).slice(0, 4) : [];

  return (
    <div
      onClick={onSelect}
      className={`group cursor-pointer rounded-[28px] border p-5 transition-all duration-300 ${
        isSelected
          ? 'border-cyan-400/80 bg-gradient-to-br from-slate-800 via-slate-900 to-slate-950 shadow-[0_30px_90px_rgba(34,211,238,0.18)] ring-1 ring-cyan-400/50'
          : 'border-slate-700/80 bg-slate-900/80 hover:border-cyan-500/60 hover:bg-slate-800/90 hover:shadow-[0_25px_70px_rgba(59,130,246,0.08)]'
      }`}
    >
      <div className="mb-3 flex items-start justify-between gap-3">
        <div>
          <p className="text-[10px] uppercase tracking-[0.22em] text-cyan-300">{course.organization || 'Organization'}</p>
          <h3 className="mt-2 text-xl font-semibold text-white">{course.course_name || 'Course'}</h3>
        </div>
        <div className="rounded-full border border-amber-400/40 bg-amber-500/10 px-2 py-1 text-[10px] font-medium uppercase tracking-[0.12em] text-amber-300">
          {course.difficulty || 'Unknown'}
        </div>
      </div>

      <p className="mb-4 line-clamp-4 text-sm leading-6 text-slate-300">{course.description || 'No description available.'}</p>

      <div className="mb-4 flex flex-wrap gap-2 text-xs text-slate-300">
        {skills.length > 0 ? skills.map((skill) => (
          <span key={skill} className="rounded-full border border-slate-700 bg-slate-800/90 px-2 py-1 text-slate-200">{skill}</span>
        )) : <span className="rounded-full border border-slate-700 bg-slate-800/90 px-2 py-1 text-slate-400">Skills not specified</span>}
      </div>

      <div className="mb-4 flex items-center justify-between text-sm text-slate-300">
        <div className="flex items-center gap-1">
          <Star size={14} className="fill-amber-400 text-amber-400" />
          <span>{course.rating ?? 'N/A'}</span>
        </div>
        <div className="flex items-center gap-2">
          {onExplain && (
            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                onExplain(course);
              }}
              className="inline-flex items-center gap-1 rounded-full border border-cyan-500/30 bg-cyan-500/10 px-2.5 py-0.5 text-[11px] font-semibold text-cyan-300 hover:bg-cyan-500/20 transition"
              title="Inspect Why Recommended"
            >
              <Sparkles size={11} /> Why?
            </button>
          )}
          <span className="font-semibold text-cyan-300">{course.final_score ? (course.final_score * 100).toFixed(0) + '%' : 'Matched'}</span>
        </div>
      </div>

      <div className="flex items-center justify-between">
        <Link
          to={`/course/${course.course_id ?? ''}`}
          onClick={(e) => e.stopPropagation()}
          className="inline-flex items-center gap-2 text-sm font-medium text-cyan-300 transition group-hover:text-cyan-200"
        >
          View course <ArrowRight size={16} />
        </Link>
        {course.url ? (
          <a href={course.url} target="_blank" rel="noreferrer" onClick={(e) => e.stopPropagation()} className="text-xs text-slate-400 underline transition hover:text-slate-200">Open link</a>
        ) : null}
      </div>
    </div>
  );
}
