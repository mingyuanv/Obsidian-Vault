

[SDIO接口WiFi驱动浅析\_有没有用stm32的sdio驱动sdio接口wifi的例子?-CSDN博客](https://blog.csdn.net/qq_38880380/article/details/79900784)

    SDIO-Wifi模块是基于SDIO接口的符合wifi无线网络标准的嵌入式模块，内置无线网络协议IEEE802.11协议栈以及TCP/IP协议栈，能够实现用户主平台数据通过SDIO口到无线网络之间的转换。SDIO具有传输数据快，兼容SD、MMC接口等特点。

     对于SDIO接口的wifi，首先，它是一个sdio的卡的设备，然后具备了wifi的功能，所以，注册的时候还是先以sdio的卡的设备去注册的。然后检测到卡之后就要驱动他的wifi功能了，显然，他是用sdio的协议，通过发命令和数据来控制的。下面先简单回顾一下SDIO的相关知识：

<span style="background:#affad1">首先，它是一个sdio的卡的设备，然后具备了wifi的功能，所以，注册的时候还是先以sdio的卡的设备去注册的</span>

<span style="background:#affad1">他是用sdio的协议，通过发命令和数据来控制的</span>

# 一、SDIO相关基础知识解析

## 1、SDIO接口

       SDIO 故名思义，就是 SD 的 I/O 接口（interface）的意思，不过这样解释可能还有点抽像。更具体的说明，SD 本来是记忆卡的标准，但是现在也可以把 SD 拿来插上一些外围接口使用，这样的技术便是 SDIO。

       所以 SDIO 本身是一种相当单纯的技术，透过 SD 的 I/O 接脚来连接外部外围，并且透过 SD 上的 I/O 数据接位与这些外围传输数据，而且 SD 协会会员也推出很完整的 SDIO stack 驱动程序，使得 SDIO 外围（我们称为SDIO 卡）的开发与应用变得相当热门。

       现在已经有非常多的手机或是手持装置都支持 SDIO 的功能（SD 标准原本就是针对 mobile device 而制定），而且许多 SDIO 外围也都被开发出来，让手机外接外围更加容易，并且开发上更有弹性（不需要内建外围）。目前常见的 SDIO 外围（SDIO 卡）有：

· Wi-Fi card（无线网络卡） 

· CMOS sensor card（照相模块） 

· GPS card 

· GSM/GPRS modem card 

· Bluetooth card 

        SDIO 的应用将是未来嵌入式系统最重要的接口技术之一，并且也会取代目前 GPIO 式的 SPI 接口。

## 2、SDIO总线

      SDIO总线 和 USB总线 类似，SDIO也有两端，其中一端是HOST端，另一端是device端。所有的通信都是由HOST端 发送 命令 开始的，Device端只要能解析命令，就可以相互通信。

<span style="background:#affad1">SDIO也有两端，其中一端是HOST端，另一端是device端。所有的通信都是由HOST端 发送 命令 开始的，Device端只要能解析命令</span>


<span style="background:#b1ffff">CLK信号</span>:<span style="background:#d3f8b6">HOST给DEVICE的 时钟信号</span>，每个时钟周期传输一个命令。

<span style="background:#b1ffff">CMD</span>信号：<span style="background:#d3f8b6">双向 的信号，用于传送 命令 和 反应</span>。

<span style="background:#b1ffff">DAT0-DAT3 </span>信号:四条用于传送的数据线。

<span style="background:#d3f8b6">VDD信号:电源信号。</span>

VSS1，VSS2:电源地信号。


## 3、SDIO热插拔原理

方法：设置一个 定时器检查 或 插拔中断检测

硬件：假如GPG10（EINT18）用于SD卡检测

GPG10 为高电平 即没有插入SD卡

GPG10为低电平  即插入了SD卡


## 4、SDIO命令

      SDIO总线上都是HOST端发起请求，然后DEVICE端回应请求。sdio命令由6个字节组成。

a --<span style="background:#affad1"> Command:用于开始传输的命令，是由HOST端发往DEVICE端的。其中命令是通过CMD信号线传送的。</span>

b -- Response:回应是DEVICE返回的HOST的命令，作为Command的回应。也是通过CMD线传送的。

c -- Data:数据是双向的传送的。可以设置为1线模式，也可以设置为4线模式。数据是通过DAT0-DAT3信号线传输的。

      SDIO的每次操作都是由HOST在CMD线上发起一个CMD，对于有的CMD，DEVICE需要返回Response，有的则不需要。

     对于读命令，首先HOST会向DEVICE发送命令，紧接着DEVICE会返回一个握手信号，此时，当HOST收到回应的握手信号后，会将数据放在4位的数据线上，在传送数据的同时会跟随着CRC校验码。当整个读传送完毕后，HOST会再次发送一个命令，通知DEVICE操作完毕，DEVICE同时会返回一个响应。

    对于写命令，首先HOST会向DEVICE发送命令，紧接着DEVICE会返回一个握手信号，此时，当HOST收到回应的握手信号后，会将数据放在4位的数据线上，在传送数据的同时会跟随着CRC校验码。当整个写传送完毕后，HOST会再次发送一个命令，通知DEVICE操作完毕，DEVICE同时会返回一个响应。


# 二、SDIO接口驱动

        前面讲到，SDIO接口的wifi，首先，它是一个sdio的卡的设备，然后具备了wifi的功能，所以SDIO接口的WiFi驱动就是在wifi驱动外面套上了一个SDIO驱动的外壳，SDIO驱动仍然符合设备驱动的分层与分离思想：

  

<font color="#ff0000"><span style="background:rgba(140, 140, 140, 0.12)"><font color="#ff0000">     设备驱动层（wifi 设备）</font></span></font>

<font color="#ff0000"><span style="background:rgba(140, 140, 140, 0.12)"><font color="#ff0000">                      |</font></span></font>

<font color="#ff0000"><span style="background:rgba(140, 140, 140, 0.12)"><font color="#ff0000">核心层（向上向下提供接口）</font></span></font>

<font color="#ff0000"><span style="background:rgba(140, 140, 140, 0.12)"><font color="#ff0000">                      |</font></span></font>

<font color="#ff0000"><span style="background:rgba(140, 140, 140, 0.12)"><font color="#ff0000">主机驱动层 （实现SDIO驱动）</font></span></font>

  

        下面先分析SDIO接口驱动的实现，看几个重要的数据结构（用于核心层与主机驱动层 的数据交换处理）。

<span style="background:#b1ffff">核心层与主机驱动层 的数据交换处理</span>

[ /include/linux/mmc/host.h ]

<span style="background:#d3f8b6">struct mmc_host     用来描述卡控制器</span>

<span style="background:#d3f8b6">struct mmc_card     用来描述卡</span>

<span style="background:#d3f8b6">struct mmc_driver  用来描述 mmc 卡驱动</span>

<span style="background:#d3f8b6">struct sdio_func      用来描述 功能设备</span>

struct mmc_host_ops   用来描述卡控制器操作接口函数功能，用于从 主机控制器层向 core 层注册操作函数，从而将core 层与具体的主机控制器隔离。也就是说 core 要操作主机控制器，就用这个 ops 当中给的函数指针操作，不能直接调用具体主控制器的函数。

      HOST层驱动分析在 前面的系列文章中 [Linux SD卡驱动开发(二) —— SD 卡驱动分析HOST篇](http://blog.csdn.net/zqixiao_09/article/details/51039595) 有详细阐述，下面只简单回顾一下一些重要函数处理
[Linux SD卡驱动开发(二) —— SD 卡驱动分析HOST篇-CSDN博客](https://blog.csdn.net/zqixiao_09/article/details/51039595)


？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？

# 三、wifi 驱动部分解析

wifi驱动的通用的软件架构

1. 分为两部分，上面为<span style="background:#d3f8b6">主机驱动，下面是我们之前所说的firmware</span>

2. 其中固件部分的主要工作是：因为天线接受和发送回来的都是802.11帧的帧，而主机接受和传送出来的数据都必须是802.3的帧，所以必须由firmware来负责802.3的帧和802.11帧之间的转换

3. <span style="background:#d3f8b6">当天线收到数据，并被firmware处理好后会放在一个buffer里，并产生一个中断，主机在收到中断后就去读这个buffer。  </span>

 SDIO<span style="background:#affad1">设备的驱动由sdio_driver结构体定义，sdio_driver其实是driver的封装。通过sdio_register_driver函数将SDIO设备驱动加载进内核，其实就是挂载到sdio_bus_type总线上去</span>


1、设备驱动的注册



























