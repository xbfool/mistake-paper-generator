import React, { useState, useEffect } from 'react';
import { Box, Text } from 'ink';
import { StatsCard } from '../components/StatsCard';
import { WeakPointsList } from '../components/WeakPointsList';
import { backend } from '../services/backend';
import type { StudentStats, WeakPoint, ScreenType } from '../types';

interface DashboardProps {
	studentName: string;
	onNavigate: (screen: ScreenType) => void;
}

export const Dashboard: React.FC<DashboardProps> = ({ studentName, onNavigate }) => {
	const [stats, setStats] = useState<StudentStats | null>(null);
	const [weakPoints, setWeakPoints] = useState<WeakPoint[]>([]);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		loadData();
	}, [studentName]);

	const loadData = async () => {
		try {
			setLoading(true);
			const [statsData, weakPointsData] = await Promise.all([
				backend.getStudentStats(studentName),
				backend.getWeakPoints(studentName),
			]);

			setStats(statsData);
			setWeakPoints(weakPointsData);
		} catch (error: any) {
			console.error('加载数据失败:', error);
		} finally {
			setLoading(false);
		}
	};

	if (loading) {
		return <Text>加载中...</Text>;
	}

	return (
		<Box flexDirection="column" padding={1}>
			{/* 统计概况 */}
			<Text bold color="cyan">📊 学习概况</Text>
			<Box marginTop={1} gap={2}>
				<StatsCard label="总题数" value={stats?.totalQuestions || 0} icon="📝" />
				<StatsCard label="错题数" value={stats?.totalMistakes || 0} icon="❌" color="red" />
				<StatsCard label="正确率" value={`${stats?.accuracy.toFixed(1)}%`} icon="✅" color="green" />
				<StatsCard label="实际水平" value={`${stats?.gradeLevel}年级`} icon="📊" color="yellow" />
			</Box>

			{/* 薄弱知识点 */}
			<Box marginTop={2} flexDirection="column">
				<Text bold color="red">🔴 薄弱知识点 Top 5</Text>
				<Box marginTop={1}>
					<WeakPointsList points={weakPoints} />
				</Box>
			</Box>

			{/* 快捷操作 */}
			<Box marginTop={2} flexDirection="column">
				<Text bold>⚡ 快捷操作</Text>
				<Box marginTop={1}>
					<Text dimColor>[2] 查看今日推荐  [3] 运行诊断测试  [4] 查看学习报告</Text>
				</Box>
			</Box>
		</Box>
	);
};
