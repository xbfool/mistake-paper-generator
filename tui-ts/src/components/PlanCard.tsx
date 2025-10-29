import React from 'react';
import { Box, Text } from 'ink';
import type { RecommendPlan } from '../types';

interface PlanCardProps {
	plan: RecommendPlan;
	isSelected?: boolean;
	isRecommended?: boolean;
}

export const PlanCard: React.FC<PlanCardProps> = ({ plan, isSelected, isRecommended }) => {
	const borderColor = isSelected ? 'cyan' : isRecommended ? 'green' : 'gray';
	const borderStyle = isSelected ? 'double' : 'single';

	return (
		<Box borderStyle={borderStyle} borderColor={borderColor} padding={1} flexDirection="column" marginY={1}>
			<Text bold>{isRecommended ? '⭐ ' : '  '}{plan.emoji} {plan.name}</Text>
			<Text dimColor>{plan.description}</Text>
			<Text>📊 {plan.total_questions}道题 | ⏱️  {plan.estimated_time}分钟 | 难度: {plan.difficulty}</Text>
			<Text dimColor>🎯 {plan.goal}</Text>
		</Box>
	);
};
