---
title: 
author: 
tags: 
aliases: 
cssclasses:
---

# 引用
[[芯片开发学习/君正T23N芯片开发/【君正T23N_IPC】/知识积累/网页知识学习/SDIO wifi驱动框架]]

[[芯片开发学习/君正T23N芯片开发/【君正T23N_IPC】/知识积累/网页知识学习/SDIO接口WiFi驱动浅析]]

[[芯片开发学习/君正T23N芯片开发/【君正T23N_IPC】/知识积累/网页知识学习/Linux SD卡驱动开发(一) —— SD 相关基础概念]]

[[芯片开发学习/君正T23N芯片开发/【君正T23N_IPC】/知识积累/网页知识学习/Linux SD卡驱动开发(二) —— SD 卡驱动分析HOST篇]]

# 1、

## 1.1、

对于 [SDIO接口](https://so.csdn.net/so/search?q=SDIO%E6%8E%A5%E5%8F%A3&spm=1001.2101.3001.7020) 的WiFi，首先，它是一个SDIO的卡设备，然后具备了WiFi的功能。所以，<span style="background:#d3f8b6">注册的时候还是先以sdio设备去注册，然后检测到卡之后再去实现它的wifi功能。显然，他是用SDIO的协议，通过发命令和数据来控制实现WiFi功能。</span>

## 1.2、

**SDIO总线 和 USB总线 类似**，SDIO也有两端，其中一端是HOST端，另一端是device端。**所有的 通信 都是 由HOST端 发送 命令 开始的**，Device端只要能解析命令，就可以相互通信。
  [CMD](https://so.csdn.net/so/search?q=CMD&spm=1001.2101.3001.7020)信号：**双向 的信号，用于传送 命令 和 反应**。
SDIO的每次操作都是由HOST在CMD线上发起一个CMD，对于有的CMD，DEVICE需要返回Response，有的则不需要。

## 1.3、


# 2、

![君正T23N芯片开发/【君正T23N\_IPC】/知识积累/总结提取/assets/SDIO wifi总结/file-20250810171415630.png](assets/SDIO%20wifi总结/file-20250810171415630.png)
<span style="background:#b1ffff">Linux MMC 子系统</span>主要分成三个部分：

- MMC核心层：完成不同协议和规范的实现，为host层和设备驱动层提供接口函数。MMC核心层由三个部分组成：MMC，SD和SDIO，分别为三类设备驱动提供接口函数；
- <span style="background:#affad1">Host 驱动层</span>：针对不同<span style="background:#fff88f">主机端的SDHC、MMC控制器的驱动</span>；
<span style="background:#affad1">- Client 驱动层：</span>针对<span style="background:#fff88f">不同客户端的设备驱动程序</span>。如SD卡、T-flash卡、SDIO接口的GPS和wifi等设备驱动


![君正T23N芯片开发/【君正T23N\_IPC】/知识积累/总结提取/assets/SDIO wifi总结/file-20250810171415854.png](assets/SDIO%20wifi总结/file-20250810171415854.png)

网络设备接口层的主要功能是<span style="background:#b1ffff">为千变万化的网络设备定义了统一、 抽象的数据结构 net_device 结构体，实现多种硬件在软件层次上的统一。</span>

它的<span style="background:#b1ffff">HOST端是开发板mmc控制器，而device端（client）则是各种带SDIO接口的模块，比如SDIO WiFi模块</span>。






## 2.1、**网络设备接口层**


### 2.1.1、net_device结构体
Linux内核使用 <span style="background:#affad1">net_device结构体表示一个具体的网络设备</span>，网络驱动的核心就是初始化net\_device 结构体中的各个成员变量，然后将初始化完成以后的net\_device 注册到 Linux内核中。

其中<span style="background:#b1ffff"> netdev_ops</span>是网络设备的操作集函数，包含了一系列的网络设备操作回调函数，
	<span style="background:#d3f8b6">类似字符设备中的 file_operations</span>


## 2.2、**设备驱动功能层**
对应net\_device结构体中的<span style="background:#b1ffff">设备驱动功能函数netdev_ops</span>，例如<span style="background:#d3f8b6">xxx\_open()、xxx\_stop()、xxx\_tx()</span>等。另一部分是<span style="background:#b1ffff">中断处理函数</span>，它<span style="background:#affad1">负责接收硬件上的数据包并传给上层协议。 这也是wifi驱动主要需要实现的接口：</span>路径 os_dep\linux\os_intfs.c，<span style="background:#affad1">rtw_netdev_ops</span><span style="background:#d3f8b6">最后在probe中赋值给net_device中设备驱动功能函数netdev_ops。</span>




## 2.3、





# 3、
WiFi 驱动

<span style="background:#b1ffff">分为两部分，上面为主机端驱动，下面firmware。</span>

主机端驱动包括上面讲的网络子系统，mmc子系统。
Wifi driver (mmc 子系统中Client 驱动层)

修改设备树节点后直接将wifi driver和host driver编译进内核，插入wifi模块后使用ifconfig -a可以看到wlan0 节点，这样wifi驱动就移植好了
## 3.1、



## 3.2、



## 3.3、





# 4、
## 4.1、



## 4.2、



## 4.3、





# 5、


# 6、



# 7、

