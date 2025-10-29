/**
 * 后端服务（纯TypeScript实现）
 */
import * as fs from 'fs';
import * as path from 'path';
import { KnowledgeGraph } from '../backend/knowledge';
import { DiagnosisSystem } from '../backend/diagnosis';
import { DailyRecommender } from '../backend/recommender';
import { claudeAPI } from '../backend/api';
import type { StudentStats, WeakPoint, RecommendPlan, DiagnoseReport, Question } from '../types';

class BackendService {
	private knowledgeGraph: KnowledgeGraph;
	private diagnosis: DiagnosisSystem;
	private recommender: DailyRecommender;

	constructor() {
		// 初始化知识图谱
		this.knowledgeGraph = new KnowledgeGraph();
		this.diagnosis = new DiagnosisSystem(this.knowledgeGraph);
		this.recommender = new DailyRecommender(this.knowledgeGraph);
	}

	/**
	 * 获取学生统计数据
	 */
	async getStudentStats(studentName: string): Promise<StudentStats> {
		try {
			const profilePath = path.join(__dirname, `../../../data/student_profiles/${studentName}_profile.json`);

			if (!fs.existsSync(profilePath)) {
				return {
					totalQuestions: 0,
					totalMistakes: 0,
					accuracy: 0,
					gradeLevel: '0',
					totalExams: 0,
				};
			}

			const profile = JSON.parse(fs.readFileSync(profilePath, 'utf-8'));

			return {
				totalQuestions: profile.total_questions || 0,
				totalMistakes: profile.total_mistakes || 0,
				accuracy: this.calculateAccuracy(profile),
				gradeLevel: '2.3', // TODO: 从诊断结果获取
				totalExams: profile.exams?.length || 0,
			};
		} catch (error) {
			console.error('获取学生统计失败:', error);
			return {
				totalQuestions: 0,
				totalMistakes: 0,
				accuracy: 0,
				gradeLevel: '0',
				totalExams: 0,
			};
		}
	}

	private calculateAccuracy(profile: any): number {
		const total = profile.total_questions || 0;
		const mistakes = profile.total_mistakes || 0;

		if (total === 0) return 0;

		return ((total - mistakes) / total) * 100;
	}

	/**
	 * 获取薄弱知识点
	 */
	async getWeakPoints(studentName: string): Promise<WeakPoint[]> {
		try {
			const profilePath = path.join(__dirname, `../../../data/student_profiles/${studentName}_profile.json`);

			if (!fs.existsSync(profilePath)) {
				return [];
			}

			const profile = JSON.parse(fs.readFileSync(profilePath, 'utf-8'));
			const weakPoints: WeakPoint[] = [];

			for (const [kpName, stats] of Object.entries(profile.knowledge_point_stats || {})) {
				const s = stats as any;
				if (s.accuracy_rate < 70 && s.total >= 2) {
					weakPoints.push({
						knowledge_point: kpName,
						accuracy_rate: s.accuracy_rate,
						total: s.total,
						mistakes: s.mistakes,
					});
				}
			}

			weakPoints.sort((a, b) => a.accuracy_rate - b.accuracy_rate);

			return weakPoints;
		} catch (error) {
			console.error('获取薄弱知识点失败:', error);
			return [];
		}
	}

	/**
	 * 获取每日推荐
	 */
	async getDailyRecommendations(studentName: string): Promise<RecommendPlan[]> {
		try {
			return this.recommender.recommend(studentName);
		} catch (error) {
			console.error('获取推荐失败:', error);
			return [];
		}
	}

	/**
	 * 运行诊断
	 */
	async runDiagnosis(studentName: string): Promise<DiagnoseReport> {
		try {
			return this.diagnosis.diagnose(studentName);
		} catch (error: any) {
			console.error('诊断失败:', error);
			throw error;
		}
	}

	/**
	 * 生成练习题
	 */
	async generatePractice(studentName: string, planId: string): Promise<Question[]> {
		try {
			// 使用Claude API生成题目
			const questions = await claudeAPI.generateQuestions('乘法口诀', 10, 2);

			return questions.map((q, idx) => ({
				question_number: idx + 1,
				question_content: q.question_content,
				question_type: '口算题',
				correct_answer: q.correct_answer,
				explanation: q.explanation,
				difficulty: 2,
				knowledge_point: '乘法口诀',
			}));
		} catch (error) {
			console.error('生成练习失败:', error);
			return [];
		}
	}
}

export const backend = new BackendService();
