import { ArrowLeft, BookOpen, Brain, Compass, Filter, RefreshCw, ShieldCheck, Sparkles, Star, UserCheck } from 'lucide-react';
import { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import CourseDetails from '../components/CourseDetails';
import CourseGrid from '../components/CourseGrid';
import EmptyState from '../components/EmptyState';
import ErrorState from '../components/ErrorState';
import EvaluationModal from '../components/EvaluationModal';
import EvaluationPanel from '../components/EvaluationPanel';
import FilterPanel from '../components/FilterPanel';
import LearningPathTimeline from '../components/LearningPathTimeline';
import LoadingState from '../components/LoadingState';
import SearchForm from '../components/SearchForm';
import SkillGapPanel from '../components/SkillGapPanel';
import api from '../services/api';
import { Course, CourseEvaluation, EvaluationResponse, FilterOptions, RecommendationResponse } from '../types';

export default function ResultsPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const initialQuery = (location.state as { query?: string } | null)?.query || 'I know Python and SQL and want to become a machine learning engineer.';

  const [query, setQuery] = useState(initialQuery);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<RecommendationResponse | null>(null);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState<'courses' | 'skills' | 'path' | 'evaluation'>('courses');
  const [selectedCourse, setSelectedCourse] = useState<Course | null>(null);
  const [filters, setFilters] = useState<FilterOptions>({});
  const [evaluationData, setEvaluationData] = useState<EvaluationResponse | null>(null);
  const [evalLoading, setEvalLoading] = useState(false);
  const [modalEvaluation, setModalEvaluation] = useState<CourseEvaluation | null>(null);

  const fetchEvaluation = async (inputQuery: string, courseId?: string) => {
    setEvalLoading(true);
    try {
      const response = await api.post('/recommendations/evaluate', {
        query: inputQuery,
        course_id: courseId,
        top_k: 8,
      });
      setEvaluationData(response.data);
      return response.data;
    } catch (err: any) {
      console.error('Failed to load evaluation data', err);
    } finally {
      setEvalLoading(false);
    }
  };

  const handleExplainCourse = async (course: Course) => {
    setEvalLoading(true);
    try {
      const response = await api.post('/recommendations/evaluate', {
        query,
        course_id: course.course_id,
        top_k: 1,
      });
      if (response.data?.evaluations && response.data.evaluations.length > 0) {
        setModalEvaluation(response.data.evaluations[0]);
      }
    } catch (err) {
      console.error('Failed to explain course', err);
    } finally {
      setEvalLoading(false);
    }
  };

  const fetchResults = async (inputQuery: string, currentSkillsOverride?: string[]) => {
    if (!inputQuery.trim()) return;
    setLoading(true);
    setError('');
    setEvaluationData(null);

    try {
      const response = await api.post('/recommendations', {
        query: inputQuery,
        current_skills: currentSkillsOverride,
        top_k: 12,
      });

      const data: RecommendationResponse = response.data;
      setResult(data);
      if (data.recommendations && data.recommendations.length > 0) {
        setSelectedCourse(data.recommendations[0]);
      } else {
        setSelectedCourse(null);
      }

      if (activeTab === 'evaluation') {
        fetchEvaluation(inputQuery);
      }

      // Record to recent searches in localStorage for dashboard
      try {
        const history = JSON.parse(localStorage.getItem('ucf_search_history') || '[]');
        const newEntry = {
          query: inputQuery,
          career: data.query?.target_career || 'General',
          timestamp: new Date().toISOString(),
          resultsCount: data.recommendations?.length || 0,
        };
        const updated = [newEntry, ...history.filter((h: any) => h.query !== inputQuery)].slice(0, 15);
        localStorage.setItem('ucf_search_history', JSON.stringify(updated));
      } catch (e) {
        // Ignore localStorage error in private mode
      }
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Unable to retrieve course recommendations. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (initialQuery) {
      fetchResults(initialQuery);
    }
  }, [initialQuery]);

  const handleSearchSubmit = (newQuery: string) => {
    setQuery(newQuery);
    fetchResults(newQuery);
  };

  // Apply client-side filters on recommended courses
  const filteredCourses = (result?.recommendations || []).filter((course) => {
    if (filters.difficulty && course.difficulty?.toLowerCase() !== filters.difficulty.toLowerCase()) {
      return false;
    }
    if (filters.minRating && (course.rating || 0) < filters.minRating) {
      return false;
    }
    if (filters.searchKeyword && filters.searchKeyword.trim()) {
      const kw = filters.searchKeyword.toLowerCase().trim();
      const combined = `${course.course_name} ${course.organization} ${course.skills} ${course.description}`.toLowerCase();
      if (!combined.includes(kw)) {
        return false;
      }
    }
    return true;
  });

  return (
    <div className="min-h-screen bg-slate-950 px-4 py-8 sm:px-8 text-slate-100">
      <div className="mx-auto max-w-7xl space-y-8">
        {/* Navigation & Search header */}
        <div className="flex flex-col gap-4">
          <div className="flex items-center justify-between">
            <button
              onClick={() => navigate('/')}
              className="inline-flex items-center gap-1.5 text-xs font-semibold text-cyan-400 hover:text-cyan-300 transition"
            >
              <ArrowLeft size={14} /> Back to Search
            </button>
            <span className="text-xs text-slate-400">
              Session Query Mode: <strong className="text-cyan-300">Semantic & Vector Matching</strong>
            </span>
          </div>

          <SearchForm onSubmit={handleSearchSubmit} initialValue={query} loading={loading} />
        </div>

        {/* Loading State */}
        {loading && <LoadingState />}

        {/* Error State */}
        {error && !loading && (
          <ErrorState message={error} onRetry={() => fetchResults(query)} />
        )}

        {/* Results Body */}
        {result && !loading && (
          <div className="space-y-8">
            {/* Query Understanding Banner */}
            <div className="rounded-3xl border border-white/10 bg-gradient-to-r from-slate-900/90 via-slate-900/80 to-cyan-950/30 p-6 shadow-2xl backdrop-blur-xl">
              <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <Sparkles size={16} className="text-cyan-400" />
                    <span className="text-xs font-bold uppercase tracking-widest text-cyan-400">
                      Query Understanding Engine
                    </span>
                  </div>
                  <h2 className="mt-1 text-2xl font-bold text-white">"{query}"</h2>
                </div>

                <div className="flex flex-wrap items-center gap-2">
                  <div className="rounded-2xl border border-slate-700 bg-slate-800/80 px-4 py-2 text-xs">
                    <span className="text-slate-400 block text-[10px] uppercase tracking-wider">Target Career</span>
                    <strong className="text-cyan-300 text-sm">{result.query?.target_career || 'General Technical'}</strong>
                  </div>
                  <div className="rounded-2xl border border-slate-700 bg-slate-800/80 px-4 py-2 text-xs">
                    <span className="text-slate-400 block text-[10px] uppercase tracking-wider">Difficulty Level</span>
                    <strong className="text-violet-300 text-sm">{result.query?.difficulty || 'Adaptive'}</strong>
                  </div>
                  <div className="rounded-2xl border border-slate-700 bg-slate-800/80 px-4 py-2 text-xs">
                    <span className="text-slate-400 block text-[10px] uppercase tracking-wider">Readiness</span>
                    <strong className="text-emerald-300 text-sm">{Math.round(result.skill_gap?.coverage_percentage || 0)}%</strong>
                  </div>
                </div>
              </div>

              {/* Detected Existing Skills Pills */}
              <div className="mt-4 flex flex-wrap items-center gap-2 border-t border-slate-800/80 pt-3 text-xs text-slate-300">
                <span className="font-semibold text-slate-400">Detected Current Skills:</span>
                {result.query?.existing_skills && result.query.existing_skills.length > 0 ? (
                  result.query.existing_skills.map((s) => (
                    <span key={s} className="rounded-full bg-slate-800 border border-slate-700 px-2.5 py-0.5 text-cyan-200">
                      ✓ {s}
                    </span>
                  ))
                ) : (
                  <span className="text-slate-500 italic">None specified (starting from foundations)</span>
                )}
              </div>
            </div>

            {/* AI-Powered Answer Panel (RAG via OpenRouter LLM) */}
            {result.llm_answer && (
              <div className="rounded-3xl border border-violet-500/30 bg-gradient-to-br from-violet-950/40 via-slate-900/90 to-indigo-950/30 p-6 shadow-2xl backdrop-blur-xl">
                <div className="flex items-center gap-2 mb-3">
                  <div className="flex items-center justify-center w-8 h-8 rounded-full bg-violet-600/30 border border-violet-500/40">
                    <Sparkles size={16} className="text-violet-300" />
                  </div>
                  <div>
                    <span className="text-xs font-bold uppercase tracking-widest text-violet-400">
                      AI-Powered Advisor
                    </span>
                    <span className="ml-2 text-[10px] text-slate-500 font-medium">
                      Powered by OpenRouter LLM
                    </span>
                  </div>
                </div>
                <div className="prose prose-invert prose-sm max-w-none text-slate-200 leading-relaxed">
                  {result.llm_answer.split('\n').map((line, i) => {
                    const trimmed = line.trim();
                    if (!trimmed) return <br key={i} />;
                    if (trimmed.startsWith('### ')) {
                      return <h4 key={i} className="text-base font-bold text-violet-200 mt-4 mb-1">{trimmed.replace('### ', '')}</h4>;
                    }
                    if (trimmed.startsWith('**') && trimmed.endsWith('**')) {
                      return <p key={i} className="font-semibold text-white mt-2">{trimmed.replace(/\*\*/g, '')}</p>;
                    }
                    if (trimmed.startsWith('- ') || trimmed.startsWith('• ')) {
                      const content = trimmed.replace(/^[-•]\s*/, '');
                      // Bold text within list items
                      const parts = content.split(/(\*\*[^*]+\*\*)/g);
                      return (
                        <div key={i} className="flex items-start gap-2 ml-2 my-0.5">
                          <span className="text-violet-400 mt-0.5">•</span>
                          <span>
                            {parts.map((part, j) =>
                              part.startsWith('**') && part.endsWith('**')
                                ? <strong key={j} className="text-cyan-300">{part.replace(/\*\*/g, '')}</strong>
                                : <span key={j}>{part}</span>
                            )}
                          </span>
                        </div>
                      );
                    }
                    // Inline bold rendering for normal paragraphs
                    const parts = trimmed.split(/(\*\*[^*]+\*\*)/g);
                    return (
                      <p key={i} className="my-1">
                        {parts.map((part, j) =>
                          part.startsWith('**') && part.endsWith('**')
                            ? <strong key={j} className="text-cyan-300">{part.replace(/\*\*/g, '')}</strong>
                            : <span key={j}>{part}</span>
                        )}
                      </p>
                    );
                  })}
                </div>
              </div>
            )}

            {/* View Mode Navigation Tabs */}
            <div className="flex flex-wrap border-b border-slate-800 gap-2">
              <button
                type="button"
                onClick={() => setActiveTab('courses')}
                className={`flex items-center gap-2 px-5 py-3 text-sm font-semibold border-b-2 transition ${
                  activeTab === 'courses'
                    ? 'border-cyan-400 text-cyan-300'
                    : 'border-transparent text-slate-400 hover:text-slate-200'
                }`}
              >
                <BookOpen size={16} />
                Recommended Courses ({filteredCourses.length})
              </button>
              <button
                type="button"
                onClick={() => setActiveTab('skills')}
                className={`flex items-center gap-2 px-5 py-3 text-sm font-semibold border-b-2 transition ${
                  activeTab === 'skills'
                    ? 'border-cyan-400 text-cyan-300'
                    : 'border-transparent text-slate-400 hover:text-slate-200'
                }`}
              >
                <Brain size={16} />
                Skill Gap Analysis ({result.skill_gap?.missing_skills?.length || 0} gaps)
              </button>
              <button
                type="button"
                onClick={() => setActiveTab('path')}
                className={`flex items-center gap-2 px-5 py-3 text-sm font-semibold border-b-2 transition ${
                  activeTab === 'path'
                    ? 'border-cyan-400 text-cyan-300'
                    : 'border-transparent text-slate-400 hover:text-slate-200'
                }`}
              >
                <Compass size={16} />
                Personalized Learning Path ({result.learning_path?.length || 0} steps)
              </button>
              <button
                type="button"
                onClick={() => {
                  setActiveTab('evaluation');
                  if (!evaluationData) {
                    fetchEvaluation(query);
                  }
                }}
                className={`flex items-center gap-2 px-5 py-3 text-sm font-semibold border-b-2 transition ${
                  activeTab === 'evaluation'
                    ? 'border-cyan-400 text-cyan-300'
                    : 'border-transparent text-slate-400 hover:text-slate-200'
                }`}
              >
                <ShieldCheck size={16} />
                Evaluation & Rationale
              </button>
            </div>

            {/* TAB 1: Recommended Courses */}
            {activeTab === 'courses' && (
              <div className="space-y-6">
                {/* Filter Controls */}
                <FilterPanel
                  filters={filters}
                  onChange={setFilters}
                  totalCoursesCount={filteredCourses.length}
                />

                {/* Selected Course Quick View Modal / Card */}
                {selectedCourse && (
                  <div className="mb-6">
                    <CourseDetails
                      course={selectedCourse}
                      targetCareer={result.query?.target_career}
                      onClose={() => setSelectedCourse(null)}
                    />
                  </div>
                )}

                {/* Course Grid */}
                <CourseGrid
                  courses={filteredCourses}
                  selectedCourseId={selectedCourse?.course_id}
                  onSelectCourse={(course) => setSelectedCourse(course)}
                  onExplainCourse={handleExplainCourse}
                />
              </div>
            )}

            {/* TAB 2: Skill Gap Analysis */}
            {activeTab === 'skills' && (
              <div className="space-y-6">
                <SkillGapPanel
                  currentSkills={result.skill_gap?.current_skills || []}
                  missingSkills={result.skill_gap?.missing_skills || []}
                  requiredSkills={result.skill_gap?.required_skills || []}
                  coverage={result.skill_gap?.coverage_percentage || 0}
                  targetCareer={result.query?.target_career || undefined}
                  missingSkillsCourses={result.skill_gap?.missing_skills_courses}
                  onSelectCourse={(course) => {
                    setSelectedCourse(course);
                    setActiveTab('courses');
                  }}
                />
              </div>
            )}

            {/* TAB 3: Personalized Learning Path */}
            {activeTab === 'path' && (
              <div className="space-y-6">
                <div className="rounded-3xl border border-white/10 bg-slate-900/60 p-6 backdrop-blur-xl">
                  <h3 className="text-xl font-bold text-white mb-1">
                    Structured Curriculum for {result.query?.target_career || 'Target Career'}
                  </h3>
                  <p className="text-xs text-slate-400">
                    Sequenced using topological sort to guarantee each milestone satisfies all course and skill prerequisites.
                  </p>
                </div>

                <LearningPathTimeline steps={result.learning_path || []} />
              </div>
            )}

            {/* TAB 4: Evaluation & Rationale */}
            {activeTab === 'evaluation' && (
              <div className="space-y-6">
                <EvaluationPanel
                  evaluations={evaluationData?.evaluations || []}
                  targetCareer={evaluationData?.target_career || result.query?.target_career || undefined}
                  studentSkills={evaluationData?.student_skills || result.query?.existing_skills}
                  missingSkills={evaluationData?.missing_skills || result.skill_gap?.missing_skills}
                  coveragePct={evaluationData?.career_coverage_pct || result.skill_gap?.coverage_percentage}
                  loading={evalLoading}
                />
              </div>
            )}
          </div>
        )}

        {/* Modal for In-depth Course Evaluation */}
        <EvaluationModal
          isOpen={!!modalEvaluation}
          evaluation={modalEvaluation}
          onClose={() => setModalEvaluation(null)}
          targetCareer={result?.query?.target_career || undefined}
        />
      </div>
    </div>
  );
}
