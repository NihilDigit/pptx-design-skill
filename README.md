# pptx-design-skill

Claude Code Skill：用代码构建演示文稿。drawio 画图 → 导出 EMF/PNG → python-pptx 组装幻灯片。

跨平台支持 Linux / macOS / Windows。

## 工作流

```
.drawio XML ──→ drawio CLI 导出 ──→ python-pptx 组装 ──→ .pptx
                 (EMF / PNG)         (设计体系 + 布局模板)
```

1. 直接编写 `.drawio` XML 文件（mxGraphModel 格式）
2. 通过 drawio Desktop CLI 导出为 EMF（Linux，无损矢量）或 PNG（全平台）
3. 用 python-pptx 脚本组装幻灯片，内置 "Clarity" 设计体系
4. 输出带嵌入图表、视频、演讲备注的 `.pptx`

## 文件结构

```
SKILL.md                        Skill 主入口，4 步工作流 + 跨平台指南
scripts/
  drawio_export.py              跨平台批量导出（自动检测 drawio CLI 路径）
  drawio_to_emf.sh              Linux/macOS EMF 快捷脚本
references/
  helpers.md                    python-pptx helper 函数库（Clarity 设计体系）
  layouts.md                    17 种幻灯片布局模板
  drawio-style.md               drawio 整页图设计规范
```

## "Clarity" 设计体系

与原项目的 NAVY+ACCENT 风格不同，Clarity 追求现代、简洁、高对比度：

| Token | 色值 | 用途 |
|-------|------|------|
| INK | `#0F172A` | 标题，近黑 |
| BODY | `#334155` | 正文 |
| MUTED | `#94A3B8` | 辅助文字 |
| ACCENT | `#3B82F6` | 强调色 |
| SURFACE | `#F8FAFC` | 卡片背景 |

设计原则：
- 左对齐标题，不用居中
- 卡片无边框，用 surface fill 区分层次
- 标签用描边而非实心填充
- 1.2" 左边距，充足留白

## Drawio 图表规范

统一字体 `微软雅黑`（Windows 默认可用），5 色模块体系：

| 角色 | 填充 | 描边 | 场景 |
|------|------|------|------|
| Primary | `#EFF6FF` | `#3B82F6` | 核心模块 |
| Secondary | `#F0FDF4` | `#22C55E` | 数据/输出 |
| Tertiary | `#FFF7ED` | `#F97316` | 外部服务 |
| Neutral | `#F8FAFC` | `#CBD5E1` | 分组容器 |
| Highlight | `#FEF3C7` | `#F59E0B` | 关键决策 |

箭头规则：
- 仅两种形式：直角折线（orthogonal）或圆角折线（curved corners）
- 显式指定出入点（exitX/exitY/entryX/entryY），禁止交叉重叠
- 平行箭头错位 Y 值，双向连接走对侧

5 种布局模式：分层架构、流水线、中心辐射、对比、决策树。

## 安装

作为 Claude Code Skill 使用：

```bash
claude skill install pptx-drawio-builder.skill
```

或直接将本仓库克隆到 `~/.claude/skills/pptx-drawio-builder/`。

## 依赖

| 工具 | 用途 | 平台 |
|------|------|------|
| [draw.io Desktop](https://github.com/jgraph/drawio-desktop) | 图表导出 CLI | 全平台 |
| python-pptx + Pillow | 幻灯片生成 | 全平台 |
| pdftocairo + inkscape | EMF 转换 | Linux |
| ffmpeg | 视频封面提取 | 全平台（可选） |

## License

GPL-3.0
