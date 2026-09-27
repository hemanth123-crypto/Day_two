import { CheckCircle2, MessageSquare, Send, Star, ThumbsDown, ThumbsUp } from 'lucide-react';
import { useState } from 'react';
import api from '../services/api';

type Props = {
  courseId?: string;
  courseName?: string;
  onSuccess?: () => void;
  className?: string;
};

export default function FeedbackForm({ courseId, courseName, onSuccess, className = '' }: Props) {
  const [rating, setRating] = useState<number>(5);
  const [hoverRating, setHoverRating] = useState<number>(0);
  const [useful, setUseful] = useState<boolean>(true);
  const [comment, setComment] = useState<string>('');
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [submitted, setSubmitted] = useState<boolean>(false);
  const [error, setError] = useState<string>('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');

    try {
      await api.post('/feedback', {
        course_id: courseId || null,
        rating,
        useful,
        comment: comment.trim() || undefined,
      });
      setSubmitted(true);
      if (onSuccess) onSuccess();
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Failed to submit feedback. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  if (submitted) {
    return (
      <div className={`rounded-2xl border border-emerald-500/30 bg-emerald-950/20 p-5 text-center ${className}`}>
        <CheckCircle2 size={32} className="mx-auto mb-2 text-emerald-400" />
        <h4 className="text-base font-semibold text-white">Thank you for your feedback!</h4>
        <p className="mt-1 text-xs text-slate-300">
          Your input has been recorded to improve future recommendations.
        </p>
        <button
          type="button"
          onClick={() => {
            setSubmitted(false);
            setComment('');
          }}
          className="mt-3 inline-flex text-xs font-medium text-cyan-400 hover:text-cyan-300 underline"
        >
          Submit another feedback
        </button>
      </div>
    );
  }

  return (
    <form
      onSubmit={handleSubmit}
      className={`rounded-2xl border border-white/10 bg-slate-900/80 p-5 shadow-inner backdrop-blur-xl ${className}`}
    >
      <div className="mb-4">
        <h4 className="text-sm font-semibold uppercase tracking-wider text-cyan-400">
          Course & Recommendation Feedback
        </h4>
        {courseName && (
          <p className="mt-1 text-xs text-slate-400 truncate">Feedback for: {courseName}</p>
        )}
      </div>

      {error && (
        <div className="mb-3 rounded-lg border border-red-500/30 bg-red-950/30 p-2.5 text-xs text-red-200">
          {error}
        </div>
      )}

      {/* Star Rating */}
      <div className="mb-4">
        <label className="mb-1.5 block text-xs font-medium text-slate-300">
          How relevant was this recommendation?
        </label>
        <div className="flex items-center gap-1">
          {[1, 2, 3, 4, 5].map((star) => (
            <button
              key={star}
              type="button"
              onClick={() => setRating(star)}
              onMouseEnter={() => setHoverRating(star)}
              onMouseLeave={() => setHoverRating(0)}
              className="p-1 transition hover:scale-110"
              title={`${star} star${star > 1 ? 's' : ''}`}
            >
              <Star
                size={22}
                className={
                  (hoverRating || rating) >= star
                    ? 'fill-amber-400 text-amber-400 drop-shadow-[0_0_8px_rgba(251,191,36,0.5)]'
                    : 'text-slate-600 hover:text-slate-500'
                }
              />
            </button>
          ))}
          <span className="ml-2 text-xs font-semibold text-amber-300">
            {rating} of 5 Stars
          </span>
        </div>
      </div>

      {/* Useful Toggle */}
      <div className="mb-4">
        <label className="mb-1.5 block text-xs font-medium text-slate-300">
          Was this recommendation useful?
        </label>
        <div className="flex gap-2">
          <button
            type="button"
            onClick={() => setUseful(true)}
            className={`flex items-center gap-1.5 rounded-xl border px-3 py-1.5 text-xs font-medium transition ${
              useful
                ? 'border-emerald-400 bg-emerald-500/20 text-emerald-300 shadow-[0_0_12px_rgba(52,211,153,0.3)]'
                : 'border-slate-700 bg-slate-800 text-slate-400 hover:text-white'
            }`}
          >
            <ThumbsUp size={14} />
            Useful
          </button>
          <button
            type="button"
            onClick={() => setUseful(false)}
            className={`flex items-center gap-1.5 rounded-xl border px-3 py-1.5 text-xs font-medium transition ${
              !useful
                ? 'border-rose-400 bg-rose-500/20 text-rose-300 shadow-[0_0_12px_rgba(244,63,94,0.3)]'
                : 'border-slate-700 bg-slate-800 text-slate-400 hover:text-white'
            }`}
          >
            <ThumbsDown size={14} />
            Not Useful
          </button>
        </div>
      </div>

      {/* Comment Field */}
      <div className="mb-4">
        <label className="mb-1.5 block text-xs font-medium text-slate-300">
          Comments / Suggestions (Optional)
        </label>
        <textarea
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          rows={2}
          placeholder="Share your thoughts to help us improve course matching..."
          className="w-full rounded-xl border border-slate-700 bg-slate-950/80 p-2.5 text-xs text-slate-200 placeholder-slate-500 outline-none transition focus:border-cyan-400 focus:ring-1 focus:ring-cyan-500/30 resize-none"
        />
      </div>

      <button
        type="submit"
        disabled={submitting}
        className="flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-cyan-400 to-violet-500 px-4 py-2 text-xs font-semibold text-slate-950 shadow-[0_4px_16px_rgba(34,211,238,0.3)] transition hover:brightness-110 disabled:opacity-50"
      >
        <Send size={13} />
        {submitting ? 'Submitting...' : 'Submit Feedback'}
      </button>
    </form>
  );
}
