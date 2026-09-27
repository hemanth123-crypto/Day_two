import { ArrowLeft, BookOpen, ExternalLink, Star } from 'lucide-react';
import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import FeedbackForm from '../components/FeedbackForm';
import LoadingState from '../components/LoadingState';
import api from '../services/api';
import { Course } from '../types';

export default function CourseDetailPage() {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const [course, setCourse] = useState<Course | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    const loadCourse = async () => {
      setLoading(true);
      setError('');
      try {
        const response = await api.get(`/courses/${courseId}`);
        setCourse(response.data);
      } catch (err: any) {
        setError(err?.response?.data?.detail || 'Unable to load course details. The course may not exist.');
      } finally {
        setLoading(false);
      }
    };
    if (courseId) {
      loadCourse();
    }
  }, [courseId]);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 px-6 py-12 text-slate-100">
        <LoadingState message="Fetching Course Metadata..." submessage="Accessing university curriculum records..." />
      </div>
    );
  }

  if (error || !course) {
    return (
      <div className="min-h-screen bg-slate-950 px-6 py-12 text-slate-100 flex items-center justify-center">
        <div className="rounded-3xl border border-red-500/30 bg-red-950/20 p-8 text-center max-w-md">
          <h2 className="text-xl font-bold text-white">Course Not Found</h2>
          <p className="mt-2 text-xs text-red-200">{error || 'Requested course is missing from the dataset.'}</p>
          <button
            onClick={() => navigate(-1)}
            className="mt-6 inline-flex items-center gap-1.5 rounded-xl bg-slate-800 px-4 py-2 text-xs font-semibold text-cyan-300 hover:bg-slate-700"
          >
            <ArrowLeft size={14} /> Go Back
          </button>
        </div>
      </div>
    );
  }

  const skillsList = course.skills
    ? course.skills.split(';').map((s) => s.trim()).filter(Boolean)
    : [];

  return (
    <div className="min-h-screen bg-slate-950 px-6 py-10 text-slate-100">
      <div className="mx-auto max-w-5xl space-y-6">
        <button
          onClick={() => navigate(-1)}
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-cyan-400 hover:text-cyan-300 transition"
        >
          <ArrowLeft size={14} /> Back to results
        </button>

        <div className="rounded-3xl border border-white/10 bg-slate-900/80 p-8 shadow-2xl backdrop-blur-2xl">
          <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-cyan-400">
                {course.organization || 'University Partner'}
              </span>
              <h1 className="mt-1 text-3xl font-black text-white">{course.course_name}</h1>
            </div>
            <span className="rounded-full border border-cyan-400/40 bg-cyan-500/10 px-4 py-1.5 text-xs font-semibold uppercase tracking-wider text-cyan-300">
              {course.difficulty || 'Intermediate'}
            </span>
          </div>

          {/* Quick Metrics */}
          <div className="mt-6 grid grid-cols-2 gap-4 sm:grid-cols-4">
            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
              <span className="block text-[10px] uppercase tracking-wider text-slate-400">Rating</span>
              <div className="mt-1 flex items-center gap-1.5 text-lg font-bold text-amber-300">
                <Star size={16} className="fill-amber-400 text-amber-400" />
                {course.rating ? `${course.rating} / 5.0` : 'N/A'}
              </div>
            </div>

            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
              <span className="block text-[10px] uppercase tracking-wider text-slate-400">Institution</span>
              <span className="mt-1 block text-sm font-semibold text-white truncate">
                {course.organization || 'Coursera'}
              </span>
            </div>

            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
              <span className="block text-[10px] uppercase tracking-wider text-slate-400">Difficulty</span>
              <span className="mt-1 block text-sm font-semibold text-cyan-300">
                {course.difficulty || 'Unknown'}
              </span>
            </div>

            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
              <span className="block text-[10px] uppercase tracking-wider text-slate-400">Course ID</span>
              <span className="mt-1 block text-sm font-mono text-slate-400 truncate">
                {course.course_id}
              </span>
            </div>
          </div>

          <div className="mt-8 grid gap-8 lg:grid-cols-[1.5fr_1fr]">
            <div className="space-y-6">
              {/* Description */}
              <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-6">
                <h3 className="text-base font-bold text-white mb-2">Description & Syllabus</h3>
                <p className="text-xs leading-relaxed text-slate-300">
                  {course.description ||
                    `This course introduces learners to the core ideas, foundational methods, and practical applications of this subject through guided study and applied examples.`}
                </p>
              </div>

              {/* Skills */}
              {skillsList.length > 0 && (
                <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-6">
                  <h3 className="text-base font-bold text-white mb-3">Target Skills & Competencies</h3>
                  <div className="flex flex-wrap gap-2">
                    {skillsList.map((skill) => (
                      <span
                        key={skill}
                        className="rounded-xl border border-slate-700 bg-slate-800/90 px-3 py-1.5 text-xs text-slate-200"
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
                  className="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-cyan-400 via-sky-500 to-violet-500 px-6 py-3 text-xs font-semibold text-slate-950 shadow-xl shadow-cyan-500/20 hover:brightness-110 transition"
                >
                  <BookOpen size={16} />
                  <span>Go to Coursera Official Course</span>
                  <ExternalLink size={14} />
                </a>
              )}
            </div>

            {/* Interactive Feedback Form */}
            <div>
              <FeedbackForm
                courseId={course.course_id}
                courseName={course.course_name}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
