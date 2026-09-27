import { Filter, RotateCcw, SlidersHorizontal, Star } from 'lucide-react';
import { FilterOptions } from '../types';

type Props = {
  filters: FilterOptions;
  onChange: (filters: FilterOptions) => void;
  availableOrganizations?: string[];
  totalCoursesCount?: number;
};

export default function FilterPanel({
  filters,
  onChange,
  availableOrganizations = [],
  totalCoursesCount,
}: Props) {
  const difficulties = ['All', 'Beginner', 'Intermediate', 'Advanced'];
  const ratingThresholds = [
    { label: 'All Ratings', value: 0 },
    { label: '4.0+ Stars', value: 4.0 },
    { label: '4.5+ Stars', value: 4.5 },
    { label: '4.8+ Stars', value: 4.8 },
  ];

  const handleDifficultyChange = (diff: string) => {
    onChange({
      ...filters,
      difficulty: diff === 'All' ? undefined : diff,
    });
  };

  const handleRatingChange = (rating: number) => {
    onChange({
      ...filters,
      minRating: rating === 0 ? undefined : rating,
    });
  };

  const handleReset = () => {
    onChange({});
  };

  const hasActiveFilters = Boolean(
    filters.difficulty ||
    filters.minRating ||
    filters.organization ||
    filters.searchKeyword
  );

  return (
    <div className="rounded-3xl border border-white/10 bg-slate-900/70 p-5 shadow-[0_20px_50px_rgba(15,23,42,0.4)] backdrop-blur-xl">
      <div className="mb-4 flex items-center justify-between">
        <div className="flex items-center gap-2 text-sm font-semibold text-white">
          <SlidersHorizontal size={16} className="text-cyan-400" />
          <span>Refine Recommendations</span>
          {totalCoursesCount !== undefined && (
            <span className="rounded-full bg-slate-800 px-2 py-0.5 text-xs text-slate-400">
              {totalCoursesCount} courses
            </span>
          )}
        </div>
        {hasActiveFilters && (
          <button
            onClick={handleReset}
            className="flex items-center gap-1 text-xs text-cyan-400 hover:text-cyan-300 transition"
          >
            <RotateCcw size={12} />
            Reset
          </button>
        )}
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {/* Difficulty */}
        <div>
          <label className="mb-2 block text-xs font-medium uppercase tracking-wider text-slate-400">
            Difficulty Level
          </label>
          <div className="flex flex-wrap gap-1.5">
            {difficulties.map((diff) => {
              const active = (!filters.difficulty && diff === 'All') || filters.difficulty === diff;
              return (
                <button
                  key={diff}
                  type="button"
                  onClick={() => handleDifficultyChange(diff)}
                  className={`rounded-full px-3 py-1 text-xs font-medium transition ${
                    active
                      ? 'border border-cyan-400/50 bg-cyan-500/20 text-cyan-200 shadow-[0_0_12px_rgba(34,211,238,0.25)]'
                      : 'border border-slate-700 bg-slate-800/80 text-slate-300 hover:border-slate-600 hover:text-white'
                  }`}
                >
                  {diff}
                </button>
              );
            })}
          </div>
        </div>

        {/* Minimum Rating */}
        <div>
          <label className="mb-2 block text-xs font-medium uppercase tracking-wider text-slate-400">
            Minimum Rating
          </label>
          <div className="flex flex-wrap gap-1.5">
            {ratingThresholds.map((t) => {
              const active = (!filters.minRating && t.value === 0) || filters.minRating === t.value;
              return (
                <button
                  key={t.value}
                  type="button"
                  onClick={() => handleRatingChange(t.value)}
                  className={`flex items-center gap-1 rounded-full px-3 py-1 text-xs font-medium transition ${
                    active
                      ? 'border border-amber-400/50 bg-amber-500/20 text-amber-200 shadow-[0_0_12px_rgba(251,191,36,0.2)]'
                      : 'border border-slate-700 bg-slate-800/80 text-slate-300 hover:border-slate-600 hover:text-white'
                  }`}
                >
                  {t.value > 0 && <Star size={10} className="fill-amber-400 text-amber-400" />}
                  {t.label}
                </button>
              );
            })}
          </div>
        </div>

        {/* Organization / Keyword Filter */}
        <div>
          <label className="mb-2 block text-xs font-medium uppercase tracking-wider text-slate-400">
            Institution / Keyword
          </label>
          <input
            type="text"
            value={filters.searchKeyword || ''}
            onChange={(e) => onChange({ ...filters, searchKeyword: e.target.value })}
            placeholder="e.g. Stanford, Google, IBM..."
            className="w-full rounded-xl border border-slate-700 bg-slate-950/80 px-3 py-1.5 text-xs text-white placeholder-slate-500 outline-none transition focus:border-cyan-400 focus:ring-1 focus:ring-cyan-500/30"
          />
        </div>
      </div>
    </div>
  );
}
