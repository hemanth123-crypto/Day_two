import { Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import CourseDetailPage from './pages/CourseDetailPage';
import CoursesExplorerPage from './pages/CoursesExplorerPage';
import DashboardPage from './pages/DashboardPage';
import HomePage from './pages/HomePage';
import LearningPathPage from './pages/LearningPathPage';
import ResultsPage from './pages/ResultsPage';
import SkillGapPage from './pages/SkillGapPage';
import EvaluationPage from './pages/EvaluationPage';

export default function App() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <Navbar />
      <main className="flex-1">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/results" element={<ResultsPage />} />
          <Route path="/skills" element={<SkillGapPage />} />
          <Route path="/learning-path" element={<LearningPathPage />} />
          <Route path="/evaluation" element={<EvaluationPage />} />
          <Route path="/explorer" element={<CoursesExplorerPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/course/:courseId" element={<CourseDetailPage />} />
        </Routes>
      </main>
      <footer className="border-t border-white/5 bg-slate-950/90 py-6 text-center text-xs text-slate-500">
        <div className="mx-auto max-w-7xl px-6 flex flex-col sm:flex-row items-center justify-between gap-3">
          <p>© 2026 University Course Finder — Intelligent Course Discovery & Learning Path Engine</p>
          <p className="text-cyan-400/80">Built with FastAPI • FAISS Vector Engine • React • Tailwind</p>
        </div>
      </footer>
    </div>
  );
}
