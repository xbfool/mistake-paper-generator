import React from 'react';
import { Box, Text } from 'ink';
import type { WeakPoint } from '../types';

interface WeakPointsListProps {
	points: WeakPoint[];
}

export const WeakPointsList: React.FC<WeakPointsListProps> = ({ points }) => {
	if (!points || points.length === 0) {
		return <Text color="green">✅ 暂无薄弱知识点</Text>;
	}

	return (
		<Box flexDirection="column">
			{points.slice(0, 5).map((point, idx) => {
				const progress = '█'.repeat(Math.floor(point.accuracy_rate / 10)) + '░'.repeat(10 - Math.floor(point.accuracy_rate / 10));
				const color = point.accuracy_rate < 40 ? 'red' : point.accuracy_rate < 70 ? 'yellow' : 'green';

				return (
					<Text key={idx}>
						{idx + 1}. {point.knowledge_point.padEnd(15)} {point.accuracy_rate.toFixed(1)}% <Text color={color}>{progress}</Text> ({point.mistakes}/{point.total})
					</Text>
				);
			})}
		</Box>
	);
};
