import { ArrowUpDown, Grid, LayoutList } from 'lucide-react';
import { useState } from 'react';
import { Course } from '../types';
import CourseCard from './CourseCard';
import EmptyState from './EmptyState';

type Props = {
  courses: Course[];
  selectedCourseId?: string;
  onSelectCourse: (course: Course) => void;
  onExplainCourse?: (course: Course) => void;
  title?: string;
};

export default function CourseGrid({
  courses,
  selectedCourseId,
  onSelectCourse,
  onExplainCourse,
  title = "Recommended Courses",
}: Props) {
  const [sortBy, setSortBy] = useState<'score' | 'rating' | 'name'>('score');

  const sortedCourses = [...courses].sort((a, b) => {
    if (sortBy === 'score') {
      return (b.final_score || 0) - (a.final_score || 0);
    }
    if (sortBy === 'rating') {
      return (b.rating || 0) - (a.rating || 0);
    }
    return (a.course_name || '').localeCompare(b.course_name || '');
  });

  if (courses.length === 0) {
    return <EmptyState title="No matching courses" description="No courses met your criteria." />;
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
        <h3 className="text-xl font-bold text-white">{title} ({courses.length})</h3>
        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-400">Sort by:</span>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as any)}
            className="rounded-xl border border-slate-700 bg-slate-900 px-3 py-1.5 text-xs text-slate-200 outline-none focus:border-cyan-400"
          >
            <option value="score">Relevance & Match Score</option>
            <option value="rating">Highest Rating</option>
            <option value="name">Course Title (A-Z)</option>
          </select>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {sortedCourses.map((course) => (
          <CourseCard
            key={course.course_id}
            course={course}
            isSelected={selectedCourseId === course.course_id}
            onSelect={() => onSelectCourse(course)}
            onExplain={onExplainCourse}
          />
        ))}
      </div>
    </div>
  );
}
