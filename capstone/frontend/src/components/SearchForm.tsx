import { Search } from 'lucide-react';
import { FormEvent, useState } from 'react';

type Props = {
  onSubmit: (query: string) => void;
  initialValue?: string;
  loading?: boolean;
};

export default function SearchForm({ onSubmit, initialValue = '', loading = false }: Props) {
  const [query, setQuery] = useState(initialValue);

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    if (query.trim()) onSubmit(query.trim());
  };

  return (
    <form onSubmit={handleSubmit} className="w-full rounded-[32px] border border-white/10 bg-slate-900/75 p-3 shadow-[0_35px_120px_rgba(14,165,233,0.12)] backdrop-blur-xl">
      <div className="flex flex-col gap-3 md:flex-row md:items-center">
        <div className="relative flex-1">
          <Search size={18} className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-cyan-300" />
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Describe your learning goal..."
            className="w-full rounded-[22px] border border-slate-700 bg-slate-950/90 py-4 pl-12 pr-4 text-base text-slate-100 shadow-inner shadow-slate-950/80 outline-none transition focus:border-cyan-400 focus:ring-2 focus:ring-cyan-500/30 placeholder:text-slate-500"
          />
        </div>
        <button
          type="submit"
          disabled={loading || !query.trim()}
          className="inline-flex items-center justify-center gap-2 rounded-[22px] bg-gradient-to-r from-cyan-400 via-sky-500 to-violet-500 px-5 py-4 font-semibold text-slate-950 shadow-[0_18px_40px_rgba(34,211,238,0.35)] transition hover:scale-[1.01] hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-50"
        >
          <Search size={18} />
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>
    </form>
  );
}
