import React, { useState, useEffect } from 'react';
import { Box, Text, useInput } from 'ink';
import { WeakPointsList } from '../components/WeakPointsList';
import { backend } from '../services/backend';

interface ReportProps {
	studentName: string;
	onBack: () => void;
}

export const Report: React.FC<ReportProps> = ({ studentName, onBack }) => {
	const [stats, setStats] = useState<any>(null);
	const [weakPoints, setWeakPoints] = useState<any[]>([]);

	useEffect(() => {
		loadData();
	}, []);

	useInput((input) => {
		if (input === 'b' || input === 'B') {
			onBack();
		}
	});

	const loadData = async () => {
		try {
			const [statsData, weakData] = await Promise.all([
				backend.getStudentStats(studentName),
				backend.getWeakPoints(studentName),
			]);
			setStats(statsData);
			setWeakPoints(weakData);
		} catch (error) {
			console.error('加载报告失败:', error);
		}
	};

	return (
		<Box flexDirection="column" padding={1}>
			<Text bold color="cyan">📊 学习报告</Text>

			{stats && (
				<Box marginTop={1} flexDirection="column" borderStyle="single" padding={1}>
					<Text>测试次数: {stats.totalExams}</Text>
					<Text>累计题数: {stats.totalQuestions}</Text>
					<Text>总体正确率: <Text bold color="green">{stats.accuracy.toFixed(1)}%</Text></Text>
				</Box>
			)}

			<Box marginTop={2} flexDirection="column">
				<Text bold color="red">🔴 薄弱知识点</Text>
				<Box marginTop={1}>
					<WeakPointsList points={weakPoints} />
				</Box>
			</Box>

			<Box marginTop={2}>
				<Text dimColor>[B]返回</Text>
			</Box>
		</Box>
	);
};
