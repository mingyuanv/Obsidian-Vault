---
title: Linux SD卡驱动开发(一) —— SD 相关基础概念-CSDN博客
source: https://blog.csdn.net/zqixiao_09/article/details/51039378
author: 
published: 
created: 2025-04-15
description: 文章浏览阅读1.6w次，点赞21次，收藏119次。本文介绍了Linux系统中SD卡驱动的基础知识，包括SD/MMC卡的概念、SDIO的特性、MCI接口以及SD协议的总线接口和请求处理流程。文章详细阐述了SD卡在开发板上的硬件连接，并探讨了MMC/SD设备驱动在Linux系统中的结构层次，强调了Core核心层的重要作用。
tags:
  - clippings
---
# **一.SD/MMC卡基础概念**

## **1.1.什么是MMC卡**

**MMC：** MMC就是MultiMediaCard的缩写，即多媒体卡。它是一种非易失性存储器件，体积小巧(24mm\*32mm\*1.4mm)，<span style="background:#d3f8b6">容量大,耗电量低,传输速度快</span>，广泛应用于消费类电子产品中。

## **1.2.什么是SD卡**

**SD：** SD卡为Secure Digital Memory Card, 即 <span style="background:#affad1">**安全数码卡**</span> 。它在MMC的基础上发展而来，增加了两个主要特色： SD卡强调数据的安全安全，可以设定所储存的使用权限，防止数据被他人复制;另外一个特色就是 传输速度比2.11版的MMC卡快 。在数据传输和物理规范上，SD卡(24mm\*32mm\*2.1mm,比 MMC卡更厚一点)，向前兼容了MMC卡.<span style="background:#affad1">所有支持SD卡的设备也支持MMC卡。SD卡和2.11版的MMC卡完全兼容。</span>

## **1.3.什么是SDIO**

**SDIO** ：SDIO是在<span style="background:#d3f8b6">SD标准上定义了一种外设接口</span>，它和SD卡规范间的一个重要区别是增加了低速标准。在SDIO卡只需要SPI和1位SD传输模式。低速卡的目标应用是以最小的 硬件 开销支持低速IO能力。

## **1.4.什么是MCI**

MCI：MCI是Multimedia Card Interface的简称，即<span style="background:#d3f8b6">多媒体卡接口。上述的MMC,SD,SDIO卡定义</span>的接口都属于MCI接口。MCI这个术语在驱动程序中经常使用，很多文件， 函数 名字都包括”mci”.

## **1.5.MMC/SD/SDIO卡的区别**

**![](https://img-blog.csdn.net/20160401203824552?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)  
**

SDIO 是目前我们比较关心的技术，SDIO 故名思义，就是 **SD 的 I/O 接口（interface ）** 的意思，不过这样解释可能还有点抽像。更具体的说明，SD 本来是记忆卡的标准，但是现在也可以<span style="background:#b1ffff">把 SD 拿来插上一些外围接口使用，这样的技术便是 SDIO </span>。

所以 SDIO 本身是一种相当单纯的技术，透过 SD 的 I/O 接脚来连接外部外围，并且透过 SD 上的I/O 数据接位与这些外围传输数据，而且 SD 协会会员也推出很完整的 SDIO stack 驱动程序，使得SDIO 外围（我们称为 SDIO 卡）的开发与应用变得相当热门。

现在已经有非常多的手机或是手持装置都支持 SDIO 的功能（SD 标准原本就是针对 mobile device而制定），而且许多 SDIO 外围也都被开发出来，让手机外接外围更加容易，并且开发上更有弹性（不需要内建外围）。目前常见的 SDIO 外围（SDIO 卡）有：

<span style="background:#fff88f">·Wi-Fi card （无线网络卡）  </span>
<span style="background:#fff88f">·CMOS sensor card （照相模块）  </span>
<span style="background:#fff88f">·GPS card  </span>
<span style="background:#fff88f">·GSM/GPRS modem card  </span>
<span style="background:#fff88f">·Bluetooth card  </span>
<span style="background:#fff88f">·Radio/TV card （很好玩）</span>

SDIO 的应用将是未来 嵌入式系统 最重要的接口技术之一，并且也会取代目前 GPIO 式的 SPI 接口。  

# **二、开发板SD资源**

以Exynos4412开发板为例，其SD卡硬件原理图如下：

![](https://img-blog.csdn.net/20160401204657008?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)

  

图中可以看到，<span style="background:#affad1">SD卡设备的连接方式就是SDIO总线的驱动方式</span>，这里使用EINT7作为NCD的控制器，当SD卡设备插入/取出时均会中断响应。

  

# **三、 SD协议概要**

## **1、 总线接口**

按照SD卡的协议的描述可分为2种总线的接口

### **SD BUS**

物理层定义：

<span style="background:#d3f8b6">D0-D3 数据传送</span>

<span style="background:#d3f8b6">CMD 进行CMD 和Respons</span>

<span style="background:#d3f8b6">CLK 大家最熟悉的HOST时钟信号线了</span>

<span style="background:#d3f8b6">VDD VSS 电源和地</span>

  

### **SPI BUS**

一般用SPI协议的接口来做

物理层定义：

<span style="background:#d3f8b6">CLK HOST时钟信号线了</span>

<span style="background:#d3f8b6">DATAIN HOST-àSD Card数据信号线</span>

<span style="background:#d3f8b6">DATAOUT SD Card àHOST数据信号线</span>

  

## **2、请求处理流程**(????)

根据协议，MMC/SD卡的驱动被分为： **卡识别阶段** 和 **数据传输阶段** 。

在卡识别阶段通过命令使MMC/SD处于：空闲(idle)、准备(ready)、识别(ident)、等待(stby)、不活动(ina)几种不同的状态；

而在数据传输阶段通过命令使MMC/SD处于：发送(data)、传输(tran)、接收(rcv)、程序(prg)、断开连接(dis)几种不同的状态。

所以可以总结MMC/SD在工作的整个过程中分为两个阶段和十种状态。下面使用图形来描述一下在两个阶段中这十种状态之间的转换关系。

### **a -- 卡识别阶段**  

![](https://img-blog.csdn.net/20160401211443441?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)  

### **b -- 数据传输阶段**  

**![](https://img-blog.csdn.net/20160401211542129?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)  
**

  

# **四、 MMC/SD设备驱动在Linux中的结构层次**

在 Linux 中MMC/SD卡的记忆体都当作<span style="background:#b1ffff">块设备</span>。MMC/SD设备驱动代码在linux-2.6.38.2<span style="background:#b1ffff">\\drivers\\mmc 分别有card、core和host三个文件夹，</span>

<span style="background:#b1ffff">**card层** </span>要<span style="background:#d3f8b6">把操作的数据以块设备的处理方式写到记忆体上或从记忆体上读取</span>；

<span style="background:#b1ffff">**core层** </span>则是<span style="background:#d3f8b6">将数据以何种格式，何种方式在 MMC/SD主机控制器与MMC/SD卡的记 忆体(即块设备)之间进行传递</span>，这种格式、方式被称之为规范或协议，

<span style="background:#b1ffff">**host层** </span>下的代码<span style="background:#d3f8b6">就是你要动手实现的具体MMC/SD设备驱动了</span>，包括RAM芯片中的 SDI控制器(支持对MMC/SD卡的控制，俗称MMC/SD主机控制器)和SDI控制器与MMC/SD卡的硬件接口电路。

那么，card、core和host这三层的关系，我们用一幅图来进行描述，图如下：

![](https://img-blog.csdn.net/20160401211158721?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)

从这幅图中的关系可以看出，整个MMC/SD模块中<span style="background:#d3f8b6">最重要的部分是 **Core核心层** ，他提供了一系列的接口函数，对上提供了将主机驱动注册到系统，给应用程序提供设备访问接口，对下提供了对主机控制器控制的方法及块设备请求的支持</span>。对于主机控制器的操作就是对相关寄存器进行读写，而对于MMC/SD设备的请求处理则比较复杂。