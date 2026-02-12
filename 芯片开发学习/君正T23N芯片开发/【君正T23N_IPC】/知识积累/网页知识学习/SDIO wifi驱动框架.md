---
title: "SDIO wifi驱动框架-CSDN博客"
source: "https://blog.csdn.net/yangzhipengyzp/article/details/137750462?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522190ba72b60177ce0ef525e57bbb4e72f%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=190ba72b60177ce0ef525e57bbb4e72f&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_positive~default-1-137750462-null-null.142^v102^pc_search_result_base9&utm_term=sdio%20wifi&spm=1018.2226.3001.4187"
author:
published:
created: 2025-04-15
description: "文章浏览阅读3.8k次，点赞45次，收藏100次。本文详细介绍了WiFidriver驱动框架，包括SDIO-Wifi模块的特性、SDIO总线协议、网络驱动架构，以及WiFi驱动如何与Host驱动协作，涉及MMC整体框架和设备树节点的移植过程。"
tags:
  - "clippings"
---
[1、WiFi driver驱动框架](https://blog.csdn.net/yangzhipengyzp/article/details/?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522190ba72b60177ce0ef525e57bbb4e72f%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=190ba72b60177ce0ef525e57bbb4e72f&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_positive~default-1-137750462-null-null.142^v102^pc_search_result_base9&utm_term=sdio%20wifi&spm=1018.2226.3001.4187#t0)

[1.1、SDIO-Wifi模块介绍](https://blog.csdn.net/yangzhipengyzp/article/details/?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522190ba72b60177ce0ef525e57bbb4e72f%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=190ba72b60177ce0ef525e57bbb4e72f&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_positive~default-1-137750462-null-null.142^v102^pc_search_result_base9&utm_term=sdio%20wifi&spm=1018.2226.3001.4187#t1)

[1.2、SDIO总线协议](https://blog.csdn.net/yangzhipengyzp/article/details/?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522190ba72b60177ce0ef525e57bbb4e72f%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=190ba72b60177ce0ef525e57bbb4e72f&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_positive~default-1-137750462-null-null.142^v102^pc_search_result_base9&utm_term=sdio%20wifi&spm=1018.2226.3001.4187#t2)

[1.3、网络驱动架构](https://blog.csdn.net/yangzhipengyzp/article/details/?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522190ba72b60177ce0ef525e57bbb4e72f%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=190ba72b60177ce0ef525e57bbb4e72f&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_positive~default-1-137750462-null-null.142^v102^pc_search_result_base9&utm_term=sdio%20wifi&spm=1018.2226.3001.4187#t3)

[1.4、MMC整体框架](https://blog.csdn.net/yangzhipengyzp/article/details/?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522190ba72b60177ce0ef525e57bbb4e72f%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=190ba72b60177ce0ef525e57bbb4e72f&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_positive~default-1-137750462-null-null.142^v102^pc_search_result_base9&utm_term=sdio%20wifi&spm=1018.2226.3001.4187#t4)

[2、WiFi 驱动](https://blog.csdn.net/yangzhipengyzp/article/details/?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522190ba72b60177ce0ef525e57bbb4e72f%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=190ba72b60177ce0ef525e57bbb4e72f&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_positive~default-1-137750462-null-null.142^v102^pc_search_result_base9&utm_term=sdio%20wifi&spm=1018.2226.3001.4187#t5)

[3.Host驱动](https://blog.csdn.net/yangzhipengyzp/article/details/?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522190ba72b60177ce0ef525e57bbb4e72f%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=190ba72b60177ce0ef525e57bbb4e72f&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_positive~default-1-137750462-null-null.142^v102^pc_search_result_base9&utm_term=sdio%20wifi&spm=1018.2226.3001.4187#t6)

[3.WIFI驱动移植](https://blog.csdn.net/yangzhipengyzp/article/details/?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522190ba72b60177ce0ef525e57bbb4e72f%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=190ba72b60177ce0ef525e57bbb4e72f&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_positive~default-1-137750462-null-null.142^v102^pc_search_result_base9&utm_term=sdio%20wifi&spm=1018.2226.3001.4187#t7)

[4.总结](https://blog.csdn.net/yangzhipengyzp/article/details/?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522190ba72b60177ce0ef525e57bbb4e72f%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=190ba72b60177ce0ef525e57bbb4e72f&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_positive~default-1-137750462-null-null.142^v102^pc_search_result_base9&utm_term=sdio%20wifi&spm=1018.2226.3001.4187#t8)


## 1、WiFi driver驱动框架

### 1.1、SDIO-Wifi模块介绍

SDIO- [Wifi模块](https://so.csdn.net/so/search?q=Wifi%E6%A8%A1%E5%9D%97&spm=1001.2101.3001.7020) 是基于SDIO接口的符合WiFi无线网络标准的嵌入式模块，内置无线网络协议IEEE802.11协议栈以及 TCP /IP协议栈，能够实现用户主平台数据通过SDIO口到无线 [网络](https://link.csdn.net/?target=https%3A%2F%2Factivity.huaweicloud.com%2Ffree_test%2Findex.html%3Futm_source%3Dhwc-csdn%26utm_medium%3Dshare-op%26utm_campaign%3D%26utm_content%3D%26utm_term%3D%26utm_adplace%3DAdPlace070851 "网络") 之间的转换。SDIO具有传输数据快，兼容SD、MMC接口等特点。

对于 [SDIO接口](https://so.csdn.net/so/search?q=SDIO%E6%8E%A5%E5%8F%A3&spm=1001.2101.3001.7020) 的WiFi，首先，它是一个SDIO的卡设备，然后具备了WiFi的功能。所以，<span style="background:#d3f8b6">注册的时候还是先以sdio设备去注册，然后检测到卡之后再去实现它的wifi功能。显然，他是用SDIO的协议，通过发命令和数据来控制实现WiFi功能。</span>

SDIO 故名思义，就是 SD 的 I/O 接口（interface）的意思，不过这样解释可能还有点抽像。更具体的说明，SD 本来是记忆卡的标准，但是现在也可以把 SD 拿来插上一些外围接口使用，这样的技术便是 SDIO。

所以 SDIO 本身是一种相当单纯的技术，透过 SD 的 I/O 引脚来连接外围，并且透过 SD 上的 I/O 数据引脚与这些外围传输数据，而且 SD 协会会员也推出很完整的 SDIO stack 驱动程序，使得 SDIO 外围（我们称为 SDIO 卡）的开发与应用变得相当热门。目前常见的 SDIO 外围（SDIO 卡）有：

- Wi-Fi card（无线 [网络](https://link.csdn.net/?target=https%3A%2F%2Factivity.huaweicloud.com%2Ffree_test%2Findex.html%3Futm_source%3Dhwc-csdn%26utm_medium%3Dshare-op%26utm_campaign%3D%26utm_content%3D%26utm_term%3D%26utm_adplace%3DAdPlace070851 "网络") 卡）
- CMOS sensor card（照相模块）
- GPS card
- GSM/GPRS modem card
- Bluetooth card

### 1.2、SDIO总线协议

SDIO总线 和 USB总线 类似，SDIO也有两端，其中一端是HOST端，另一端是device端。所有的通信都是由HOST端发送命令开始的，Device端只要能解析命令，就可以相互通信。 对于SDIO总线，它的<span style="background:#b1ffff">HOST端是开发板mmc控制器，而device端则是各种带SDIO接口的模块，比如SDIO WiFi模块</span>。

SDIO协议是由SD卡协议演化升级而来的，很多地方保留了SD卡的读写协议，同时SDIO协议又<span style="background:#d3f8b6">在SD卡协议之上添加了CMD52和CMD53命令</span>。由于这个，SDIO和SD卡规范间的一个重要区别就是<span style="background:#d3f8b6">增加了低速标准</span>。低速卡的目标应用是以最小的 硬件 来支持低速I/O能力。

SD总线通信是基于指令和数据比特流，起始位开始和停止位结束。SD总线通信有三个元素：

Command：由host发送到卡设备，使用CMD线发送；

Response：从card端发送到host端，作为对前一个CMD的相应，通过CMD线发送；

Data：即能从host传输到card，也能从card传输到host，通过data线传输。

SDIO的硬件电路

![](https://i-blog.csdnimg.cn/blog_migrate/9ebe4813887244cbb00b6431c6200a4e.png) 可以看到，SDIO接口总共有七个引脚，分别是<span style="background:#b1ffff">DAT0-3（数据），CLK（时钟），CMD（命令），VIO（电源）</span>

### 1.3、网络驱动架构

字符设备在 /dev 目录下会有对应设备文件节点并且在注册时会有设备号。网络设备没有对应设备节点和设备号，网络设备使用套接字来实现网络数据的接收和发送 **。** Linux 网络设备驱动程序的体系结构如图中黄色部分所示所示，从上到下可以划分为 4 层，依次为 [网络协议](https://so.csdn.net/so/search?q=%E7%BD%91%E7%BB%9C%E5%8D%8F%E8%AE%AE&spm=1001.2101.3001.7020 "网络协议") 接口层、网络设备接口层、提供实际功能的设备驱动功能层以及网络设备与媒介层。

![](https://i-blog.csdnimg.cn/blog_migrate/b20e789c6bbf59c8eca0e6db4e70da1d.png)

#### **网络协议接口层：**

最主要的功能就是<span style="background:#b1ffff">给上层协议提供了透明的数据包发送和接收接口</span>。当上层的协议需要发送数据包时，就会调用 dev\_queue\_xmit() 函数。当上层需要接收数据包时，就会调用netif\_rx()函数。函数定义如下：

#### ![](https://i-blog.csdnimg.cn/blog_migrate/a30ed430b9372e8a8f710254e8b70d4d.png) **网络设备接口层**

网络设备接口层的主要功能是<span style="background:#b1ffff">为千变万化的网络设备定义了统一、 抽象的数据结构 net_device 结构体，实现多种硬件在软件层次上的统一。</span>

Linux内核使用 <span style="background:#affad1">net_device结构体表示一个具体的网络设备</span>，网络驱动的核心就是初始化net\_device 结构体中的各个成员变量，然后将初始化完成以后的net\_device 注册到 Linux内核中。

net\_device数据结构定义在include/linux/netdevice.h，如下所示

![](https://i-blog.csdnimg.cn/blog_migrate/fbe590f9d7a0240fd5326d0db7364307.png)

1. name\[IFNAMSIZ\]; 设备的名称（如：eth0）
2. mem\_start， mem\_end：描述设备所用的共享内存，用于设备与内核沟通
3. base\_addr设备自有内存映射到I/O内存的起始地址
4. irq：络设备的中断号。
5. dev\_list 是全局网络设备列表。
6. napi\_list 是 napi 网络设备的列表入口。
7. wireless\_handlers，wireless\_data用于无线设备的参数和指针函数
8. if\_port接口所使用的端口类型
9. dma设备所使用的DMA通道
10. mtu MTU 代表最大传输单元 ，表示设备能处理的帧的最大尺寸
11. ethtool\_ops 是网络管理工具相关函数集，用户空间网络管理工具会调用此结构体中的相关函数获取网卡状态或者配置网卡。
12.<span style="background:#b1ffff"> netdev\_ops</span>是网络设备的操作集函数，包含了一系列的网络设备操作回调函数，
	<span style="background:#d3f8b6">类似字符设备中的 file_operations</span>

13.Ifindex：独一无二的ID，当设备以dev\_new\_index注册时分配给每个设备

14.dev\_id用于区别可由不同OS同时共享的同一种设备的诸多虚拟实例

#### **设备驱动功能层**

对应net\_device结构体中的<span style="background:#b1ffff">设备驱动功能函数netdev_ops</span>，例如<span style="background:#d3f8b6">xxx\_open()、xxx\_stop()、xxx\_tx()</span>等。另一部分是<span style="background:#b1ffff">中断处理函数</span>，它<span style="background:#affad1">负责接收硬件上的数据包并传给上层协议。 这也是wifi驱动主要需要实现的接口：</span>路径 os_dep\linux\os_intfs.c，<span style="background:#affad1">rtw_netdev_ops</span><span style="background:#d3f8b6">最后在probe中赋值给net_device中设备驱动功能函数netdev_ops。</span>

![](https://i-blog.csdnimg.cn/blog_migrate/97446b98133957956dfa62d4530924e7.png)

### 1.4、MMC整体框架

Linux 内核中，MMC不仅是一个驱动，而是一个子系统。内核把mmc, sd以及sdio三者的驱动代码整合在一起，俗称MMC子系统。

![](https://i-blog.csdnimg.cn/blog_migrate/0fcfe959f93b0372c2eaf9d795f0c5ea.png)

<span style="background:#b1ffff">Linux MMC 子系统</span>主要分成三个部分：

- MMC核心层：完成不同协议和规范的实现，为host层和设备驱动层提供接口函数。MMC核心层由三个部分组成：MMC，SD和SDIO，分别为三类设备驱动提供接口函数；
- <span style="background:#affad1">Host 驱动层</span>：针对不同<span style="background:#fff88f">主机端的SDHC、MMC控制器的驱动</span>；
<span style="background:#affad1">- Client 驱动层：</span>针对<span style="background:#fff88f">不同客户端的设备驱动程序</span>。如SD卡、T-flash卡、SDIO接口的GPS和wifi等设备驱动

## 2、WiFi 驱动

<span style="background:#b1ffff">分为两部分，上面为主机端驱动，下面firmware。</span>

主机端驱动包括上面讲的网络子系统，mmc子系统。

Firmware在WiFi芯片内部运行,用来实现802.3的帧和802.11帧之间的转换。

Wifi工作流程如下：

![](https://i-blog.csdnimg.cn/blog_migrate/20e97fe25d16cb0cd0fb6b84a26b3560.png)

### <span style="background:#b1ffff">Wifi driver (mmc 子系统中Client 驱动层)</span>

#### sdio 驱动结构体

![](https://i-blog.csdnimg.cn/blog_migrate/fffadfd9ae77dd9863a429bed4a9ee78.png)

#### 模块加载函数：(?????)

![君正T23N芯片开发/【君正T23N\_IPC】/知识积累/网页知识学习/assets/SDIO wifi驱动框架/file-20250810171415186.png](assets/SDIO%20wifi驱动框架/file-20250810171415186.png)

<span style="background:#affad1">当sdio控制器扫描到设备的时候会去读取设备的id即wifi模块的pid和vid，如果设备id匹配上了之后会调用使用sdio\_register\_driver注册进去的probe函数。</span>

![君正T23N芯片开发/【君正T23N\_IPC】/知识积累/网页知识学习/assets/SDIO wifi驱动框架/file-20250810171415417.png](assets/SDIO%20wifi驱动框架/file-20250810171415417.png)

![](https://i-blog.csdnimg.cn/blog_migrate/e44cf3809372634cfb7c25f4fd659b88.png)

当使用命令ifconfig eth0 up时， netdev\_open 接口将会被调用：

netdev\_open

|---> rtw\_hal\_init硬件抽象层的初始化

|--->rtw\_start\_drv\_threads

|--->kthread\_run(rtw\_cmd\_thread, padapter, "RTW\_CMD\_THREAD"); 开一个cmd线程，用来发送命令

|--->rtw\_hal\_start\_thread开一个数据传输线程

|---> rtw\_hal\_enable\_interrupt使能host中断

|--->rtw\_cfg80211\_init\_wiphy 初始化cfg80211wifi的phy

|--->rtw\_netif\_wake\_queue 唤醒队列

接收数据：

中断上半部分

sd\_sync\_int\_hdl

|--->rtw\_start\_drv\_threads

|--->sd\_int\_hdl

|--->sd\_int\_dpc

|--->sd\_recv\_rxfifo从接收fifo读数据

|--->sd\_rxhandler

|--->rtw\_enqueue\_recvbuf 入接收队列

|--->tasklet\_schedule 调度tasklet处理数据包

中断下半部分：

rtl8188fs\_recv\_tasklet

|--->rtw\_start\_drv\_threads

|--->rtl8188fs\_recv\_hdl

|--->rtw\_dequeue\_recvbuf从接收队列取出数据包

|---> rtw\_skb\_alloc申请skbuff缓冲区

|--->pre\_recv\_entry数据包上报

数据发送：

rtw\_xmit\_entry

|--->\_rtw\_xmit\_entry

|--->rtw\_xmit

|--->do\_queue\_select选择一个发送队列

|--->rtl8188fs\_hal\_xmit

|--->rtw\_xmitframe\_enqueue

|--->rtw\_xmit\_classifier将数据包放入发送队列中

## 3.Host驱动

SDHC：Secure Digital(SD) Host Controller，是指一套sd host控制器的设计标准，一般挂载sd和sdio设备，隶属于mmc子系统，其寄存器偏移以及意义都有一定的规范，并且提供了对应的驱动程序，方便vendor进行host controller的开发。

mmc core将sdhci host抽象出struct sdhci\_host来进行管理和维护。

![](https://i-blog.csdnimg.cn/blog_migrate/1731e6790ef64a58799cb297b4bad0f2.png)

1. hw\_name 硬件总线名
2. ops 硬件操作函数集
3. mmc mmc设备结构体
4. max\_clk，timeout\_clk，clk\_mu，pwr 硬件相关，最大支持的频率，电流，电压等。
5. mrq mmc请求
6. cmd用于存放当前要向硬件发送的命令
7. data 用于存放当前mmc请求的数据
8. sg\_miter 存放pio当前状态，目前进行io操作的页面地址，当前页面指针，里面指向了当前页面的scatterlist，实现不连续的物理内存块到连续的虚拟内存块映射。scatterlist介绍查看 [Linux 4.14内核———— scatterlist介绍\_struct scatterlist-CSDN博客](https://blog.csdn.net/yangguoyu8023/article/details/125332274 "Linux 4.14内核———— scatterlist介绍_struct scatterlist-CSDN博客")
9. blocks 剩余需要进行PIO传输的块数量
10. adma\_table-align\_mask ADMA传输相关，当使用ADMA传输数据时被使用
11. finish\_tasklet mmc请求，命令发送完成，数据传输完成的回调函数
12. buf\_ready\_int 用于唤醒发送读取命令后的读准备函数
13. tuning\_done 读取命令是否发送成功

sdhci core要求host提供标准的访问硬件的一些方法，用于实际和硬件交互的驱动，这些方法就被定义在了struct sdhci\_ops结构体内部。

![](https://i-blog.csdnimg.cn/blog_migrate/0e65b578720478acf2033a1ab0478542.png)

sdhci core使用sdhci\_ops作为sdhci host抽象出来的mmc host的操作集，用于实现mmc core关于host的操作函数，如向硬件发送命令请求（ request 方法），检测host的卡槽中card的插入状态（get\_cd方法）。pre\_req, pre\_req是为了实现异步请求处理而设置的，当一个异步请求还没有处理完成的时候，可以先准备另外一个异步请求而不必等待。

![](https://i-blog.csdnimg.cn/blog_migrate/a45fae7f6c5992cfa815123d1c60f640.png)

Probe硬件探测函数：

sdhci\_esdhc\_imx\_probe

|--->sdhci\_pltfm\_init

|--->sdhci\_alloc\_host 申请一个host

|--->host->ops = &sdhci\_pltfm\_ops;注册通用电源管理操作函数

|--->request\_mem\_region 向内核申请io内存

|--->ioremap将io内存地址映射到内核虚拟地址

|--->devm\_kzalloc申请host设备资源内存

|--->devm\_clk\_get获取时钟源

|--->sdhci\_esdhc\_imx\_probe\_dt检查设备树配置，初始化pltfm\_imx\_data和wifi\_mmc\_host结构体

|--->sdhci\_add\_host

|--->mmc->ops = &sdhci\_ops;

|--->tasklet\_init(,sdhci\_tasklet\_finish，)请求处理完成时的软中断函数，通知mmc core request已经处理完成

|--->request\_threaded\_irq注册host中断，中断上半部分sdhci\_irq，下半部分线程化中断sdhci\_thread\_irq。

|--->mmc\_add\_host注册mmc\_host到mmc core中

|--->sdhci\_enable\_card\_detection 扫描硬件检查是否有卡插入

收发数据：

mmc\_wait\_for\_req ->\_\_mmc\_start\_req->mmc\_start\_request-> host->ops->request

mmc core 最后调用host->ops-> request 发送请求命令。

sdhci\_request

|--->sdhci\_do\_get\_cd 检查card还在不在

|--->sdhci\_send\_command

|--->sdhci\_prepare\_data准备数据，设置需要的寄存器

|--->sdhci\_set\_transfer\_irqs 根据传输方式使能PIO或者DMA中断

|--->sdhci\_writel(host, host->ier, SDHCI\_INT\_ENABLE); 清中断标志

|--->sdhci\_writel(host, host->ier, SDHCI\_SIGNAL\_ENABLE);使能中断

|--->sdhci\_set\_transfer\_mode设置传输模式PIO or DMA

|--->sdhci\_writew(host,SDHCI\_MAKE\_CMD(cmd->opcode,flags), SDHCI\_COMMAND);向设备IOMEM写命令，随后触发中断 **sdhci\_irq**

|--->mmiowb 保证 编译器 顺序编译，防止编译器优化打乱执行顺序

**sdhci\_irq**

|--->sdhci\_data\_irq

|--->sdhci\_transfer\_pio

|--->sdhci\_read\_block\_pio 从card的IO设备缓冲区读报文到内存

|--->sdhci\_write\_block\_pio 把报文从内存写入IO设备缓冲区

|--->sg\_miter\_stop停止物理地址到虚拟地址映射

**sdhci\_irq** 如果是卡插拔或者读数据中断返回IRQ\_WAKE\_THREAD，唤醒线程化中断，

**sdhci\_thread\_irq**

|--->sdhci\_card\_event 向mmc core报告卡插入或者拔出

|--->sdio\_run\_irqs 运行wifi接收数据中断sd\_sync\_int\_hdl

|--->process\_sdio\_pending\_irqs

|--->func->irq\_handler(func); wifi 驱动只注册了一个接收中断，直接调用，这里的irq\_handler就是wifi driver probe函数注册的sdio中断函数sd\_sync\_int\_hdl

## 3.WIFI驱动移植

设备树节点：

下面两个同名节点会合并成一个节点，Pingctrl和时针由host驱动自己管理，pinctrl-0~ pinctrl-3对应设备三种工作状态的引脚配置。cd-gpios用来监测卡是否存在<font color="#9bbb59">，vmmc-supply为电源管理支持</font>。

![](https://i-blog.csdnimg.cn/blog_migrate/0090e61da286eeb79285605ff3272eda.png)

![](https://i-blog.csdnimg.cn/blog_migrate/7869ad13f2e2532ec57db1706f89ca72.png)

修改设备树节点后直接将wifi driver和host driver编译进内核，插入wifi模块后使用ifconfig -a可以看到wlan0 节点，这样wifi驱动就移植好了。 ![](https://i-blog.csdnimg.cn/blog_migrate/41a0af8916c0905aecfd1bcfd416deab.png)

## 4.总结

Wifi模块对于网络子系统来说，是一个网络设备，对于mmc子系统来说，Wifi模块就是一个块设备，报文收发就是对一个存储卡的读写。<span style="background:#b1ffff">wifi驱动就是一个存储卡到网络设备转换的媒介。对于驱动开发者来说，需要关注的是host驱动和设备树节点。</span>