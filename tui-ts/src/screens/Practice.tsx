import React, { useState, useEffect } from 'react';
import { Box, Text, useInput } from 'ink';
import TextInput from 'ink-text-input';
import { backend } from '../services/backend';
import type { Question } from '../types';

interface PracticeProps {
	studentName: string;
	planId: string;
	onBack: () => void;
}

export const Practice: React.FC<PracticeProps> = ({ studentName, planId, onBack }) => {
	const [questions, setQuestions] = useState<Question[]>([]);
	const [currentIndex, setCurrentIndex] = useState(0);
	const [answer, setAnswer] = useState('');
	const [feedback, setFeedback] = useState<string | null>(null);
	const [correct, setCorrect] = useState(0);
	const [wrong, setWrong] = useState(0);
	const [finished, setFinished] = useState(false);

	useEffect(() => {
		loadQuestions();
	}, []);

	const loadQuestions = async () => {
		const q = await backend.generatePractice(studentName, planId);
		setQuestions(q);
	};

	const handleSubmit = () => {
		if (!answer.trim()) return;

		const question = questions[currentIndex];
		const isCorrect = answer.trim().toLowerCase() === question.correct_answer.toLowerCase();

		if (isCorrect) {
			setCorrect(correct + 1);
			setFeedback('✅ 正确！');
		} else {
			setWrong(wrong + 1);
			setFeedback(`❌ 错误。正确答案：${question.correct_answer}`);
		}

		setTimeout(() => {
			if (currentIndex + 1 < questions.length) {
				setCurrentIndex(currentIndex + 1);
				setAnswer('');
				setFeedback(null);
			} else {
				setFinished(true);
			}
		}, 1500);
	};

	useInput((input) => {
		if ((input === 'b' || input === 'B') && finished) {
			onBack();
		}
	});

	if (questions.length === 0) {
		return <Text>加载练习题...</Text>;
	}

	if (finished) {
		const total = questions.length;
		const accuracy = ((correct / total) * 100).toFixed(1);

		return (
			<Box flexDirection="column" padding={1}>
				<Text bold color="green">🎉 练习完成！</Text>

				<Box marginTop={1} borderStyle="double" borderColor="green" padding={1} flexDirection="column">
					<Text>总题数: {total}</Text>
					<Text>正确: <Text color="green">{correct}</Text></Text>
					<Text>错误: <Text color="red">{wrong}</Text></Text>
					<Text>正确率: <Text bold color="cyan">{accuracy}%</Text></Text>
				</Box>

				<Box marginTop={2}>
					<Text dimColor>[B]返回主页</Text>
				</Box>
			</Box>
		);
	}

	const question = questions[currentIndex];
	const progress = `${currentIndex + 1}/${questions.length}`;

	return (
		<Box flexDirection="column" padding={1}>
			<Text bold color="cyan">✍️ 练习中  进度: {progress}</Text>

			<Box marginTop={1} borderStyle="single" padding={1} flexDirection="column">
				<Text bold>第 {currentIndex + 1} 题</Text>
				<Text>{question.question_content}</Text>
				<Text dimColor>知识点: {question.knowledge_point}</Text>
			</Box>

			<Box marginTop={1}>
				<Text>你的答案: </Text>
				<TextInput value={answer} onChange={setAnswer} onSubmit={handleSubmit} />
			</Box>

			{feedback && (
				<Box marginTop={1}>
					<Text color={feedback.startsWith('✅') ? 'green' : 'red'}>{feedback}</Text>
				</Box>
			)}

			<Box marginTop={1}>
				<Text dimColor>已完成: {correct}对 {wrong}错</Text>
			</Box>
		</Box>
	);
};
