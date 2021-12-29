请使用抓包工具（如 Fiddler）获取 pid 和 Authorization 后再使用本工具。配置文件格式如下

```json
{
  "auth": "Bearer XXXXXXXXX",
  "pid": "XXXXXXX",
  "name": "张三",
  "no": "22XXXXX"
}
```

使用配置文件调用脚本的格式如下

```shell
main.py config.json
```

您可以结合命令行脚本使用本工具以实现自动化。
