/**
 * 诊断系统（TypeScript实现）
 */
import { KnowledgeGraph } from './knowledge';
import type { DiagnoseReport } from '../types';
import * as fs from 'fs';
import * as path from 'path';

export class DiagnosisSystem {
	private knowledgeGraph: KnowledgeGraph;

	constructor(knowledgeGraph: KnowledgeGraph) {
		this.knowledgeGraph = knowledgeGraph;
	}

	/**
	 * 诊断学生
	 */
	diagnose(studentName: string, subject: string = '数学', targetGrade: number = 3): DiagnoseReport {
		// 加载学生档案
		const profilePath = path.join(__dirname, `../../../data/student_profiles/${studentName}_profile.json`);

		if (!fs.existsSync(profilePath)) {
			throw new Error(`学生档案不存在: ${studentName}`);
		}

		const profile = JSON.parse(fs.readFileSync(profilePath, 'utf-8'));

		// 获取目标年级的所有知识点
		const targetPoints = this.knowledgeGraph.getPointsByGradeSubject(subject, targetGrade);

		// 分析已掌握的知识点
		const masteredPoints = this.analyzeMasteredPoints(profile, subject);

		// 找出薄弱知识点
		const weakPoints = this.findWeakPoints(profile, subject, targetGrade);

		// 回溯根本原因
		const rootCauses = this.findRootCauses(weakPoints, masteredPoints);

		// 估算实际水平
		const actualLevel = this.estimateGradeLevel(masteredPoints, subject, targetGrade);

		// 生成建议
		const recommendations = this.generateRecommendations(rootCauses, weakPoints, actualLevel, targetGrade);

		return {
			student_name: studentName,
			target_grade: targetGrade,
			actual_grade_level: actualLevel,
			mastered_count: masteredPoints.size,
			weak_count: weakPoints.length,
			root_causes: rootCauses.map(p => ({
				id: p.id,
				name: p.name,
				grade: p.grade,
				importance: p.importance,
			})),
			recommendations,
		};
	}

	private analyzeMasteredPoints(profile: any, subject: string): Set<string> {
		const mastered = new Set<string>();

		for (const [kpName, stats] of Object.entries(profile.knowledge_point_stats || {})) {
			const s = stats as any;
			if (s.accuracy_rate >= 80 && s.total >= 3) {
				// 找到对应的知识点ID
				for (const point of Array.from(this.knowledgeGraph['knowledgePoints'].values())) {
					if (point.name === kpName && point.subject === subject) {
						mastered.add(point.id);
						break;
					}
				}
			}
		}

		return mastered;
	}

	private findWeakPoints(profile: any, subject: string, grade: number): any[] {
		const weakPoints: any[] = [];

		for (const [kpName, stats] of Object.entries(profile.knowledge_point_stats || {})) {
			const s = stats as any;
			if (s.accuracy_rate < 60 && s.total >= 2) {
				for (const point of Array.from(this.knowledgeGraph['knowledgePoints'].values())) {
					if (point.name === kpName && point.subject === subject && point.grade <= grade) {
						weakPoints.push({ point, accuracy: s.accuracy_rate });
						break;
					}
				}
			}
		}

		return weakPoints;
	}

	private findRootCauses(weakPoints: any[], masteredPoints: Set<string>): any[] {
		const rootCauses: any[] = [];

		for (const { point } of weakPoints.slice(0, 5)) {
			const rootCause = this.knowledgeGraph.findRootCause(point.id, masteredPoints);
			if (rootCause && !rootCauses.find(rc => rc.id === rootCause.id)) {
				rootCauses.push(rootCause);
			}
		}

		return rootCauses;
	}

	private estimateGradeLevel(masteredPoints: Set<string>, subject: string, targetGrade: number): number {
		let actualLevel = 0.0;

		for (let grade = 1; grade <= targetGrade; grade++) {
			const gradePoints = this.knowledgeGraph.getPointsByGradeSubject(subject, grade);
			if (gradePoints.length === 0) continue;

			const masteredCount = gradePoints.filter(p => masteredPoints.has(p.id)).length;
			const masteryRate = masteredCount / gradePoints.length;

			if (masteryRate >= 0.8) {
				actualLevel = grade;
			} else if (masteryRate >= 0.5) {
				actualLevel = grade - 0.5;
			} else {
				break;
			}
		}

		return Math.round(actualLevel * 10) / 10;
	}

	private generateRecommendations(rootCauses: any[], weakPoints: any[], actualLevel: number, targetGrade: number): any[] {
		const recommendations: any[] = [];

		if (rootCauses.length > 0) {
			const root = rootCauses[0];
			recommendations.push({
				priority: '高',
				title: `优先补习：${root.grade}年级 - ${root.name}`,
				description: '这是当前薄弱环节的根本原因',
				action: `生成「${root.name}」专项练习`,
			});
		}

		if (actualLevel < targetGrade - 0.5) {
			recommendations.push({
				priority: '高',
				title: `建议从${Math.floor(actualLevel + 1)}年级内容开始系统学习`,
				description: `当前实际掌握水平为${actualLevel}年级`,
				action: '制定系统补习计划',
			});
		}

		return recommendations;
	}
}
