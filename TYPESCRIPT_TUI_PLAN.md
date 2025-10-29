# TypeScript Ink TUI 开发计划

**目标**: 使用TypeScript + React + Ink创建美观的终端界面
**预计时间**: 3-4天
**状态**: 🔲 待开始

---

## 📋 文件创建清单

### 阶段1：项目基础（预计2小时）

#### 配置文件（4个）
- [x] `tui-ts/package.json` - npm配置
- [x] `tui-ts/tsconfig.json` - TypeScript配置
- [ ] `tui-ts/.gitignore` - Git忽略
- [ ] `tui-ts/README.md` - 项目说明

#### 类型定义（1个）
- [x] `tui-ts/src/types/index.ts` - 完整类型定义

#### 后端服务（1个）
- [x] `tui-ts/src/services/backend.ts` - Python CLI调用

---

### 阶段2：基础组件（预计3小时）

#### 组件文件（6个）
- [ ] `tui-ts/src/components/Header.tsx` - 顶部栏
- [ ] `tui-ts/src/components/Footer.tsx` - 底部栏
- [ ] `tui-ts/src/components/StatsCard.tsx` - 统计卡片
- [ ] `tui-ts/src/components/WeakPointsList.tsx` - 薄弱点列表
- [ ] `tui-ts/src/components/PlanCard.tsx` - 推荐方案卡片
- [ ] `tui-ts/src/components/QuestionCard.tsx` - 题目卡片

#### Hooks（2个）
- [ ] `tui-ts/src/hooks/useStudent.ts` - 学生数据Hook
- [ ] `tui-ts/src/hooks/useBackend.ts` - 后端调用Hook

---

### 阶段3：核心界面（预计6小时）

#### 界面文件（5个）
- [ ] `tui-ts/src/screens/Dashboard.tsx` - 主页
- [ ] `tui-ts/src/screens/Daily.tsx` - 每日推荐
- [ ] `tui-ts/src/screens/Diagnose.tsx` - 诊断测试
- [ ] `tui-ts/src/screens/Practice.tsx` - 练习答题
- [ ] `tui-ts/src/screens/Report.tsx` - 学习报告

---

### 阶段4：主应用（预计2小时）

#### 应用文件（2个）
- [x] `tui-ts/src/app.tsx` - 主应用组件（已创建基础版）
- [ ] `tui-ts/src/index.tsx` - 入口文件

---

### 阶段5：TypeScript后端实现（预计6小时）

#### 后端服务文件（用TypeScript重写核心逻辑）
- [ ] `tui-ts/src/backend/api.ts` - Claude API调用
- [ ] `tui-ts/src/backend/knowledge.ts` - 知识图谱加载
- [ ] `tui-ts/src/backend/diagnosis.ts` - 诊断逻辑
- [ ] `tui-ts/src/backend/recommender.ts` - 推荐引擎
- [ ] `tui-ts/src/backend/practice.ts` - 练习生成

#### 数据加载
- [ ] 读取knowledge_data/*.json配置
- [ ] 读取student_profiles/*.json档案
- [ ] 调用Claude API（使用@anthropic-ai/sdk）

---

### 阶段6：编译和打包（预计1小时）

#### 配置文件
- [ ] 配置build脚本
- [ ] 配置启动脚本
- [ ] 创建启动器（可执行文件）

---

### 阶段7：测试和优化（预计2小时）

#### 测试
- [ ] 所有界面导航测试
- [ ] 数据加载测试
- [ ] 练习流程测试
- [ ] 错误处理测试

---

## 📊 总计

- **配置文件**: 6个
- **TypeScript文件**: 20个
- **预计代码量**: ~1500行
- **预计时间**: 18小时（3-4天）

---

## 🎯 执行顺序

1. ✅ 项目初始化（已完成部分）
2. 安装依赖
3. 创建基础组件
4. 创建核心界面
5. 完善app.tsx
6. 创建index.tsx入口
7. Python CLI适配
8. 测试调试

---

## ✅ 完成标准

每个阶段完成后：
- ✅ 代码编译通过
- ✅ 功能正常运行
- ✅ 无TypeScript错误
- ✅ 界面美观清晰

---

**准备就绪，开始执行！**
