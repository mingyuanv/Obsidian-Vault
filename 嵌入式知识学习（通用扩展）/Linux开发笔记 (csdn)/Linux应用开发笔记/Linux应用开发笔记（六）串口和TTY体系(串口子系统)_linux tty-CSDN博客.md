---
title: "Linux应用开发笔记（六）串口和TTY体系(串口子系统)_linux tty-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/137513476?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读4.9k次，点赞36次，收藏58次。串口是我们在调试中常常需要的一环，它可以帮助我们实时打印信息，其基础知识在之前的学习笔记中已经提到了，感兴趣或者用什么问题可以回顾一下，这部分主要解释Linux下的TTY体系。TTY设备不仅支持UART（通用异步收发传输器）通信，还支持键盘输入、显示器输出以及更复杂的功能，如伪终端。TTY体系在Linux系统中指的是一种终端设备体系，它提供了用户与操作系统之间的交互界面。TTY一词源于Teleprinter（电传打印机），在早期的计算机系统中，TTY是以打字机作为输入输出设备的终端系统。_linux tty"
tags:
  - "clippings"
---
---

## 前言

  串口是我们在调试中常常需要的一环，它可以帮助我们实时打印信息，其基础知识在之前的学习笔记中已经提到了，感兴趣或者用什么问题可以回顾一下，这部分主要解释 Linux 下的 [TTY](https://so.csdn.net/so/search?q=TTY&spm=1001.2101.3001.7020) 体系。TTY设备不仅支持UART（通用异步收发传输器）通信，还支持键盘输入、显示器输出以及更复杂的功能，如伪终端。

## 一、TTY体系

### 1\. 什么是TTY

  TTY体系在 [Linux系统](https://so.csdn.net/so/search?q=Linux%E7%B3%BB%E7%BB%9F&spm=1001.2101.3001.7020) 中指的是一种终端设备体系，它提供了用户与操作系统之间的交互界面。TTY一词源于Teleprinter（电传打印机），在早期的 计算机系统 中，TTY是以打字机作为输入输出设备的终端系统。而在现代的Linux系统中，TTY则对应着虚拟终端。  
  TTY体系主要由多个虚拟终端组成，每个虚拟终端都对应着一个TTY设备文件。这些设备文件位于/dev目录下，以tty开头，后面跟随一个数字，如tty1、tty2等。用户可以通过TTY设备读取输入的字符，并将输出字符发送到TTY设备，这些字符可以是用户输入的命令、系统的输出信息等。  
  在Linux系统中，TTY终端设备主要分为三种类型：串口终端（/dev/ttyS\*）、虚拟终端（/dev/tty\*）和控制台终端（/dev/ console ）。串口终端是使用计算机串口连接的终端设备；虚拟终端则是用户登录时使用的终端，用户可以通过Ctrl+Alt+\[F1-F6\]组合键切换到不同的虚拟终端；控制台终端则包括系统控制台、当前控制台和虚拟控制台。

### 2\. TTY中各设备节点的差别

- 设备类型与用途：  
	**/dev/ttyS0** ：通常代表PC的串口，用于串行通信，连接外部设备如调制解调器或其他串口设备。  
	**/dev/tty** ：表示当前程序所在的终端，可能是虚拟终端，也可能是真实的终端。它代表了一个通用的终端接口，不特定于某个具体的串口或虚拟终端。  
	**/dev/tty0** ：通常表示前台程序的虚拟终端，即用户当前正在操作的界面。  
	**/dev/tty1, /dev/tty2, … /dev/ttyn** ：表示不同的虚拟终端。用户可以在这些虚拟终端之间切换，每个虚拟终端都可以独立运行程序。
- 访问与交互：  
	\-当一个程序在后台运行时，如果它尝试访问/dev/tty0，它实际上是在访问前台程序的终端。这意味着后台程序可以与前台程序的终端进行交互。  
	\-当前程序无论在前台还是后台切换，其自己的/dev/tty都不会改变，这保证了程序与其终端的稳定连接。

### 3.Terminal和Console

  Terminal我们常常指终端，而Console为控制台，这表明他有更大的权限和查看更多的信息，例如内核信息等。从某种角度来说， **console可能是任何一个terminal，但不是所有terminal都是console** 。虽然在日常的使用中我们常常会混淆二者的定义，但Terminal和Console在定义、功能、物理与虚拟特性以及交互方式上存在明显的差别。

- 定义与功能：  
	  Terminal：它是用户与计算机系统交互的界面，特别是图形用户界面（GUI）环境下的模拟终端仿真器。终端仿真器提供了一个命令行界面（CLI），用户可以通过输入命令和参数与操作系统进行交互。常见的终端仿真器包括GNOME Terminal、KDE Konsole、xterm等。终端的本质在于它能接受输入并显示输出，是处理计算机主机输入输出的设备，典型的终端包括显示器键盘套件、打印机打字机套件等。  
	  Console：它通常指的是连接到计算机系统的物理设备，如键盘和显示器。在Linux系统中，控制台提供了一个字符终端界面，用户可以直接在控制台上输入命令和查看输出。控制台在计算机程序中用于输入和输出文本或命令，提供了一个命令行界面或命令行提示符，允许用户通过键盘输入命令，并显示程序的输出结果。
- 物理与虚拟特性：  
	  Terminal：可以是物理的，也可以是虚拟的。物理终端直接连接在主机上，包括显示器、键盘鼠标等。虚拟终端则通过软件模拟实现，例如使用TCP/IP承载的远程终端（如Telnet和SSH）。  
	  Console：通常指的是物理设备，特别是当提及Linux系统的控制台时，它指的是连接到计算机系统的物理键盘和显示器。尽管有些程序可以模拟终端设备的功能，被称为控制台软件，但从本质上讲，控制台更多地与物理设备相关联。
- 交互方式：  
	  Terminal：提供了多种交互方式，包括本地终端和远程终端。本地终端通过VGA、PS/2或USB等接口连接主机和显示器/键盘。远程终端则通过网络连接，如Telnet和SSH，允许用户远程访问和操作计算机系统。  
	  Console：通常是一个文本界面，提供了命令行界面或命令行提示符，用户通过键盘输入命令并与操作系统进行交互。控制台通常以黑色背景和白色或其他亮色的文本显示，以便用户清晰地看到输入和输出。  
	在实际使用中，我们可以使用：Console=/dev/XXX (XXX指前面提到了各个设备节点)来指定哪一个终端作为本次的控制台从而获得更高权限，此外若存在多个Console的值，会自动取最后一次的赋值。

## 二、TTY驱动框架

  Linux tty子系统包含通常包含tty核心、tty行规程和tty驱动。  
① **tty核心** 是对整个tty设备的抽象，对用户提供统一的接口。  
② **tty行规程** 用于处理控制字符、回显输入数据、缓存输入数据、显示数据输出等。行规程可以根据应用层的需求进行设置，如果应用层不需要这些处理机制，可以将其设置为原始模式。  
③ **tty驱动** 则是面向tty设备的硬件驱动。  
  在TTY驱动框架中，数据的传输过程是一个涉及多个层次和 组件 的复杂过程。首先，我们假设一个应用程序需要与串口设备进行通信。那么他的处理流程大体如下所示：  
**打开设备文件** ：应用程序首先通过系统调用（如open）打开与串口设备对应的设备文件，例如/dev/ttyS0（对于第一个串口设备）。这个操作会触发TTY驱动框架的相应处理，将应用程序与特定的TTY设备关联起来。  
**配置串口参数** ：接下来，应用程序可能会调用如termios或类似的API来配置串口的参数，如波特率、数据位、停止位和校验位等。这些配置参数会传递给TTY驱动框架，以确保数据的正确传输。  
**发送数据** ：一旦串口配置完成，应用程序就可以通过write系统调用向串口发送数据。这些数据首先被写入到TTY驱动框架的发送缓冲区中。然后，TTY驱动框架会按照配置好的串口参数，将数据格式化 并发 送到实际的串口硬件。在发送过程中，TTY驱动框架会处理如奇偶校验、停止位等细节。  
**接收数据** ：当串口接收到数据时，TTY驱动框架会读取这些数据，并将其放入接收缓冲区中。然后，它会检查数据的完整性（例如，是否包含正确的奇偶校验位）。如果数据完整无误，TTY驱动框架会通过中断或其他机制通知应用程序有数据可读。应用程序随后可以通过read系统调用从接收缓冲区中读取数据。  
**错误处理** ：在整个传输过程中，TTY驱动框架还会处理可能出现的错误情况，如串口通信中断、硬件故障等。当发生错误时，TTY驱动框架会采取相应的措施，如通知应用程序、重试发送或关闭串口等。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/fd7962081f137a6493c26528cc7cacb2.png)  
  我们可以看出信息流的方向，是一个纵向的通路，一端是计算机程序，另一端是某种硬件。以打印一个字符“A”为例，从keyboard输入，tty的驱动层收到的数据通过 tty 驱动向上回流，先进入 tty 行规程，当检测到这是一个普通的字符时，直接返回到驱动层从而下发到指定的tty硬件设备上进行回显。如果将行规程设置为原始模式，则回在进过行规程判别后再进入tty核心， 最后被用户获取。

## 三、串口调试

  本次实验依旧是基于泰山派(RK3566)，其引脚分布如下图所示：  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ea98369704fb6ac02d1174c5e2390ba3.png)  
  测试串口我们需要一个串口调试工具，我这里借用的是32开发板的串口模块CH340，当然也可以直接接这样一个模块。通过上面的 引脚定义 中我们可以知道用户GPIO中的8、9脚对应UART3，这里我们通过杜邦线把UART3\_TX\_M1连接到CH340的RXD引脚，UART3\_RX\_M1连接到CH340的TXD引脚，并且进行共地，连接如下表所示。

| GPIO | 引脚功能 | CH340 |
| --- | --- | --- |
| GPIO3\_B7 | UART3\_TX | RXD |
| GPIO3\_C0 | UART3\_RX | TXD |
| GND |  | GND |

  其调试流程大致如下：

```c
//无权限请使用sudo进入root权限
stty -F /dev/ttyS3
12
```

  之后会显示串口信息，包括波特率等。

```c
//更改波特率 ispeed：输入波特率  ospeed：输出波特率
stty -F /dev/ttyS3 ispeed 115200 ospeed 115200
12
```

  进行串口输出。

```c
//向串口3输出hello
echo "hello" > /dev/ttyS3
12
```

  这里作者全程是在root用户下进行的，如果无法执行可以先赋权限

```c
sudo chmod 777 /dev/ttyS3
1
```

## 四、驱动编写

  在结束前面的准备工作之后，我们就要开始进行最喜闻乐见的环节了。对于 [uart](https://so.csdn.net/so/search?q=uart&spm=1001.2101.3001.7020) 编程来说，大体分为三个部分：open→设置行规程→write/read。  
  首先我们需要了解一下termios，它包含uart所需要的一些基本参数:

```c
//注：这里参数的取值可选项有很多，笔者不在这里赘述了，如果大家感兴趣的可以去自行查阅
struct termios {
    tcflag_t c_iflag;        /* 输入模式标志位 */
    tcflag_t c_oflag;        /* 输出模式标志位 */
    tcflag_t c_cflag;        /* 控制模式标志位 */
    tcflag_t c_lflag;        /* 本地模式标志位 */
    cc_t c_cc[NCCS];        /* 控制字符数组 */
    cc_t c_line;            /* 线路规程 */
    speed_t c_ispeed;        /* 输入波特率 */
    speed_t c_ospeed;        /* 输出波特率 */
};
1234567891011
```

  接下来我们进行实际操作，先打开串口：

```c
int open_port(char *com)
{
    int fd;
    //O_NOCTTY -------- 打开的串口不作为控制终端
    fd = open(com, O_RDWR|O_NOCTTY);
    if (-1 == fd){
        return(-1);
    }
    
      if(fcntl(fd, F_SETFL, 0)<0) /* 设置串口为阻塞状态*/
      {
            printf("fcntl failed!\n");
            return -1;
      }
  
      return fd;
}
1234567891011121314151617
```

  在打开串口之后，我们常常使用tcgetattr( ) 函数 得到当前串口的参数，以此来检测到是否链接成功。

```c
#include <termios.h>
#include <unistd.h>
//检测当前串口参数，并保存在第二个参数中，通常获取串口需要对原始信息进行备份，在程序退出前需要修改回来
int tcgetattr(int fd, struct termios *termios_p);
1234
```

  此外，我们还需要一个tcsetattr( )函数用来设置终端参数

```c
#include <termios.h>
#include <unistd.h>
//设置终端参数
int tcgetattr(int fd, int optional_actions, const struct termios *termios_p);
1234
```
- 参数
	- int fd: 要设置属性的文件描述符
	- int optional\_actions: 设置属性时，可以控制属性生效的时刻，optional\_actions可以取下面几个值：
		- TCSANOW: 立即生效
		- TCADRAIN: 改变在所有写入fd 的输出参数都被传输后生效，这个函数应当用于修改影响输出的参数时使用
		- TCSAFLUSH ：改变在所有写入fd 引用的对象的输出都被传输后生效，所有已接受但未读入的输入都在改变发生前丢弃(同 TCSADRAIN，但会舍弃当前所有值)
	- \*termios termios\_p: 用来设置的串口属性的结构体指针,对串口的termios配置好后，传入函数即可。
- 返回值：成功返回0，失败返回-1。

  这里也可以使用ioctl系统调用来代替tcgetattr( )和tcsetattr( )，其原型为：

```c
#include <sys/ioctl.h>
//向设备文件发送命令，控制一些特殊操作
int ioctl(int fd, unsigned long request, ...);
123
```
- 参数：
	- fd：与write、read类似，fd文件句柄指定要操作哪个文件。
	- reques：操作请求的编码，它是跟硬件设备驱动相关的，不同驱动设备支持不同的编码， 驱动程序通常会使用头文件提供可用的编码给上层用户。

| 名称 | 功能 |
| --- | --- |
| FIONBIO | 设置文件描述符（如套接字）为非阻塞模式 |
| TCGETS | 获取当前设置 |
| TCSETS | 设置新的配置 |
| SIOCGIFADDR | 获取接口地址 |
| SIOCSIFADDR | 设置接口地址 |

- “…”：这是一个没有定义类型的指针，它与printf函数定义中的“…”类似， 不过ioctl此处只能传一个参数。部分驱动程序执行操作请求时可能需要配置参数， 或者操作完成时需要返回数据，都是通过此处传的指针进行访问的。
- 返回值：0：成功；-1：错误

  接下来就就是完整的端口设置（初始化）程序了：

```c
int set_opt(int fd,int nSpeed, int nBits, char nEvent, int nStop)
{
    struct termios newtio,oldtio;
    //if(ioctl(fd,TCGETS, &oldtio) !=0)
    if ( tcgetattr( fd,&oldtio) != 0) { 
        perror("SetupSerial 1");
        return -1;
    }
    
    bzero( &newtio, sizeof( newtio ) );
    newtio.c_cflag |= CLOCAL | CREAD; 
    newtio.c_cflag &= ~CSIZE; 

    newtio.c_lflag  &= ~(ICANON | ECHO | ECHOE | ISIG);  /*Input*/
    newtio.c_oflag  &= ~OPOST;   /*Output*/
    //选择传输位数
    switch( nBits )
    {
    case 7:
        newtio.c_cflag |= CS7;
    break;
    case 8:
        newtio.c_cflag |= CS8;
    break;
    }
    //选择校验位
    switch( nEvent )
    {
    case 'O':
        newtio.c_cflag |= PARENB;
        newtio.c_cflag |= PARODD;
        newtio.c_iflag |= (INPCK | ISTRIP);
    break;
    case 'E': 
        newtio.c_iflag |= (INPCK | ISTRIP);
        newtio.c_cflag |= PARENB;
        newtio.c_cflag &= ~PARODD;
    break;
    case 'N': 
        newtio.c_cflag &= ~PARENB;
    break;
    }
    //选择传输速率
    switch( nSpeed )
    {
    case 2400:
        cfsetispeed(&newtio, B2400);
        cfsetospeed(&newtio, B2400);
    break;
    case 4800:
        cfsetispeed(&newtio, B4800);
        cfsetospeed(&newtio, B4800);
    break;
    case 9600:
        cfsetispeed(&newtio, B9600);
        cfsetospeed(&newtio, B9600);
    break;
    case 115200:
        cfsetispeed(&newtio, B115200);
        cfsetospeed(&newtio, B115200);
    break;
    default:
        cfsetispeed(&newtio, B9600);
        cfsetospeed(&newtio, B9600);
    break;
    }
    //选择停止位
    if( nStop == 1 )
        newtio.c_cflag &= ~CSTOPB;
    else if ( nStop == 2 )
        newtio.c_cflag |= CSTOPB;
    //设置等待时间
    newtio.c_cc[VMIN]  = 1;  // 读数据时的最小字节数: 没读到这些数据我就不返回!
    newtio.c_cc[VTIME] = 0;  // 等待第1个数据的时间
    //设置阻塞模式
    tcflush(fd,TCIFLUSH);
    //使能配置生效
    //if(ioctl(fd,TCSETS, &newtio) !=0)
    if((tcsetattr(fd,TCSANOW,&newtio))!=0)
    {
        perror("com set error");
        return -1;
    }
    return 0;
}
12345678910111213141516171819202122232425262728293031323334353637383940414243444546474849505152535455565758596061626364656667686970717273747576777879808182838485
```

**注：本文部分参考了野火、韦东山和网上的公开资料，这里感谢各位的分享，若有侵权请联系笔者。**

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/137513476

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