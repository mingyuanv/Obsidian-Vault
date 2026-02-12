---
title: "Qt学习笔记（二）Qt 信号与槽_qt 父类的信号和槽是连接的,子类的信号和槽会自动连接-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/142997440?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读1.3k次，点赞30次，收藏28次。在学习 Qt 的过程中，信号与槽是必不可少的部分，也是 Qt 编程的基础，是 Qt 编程的一大创新，这里分一个章节来学习这个 Qt 的信号与槽。信号（Signal）就是在特定情况下被发射的事件，例如 PushButton 最常见的信号就是鼠标单击时发射的 clicked() 信号，一个 ComboBox 最常见的信号是选择的列表项变化时发射的CurrentIndexChanged() 信号。_qt 父类的信号和槽是连接的,子类的信号和槽会自动连接"
tags:
  - "clippings"
---
## 系列文章目录

[Qt学习](https://so.csdn.net/so/search?q=Qt%E5%AD%A6%E4%B9%A0&spm=1001.2101.3001.7020) 笔记（一）Qt的基础知识及环境编译（泰山派）  
Qt学习笔记（二）Qt 信号与槽  
Qt学习笔记（三） [网络编程](https://so.csdn.net/so/search?q=%E7%BD%91%E7%BB%9C%E7%BC%96%E7%A8%8B&spm=1001.2101.3001.7020)  
Qt学习笔记（四）多线程

---

## 前言

  在学习 Qt 的过程中，信号与槽是必不可少的部分，也是 Qt 编程的  
基础，是 Qt 编程的一大创新，这里分一个章节来学习这个 Qt 的信号与槽。

---

## 一、Qt 信号与槽机制

### 1.1 什么是信号和槽

  信号（Signal）就是在特定情况下被发射的事件，例如 PushButton 最常见的信号就是鼠标单击时发射的 clicked() 信号，一个 ComboBox 最常见的信号是选择的列表项变化时发射的CurrentIndexChanged() 信号。GUI 程序设计的主要内容就是对界面上各 组件 的信号的响应，只需要知道什么情况下发射哪些信号，合理地去响应和处理这些信号就可以了。  
  槽（Slot）就是对信号响应的 函数 。槽就是一个函数，与一般的 C++函数是一样的，可以定义在类的任何部分（public、private 或 protected），可以具有任何参数，也可以被直接调用。槽函数与一般的函数不同的是：槽函数可以与一个信号关联，当信号被发射时，关联的槽函数被自动执行。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/ec4133040b614f1aa8b8b40c741ead7a.png)

### 1.1 信号和槽的关联及断连

  信号与槽关联是用 QObject::connect() 函数实现的，它是connect() 是 QObject 类的一个静态函数，其基本格式是：

```cpp
// 完整格式
QObject::connect(sender, SIGNAL(signal()), receiver, SLOT(slot()));

// 在实际调用时可以忽略前面的限定符
connect(sender, SIGNAL(signal()), receiver, SLOT(slot()));
12345
```

  其中，sender 是发射信号的对象的名称，signal() 是信号名称。信号可以看做是特殊的函数，需要带括号，有参数时还需要指明参数。receiver 是接收信号的对象名称，slot() 是槽函数的名称，需要带括号，有参数时还需要指明参数。  
  断开连接需要使用 disconnect()函数，其格式如下：

```cpp
// 断开一切与 myObject 连接的信号或槽
bool QObject::disconnect(sender,SIGNAL(signal()), receiver, SLOT(slot()));
12
```

  信号与槽机制是 Qt GUI 编程的基础，使用信号与槽机制可以比较容易地将信号与响应代码关联起来。我们在平常编辑的时候可以直接利用UI设计器进行编辑（自动关联），当运行之后会自动生成Ui\_MainWindow.h文件。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/130ac95918904288be1dcc60dcbe1eb1.png)  
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/636089a53855465a944b47da934e0109.png)

## 二、编辑槽函数

### 1\. 自动关联

  右键我们的控件，选择转到槽，然后选择一个触发方式，之后便会在mainwindow.cpp文件下生成一个槽函数，并在mainwindow.h下进行申明。这里要特别注意，槽函数 **只能申明在private slots 或者public slots下** 。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/dd6b2ba73134491c95c45b103fbcef87.png)  
  在生成的on\_connect\_clicked( )槽函数中进行功能编辑，笔者这里是进行了一个打印功能。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/2809f22d4e614f3a924830df860a4582.png)  
  执行之后可以看到，下方的控制窗口已经打印出来了信息。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/9a8c63aeffce46628f297ba57f5d520c.png)

### 2\. 手动关联

  这种方式需要用的我们上文提到的connect和disconnect函数，主要是服务于大型项目。它可以自定义更多槽函数功能和名称，具有极大的灵活性，同时由于所有界面都在代码中定义，避免了 UI 文件和逻辑代码分离带来的管理复杂性，所有人都能在代码中找到界面和逻辑。以下是手动关联的基本流程：

1. 创建项目与 UI 设计  
	  假设你已经在 Qt Designer 中设计了一个简单的窗口（也可以纯代码编写），包含一个按钮 pushButton 和一个标签 label。
2. 创建 C++ 类  
	  创建一个 C++ 类并添加信号的声明，通常是继承自 QMainWindow 或 QWidget。
```cpp
// 头文件 mainwindow.h
#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

signals:
    void myCustomSignal();  // 声明自定义信号
    
private slots:  // 声明槽函数
    void onButtonClicked();
    
private:
    Ui::MainWindow *ui;  // UI 指针
};
#endif // MAINWINDOW_H
12345678910111213141516171819202122232425262728
```
1. 实现构造函数与析构函数
```cpp
// 源文件 mainwindow.cpp
#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);  // 设置 UI

    // 手动连接信号与槽
    connect(ui->pushButton, SIGNAL(clicked()), this, SLOT(onButtonClicked())); // 连接按钮的点击信号到槽
}

MainWindow::~MainWindow()
{
    delete ui;
}

12345678910111213141516171819
```
1. 实现槽函数  
	  在 mainwindow.cpp 中，实现槽函数，这部分同上文自动关联。

---

**免责声明：本文参考了网上公开的部分资料，仅供学习参考使用，若有侵权或勘误请联系笔者。**

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/142997440

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