---
title: "{{title}}"
aliases: 
tags: 
description: 
source:
---

# 备注(声明)：


# 参考文章：

```cardlink
url: https://blog.csdn.net/BeiJingXunWei/article/details/135525790?spm=1001.2101.3001.10796
title: "RK3568驱动指南｜第十篇 热插拔-第116章netlink监听广播信息实验_netlink rk-CSDN博客"
description: "文章浏览阅读1.3k次，点赞18次，收藏25次。套接字类型指定了套接字的数据传输方式，常用的套接字类型包括SOCK_STREAM、SOCK_DGRAM、SOCK_RAW等。协议类型指定了套接字所使用的具体协议类型，常用的协议类型包括IPPROTO_TCP、IPPROTO_UDP、IPPROTO_ICMP等。协议族指定了套接字所使用的协议类型，常用的协议族包括AF_INET、AF_INET6、AF_UNIX等。其中，domain参数指定了套接字的协议族，type参数指定了套接字的类型，protocol参数指定了套接字所使用的具体协议。_netlink rk"
host: blog.csdn.net
```




# 一、netlink机制介绍

## netlink机制介绍
### 1 、用于内核和用户空间之间进行双工通信的机制(❤️)


### 2 、基于socket通信机制，并提供了一种可靠的、异步的、多播的、有序的通信方式。(❤️)


### 3 、Netlink机制的主要特点包括：
> （1）双工通信：Netlink允许内核和用户空间之间进行**双向通信**，使得内核可以向用户空间发送消息，同时也可以接收来自用户空间的消息。
> 
> （2）可靠性：Netlink提供了**可靠**的消息传递机制，保证消息的完整性和可靠性。它使用了确认和重传机制，以确保消息的可靠传输。
> 
> （3）异步通信：Netlink支持**异步通信**，即内核和用户空间可以独立地发送和接收消息，无需同步等待对方的响应。
> 
> （4）多播支持：Netlink允许向多个进程或套接字广播消息，以实现**一对多**的通信。
> 
> （5）有序传输：Netlink保证消息的**有序传输**，即发送的消息按照发送的顺序在接收端按序接收。
> 


### 4 、常见的应用
> （1）系统管理工具：如**ifconfig、ip等工具使用Netlink与内核通信来获取和配置网络接口**的信息。
> 
> （2）进程间通信：**进程可以使用Netlink进行跨进程通信**，实现进程间的数据交换和协调。
> 
> （3）内核模块和用户空间应用程序的通信：**内核模块可以通过Netlink向用户空间应用程序发送通知或接收**用户空间应用程序的指令。



### 5、




# 二、netlink的使用

## 创建socket
### 1 、套接字可以理解为应用程序和网络之间的桥梁(❤️)


### 2 、用于在网络上进行数据的收发和处理


### 3 、该系统调用的原型和所需头文件 如下

|   |   |
|---|---|
|所需头文件|函数原型|
|#include <sys/types.h>          <br><br>#include <sys/socket.h>|int socket**(**int domain**,** int type**,** int protocol**);**|

>` domain参数`指定了**套接字的协议族**，`type参数`指定了套接字的**类型**，`protocol参数`指定了套接字所使用的**具体协议**。


### 4 、协议族(❤️)
- 1 指定套接字通信的域或协议家族，决定了地址格式和通信范围。

|参数宏定义|含义描述|典型应用场景|**本实验设定**|
|---|---|---|---|
|`AF_INET`|IPv4 互联网协议族|传统的 TCP/UDP 网络通信 (如网页浏览)|❌|
|`AF_INET6`|IPv6 互联网协议族|下一代互联网通信|❌|
|`AF_UNIX`|Unix 域协议族|同一台机器上进程间的高效通信 (IPC)|❌|
|**`AF_NETLINK`**|**Netlink 协议族**|**Linux 内核与用户空间进程之间的通信**|**✅ 是**|

> **说明**：本实验涉及监听内核事件，必须使用 `AF_NETLINK`，这是 Linux 特有的用于内核与用户态交互的协议族。


### 5、套接字类型(❤️)
- 1 指定数据传输的方式、连接特性及可靠性。

|参数宏定义|含义描述|典型协议/场景|**本实验设定**|
|---|---|---|---|
|`SOCK_STREAM`|面向连接的流套接字|TCP (可靠传输，保证顺序)|❌|
|`SOCK_DGRAM`|无连接的数据报套接字|UDP (不可靠传输，低延迟)|❌|
|**`SOCK_RAW`**|**原始套接字**|**直接访问底层协议头，无需内核处理**|**✅ 是**|

> **说明**：设置为 `SOCK_RAW` **允许程序直接接收内核发出的原始 Netlink 消息包**，绕过标准的协议栈处理，适用于监听底层内核事件（如 uevent）。



 
### 6、协议类型(❤️)
- 1 在指定的协议族下，进一步细分具体的通信子协议或功能模块。

|参数宏定义|含义描述|典型应用场景|**本实验设定**|
|---|---|---|---|
|`IPPROTO_TCP`|TCP 协议|可靠数据传输 (需配合 AF_INET)|❌|
|`IPPROTO_UDP`|UDP 协议|快速数据传输 (需配合 AF_INET)|❌|
|`IPPROTO_ICMP`|ICMP 协议|网络诊断 (如 Ping 命令)|❌|
|`NETLINK_ROUTE`|路由与接口管理|监控网卡状态、路由表变化 (ip 命令底层)|❌|
|**`NETLINK_KOBJECT_UEVENT`**|**内核对象事件通知**|**接收设备热插拔、驱动加载等 uevent 事件**|**✅ 是**|

> **说明**：`NETLINK_KOBJECT_UEVENT` 是专门用于接收内核对象（kobject）状态变更（如 USB 插入、设备移除）的协议通道，是 `udev` 等设备管理工具的核心基础。


### 7、使用以下代码创建一个新的套接字：
```c
int socket_fd = socket(AF_NETLINK, SOCK_RAW, NETLINK_KOBJECT_UEVENT);
```

> AF_NETLINK：指定了使用Netlink协议族。Netlink协议族是一种Linux特定的协议族，用于内核和用户空间之间的通信。
> 
> SOCK_RAW：指定了创建原始套接字，这种套接字类型可以直接访问底层协议，而不需要进行协议栈处理。在这种情况下，我们可以直接使用Netlink协议进行通信。
> 
> NETLINK_KOBJECT_UEVENT：指定了Netlink协议的一种类型，即kobject uevent类型。kobject uevent用于内核对象相关的事件通知，当内核中的kobject对象发生变化时，会通过此类型的Netlink消息通知用户空间。


### 8、




## 绑定套接字
### 1 、创建套接字后，需要将其与一个网络地址绑定(❤️)


### 2 、用bind()系统调用


### 3 、原型和所需头文件如下：

|                                                             |                                                                                                      |
| ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| #include <sys/types.h>          <br>#include <sys/socket.h> | int bind**(**int sockfd**,** const struct sockaddr *****addr**,**<br><br>socklen_t addrlen**);**<br> |

>` sockfd`参数指定了需要绑定的**套接字描述符**，
> `addr`参数指定了**需要绑定的地址信息**，这里使用**sockaddr_nl结构体**，sockaddr_nl结构体的定义如下：

> `addrlen`参数：addrlen参数是一个整数，指定了**addr所指向的结构体对应的字节长度**。它用于确保正确解析传递给addr参数的结构体的大小。





### 4 、sockaddr_nl结构体的定义如下：(❤️)
```c
struct sockaddr_nl {
    sa_family_t nl_family;  // AF_NETLINK
    unsigned short nl_pad;  // zero
    uint32_t nl_pid;        // port ID
    uint32_t nl_groups;     // multicast groups mask
};
```

> `nl_family`：表示**地址族**，此处固定为**AF_NETLINK**，指示使用Netlink协议族。
> 
>` nl_pad`：**填充字段，设置为0**。在结构体中进行字节对齐时使用。
> 
> `nl_pid`：端口ID，表示进程的标识符。可以将其设置为**当前进程的PID，也可以设为0**，表示不加入任何多播组。
> 
>` nl_groups`：多播组掩码，用于**指定感兴趣的多播组**。当设置为**1时，表示用户空间进程只会接收内核事件的基本组的内核事件**。这意味着，用户空间进程将只接收到属于基本组的内核事件，而不会接收其他多播组的事件。



### 5、编程示例如下
```c
struct sockaddr_nl *nl;  // 定义一个指向 struct sockaddr_nl 结构体的指针 nl
 
bzero(nl, sizeof(struct sockaddr_nl));  // 将 nl 指向的内存区域清零，确保结构体的字段初始化为0
 
nl->nl_family = AF_NETLINK;  // 设置 nl 结构体的 nl_family 字段为 AF_NETLINK，指定地址族为 Netlink
nl->nl_pid = 0;  // 设置 nl 结构体的 nl_pid 字段为 0，表示目标进程 ID 为 0，即广播给所有进程
nl->nl_groups = 1;  // 设置 nl 结构体的 nl_groups 字段为 1，表示只接收基本组的内核事件
 
ret = bind(socket_fd, (struct sockaddr *)nl, sizeof(struct sockaddr_nl));  // 使用 bind 函数将 socket_fd 套接字与 nl 地址结构体绑定在一起
 
if (ret < 0) {
    printf("bind error\n");
    return -1;
}
```

### 6、


### 7、




## 接收数据
### 1 、直接使用recv函数进行接收
- 1 Netlink套接字在接收数据时不需要调用listen函数

### 2 、recv函数的相关说明：
```c
#include <sys/types.h>
#include <sys/socket.h>

ssize_t recv(int sockfd, void *buf, size_t len, int flags);
```

> 函数参数：
> 
> sockfd：指定套接字描述符，即要接收数据的Netlink套接字。
> 
> `buf`：**指向数据接收缓冲区的指针**，用于存储接收到的数据。
> 
> len：指定要读取的数据的字节大小。
> 
>` flags`：指定一些标志，用于控制数据的接收方式。通常情况下，可以将其设置**为0**。
> 
> 返回值：
> 
> 成功情况下，**返回实际读取到的字节数。**
> 
> 如果返回值`为0`，表示**对方已经关闭了连接。**
> 
> 如果返回值`为-1`，表示发生了**错误**，可以通过查看errno变量来获取具体的错误代码。


### 3 、具体代码示例如下
```c
while (1) {
    bzero(buf, 4096);  // 将缓冲区 buf 清零，确保数据接收前的初始化
    len = recv(socket_fd, &buf, 4096, 0);  // 从 socket_fd 套接字接收数据，存储到缓冲区 buf 中，最大接收字节数为 4096
 
    for (i = 0; i < len; i++) {
        if (*(buf + i) == '\0') {  // 如果接收到的数据中有 '\0' 字符，将其替换为 '\n'，以便在打印时换行显示
            buf[i] = '\n';
        }
    }
 
    printf("%s\n", buf);  // 打印接收到的数据
}
```


### 4 、




# 三、实验：

##  实验程序的编写
### 1 、使用netlink监听广播信息的应用程序
> 本应用程序对应的网盘路径为：iTOP-RK3568开发板【底板V1.7版本】\03_【iTOP-RK3568开发板】指南教程\02_Linux驱动配套资料\04_Linux驱动例程\80_netlink。



### 2 、netlink.c.c代码如下(❤️)
```c
#include <stdio.h>
#include <strings.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <linux/netlink.h>
 
int main(int argc, char *argv[]) {
    int ret;
    struct sockaddr_nl *nl;  // 定义一个指向 struct sockaddr_nl 结构体的指针 nl
    int len = 0;
    char buf[4096] = {0};  // 数据接收缓冲区
    int i = 0;
 
    bzero(nl, sizeof(struct sockaddr_nl));  // 将 nl 指向的内存区域清零，确保结构体的字段初始化为0
    nl->nl_family = AF_NETLINK;  // 设置 nl 结构体的 nl_family 字段为 AF_NETLINK，指定地址族为 Netlink
    nl->nl_pid = 0;  // 设置 nl 结构体的 nl_pid 字段为 0，表示目标进程 ID 为 0，即广播给所有进程
    nl->nl_groups = 1;  // 设置 nl 结构体的 nl_groups 字段为 1，表示只接收基本组的内核事件
 
    int socket_fd = socket(AF_NETLINK, SOCK_RAW, NETLINK_KOBJECT_UEVENT);  // 创建一个 Netlink 套接字
    if (socket_fd < 0) {
        printf("socket error\n");
        return -1;
    }
 
    ret = bind(socket_fd, (struct sockaddr *)nl, sizeof(struct sockaddr_nl));  // 使用 bind 函数将 socket_fd 套接字与 nl 地址结构体绑定在一起
    if (ret < 0) {
        printf("bind error\n");
        return -1;
    }
 
    while (1) {
        bzero(buf, 4096);  // 将缓冲区 buf 清零，确保数据接收前的初始化
        len = recv(socket_fd, &buf, 4096, 0);  // 从 socket_fd 套接字接收数据，存储到缓冲区 buf 中，最大接收字节数为 4096
 
        for (i = 0; i < len; i++) {
            if (*(buf + i) == '\0') {  // 如果接收到的数据中有 '\0' 字符，将其替换为 '\n'，以便在打印时换行显示
                buf[i] = '\n';
            }
        }
 
        printf("%s\n", buf);  // 打印接收到的数据
    }
 
    return 0;
}
```

### 3 、


##  运行测试

### 4 、驱动文件为上一章编译生成的uevent_ops.ko


### 5、让应用程序在后台运行
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第116章 netlink监听广播信息实验/file-20260313152657471.png]]

### 6、加载uevent_ops.ko驱动(❤️)
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第116章 netlink监听广播信息实验/file-20260313152707749.png]]

### 7、


### 8、



## 
### 1 、


### 2 、


### 3 、



### 4 、


### 5、


### 6、


### 7、


### 8、



## 
### 1 、


### 2 、


### 3 、



### 4 、



### 5、


### 6、


### 7、


### 8、


# 四、

## 
### 1 、


### 2 、


### 3 、



### 4 、



### 5、


### 6、


### 7、


### 8、



## 
### 1 、


### 2 、


### 3 、



### 4 、


### 5、


### 6、


### 7、


### 8、



## 
### 1 、


### 2 、


### 3 、



### 4 、



### 5、


### 6、


### 7、


### 8、


# 五、

## 
### 1 、


### 2 、


### 3 、



### 4 、



### 5、


### 6、


### 7、


### 8、



## 
### 1 、


### 2 、


### 3 、



### 4 、


### 5、


### 6、


### 7、


### 8、



## 
### 1 、


### 2 、


### 3 、



### 4 、



### 5、


### 6、


### 7、


### 8、


