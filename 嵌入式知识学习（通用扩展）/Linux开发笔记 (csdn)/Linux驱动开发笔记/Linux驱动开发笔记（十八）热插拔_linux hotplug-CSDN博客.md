---
title: "Linux驱动开发笔记（十八）热插拔_linux hotplug-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/140327063?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读1.5k次，点赞20次，收藏28次。前面已经学习了很多外设，但是这些设备都存在一个问题，无法在运行的过程中自动检测设备的插入或移除，所以这里引入了热插拔的概念。在Linux操作系统中，热插拔（Hot Plug）指的是在不关闭系统电源的情况下，动态地插入或移除硬件设备的能力。这对于服务器和其他需要高可用性的系统非常重要，因为它允许在运行时更换或添加设备而不影响系统的正常运行。热插拔机制有很多，目前来说一般是在嵌入式设备上使用mdev，在x86上使用udev，当然也可以在嵌入式设备上使用udev。_linux hotplug"
tags:
  - "clippings"
---
---

## 前言

  前面已经学习了很多外设，但是这些设备都存在一个问题，无法在运行的过程中自动检测设备的插入或移除，所以这里引入了热插拔的概念。

---

## 一、热插拔

### 1.1 定义

  在 Linux 操作系统中，热插拔（Hot Plug）指的是在不关闭系统电源的情况下，动态地插入或移除硬件设备的能力。这对于 [服务器](https://so.csdn.net/so/search?q=%E6%9C%8D%E5%8A%A1%E5%99%A8&spm=1001.2101.3001.7020) 和其他需要 高可用性 的系统非常重要，因为它允许在运行时更换或添加设备而不影响系统的正常运行。  
  热插拔机制有很多，目前来说一般是在嵌入式设备上使用mdev，在x86上使用udev，当然也可以在嵌入式设备上使用udev。udev是基于netlink机制实现的，通过监听内核发生的uevent来执行相应的热插拔操作；mdev是基于uevent\_helper机制，内核产生的uevent会调用uevent\_helper所指的用户程序的medv来执行热插拔操作。

### 1.2 事件的传递机制

  当系统内核发现系统中添加或者删除了某个新的设备时，内核检测到后会产生一个hotplug event并查找/proc/sys/ kernel /hotplug去找出管理设备连接的用户空间程序。若udev已经启动，内核会通知udev去检测sysfs中关于这个新设备的信息并创建设备节点。udev就会去执行udevd，以便让udevd可以产生或者删除硬件的设备文件。 接着udevd会通过libsysfs读取sys文件系统，以便取得该硬件设备的信息(如/dev/vcs，在/sys/class/tty/vcs/dev存放的是”7:0”，既/dev/vcs的主次设备号)；然后再向namedev查询该外部设备的设备文件信息，例如文件的名称、权限等。最后，udevd就依据上述的结果，在/dev/目录中自动建立该外部设备的设备文件，同时在/etc/udev/rules.d下检查有无针对该设备的使用权限。  
  当设备插入或移除时，hotplug机制会让内核会通过netlink socket 通讯(内核调用kobject\_uevent 函数 发送netlink message给用户空间，该功能由内核的统一设备模型里的子系统这一层实现)向用户传递一个事件的发生，Udevd通过标准的socket机制，创建socket连接来获取内核广播的uevent事件 并解析这些uevent事件。  
  运行udevd以后，使用udev trigger的时候，会把内核中已存在的设备的节点创建出来，其具体过程为：udevtrigger通过向/sysfs 文件系统下现有设备的uevent节点写"add"字符串，从而触发uevent事件，使得udevd能够接收到这些事件，并创建buildin的设备驱动的设备节点连同任何已insmod的模块的设备节点。  
  部分重点概念如下：

1. 内核事件的生成：当硬件设备状态发生变化（如插入或移除设备）时，内核生成一个kobject事件。这个事件会通过netlink套接字传递到用户空间。
2. netlink套接字：netlink是一种特殊的套接字类型，用于内核和用户空间之间的通信。kobject事件通过netlink套接字发送到用户空间的udevd守护进程。
3. udev守护进程：udevd是一个用户空间的守护进程，负责接收内核发送的设备事件。udevd监听netlink套接字，获取设备事件并执行相应的操作。
4. udev规则：udevd根据预定义的udev规则文件（通常位于/etc/udev/rules.d/）来决定如何处理这些事件。规则文件中定义了不同设备类型的匹配条件和相应的操作。
5. 执行操作：根据匹配的规则，udevd可以执行一系列操作，例如创建或删除设备节点、设置设备权限、挂载文件系统、启动或停止服务等。

## 二、udev的实现

### 2.1 相关API函数

**kobject\_uevent 函数**

```c
//发送一个uevent
int kobject_uevent(struct kobject *kobj, enum kobject_action action)
{
    return kobject_uevent_env(kobj, action, NULL);
}
12345
```
- 参数
	- kobj：发生动作的kobject
	- action：发生的动作
- 返回值
	- 成功：0
	- 失败：非0

| 名称 | 含义 | 应用 |
| --- | --- | --- |
| KOBJ\_ADD | 表示设备被添加到系统中 | 当新的硬件设备（例如 USB 设备）插入系统时，驱动程序会触发 KOBJ\_ADD 事件 |
| KOBJ\_REMOVE | 表示设备被从系统中移除 | 当硬件设备（例如 USB 设备）从系统中拔出时，驱动程序会触发 KOBJ\_REMOVE 事件 |
| KOBJ\_CHANGE | 表示设备的某些属性发生了变化 | 当设备的配置或状态发生变化时（例如网卡的 IP 地址变化），驱动程序会触发 KOBJ\_CHANGE 事件 |
| KOBJ\_MOVE | 表示设备被移动到另一个位置 | 在某些设备管理操作中，设备可能被移动到系统中的不同位置 |
| KOBJ\_ONLINE | 表示设备已经上线，准备好使用 | 当热插拔的 CPU 或内存被启用并准备好使用时 |
| KOBJ\_OFFLINE | 表示设备已经下线，不再可用 | 当热插拔的 CPU 或内存被禁用时 |

**add\_uevent\_var函数**  
  add\_uevent\_var 是一个用于向 uevent 环境中添加环境变量的内核函数。在处理 uevent 的回调函数中，你可以使用这个函数来添加标准或自定义的环境变量。

```c
int add_uevent_var(struct kobj_uevent_env *env, const char *format, ...);
12
```
- 参数
	- env：指向 kobj\_uevent\_env 结构的指针，这个结构表示 uevent 的环境。
	- format：格式化字符串，用于指定要添加的环境变量及其值，类似于 printf 的格式化字符串。
	- …：可变参数，根据 format 字符串提供的值。
- 返回值
	- 成功：0
	- 失败：负值，通常是因为环境变量列表已满或者内存分配失败。

### 2.2 kset\_uevent\_ops

  kset\_uevent\_ops 是 Linux 内核中用于定义处理由 kobjects 生成的 uevents（用户空间事件）的一组操作的 结构体 。 Kobjects 是表示内核实体的内核对象，并在内核的设备模型中使用。kset\_uevent\_ops 结构允许您指定自定义函数，当与特定 kset 关联的 kobjects 生成 uevents 时，将调用这些函数。一个 kset 是一组 kobjects，而 kset\_uevent\_ops 结构提供了处理在该集合中添加、移除或更改 kobjects 等事件的钩子。

```c
struct kset_uevent_ops {
    int (* const filter)(struct kset *kset, struct kobject *kobj);
    const char *(* const name)(struct kset *kset, struct kobject *kobj);
    int (* const uevent)(struct kset *kset, struct kobject *kobj, struct kobj_uevent_env *env);
};
12345
```
- filter：用于过滤 kobjects，决定是否为特定的 kobject 生成 uevent。如果返回值为 0，则不生成 uevent；否则生成 uevent。
- name：返回 kobject 的名称字符串，用于生成 uevent 的名称部分。
- uevent：当为 kobject 生成 uevent 时调用，允许在生成的 uevent 环境中添加自定义环境变量或修改 uevent 的其他属性。返回值决定操作是否成功。常见的 uevent 环境变量：
	- ACTION：描述事件的类型，例如 “add”（添加），“remove”（移除），“change”（更改）等。
	- DEVPATH：设备路径，相对于 /sys 文件系统的路径，表示发生事件的设备的位置。
	- SUBSYSTEM：表示生成事件的子系统，例如 “block”（块设备），“net”（网络设备）等。
	- SEQNUM：事件的序列号，用于标识事件的顺序。
	- DEVNAME：设备名称，通常用于表示设备的节点名称，例如 “sda”。
	- DEVTYPE：设备类型，描述设备的类型，例如 “disk”（磁盘），“partition”（分区）等。
	- MAJOR：设备的主设备号。
	- MINOR：设备的次设备号.

### 2.3 netlink

  netlink 是 Linux 内核与用户空间进程之间进行通信的机制之一。它广泛用于网络子系统，但也可用于其他内核子系统。Netlink 提供了一种 双向通信 机制，可以从用户空间向内核发送消息，并从内核接收消息。netlink是基于socket套接字的，所以可以在应用层使用socket接口。以下是一些基本概念：

- Netlink 套接字：用于通信的套接字，类似于传统的网络套接字。
- Netlink 消息：在套接字上传输的数据，包含头部和有效载荷。
- Netlink 协议：Netlink 支持多种协议，例如 NETLINK\_ROUTE（路由和邻居表）和 NETLINK\_GENERIC（通用接口）。

  在用户空间程序中使用 Netlink 的基本步骤如下（本质上是创建socket套接字，这部分内容在应用层的代码上已经讲述过了 [socket详解](https://blog.csdn.net/sincerelover/article/details/137271995) ）：

1. 创建 socket 套接字
2. 绑定 socket 套接字  
	  值得注意的是，在网络编程中，不同的协议族使用不同的地址结构体。对于 Netlink 套接字，我们使用 struct sockaddr\_nl，而不是 struct sockaddr\_in。这是因为 struct sockaddr\_in 是专门为 Internet 协议（IPv4）设计的，而 struct sockaddr\_nl 是为 Netlink 设计的，以下是二者的结构体原型。
```c
//绑定到一个 IP 地址和端口，用于网络通信。
struct sockaddr_in {
    short int sin_family;            // 地址族 (AF_INET)
    unsigned short int sin_port;  // 端口号
    struct in_addr sin_addr;        // IP 地址
    unsigned char sin_zero[8];    // 填充字段
};

//绑定到一个 Netlink 地址，用于内核和用户空间进程之间的消息传递。
struct sockaddr_nl {
    sa_family_t nl_family;          // 地址族 (AF_NETLINK)
    unsigned short nl_pad;          // 填充字段 (一般不使用)
    pid_t nl_pid;                  // 进程 ID
    __u32 nl_groups;              // 多播组位掩码，设置为1时表示用户空间只接受内核事件的基本组的内核事件
};
123456789101112131415
```
1. 接收和处理 Netlink 响应
2. 关闭 Netlink 套接字

## 三、mdev的实现

### 3.1 相关API函数

**call\_usermodehelper\_exec函数**  
  call\_usermodehelper\_exec 是 Linux 内核中的一个函数，通常用于 **从内核中执行用户空间的程序或脚本** ，例如处理热插拔事件或在内核模块加载时执行初始化脚本。 **这个函数不需要我们手动调用，这里简单了解即可。**

```c
//
int call_usermodehelper_exec(struct subprocess_info *info, int wait);
12
```
- 参数
	- info：一个指向 subprocess\_info 结构体的指针，包含需要执行的用户空间程序的信息。
	- wait：等待模式，可以是以下值之一：
		- UMH\_NO\_WAIT：不等待用户空间程序完成，立即返回。
		- UMH\_WAIT\_EXEC：等待用户空间程序启动，但不等待其完成。
		- UMH\_WAIT\_PROC：等待用户空间程序完成执行。
- 返回值
	- 成功时，返回 0。
	- 失败时，返回负的错误代码。

**dup2函数**  
  在实际的使用过程中，我们并 **不能在用户层中直接打印信息** ，此时就需要使用到dup2 函数来复制文件描述符的一个系统调用。 **它将一个文件描述符复制到另一个文件描述符** ，并自动关闭目标文件描述符（如果它已经打开）。这种操作在重定向标准输入、输出和错误流时非常有用。

```c
//重定向标准输入、输出
int dup2(int oldfd, int newfd);
12
```
- 参数
	- oldfd: 现有的文件描述符，它将被复制。
	- newfd: 目标文件描述符。dup2 将 oldfd 复制到 newfd，如果 newfd 已经打开，它将首先被关闭。
- 返回值
	- 成功时，返回新的文件描述符，即 newfd。
	- 失败时，返回 -1，并设置 errno 以指示错误。

### 3.2 实现流程

  mdev 是一个轻量级的设备管理工具，通常用于嵌入式 Linux 系统中，作为 udev 的替代方案。mdev 可以自动创建和删除 /dev 目录中的设备节点，并且支持加载设备驱动程序。以下是实现 mdev 的基本过程:

1. 配置 mdev： [参考资料](https://blog.csdn.net/BeiJingXunWei/article/details/135527770)
2. 在启动时启用 mdev： `echo /sbin/mdev > /proc/sys/kernel/hotplug`
3. 重定向标准输入、输出
```c
//示例
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>

int main() {
    int fd;
    fd = open("output.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd < 0) {
        perror("open");
        return 1;
    }

    // 使用 dup2 将标准输出重定向到文件
    if (dup2(fd, STDOUT_FILENO) < 0) {
        perror("dup2");
        close(fd);
        return 1;
    }

    // 现在标准输出将被重定向到文件 output.txt
    printf("This will be written to the file.\n");

    // 关闭文件描述符
    close(fd);
    return 0;
}
123456789101112131415161718192021222324252627
```

---

**免责声明：本实验基于网络上的公开资料若有侵权请联系作者删除。**

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/140327063

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