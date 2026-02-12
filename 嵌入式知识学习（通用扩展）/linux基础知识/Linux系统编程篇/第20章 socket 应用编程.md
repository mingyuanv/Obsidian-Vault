---
title: "【北京迅为】《iTOP-3588开发板系统编程手册》-第20章 socket 应用编程"
source: "https://blog.csdn.net/BeiJingXunWei/article/details/138133974"
author:
  - "[[BeiJingXunWei]]"
published: 2024-04-23
created: 2025-09-11
description: "文章浏览阅读1.3k次，点赞13次，收藏11次。Socket是计算机网络编程中一个重要的概念，它是在应用层和传输层之间提供的一种抽象接口，用于实现应用程序之间的数据交换。Socket允许程序员使用一种通用的接口来访问底层传输协议，如TCP和UDP，以便进行网络通信。Socket是一种编程接口，它提供了一种标准化的方式来创建网络连接，并允许应用程序在网络上发送和接收数据。Socket API提供了一组函数，这些函数可以用于创建和配置套接字，建立连接，发送和接收数据，以及关闭连接等操作。_rk3588 socket"
tags:
  - "clippings"
---
[RK3588](https://so.csdn.net/so/search?q=RK3588&spm=1001.2101.3001.7020) 是一款低功耗、高性能的处理器，适用于基于arm的PC和Edge计算设备、个人移动互联网设备等数字多媒体应用，RK3588支持8K视频编解码，内置GPU可以完全兼容OpenGLES 1.1、2.0和3.2。RK3588引入了新一代完全基于硬件的最大4800万像素ISP，内置NPU，支持INT4/INT8/INT16/FP16混合运算能力，支持安卓12和、Debian11、Build root、Ubuntu20和22版本登系统。了解更多信息可点击 [迅为官网](http://www.topeetboard.com/Product/3588hk.html "迅为官网  ")

【粉丝群】824412014

【实验平台】：迅为RK3588开发板

【内容来源】《iTOP-3588开发板系统编程手册》

【全套资料及网盘获取方式】联系淘宝客服加入售后技术支持群内下载

【视频介绍】： [【强者之芯】 新一代AIOT高端应用芯片 iTOP -3588人工智能工业AI主板](https://blog.csdn.net/BeiJingXunWei/article/details/?share_source=copy_web&vd_source=2028a54593d986008d44cdb9a5d790c7)

---

## 第20章 socket 应用编程

### 20.1 socket介绍

Socket是计算机网络编程中一个重要的概念，它是在应用层和传输层之间提供的一种抽象接口，用于实现应用程序之间的数据交换。Socket允许程序员使用一种通用的接口来访问底层传输协议，如 TCP 和UDP，以便进行网络通信。

Socket是一种编程接口，它提供了一种标准化的方式来创建网络连接，并允许应用程序在网络上发送和接收数据。Socket API提供了一组函数，这些函数可以用于创建和配置套接字，建立连接，发送和接收数据，以及关闭连接等操作。

在计算机网络中，通常使用两种不同的套接字类型：流套接字和数据报套接字。流套接字提供了面向连接的可靠数据传输，例如TCP协议，而数据报套接字则提供了不可靠的数据传输，例如UDP协议。下面对一些常见的Socket编程相关术语进行介绍：

| 相关术语 | 属于介绍 |
| --- | --- |
| IP地址 | 唯一标识了网络上的一台主机 |
| 端口号 | 是一个16位数字，用于标识一个应用程序在主机上的具体位置 |
| 套接字 | 用于标识一条网络连接的两端，包含IP地址和端口号 |
| 服务器 | 在网络上提供服务的主机 |
| 客户端 | 与服务器进行通信的主机 |

Socket编程通常分为两个部分：服务器端和客户端。服务器端监听一个指定的端口，等待客户端连接。一旦客户端连接到服务器端，服务器端将创建一个新的套接字来处理该客户端的请求。服务器可以同时处理多个客户端请求，每个客户端都会有自己的套接字连接。

客户端首先创建一个套接字，然后连接到服务器端的指定IP地址和端口号。一旦连接建立，客户端可以通过套接字发送和接收数据。客户端通常是一次性连接，一旦任务完成就关闭套接字。

Socket编程可以用于各种不同的应用程序，例如聊天程序、文件传输、在线游戏等。Socket编程还可以用于创建网络服务器，提供Web服务、FTP服务、邮件服务等。

### 20.2 socket编程步骤

socket编程的主要步骤和对应的系统调用如下所示：

| 步骤 | 介绍 | 系统调用 |
| --- | --- | --- |
| 1 | 创建套接字 | socket(domain, type, protocol) |
| 2 | 绑定套接字 | bind(sockfd, addr, addrlen) |
| 3 | 监听连接 | listen(sockfd, backlog) |
| 4 | 接受连接 | accept(sockfd, addr, addrlen) |
| 5 | 接收和发送数据 | recv(sockfd, buf, len, flags)  send(sockfd, buf, len, flags) |
| 6 | 关闭套接字 | close(sockfd) |

在本小节将对socket编程的每个步骤进行详细的介绍

#### 20.2.1创建套接字

在 Linux socket编程中，创建套接字是构建网络应用程序的第一步。套接字可以理解为应用程序和网络之间的桥梁，用于在网络上进行数据的收发和处理。

在Linux中，可以使用socket系统调用创建套接字。该系统调用的原型和所需头文件如下所示：

|  | 所需头文件 | 函数原型 |
| --- | --- | --- |
| 1  2 | #include <sys/types.h>  #include <sys/socket.h> | int socket **(**int domain**,**int type**,**int protocol**);** |

其中，domain参数指定了套接字的协议族，type参数指定了套接字的类型，protocol参数指定了套接字所使用的具体协议。下面分别介绍这三个参数的含义：

****（1）**** ****协议族****

协议族指定了套接字所使用的协议类型，常用的协议族包括AF\_INET、AF\_INET6、AF\_UNIX等。其中，AF\_INET表示IPv4协议族，AF\_INET6表示IPv6协议族，AF\_UNIX表示Unix域协议族。

****（2）**** ****套接字类型****

套接字类型指定了套接字的数据传输方式，常用的套接字类型包括SOCK\_STREAM、SOCK\_DGRAM、SOCK\_RAW等。其中，SOCK\_STREAM表示面向连接的流套接字，主要用于可靠传输数据，例如TCP协议。SOCK\_DGRAM表示无连接的数据报套接字，主要用于不可靠传输数据，例如UDP协议。SOCK\_RAW表示原始套接字，可以直接访问底层网络协议。

****（3）**** ****协议类型****

协议类型指定了套接字所使用的具体协议类型，常用的协议类型包括IPPROTO\_TCP、IPPROTO\_UDP、IPPROTO\_ICMP等。其中，IPPROTO\_TCP表示TCP协议，IPPROTO\_UDP表示UDP协议，IPPROTO\_ICMP表示ICMP协议，通常使用0表示由系统自动选择适合的协议

例如可以使用以下代码创建一个新的套接字：

```cpp
int sockfd = socket(AF_INET, SOCK_STREAM, 0);cpp
```

#### 20.2.2绑定套接字

创建套接字后，需要将其与一个网络地址绑定，以便其他计算机可以访问该套接字。在Linux系统下，可以使用bind()系统调用绑定套接字和地址。该系统调用的原型和所需头文件如下所示：

|  | 所需头文件 | 函数原型 |
| --- | --- | --- |
| 1  2 | #include <sys/types.h>  #include <sys/socket.h> | int bind **(**int sockfd**,**const struct sockaddr **\*** addr**,**  socklen\_t addrlen**);** |

其中，sockfd参数指定了需要绑定的套接字描述符，addr参数指定了需要绑定的地址信息，可以是struct sockaddr\_in或struct sockaddr\_in6等结构体类型，addrlen参数指定了地址信息的长度。使用以下代码将套接字和地址绑定：

```cpp
//创建一个 sockaddr_in 结构体类型的 servaddr 变量用于存储服务器的地址信息，并将其清零。

struct sockaddr_in servaddr;

memset(&servaddr, 0, sizeof(servaddr));

 

servaddr.sin_family = AF_INET;//指定使用 IPv4 协议（AF_INET）

servaddr.sin_addr.s_addr = htonl(INADDR_ANY);//监听本地任意可用的 IP 地址（INADDR_ANY）

servaddr.sin_port = htons(port);//使用指定的端口号（port）。

 

//将套接字 sockfd 绑定到指定的地址 servaddr 上，bind() 函数返回值为0表示绑定成功，

if (bind(sockfd, (struct sockaddr)&servaddr, sizeof(servaddr)) != 0)

{

    perror("bind");

    exit(EXIT_FAILURE);

}
cpp
```

其中，servaddr是一个struct sockaddr\_in类型的变量，用于存储需要绑定的地址信息，sockaddr\_in 结构体的定义如下：

```cpp
struct sockaddr_in {

    sa_family_t sin_family; // 地址族

    in_port_t sin_port; // 端口号

    struct in_addr sin_addr; // IP 地址

    char sin_zero[8]; // 填充字符

};
cpp
```

在初始化 sockaddr\_in 结构体时，用到了以下函数：

****memset()：**** 用来将 sockaddr\_in 结构体的各个成员变量初始化为 0，这是一个常用的初始化方式。其函数原型如下：

|  | 所需头文件 | 函数原型 |
| --- | --- | --- |
| 1 | #include <string.h> | void **\*** memset **(**void **\*** s**,**int c**,**size\_t n**);** |

其中，s 参数是需要被初始化的内存区域指针，c 参数是填充字符，n 参数是需要填充的内存字节数。

****htons**** ****l**** ****()**** ****和htons()**** ****：**** 用于将本机字节序的端口号转换为网络字节序的端口号。其函数原型如下：

|  | 所需头文件 | 函数原型 |
| --- | --- | --- |
| 1  2 | #include <arpa/inet.h> | uint32\_t htonl **(**uint32\_t hostlong**);**  uint16\_t htons **(**uint16\_t hostshort**);** |

其中，hostshort 和hostlong参数是本机字节序的端口号，函数返回值是网络字节序的端口号。

#### 20.2.3监听连接

绑定套接字后，需要开始监听连接请求，以便其他网络上的客户端能够与该套接字建立连接。这一步骤通常在服务器端完成。。在Linux系统下，可以使用listen()系统调用监听套接字。该系统调用的原型如下：

|  | 所需头文件 | 函数原型 |
| --- | --- | --- |
| 1 | #include <sys/socket.h> | int listen **(**int socket**,**int backlog**);** |

其中，sockfd参数指定了需要监听的套接字描述符，backlog参数指定了连接队列的长度，即等待接受的连接数。例如可以使用以下代码开始监听连接

```cpp
if (listen(sockfd, SOMAXCONN) != 0) 

{

    perror("listen");

    exit(EXIT_FAILURE);

}
cpp
```

其中，SOMAXCONN是一个宏定义，指定了连接队列的最大长度。

#### 20.3.4接受连接

当有客户端请求连接时，需要接受该连接并进行处理。在Linux系统下，可以使用accept()系统调用接受连接请求。该系统调用的原型和所需头文件如下所示：

|  | 所需头文件 | 函数原型 |
| --- | --- | --- |
| 1  2 | #include <sys/socket.h> | int accept **(**int socket**,**struct sockaddr **\*** restrict address**,**socklen\_t **\*** restrict address\_len**);** |

其中，sockfd参数指定了需要接受连接的套接字描述符，addr参数用于存储客户端的地址信息，addrlen参数用于存储地址信息的长度。使用以下代码接受连接请求：

```cpp
// 定义一个 sockaddr_in 结构体，用于存储客户端的 IP 地址和端口号

struct sockaddr_in cliaddr;

 

// 定义一个 socklen_t 类型的变量 clilen，用于存储客户端地址结构体的长度

socklen_t clilen = sizeof(cliaddr);

 

// 调用 accept() 系统调用，接受客户端的连接请求，并返回一个新的套接字描述符 connfd，

// 用于与客户端进行通信。accept() 函数会阻塞程序，直到有客户端连接到服务器端。

// sockfd 是服务端的监听套接字，cliaddr 是指向 sockaddr_in 结构体的指针，用于存储客户端的地址信息。

// clilen 是客户端地址结构体的长度，accept() 函数会将实际接受到的客户端地址长度存储到该变量中。

int connfd = accept(sockfd, (struct sockaddr*)&cliaddr, &clilen);

 

if (connfd < 0)// 判断 accept() 函数的返回值，判断客户端连接是否失败

{

    perror("accept");

    exit(EXIT_FAILURE);

}
cpp
```

#### 20.3.5接收和发送数据

在 Linux socket 编程中，接收和发送数据是套接字编程的核心步骤之一。当套接字绑定并且处于监听状态，已经成功接受了客户端的连接请求后，接下来就是进行数据的收发。下面将详细介绍如何在 Linux 系统中实现接收和发送数据的过程。

****接收数据****

在接收数据之前，需要先了解数据在网络传输中的一些基本概念。在 TCP 协议中，发送方发送的数据被分割成一个个 TCP 报文段，每个报文段都包含一个 TCP 首部和数据部分。TCP 首部中包含了一些控制信息，如序号、确认号、窗口大小等，用来保证数据的可靠传输。而数据部分则是发送方发送的应用层数据，如 HTTP 报文、FTP 文件等。

在 Linux socket 编程中，接收数据的过程分为两步：先接收 TCP 首部，再接收数据部分。具体步骤如下：

（1）创建一个缓冲区用于接收数据。缓冲区的大小一般为数据部分的大小。

（2）调用 recv() 系统调用接收数据。其函数原型和所需头文件如下：

|  | 所需头文件 | 函数原型 |
| --- | --- | --- |
| 1 | #include <sys/socket.h> | ssize\_t recv **(**int socket**,**void **\*** buffer**,**size\_t length**,**int flags**);** |

其中，sockfd 参数是需要接收数据的套接字描述符，buf 参数是用于存储接收数据的缓冲区指针，len 参数是需要接收的数据的最大长度，flags 参数是接收标志，通常为 0。函数返回值为实际接收到的字节数，如果返回值为 0，表示对端已经关闭连接。

在调用 recv() 系统调用时，会先接收 TCP 首部，然后再接收数据部分。如果数据部分比较大，可能需要多次调用 recv() 系统调用才能接收完整的数据。因此，需要使用一个循环来不断接收数据，直到接收到全部数据或者出现错误为止。

另外，需要注意的是，recv() 系统调用是一个阻塞调用，即程序会一直等待直到接收到数据或者出现错误才会返回。如果不希望阻塞调用，可以使用非阻塞 I/O 或者多路复用技术，之前的章节已经学习过了，这里不再进行赘述。

1. 处理接收到的数据。在数据接收完成后，需要对接收到的数据进行处理。具体处理方式根据具体的应用场景而定，如将接收到的数据显示在终端上、将数据写入文件等。

****发送数据****

发送数据的步骤如下：

（1）定义数据缓冲区：需要定义一个用于存储待发送数据的缓冲区，比如 char buf\[MAXLINE\]。

（2）将数据拷贝到缓冲区：将需要发送的数据拷贝到缓冲区中，可以使用 strcpy()、memcpy() 等函数进行拷贝操作。

（3）使用 send() 函数发送数据：send() 函数用于向已经建立连接的套接字发送数据，其函数原型如下：

|  | 所需头文件 | 函数原型 |
| --- | --- | --- |
| 1 | #include <sys/socket.h> | ssize\_t send **(**int sockfd**,**const void **\*** buf**,**size\_t len**,**int flags**);** |

函数调用成功将返回发送数据的字节数（返回值为非负数），返回-1 表示发送失败。

send()函数参数含义如下所示：

|  | 参数名称 | 参数含义 |
| --- | --- | --- |
| 1 | sockfd | 需要发送数据的套接字描述符。 |
| 2 | buf | 待发送数据的缓冲区指针。 |
| 3 | len | 待发送数据的长度。 |
| 4 | flags | 传输标志，通常为 0。 |

数据接收示例代码如下：

```cpp
ssize_t n = send(connfd, buf, strlen(buf), 0);

if (n < 0)

{

    perror("send");

    exit(EXIT_FAILURE);

}
cpp
```

需要注意的是，send() 函数并不保证一次能够将所有数据都发送出去，如果数据量比较大，可能需要多次调用 send() 函数才能将所有数据发送出去。

（4）判断是否发送完毕：可以通过判断 send() 函数的返回值和待发送数据的长度是否相等来确定是否发送完毕。

示例代码如下：

```cpp
if (n == strlen(buf))

{

    printf("Send successfully!\n");

}

else

{

    printf("Send incomplete!\n");

}
cpp
```

#### 20.3.6关闭套接字

关闭套接字是一个非常重要的步骤。当套接字不再需要使用时，应该立即关闭以释放系统资源和避免资源浪费。，关闭套接字的步骤非常简单，只需要调用 close() 系统调用即可。close() 系统调用的函数原型如下：

```cpp
int close(int sockfd);cpp
```

其中，sockfd 参数是需要关闭的套接字描述符。函数返回值为 0 表示成功，返回值为 -1 表示失败。

### 20.3 socket编程实验

本小节代码在配套资料“ iTOP-3588开发板\\03\_【iTOP-RK3588开发板】指南教程\\03\_系统编程配套程序 \\ 70 ”目录下，如下图所示：

![[Clippings/assets/【北京迅为】《iTOP-3588开发板系统编程手册》-第20章 socket 应用编程/3decbc02f841549da2c66dabee48b71d_MD5.png]]

****实验要求：****

服务端接收客户端发来的数据，并将发过来的数据以及客户端ip打印出来。

****实验步骤：****

首先进入到 ubuntu 的终端界面输入以下命令来创建服务器端程序 demo70\_server.c文件，如下图所示：

> vim demo70\_server.c

然后向该文件中添加以下内容：

```cpp
#include <stdio.h>

#include <stdlib.h>

#include <string.h>

#include <unistd.h>

#include <sys/types.h>

#include <sys/socket.h>

#include <netinet/in.h>

#include <arpa/inet.h>

 

#define PORT 8888

#define BUFFER_SIZE 1024

 

int main()

{

    int sockfd, connfd;

    struct sockaddr_in servaddr, cliaddr;

    socklen_t cliaddr_len = sizeof(cliaddr);

    char buffer[BUFFER_SIZE];

 

    // 创建套接字

    sockfd = socket(AF_INET, SOCK_STREAM, 0);

    if (sockfd == -1) 

    {

        perror("socket"); // 输出错误信息

        exit(EXIT_FAILURE);

    }

 

    // 绑定地址和端口号

    memset(&servaddr, 0, sizeof(servaddr));

    servaddr.sin_family = AF_INET;

    servaddr.sin_addr.s_addr = htonl(INADDR_ANY); // INADDR_ANY 表示本机的所有IP地址

    servaddr.sin_port = htons(PORT); // 绑定端口号

    if (bind(sockfd, (struct sockaddr *)&servaddr, sizeof(servaddr)) == -1) 

    {

        perror("bind"); // 输出错误信息

        exit(EXIT_FAILURE);

    }

 

    // 监听连接

    if (listen(sockfd, 10) == -1) 

    {

        perror("listen"); // 输出错误信息

        exit(EXIT_FAILURE);

    }

 

    printf("Server started.\n");

 

    // 接受客户端连接

    connfd = accept(sockfd, (struct sockaddr *)&cliaddr, &cliaddr_len);

    if (connfd == -1) 

    {

        perror("accept"); // 输出错误信息

        exit(EXIT_FAILURE);

    }

 

    printf("Client connected: %s:%d\n", inet_ntoa(cliaddr.sin_addr), ntohs(cliaddr.sin_port)); // 输出客户端地址和端口号

 

    // 接收数据

    while (1) 

    {

        memset(buffer, 0, BUFFER_SIZE); // 清空缓冲区

        ssize_t numBytes = recv(connfd, buffer, BUFFER_SIZE - 1, 0); // 接收数据

        if (numBytes == -1) 

        {

            perror("recv"); // 输出错误信息

            exit(EXIT_FAILURE);

        }

        else if (numBytes == 0) 

        {

            printf("Client closed connection.\n"); // 客户端关闭连接

            break;

        }

        else 

        {

            printf("Received from client (%s:%d): %s", inet_ntoa(cliaddr.sin_addr), ntohs(cliaddr.sin_port), buffer); // 输出接收到的数据和客户端地址和端口号

        }

    }

 

    // 关闭套接字

    close(connfd);

    close(sockfd);

 

    printf("Server terminated.\n");

 

    return 0;

}
cpp
```

保存退出之后，创建客户端程序demo70\_server.c，然后向该文件写入以下内容如下所示：

```cpp
#include <stdio.h>

#include <stdlib.h>

#include <string.h>

#include <unistd.h>

#include <sys/types.h>

#include <sys/socket.h>

#include <netinet/in.h>

#include <arpa/inet.h>

 

#define PORT 8888

#define BUFFER_SIZE 1024

 

int main(int argc, char *argv[])

{

    int sockfd;

    struct sockaddr_in servaddr;

    char buffer[BUFFER_SIZE];

 

     // 检查命令行参数个数

    if (argc < 2) 

    {

        fprintf(stderr, "Usage: %s server_ip\n", argv[0]); // 打印使用方法

        exit(EXIT_FAILURE);

    }

 

    // 创建套接字

    sockfd = socket(AF_INET, SOCK_STREAM, 0);

    if (sockfd == -1) // 创建套接字失败

    {

        perror("socket"); // 打印错误信息

        exit(EXIT_FAILURE);

    }

 

    // 设置服务端地址和端口号

    memset(&servaddr, 0, sizeof(servaddr)); // 将地址结构体清零

    servaddr.sin_family = AF_INET; // 使用IPv4地址

    servaddr.sin_addr.s_addr = inet_addr(argv[1]); // 从命令行参数中获取服务器IP地址

    servaddr.sin_port = htons(PORT); // 设置服务器端口号

 

    // 连接服务器

    if (connect(sockfd, (struct sockaddr *)&servaddr, sizeof(servaddr)) == -1) // 连接失败

    {

        perror("connect"); // 打印错误信息

        exit(EXIT_FAILURE);

    }

 

    // 从终端读入数据并发送给服务器

    while (fgets(buffer, BUFFER_SIZE, stdin) != NULL) // 从标准输入中读取一行数据

    {

        if (send(sockfd, buffer, strlen(buffer), 0) == -1) // 发送消息到服务器

        {

            perror("send"); // 打印错误信息

            exit(EXIT_FAILURE);

        }

    }

 

    // 关闭套接字

    close(sockfd);

 

    return 0;

 

}
cpp
```

保存退出之后，使用以下命令设置交叉编译器环境，并分别对demo70\_server.c和demo70\_client.c进行编译和交叉编译，编译完成如下图所示：

> export PATH=/usr/local/ [arm64](https://so.csdn.net/so/search?q=arm64&spm=1001.2101.3001.7020) /gcc-arm-10.3-2021.07-x86\_64-aarch64-none-linux-gnu/bin:$PATH
> 
> gcc -o demo70\_server demo70\_server.c
> 
> aarch64-none-linux-gnu-gcc -o demo70\_client demo70\_client.c

![[Clippings/assets/【北京迅为】《iTOP-3588开发板系统编程手册》-第20章 socket 应用编程/943d86a3933cc70bc5d591db65d5acc0_MD5.png]] 然后将交叉编译生成的demo70\_client文件拷贝到/home/nfs共享目录下，如下图所示：

![[Clippings/assets/【北京迅为】《iTOP-3588开发板系统编程手册》-第20章 socket 应用编程/c239fceca7f90931b120679f81d85e48_MD5.png]]

首先启动开发板，Buildroot系统启动之后，首先使用以下命令进行nfs共享目录的挂载（ 其中 192.168.1.7 为作者ubuntu的ip地址，需要根据自身ubuntu的ip来设置 ），如下图所示：

> mount -t nfs -o nfsvers=3,nolock 192.168.1.7:/home/nfs /mnt

![[Clippings/assets/【北京迅为】《iTOP-3588开发板系统编程手册》-第20章 socket 应用编程/b4aad5c3877a8e546773194a6634e06a_MD5.png]] nfs共享目录挂载到了开发板的/mnt目录下，进入到/mnt目录下，如下图所示：

![[Clippings/assets/【北京迅为】《iTOP-3588开发板系统编程手册》-第20章 socket 应用编程/50f2f9776da976b30580f59c1a1035d8_MD5.png]] 可以看到/mnt目录下的demo70\_client文件已经存在了，该程序为socket的客户端，首先使用命令“ ifconfig ”命令查看本机IP如下图所示：

![[Clippings/assets/【北京迅为】《iTOP-3588开发板系统编程手册》-第20章 socket 应用编程/19dc53a5f252e6153e8949dc777aca45_MD5.png]] 可以看到开发板IP为192.168.1.106，然后在虚拟机ubuntu上使用“ifconfig”命令查看服务端IP，如下所示：

![[Clippings/assets/【北京迅为】《iTOP-3588开发板系统编程手册》-第20章 socket 应用编程/e764563b1d2c7aadbd58233370a7287b_MD5.png]]

可以看到服务端IP为192.168.1.7，然后在虚拟机ubuntu使用“./demo70\_server ”命令运行服务端程序，如下图所示：

![[Clippings/assets/【北京迅为】《iTOP-3588开发板系统编程手册》-第20章 socket 应用编程/f7696edfbdb09dac6f1f1bc46adfb045_MD5.png]]

可以看到该应用会阻塞，等待服务端连接，下面回到开发板终端，使用以下命令运行socket客户端应用程序连接服务端，如下图所示：

> ./demo70\_client 192.168.1.7

![[Clippings/assets/【北京迅为】《iTOP-3588开发板系统编程手册》-第20章 socket 应用编程/c313754127e2f99295327da1668c8ae8_MD5.png]]

然后输入要发送的数据，如下图所示：

![[Clippings/assets/【北京迅为】《iTOP-3588开发板系统编程手册》-第20章 socket 应用编程/1a5907fb0a5ed933191b842f6b6a70ad_MD5.png]]

在虚拟机ubuntu虚拟机运行的服务端代码会接收到相应的数据如下图所示：

![[Clippings/assets/【北京迅为】《iTOP-3588开发板系统编程手册》-第20章 socket 应用编程/f694dda207ebc087a924a75f3aaa0eb1_MD5.png]]

至此，我们的socket简单测试就完成了，本小节只是对socket编程进行简单的认识，如果想要更深入的了解socket编程可以在网上寻找专门的书籍或者视频来进行学习。

微信公众号

内容来源：csdn.net

作者昵称：北京迅为

原文链接：https://blog.csdn.net/BeiJingXunWei/article/details/138133974

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

![[Clippings/assets/【北京迅为】《iTOP-3588开发板系统编程手册》-第20章 socket 应用编程/90bd0cbf3aff8fdff8bf9b011b581e20_MD5.png]]

程序员都在用的中文IT技术交流社区

![[Clippings/assets/【北京迅为】《iTOP-3588开发板系统编程手册》-第20章 socket 应用编程/08a47e60886378fe60a3d9c8f4ae8bc6_MD5.png]]

专业的中文 IT 技术社区，与千万技术人共成长

![[Clippings/assets/【北京迅为】《iTOP-3588开发板系统编程手册》-第20章 socket 应用编程/a51be6c085b867a5bd82d8dc1cea9b46_MD5.png]]

关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！

客服 返回顶部

微信公众号

![[Clippings/assets/【北京迅为】《iTOP-3588开发板系统编程手册》-第20章 socket 应用编程/efb7921311640694e61fee00900550d6_MD5.jpg]] 公众号名称：迅为电子 微信扫码关注或搜索公众号名称

复制公众号名称