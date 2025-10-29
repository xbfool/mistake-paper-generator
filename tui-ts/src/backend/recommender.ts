/**
 * 推荐引擎（TypeScript实现）
 */
import { KnowledgeGraph } from './knowledge';
import type { RecommendPlan } from '../types';
import * as fs from 'fs';
import * as path from 'path';

export class DailyRecommender {
	private knowledgeGraph: KnowledgeGraph;

	constructor(knowledgeGraph: KnowledgeGraph) {
		this.knowledgeGraph = knowledgeGraph;
	}

	/**
	 * 生成每日推荐方案
	 */
	recommend(studentName: string, subject: string = '数学', grade: number = 3): RecommendPlan[] {
		// 加载学生档案
		const profilePath = path.join(__dirname, `../../../data/student_profiles/${studentName}_profile.json`);

		if (!fs.existsSync(profilePath)) {
			return this.getDefaultPlans();
		}

		const profile = JSON.parse(fs.readFileSync(profilePath, 'utf-8'));

		// 分析薄弱知识点
		const weakPoints = this.getWeakPoints(profile, subject, grade);

		// 生成推荐方案
		const plans: RecommendPlan[] = [];

		// 方案1：薄弱点突破
		if (weakPoints.length > 0) {
			plans.push(this.createWeaknessPlan(weakPoints));
		}

		// 方案2：全面复习
		plans.push(this.createComprehensivePlan(grade));

		// 方案3：快速练习
		plans.push(this.createQuickPlan());

		// 方案4：基础补习（如果有根因）
		const rootCauses = this.findRootCauses(weakPoints, profile);
		if (rootCauses.length > 0) {
			plans.unshift(this.createRemedialPlan(rootCauses[0]));
		}

		return plans;
	}

	private getWeakPoints(profile: any, subject: string, grade: number): any[] {
		const weakPoints: any[] = [];

		for (const [kpName, stats] of Object.entries(profile.knowledge_point_stats || {})) {
			const s = stats as any;
			if (s.accuracy_rate < 60 && s.total >= 2) {
				weakPoints.push({
					name: kpName,
					accuracy: s.accuracy_rate,
					total: s.total,
					mistakes: s.mistakes,
				});
			}
		}

		weakPoints.sort((a, b) => a.accuracy - b.accuracy);
		return weakPoints;
	}

	private findRootCauses(weakPoints: any[], profile: any): any[] {
		// 简化实现
		return [];
	}

	private createWeaknessPlan(weakPoints: any[]): RecommendPlan {
		return {
			plan_id: 'weakness',
			name: '薄弱点突破',
			emoji: '🎯',
			description: `重点练习${weakPoints.length}个薄弱知识点`,
			total_questions: 15,
			estimated_time: 20,
			difficulty: '简单→中等',
			goal: '巩固薄弱环节，提高正确率',
			priority: '高',
		};
	}

	private createComprehensivePlan(grade: number): RecommendPlan {
		return {
			plan_id: 'comprehensive',
			name: '全面复习',
			emoji: '📚',
			description: `覆盖${grade}年级主要知识点`,
			total_questions: 20,
			estimated_time: 30,
			difficulty: '中等',
			goal: '全面复习，查漏补缺',
			priority: '中',
		};
	}

	private createQuickPlan(): RecommendPlan {
		return {
			plan_id: 'quick',
			name: '快速练习',
			emoji: '⚡',
			description: '10道精选题目',
			total_questions: 10,
			estimated_time: 10,
			difficulty: '简单',
			goal: '保持手感',
			priority: '低',
		};
	}

	private createRemedialPlan(rootCause: any): RecommendPlan {
		return {
			plan_id: 'remedial',
			name: '基础补习',
			emoji: '🔧',
			description: `回溯到${rootCause.grade}年级，补习「${rootCause.name}」`,
			total_questions: 15,
			estimated_time: 20,
			difficulty: '简单',
			goal: '打牢基础',
			priority: '高',
		};
	}

	private getDefaultPlans(): RecommendPlan[] {
		return [
			this.createQuickPlan(),
			this.createComprehensivePlan(3),
		];
	}
}
