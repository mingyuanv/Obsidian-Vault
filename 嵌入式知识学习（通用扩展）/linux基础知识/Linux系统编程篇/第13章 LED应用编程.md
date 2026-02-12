---
title: "【北京迅为】《iTOP-3588开发板系统编程手册》-第13章 LED应用编程"
source: "https://blog.csdn.net/BeiJingXunWei/article/details/138001842"
author:
  - "[[BeiJingXunWei]]"
published: 2024-04-20
created: 2025-09-11
description: "文章浏览阅读1.4k次，点赞27次，收藏30次。RK3588是一款低功耗、高性能的处理器，适用于基于arm的PC和Edge计算设备、个人移动互联网设备等数字多媒体应用，RK3588支持8K视频编解码，内置GPU可以完全兼容OpenGLES 1.1、2.0和3.2。RK3588引入了新一代完全基于硬件的最大4800万像素ISP，内置NPU，支持INT4/INT8/INT16/FP16混合运算能力，支持安卓12和、Debian11、Build root、Ubuntu20和22版本登系统。了解更多信息可点击【粉丝群】824412014。_rk3588 led"
tags:
  - "clippings"
---
[RK3588](https://so.csdn.net/so/search?q=RK3588&spm=1001.2101.3001.7020) 是一款低功耗、高性能的处理器，适用于基于arm的PC和 Edge 计算设备、个人移动互联网设备等数字多媒体应用，RK3588支持8K [视频编解码](https://so.csdn.net/so/search?q=%E8%A7%86%E9%A2%91%E7%BC%96%E8%A7%A3%E7%A0%81&spm=1001.2101.3001.7020) ，内置GPU可以完全兼容OpenGLES 1.1、2.0和3.2。RK3588引入了新一代完全基于硬件的最大4800万像素ISP，内置NPU，支持INT4/INT8/INT16/FP16混合运算能力，支持安卓12和、Debian11、Build root、Ubuntu20和22版本登系统。了解更多信息可点击 [迅为官网](http://www.topeetboard.com/Product/3588hk.html "迅为官网  ")

【粉丝群】824412014

【实验平台】：迅为RK3588开发板

【内容来源】《iTOP-3588开发板系统编程手册》

【全套资料及网盘获取方式】联系淘宝客服加入售后技术支持群内下载

【视频介绍】： [【强者之芯】 新一代AIOT高端应用芯片 iTOP -3588人工智能工业AI主板](https://blog.csdn.net/BeiJingXunWei/article/details/?share_source=copy_web&vd_source=2028a54593d986008d44cdb9a5d790c7)

---

## 第13章 LED应用编程

在本章节将会使用系统编程的知识来对LED（可在底板GPIO座子连接LED小灯）进行实际的控制。

### 13.1应用层操控硬件的两种方式

在 Linux 操作系统中， [应用层](https://so.csdn.net/so/search?q=%E5%BA%94%E7%94%A8%E5%B1%82&spm=1001.2101.3001.7020 "应用层") 操控硬件可以使用以下两种方式对硬件设备进行控制：

****1.通过/dev目录下的设备节点来控制硬件设备：****

在Linux系统中，设备节点是一种虚拟文件，它代表着硬件设备或设备驱动程序，提供了一种访问硬件设备的标准接口。在/dev目录下，每个设备节点都对应着一个硬件设备或设备驱动程序，它们可以像普通文件一样被打开、读取、写入和关闭等操作。通过这些操作，用户可以访问和控制硬件设备。

例如，/dev/sda代表着第一个硬盘，/dev/ttyS0代表着第一个串口。用户可以使用文件操作函数，如open()、read()、write()等对设备节点进行访问和操作，从而控制硬件设备。

****2.通过sysfs文件系统对硬件设备进行操控：****

Sysfs是Linux内核提供的一种虚拟文件系统，它以文件系统的形式向用户空间公开了内核对象的属性和状态信息。通过sysfs，用户空间应用程序可以获取和修改内核中的各种对象属性，例如硬件设备、总线、进程等等。

在sysfs中，每个内核对象都被表示为一个目录，该目录中的文件包含有关该对象的信息和控制该对象的接口。例如，在/sys/devices目录下，每个硬件设备都有一个目录，该目录包含有关该设备的信息和控制该设备的接口。在/sys/class目录下，每个类都有一个目录，该目录包含有关该类的信息和控制该类的接口。在/sys/ kernel 目录下，内核的一些参数和状态信息都可以被查看和修改。

sysfs的特点如下所示：

| 步骤 | 描述 |
| --- | --- |
| 可读写 | sysfs中的大多数文件都是可读写的，允许应用程序读取和修改内核对象的属性和状态信息 |
| 动态更新 | sysfs中的文件随着内核对象的状态和属性的变化而动态更新，应用程序可以实时获取最新的信息 |
| 轻量级 | sysfs是一个轻量级的虚拟文件系统，可以快速地读取和修改内核对象的信息 |
| 易于使用 | sysfs的接口简单明了，易于使用。用户空间的应用程序可以使用标准的文件系统操作来访问sysfs中的文件，例如读取、写入和查找等 |
| 可扩展性 | sysfs可以动态添加和删除内核对象，因此可以随着内核对象的增加而动态地扩展 |

在Linux操作系统中，设备驱动程序负责控制硬件设备的访问和操作，对于简单的设备，驱动程序通常会使用sysfs文件系统来实现用户空间与内核空间的通信。在这种情况下，驱动程序会将设备的一些属性导出到sysfs文件系统中，以属性文件的形式为用户空间提供对这些数据和属性的访问支持。例如，LED和GPIO设备可以通过sysfs文件系统来控制。

sysfs文件系统使用文件和目录来表示内核对象，其中每个文件都表示一个属性。应用程序可以使用标准的文件系统操作（如读、写和查找等）来访问sysfs中的这些文件，从而读取或修改内核对象的属性。sysfs文件系统具有动态更新、可读写、轻量级和易于使用等特点，因此非常适合用于控制简单的硬件设备。

然而，对于较复杂的设备，通常需要使用设备节点的方式进行控制。例如，液晶显示器（LCD）、触摸屏、摄像头等设备，其控制需要更复杂的通信和数据处理方式。因此，驱动程序会创建设备节点来表示这些设备，并提供一组设备驱动程序接口（例如ioctl和mmap等）供用户空间程序进行访问。用户空间程序可以使用标准的I/O系统调用来读取或写入设备节点，从而控制这些设备。

### 13.2 LED硬件控制

iTOP-3588开发板靠近耳机接口一侧有一个gpio座子，其中5号引脚默认为gpio，6号引脚为GND，可外接一个LED小灯，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第13章 LED应用编程/b3fd6785588a0190aebd0a7d6fec18cf\_MD5.png](assets/第13章%20LED应用编程/b3fd6785588a0190aebd0a7d6fec18cf_MD5.png)

打开rk3588-evb.dtsi设备树对以下内容进行修改，修改完成如下所示：  
![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第13章 LED应用编程/1e92e3470c7e435ba87243e0eaa05c2b\_MD5.png](assets/第13章%20LED应用编程/1e92e3470c7e435ba87243e0eaa05c2b_MD5.png)

至此，关于设备树相关的修改就完成了，保存退出之后，编译内核，然后将生成的boot.img镜像烧写到开发板上即可。

内核对于LED设备的控制使用的是标准LED驱动框架，在/dev 目录下并没有其对应的设备节点，其最终的控制就是使用 sysfs 子系统实现的。首先使用以下命令进入到/sys/class/leds 目录下，如下图所示：

> cd /sys/class/leds/

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第13章 LED应用编程/918b1066ade08cfd305e482697a95552\_MD5.png](assets/第13章%20LED应用编程/918b1066ade08cfd305e482697a95552_MD5.png)

这里的work目录就是用户 LED 设备文件夹，进入work目录下，如下所示：

该目录下的文件分别为brightness、device、max\_brightness、power、subsystem和uevent，需要注意的是 brightness和max\_brightness 文件，这三个文件都是 LED 设备的属性文件，下面对这两个文件分别进行讲解：

****brightnes**** ****s**** ：表示当前 LED 灯的亮度值，它的可取值范围为 \[0~max\_brightness\]，iTOP-RK3588的LED 设备不支持多级亮度，以非 0 值来表示 LED 为点亮状态，以0 值表示熄灭状态。

默认情况下LED灯为常亮状态，在/sys/class/leds/work目录下使用以下命令关闭LED灯，如下图所示：

> echo 0 > brightness

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第13章 LED应用编程/8f444d1ecc4f409d41cfc81c6c017748\_MD5.png](assets/第13章%20LED应用编程/8f444d1ecc4f409d41cfc81c6c017748_MD5.png)

命令使用之后可以看到LED灯会熄灭，如果想要打开LED灯,可以使用以下命令向brightness写入一个非零值（这里写入1），如下图所示：

> echo 1 > brightness

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第13章 LED应用编程/9ddea324213f03f6b859cddb5fe636d9\_MD5.png](assets/第13章%20LED应用编程/9ddea324213f03f6b859cddb5fe636d9_MD5.png)

****max\_brightness：**** 该属性文件为只读属性，不能写，用于获取 LED 设备的最大亮度等级。

### 13.3编写LED应用程序

本小节代码在配套资料“ iTOP-3588开发板\\03\_【iTOP-RK3588开发板】指南教程\\03\_系统编程配套程序 \\ 61 ”目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第13章 LED应用编程/bcaf36599ae565013de0e175d0ad56f4\_MD5.png](assets/第13章%20LED应用编程/bcaf36599ae565013de0e175d0ad56f4_MD5.png)

****实验要求：****

通过应用程序来控制LED灯的亮灭。传入的参数为“on”LED亮起，传入参数为“off”LED灯熄灭。

****实验步骤：****

首先进入到 ubuntu 的终端界面输入以下命令来创建 demo61\_ledctrl.c文件，如下图所示：

> vim demo61\_ledctrl.c

```cpp
#include <sys/types.h>

#include <sys/stat.h>

#include <fcntl.h>

#include <stdio.h>

#include <fcntl.h>

#include <unistd.h>

#include <string.h>

 

#define LED_BRIGHTNESS "/sys/class/leds/work/brightness"  // 定义 LED 亮度控制文件路径

int main(int argc, char *argv[])

{

    int fd = open(LED_BRIGHTNESS, O_RDWR); // 打开 LED 亮度控制文件，返回文件描述符

 

     if (fd < 0) // 判断文件是否打开成功

    { 

        printf("brightness file open error\n"); // 打印错误信息

        close(fd); // 关闭文件描述符

        return -1; // 返回错误码

    }

 

    if (!strcmp(argv[1], "on"))  // 如果命令行参数为 "on"

    {

        write(fd, "1", 1); // 将亮度设置为 1

    }

    else if (!strcmp(argv[1], "off")) // 如果命令行参数为 "off"

    { 

        write(fd, "0", 1); // 将亮度设置为 0

    } 

    else // 如果命令行参数不为 "on" 或 "off"

    { 

    printf("Invalid command\n"); // 打印错误信息

        close(fd); // 关闭文件描述符

        return -1; // 返回错误码

    }

close(fd); // 关闭文件描述符

    return 0; // 返回成功码

}
cpp
```

上述代码定义了fd为LED亮灭控制brightness文件的文件描述符，第21 行和第25行为两个字符串判断，如果传入的参数为“on”则向brightness文件写入1，LED亮起，如果传入参数为“off”则向brightness文件写入0，LED灯熄灭。

保存退出之后，使用以下命令设置交叉编译器环境，并对demo61\_ledctrl.c进行交叉编译，编译完成如下图所示：

> export PATH=/usr/local/ [arm64](https://so.csdn.net/so/search?q=arm64&spm=1001.2101.3001.7020) /gcc-arm-10.3-2021.07-x86\_64-aarch64-none-linux-gnu/bin:$PATH
> 
> aarch64-none-linux-gnu-gcc -o demo61\_ledctrl demo61\_ledctrl.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第13章 LED应用编程/7a73181332f8416b98c94b040311f022\_MD5.png](assets/第13章%20LED应用编程/7a73181332f8416b98c94b040311f022_MD5.png)

最后将交叉编译生成的demo61\_ledctrl文件拷贝到/home/nfs共享目录下即可。

### 13.4开发板测试

Buildroot系统启动之后，首先使用以下命令进行nfs共享目录的挂载（ 其中 192.168.1.7 为作者ubuntu的ip地址，需要根据自身ubuntu的ip来设置 ），如下图所示：

mount -t nfs -o nfsvers=3,nolock 192.168.1.7:/home/nfs /mnt

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第13章 LED应用编程/b4aad5c3877a8e546773194a6634e06a\_MD5.png](assets/第13章%20LED应用编程/b4aad5c3877a8e546773194a6634e06a_MD5.png)

nfs共享目录挂载到了开发板的/mnt目录下，进入到/mnt目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第13章 LED应用编程/d260759dcc6ec9bcf32aae19ecdbb60a\_MD5.png](assets/第13章%20LED应用编程/d260759dcc6ec9bcf32aae19ecdbb60a_MD5.png)

可以看到/mnt目录下demo97\_ledctrl文件已经存在了，输入以下命令关闭led灯，如下图所示：

> ./demo61\_ledctrl off

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第13章 LED应用编程/2c2328412ce417ae4e2aa3f2d3f4bda0\_MD5.png](assets/第13章%20LED应用编程/2c2328412ce417ae4e2aa3f2d3f4bda0_MD5.png)

可以看到LED灯熄灭了，然后使用以下命令打开led灯，如下图所示：

> ./demo61\_ledctrl on

命令运行成功之后，可以看到LED灯又被打开了。

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第13章 LED应用编程/5b68bdc1b14fc09dbd74bb553ab1c96b\_MD5.png](assets/第13章%20LED应用编程/5b68bdc1b14fc09dbd74bb553ab1c96b_MD5.png)

至此，LED应用程序在开发板的测试就完成了。

微信公众号

内容来源：csdn.net

作者昵称：北京迅为

原文链接：https://blog.csdn.net/BeiJingXunWei/article/details/138001842

作者主页：https://blog.csdn.net/BeiJingXunWei

实付 元

[使用余额支付](https://blog.csdn.net/BeiJingXunWei/article/details/)

点击重新获取

扫码支付

钱包余额 0

抵扣说明：

1.余额是钱包充值的虚拟货币，按照1:1的比例进行支付金额的抵扣。  
2.余额无法直接购买下载，可以购买VIP、付费专栏及课程。

[余额充值](https://i.csdn.net/#/wallet/balance/recharge)

举报

[AI 搜索](https://ai.csdn.net/?utm_source=cknow_pc_blog_right_hover) [智能体](https://ai.csdn.net/cmd?utm_source=cknow_pc_blog_right_hover) [AI 编程](https://ai.csdn.net/coding?utm_source=cknow_pc_blog_right_hover) [AI 作业助手](https://ai.csdn.net/homework?utm_source=cknow_pc_blog_right_hover)

隐藏侧栏 ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第13章 LED应用编程/90bd0cbf3aff8fdff8bf9b011b581e20\_MD5.png](assets/第13章%20LED应用编程/90bd0cbf3aff8fdff8bf9b011b581e20_MD5.png)

程序员都在用的中文IT技术交流社区

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第13章 LED应用编程/08a47e60886378fe60a3d9c8f4ae8bc6\_MD5.png](assets/第13章%20LED应用编程/08a47e60886378fe60a3d9c8f4ae8bc6_MD5.png)

专业的中文 IT 技术社区，与千万技术人共成长

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第13章 LED应用编程/a51be6c085b867a5bd82d8dc1cea9b46\_MD5.png](assets/第13章%20LED应用编程/a51be6c085b867a5bd82d8dc1cea9b46_MD5.png)

关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！

客服 返回顶部

微信公众号

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第13章 LED应用编程/efb7921311640694e61fee00900550d6\_MD5.jpg](assets/第13章%20LED应用编程/efb7921311640694e61fee00900550d6_MD5.jpg) 公众号名称：迅为电子 微信扫码关注或搜索公众号名称

复制公众号名称

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第13章 LED应用编程/b3fd6785588a0190aebd0a7d6fec18cf\_MD5.png](assets/第13章%20LED应用编程/b3fd6785588a0190aebd0a7d6fec18cf_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第13章 LED应用编程/1e92e3470c7e435ba87243e0eaa05c2b\_MD5.png](assets/第13章%20LED应用编程/1e92e3470c7e435ba87243e0eaa05c2b_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第13章 LED应用编程/918b1066ade08cfd305e482697a95552\_MD5.png](assets/第13章%20LED应用编程/918b1066ade08cfd305e482697a95552_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第13章 LED应用编程/8f444d1ecc4f409d41cfc81c6c017748\_MD5.png](assets/第13章%20LED应用编程/8f444d1ecc4f409d41cfc81c6c017748_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第13章 LED应用编程/9ddea324213f03f6b859cddb5fe636d9\_MD5.png](assets/第13章%20LED应用编程/9ddea324213f03f6b859cddb5fe636d9_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第13章 LED应用编程/bcaf36599ae565013de0e175d0ad56f4\_MD5.png](assets/第13章%20LED应用编程/bcaf36599ae565013de0e175d0ad56f4_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第13章 LED应用编程/7a73181332f8416b98c94b040311f022\_MD5.png](assets/第13章%20LED应用编程/7a73181332f8416b98c94b040311f022_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第13章 LED应用编程/b4aad5c3877a8e546773194a6634e06a\_MD5.png](assets/第13章%20LED应用编程/b4aad5c3877a8e546773194a6634e06a_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第13章 LED应用编程/d260759dcc6ec9bcf32aae19ecdbb60a\_MD5.png](assets/第13章%20LED应用编程/d260759dcc6ec9bcf32aae19ecdbb60a_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第13章 LED应用编程/2c2328412ce417ae4e2aa3f2d3f4bda0\_MD5.png](assets/第13章%20LED应用编程/2c2328412ce417ae4e2aa3f2d3f4bda0_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第13章 LED应用编程/5b68bdc1b14fc09dbd74bb553ab1c96b\_MD5.png](assets/第13章%20LED应用编程/5b68bdc1b14fc09dbd74bb553ab1c96b_MD5.png)