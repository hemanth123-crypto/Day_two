import { ChevronLeft, ChevronRight, Filter, Search, SlidersHorizontal } from 'lucide-react';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import CourseCard from '../components/CourseCard';
import EmptyState from '../components/EmptyState';
import LoadingState from '../components/LoadingState';
import api from '../services/api';
import { Course } from '../types';

export default function CoursesExplorerPage() {
  const navigate = useNavigate();
  const [courses, setCourses] = useState<Course[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pageSize] = useState(12);
  const [search, setSearch] = useState('');
  const [difficulty, setDifficulty] = useState('All');
  const [loading, setLoading] = useState(false);

  const loadCourses = async () => {
    setLoading(true);
    try {
      const params: any = {
        page,
        page_size: pageSize,
      };
      if (difficulty !== 'All') {
        params.difficulty = difficulty;
      }
      if (search.trim()) {
        params.search = search.trim();
      }

      const response = await api.get('/courses', { params });
      setCourses(response.data.courses || []);
      setTotal(response.data.total || 0);
    } catch (e) {
      setCourses([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCourses();
  }, [page, difficulty]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(1);
    loadCourses();
  };

  const totalPages = Math.ceil(total / pageSize) || 1;

  return (
    <div className="min-h-screen bg-slate-950 px-4 py-10 sm:px-8 text-slate-100">
      <div className="mx-auto max-w-7xl space-y-8">
        <div>
          <h1 className="text-3xl sm:text-4xl font-black text-white">Course Knowledge Base</h1>
          <p className="mt-1 text-sm text-slate-400">
            Browse, filter, and explore all 884 verified online university courses currently indexed in the vector database.
          </p>
        </div>

        {/* Filter & Search Bar */}
        <div className="rounded-3xl border border-white/10 bg-slate-900/70 p-5 backdrop-blur-xl">
          <form onSubmit={handleSearchSubmit} className="flex flex-col gap-3 md:flex-row md:items-center">
            <div className="relative flex-1">
              <Search size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-cyan-400" />
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search course title, skills, or curriculum descriptions..."
                className="w-full rounded-2xl border border-slate-700 bg-slate-950/80 py-3 pl-11 pr-4 text-xs text-white placeholder-slate-500 outline-none focus:border-cyan-400"
              />
            </div>

            <div className="flex items-center gap-2">
              <div className="flex rounded-2xl border border-slate-700 bg-slate-950/80 p-1">
                {['All', 'Beginner', 'Intermediate', 'Advanced'].map((diff) => (
                  <button
                    key={diff}
                    type="button"
                    onClick={() => {
                      setDifficulty(diff);
                      setPage(1);
                    }}
                    className={`rounded-xl px-3 py-1.5 text-xs font-semibold transition ${
                      difficulty === diff
                        ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/30'
                        : 'text-slate-400 hover:text-white'
                    }`}
                  >
                    {diff}
                  </button>
                ))}
              </div>

              <button
                type="submit"
                className="rounded-2xl bg-cyan-500 px-5 py-3 text-xs font-bold text-slate-950 hover:bg-cyan-400 transition"
              >
                Search
              </button>
            </div>
          </form>
        </div>

        {/* Courses Grid */}
        {loading ? (
          <LoadingState message="Loading Courses..." submessage="Filtering through Coursera curriculum catalogue..." />
        ) : courses.length === 0 ? (
          <EmptyState
            title="No courses match your filter"
            description="Try changing the difficulty filter or clearing the search box."
            actionText="Reset filters"
            onAction={() => {
              setSearch('');
              setDifficulty('All');
              setPage(1);
            }}
          />
        ) : (
          <div className="space-y-6">
            <div className="flex items-center justify-between text-xs text-slate-400">
              <span>Showing {(page - 1) * pageSize + 1} - {Math.min(page * pageSize, total)} of {total} courses</span>
              <span>Page {page} of {totalPages}</span>
            </div>

            <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
              {courses.map((course) => (
                <CourseCard
                  key={course.course_id}
                  course={course}
                  onSelect={() => navigate(`/course/${course.course_id}`)}
                />
              ))}
            </div>

            {/* Pagination Controls */}
            <div className="flex items-center justify-center gap-3 pt-6 border-t border-slate-800">
              <button
                type="button"
                onClick={() => setPage((p) => Math.max(p - 1, 1))}
                disabled={page <= 1}
                className="flex items-center gap-1 rounded-xl border border-slate-800 bg-slate-900 px-4 py-2 text-xs font-medium text-slate-300 hover:border-slate-700 disabled:opacity-40"
              >
                <ChevronLeft size={16} /> Previous
              </button>

              <span className="text-xs text-slate-400 font-medium">
                Page <strong className="text-white">{page}</strong> of {totalPages}
              </span>

              <button
                type="button"
                onClick={() => setPage((p) => Math.min(p + 1, totalPages))}
                disabled={page >= totalPages}
                className="flex items-center gap-1 rounded-xl border border-slate-800 bg-slate-900 px-4 py-2 text-xs font-medium text-slate-300 hover:border-slate-700 disabled:opacity-40"
              >
                Next <ChevronRight size={16} />
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
