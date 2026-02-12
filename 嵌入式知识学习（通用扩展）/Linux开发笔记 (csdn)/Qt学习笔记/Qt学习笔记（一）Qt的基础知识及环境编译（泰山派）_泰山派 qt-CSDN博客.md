---
title: "Qt学习笔记（一）Qt的基础知识及环境编译（泰山派）_泰山派 qt-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/142909247?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读1.1k次，点赞21次，收藏28次。最近已经停更很久了，本系列主要是对Qt进行一个简单的学习和了解，这部分内容不是很多，操作也是较为简单的。_泰山派 qt"
tags:
  - "clippings"
---
## 系列文章目录

[Qt学习](https://so.csdn.net/so/search?q=Qt%E5%AD%A6%E4%B9%A0&spm=1001.2101.3001.7020) 笔记（一）Qt的基础知识及环境编译（泰山派）  
Qt学习笔记（二）Qt 信号与槽  
Qt学习笔记（三） [网络编程](https://so.csdn.net/so/search?q=%E7%BD%91%E7%BB%9C%E7%BC%96%E7%A8%8B&spm=1001.2101.3001.7020)  
Qt学习笔记（四）多线程

---

---

## 前言

  最近已经停更很久了，本系列主要是对Qt进行一个简单的学习和了解，这部分内容不是很多，操作也是较为简单的。

---

## 一、Qt的基本知识

### 1.1 Qt的引入

  Qt 是一个跨平台的 C++开发库，主要用来开发图形用户界面（Graphical User Interface，简称 GUI）程序。Qt 除了可以绘制漂亮的界面（包括控件、布局、交互），还包含很多其它功能，比如多线程、访问数据库、图像处理、音频视频处理、网络通信、文件操作等。理论上来说，Qt 基本可以做出市面上所有的流行App，像 WPS、网易云、Maya(3D 建模)，甚至一些游戏的内核都可以使用 Qt 来实现。  
  Qt 支持的操作系统有很多，例如通用操作系统 Windows 、Linux、Unix，智能手机系统Android、iOS、WinPhone， 嵌入式系统 QNX、VxWorks 等等。在嵌入式里，使用 Qt 来开发界面已经是无可替代的一种趋势。工控界面最常用，一些移动端的界面也开始使用 Qt。

### 1.2 Qtcreator

  Qt Creator 是一个强大的集成开发环境（IDE），专为开发 Qt 应用程序而设计。它提供了用户友好的界面，便于编写、调试和构建应用程序。本文第2节提供了Windows的安装包，使用方法可以参考 [Qtcreator入门操作](https://blog.csdn.net/a1547998353/article/details/140058717?ops_request_misc=&request_id=&biz_id=102&utm_term=qt%E5%AD%A6%E4%B9%A0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduweb~default-9-140058717.142%5Ev100%5Epc_search_result_base4&spm=1018.2226.3001.4187) 。

- 跨平台支持：支持 Windows、macOS 和 Linux，方便开发跨平台应用。
- 项目管理：可以轻松创建、打开和管理 Qt 项目（如.pro 文件和 CMake 项目）。
- 代码编辑：提供智能代码补全、语法高亮和代码重构功能，提升编程效率。
- 调试工具：集成调试器，可以方便地进行断点调试和变量监控。
- 图形界面设计：支持使用 Qt Designer 进行可视化界面设计，简化 UI开发。

### 1.3 Qt项目文件

  Qt Creator 和其他 IDE 开发软件一样。都是分组管理项目内的各种源文件，下面是项目内的文件简介。

- .pro 文件是项目管理文件，当您加入了文件或者删除了文件，Qt Creator 会自动修改这个.pro 文件。有时候我们需要打开这个.pro 文件来添加设置项。
- .ui 是一个 xml 类型的样式文件，它是自动生成的且不能进行手动编辑的，只能够通过图形界面修改其属性。
- .h 仍然代表头文件，其中包含对应.cpp文件中类的声明。
- .cpp 是指源文件，我们主要类的实现都是在这里面进行的。

### 1.4 C++语法回顾

  通常情况下，我们使用C++进行Qt编译（之前我们开始过C++系列的学习，当时是为了刷leecode），这里我们简单回顾一下为什么使用C++。  
**新数据类型**  
  大家可以回想一下，当年在编辑32程序的时候，最苦恼的事情莫过于没有一个真正意义上的标志量，所以我们不得不用“1”代表开启，“0”代表关闭，或者去自定义。但是现在不一样了，C++比 C 语言新增的布尔类型（bool），它可以容许我们直接表示一个接口或者设备是否启用，这对于我们后序进行UI设计的时候极为有用。  
**新输入输出方式**  
  在 C++里，我们使用以 cin 和 cout 代替了 scanf 和 printf 。在输入和输出的流程上是不变的，只是关键字变了，用法也变了，例如： `cout<<x<<endl;`表示输出一个x参数； `cin>>x;`表示输入一个参数。这里的x可以是任意数据类型，甚至可以写成一个表达式，而 endl 指的是换行符。  
**命名空间 namespace**  
  之所以使用 namespace是因为有些名字容易冲突，为了加以区分所以加个前缀，比如C++ 标准库 里面定义了 vector 容器，我们也写了个 vector 类，这样名字就冲突了。通常我们会这样定义 `using namespace std;`，using 是编译指令，std就是我们定义的 命名空间 。  
**this 指针**  
  在 C++中，this 指针是指向类自身数据的指针，简单的来说就是指向当前类的当前实例对象。如果我们把类看成一个结构体，然后this就是在成员函数中的这个结构体的代称。每个对象都拥有一个 this 指针，this 指针记录对象的内存地址。关于类的 this 指针有以下特点：  
（1） this 只能在成员函数中使用，全局函数、静态函数都不能使用 this。  
（2） this 在成员函数的开始前构造，在成员函数的结束后清除。  
（3） this 指针会因 编译器 不同而有不同的放置位置。

```cpp
// 示例
class MyClass {
public:
    int value;

    void setValue(int value) {
        this->value = value; // 使用 this 指针区分参数和成员变量
    }
};
123456789
```

## 二、Qt的移植

  前面提到，本次的移植主要针对泰山派，这里提供了笔者已经测试好的安装包： [百度云盘：Qt5.12.10环境，提取码：x6tf](https://pan.baidu.com/s/13BXBZ_A1VRDch-iykpjF8Q?pwd=x6tf) 。具体的操作流程请参考泰山派的共享文档即可： [泰山派移植Qt](https://lceda001.feishu.cn/wiki/KmQ0wLSq9ijwvHkXV2JcmyYGnlb) 。  
  经过笔者测试的各种组合，还是建议搞一个Windows版本的作为主编译器，之后和以前做驱动代码一样，将程序文件夹放到 Linux 系统中交叉编译再移植，值得注意的是Linux的编译环境要和Windows下的版本一致（例如都是qt5.12.10），然后开发板上的Qt库要根据自己不同的系统进行编译下载（例如：Buildroot，Debian等，值得一提的是，如果是Ubuntu系统可以直接把Linux下编译好的交库烧录进去即可）。  
  值得一提的是，如果泰山派执行程序时出现了花屏，刷新错乱的问题，我们只需要禁止掉buildroot的系统界面即可（禁止之后就不可以得到文件系统的GUI界面，我们只能完全靠命令行控制）。

---

**免责声明：本文参考了网上公开的部分资料，仅供学习参考使用，若有侵权或勘误请联系笔者。**

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/142909247

作者主页：https://blog.csdn.net/sincerelover

实付 元

[使用余额支付](https://blog.csdn.net/sincerelover/article/details/)

点击重新获取

扫码支付

钱包余额 0

抵扣说明：

1.余额是钱包充值的虚拟货币，按照1:1的比例进行支付金额的抵扣。  
2.余额无法直接购买下载，可以购买VIP、付费专栏及课程。

[余额充值](https://i.csdn.net/#/wallet/balance/recharge)

举报

![程序员都在用的中文IT技术交流社区](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_app.png)

程序员都在用的中文IT技术交流社区

程序员都在用的中文IT技术交流社区

![专业的中文 IT 技术社区，与千万技术人共成长](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_wechat.png)

专业的中文 IT 技术社区，与千万技术人共成长

专业的中文 IT 技术社区，与千万技术人共成长

![关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_video.png)

关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！

关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！

客服 返回顶部