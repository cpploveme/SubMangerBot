# Submanger

Submanger Bot 是一个管理订阅链接的机器人 可以帮助使用者更方便地管理订阅
> Submanger Bot 本身只是一个订阅管理器 不具备任何代理能力 也不提供任何订阅链接

## 使用前说明

这是更新截止到2023年的Bot 尽管本项目完全手写无AI 但它不支持异步容易卡死 代码极度混乱同一个功能写十遍无法维护 因此在闭源分发停止两年后于此开源

如果使用时遇到任何问题 请勿提出任何issue 因为不再维护

如果您需要更多稳定的高级功能 欢迎联系 [@Temp_ChatBot](http://t.me/Temp_ChatBot)

## 环境要求
最低配置 1c0.5g\
需连接Telegram服务器 请自行配置代理服务\
~~目前仅支持 `x86` 架构的 `Linux/Windows` 系统 如需其他系统或架构的打包请私聊~~ 开源了随便玩哈

## 安全

Submanger Bot 仅会在 config.yaml 文件中存储配置文件信息 在 My_sub.db 中存储订阅链接 在 Airport.list 文件中存储机场名称

Submanger Bot 的全部数据仅会存储在本地和Telegram服务器(聊天记录) 除拥有ssh账密,Telegram Bot Token或超管授予权限外无法通过其他方式从Bot获取数据 ~~真没后门 你可以反一下试试~~ 开源了反尼玛币

Submanger Bot 仅会连接 Telegram服务器 订阅链接服务器 subconverter服务器  除此之外不会连接任何其他服务 ~~你可以自己抓包试试~~ 直接看代码好吧

## 安装

> 看看有啥 requirement 自己装一下吧

~~### 一键脚本~~

~~一键脚本目前仅支持 `Debian/Ubuntu` 系统 其他系统请自行手动下载~~

~~脚本启动后会下载bot本体 配置进程守护 `screen` 并要求填写 `授权Token` `Telegram Bot Token` `超管Telegram id`~~

~~目前的一键脚本请在群内置顶获取~~ 这个旧版开源的 没必要一键脚本

### ~~手动下载~~

~~Submanger Bot 直接以二进制单文件形式提供 目前仅支持 `Linux x86/Windows x86` 系统~~
~~如果需要其他架构的打包 请私聊我~~

## 配置
> 由于机器人的配置比较复杂 建议搭配 `readme.config.yaml` 与 [#使用](#使用方法) 查看

### 必要配置

以下配置必须设置 否则 Bot 将无法启动:

- `token`: 你的 Bot 授权Token
- `telegramtoken` 你的 Telegram Bot Token（请于 `@BotFather` 获取）
- `administrator`： 超级管理员id

如以一键脚本安装 会要求填写以上配置

### 可选配置

请自行查看 `readme.config.yaml` ~~其实就是懒得写~~

### 数据库
`My_sub.db` : 使用Sqlite数据库 以明文方式存储订阅到本地\
`Airport.list` : 机场名称数据库 每行格式为 `域名 机场名` Bot不会提供数据库 请自行收集
> 在识别机场名称时 会先从数据库中查找对应域名 若未找到则会尝试自动识别域名 但自动识别到的机场名并不会添加进数据库 

## 使用
### 游客
无授权者即游客 在关闭唯一管理模式时 (`adminOnlyMode` 为 0) 可以使用如下指令:
```
查询订阅 /subinfo
转换订阅 /convert
注册试用 /free
消息延迟 /ping
版本信息 /version
```
#### /subinfo <链接>

查询订阅链接信息 显示机场名称 流量 过期时间等信息\
可回复包含订阅链接的消息或写在后面 一次可查询多个订阅 会自动去除订阅转换与短链接并去重\
订阅不会写入日志或数据库中

#### /convert <链接/节点>

订阅转换 可转换链接或节点\
可回复包含链接或节点的消息或写在后面 一次可转换多个 会自动去除订阅转换与短链接并去重

#### /free <链接/域名>

获取白嫖订阅 仅支持获取使用V2board/SSpanel的无验证机场的试用订阅

#### /ping

获取Bot的消息延迟 会测试多次取平均值

#### /version

获取Bot的版本信息

### 管理
授权者即管理 至少可以使用如下指令:
```
发送消息 /chat 内容
发送通知 /notice 内容
添加订阅 /add 订阅链接 备注
删除订阅 /del 编号
查找订阅 /search 内容
更新订阅 /update 编号 订阅链接 备注
整理订阅 /sort
自动添加 /auto 回复/内容
获取订阅 /get 编号
页面跳转 /page 页数
交换订阅 /swap 编号 编号
修改备注 /comment 编号 备注
测活订阅 /prune
注册任务 /register
取消任务 /unregister
离开群聊 /leave
```

#### /chat /notice <内容>

使用Bot对全部授权者发送消息

#### /add <订阅链接> <内容>

向订阅库添加订阅

#### /del <编号> <可选:编号2> <可选:编号3>... 

删除订阅库内对应编号的订阅

#### /search <关键词> <可选:页数>

显示说明或链接包含关键词的订阅 每页共20个

#### /update <编号> <订阅链接> <备注>

更新特定编号的订阅的信息

#### /sort

在使用 `/del` 删除订阅后 该订阅原来位置的编号会空缺 使用本命令可以使编号连贯

#### /auto

自动添加订阅 可以回复或者后面以空格分开 可一次添加多个\
对于每个订阅 会先尝试识别机场名 然后尝试获取订阅流量信息

#### /get <编号> (等效于点击按钮获取)

获取特定编号的订阅 如果是已信任群组 (参见 [#/trust](#/trust)) 则会发在群组中 否则发在私聊

#### /page <页数>

在使用 `/search` 命令搜索后 通过回复Bot的查找消息可进行页数跳转

#### /swap <编号> <编号>

交换两个不同编号的订阅信息

#### /comment <编号> <说明>

修改特定编号订阅的备注说明

#### /prune <可选:关键词>

手动测活订阅 可使用关键词限制测活的具体订阅

#### /register <可选:关键词>

将该群组或私聊添加进订阅监测任务中 可使用关键词限制监测显示的订阅

#### /unregister

将该群组或私聊从订阅监测任务中删除

#### /leave

使 Bot 从群组中离开

### 超管
超管具有最大的操作权限 在启动时读取 可以使用的命令如下:
```
给予授权 /grant
取消授权 /ungrant
清除授权 /grantclear
授权列表 /list
信任群组 /trust
取消信任 /distrust
赠与订阅 /invite
添加域名 /addkeyword
删除域名 /delkeyword
获取数据 /database
安装数据 /install
查询日志 /log
重载配置 /reload
保存配置 /save
获取配置 /value
设置配置 /set
```

#### /grant <可选:Telegram User id 1> <可选:Telegram User id 2>...

回复一个用户的消息或后面写入用户id可将此用户的权限提升为管理员 会被写入到 Config 的 `admin` 中

#### /ungrant <可选:Telegram User id 1> <可选:Telegram User id 2>...

回复一个用户的消息或后面写入用户id可将此用户的权限降低为游客 会从 Config 的 `admin` 中删除

#### /grantclear

清理所有人的管理员权限

#### /list

查看管理员列表 等效于 `/value admin`
 
#### /trust

将该群组设定为可信任群组 获取的订阅会发在群组中 否则会发在获取者的私聊 会被写入到 Config 的 `trust` 中

#### /distrust

将该群组设定为非可信任群组 会从 Config 的 `trust` 中删除

#### /invite <编号>
对于该功能 若 `allowAdminToInvite` 值为 1 则管理员也可使用此命令\
通过回复他人消息来给予他人订阅库中特定订阅

#### /addkeyword <域名> <机场名>

将机场名信息添加进数据库

#### /delkeyword <域名>

将机场名信息从数据库中删除

#### /database <密码>

获取订阅数据库

#### /log <密码>

获取日志

#### /install <密码>

通过回复订阅数据库文件 来恢复原有的数据库

#### /reload

若 Bot 未关闭 而修改了配置文件 可使用此命令重新读取

#### /save

保存 Bot 当前配置

#### /value <路径>

获取配置文件中特定路径的值

需要对 `config.yaml` 很熟悉\
不同级的路径用 `.` 分开


如 `convert` 的配置为:
```
convert:
  backend: https://api.nexconvert.com/
  config: https://cdn.jsdelivr.net/gh/lhl77/sub-ini@main/tsutsu-mini-gfw.ini
  target: clash
  parameter: &emoji=true&remove_emoji=false&interval=3600&udp=true&expand=false&list=false&scv=true&fdn=true&new_name=true
```
则读取的值为:
```
/value convert
返回:
[✅][配置 convert 的值为]

{'backend': 'https://api.nexconvert.com/', 'config': 'https://cdn.jsdelivr.net/gh/lhl77/sub-ini@main/tsutsu-mini-gfw.ini', 'target': 'clash', 'parameter': '&emoji=true&remove_emoji=false&interval=3600&udp=true&expand=false&list=false&scv=true&fdn=true&new_name=true'}
```

\
如 `cron` 的配置为:
```
cron:
  enable: 1
  interval: 3600
  list:
  - 123456
  - -789: 关键词
```
则读取的值为:
```
/value cron.interval
返回:
[✅][配置 cron.interval 的值为]

3600
```

#### /set <路径> <值>

设置配置文件中特定路径的值

## 其他

### 鉴权方式

Bot 采用本地鉴权 读取Bot用户名后加密并与token匹配 若不一致则自动退出程序无法启动\
授权后可注销Bot重新注册同一用户名的Bot 但无法更换Bot用户名

### 命令缩写
对于 `/subinfo` `/chat` `/notice` `/add` `/del` `/search` `/update` 命令\
可直接使用首字母 `/s` 使用命令 (`/subinfo` 为 `/i`)

### 订阅概要

对于搜索后的对于面板 如果可以翻页 点击页数显示按钮即可显示订阅概要

### 订阅监测

如需使用监测功能 请将 `cron.enable` 的值设置为 1
`cron.delay` 为监测延时 每获取一轮订阅后延迟一段时间重新获取

为避免短时间内多次获取同一机场订阅 监测会打乱顺序逐条获取



