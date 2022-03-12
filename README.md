# 《今日人品》

不基于 `random.randint(0, 100)` 的今日人品

## 使用

游戏内输入 `!!jrrp` 即可获取到今日人品

### 配置

配置文件位于 `config/jrrp/config.json`

默认配置为：

```json
{
    "enable": true,
    "online_mode": true,
    "command": "!!jrrp"
}
```

`enable`：是否启用今日人品

`online_mode`：是否从 Mojang 获取玩家的 在线UUID

`command`：今日人品的指令

## 许可 

使用 [GPL-3.0-or-later](./LICENSE) 进行许可
