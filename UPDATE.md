# FF.PyAdmin

## v1.2

**2020-07-10 更新:**

- 升级所有包为最新版本(Python3.8测试通过): `Flask==1.1.2, WTForms==2.3.1`, 旧依赖库(正常可用): `requirements.old.txt`
- 升级 `LayUI==2.5.6`
- 自动表格 `$.autoTbl` 增加属性 `colsFields`, 可指定要显示的表格字段. 增加属性 `colsAlign` 指定默认对齐方式
- 新增示例: 真分页, 真排序, 前端增加字段, 后端隐藏字段, 指定显示字段, 控制表格字段显示顺序, 指定对齐方式等, 详见 `/bgp` 及前后端注释
- 异步请求 `$.mkAjax` 增加回调方法 `done_err`, Ajax 请求成功但返回 `ok!=1` 时可触发
- 增加信号中异步任务示例: `/async_signal_demo`
- 使用 `flask_wtf` 原生 `CSRFProtect`, 增加例外示例: `/log/csrf_exempt_demo`
- 表单校验增加 `FloatRound` 用于校验浮点数, 金额等, 银行家舍入法, 默认保留2位小数
- 增加默认消息页面: `base-msg.html`
- 增加开发环境快捷启动方式: `python3 dev.py`, `PyCharm Script path` 可指向该文件
- 增加助手函数: `get_round` `get_ymd` `get_next_month_first` `get_month_last` `get_last_month_last`
- 增加模板函数: `get_date`, 示例表单默认昨天日期: `<input value="{{ get_date(out_fmt="%Y-%m-%d", add_days=-1) }}">`
- 对称加密类库更新: `AESCipher`, 增加助手函数, 用法详见注释
- `flask.json` 增加 `JSONEncoder` 对 `Decimal` 支持
- 数据库日志服务改用 `flask.json`, 以适应常见各类数据类型
- ORM 增加 `hide_keys_dicts` 方法, 将 `.all()` 转为字典并隐藏指定字段
- 调试模式且 Ajax POST 请求时将 Response JSON 显示在控制器方便调试
- 修正 `logger` 文件日志级别

## v1.1

**2019-12-20 更新:**

- 新增配置项: `MAIL_OPEN` 邮件发送开关, 与邮件配置项配合使用, 默认 `False`
- 新增配置项: `EXCEPTION_LOG_CODE` 触发记录文件日志的响应码, 默认 `[500]`
- 新增配置项: `SYS_ROLE_ID` 保留角色(权限组) ID 设置, 禁止将其他用户授权为该角色, 默认 `0`
- 用户表使用 `id` 字段配合 `flask_login` (原使用 `job_number` 字段)
- 用户权限组关联使用 `role_id` 字段 (原使用 `role` 标识)
- 日志表增加 `log_content` 字段, 用于记录日志详情, 日志记录方式见 ASNCharge.add()
- 数据库操作使用 `replace` 方法新增数据时, 确保总能获取到最新插入数据后的自增主键 ID
- 自定义信号机制(事件订阅-发布), 使用见示例代码: 系统管理事件, 用户登录成功事件
- 封装了邮件发送类, 基于 `flask_mail`, 支持邮件内容按模板渲染(HTML, TEXT), 支持异步发送邮件(默认)
- 附带了一个通用的邮件模板, 通过手机系统邮件/钉钉/QQ/微信/Foxmail/Outlook等邮件客户端兼容性测试

