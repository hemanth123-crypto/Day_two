import { ExternalLink, Star, X } from 'lucide-react';
import { Course } from '../types';
import FeedbackForm from './FeedbackForm';
import RecommendationExplanation from './RecommendationExplanation';

type Props = {
  course: Course;
  targetCareer?: string | null;
  onClose?: () => void;
  showFeedback?: boolean;
};

export default function CourseDetails({
  course,
  targetCareer,
  onClose,
  showFeedback = true,
}: Props) {
  const skillsList = course.skills
    ? course.skills.split(';').map((s) => s.trim()).filter(Boolean)
    : [];

  return (
    <div className="rounded-3xl border border-cyan-500/30 bg-slate-900/95 p-6 shadow-2xl backdrop-blur-2xl">
      <div className="flex items-start justify-between gap-4">
        <div>
          <span className="text-xs font-semibold uppercase tracking-wider text-cyan-400">
            {course.organization || 'Coursera Partner'}
          </span>
          <h2 className="mt-1 text-2xl font-bold text-white">{course.course_name}</h2>
          <div className="mt-2 flex flex-wrap items-center gap-3 text-xs text-slate-300">
            <span className="flex items-center gap-1 font-semibold text-amber-300">
              <Star size={13} className="fill-amber-400 text-amber-400" />
              {course.rating ? `${course.rating} / 5.0` : 'Unrated'}
            </span>
            <span>•</span>
            <span className="rounded-full bg-slate-800 px-2.5 py-0.5 text-cyan-300">
              {course.difficulty || 'Intermediate'} Level
            </span>
            {course.final_score !== undefined && (
              <>
                <span>•</span>
                <span className="font-bold text-emerald-400">
                  {Math.round(course.final_score * 100)}% Match Score
                </span>
              </>
            )}
          </div>
        </div>

        {onClose && (
          <button
            onClick={onClose}
            className="rounded-full bg-slate-800 p-2 text-slate-400 hover:bg-slate-700 hover:text-white transition"
          >
            <X size={18} />
          </button>
        )}
      </div>

      <div className="mt-6 grid gap-6 lg:grid-cols-[1.4fr_1fr]">
        <div className="space-y-5">
          {/* Recommendation Reason */}
          <RecommendationExplanation course={course} targetCareer={targetCareer} />

          {/* Description */}
          <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-5">
            <h3 className="text-sm font-semibold text-white">Course Overview</h3>
            <p className="mt-2 text-xs leading-relaxed text-slate-300">
              {course.description ||
                `This curriculum covers the core ideas, tools, and practical exercises behind ${course.course_name}. Designed to help learners develop practical competency through applied lessons and structured study.`}
            </p>
          </div>

          {/* Skills Covered */}
          {skillsList.length > 0 && (
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-5">
              <h3 className="text-sm font-semibold text-white">Skills You Will Learn</h3>
              <div className="mt-3 flex flex-wrap gap-2">
                {skillsList.map((skill) => (
                  <span
                    key={skill}
                    className="rounded-xl border border-slate-700 bg-slate-800/80 px-3 py-1 text-xs text-slate-200"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          )}

          {course.url && (
            <a
              href={course.url}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-cyan-400 to-sky-500 px-5 py-2.5 text-xs font-semibold text-slate-950 shadow-lg shadow-cyan-500/20 hover:brightness-110 transition"
            >
              <span>Enroll / View Course on Coursera</span>
              <ExternalLink size={14} />
            </a>
          )}
        </div>

        {/* Feedback Section */}
        {showFeedback && (
          <div>
            <FeedbackForm courseId={course.course_id} courseName={course.course_name} />
          </div>
        )}
      </div>
    </div>
  );
}
