/**
 * 知识图谱系统（TypeScript版）
 */
import * as fs from 'fs';
import * as path from 'path';

export interface KnowledgePoint {
	id: string;
	category: string;
	name: string;
	description: string;
	difficulty: number;
	keywords: string[];
	prerequisites: string[];
	next_points: string[];
	typical_questions: string[];
	common_mistakes: string[];
	learning_tips: string;
	importance: number;
	avg_learning_time: number;
	grade: number;
	subject: string;
}

export class KnowledgeGraph {
	private knowledgePoints: Map<string, KnowledgePoint> = new Map();
	private dataDir: string;

	constructor(dataDir: string = '../knowledge_data') {
		this.dataDir = path.join(__dirname, dataDir);
		this.loadAllKnowledge();
	}

	/**
	 * 加载所有知识点配置
	 */
	private loadAllKnowledge() {
		const subjects = ['math', 'chinese', 'english'];

		for (const subject of subjects) {
			for (let grade = 1; grade <= 6; grade++) {
				const configPath = path.join(this.dataDir, subject, `grade_${grade}.json`);

				if (fs.existsSync(configPath)) {
					try {
						const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));

						if (config.modules) {
							for (const [moduleName, moduleData] of Object.entries(config.modules)) {
								const module = moduleData as any;
								if (module.points && Array.isArray(module.points)) {
									for (const point of module.points) {
										const kp: KnowledgePoint = {
											...point,
											grade: config.grade,
											subject: config.subject,
										};
										this.knowledgePoints.set(point.id, kp);
									}
								}
							}
						}
					} catch (error) {
						// 配置文件格式错误或不存在，跳过
					}
				}
			}
		}

		console.log(`✓ 知识图谱加载完成：${this.knowledgePoints.size} 个知识点`);
	}

	/**
	 * 获取知识点
	 */
	getPoint(pointId: string): KnowledgePoint | undefined {
		return this.knowledgePoints.get(pointId);
	}

	/**
	 * 获取某学科某年级的所有知识点
	 */
	getPointsByGradeSubject(subject: string, grade: number): KnowledgePoint[] {
		return Array.from(this.knowledgePoints.values()).filter(
			p => p.subject === subject && p.grade === grade
		);
	}

	/**
	 * 获取所有前置知识点（递归）
	 */
	getAllPrerequisites(pointId: string): KnowledgePoint[] {
		const result: KnowledgePoint[] = [];
		const visited = new Set<string>();

		const dfs = (id: string) => {
			if (visited.has(id)) return;
			visited.add(id);

			const point = this.getPoint(id);
			if (!point) return;

			for (const prereqId of point.prerequisites) {
				dfs(prereqId);
			}

			if (id !== pointId) {
				result.push(point);
			}
		};

		dfs(pointId);
		return result;
	}

	/**
	 * 查找薄弱点的根本原因
	 */
	findRootCause(weakPointId: string, masteredPoints: Set<string>): KnowledgePoint | null {
		const allPrereqs = this.getAllPrerequisites(weakPointId);

		for (const point of allPrereqs) {
			if (!masteredPoints.has(point.id)) {
				return point;
			}
		}

		return this.getPoint(weakPointId) || null;
	}
}
