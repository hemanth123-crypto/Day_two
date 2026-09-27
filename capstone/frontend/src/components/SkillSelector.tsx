import { Plus, X } from 'lucide-react';
import { useState } from 'react';

type Props = {
  selectedSkills: string[];
  onChange: (skills: string[]) => void;
  popularSkills?: string[];
  label?: string;
};

const DEFAULT_POPULAR = [
  'Python', 'SQL', 'Java', 'Machine Learning', 'Pandas', 'Statistics',
  'Deep Learning', 'Cloud Computing', 'AWS', 'Data Analysis', 'Docker', 'Git'
];

export default function SkillSelector({
  selectedSkills,
  onChange,
  popularSkills = DEFAULT_POPULAR,
  label = "Select or Type Skills",
}: Props) {
  const [customInput, setCustomInput] = useState('');

  const addSkill = (skill: string) => {
    const trimmed = skill.trim();
    if (!trimmed) return;
    if (!selectedSkills.some((s) => s.toLowerCase() === trimmed.toLowerCase())) {
      onChange([...selectedSkills, trimmed]);
    }
    setCustomInput('');
  };

  const removeSkill = (skillToRemove: string) => {
    onChange(selectedSkills.filter((s) => s !== skillToRemove));
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      addSkill(customInput);
    }
  };

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <label className="text-xs font-semibold uppercase tracking-wider text-slate-300">
          {label}
        </label>
        {selectedSkills.length > 0 && (
          <button
            type="button"
            onClick={() => onChange([])}
            className="text-[11px] text-slate-400 hover:text-cyan-300 transition"
          >
            Clear all ({selectedSkills.length})
          </button>
        )}
      </div>

      {/* Selected skill chips */}
      {selectedSkills.length > 0 && (
        <div className="flex flex-wrap gap-1.5 p-2 rounded-2xl border border-cyan-500/20 bg-slate-950/60">
          {selectedSkills.map((skill) => (
            <span
              key={skill}
              className="inline-flex items-center gap-1.5 rounded-full border border-cyan-400/40 bg-cyan-500/15 px-3 py-1 text-xs font-medium text-cyan-200 shadow-sm"
            >
              {skill}
              <button
                type="button"
                onClick={() => removeSkill(skill)}
                className="text-cyan-400 hover:text-white transition"
              >
                <X size={12} />
              </button>
            </span>
          ))}
        </div>
      )}

      {/* Input for custom skill */}
      <div className="flex gap-2">
        <input
          type="text"
          value={customInput}
          onChange={(e) => setCustomInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Add a skill (e.g. Scikit-learn, React, Kubernetes)..."
          className="flex-1 rounded-xl border border-slate-700 bg-slate-950/80 px-3.5 py-2 text-xs text-white placeholder-slate-500 outline-none transition focus:border-cyan-400 focus:ring-1 focus:ring-cyan-500/30"
        />
        <button
          type="button"
          onClick={() => addSkill(customInput)}
          disabled={!customInput.trim()}
          className="flex items-center gap-1 rounded-xl bg-slate-800 px-3.5 py-2 text-xs font-semibold text-cyan-300 transition hover:bg-slate-700 disabled:opacity-40"
        >
          <Plus size={14} />
          Add
        </button>
      </div>

      {/* Quick-add popular suggestions */}
      <div>
        <span className="text-[10px] uppercase tracking-wider text-slate-400 block mb-1.5">
          Popular suggestions:
        </span>
        <div className="flex flex-wrap gap-1">
          {popularSkills.map((skill) => {
            const isSelected = selectedSkills.some((s) => s.toLowerCase() === skill.toLowerCase());
            return (
              <button
                key={skill}
                type="button"
                onClick={() => (isSelected ? removeSkill(skill) : addSkill(skill))}
                className={`rounded-lg px-2.5 py-1 text-[11px] font-medium transition ${
                  isSelected
                    ? 'border border-cyan-400 bg-cyan-500/20 text-cyan-200'
                    : 'border border-slate-800 bg-slate-900/60 text-slate-400 hover:border-slate-700 hover:text-slate-200'
                }`}
              >
                {isSelected ? '✓ ' : '+ '}
                {skill}
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
