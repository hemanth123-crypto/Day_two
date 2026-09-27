import { Brain, CheckCircle2, ChevronRight, Sparkles, Target, Zap } from 'lucide-react';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import SkillGapPanel from '../components/SkillGapPanel';
import SkillSelector from '../components/SkillSelector';
import api from '../services/api';
import { Course, SkillGap } from '../types';

export default function SkillGapPage() {
  const navigate = useNavigate();
  const [currentSkills, setCurrentSkills] = useState<string[]>(['Python', 'SQL']);
  const [targetCareer, setTargetCareer] = useState<string>('Machine Learning Engineer');
  const [careers, setCareers] = useState<Array<{ career: string; required_skills: string[] }>>([]);
  const [skillGap, setSkillGap] = useState<SkillGap | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Fetch career list from API
  useEffect(() => {
    const loadCareers = async () => {
      try {
        const response = await api.get('/skills/careers');
        if (response.data && response.data.careers) {
          setCareers(response.data.careers);
        }
      } catch (e) {
        // Fallback default careers
        setCareers([
          { career: 'Data Scientist', required_skills: ['Python', 'SQL', 'Statistics', 'Pandas', 'Machine Learning'] },
          { career: 'Machine Learning Engineer', required_skills: ['Python', 'Machine Learning', 'Deep Learning', 'Scikit-learn', 'TensorFlow', 'Mathematics'] },
          { career: 'Data Analyst', required_skills: ['SQL', 'Excel', 'Python', 'Data Analysis', 'Tableau', 'Power BI'] },
          { career: 'Cloud Engineer', required_skills: ['Cloud Computing', 'AWS', 'Azure', 'Linux', 'Docker', 'Networking'] },
          { career: 'Software Developer', required_skills: ['Programming', 'Data Structures', 'Algorithms', 'Git', 'APIs', 'Databases'] },
        ]);
      }
    };
    loadCareers();
  }, []);

  const handleAnalyze = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await api.post('/skills/analyze', {
        current_skills: currentSkills,
        target_career: targetCareer,
      });
      setSkillGap(response.data);
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Failed to analyze skill gaps.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    handleAnalyze();
  }, [targetCareer]);

  return (
    <div className="min-h-screen bg-slate-950 px-4 py-10 sm:px-8 text-slate-100">
      <div className="mx-auto max-w-6xl space-y-8">
        <div>
          <div className="inline-flex items-center gap-2 rounded-full border border-violet-400/30 bg-violet-500/10 px-3.5 py-1 text-xs font-semibold text-violet-300">
            <Brain size={14} />
            Diagnostic Skill Engine
          </div>
          <h1 className="mt-2 text-3xl sm:text-4xl font-black text-white">
            Skill-Gap Analysis Studio
          </h1>
          <p className="mt-1 text-sm text-slate-400 max-w-2xl">
            Input your existing technical background and choose your target career. Our system compares your profile against industry competency models and pinpoints courses to eliminate every deficit.
          </p>
        </div>

        {/* Configuration Panel */}
        <div className="grid gap-6 lg:grid-cols-2">
          {/* Target Career Selection */}
          <div className="rounded-3xl border border-white/10 bg-slate-900/70 p-6 backdrop-blur-xl">
            <label className="block text-xs font-bold uppercase tracking-wider text-cyan-400 mb-3">
              Target Career Role
            </label>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              {careers.map((c) => {
                const isSelected = targetCareer === c.career;
                return (
                  <button
                    key={c.career}
                    type="button"
                    onClick={() => setTargetCareer(c.career)}
                    className={`rounded-2xl border p-3.5 text-left transition ${
                      isSelected
                        ? 'border-cyan-400 bg-cyan-500/15 text-white shadow-[0_0_20px_rgba(34,211,238,0.2)] ring-1 ring-cyan-400/50'
                        : 'border-slate-800 bg-slate-950/60 text-slate-300 hover:border-slate-700 hover:bg-slate-800/80'
                    }`}
                  >
                    <span className="block text-xs font-bold">{c.career}</span>
                    <span className="mt-1 block text-[10px] text-slate-400 truncate">
                      {c.required_skills.slice(0, 3).join(', ')}...
                    </span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Current Skills Selector */}
          <div className="rounded-3xl border border-white/10 bg-slate-900/70 p-6 backdrop-blur-xl space-y-4">
            <SkillSelector
              label="Your Current Technical Skills"
              selectedSkills={currentSkills}
              onChange={setCurrentSkills}
            />

            <button
              type="button"
              onClick={handleAnalyze}
              disabled={loading}
              className="w-full flex items-center justify-center gap-2 rounded-2xl bg-gradient-to-r from-cyan-400 to-violet-500 py-3 text-xs font-bold text-slate-950 shadow-lg shadow-cyan-500/20 hover:brightness-110 transition disabled:opacity-50"
            >
              <Zap size={15} />
              {loading ? 'Evaluating Competencies...' : 'Recalculate Skill Gap'}
            </button>
          </div>
        </div>

        {error && (
          <div className="rounded-2xl border border-red-500/30 bg-red-950/20 p-4 text-xs text-red-200">
            {error}
          </div>
        )}

        {/* Skill Gap Results */}
        {skillGap && (
          <div className="space-y-6">
            <SkillGapPanel
              currentSkills={skillGap.current_skills}
              missingSkills={skillGap.missing_skills}
              requiredSkills={skillGap.required_skills}
              coverage={skillGap.coverage_percentage}
              targetCareer={targetCareer}
              missingSkillsCourses={skillGap.missing_skills_courses}
              onSelectCourse={(course: Course) => navigate(`/course/${course.course_id}`)}
            />

            {/* Action to Generate Learning Path */}
            <div className="flex justify-end">
              <button
                type="button"
                onClick={() =>
                  navigate('/results', {
                    state: {
                      query: `I know ${currentSkills.join(' and ')} and want to become a ${targetCareer}`,
                    },
                  })
                }
                className="inline-flex items-center gap-2 rounded-2xl bg-gradient-to-r from-cyan-400 to-sky-500 px-6 py-3 text-xs font-bold text-slate-950 shadow-xl shadow-cyan-500/20 hover:brightness-110 transition"
              >
                <span>Generate Full Learning Path & Courses</span>
                <ChevronRight size={16} />
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
