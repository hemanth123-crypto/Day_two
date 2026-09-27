import { ArrowRight, Compass, Route, Sparkles } from 'lucide-react';
import { useEffect, useState } from 'react';
import LearningPathTimeline from '../components/LearningPathTimeline';
import LoadingState from '../components/LoadingState';
import SkillSelector from '../components/SkillSelector';
import api from '../services/api';
import { LearningPathStep } from '../types';

export default function LearningPathPage() {
  const [currentSkills, setCurrentSkills] = useState<string[]>(['Python', 'SQL']);
  const [targetCareer, setTargetCareer] = useState<string>('Machine Learning Engineer');
  const [steps, setSteps] = useState<LearningPathStep[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const careers = [
    'Machine Learning Engineer',
    'Data Scientist',
    'Data Analyst',
    'Cloud Engineer',
    'Software Developer',
    'Data Engineer',
  ];

  const generatePath = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await api.post('/learning-path', {
        current_skills: currentSkills,
        target_career: targetCareer,
      });
      if (response.data && response.data.path) {
        setSteps(response.data.path);
      }
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Failed to generate personalized learning path.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    generatePath();
  }, [targetCareer]);

  return (
    <div className="min-h-screen bg-slate-950 px-4 py-10 sm:px-8 text-slate-100">
      <div className="mx-auto max-w-6xl space-y-8">
        <div>
          <div className="inline-flex items-center gap-2 rounded-full border border-cyan-400/30 bg-cyan-500/10 px-3.5 py-1 text-xs font-semibold text-cyan-300">
            <Compass size={14} />
            Topological Sequence Studio
          </div>
          <h1 className="mt-2 text-3xl sm:text-4xl font-black text-white">
            Personalized Learning Path
          </h1>
          <p className="mt-1 text-sm text-slate-400 max-w-2xl">
            Education requires correct sequencing. This engine applies topological sorting to academic prerequisites to ensure you never take an advanced machine learning or cloud course before its mathematical or programming foundations.
          </p>
        </div>

        {/* Configuration Bar */}
        <div className="grid gap-6 lg:grid-cols-2">
          <div className="rounded-3xl border border-white/10 bg-slate-900/70 p-6 backdrop-blur-xl space-y-3">
            <label className="block text-xs font-bold uppercase tracking-wider text-cyan-400">
              Select Target Career Track
            </label>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
              {careers.map((career) => (
                <button
                  key={career}
                  type="button"
                  onClick={() => setTargetCareer(career)}
                  className={`rounded-2xl border p-3 text-center text-xs font-semibold transition ${
                    targetCareer === career
                      ? 'border-cyan-400 bg-cyan-500/20 text-cyan-200 shadow-[0_0_16px_rgba(34,211,238,0.25)]'
                      : 'border-slate-800 bg-slate-950/60 text-slate-400 hover:border-slate-700 hover:text-white'
                  }`}
                >
                  {career}
                </button>
              ))}
            </div>
          </div>

          <div className="rounded-3xl border border-white/10 bg-slate-900/70 p-6 backdrop-blur-xl space-y-4">
            <SkillSelector
              label="Skills You Already Have"
              selectedSkills={currentSkills}
              onChange={setCurrentSkills}
            />

            <button
              type="button"
              onClick={generatePath}
              disabled={loading}
              className="w-full rounded-2xl bg-gradient-to-r from-cyan-400 to-sky-500 py-3 text-xs font-bold text-slate-950 shadow-lg shadow-cyan-500/20 hover:brightness-110 transition disabled:opacity-50"
            >
              {loading ? 'Synthesizing Path...' : 'Re-sequence Learning Path'}
            </button>
          </div>
        </div>

        {error && (
          <div className="rounded-2xl border border-red-500/30 bg-red-950/20 p-4 text-xs text-red-200">
            {error}
          </div>
        )}

        {loading ? (
          <LoadingState message="Computing prerequisite graphs..." submessage="Executing topological sort across skill taxonomy..." />
        ) : (
          <div className="space-y-6">
            <div className="rounded-3xl border border-cyan-500/20 bg-slate-900/60 p-5 flex items-center justify-between">
              <div>
                <h3 className="text-lg font-bold text-white">Recommended Sequence for {targetCareer}</h3>
                <p className="text-xs text-slate-400">Total {steps.length} ordered progression milestones mapped to real Coursera courses</p>
              </div>
            </div>

            <LearningPathTimeline steps={steps} />
          </div>
        )}
      </div>
    </div>
  );
}
