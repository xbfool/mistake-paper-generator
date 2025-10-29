/**
 * 类型定义
 */

export interface StudentStats {
	totalQuestions: number;
	totalMistakes: number;
	accuracy: number;
	gradeLevel: string;
	totalExams: number;
}

export interface WeakPoint {
	knowledge_point: string;
	accuracy_rate: number;
	total: number;
	mistakes: number;
}

export interface RecommendPlan {
	plan_id: string;
	name: string;
	emoji: string;
	description: string;
	total_questions: number;
	estimated_time: number;
	difficulty: string;
	goal: string;
	priority: string;
	knowledge_points?: Array<{
		id: string;
		name: string;
		grade: number;
		questions_count: number;
	}>;
}

export interface DiagnoseReport {
	student_name: string;
	target_grade: number;
	actual_grade_level: number;
	mastered_count: number;
	weak_count: number;
	root_causes: Array<{
		id: string;
		name: string;
		grade: number;
		importance: number;
	}>;
	recommendations: Array<{
		priority: string;
		title: string;
		description: string;
		action: string;
	}>;
}

export interface Question {
	question_number: number;
	question_content: string;
	question_type: string;
	correct_answer: string;
	explanation?: string;
	difficulty: number;
	knowledge_point: string;
}

export type ScreenType = 'dashboard' | 'daily' | 'diagnose' | 'practice' | 'report' | 'scan';
