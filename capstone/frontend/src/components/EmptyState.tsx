import { BookOpen, Search } from 'lucide-react';

type Props = {
  title?: string;
  description?: string;
  actionText?: string;
  onAction?: () => void;
};

export default function EmptyState({
  title = "No courses found",
  description = "Try adjusting your search criteria, removing strict filters, or entering a broader learning goal.",
  actionText,
  onAction,
}: Props) {
  return (
    <div className="mx-auto max-w-md rounded-3xl border border-white/10 bg-slate-900/60 p-8 text-center backdrop-blur-xl">
      <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-cyan-500/10 border border-cyan-500/20 text-cyan-400">
        <Search size={26} />
      </div>
      <h3 className="text-lg font-bold text-white">{title}</h3>
      <p className="mt-2 text-sm text-slate-400 leading-relaxed">{description}</p>
      {actionText && onAction && (
        <button
          type="button"
          onClick={onAction}
          className="mt-6 inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-cyan-400 to-sky-500 px-5 py-2.5 text-xs font-semibold text-slate-950 transition hover:brightness-110 shadow-lg shadow-cyan-500/20"
        >
          <BookOpen size={14} />
          {actionText}
        </button>
      )}
    </div>
  );
}
