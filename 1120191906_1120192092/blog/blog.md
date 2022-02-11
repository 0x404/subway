# 地铁导航博客



## 1. 团队成员

> 成员1：
>
> * 姓名：曾群鸿
> * 学号：1120192092
>
> 成员2：
>
> * 姓名：肖誉
> * 学号：1120191906



## 2. 成果展示

### 1.1 命令行成果

​	完成了命令行参数的漫游，通过\b参数完成两站点间线路查询，\z参数完成通过文件测试，\a参数完成从一个点线路漫游。

| ![](http://image-hosting-404.oss-cn-beijing.aliyuncs.com/img/gui_result.png) | ![](http://image-hosting-404.oss-cn-beijing.aliyuncs.com/img/gui_result_z.png) | ![](http://image-hosting-404.oss-cn-beijing.aliyuncs.com/img/gui_result_a.png) |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |



### 1.2 GUI成果

![](http://image-hosting-404.oss-cn-beijing.aliyuncs.com/img/GUI.jpg)

### 1.3 web端成果

web端服务已经部署在云服务器上，请访问http://0x404.tech, 进行体验



## 3. PSP耗时

| PSP2.1                                  | Personal Software Process Stages        | 预估耗时（分钟） | 实际耗时（分钟） |
| --------------------------------------- | --------------------------------------- | ---------------- | ---------------- |
| Planning                                | 计划                                    | 30               | 20               |
| · Estimate                              | · 估计这个任务需要多少时间              | 20               | 10               |
| Development                             | 开发                                    | **1200**         | 890              |
| · Analysis                              | · 需求分析 (包括学习新技术)             | 200              | 250              |
| · Design Spec                           | · 生成设计文档                          | 60               | 120              |
| · Design Review                         | · 设计复审 (和同事审核设计文档)         | 120              | 20               |
| · Coding Standard                       | · 代码规范 (为目前的开发制定合适的规范) | 40               | 45               |
| · Design                                | · 具体设计                              | 300              | 280              |
| · Coding                                | · 具体编码                              | 700              | 800              |
| · Code Review                           | · 代码复审                              | 120              | 50               |
| · Test                                  | · 测试（自我测试，修改代码，提交修改）  | 120              | 150              |
| Reporting                               | 报告                                    | 120              | 20               |
| · Test Report                           | · 测试报告                              | 120              | 80               |
| · Size Measurement                      | · 计算工作量                            | 40               | 30               |
| · Postmortem & Process Improvement Plan | · 事后总结, 并提出过程改进计划          | 120              | 100              |
|                                         | 合计                                    | **3190**         | 2735             |



## 4. 需求分析

#### 4. 1功能需求

##### 4.1.1 第一阶段

- 输入起点、终点 输出一条有效路径 输出换乘站换乘的线路名称
- 输入一个站点 找到一条路径漫游整个地铁线路
  - 录入北京地铁线路 将文本信息读入成结构化的线路信息(Txt -> Line)
  - 将站点名称作为**唯一标识**，建立从名称到边、名称到站点类的映射
  - 按照地铁线路信息用邻接表存储整张图
    - 地图可以理解为无向图，找有效路径可以转换为边权为1的最短路
    - 地铁特点是没有重复边，因此站与站之间的边属于唯一的一条线路
    - 判断换乘只需知道前后两条边是否属于统一线路
  - 解析用户输入 找到起点，终点
  - 通过宽搜找到最短路，逆序存储路线
  - 路线解码，如果一个站点前后的边所属路线不一致，则在此站点换乘

##### 4.1.2 第二阶段

* 输入起点，给出一条遍历所有站点的路线
  * 找到经过站点数量最少的路线
  * 如何找到更优的方法

##### 4.1.3 第三阶段

* 将前面两个阶段的功能以图形界面展示
* 给定一个站点名，确定该站点在图像上的位置
  * 使用像素坐标作为站点在图像上的位置
  * 计算像素坐标的相对坐标，以适应不同图像大小
* 给定一个相对坐标列表，在图像上打印坐标列表中的每个坐标点
* 实现从一个站点名列表到站点相对坐标列表的转换
* 实现用户友好的查询站点等信息的提交界面

#### 4. 2DFD图

- 顶层数据流图
  ![DFD1](https://image-hosting-404.oss-cn-beijing.aliyuncs.com/img/DFD1.jpg)
- 二层数据流图
  ![DFD2](https://image-hosting-404.oss-cn-beijing.aliyuncs.com/img/DFD2.jpg)

#### 4.3 用例图

![](http://image-hosting-404.oss-cn-beijing.aliyuncs.com/img/example.png)

#### 4.4 性能需求

- 在人能够承受的时间范围内找到可行路线

#### 4.5 正确性需求

- 用户输入正确是能找到一条可以乘坐的路线
- 不出现错误的站点连接
- 不出现错误的站点



## 5. 接口设计

### 5.1 核心程序接口

#### 5.1.1 概述

##### Station

对地铁站进行封装

| 数据名称     | 数据类型 | 描述         |
| ------------ | -------- | ------------ |
| station_name | str      | 站名称       |
| trans        | Bool     | 是否为换乘站 |

| 接口名称       | 参数列表 | 返回值 | 描述             |
| -------------- | -------- | ------ | ---------------- |
| name(self)     |          | str    | 获得station_name |
| is_trans(self) |          | Bool   | 获得trans        |

##### Edge

两个相邻站点间的连接

| 数据名称     | 数据类型 | 描述         |
| ------------ | -------- | ------------ |
| st_j         | str      | 当前边终点站 |
| line_belongs | str      | 所属线路名称 |

| 接口名称         | 参数列表 | 返回值 | 描述             |
| ---------------- | -------- | ------ | ---------------- |
| station_to(self) |          | str    | 获得st_j         |
| belong_to(self)  |          | str    | 获得line_belongs |

##### Line

一条地铁线路，记录线路名、环状信息和所有站点

| 数据名称  | 数据类型 | 描述               |
| --------- | -------- | ------------------ |
| line_name | str      | 线路名称           |
| st_list   | list     | 线路上包含站点列表 |
| ring      | Bool     | 是否为环形线路     |

| 接口名称           | 参数列表 | 返回值 | 描述          |
| ------------------ | -------- | ------ | ------------- |
| name(self)         |          | str    | 获得line_name |
| is_ring(self)      |          | Bool   | 获得ring      |
| station_list(self) |          | list   | 获得st_list   |

##### SubwaySys

地铁系统

| 数据名称 | 数据类型              | 描述                 |
| -------- | --------------------- | -------------------- |
| str2st   | dict (str -> Station) | 站点名称 -> 站点类   |
| nexto    | dict (str -> Edge)    | 站点名称 -> 相连的边 |
| lines    | list(line)            | 线路集合             |

| 接口名称                                       | 参数列表              | 返回值 | 描述                                   |
| ---------------------------------------------- | --------------------- | ------ | -------------------------------------- |
| add_line(self, line)                           | (Line)                |        | 加入一条线路                           |
| _link(self, st_i, st_j, edge_belong)           | (Station,Station,str) |        | 连接st_i和st_j，未出现的站点存入str2st |
| get_edge_belongs(self, st_i, st_j,edge_belong) | (str,str,str)         | str    | 输入两站点名称，返回线路名称           |
| is_next(self, st_i, st_j)                      | (str,str)             | Bool   | 返回两站点是否相                       |
| travel_path_from(self, start)                  | (str)                 | list   | 返回从某站点遍历的路径                 |
| shortest_path(self, start, end)                | (Station,Station)     | list   | 从Start到End搜索一条经历最少站点的路   |
| walk_side(self, file_path)                     | (str)                 |        | 读测试文件路径，进行测试               |

##### utils

| 接口名称                    | 参数列表 | 返回值     | 描述                                               |
| --------------------------- | -------- | ---------- | -------------------------------------------------- |
| load_lines(data_path)       | (str)    | list[line] | 从项目文本中读取相关地铁线路，组织成Line的集合返回 |
| load_station_pos(data_path) | (str)    | list[x,y]  | 从文本中读出站点坐标，返回站的坐标集合             |
| load_test_file(data_path)   | (str)    | list[str]  | 根据空格分割字符串                                 |
| load_test_file(data_path)   | (str)    | list[str]  | 从测试文件中找到漫游路径                           |

##### Solution

| 接口名称                              | 参数列表       | 返回值    | 描述                                 |
| ------------------------------------- | -------------- | --------- | ------------------------------------ |
| get_line_belong(st_i, st_j, nexto)    | (str,str,map)  | str       | 返回两个站点所在线路名称             |
| is_nexto(st_i, st_j, nexto)           | (str,str,map)  | Bool      | 两个站点是否连接                     |
| docorate_path(path, nexto)            | (list,map)     | list      | 从遍历的最短路解生成换乘信息         |
| shortest_path(start, end, nexto)      | (str,str,map)  | list      | 从两站点找到一条最短路               |
| travel_path_from(start, nexto, lines) | (str,map,list) | list      | 从某站点开始漫游所有站点             |
| shortest_path(self, start, end)       | (str,str)      | list      | 从Start到End搜索一条经历最少站点的路 |
| verify_path(path, nexto)              | (str,map)      | {"stats"} | 从测试文件中判断当前文件是否成功     |



#### 5.1.2 UML

类图：

![](http://image-hosting-404.oss-cn-beijing.aliyuncs.com/img/uml1.png)

泳道图：

![](http://image-hosting-404.oss-cn-beijing.aliyuncs.com/img/shortest_act.png)

### 5.2 web程序接口

### 5.3.1 概述

web程序使用django框架作为后端，利用django自动生成的基本框架，主要完成路由的定义，前端界面的设计，在已有的核心程序subway中提供两个询问接口，供django的view模块调用。

#### 前端界面接口

前端界面主要的接口为向后端提交最短路线查询接口，以及提交遍历路径查询接口。

1. 提交最短路线查询接口，通过获取页面文本输入框的信息，利用`ajax`向指定路由提交，并等待后端响应。

   对响应结果进行判断处理，如果返回一个正常的绘画路径，则进行画布的输出，否则进行异常处理。

2. 提交遍历路径查询接口，通过获取页面文本输入框的信息，利用`ajax`向指定路由提交，并等待后端响应。

   对响应结果进行判断处理，如果返回一个正常的绘画路径，则进行画布的输出，否则进行异常处理。

#### 后端接口

后端接口主要分为django路由接口，django的view模块接口

1. django路由接口：通过路由解析，将前端发送的不同请求转到view模块中不同函数进行处理
2. view模块接口：调用核心程序提供的查询接口，将查询结果以HttpResponse返回

#### 核心程序接口

程序入口为subway.py，在core模块中已经完成所有功能的实现，在subway.py中增加两个web查询接口，以供django后端进行调用。

1. 查询最短路径接口，通过core模块的查询最短路径算法，得到一个站点路径名列表，再通过utils模块中获取站点在图上的相对坐标，返回结果。
2. 查询遍历路径接口，通过core模块的查询遍历路径算法，得到一个站点路径名列表，再通过utils模块中获取站点在图上的相对坐标，返回结果。

### 5.3.2 UML

web程序活动图如下

![](http://image-hosting-404.oss-cn-beijing.aliyuncs.com/img/web_pic1.png)

## 6. 测试

我们本次结对项目的测试基于[pytest](https://docs.pytest.org/en/6.2.x/)进行，该工具能自动检查代码中的测试模块，通过`xxx_test.py`标识一个测试文件，`test_yyy()`标识一个测试函数，pytest会扫描目录中所有以`_test`为后缀的文件，并执行该文件中的所有测试函数，自动化完成测试。

为保证代码的正确性，我们要求每完成一个新的功能，都需要由功能的实现者实现该模块的测试函数编写，并制定了`pre_commit`脚本，在每次提交前利用`pytest`完成所有模块的测试检查，只有所有测试通过后才能提交。

有关测试的具体信息请见[测试文档](测试文档.md)

### 6.1 单元测试

单元测试使用边界值分析法和等价类方法，设计黑盒测试用例，对每个单元进行测试。

详细的单元测试方法和测试用例请见：[单元测试文档](测试文档.md)

### 6.2 功能测试

#### 6.2.1 最短路径查询功能测试

* 测试用例一，出发点：良乡大学城，终点：中关村

  <img src="http://image-hosting-404.oss-cn-beijing.aliyuncs.com/img/test1.png" style="zoom:67%;" />

* 测试用例二，出发点：中关村，终点：中关村

  <img src="http://image-hosting-404.oss-cn-beijing.aliyuncs.com/img/test2.png" style="zoom:67%;" />

* 测试用例三，出发点：外星，终点：中关村

  <img src="http://image-hosting-404.oss-cn-beijing.aliyuncs.com/img/test3.png" style="zoom:67%;" />

* 测试用例四，出发点：西土城，终点：金台路

  ![](http://image-hosting-404.oss-cn-beijing.aliyuncs.com/img/test4.png)

#### 6.2.2 遍历路径查询功能测试

* 出发站：天安门东

  <img src="http://image-hosting-404.oss-cn-beijing.aliyuncs.com/img/test5.png" style="zoom:67%;" />



## 7. 性能测试

程序通过cProfile进行性能分析，并通过可视化工具判断不同代码块耗时所占不同比重，从而找到影响性能的瓶颈，对瓶颈部分进行优化。

### 7.1 最短路径查询功能性能测试

<img src="http://image-hosting-404.oss-cn-beijing.aliyuncs.com/img/profile2.png" style="zoom:67%;" />

<img src="http://image-hosting-404.oss-cn-beijing.aliyuncs.com/img/profile3.png" style="zoom:67%;" />

最短路径查询功能的瓶颈主要在于文件IO上，本项目中文件IO使用常规的`python`文件IO，可以考虑对IO瓶颈优化。可以对文件进行分块，申请一个线程池，使用多线程来加速文件IO处理。

### 7.2 遍历路径查询功能性能测试

<img src="http://image-hosting-404.oss-cn-beijing.aliyuncs.com/img/profile.png" style="zoom:67%;" />

由分析结果可知，在程序中，最耗时的部分是查找最短路的部分，由于在遍历过程中需要多次枚举当前遍历的地铁线路，计算从当前点到地铁线路起始点或者终点的最短路线。

故需要频繁调用`Solution`模块中的`shortest_path`模块，`shortest_path`使用BFS算法计算最短路径，时间复杂度为$O(n)$，结合遍历查询功能函数代码分析可知，遍历查询模块的时间复杂度为$O(m^2n)$，其中$m$为地铁线路个数。

考虑到如果遍历功能需要多次使用，则可以考虑先计算所有站点对之前的最短路径，然后离线存到一个文件中，并在程序开始时进行加载。每次查询两点之间的最短路径，即可达到$O(1)$，整体复杂度可以优化到$O(m^2)$。

北京地铁数目一共有$459$个，即$n=459$，优化后的性能将会是优化前性能的$1/459$，收益非常可观。

## 8. 代码规范

在结对编程时，我们对代码规范做出了如下几个基本原则：
* 遵循[Google Python代码风格](https://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/python_language_rules/)
* 代码风格尽量统一
* 每个功能模块需要有清晰的注释说明
* 使用[Google开源注释风格](https://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/python_style_rules/#comments)，边**尽量**在注释中举简单例子，便于理解

并且使用代码风格检查工具`black`和`pylint`进行代码风格的统一管理：
* [pylint](https://www.pylint.org/)，每次提交需要确保通过pylint
* [black](https://pypi.org/project/black/)，使用black帮助格式化代码风格，每次提交需确保通过black

为保证每次向服务器提交的代码都符合规范，我们制定了`pre_commit`脚本，该脚本会使用`black`和`pylint`对所提交代码进行分析，每次提交都需要保证通过该脚本的代码分析，从而保持代码风格的一致性和规范性。

## 9. git提交规范

为保证git提交的历史较容易追溯和明确修改内容，我们制定了如下git提交规范：

### 9. 1提交信息格式

* 每个git commit提交信息由`header`、`body`和`footer`三部分组成

* `body`和`footer`可以省略，`header`不可省略

* `header`由三个部分组成：`type`，`scope`，`subject`

* `scope`可省略，`type`和`subject`不可省略

  

提交格式如下所示：

```
<type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

**参考提交格式**：

```
docs(blog): update blog of week1
```

```
test(model): add pytest on shortest path

In order to improve code instructions, the black box test method is used to design test cases 
```

### 9.2Header格式

#### 9.2.1 type

* docs: 对blog或者readme等文档进行修改
* fix: 修复bug
* style: 调整代码或者注释格式，不改变代码实际功能
* test: 增加或者修改测试文件
* feat: 增加新的功能点
* perf: 提高代码性能
* refactor: 重构代码（即没有修复bug也没有增加功能点）

#### 9.2.2 scope

* 本次提交影响的范围，scope的内容可以省略
* 在本项目中，scope可以为：
  * core
  * model
  * utils
  * subway
  * ...
* 如果觉得较难确定scope，可以不写

#### 9.2.3 subject

* subject中填写本次提交的主题
* 第一个字母不要大写
* 结尾不加.(句号)

### 9.3body格式（可省略）

该格式在本项目中可以省略

### 9.4footer格式（可省略）

该格式在本项目中可以省略



## 10. 界面设计

### 10.1 WEB界面设计

#### 10.2.1 详细设计过程
WEB界面的设计过程，主要先考虑站点显示功能的实现。当时想到一个比较简单的方法，设置一个画布，把北京地铁的图片作为画布的背景，然后在画布上进行打点画圆，通过不断地打点即可实现一个地铁站遍历的效果。

但是要完成这个功能首先需要确定的是打点的坐标从哪来，最后的实现方法为通过图片的像素逐一确定每个地铁站的像素坐标，然后与地铁背景图标坐标成等比例缩放，得到每个站点在图片上的相对坐标，然后利用相对坐标打点画图实现。

由于这个过程人为完成，所以在实现的过程中，经常会出现数据坐标有误的情况，因此处于不断地修复数据过程中。较为方便的是，由于存在遍历所有站点的功能，所以每当遍历完所有站点时，较容易找出哪些站点的坐标出现偏差，再进行修复即可。

其次，考虑用户与界面的交互。由于系统支持的功能较少，仅有遍历地铁站点和查询最短路径，出于使用的直观性，直接将用户交互界面设置在地铁画布的右边，分为上下两个区域，分别完成不同的功能交互。

WEB前端界面迭代过程：
* V1：支持输入站点查询后打点
* V2：在每次打点前先把画布上已有的点清空
* V3：修复了若干次相对坐标有误的数据
* V4：支持打点时当前所在站点为红色，已经经过的站点为黑色

当前WEB前端界面如下所示：
![](http://image-hosting-404.oss-cn-beijing.aliyuncs.com/img/web_pic2.png)

#### 10.2.2 界面模块与其他模块的对接
* 服务已部署于云服务器上，可以直接访问http://0x404.tech/

由于WEB后端采用Django框架，所以只需要配置Django路由和View模块即可完成后端处理前端的数据。

由于程序的功能不多，仅有查询最短路径和遍历所有站点两个功能，并且在前端已经预先设置好了接口。所以只需要指定两个路由路径，由前端发送数据到指定路径，再转接View模块的函数对数据进行处理即可。

因此在View模块中设置两个接口，用于处理前端发送请求，并且将前两阶段实现的subway核心模块封装到django中，在View模块中调用核心模块算法进行数据处理，返回HttpResponse。

在整个接口对接过程中，在设计上体现了MVC设计模式。前端界面通过ajax向指定路由发送POST请求，将前端的数据传到后端。后端路由解析对应的请求，发送给View模块下对应的处理函数。处理函数处理前端发送过来的数据，调用核心代码提供的query接口，完成数据的计算并发送给前端。


在这个过程中，路由扮演了Controller的角色，负责处理不同的请求，调用不同的view函数。而核心代码在这个过程中扮演了Model角色，负责处理数据。前端界面则扮演了View角色，通过接受后端传来的数据，进行不同的图案绘制和处理。




## 11. 结对过程

由于本项目大部分在寒假完成，故采用线上会议方式完成结对编程：

![](http://image-hosting-404.oss-cn-beijing.aliyuncs.com/img/meeting.png)

## 12. 收获体会