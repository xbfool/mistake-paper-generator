import React, { useState, useEffect } from 'react';
import { Box, Text, useInput } from 'ink';
import SelectInput from 'ink-select-input';
import { PlanCard } from '../components/PlanCard';
import { backend } from '../services/backend';
import type { RecommendPlan } from '../types';

interface DailyProps {
	studentName: string;
	onBack: () => void;
	onStartPractice?: (plan: RecommendPlan) => void;
}

export const Daily: React.FC<DailyProps> = ({ studentName, onBack, onStartPractice }) => {
	const [plans, setPlans] = useState<RecommendPlan[]>([]);
	const [selectedIndex, setSelectedIndex] = useState(0);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		loadPlans();
	}, []);

	const loadPlans = async () => {
		try {
			const plansData = await backend.getDailyRecommendations(studentName);
			setPlans(plansData);
		} catch (error: any) {
			console.error('加载推荐失败:', error);
		} finally {
			setLoading(false);
		}
	};

	useInput((input) => {
		if (input === 'b' || input === 'B') {
			onBack();
		}
	});

	const items = plans.map((plan, index) => ({
		label: `${index === 0 ? '⭐ ' : '  '}${plan.emoji} ${plan.name}`,
		value: plan,
	}));

	const handleSelect = (item: any) => {
		if (onStartPractice) {
			onStartPractice(item.value);
		}
	};

	if (loading) {
		return <Text>加载推荐方案...</Text>;
	}

	return (
		<Box flexDirection="column" padding={1}>
			<Text bold color="cyan">📅 今日推荐</Text>
			<Box marginTop={1} />

			{plans.length > 0 ? (
				<Box flexDirection="column">
					{plans.map((plan, idx) => (
						<PlanCard
							key={plan.plan_id}
							plan={plan}
							isSelected={idx === selectedIndex}
							isRecommended={idx === 0}
						/>
					))}

					<Box marginTop={2}>
						<Text dimColor>提示: 使用方向键选择方案，Enter开始练习，[B]返回</Text>
					</Box>
				</Box>
			) : (
				<Text>暂无推荐方案</Text>
			)}
		</Box>
	);
};
