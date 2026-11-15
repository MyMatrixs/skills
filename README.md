# MyMatrixs skills

这个仓库用于集中管理我的 Codex skills。每个 skill 独立放在仓库根目录下，以 `SKILL.md` 为入口；以后可以继续添加其他 skill，不会混在一起。

| Skill | 用途 |
| --- | --- |
| [ai-video-production](ai-video-production/SKILL.md) | 规划、生成、拼接和审阅可追溯的 AI 视频项目，管理人物、场景参照、原生音视频和版本化成片。 |

## 安装

克隆仓库后，把需要的 skill 目录复制到 Codex 的 skills 目录。在 Windows PowerShell 中：

```powershell
git clone https://github.com/MyMatrixs/skills.git
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse -Force .\skills\ai-video-production "$env:USERPROFILE\.codex\skills"
```

视频 skill 的 AutoDL 辅助脚本是可选的。如需使用，在已安装的 skill 目录中将 `.env.example` 复制为 `.env`，填写自己的 token 和实例 UUID。`.env` 只保存在本机，不会提交到这个仓库。

## 添加其他 skill

在仓库根目录新建一个以 skill 命名的目录，并放入自己的 `SKILL.md`。可复用的参考文档、脚本和小型模板放在该目录内；项目视频、生成素材、凭证和机器缓存放在仓库外。
