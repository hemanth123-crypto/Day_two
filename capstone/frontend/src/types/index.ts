export type Course = {
  course_id: string;
  course_name: string;
  description?: string;
  difficulty?: string;
  rating?: number | null;
  organization?: string;
  url?: string;
  skills?: string;
  search_text?: string;
  semantic_score?: number;
  skill_score?: number;
  difficulty_score?: number;
  rating_score?: number;
  career_match_score?: number;
  semantic_norm?: number;
  skill_norm?: number;
  difficulty_norm?: number;
  rating_norm?: number;
  career_norm?: number;
  final_score?: number;
  explanation?: string;
  matched_skills?: string[];
};

export type ParsedQuery = {
  query: string;
  existing_skills: string[];
  target_career?: string | null;
  desired_skills: string[];
  weak_skills?: string[];
  difficulty?: string;
  domain?: string;
};

export type SkillGap = {
  current_skills: string[];
  required_skills: string[];
  existing_skills: string[];
  missing_skills: string[];
  coverage_percentage: number;
  target_career?: string;
  missing_skills_courses?: Record<string, Course[]>;
};

export type LearningPathStep = {
  order: number;
  course: string;
  course_id?: string;
  difficulty: string;
  skills: string[];
  prerequisites: string[];
  reason: string;
  url?: string;
  organization?: string;
  rating?: number | null;
};

export type RecommendationResponse = {
  query: ParsedQuery;
  skill_gap: SkillGap;
  recommendations: Course[];
  prerequisites: Record<string, string[]>;
  learning_path: LearningPathStep[];
  llm_answer?: string | null;
};

export type FeedbackSubmission = {
  course_id?: string | null;
  rating: number;
  useful: boolean;
  comment?: string;
};

export type FeedbackItem = {
  id: number;
  course_id?: string | null;
  rating: number;
  useful: boolean;
  comment?: string;
  created_at?: string;
};

export type FeedbackStats = {
  total_feedback: number;
  average_rating: number;
  usefulness_rate: number;
  rating_distribution: Record<number, number>;
  recent_feedback: FeedbackItem[];
};

export type FilterOptions = {
  difficulty?: string;
  minRating?: number;
  searchKeyword?: string;
  organization?: string;
};

export type FactorDetail = {
  name: string;
  weight: number;
  raw_score: number;
  normalized_score: number;
  points_contributed: number;
  percentage_of_final: number;
  explanation: string;
};

export type PrerequisiteReadiness = {
  status: 'READY' | 'MOSTLY_READY' | 'PREREQUISITES_RECOMMENDED';
  readiness_score: number;
  satisfied_prerequisites: string[];
  missing_prerequisites: string[];
  guidance: string;
};

export type CourseEvaluation = {
  course_id: string;
  course_name: string;
  organization: string;
  difficulty: string;
  rating?: number | null;
  final_score: number;
  rank: number;
  verdict: string;
  verdict_badge: string;
  prerequisite_readiness: PrerequisiteReadiness;
  factors: Record<string, FactorDetail>;
  closed_skill_gaps: string[];
  reinforced_skills: string[];
  key_strengths: string[];
  considerations: string[];
  detailed_justification: string;
};

export type EvaluationResponse = {
  query: string;
  target_career: string;
  student_skills: string[];
  missing_skills: string[];
  career_coverage_pct: number;
  evaluations: CourseEvaluation[];
  evaluation_methodology: {
    scoring_model: string;
    weights: Record<string, number>;
    prerequisite_reasoning: string;
    evaluation_metrics: Record<string, any>;
  };
};

export type EvaluationRequest = {
  query: string;
  current_skills?: string[];
  target_career?: string;
  preferred_difficulty?: string;
  course_id?: string;
  top_k?: number;
};

