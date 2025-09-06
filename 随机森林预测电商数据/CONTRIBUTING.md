# 🤝 贡献指南

感谢你对电商数据科学项目的关注！我们欢迎任何形式的贡献。

## 🎯 贡献方式

### 🐛 报告Bug

如果你发现了Bug，请：

1. 检查[Issues](https://github.com/YOUR_USERNAME/ecommerce-ml-prediction/issues)确认问题未被报告
2. 创建新的Issue，包含：
   - 清晰的标题和描述
   - 重现步骤
   - 期望行为vs实际行为
   - 环境信息（Python版本、操作系统等）
   - 相关的错误日志或截图

### 💡 功能建议

我们欢迎新功能建议：

1. 创建Feature Request Issue
2. 详细描述功能需求和使用场景
3. 如果可能，提供设计草图或伪代码

### 🔧 代码贡献

#### 开发环境设置

```bash
# 1. Fork并克隆仓库
git clone https://github.com/YOUR_USERNAME/ecommerce-ml-prediction.git
cd ecommerce-ml-prediction

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 安装开发依赖
pip install pytest flake8 black
```

#### 开发流程

1. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **编写代码**
   - 遵循现有代码风格
   - 添加必要的注释
   - 编写单元测试

3. **代码检查**
   ```bash
   # 代码格式化
   black .
   
   # 代码检查
   flake8 .
   
   # 运行测试
   pytest
   ```

4. **提交更改**
   ```bash
   git add .
   git commit -m "feat: 添加新功能描述"
   ```

5. **推送并创建PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## 📝 代码规范

### Python代码风格

- 使用[Black](https://black.readthedocs.io/)进行代码格式化
- 遵循[PEP 8](https://www.python.org/dev/peps/pep-0008/)规范
- 使用有意义的变量和函数名
- 添加类型注解（推荐）

### 提交信息规范

使用[约定式提交](https://www.conventionalcommits.org/)格式：

```
<类型>[可选范围]: <描述>

[可选正文]

[可选脚注]
```

**类型：**
- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具变动

**示例：**
```
feat(model): 添加XGBoost预测模型

- 实现XGBoost分类器
- 添加模型评估指标
- 更新文档说明

Closes #123
```

## 🧪 测试指南

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_model.py

# 生成覆盖率报告
pytest --cov=.
```

### 编写测试

- 为新功能编写单元测试
- 测试文件命名：`test_*.py`
- 测试函数命名：`test_*`
- 使用有意义的断言消息

## 📚 文档贡献

### 文档类型

- **README.md**: 项目概述和快速开始
- **API文档**: 函数和类的详细说明
- **教程**: 使用示例和最佳实践
- **FAQ**: 常见问题解答

### 文档规范

- 使用Markdown格式
- 添加适当的标题层级
- 包含代码示例
- 保持简洁明了

## 🎨 UI/UX贡献

### 设计原则

- **一致性**: 保持视觉风格统一
- **可访问性**: 支持不同设备和用户需求
- **性能**: 优化加载速度和响应性
- **用户体验**: 直观易用的界面设计

### 设计资源

- 颜色方案：莫兰迪紫色系
- 字体：Segoe UI, Microsoft YaHei
- 图标：使用Emoji或SVG图标

## 🔍 代码审查

### PR审查清单

- [ ] 代码符合项目规范
- [ ] 包含必要的测试
- [ ] 文档已更新
- [ ] 无明显性能问题
- [ ] 向后兼容性

### 审查流程

1. 自动化检查（CI/CD）
2. 代码审查（至少1人）
3. 测试验证
4. 合并到主分支

## 🏆 贡献者认可

我们会在以下地方认可贡献者：

- README.md的贡献者列表
- 发布说明中的感谢
- 项目网站的贡献者页面

## 📞 联系方式

如有任何问题，可以通过以下方式联系：

- 创建GitHub Issue
- 发送邮件到项目维护者
- 参与项目讨论区

## 🎉 感谢

感谢所有为项目做出贡献的开发者！你们的努力让这个项目变得更好。

---

**记住：每一个贡献都很重要，无论大小！** 🚀