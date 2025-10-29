/**
 * Claude API调用
 */
import Anthropic from '@anthropic-ai/sdk';
import * as fs from 'fs';
import * as path from 'path';

export class ClaudeAPI {
	private client: Anthropic;

	constructor() {
		// 从.env文件读取API密钥
		const apiKey = process.env.ANTHROPIC_API_KEY || this.loadApiKeyFromEnv();

		if (!apiKey) {
			throw new Error('未找到ANTHROPIC_API_KEY，请在.env文件中配置');
		}

		this.client = new Anthropic({ apiKey });
	}

	private loadApiKeyFromEnv(): string | undefined {
		try {
			const envPath = path.join(__dirname, '../../../.env');
			const envContent = fs.readFileSync(envPath, 'utf-8');
			const match = envContent.match(/ANTHROPIC_API_KEY=(.+)/);
			return match ? match[1].trim() : undefined;
		} catch {
			return undefined;
		}
	}

	/**
	 * 生成练习题
	 */
	async generateQuestions(knowledgePoint: string, count: number, grade: number): Promise<any[]> {
		const prompt = `请为小学${grade}年级数学知识点「${knowledgePoint}」生成${count}道练习题。

要求：
1. 题目准确考查该知识点
2. 难度适中
3. 包含题目、答案、解析

返回JSON格式：
{
  "questions": [
    {
      "question_content": "题目内容",
      "correct_answer": "正确答案",
      "explanation": "解析"
    }
  ]
}`;

		const message = await this.client.messages.create({
			model: 'claude-sonnet-4-5-20250929',
			max_tokens: 2048,
			messages: [{ role: 'user', content: prompt }],
		});

		const responseText = message.content[0].text;

		// 提取JSON
		let jsonText = responseText.trim();
		if (jsonText.includes('```json')) {
			const start = jsonText.indexOf('```json') + 7;
			const end = jsonText.indexOf('```', start);
			jsonText = jsonText.substring(start, end).trim();
		}

		const result = JSON.parse(jsonText);
		return result.questions || [];
	}
}

export const claudeAPI = new ClaudeAPI();
