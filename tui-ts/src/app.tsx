/**
 * 主应用组件
 */
import React, { useState } from 'react';
import { Box, Text, useApp, useInput } from 'ink';
import { Dashboard } from './screens/Dashboard';
import { Daily } from './screens/Daily';
import { Diagnose } from './screens/Diagnose';
import { Report } from './screens/Report';
import type { ScreenType } from './types';

interface AppProps {
	studentName?: string;
}

export const App: React.FC<AppProps> = ({ studentName = '琪琪' }) => {
	const { exit } = useApp();
	const [currentScreen, setCurrentScreen] = useState<ScreenType>('dashboard');

	// 全局快捷键
	useInput((input, key) => {
		if (input === 'q' || input === 'Q') {
			exit();
		} else if (input === '1') {
			setCurrentScreen('dashboard');
		} else if (input === '2') {
			setCurrentScreen('daily');
		} else if (input === '3') {
			setCurrentScreen('diagnose');
		} else if (input === '4') {
			setCurrentScreen('report');
		}
	});

	// 渲染当前屏幕
	const renderScreen = () => {
		switch (currentScreen) {
			case 'dashboard':
				return <Dashboard studentName={studentName} onNavigate={setCurrentScreen} />;
			case 'daily':
				return <Daily studentName={studentName} onBack={() => setCurrentScreen('dashboard')} />;
			case 'diagnose':
				return <Diagnose studentName={studentName} onBack={() => setCurrentScreen('dashboard')} />;
			case 'report':
				return <Report studentName={studentName} onBack={() => setCurrentScreen('dashboard')} />;
			default:
				return <Dashboard studentName={studentName} onNavigate={setCurrentScreen} />;
		}
	};

	return (
		<Box flexDirection="column">
			{/* Header */}
			<Box borderStyle="double" borderColor="cyan" padding={1}>
				<Text bold color="cyan">
					🎓 智能学习系统 v2.0  |  学生: {studentName}  |  数学 3年级
				</Text>
			</Box>

			{/* Content */}
			<Box marginTop={1}>{renderScreen()}</Box>

			{/* Footer */}
			<Box marginTop={1} borderStyle="single" borderColor="gray" padding={1}>
				<Text dimColor>
					快捷键: [1]主页 [2]推荐 [3]诊断 [4]报告 [Q]退出
				</Text>
			</Box>
		</Box>
	);
};
