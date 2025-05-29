### 把自己关注的股票加入自选，设置关注目标价等,炒股有风险，投资需谨慎呐！
**1.安装环境**
```
1.1 安装node，我这20版本，14版本以上即可，前端依赖可以用npm，也可以用yarn
1.2 安装python3，当前安装版本为python 3.13.3

```

**2.创建虚拟环境**
```
MAC:
创建虚拟环境：python3 -m venv venv
激活虚拟环境：source venv/bin/activate

windows：
创建虚拟环境：python3 -m venv venv
激活虚拟环境：venv\Scripts\activate.bat
```

**3.初始化安装依赖：**
* ```pip install -r requirements.txt```

*** 4.给vue安装依赖 ***
```
1.打开/templates/vue的终端
2.npm install
```

***4.启动：***
**4.1分开启动**
```
1.打开根目录终端，激活虚拟环境
2.启动python项目：python3 manage.py runserver
3.打开/templates/vue的终端：npm run dev 
4.打开网页:https://localhost:3000/
```
**4.2一键启动**
```
1.根目录下开启终端
2.MAC: npm run start  ||  yarn start
3.Windows: npm run dev  ||  yarn dev
```

### 页面：
|#|页面|预览|
|---|---|----
|1|`炒股框架逻辑记录页面 你配吗`|![](/gitImage/recode.png "炒股框架逻辑记录页面")
|2|`股票列表页面       `|![](/gitImage/info.png "股票列表页面")
|3|`新增股票弹窗       `|![](/gitImage/add.png "新增股票弹窗")
|4|`其他页面          `|`其他页面太多就不一一列举了`








