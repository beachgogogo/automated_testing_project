# 电商系统接口自动化测试项目

## 项目概述
基于 Postman 的电商系统 API 接口测试项目，覆盖用户、登录、商品、订单四大模块，
设计并实现 18+ 条测试用例，涵盖正常场景与异常场景。

## 技术栈
- Postman / Newman
- REST API 测试
- Bearer Token 认证机制

## 测试范围
| 模块     | 用例数 | 覆盖场景                     |
| -------- | ------ | ---------------------------- |
| 用户模块 | 5      | 查询、异常ID、边界值         |
| 登录认证 | 4      | 成功/失败/空值/错误密码      |
| 商品模块 | 1      | 列表查询                     |
| 订单模块 | 8      | 认证校验、创建订单、参数异常 |

## 项目亮点
- 使用 Postman Environment 实现环境隔离，支持快速切换测试环境
- 使用 Tests 断言实现响应状态码、字段完整性、安全性校验（密码不外泄）
- 通过 Collection Runner 批量执行，提升回归测试效率
- 测试过程中发现后端订单 ID 生成重复的设计缺陷

## 如何运行
1. 导入 `Ecommerce_API_Test.json` 到 Postman Collections
2. 导入 `Local_Ecommerce.json` 到 Postman Environments
3. 启动后端服务（Flask app.py）
4. 在 Collection Runner 中选择环境并执行