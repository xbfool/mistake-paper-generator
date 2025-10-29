import React, { useState, useEffect } from 'react';
import { Box, Text, useInput } from 'ink';
import Spinner from 'ink-spinner';
import { backend } from '../services/backend';
import type { DiagnoseReport } from '../types';

interface DiagnoseProps {
	studentName: string;
	onBack: () => void;
}

export const Diagnose: React.FC<DiagnoseProps> = ({ studentName, onBack }) => {
	const [report, setReport] = useState<DiagnoseReport | null>(null);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		runDiagnosis();
	}, []);

	useInput((input) => {
		if (input === 'b' || input === 'B') {
			onBack();
		}
	});

	const runDiagnosis = async () => {
		try {
			const reportData = await backend.runDiagnosis(studentName);
			setReport(reportData);
		} catch (error: any) {
			console.error('诊断失败:', error);
		} finally {
			setLoading(false);
		}
	};

	if (loading) {
		return (
			<Box>
				<Text color="cyan">
					<Spinner type="dots" />
				</Text>
				<Text> 正在诊断...</Text>
			</Box>
		);
	}

	if (!report) {
		return <Text color="red">诊断失败</Text>;
	}

	return (
		<Box flexDirection="column" padding={1}>
			<Text bold color="cyan">🔍 诊断测试结果</Text>

			<Box marginTop={1} flexDirection="column" borderStyle="single" borderColor="cyan" padding={1}>
				<Text>目标年级: {report.target_grade} | 实际水平: <Text bold color="yellow">{report.actual_grade_level}年级</Text></Text>
				<Text>已掌握: {report.mastered_count}个 | 薄弱: <Text color="red">{report.weak_count}个</Text></Text>
			</Box>

			{report.root_causes && report.root_causes.length > 0 && (
				<Box marginTop={2} flexDirection="column">
					<Text bold color="red">🔴 需要补习的前置知识点</Text>
					{report.root_causes.slice(0, 5).map((cause, idx) => (
						<Text key={idx}>
							  {idx + 1}. [{cause.grade}年级] {cause.name} {'★'.repeat(cause.importance)}
						</Text>
					))}
				</Box>
			)}

			{report.recommendations && report.recommendations.length > 0 && (
				<Box marginTop={2} flexDirection="column">
					<Text bold color="yellow">💡 学习建议</Text>
					{report.recommendations.slice(0, 3).map((rec, idx) => (
						<Box key={idx} flexDirection="column" marginTop={1}>
							<Text bold>【{rec.priority}】{rec.title}</Text>
							<Text dimColor>  {rec.description}</Text>
							<Text dimColor>  💡 {rec.action}</Text>
						</Box>
					))}
				</Box>
			)}

			<Box marginTop={2}>
				<Text dimColor>[B]返回</Text>
			</Box>
		</Box>
	);
};
