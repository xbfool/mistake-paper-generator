import React from 'react';
import { Box, Text } from 'ink';

interface StatsCardProps {
	label: string;
	value: string | number;
	icon?: string;
	color?: string;
}

export const StatsCard: React.FC<StatsCardProps> = ({ label, value, icon = '📊', color = 'cyan' }) => {
	return (
		<Box borderStyle="round" borderColor={color} padding={1} flexDirection="column" alignItems="center" minWidth={15}>
			<Text>{icon}</Text>
			<Text dimColor>{label}</Text>
			<Text bold color={color}>{value}</Text>
		</Box>
	);
};
