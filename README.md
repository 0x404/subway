# 结对项目：地铁漫游

## 零、任务

使用北京地铁交通图，提供地铁换乘服务。

![](https://www.bjsubway.com/subway/images/subway_map.jpg)

## 一、作业要求

1. 阅读个人软件开发流程（PSP）的相关资料。
2. 可选的语言包括:C++，C#，Java，Python。运行环境为64bit Windows 10。
3. 提交的代码要求经过代码质量分析工具的分析并消除所有的警告。如[Code Quality Analysis](http://msdn.microsoft.com/en-us/library/dd264897.aspx)。
4. 完成项目的首个版本之后，请使用**性能分析工具**来找出代码中的性能瓶颈并进行改进。
5. 使用单元测试对项目进行测试，并查看测试分支覆盖率等指标；并写出至少10个测试用例确保你的程序能够正确处理各种情况。如[Studio Profiling Tools](https://msdn.microsoft.com/en-us/library/mt210448.aspx)。
6. 使用Git来管理源代码和测试用例，**代码有进展即签入本地仓库，定期推送到服务器上，并发送合并请求提交每周的工作成果。签入记录不合理的项目会被抽查询问项目细节。**
7. 按照要求发布博客，结合结对项目的实践经历，撰写解决项目的心路历程与收获。**博客与项目明显不符的作业将取消作业成绩。**

> 注意：要求3、4、5根据所选编程语言使用对应的开发工具来完成。

## 二、需求

**共4个阶段，每周更新**

### 第1阶段

- 把这个图的各个线路，各个站点，换乘信息等用**文本文件  (假设名字叫 beijing-subway.txt)**的形式保存起来，应该保存的信息有 {线路号，线路的各个站名，车站的换乘信息}， 应用程序可以读取这个文件，就能掌握关于北京地铁线路的所有信息，应该用什么样的格式呢？
- 写一个命令行程序 （不妨叫 subway.exe），这个程序启动的时候， 会读取beijing-subway.txt 的信息，然后这个程序就等待用户的输入， 用户可以输入地铁的线路编号，然后程序就输出此地铁线路的所有站名（按某一方向顺序输出即可）。 输出站名后，程序又进入等待状态。
- 找到两点之间的最有效线路？ 请实现下面这个需求：

```
　　subway.exe   /b 知春路   中关村
```

　　返回经历的站名的个数，和路径，如果有换乘，请列出换乘的线路， 例如：

```
　　4
　　知春路
　　知春里
　　海淀黄庄  换乘10号线
　　中关村
```

### 第2阶段

- 如果乘客有钱又有闲，那么，怎样才能尽可能快地遍历地铁的所有车站呢（只用经过一次，不用下车，就算经过车站）。 例如，注意到13号线和10号线相交的**知春路地铁站**，我们选它作为一个起始站，从这个站出发，要经历多少站（换乘不出地铁系统，即不能从一个地铁口走到路面，然后从另一个站进去），才能把所有地铁站都遍历呢？

  扩展命令行程序，让它接受一个地铁站名。  例如这个格式： 
  ```
  subway.exe /a  知春路
  ```

程序输出总共经历多少站， 以及经历的站名， 举一个特例，假如地铁系统只有知春路， 西土城两个站， 那么这个程序应该输出：

```
　　3
　　知春路
　　西土城
　　知春路
```

- 在地铁系统中换乘是比较麻烦的一件事情，花费额外的时间和体力 （下车，步行到下一个线路，等车，挤上车，再找座位）。 做一个改进， 每次换乘，相当于额外经历了 3 个车站， 还是要求遍历所有车站的最优线路，程序应该怎么修改呢？  
  ```
  总的车站数量 = 实际经过的车站数量 + 换乘等价的车站数量
  ```

### 第3阶段
  
- 能否做成图形界面呢？ 首先我们要给每个站点一个坐标信息。
	- 修改 beijing-subway.txt 文件，加入适当的信息，为实现图形界面做准备。 如何设计这些坐标呢？
	- 改进 subway.exe，  加一个  `/g` 的命令行参数， 让它根据你提供的坐标画出各个地铁站，线路，以及换乘站。
	- 存储有下面4个方案：
		- 用文本文件，用自定义的格式存放
		- 用XML格式存放
		- 用数据库的方式来存放， 例如 [sqlite](https://www.sqlite.org/)
		- 还可以用自己定义的二进制的格式来存放。
   
   	请比较几种方式的优缺点，特别是，这些方式如何应对变化的内部，外部因素。 

- 在GUI（图形界面）中实现遍历的解法。 
	扩展 subway.exe,  处理下面参数的时候，subway.exe /g  知春路

程序在图形界面中显示地铁地图 （各个站点的相对位置和官方地图类似即可），然后用一个小亮点表示乘客，乘客正在经过的车站就会闪亮，乘客走过的路用不同的颜色标识，同时在适当的地方有数字表明乘客已经经过车站的数目。

### 扩展需求

请结对的同学商量一下是否要进行扩展，如果有时间，可从以下2个方向选择一个进行。

- 让程序能处理上海的地铁地图，或者其它城市的地图。把程序由 “固定处理一个地图” 升级为 “能处理多个地图”， 程序的什么模块需要变化？
- 把程序移植到网页/手机，用户指定起点和终点，程序就报告这两个点的最优路径。 把程序从 PC 平台搬到 Web 或 Mobile,  原来写的所有代码都要扔掉么？ 还是有很多部分可以重用？ 怎样重用？

## 三、测试

```
subway.exe  /z filename 
```

`filename`指向一个文本文件，里面放了 `/a` 参数的答案

这个 `/z` 参数要求在命令行输出：

- true： 如果`filename`文件中的数据的确覆盖了整个地铁的所有站点至少一次，并且车站的数量是对的，车站的遍历次序是合理的。
- false: 车站的遍历次序仍然合理，但是有遗漏的站点，或者车站的数量错误。 如果有遗漏的站点，这个程序要至少输出一个遗漏的车站名。
- error: 如果车站的遍历次序不合理（例如直接从“知春路” 站到了“中关村” 站）， 打印出出错的两个站名。

## 四、博客撰写要求

使用Markdown编写小组博客，可在小组目录中建立一个名为blog的子目录，建议每周一个文件，描述一周的工作进展。

- 在开始实现程序之前，在**PSP表格**记录下你估计的时间。
- 看教科书和其它资料中关于Information Hiding, Interface Design, Loose Coupling的章节，说明你们在结对编程中是如何利用这些方法对接口进行设计的。
- 描述重要**模块接口的设计与实现过程**。设计包括代码如何组织，比如会有几个类，几个函数，他们之间关系如何，关键函数是否需要画出流程图？说明你的算法的关键（不必列出源代码），以及独到之处。
- 阅读有关UML的内容：[UML](https://en.wikipedia.org/wiki/Unified_Modeling_Language)。 画出UML图显示计算模块部分各个实体之间的关系(画一个图即可)。
- 看Design by Contract, Code Contract的内容：
  [Design by contract](http://en.wikipedia.org/wiki/Design_by_contract)
  [Code contract](http://msdn.microsoft.com/en-us/devlabs/dd491992.aspx)
  描述这些做法的优缺点, 说明你是如何把它们融入结对作业中的。
- 程序的代码规范，设计规范。 你们两如何达成共识，采用了什么规范？ 程序中是否有异常处理？你是如何处理各种异常的？
- **界面模块的详细设计过程**：你的程序有用户界面么？在博客中详细介绍界面模块是如何设计的。
- **界面模块与其它模块的对接**：详细地描述UI模块的设计与其他模块的对接，并在博客中截图实现的功能。界面/控制/数据模块体现了 [MVC 的设计模式](https://en.wikipedia.org/wiki/Model–view–controller)了么？
- **描述结对的过程**，提供非摆拍的两人在讨论的结对照片。可以做遮挡或美化。
- 看教科书和其它参考书，网站中关于[结对编程的章节](http://www.cnblogs.com/xinz/archive/2011/08/07/2130332.html)，说明你们采用了哪种合作方式，以及结对编程的优点和缺点。
  - 结对的每一个人的优点和缺点在哪里 (要列出至少三个优点和一个缺点)。
  - 你如何说服你的伙伴改进TA 的缺点？请考虑一下三明治方法。 
- 在你实现完程序之后，在附录提供的**PSP表格**记录下你在开发各个步骤上实际花费的时间。并说明差异的原因。 
- 其它收获，例如，如何攻克技术难点，你做了哪些阅读，探索，可以把资料和经历描述一下。 如果你的项目是和其他同学一起比赛（例如比赛速度），描述一下你的程序和其他程序的优劣。 

## 五、评分规则

结对项目分数由三部分组成，分别是
* 博客 — 25分。
* 程序 — 25分

```
5分为源代码管理评分，该评分主要通过源代码管理中的commit注释信息，增量修改的内容，是否有运行说明等给分。
15分为正确性评分。
5分为性能评分。
当程序的正确性评分等于15分时才可以参与性能评分环节，所以请各位同学务必保证自己程序的正确性。
```

* 注意事项：

```
按时间完成并提交——正常评分
晚交一周以内——折扣90%
晚交一周以上——折扣70%
不交或抄袭——0分【严禁代码与博客等一切形式的抄袭！请各位同学千万不要触碰底线，勿谓言之不预也！】
```

*附：PSP 2.1表格*

| PSP2.1 | Personal Software Process Stages | 预估耗时（分钟） | 实际耗时（分钟） |
| --- | --- | --- | --- |
| Planning | 计划 |  |  |
| · Estimate | · 估计这个任务需要多少时间 |  |  |
| Development | 开发 |  |  |
| · Analysis | · 需求分析 (包括学习新技术) |  |  |
| · Design Spec | · 生成设计文档 |  |  |
| · Design Review | · 设计复审 (和同事审核设计文档) |  |  |
| · Coding Standard | · 代码规范 (为目前的开发制定合适的规范) |  |  |
| · Design | · 具体设计 |  |  |
| · Coding | · 具体编码 |  |  |
| · Code Review | · 代码复审 |  |  |
| · Test | · 测试（自我测试，修改代码，提交修改） |  |  |
| Reporting | 报告 |  |  |
| · Test Report | · 测试报告 |  |  |
| · Size Measurement | · 计算工作量 |  |  |
| · Postmortem & Process Improvement Plan | · 事后总结, 并提出过程改进计划 |  |  |
|  | 合计 |  |  |



