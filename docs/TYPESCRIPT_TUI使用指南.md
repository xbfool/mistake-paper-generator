# TypeScript TUI 使用指南

## 🎨 纯TypeScript实现的终端界面

**技术栈**: TypeScript + React + Ink
**特点**: 美观、流畅、功能完整

---

## 🚀 安装和运行

### 安装依赖
```bash
cd tui-ts
npm install
```

### 开发模式（推荐）
```bash
npm run dev
```

### 构建运行
```bash
npm run build
npm start
```

### 指定学生
```bash
npm start 琪琪
```

---

## 📊 已实现功能

### ✅ 核心界面
1. **Dashboard（主页）** - 按1
   - 学习统计卡片
   - 薄弱知识点Top 5
   - 快捷操作

2. **Daily（每日推荐）** - 按2
   - 4个智能推荐方案
   - 方案详情展示

3. **Diagnose（诊断测试）** - 按3
   - 实际水平评估
   - 前置知识点检测
   - 学习建议

4. **Report（学习报告）** - 按4
   - 总体统计
   - 薄弱知识点详情

### ✅ TypeScript后端
- 知识图谱加载（读取JSON配置）
- 诊断系统（TypeScript实现）
- 推荐引擎（TypeScript实现）
- Claude API调用（AI出题）

---

## ⌨️ 快捷键

```
1 - Dashboard（主页）
2 - Daily（每日推荐）
3 - Diagnose（诊断测试）
4 - Report（学习报告）

Q - 退出
B - 返回上一界面
```

---

## 🎯 使用流程

### 第一次使用

1. 确保有学生数据（使用Python CLI）
```bash
cd ..
python3 main.py add-exam -s 琪琪 --source "测试"
```

2. 启动TypeScript TUI
```bash
cd tui-ts
npm run dev
```

3. 界面导航
- 自动显示Dashboard
- 按数字键2-4切换界面
- 按B返回，按Q退出

### 每日使用

```bash
cd tui-ts
npm run dev

# 在TUI中：
# 1. 查看Dashboard（学习概况）
# 2. 按2查看今日推荐
# 3. 按3运行诊断测试
# 4. 按4查看学习报告
```

---

## 📦 项目结构

```
tui-ts/
├── package.json              # npm配置
├── tsconfig.json             # TypeScript配置
├── src/
│   ├── index.tsx             # 入口文件
│   ├── app.tsx               # 主应用
│   ├── types/index.ts        # 类型定义
│   ├── backend/              # TypeScript后端
│   │   ├── api.ts            # Claude API
│   │   ├── knowledge.ts      # 知识图谱
│   │   ├── diagnosis.ts      # 诊断系统
│   │   └── recommender.ts    # 推荐引擎
│   ├── services/
│   │   └── backend.ts        # 统一后端服务
│   ├── components/           # UI组件
│   │   ├── StatsCard.tsx
│   │   ├── WeakPointsList.tsx
│   │   └── PlanCard.tsx
│   └── screens/              # 界面
│       ├── Dashboard.tsx
│       ├── Daily.tsx
│       ├── Diagnose.tsx
│       ├── Practice.tsx
│       └── Report.tsx
└── dist/                     # 编译输出
```

---

## 🎨 界面特点

### 美观
- ✨ Unicode边框和图标
- 🎨 彩色文字和进度条
- 📊 清晰的布局
- ⚡ 流畅的动画

### 功能
- ✅ 完整的数据展示
- ✅ TypeScript后端（无需Python）
- ✅ 实时数据加载
- ✅ 流畅的导航

### 体验
- ⌨️ 简单的快捷键
- 🖱️ 清晰的提示
- 📱 响应式设计
- ⚡ 快速启动

---

## 🔧 技术亮点

### 纯TypeScript实现
- 不依赖Python运行时
- 所有逻辑用TS重写
- 直接读取JSON数据
- 调用Claude API出题

### React组件化
- 清晰的组件结构
- 可复用的UI组件
- Hooks状态管理

### Ink框架
- 现代化TUI
- 丰富的组件库
- 流畅的体验

---

## ⚠️ 注意事项

1. **需要学生数据**
   - 使用Python CLI先创建学生档案
   - 或手动创建JSON文件

2. **API密钥**
   - 确保.env中有ANTHROPIC_API_KEY
   - Claude API用于生成练习题

3. **Node.js版本**
   - 需要Node.js 18+

---

## 📝 开发说明

### 添加新界面
1. 在`src/screens/`创建新组件
2. 在`app.tsx`中注册
3. 添加快捷键绑定

### 添加新组件
1. 在`src/components/`创建
2. 在`index.ts`中导出

---

## 🎉 完成状态

✅ **核心功能100%完成**
- 所有界面已实现
- TypeScript后端完整
- 可立即使用

---

**现在就试试：**

```bash
cd tui-ts
npm install
npm run dev
```

按数字键1-4导航，美观流畅！🎨
