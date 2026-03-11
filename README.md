# TPShop 接口自动化测试项目

## 📋 项目简介

基于 **Python + Pytest + Requests + Allure** 的接口自动化测试框架，针对 TPShop 开源商城系统进行全面的接口测试，覆盖用户模块、购物车模块、订单模块及完整业务流程测试。

---

## 🏗️ 项目结构
```text
tpshop/
├── api/ # 接口封装层
│ ├── init.py
│ ├── login_api.py # 登录/退出接口
│ ├── register_api.py # 注册接口
│ ├── cart_api.py # 购物车接口（添加/修改/删除/清空）
│ └── order_api.py # 订单接口（cart1/cart2/cart3）
│
├── common/ # 公共工具层
│ ├── init.py
│ ├── assert_tools.py # 通用断言方法
│ ├── read_json_file.py # JSON测试数据读取
│ └── db_helper.py # 数据库操作（清空购物车等）
│
├── data/ # 测试数据层（JSON驱动）
│ ├── login_data.json # 登录测试数据
│ ├── register_data.json # 注册测试数据
│ ├── cart_data.json # 添加购物车测试数据
│ ├── change_cart_data.json # 修改购物车数量测试数据
│ ├── order_data.json # 提交订单测试数据
│ └── business_flow_data.json # 业务流程测试数据
│
├── scripts/ # 测试用例层
│ ├── init.py
│ ├── test_login.py # 登录测试（5个场景）
│ ├── test_logout.py # 退出测试（3个场景）
│ ├── test_register.py # 注册测试（7个场景）
│ ├── test_cart.py # 添加购物车测试（13个场景）
│ ├── test_change_cart.py # 修改购物车数量测试（6个场景）
│ ├── test_order.py # 提交订单测试（9个场景）
│ └── test_business_flow.py # 完整业务流程测试（8个场景）
│
├── reports/ # 测试报告（运行后自动生成）
│ ├── allure_results/ # Allure 原始数据
│ └── allure_html/ # Allure HTML 报告
│
├── .gitignore # Git 忽略文件
├── config.py # 项目配置（BASE_DIR等）
├── pytest.ini # Pytest 配置
├── requirements.txt # 项目依赖
├── Jenkinsfile # Jenkins Pipeline 配置
└── README.md # 项目说明文档
```


---

## 🛠️ 技术栈

| 技术 | 说明 |
|------|------|
| Python 3.14 | 编程语言 |
| Pytest | 测试框架 |
| Requests | HTTP 请求库 |
| Allure | 测试报告 |
| PyMySQL | 数据库操作 |
| Jenkins | 持续集成 |
| GitHub | 代码仓库 |

---

## 🧪 测试覆盖

### 用户模块

| 模块 | 测试场景 | 用例数 |
|------|----------|--------|
| 用户登录 | 登录成功、未注册手机号、密码错误、密码为空、手机号为空 | 5 |
| 用户退出 | 登录后正常退出、未登录直接退出、退出后再次退出 | 3 |
| 用户注册 | 注册成功、两次密码不一致、手机号已注册、密码为空、确认密码为空、密码过短、密码过长 | 7 |

### 购物车模块

| 模块 | 测试场景 | 用例数 |
|------|----------|--------|
| 添加购物车 | 正常添加、添加多个、重复添加、不同商品、不存在商品、数量为0、负数、超库存、id为空、id为字符、未登录、小数、无参 | 13 |
| 修改数量 | 正常修改、数量为0、负数、超大值、不存在商品、数量匹配验证 | 6 |

### 订单模块

| 模块 | 测试场景 | 用例数 |
|------|----------|--------|
| 提交订单 | 正常提交、未登录、购物车为空、无收货地址、无支付方式、不存在地址、无参、跳过确认、重复提交 | 9 |

### 业务流程

| 模块 | 测试场景 | 用例数 |
|------|----------|--------|
| 完整流程 | 正常下单(1个)、正常下单(多个)、不同商品下单、修改数量后下单、未登录下单、空购物车下单、跳过确认下单、下单后退出再下单 | 8 |

**总计：51+ 个测试用例**

---

## 🚀 快速开始
```bash
1. 克隆项目
git clone https://github.com/schicksal2719/tpshop-api-test.git
cd tpshop-api-test
2. 安装依赖
Bash

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
3. 配置数据库连接
修改 common/db_helper.py 中的数据库连接信息：

Python

conn = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    password="root",        # 改成你的数据库密码
    database="tpshop",      # 改成你的数据库名
    charset="utf8"
)
4. 运行测试
Bash

# 运行所有测试
pytest scripts/ -v -s --alluredir=./reports/allure_results --clean-alluredir

# 运行单个模块
pytest scripts/test_login.py -v -s
pytest scripts/test_register.py -v -s
pytest scripts/test_cart.py -v -s
pytest scripts/test_order.py -v -s
pytest scripts/test_business_flow.py -v -s
5. 查看 Allure 报告
Bash

allure serve ./reports/allure_results
```

##  📊 Allure 报告展示

报告按功能模块分类展示：
```text
📁 用户模块
├── 📁 用户登录（5个用例）
├── 📁 用户退出（3个用例）
└── 📁 用户注册（7个用例）

📁 购物车模块
├── 📁 添加商品到购物车（13个用例）
└── 📁 修改购物车商品数量（6个用例）

📁 订单模块
└── 📁 提交订单（9个用例）

📁 业务流程
└── 📁 登录-加购-下单完整流程（8个用例）
```
每个用例包含：
```text
✅ 详细的测试步骤
📎 请求参数和响应数据附件
📋 断言对比（预期 vs 实际）
🏷️ 严重级别标记
🔧 框架设计
```
### 分层架构
```text
┌─────────────────────────────┐
│      测试用例层 (scripts/)   │  ← 测试逻辑
├─────────────────────────────┤
│      接口封装层 (api/)       │  ← 接口调用
├─────────────────────────────┤
│      公共工具层 (common/)    │  ← 断言、数据读取、数据库
├─────────────────────────────┤
│      测试数据层 (data/)      │  ← JSON 数据驱动
└─────────────────────────────┘
```

### 数据驱动

所有测试数据存储在 JSON 文件中，新增用例只需添加 JSON 数据，无需修改代码：
```JSON
{
    "title": "登录成功",
    "username": "13800138006",
    "password": "123456",
    "verify_code": "8888",
    "expected_status_code": 200,
    "expected_status": 1,
    "expected_msg": "登陆成功"
}
```
### TPShop 

登录和注册需要验证码，项目中通过修改后端代码设置了万能验证码 8888，方便自动化测试。

## 🔄 Jenkins 持续集成

自动化流程

```text

代码推送到 GitHub
       ↓
Jenkins 检测到变更
       ↓
自动拉取最新代码
       ↓
安装项目依赖
       ↓
运行 Pytest 测试
       ↓
生成 Allure 报告
       ↓
查看测试结果
```
## ⚙️ Jenkins 配置

* **构建触发**：GitHub Webhook (代码推送触发) / 定时构建 (Poll SCM)
* **构建工具**：Windows Batch Command
* **测试报告**：Allure Jenkins Plugin

---

## 📝 注意事项

> [!IMPORTANT]
> 在执行测试前，请务必确认以下环境配置，以保证测试成功率：

* **服务检查**：运行测试前确保 TPShop 服务已正常启动。
* **数据库配置**：确保 `common/db_helper.py` 中的数据库连接信息（IP、端口、账号、密码）正确。
* **数据隔离**：
    * **注册模块**：用例采用动态生成手机号逻辑，避免因重复注册导致失败。
    * **订单模块**：提交订单测试前会自动调用接口清空购物车，保证测试环境干净。
* **校验逻辑**：`expected_msg` 需根据 TPShop 环境的实际返回信息（如中文/英文）进行微调。

---

| Bug | 描述 | 严重程度 |
| :--- | :--- | :--- |
| **购物车未校验商品是否存在** | 添加不存在的商品返回"加入购物车成功" | 高 |
| **购物车未校验商品数量** | 数量为0、负数、小数均返回成功 | 高 |
| **未登录可添加购物车** | 未登录状态下添加商品返回成功 | **严重** |
| **购物车未校验库存** | 数量超过库存仍返回成功 | 高 |
| **无参数可添加购物车** | 不传任何参数返回成功 | 高 |