---
title: "Linux应用开发笔记（一）交叉编译及执行_ssh server 交叉编译-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/137156982?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读700次，点赞10次，收藏12次。GCC（GNU Compiler Collection）是一个开源的编译器集合，包含C、C++、Objective-C、Fortran、Java、Ada和Go语言的编译器。它原本是GNU项目的编译器，现已被大多数类Unix操作系统（如Linux、BSD、Mac OS X等）采纳为标准的编译器。GCC的初衷是为GNU操作系统专门编写的一款编译器。_ssh server 交叉编译"
tags:
  - "clippings"
---
Linux 应用开发笔记（一）交叉编译及执行  

---

## 一、GCC编译器

### 1\. 什么是GCC

GCC（GNU Compiler Collection）是一个开源的编译器集合，包含C、C++、Objective-C、 Fortran 、Java、Ada和Go语言的编译器。它原本是 [GNU项目](https://so.csdn.net/so/search?q=GNU%E9%A1%B9%E7%9B%AE&spm=1001.2101.3001.7020) 的编译器，现已被大多数类Unix操作系统（如Linux、BSD、Mac OS X等）采纳为标准的编译器。GCC的初衷是为GNU操作系统专门编写的一款编译器。

### 2\. 安装GCC

1. 在虚拟机中更新一下apt，输入以下命令：
```c
sudo apt update
1
```
1. 安装交叉编译器和vim编辑器：
```c
sudo apt install gcc-aarch64-linux-gnu g++-aarch64-linux-gnu vim
1
```
1. 安装完成之后可以输入以下命令验证gcc、g++和vim的安装是否成功：
```c
aarch64-linux-gnu-gcc --version
vim --version
12
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/42c56280e2e1025bb53dfb74796430d4.png)

### 3.交叉编译

这里可以使用SSH使得 虚拟机 和VScode互联，从而直接编辑程序放到虚拟机的文件夹里，详细可以看：  
https://blog.csdn.net/qq\_62464995/article/details/131029280  
程序就举最简单的hello world吧，接着寻找所创建的文件的目录，可以看到这里有.c文件  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/8db448341c8667653b62bf4d835e6ef1.png)  
可以看到这里存在hello.c文件，接着进行编译：

```c
sudo aarch64-linux-gnu-gcc hello.c
1
```

此时可以看到目录下产生了一个a.out文件，只需要将其传到开发板即可编译。值得一提的是，由于虚拟机并不是arm64框架，所以不能执行。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ee398800c8063a959a020775d709269c.png)  
传输结束后，再输入：

```c
sudo ./a.out
1
```

这样就可以执行编译好的代码了，如果不能成功编译，可能是没有赋予权限，这个时候需要输入：

```c
sudo chmod 777 a.out
1
```

接下来就可以正常读取了。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/250d80f8eb3520a9b8f5acc8fab10993.png)

## 二、ssh的使用

### 1\. 连入局域网

这里主要有两种方式：WIFI和USB。  
**USB**:[泰山派配网](https://lceda001.feishu.cn/docx/YJjodkE1HoubsbxrfuwcXAGLn3e)  
**WIFI**:

```c
//先查看附件WiFi信息
nmcli device wifi list
// 找到自己的wifi之后连接，输入时不带[]
nmcli device wifi connect [wifi名称] password [wifi密码]
1234
```

### 2\. 连接SSH

```c
//先习惯性更新一下
apt-get update
//安装ssh
sudo apt-get install openssh-client
sudo apt-get install openssh-server
//启动ssh
/etc/init.d/ssh start
//修改配置，输入i进入编辑模式，然后将#PermitRootLogin without-password改为PermitRootLogin yes
vim /etc/ssh/sshd_config
//重启并连接
/etc/init.d/ssh restart
1234567891011
```

连接之后，通过 软件 移动即可，如下所示：  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/2930cab1a8e4418fa20d02d751292ca4.png)

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/137156982

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