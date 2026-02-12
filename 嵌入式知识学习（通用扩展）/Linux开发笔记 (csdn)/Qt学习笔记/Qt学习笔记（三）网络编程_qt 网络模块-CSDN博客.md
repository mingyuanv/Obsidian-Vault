---
title: "Qt学习笔记（三）网络编程_qt 网络模块-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/143051705?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读1.2k次，点赞16次，收藏16次。之前我们在Linux应用层的学习时提到了网络编程，本节是进行Qt下TCP / IP 客户端的编写。_qt 网络模块"
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

  之前我们在 Linux 应用层的学习时提到了网络编程，本节是进行Qt下TCP / IP 客户端的编写。

---

## 一、Qt网络模块

  Qt 网络模块为我们提供了编写 TCP / IP 客户端和服务器的类。它提供了较低级别的类，例如代表低级网络概念的 QTcpSocket，QTcpServer 和QUdpSocket，以及诸如 QNetworkRequest，QNetworkReply 和QNetworkAccessManager 之类的高级类来执行使用通用协议的网络操作。它还提供了诸如QNetworkConfiguration，QNetworkConfigurationManager，QNetworkSession等类，实现承载管理。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/3124eccb4b48412da49fb295e73ac5ac.png)

## 二、TCP网络的编写

### 2.1 服务端

  所谓服务端就是指通过监听某个端口指令来判断是否有客户端连接，如果有则建立新的socket，之后客户端负责输入ip和port就可以完成连接了。在QT中，socket被视为输入输出流，数据的收发是通过read()和write()来实现。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/81d10a3a744344aeb66221a9b16d805b.png#pic_center)

#### 2.1.1 编写思路

 1. 创建QTcpServer服务端对象  
  这部分就是简单的对象实例化和槽 函数 的链接。  
 2. 开始/停止监听  
  在这个过程中最主要的是listen()函数，它可以设置监听的IP地址和端口，一般一个服务器端程序只监听某个端口的网络连接。

```cpp
//   函数返回 true 时，表示监听成功
bool QTcpServer::listen(const QHostAddress &address = QHostAddress::Any, quint16 port = 0)
12
```

 3. 动态创建QTcpSocket对象  
   这里主要利用nextPendingConnection()函数，它用于有新的客户端接入时，创建一个与客户端连接的QTcpSocket对象，然后发射 newConnection() 信号，通常我们在槽函数中使用它来进行新链接的创建。  
 4. 接受消息并处理或者判断连接状态并连接\\断开  
   这里就很简单，可以创建类似用下文的receiveMessege\_Slot()进行数据处理，或者是错误码检测之类的。

#### 2.1.2 实现代码

   记得编译前，在.pro文件中修改 `QT += network` ，这里注意下。

```cpp
// mainwindow.h
#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QtMqtt/qmqttclient.h>
#include <QObject>
#include <QTcpServer>
#include <QTcpSocket>

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

private slots:
    void netConnect_Slot(void);
    void receiveMessege_Slot(void);
    void disConnect_Slot(void);

private:
    Ui::MainWindow *ui;
    QTcpServer *m_server;
    QList<QTcpSocket*> m_clients;
};
#endif // MAINWINDOW_H

// mainwindow.c
#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    m_server = new QTcpServer(this);
    connect(m_server, SIGNAL(newConnection()), this, SLOT(netConnect_Slot()));

    if (!m_server->listen(QHostAddress::Any, 1883)) {
        qDebug() << "Failed to Connect!";
    } else {
        qDebug() << "Succeed to Connect!";
    }
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::netConnect_Slot()
{
    QTcpSocket *m_socket = m_server->nextPendingConnection();
    connect(m_socket, SIGNAL(readyRead()), this, SLOT(receiveMessege_Slot()));
    connect(m_socket, SIGNAL(disconnected()), this, SLOT(disConnect_Slot()));
    m_clients.append(m_socket);
    qDebug() << "New client connected";
}

void MainWindow::receiveMessege_Slot()
{
    QTcpSocket *m_socket = qobject_cast<QTcpSocket *>(sender());
    if (m_socket) {
        QByteArray requestData = m_socket->readAll();
        qDebug() << "Received MQTT message:" << requestData;
    }
}

void MainWindow::disConnect_Slot()
{
    QTcpSocket *m_socket = qobject_cast<QTcpSocket *>(sender());
    if (m_socket) {
        m_clients.removeOne(m_socket);
        m_socket->deleteLater();
        qDebug() << "Client disconnected";
    }
}
123456789101112131415161718192021222324252627282930313233343536373839404142434445464748495051525354555657585960616263646566676869707172737475767778798081828384858687
```

### 2.2 客户端

   这部分的内容十分重要，涉及到我们后期使用mqtt协议，通常情况下我们不主动搭建服务器，仅调用客户端就满足对“上云”的要求了。

#### 2.2.1 编写思路

 1. QTcpSocket 实例化并与信号和槽连接  
 2. 连接到服务器（指定的 IP 和端口）  
  这里主要是利用 `tcpSocket->connectToHost("服务器地址", 端口号);`进行连接，注意和上面的listen区分一下。  
 3. 消息通过 TCP 套接字发送到服务器  
  利用write和readAll即可完成数据的读写。

#### 2.2.2 实现代码

```cpp
#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QTcpSocket>
#include <QTextEdit>
#include <QLineEdit>
#include <QPushButton>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void onConnectButtonClicked();
    void onSendButtonClicked();
    void onReadyRead();
    void onError(QAbstractSocket::SocketError socketError);

private:
    Ui::MainWindow *ui;
    QTcpSocket *tcpSocket;
    QTextEdit *logTextEdit;
    QLineEdit *messageLineEdit;
    QPushButton *connectButton;
    QPushButton *sendButton;
};

#endif // MAINWINDOW_H

#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QDebug>
#include <QMessageBox>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow),
    tcpSocket(new QTcpSocket(this))
{
    ui->setupUi(this);

    // 获取控件
    logTextEdit = findChild<QTextEdit*>("logTextEdit");
    messageLineEdit = findChild<QLineEdit*>("messageLineEdit");
    connectButton = findChild<QPushButton*>("connectButton");
    sendButton = findChild<QPushButton*>("sendButton");

    // 连接信号和槽
    connect(connectButton, &QPushButton::clicked, this, &MainWindow::onConnectButtonClicked);
    connect(sendButton, &QPushButton::clicked, this, &MainWindow::onSendButtonClicked);
    connect(tcpSocket, &QTcpSocket::readyRead, this, &MainWindow::onReadyRead);
    connect(tcpSocket, &QTcpSocket::errorOccurred, this, &MainWindow::onError);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::onConnectButtonClicked()
{
    // 连接到服务器
    tcpSocket->connectToHost("127.0.0.1", 1234);

    if (!tcpSocket->waitForConnected(3000)) {
        QMessageBox::critical(this, "错误", "连接服务器失败: " + tcpSocket->errorString());
    } else {
        logTextEdit->append("已连接到服务器！");
    }
}

void MainWindow::onSendButtonClicked()
{
    // 发送消息到服务器
    QString message = messageLineEdit->text();
    if (message.isEmpty()) {
        return;
    }

    tcpSocket->write(message.toUtf8());

    if (!tcpSocket->waitForBytesWritten(3000)) {
        QMessageBox::critical(this, "错误", "发送失败: " + tcpSocket->errorString());
    } else {
        logTextEdit->append("发送消息: " + message);
    }
}

void MainWindow::onReadyRead()
{
    // 读取服务器的响应
    QByteArray response = tcpSocket->readAll();
    logTextEdit->append("收到服务器响应: " + response);
}

void MainWindow::onError(QAbstractSocket::SocketError socketError)
{
    // 处理连接错误
    Q_UNUSED(socketError);
    QMessageBox::critical(this, "错误", "发生错误: " + tcpSocket->errorString());
}

123456789101112131415161718192021222324252627282930313233343536373839404142434445464748495051525354555657585960616263646566676869707172737475767778798081828384858687888990919293949596979899100101102103104105106107108109110111
```

## 三、 浅谈MQTT

  老粉丝可能知道，笔者钟情于MQTT作为远距离形象传递的手段（主要是目前这种资料比较多，笔者太菜了学不会别的），本小节就简单讲一下我的一些理解。MQTT是一种 **基于TCP/IP协议** 的"轻量级"通讯协议，该协议主要是 **发布/订阅(publish/subscribe)模式** 的。在通讯过程中, MQTT协议中有三种身份: 发布者(Publish)、代理(Broker)(服务器)、订阅者(Subscribe)。 其中，消息的发布者和订阅者都是客户端，消息代理是服务器，消息发布者可以同时是订阅者。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/7cea41850bcf4a67bb3252e3fc8ad434.png#pic_center)  
  MQTT传输的消息分为 **由主题（Topic）和负载（payload）两部分组成** ，也就我们常见的“Topic+data”的结构。除此之外， **消息服务质量(QoS）管理** 是MQTT保证可靠传输的一大依仗，它有三种消息发布服务质量:

1. QoSO:“至多一次”，消息发布完全依赖底层TCP/IP网络，会发生消息丢失或重复。
2. QoS1:“至少—次”，确保消息到达，但消息重复可能会发生。
3. QoS2:“只有一次”，确保消息到达一次。

  常见的MQTT报文有以下15种，其中可以分为三大类： **连接、发布和订阅** ，对应MQTT的实现流程。而一个 **MQTT数据包由固定头(Fixed header)、可变头(Variable header)、消息体(payload)三部分构成** 。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/70716e1d80094d73a1c8ad57606ef727.png)  
  知道以上这部分其实就差不多了，毕竟我们不是专业搞信息工程或者网络专业的，剩下的很琐碎的东西学起来就很费时费力了。

---

**免责声明：本文参考了网上公开的部分资料，仅供学习参考使用，若有侵权或勘误请联系笔者**

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/143051705

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