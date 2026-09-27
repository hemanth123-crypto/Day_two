import { AlertCircle, RefreshCw } from 'lucide-react';

type Props = {
  message: string;
  onRetry?: () => void;
};

export default function ErrorState({ message, onRetry }: Props) {
  return (
    <div className="mx-auto max-w-lg rounded-3xl border border-red-500/30 bg-red-950/20 p-8 text-center backdrop-blur-xl shadow-2xl">
      <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-red-500/10 border border-red-500/20 text-red-400">
        <AlertCircle size={28} />
      </div>
      <h3 className="text-lg font-bold text-white">Something went wrong</h3>
      <p className="mt-2 text-sm text-red-200/80 leading-relaxed">{message}</p>
      {onRetry && (
        <button
          type="button"
          onClick={onRetry}
          className="mt-6 inline-flex items-center gap-2 rounded-xl bg-red-500/20 border border-red-500/30 px-5 py-2.5 text-xs font-semibold text-red-200 transition hover:bg-red-500/30"
        >
          <RefreshCw size={14} />
          Try Again
        </button>
      )}
    </div>
  );
}
