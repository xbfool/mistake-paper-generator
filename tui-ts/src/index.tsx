#!/usr/bin/env node
import React from 'react';
import { render } from 'ink';
import { App } from './app';

// 获取命令行参数
const args = process.argv.slice(2);
const studentName = args[0] || '琪琪';

// 渲染应用
render(<App studentName={studentName} />);
