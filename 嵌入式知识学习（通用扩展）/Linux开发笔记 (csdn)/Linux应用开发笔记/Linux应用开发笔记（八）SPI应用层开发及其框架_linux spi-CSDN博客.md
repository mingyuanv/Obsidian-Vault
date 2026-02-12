---
title: "Linux应用开发笔记（八）SPI应用层开发及其框架_linux spi-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/137743668?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读2.8k次，点赞27次，收藏43次。本文详细介绍了SPI协议的扩展、不同模式的区别，以及Linux内核的SPI驱动框架结构，包括用户空间接口、内核驱动层和硬件协同。同时提供了SPI应用编程的示例，如数据结构、ioctl函数使用和基本操作流程。"
tags:
  - "clippings"
---
本文详细介绍了SPI协议的扩展、不同模式的区别，以及Linux内核的SPI驱动框架结构，包括用户空间接口、内核驱动层和硬件协同。同时提供了SPI应用编程的示例，如数据结构、ioctl函数使用和基本操作流程。

摘要生成于 [C知道](https://ai.csdn.net/?utm_source=cknow_pc_ai_abstract) ，由 DeepSeek-R1 满血版支持， [前往体验 >](https://ai.csdn.net/?utm_source=cknow_pc_ai_abstract)

---

## 前言

  与 [IIC](https://so.csdn.net/so/search?q=IIC&spm=1001.2101.3001.7020) 类似，SPI协议也是我们的老朋友了，这里依然不多作赘述，本文将介绍SPI的驱动框架和应用程序编写。

## 一、扩展SPI协议（Single/Dual/Quad/Octal SPI）

  为了适应更高速率的通讯需求，半导体厂商扩展SPI协议，主要发展出了Dual/Quad/Octal SPI协议，加上 标准SPI协议（Single SPI），这四种协议的主要区别是数据线的数量及通讯方式，具体见下表。

| 协议 | 数据线数量及功能 | 通讯方式 |
| --- | --- | --- |
| Single SPI（标准SPI） | 1根发送，1根接收 | 全双工 |
| Dual SPI（双线SPI） | 收发共用2根数据线 | 半双工 |
| Quad SPI（四线SPI） | 收发共用4根数据线 | 半双工 |
| Octal SPI（八线SPI） | 收发共用8根数据线 | 半双工 |

  扩展的三种SPI协议都是半双工的通讯方式，也就是说它们的数据线是分时进行收发 数据的。例如，标准SPI（Single SPI）与双线SPI（Dual SPI）都是两根数据线，但标准SPI（Single SPI）的其中一根数据线只用来发送，另一根数据线只用来接收，即全双工；而双线SPI（Dual SPI）的两根线都具有收发功能，但在同一时刻只能是发送或者是接收，即半双工，但其主要针对 [SPI Flash](https://so.csdn.net/so/search?q=SPI%20Flash&spm=1001.2101.3001.7020) ，而不是所有SPI外设；四线SPI（Quad SPI）同样主要针对SPI Flash，其目标是在一个时钟周期内传输4个bit数据；Octal SPI（八线SPI）通同一时钟周期内能够传输更多的数据，从而实现了更高的传输速率，此外Octal SPI还引入了多种时钟模式，以支持不同的数据传输速率和时序要求。

- SDR和DDR模式

  扩展的SPI协议还增加了SDR模式（单倍速率Single Data Rate）和DDR模式（双倍速率Double Data Rate）。例如在标准SPI协议的SDR模式下，只在SCK的单边沿进行数据传输，即一个SCK时钟只传输一位数据；而在它的DDR模式下，会在SCK的上升沿和下降沿都进行数据传输，即一个SCK时钟能传输两位数据，传输速率提高一倍。

## 二、SPi驱动框架

- 用户空间

  对于用户而言，SPI驱动 模型 提供了一种方便、灵活的方式来与外部设备进行通信。用户无需深入了解底层硬件细节，只需通过SPI接口发送相应的指令和数据，即可实现对外部设备的控制或数据的读取。这种抽象化的接口使得用户能够更专注于应用层面的开发，提高了开发效率和便利性。例如，和 MTD 层交互以便把 SPI 接口的存储设备实现为某个文件系统，和TTY 子系统交互把 SPI 设备实现为一个 TTY 设备，和网络子系统交互以便把一个 SPI 设备实现为一个网络设备，等等。当然，如果是一个专有的 SPI 设备，我们也可以按设备的协议要求，实现自己的专有协议驱动。

- 内核方面

  在内核层面，SPI驱动模型负责管理和控制SPI接口的工作。 Linux 内核中的SPI驱动架构通常分为三个层次：SPI核心层、SPI控制器驱动层和SPI设备驱动层。  
   - SPI核心层（SPI通用接口层）是Linux的SPI核心部分，提供了核心 数据结构 的定义、SPI控制器驱动和设备驱动的注册、注销管理等API。其为硬件平台无关层，向下屏蔽了物理总线控制器的差异，定义了统一的访问策略和接口；其向上提供了统一的接口，以便SPI设备驱动通过总线控制器进行数据收发。  
   - SPI控制器驱动层，每种处理器平台都有自己的控制器驱动，属于平台移植相关层。它的职责是为系统中每条 SPI总线 实现相应的读写方法。在物理上，每个SPI控制器可以连接若干个SPI从设备。  
   - SPI设备驱动层则实现了与具体SPI设备的通信协议和数据交换机制。内核通过SPI驱动模型，为上层应用提供了统一的接口，使得应用能够通过SPI接口与底层硬件进行通信。同时，内核还负责处理SPI接口的中断和错误情况，确保数据传输的稳定性和可靠性。

- 硬件方面

  在硬件方面，SPI驱动模型与具体的SPI控制器和从设备紧密相关。SPI控制器负责产生时钟信号、控制从设备的使能以及数据的发送和接收。从设备则根据SPI接口的协议进行数据的传输和处理。SPI驱动模型需要与这些硬件设备进行协同工作，确保数据的正确传输和设备的正常工作。 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/223770f33b39c3bb9a3d8816a4a070ed.png)

## 三、SPI应用编程

### 1\. SPI相关数据结构与ioctl函数

  编写应用程序需要使用到spi\_ioc\_transfer 结构体 ，如下所示:

```c
struct spi_ioc_transfer {
   __u64             tx_buf;     //发送数据缓存
   __u64             rx_buf;     //接收数据缓存

   __u32             len;        //数据长度
   __u32             speed_hz;   //通讯速率

   __u16             delay_usecs;    //两个spi_ioc_transfer之间的延时，微秒
   __u8              bits_per_word;  //数据长度
   __u8              cs_change;      //取消选中片选
   __u8              tx_nbits;       //单次数据宽度(多数据线模式)
   __u8              rx_nbits;       //单次数据宽度(多数据线模式)
   __u16             pad;
};
1234567891011121314
```

  在编写应用程序时还需要使用ioctl函数设置spi相关配置，其函数原型如下

```c
#include <sys/ioctl.h>

 int ioctl(int fd, unsigned long request, ...);
123
```

  其中对于终端 request 的值常用的有以下几种:

| 参数取值 | 功能 |
| --- | --- |
| SPI\_IOC\_RD\_MODE32 | 设置读取SPI模式(对应上文的SPI的四种模式的表格,SPI\_MODE\_x) |
| SPI\_IOC\_WR\_MODE32 | 设置写入SPI模式(对应上文的SPI的四种模式的表格,SPI\_MODE\_x) |
| SPI\_IOC\_RD\_LSB\_FIRST | 设置SPI读取数据模式(LSB先行返回1) |
| SPI\_IOC\_WR\_LSB\_FIRST | 设置SPI写入数据模式。(0:MSB，非0：LSB) |
| SPI\_IOC\_RD\_BITS\_PER\_WORD | 设置SPI读取设备的字长 |
| SPI\_IOC\_WR\_BITS\_PER\_WORD | 设置SPI写入设备的字长 |
| SPI\_IOC\_RD\_MAX\_SPEED\_HZ | 设置读取SPI设备的最大通信频率 |
| SPI\_IOC\_WR\_MAX\_SPEED\_HZ | 设置写入SPI设备的最大通信速率 |
| SPI\_IOC\_MESSAGE(N) | 一次进行双向/多次读写操作 |

### 2\. 基本函数

- 初始化
```c
void spi_init(void)
{
    int ret = 0;
    //打开 SPI 设备
    fd = open(SPI_DEV_PATH, O_RDWR);
    if (fd < 0)
        printf("can't open %s\n",SPI_DEV_PATH);

    //spi mode 设置SPI 工作模式
    ret = ioctl(fd, SPI_IOC_WR_MODE32, &mode);
    if (ret == -1)
        printf("can't set spi mode\n");

    //bits per word  设置一个字节的位数
    ret = ioctl(fd, SPI_IOC_WR_BITS_PER_WORD, &bits);
    if (ret == -1)
        printf("can't set bits per word\n");

    //max speed hz  设置SPI 最高工作频率
    ret = ioctl(fd, SPI_IOC_WR_MAX_SPEED_HZ, &speed);
    if (ret == -1)
        printf("can't set max speed hz\n");

    //打印
    printf("spi mode: 0x%x\n", mode);
    printf("bits per word: %d\n", bits);
    printf("max speed: %d Hz (%d KHz)\n", speed, speed / 1000);
}
12345678910111213141516171819202122232425262728
```
- 数据传输
```c
void transfer(int fd, uint8_t const *tx, uint8_t const *rx, size_t len)
{
   int ret;

   struct spi_ioc_transfer tr = {
       .tx_buf = (unsigned long)tx,    //发送缓冲区地址
       .rx_buf = (unsigned long)rx,    //接收缓冲区地址
       .len = len,                    //一次传输的数据长度
       .delay_usecs = delay,        //如果不为零则用于设置两次传输之间的时间延迟
       .speed_hz = speed,            //speed_hz,指定SPI通信的比特率
       .bits_per_word = bits,        //指定字节长度，既一个字节占用多少比特
       .tx_nbits = 1,                    
       .rx_nbits = 1
   };

   ret = ioctl(fd, SPI_IOC_MESSAGE(1), &tr);
   
   if (ret < 1)
123456789101112131415161718
```

**注：tx\_nbits/rx\_nbits 指定“写/读”数据宽度，SPI 支持1、2、4位宽度，如果没有特殊数据要求的话，一般设置为1或0（设置为0表示使用默认的宽度既宽度为1）。**

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/137743668

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

 [![](https://csdnimg.cn/release/blogv2/dist/pc/img/toolbar/Group-dark.png) 点击体验  
DeepSeekR1满血版](https://ai.csdn.net/?utm_source=cknow_pc_blogdetail&spm=1001.2101.3001.10583) 隐藏侧栏

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

![](https://i-blog.csdnimg.cn/blog_migrate/223770f33b39c3bb9a3d8816a4a070ed.png)