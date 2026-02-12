---
title: "Linux应用开发笔记（四）网络编程（一）TCP和UDP_linux tcp和udp编写-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/137271995?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读791次，点赞13次，收藏16次。之前我们常常使用串口等进行信息打印，但是这种方式并不适用与多主(从)机的网络系统，这里编引入了网络编程的概念。简单来说，Linux网络编程涉及使用套接字（sockets）进行进程间通信，特别是在不同主机上的进程之间。套接字提供了一种标准的接口，用于在不同主机之间传输数据，无论它们使用的是何种操作系统或网络协议。_linux tcp和udp编写"
tags:
  - "clippings"
---
> 提示：文章写完后，目录可以自动生成，如何生成可参考右边的 [帮助文档](https://so.csdn.net/so/search?q=%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3&spm=1001.2101.3001.7020)

---

## 前言

  之前我们常常使用串口等进行信息打印，但是这种方式并不适用与多主(从)机的网络系统，这里编引入了网络编程的概念。简单来说， Linux 网络编程涉及使用套接字（sockets）进行进程间通信，特别是在不同主机上的进程之间。套接字提供了一种标准的接口，用于在不同主机之间传输数据，无论它们使用的是何种操作系统或网络协议。

## 一、网络通信

### 1\. 数据传输三要素

- 源（Source）：  
	  源指的是数据传输的起始点，即数据发送方。在网络通信中，这通常是一个具体的设备或应用程序，它负责生成并发送数据。例如，在一个客户端-服务器架构中，客户端可能是数据的源，当它向服务器发送请求时。
- 目的（Destination）：  
	  目的是数据传输的终点，即数据接收方。与源相对应，目的也是网络中的一个设备或应用程序，它负责接收并处理从源发送过来的数据。在前面的例子中，服务器就是数据的目的地，因为它接收并响应客户端的请求。
- 长度（Length）：  
	  长度指的是要传输的数据的大小或量。这通常以字节（bytes）为单位来衡量，并且是数据传输过程中一个重要的参数。知道数据的长度有助于接收方正确地接收和解析数据，也能帮助网络中的中间设备（如路由器或交换机）有效地处理和转发数据。在某些协议中，数据包的长度信息可能包含在数据包头中，以便在传输过程中进行验证和处理。

### 2\. 网络通讯的两个实体

  在网络通讯中，客户（Client）和服务器（ Server ）是两种主要的通讯实体，它们分别扮演不同的角色：

- 客户（Client）：  
	  客户端是发起请求的一方。它通常是一个用户操作的设备或软件，用于访问服务器上的资源或服务。客户端可以是各种形式的设备，如个人电脑、智能手机、平板电脑等，也可以是运行在这些设备上的应用程序，如网页浏览器、电子邮件客户端、即时通讯软件等。客户端通常不直接存储大量的数据或执行复杂的计算任务，而是依赖服务器来处理这些需求。
- 服务器（Server）：  
	  服务器是响应客户端请求的一方。它提供数据、资源或服务，以满足客户端的需求。服务器通常是一台高性能的计算机或一组计算机集群，运行着专门的服务软件，用于处理来自多个客户端的并发请求。服务器可以存储大量的数据，并执行各种复杂的计算任务。它还可以运行数据库管理系统、文件服务器、邮件服务器、Web服务器等各种服务，以支持不同类型的客户端应用。

  在客户端-服务器架构中，客户端和服务器之间的通信通常遵循请求-响应模式，即：

- 客户端向服务器发送一个请求，请求可以包含需要的数据、要执行的操作或其他相关信息；
- 服务器接收到请求后进行处理，根据请求的类型和内容来检索数据、执行计算或执行其他必要的操作；
- 服务器将处理结果打包成一个响应，并将其发送回客户端；
- 客户端接收到响应后解析并显示结果，或者根据需要进行进一步的处理；

### 3\. TCP/UDP协议

  TCP（Transmission Control Protocol，传输控制协议）和UDP（User Datagram Protocol，用户数据报协议）是 计算机网络 中两种常用的传输层协议。它们在网络通讯中发挥着重要作用，但具有不同的特性和应用场景。

#### 3.1 TCP协议

  TCP是一种面向连接的、可靠的、基于字节流的传输层协议。它提供了许多功能，如数据流传送、可靠性、有效流控、全双工操作和多路复用等。TCP通过建立连接（三次握手）和确认机制来确保数据的可靠传输。这种协议适用于需要高可靠性的应用，如文件传输、电子邮件和网络浏览器通信等。  
  TCP建立连接的过程通常被称为“三次握手”。这个过程确保了通信双方（客户端和服务器）都准备好进行数据传输。以下是三次握手的详细步骤：

- 第一次握手：客户端向服务器发送一个SYN包（同步包），其中包含客户端的初始序列号。此时，客户端进入SYN\_SEND状态，等待服务器的确认。
- 第二次握手：服务器收到SYN包后，会确认客户端的SYN（通过发送一个ACK包，其中ack=客户端的序列号+1），同时服务器也会发送一个自己的SYN包，其中包含服务器的初始序列号。这个包通常被称为SYN+ACK包。此时，服务器进入SYN\_RECV状态。
- 第三次握手：客户端收到服务器的SYN+ACK包后，会再次发送一个ACK包以确认收到服务器的SYN包（ack=服务器的序列号+1）。发送完这个ACK包后，客户端和服务器都进入ESTABLISHED状态，表示连接已建立成功。  
	  除了三次握手外，TCP还使用确认机制来确保数据的可靠传输。在TCP中，每个发送的数据段都会包含一个序列号，接收方在成功接收到数据段后会发送一个确认应答（ACK包），其中包含已接收到的最后一个数据段的序列号加1。这样，发送方就能知道哪些数据段已被成功接收，哪些可能需要重传。如果发送方在规定的时间内没有收到确认应答，它会认为数据段可能已丢失，并触发重传机制。这种超时重传机制是TCP确保数据可靠传输的重要手段之一。  
	![TCP](https://i-blog.csdnimg.cn/blog_migrate/043393e91b163f93986843845a5b3b32.png)

#### 3.2 UDP协议

  UDP协议是一种无连接的、不可靠的、基于数据报的传输层协议。与TCP相比，UDP更加简单和高效，因为它不需要建立连接和维护状态信息。UDP的优势在于其低开销和快速传输速度，适用于对实时性要求较高的应用，如视频通话、音频流传输和实时游戏等。此外，UDP还支持广播和多播功能，可以将数据发送给多个目标主机。  
  总的来说，TCP和UDP各有其优势和适用场景。TCP适用于需要高可靠性和完整性的数据传输，而UDP则更适用于对实时性要求较高或需要广播/多播功能的应用。在选择使用哪种协议时，需要根据具体的应用需求和网络环境进行权衡和决策。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7076cf7718900884ecd15b39ccb8b16a.png)

## 二、网络协议的编写

  首先我们需要引入套接字（sockets）的概念，这是网络通信的端点，它提供了一个编程接口，使得应用程序能够通过网络发送和接收数据。套接字是计算机网络中进行网络通信的编程接口，无论是在同一台计算机上还是在不同的计算机之间，都可通过套接字进行数据传输。  
  在 [Linux网络编程](https://so.csdn.net/so/search?q=Linux%E7%BD%91%E7%BB%9C%E7%BC%96%E7%A8%8B&spm=1001.2101.3001.7020) 中，套接字可以分为不同类型的，如 **流套接字** （SOCK\_STREAM，用于TCP协议）和 **数据报套接字** （SOCK\_DGRAM，用于UDP协议）。流套接字提供了一种可靠、双向、基于连接的数据传输服务，适用于需要稳定可靠传输的应用场景，如文件传输、邮件发送等；而数据报套接字则提供了一种无连接、不可靠的数据传输服务，适用于对实时性要求较高、能够容忍一定数据丢失的应用场景，如实时音视频传输、在线游戏等。

### 1.socket的相关函数

  套接字编程涉及使用特定的系统调用来创建、连接、读写和关闭套接字。常见的套接字编程函数包括socket()、bind()、listen()、accept()、connect()、send()、recv()等。这些函数允许开发者在应用程序中创建套接字，并将其绑定到特定的IP地址和端口号，从而实现网络通信的功能。  
  其相关函数如下：

#### socket( )函数

```c
//socket()用于创建套接字(AF_INET)，同时指定协议(SOCK_STREAM)和类型(0)
#include <sys/types.h>          
#include <sys/socket.h>//需要引入的头文件
int socket(int domain, int type, int protocol);
1234
```

**参数** ：  
a) domain可以选择为：

- AF\_INET：IPv4因特网域
- AF\_INET6：IPv6因特网域
- AF\_UNIX：Unix域
- AF\_ROUTE：路由套接字
- AF\_KEY：密钥套接字
- AF\_UNSPEC：未指定

b) type可以选择为：

- SOCK\_STREAM:流式套接字提供可靠的，面向连接的通信流，它使用TCP协议，从而保证了数据传输的正确性和顺序性
- SOCK\_DGRAM：数据报套接字定义了一种无连接的服，数据通过相互独立的报文进行传输，是无序的，并且不保证是可靠，无差错的。它使用数据报协议

c) protocol：通常赋值为“0”

- 0选择type类型对应的默认协议
- IPPROTO\_TCP：TCP传输协议
- IPPROTO\_UDP：UDP传输协议
- IPPROTO\_SCTP：SCTP传输协议
- IPPROTO\_TIPC：TIPC传输协议

**返回值** ：成功返回非负套接字描述符，失败返回-1

#### bind( )函数

```c
//用于绑定IP地址和端口号到socket
int bind(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
12
```

**参数** ：

- sockfd：socket描述符
- addr：指向包含有本机IP地址及端口号等信息的sockaddr类型的指针，指向要绑定给sockfd的协议地址结构，这个地址结构根据地址创建socket时的地址协议族的不同而不同。
- addrlen：地址的长度，一般用sizeof(struct sockaddr\_in)表示

**返回值** ：成功返回0，失败返回-1

#### listen( )函数

```c
//监听被绑定的端口
int listen(int sockfd, int backlog);
12
```

**参数** ：

- sockfd：socket系统调用返回的服务端socket描述符
- backlog:指定在请求队列中允许的最大的请求数，大多数系统默认为5

**返回值** ：成功返回0，失败返回-1

#### accept( )函数

```c
//接收连接请求,由TCP服务器调用，用于从已完成连接队列对头返回下一个已完成连接，如果已完成连接队列为空，那么进程被投入睡眠
int accept(int sockfd, struct sockaddr *addr, socklen_t *addrlen);
12
```

**参数** ：

- sockfd：是socket系统调用返回的服务器端socket描述符
- addr:用来返回已连接的对端（客户端）的协议地址
- addrlen:客户端地址长度，注意需要取地址

**返回值** ：  
  该函数的返回值是一个新的套接字的描述符，返回值是表示已连接的套接字描述符，而第一个参数是服务器监听套接字描述符，一个服务器通常仅仅创建一个监听套接字，它在该服务器的生命周期内一直存在。内核为每个由服务器进程接受的客户连接创建一个已连接套接字（表示TCP三次握手已完成），当服务器完成对某个给定客户的服务时，相应的已连接套接字就会被关闭。

#### connect( )函数

```c
//发送连接请求,用于绑定之后的client端（客户端），与服务器建立连接
int connect(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
12
```

**参数** ：

- sockfd：创建的socket描述符
- addr：服务端的ip地址和端口号的地址结构指针
- addrlen：地址的长度，通常被设置为sizeof(struct sockaddr)

**返回值** ：成功返回0，遇到错误时返回-1，并且errno中包含相应的错误码

#### send( )函数

```c
//TCP发送信息
ssize_t send(int sockfd, const void *buf, size_t len, int flags);
12
```

**参数** ：

- sockfd：为已建立好连接的套接字描述符即accept函数的返回值
- buf：要发送的内容 len:发送内容的长度
- flags：设置为MSG\_DONTWAITMSG 时表示非阻塞，设置为0时功能和write一样  
	**返回值** ：成功返回实际发送的字节数，失败：返回 -1

#### recv( )函数

```c
//TCP接收信息
ssize_t recv(int sockfd, const void *buf, size_t len, int flags);  
12
```

**参数** ：

- sockfd：在哪个套接字接
- buf：存放要接收的数据的首地址
- len：要接收的数据的字节
- flags：设置为MSG\_DONTWAITMSG 时 表示非阻塞，设置为0时功能和read一样

**返回值** ：成功返回实际发送的字节数，失败：返回 -1

#### recvfrom函数（UDP）

```c
//recvfrom通常用于【无连接】套接字，因为此函数可以获得发送者的地址。
ssize_t recvfrom(int sockfd, void *buf, size_t len, int flags,

                struct sockaddr *src_addr, socklen_t *addrlen);
1234
```

**参数** ：

- src\_addr：struct sockaddr类型的变量，该变量保存源机的IP地址及端口号
- addrlen： 常置为sizeof (struct sockaddr)

#### sendto函数（UDP）

```c
//sendto和send相似，区别在于sendto允许在无连接的套接字上指定一个目标地址。
ssize_t sendto(int sockfd, const void *buf, size_t len, int flags,

               const struct sockaddr *dest_addr, socklen_t addrlen);
1234
```

**参数** ：

- dest\_addr 表示目地机的IP地址和端口号信息
- addrlen 常常被赋值为sizeof (struct sockaddr)，值得注意的是此时为传输地址  
	**返回值** ：发送的数据字节长度或在出现发送错误时返回－1

#### 辅助函数

```c
#include <arpa/inet.h>
// 将 short 类型的整型端口号转换为 sockaddr_in 中的 sin_port 类型的网络端口号
// 将主机字节顺序转换为网络字节顺序
uint16_t htons(uint16_t hostshort);
1234
```

### 2\. TCP协议的编程流程

  本次的代码由服务器端和客户端段两部分组成，我们需要对其分别进行编码。

- 服务器端：  
	创建套接字(socket)→将socket与IP地址和端口绑定(bind)→监听被绑定的端口(listen)→接收连接请求（accept)→从socket中读取客户端发送来的信息(recv)→关闭socket(close)
```c
1#include <stdio.h>
2#include <stdlib.h>
3#include <string.h>
4#include <sys/types.h>
5#include <sys/socket.h>
6#include <netinet/in.h>
7#include <arpa/inet.h>
8#include <unistd.h>
9#include <signal.h>
10
11#define SERVER_PORT 8180
12#define C_QUEUE     10 
13
14/************************************************************
15*函数功能描述：从8180端口接收客户端数据
16*输入参数：无
17*输出参数：打印客户IP以及发来的信息
18*返回值：无
21*************************************************************/
22
23int main(int argc, char **argv)
24{
25    char buf[512];
26    int len;
27    int duty_socket;
28    int customer_socket;
29    struct sockaddr_in socket_server_addr;
30    struct sockaddr_in socket_client_addr;
31    int ret;
32    int addr_len;
33
34    signal(SIGCHLD, SIG_IGN);
35    
36      /* 服务器端开始建立socket描述符 */
37    duty_socket = socket(AF_INET, SOCK_STREAM, 0);
38    if (duty_socket == -1)
39    {
40        printf("socket error");
41        return -1;
42    }
43    
44      /* 服务器端填充 sockaddr_in结构 */
45    socket_server_addr.sin_family   = AF_INET;
46      /* 端口号转换为网络字节序 */
47    socket_server_addr.sin_port     = htons(SERVER_PORT);
48      /* 接收本机所有网口的数据 */
49    socket_server_addr.sin_addr.s_addr  = INADDR_ANY;
50    memset(socket_server_addr.sin_zero, 0, 8);
51    
52      /* 捆绑sockfd描述符 */
53    ret = bind(duty_socket, (const struct sockaddr *)&socket_server_addr, sizeof(struct sockaddr));
54    if (ret == -1)
55    {
56        printf("bind error!\n");
57        return -1;
58    }
59    ret = listen(duty_socket, C_QUEUE);
60    if (ret == -1)
61    {
62        printf("listen error!\n");
63        return -1;
64    }
65    
66    while (1)
67    {
68        addr_len = sizeof(struct sockaddr);
69          /* 服务器阻塞,直到客户程序建立连接 */
70        customer_socket = accept(duty_socket, (struct sockaddr *)&socket_client_addr, &addr_len);
71        if (customer_socket != -1)
72        {
73              /*inet_ntoa的作用是将一个32位Ipv4地址转换为相应的点分十进制数串*/
74            printf("Get connect from %s\n", inet_ntoa(socket_client_addr.sin_addr));
75        }
76        if (!fork())
77        {
78            while (1)
79            {
80                memset(buf, 512, 0);
81                  /*接收数据*/
82                len = recv(customer_socket, buf, sizeof(buf), 0);
83                buf[len] = '\0';
84                if (len <= 0)
85                {
86                    close(customer_socket);
87                    return -1;
88                }
89                else
90                {
91                    printf("Get connect from %s, Msg is %s\n", inet_ntoa(socket_client_addr.sin_addr), buf);
92                }
93            }
94        }
95    }
96    
97    close(duty_socket);
98    return 0;
99}
12345678910111213141516171819202122232425262728293031323334353637383940414243444546474849505152535455565758596061626364656667686970717273747576777879808182838485868788899091929394959697
```
- 客户端端：  
	创建套接字(socket)→连接指定计算机的端口(connect)→从socket中读取服务端发送过来的消息(send)→关闭socket(close)
```c
1#include <stdio.h>
2#include <stdlib.h>
3#include <string.h>
4#include <sys/types.h>
5#include <sys/socket.h>
6#include <netinet/in.h>
7#include <arpa/inet.h>
8#include <unistd.h>
9
10#define SERVER_PORT 8180
11/************************************************************
12*函数功能描述：向指定IP的8180端口发送数据
13*输入参数：点分十进制服务器IP
14*输出参数：无
15*返回值：无
18*************************************************************/
19
20int main(int argc, char **argv)
21{
22    unsigned char buf[512];
23    int len;
24    struct sockaddr_in socket_server_addr;
25    int ret;
26    int addr_len;
27    int client_socket;
28
29    
30    if (argc != 2)
31    {
32        printf("Usage:\n");
33        printf("%s <server_ip>\n", argv[0]);
34        return -1;
35    }
36    
37    /* 客户程序开始建立 sockfd描述符 */
38    client_socket = socket(AF_INET, SOCK_STREAM, 0);
39    if (client_socket == -1)
40    {
41        printf("socket error");
42        return -1;
43    }
44    
45      /* 客户程序填充服务端的资料 */
46    socket_server_addr.sin_family   = AF_INET;
47      /*主机字节序转换为网络字节序*/
48    socket_server_addr.sin_port     = htons(SERVER_PORT);
49    if (inet_aton(argv[1], &socket_server_addr.sin_addr) == 0)
50    {
51        printf("invalid server ip\n");
52        return -1;
53    }
54    memset(socket_server_addr.sin_zero, 0, 8);
55    /* 客户程序发起连接请求 */
56    ret = connect(client_socket, (const struct sockaddr *)&socket_server_addr, sizeof(struct sockaddr));
57    if (ret == -1)
58    {
59        printf("connect error!\n");
60        return -1;
61    }
62
63    
64    while (1)
65    {
66        if (fgets(buf, sizeof(buf), stdin))
67        {
68            len = send(client_socket, buf, strlen(buf), 0);
69            if (len <= 0)
70            {
71                close(client_socket);
72                return -1;
73            }
74        }
75    }
76    
77    close(client_socket);
78    return 0;
79}
1234567891011121314151617181920212223242526272829303132333435363738394041424344454647484950515253545556575859606162636465666768697071727374757677
```

### 3\. UDP协议的编程流程

  UDP协议的代码较为简单，在客户端可以沿用TCP中的代码（需要改变socket函数中的type），其大致流程为：  
创建套接字(socket)→将socket与IP地址和端口绑定(bind)→接收信息(recvform)→关闭socket(close)

```c
1#include <stdio.h>
2#include <stdlib.h>
3#include <string.h>
4#include <sys/type.h>
5#include <sys/socket.h>
6#include <netinet/in.h>
7#include <arpa/inet.h>
8#include <unistd.h>
9#include <signal.h>
10
11/*服务器端口为8180*/
12#define SERVER_PORT 8180
13
14/************************************************************
15*函数功能描述：从8180端口接收客户端数据
16*输入参数：无
17*输出参数：打印客户IP以及发来的信息
18*返回值：无
21*************************************************************/
22
23
24int main(int argc, char **argv)
25{
26    unsigned char buf[512];
27    int len;
28    int duty_socket;
29    int customer_socket;
30    struct sockaddr_in socket_server_addr;
31    struct sockaddr_in socket_client_addr;
32    int ret;
33    int addr_len;
34
35      /* 创建数据报套接字 */
36    duty_socket = socket(AF_INET, SOCK_DGRAM, 0);
37    if (duty_socket == -1)
38    {
39        printf("socket error");
40        return -1;
41    }
42    
43      /* 服务器端填充 sockaddr_in结构 */
44    socket_server_addr.sin_family   = AF_INET;
45    socket_server_addr.sin_port     = htons(SERVER_PORT);
46    socket_server_addr.sin_addr.s_addr  = INADDR_ANY;
47    memset(socket_server_addr.sin_zero, 0, 8);
48    
49      /*绑定套接字*/
50    ret = bind(duty_socket, (const struct sockaddr *)&socket_server_addr, sizeof(struct sockaddr));
51    if (ret == -1)
52    {
53        printf("bind error!\n");
54        return -1;
55    }
56
57    
58    while (1)
59    {
60        addr_len = sizeof(struct sockaddr);
61          /* 接收客户端数据报，返回的为接收到的字节数 */ 
62        len = recvfrom(duty_socket, buf, sizeof(buf), 0, (struct sockaddr *)&socket_client_addr, &addr_len);
63        if (len > 0)
64        {
65            buf[len] = '\0';
66            printf("Get Msg from %s : %s\n", inet_ntoa(socket_client_addr.sin_addr), buf);
67        }
68   
69    }
70    
71    close(duty_socket);
72    return 0;
73}
74
123456789101112131415161718192021222324252627282930313233343536373839404142434445464748495051525354555657585960616263646566676869707172
```
```c
1#include <stdio.h>
2#include <stdlib.h>
3#include <string.h>
4#include <sys/socket.h>
5#include <netinet/in.h>
6#include <arpa/inet.h>
7#include <unistd.h>
8
9/*服务器端口为8180*/
10#define SERVER_PORT 8180
11
12/************************************************************
13*函数功能描述：向指定IP的8180端口发送数据
14*输入参数：点分十进制服务器IP
15*输出参数：无
16*返回值：无
19*************************************************************/
20
21int main(int argc, char **argv)
22{
23    unsigned char buf[512];
24    int len;
25    struct sockaddr_in socket_server_addr;
26    int ret;
27    int addr_len;
28    int client_socket;
29
30    
31    if (argc != 2)
32    {
33        printf("Usage:\n");
34        printf("%s <server_ip>\n", argv[0]);
35        return -1;
36    }
37    
38    /*创建数据报套接字*/
39    client_socket = socket(AF_INET, SOCK_DGRAM, 0);
40    if (client_socket == -1)
41    {
42        printf("socket error");
43        return -1;
44    }
45    
46    socket_server_addr.sin_family   = AF_INET;
47    socket_server_addr.sin_port     = htons(SERVER_PORT);
48    if (inet_aton(argv[1], &socket_server_addr.sin_addr) == 0)
49    {
50        printf("invalid server ip\n");
51        return -1;
52    }
53    memset(socket_server_addr.sin_zero, 0, 8);
54    
55    ret = connect(client_socket, (const struct sockaddr *)&socket_server_addr, sizeof(struct sockaddr));
56    if (ret == -1)
57    {
58        printf("connect error!\n");
59        return -1;
60    }
61
62    
63    while (1)
64    {
65        if (fgets(buf, sizeof(buf), stdin))
66        {
67            len = send(client_socket, buf, strlen(buf), 0);
68            if (len <= 0)
69            {
70                close(client_socket);
71                return -1;
72            }
73        }
74    }
75    
76    close(client_socket);
77    return 0;
78}
79
1234567891011121314151617181920212223242526272829303132333435363738394041424344454647484950515253545556575859606162636465666768697071727374757677
```

**注：本实验基于韦东山老师的公开资料若有侵权请联系作者删除。**

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/137271995

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