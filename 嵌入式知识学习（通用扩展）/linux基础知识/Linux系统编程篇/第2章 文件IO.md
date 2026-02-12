---
title: "【北京迅为】《iTOP-3588开发板系统编程手册》第2章 文件IO"
source: "https://blog.csdn.net/BeiJingXunWei/article/details/137345732"
author:
  - "[[BeiJingXunWei]]"
published: 2024-04-03
created: 2025-09-11
description: "文章浏览阅读861次，点赞29次，收藏25次。RK3588是一款低功耗、高性能的处理器，适用于基于arm的PC和Edge计算设备、个人移动互联网设备等数字多媒体应用，RK3588支持8K视频编解码，内置GPU可以完全兼容OpenGLES 1.1、2.0和3.2。RK3588引入了新一代完全基于硬件的最大4800万像素ISP，内置NPU，支持INT4/INT8/INT16/FP16混合运算能力，支持安卓12和、Debian11、Build root、Ubuntu20和22版本登系统。了解更多信息可点击【粉丝群】824412014。_itop3588"
tags:
  - "clippings"
---


在第一章对系统编程进行了初步了解之后，本章给大家介绍 Linux 应用编程中最基础的知识“文件I/O（Input、Outout）”即文件的读写操作。我们之后要编写的应用程序都离不开对文件的读写，所以文件的I/O 操作是系统编程最基础也是最重要的部分。

在Linux哲学中有一点贯穿了Linux系统，那就是“一切皆文件”，Linux将每个文件或目录都视为一个对象（ 除了常规的文件和目录之外，Linux还将硬件设备、网络套接字、管道、进程、共享内存等抽象概念表示为文件 ），并通过文件描述符（File Descriptor）来引用它们。本章节会在第1小节对文件描述符进行介绍，在之后的小节中会对一些常用的系统调用进行介绍。并在章节末通过一个综合练习，对学到的内容进行巩固。

### 2.1文件描述符

****学习前的疑问**** ****：****

1. 什么是文件描述符？
2. 文件描述符的作用是什么？
3. 文件描述符是怎样进行使用的？

在Linux系统中， 文件描述符（File Descriptor）是一种用于引用已打开文件、设备、管道、套接字等I/O资源的机制 。每当打开一个文件或设备时，Linux内核会为该文件分配一个文件描述符，用于之后对该文件的访问和操作。

文件描述符使用C语言的int类型来表示。打开文件会占用一定的内存资源，所以每个Linux进程打开文件的个数是有上限的，文件描述符从0开始，默认最大数量为1024个，即取值范围为0-1023，如果超过进程可打开的最大文件数，内核将会发送警告信号给对应的进程，然后结束进程。

文件描述符的使用可以概括为以下几个方面：

1）打开文件：在Linux中，可以使用open()系统调用打开一个文件，该系统调用返回一个文件描述符，该文件描述符唯一地标识该文件，同时也可以用于访问和操作该文件。

2）读写文件：一旦文件已经打开，可以使用read()和write()等系统调用读取和写入文件的内容。这些系统调用需要一个文件描述符作为参数，以指定要读取或写入的文件。

3）关闭文件：在不再需要使用文件时，应该使用close()系统调用来关闭文件描述符，这样可以释放文件描述符所占用的系统资源。

在Linux系统中，系统预定义了三个标准的文件描述符：stdin（标准输入0）、stdout（标准输出1）和stderr（标准错误输出2）。一般情况下，标准输入0对应终端的输入设备（通常是用户的键盘），标准输出1和标准错误2对应终端输出设备（通常指的是 LCD 显示器）。

文件描述符是一个非常重要的概念，它是Linux系统中访问和操作I/O资源的基础机制。开发人员需要深入理解文件描述符的概念和使用方法，以便更好地编写可靠、高效的Linux应用程序。

### 2.2打开文件

本小节代码在配套资料“ iTOP-3588开发板\\03\_【iTOP-RK3588开发板】指南教程\\03\_系统编程配套程序 \\02 ”目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/a6e50043a5540b1c1754623c1c614997\_MD5.png](assets/第2章%20文件IO/a6e50043a5540b1c1754623c1c614997_MD5.png)

****学习前的疑问：****

1. 打开文件要使用哪个系统调用API？
2. open 函数要怎样进行使用？

在Linux系统中，open()是一个非常重要的系统调用，其作用是打开一个文件，并返回该文件对应的文件描述符（File Descriptor）。关于文件描述符已经在上一小节进行了介绍，通过文件描述符，可以实现读取、写入和修改文件等操作。

open()函数所使用的头文件和函数原型，如下所示：

|  | 所需头文件 | 函数原型 |
| --- | --- | --- |
| 1  2  3 | #include <sys/types.h>  #include <sys/stat.h>  #include <fcntl.h> | int open **(**const char **\*** pathname**,**int flags**);**  int open **(**const char **\*** pathname**,**int flags**,** mode\_t mode**);** |

open()函数执行成功之后会返回的int型文件描述符，出错时返回-1，并设置error值（关于error值在之后的小节会进行讲解）。

open()函数三个参数含义如下所示：

|  | 参数名称 | 参数含义 |
| --- | --- | --- |
| 1 | pathname参数 | 用于标识需要打开或创建的文件路径和文件名。 |
| 2 | flags参数 | 用于指定文件打开方式，可以使用按位或设置多个标志位。 |
| 3 | mode参数 | 用于指定文件的访问权限，即文件的读、写、执行权限等。 |

常用的flags标志位参数分为主参数和副参数，主参数有三个分别为O\_RDONLY、O\_WRONLY、O\_RDWR，三个主参数在使用的时候只能使用一个（即为互斥关系），具体用途如下图所示：

| 标志 | 用途 |
| --- | --- |
| O\_RDONLY | 只读模式打开文件 |
| O\_WRONLY | 只写模式打开文件 |
| O\_RDWR | 可读可写模式打开文件 |

副参数有很多，可以使用“|”符号与主参数进行同时使用（ 副参数没有互斥关系，可以多个同时使用 ），副参数的具体用途如下图所示：

| 标志 | 用途 |
| --- | --- |
| O\_CREAT | 要打开的文件名不存在时自动创建改文件。 |
| O\_EXCL | 要和O\_CREAT一起使用才能生效，如果文件存在则open()调用失败。 |
| O\_APPEND | 以追加模式打开文件 |
| O\_NONBLOCK | 以非阻塞模式打开 |
| O\_DIRECT | 直接IO |
| O\_SYNC | 同步IO |
| O\_ASYNC | 用于终端式套接字，指定文件读写时产生的信号 |
| O\_TRUNC | 若文件存在，则将长度截为0 |

****mode:**** 权限掩码，对不同用户和组设置可执行、读、写权限，使用八进制数表示，此参数可不写。只有当 flags 参数中包含 O\_CREAT 或 O\_TMPFILE 标志时才有效（O\_TMPFILE 标志用于创建一个临时文件）mode的参数类型为mode\_t，是一个32位的无符号整形数据，使用低12位每三位一组来进行权限的表示。

1-3位表示O---用于表示其他用户的权限；

4-6位表示G---用于表示同组用户（group）的权限，即与文件所有者有相同组 ID 的所有用户；

7-9位表示U---用于表示文件所属用户的权限，即文件或目录的所属者；

10-12位表示S---用于表示文件的特殊权限，一般情况下用不到(设置为0)。

对应的权限表格如下所示：

| 字母 | 权限 | 二进制 | 十进制 |
| --- | --- | --- | --- |
| r | 读权限 | 100 | 4 |
| w | 写权限 | 010 | 2 |
| x | 执行权限 | 001 | 1 |

至此关于open()函数的相关讲解就完成了，下面进行相应的实验。

****实验要求：****

通过系统调用open()函数，创建一个可读可写名称为test的文件，并打印其文件描述符。

****实验步骤：****

首先进入到 ubuntu 的终端界面输入以下命令来创建demo02\_open.c文件，如下图所示：

> vim demo02\_open.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/a4aa329921c6bf5d4b63dc129846838c\_MD5.png](assets/第2章%20文件IO/a4aa329921c6bf5d4b63dc129846838c_MD5.png)

然后向该文件中添加以下内容：

```cpp
#include <sys/types.h>

#include <sys/stat.h>

#include <fcntl.h>

#include <stdio.h>

 

int main() 

{

    int fd = open("test", O_RDWR | O_CREAT, 0666); 

    if (fd < 0) //对open函数返回的文件描述符进行判断

    {

        perror("open file error \n");

        return -1;

    }

    printf("fd = %d\n", fd);

    return 0;

}
cpp
```

调在上述代码中，我们使用open()函数创建了一个名为test的文件，并指定了O\_RDWR和O\_CREAT标志，表示文件可读可写并且在文件不存在时创建它。此外，我们还使用了0666权限位来设置文件的读、写和执行权限，这意味着所有用户都可以读取和写入该文件。

保存退出之后，使用以下命令对demo02\_open.c进行编译，编译完成如下图所示：

> gcc -o demo02\_open demo02\_open.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/a4f6d07e973e3208a0ae93b806142987\_MD5.png](assets/第2章%20文件IO/a4f6d07e973e3208a0ae93b806142987_MD5.png) 可以看到当前文件夹中并没有test文件，然后使用命令“./demo02\_open”来运行，运行成功如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/996fafc484346bda133c71f8908b5be1\_MD5.png](assets/第2章%20文件IO/996fafc484346bda133c71f8908b5be1_MD5.png)

可以看到程序运行成功之后，打印的文件描述符为3，在2.1小节中也讲解过在一个进程中至少包含三个文件描述符，0表示标准输入stdin，1表示标准输出stdout，2表示标准错误stderr，所以分配的文件描述符一般都是从 3 开始，然后使用“ls”命令查看当前文件夹的文件信息，可以看到test文件已经被创建成功了。

至此，关于open()函数的实验就完成了。

### 2.3关闭文件

在上一小节中学习了open()函数用来打开文件，那有没有系统调用用来关闭文件呢，答案是肯定的，将在本小节讲解关闭文件。

本小节代码在配套资料“ iTOP-3588开发板\\03\_【iTOP-RK3588开发板】指南教程\\03\_系统编程配套程序 \\ 03 ”目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/847a589955a9935f514a9d1d49f7645d\_MD5.png](assets/第2章%20文件IO/847a589955a9935f514a9d1d49f7645d_MD5.png)

****学习前的疑问：****

1. 关闭文件要使用哪个系统调用API？
2. close()函数要怎样进行使用？

上面的描述其实并不准确，本小节要讲解的close()函数的功能是关闭一个打开的文件描述符，并不是关闭文件。在程序打开一个文件之后，操作系统会为该文件分配一个文件描述符，通过该文件描述符我们可以对文件进行读写等操作。当不再需要访问该文件时，应该及时关闭文件描述符以释放系统资源。

close()函数所使用的头文件和函数原型，如下所示：

|  | 参数名称 | 参数含义 |
| --- | --- | --- |
| 1 | fd参数 | 参数fd是一个打开的文件描述符 |

至此关于close()函数的相关讲解就完成了，下面进行相应的实验。

****实验要求：****

在同一目录下创建并打开一个可读可写“test”，打印文件描述符后关闭文件。

****实验步骤：****

首先进入到ubuntu的终端界面输入以下命令来创建demo03\_close.c文件，如下图所示：

> vim demo03\_close.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/4c5d7c27605c5bbe060160bcb10308f5\_MD5.png](assets/第2章%20文件IO/4c5d7c27605c5bbe060160bcb10308f5_MD5.png) 然后向该文件中添加以下内容：

```cpp
#include <stdio.h>

#include <sys/types.h>

#include <sys/stat.h>

#include <fcntl.h>

#include<unistd.h>

 

int main() 

{

    int fd = open("test", O_RDWR | O_CREAT, 0666); 

    if (fd < 0) //对open函数返回的文件描述符进行判断

    {

        perror("open file error \n");

        return -1;

    }

    printf("fd = %d\n", fd);

    close(fd);

    return 0;

}
cpp
```

和2.2小节代码相比，只是加入了16行的close()函数，保存退出之后，使用以下命令对demo03\_close.c进行编译，编译完成如下图所示：

> gcc -o demo03\_close demo03\_close.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/2d6c969b3b70dd03e4693c285e4cc8c0\_MD5.png](assets/第2章%20文件IO/2d6c969b3b70dd03e4693c285e4cc8c0_MD5.png) 然后使用命令“./demo03\_close ”来运行，运行成功如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/c4c0a6966a3412ac4d49b7d08839f0ac\_MD5.png](assets/第2章%20文件IO/c4c0a6966a3412ac4d49b7d08839f0ac_MD5.png)

可以看到实验现象和上一小节相同，其中close()函数的作用只是关闭已经打开的文件描述符，释放系统资源。

至此关于close函数的实验就完成了。

### 2.4读文件

学习了打开文件和关闭文件相关的系统调用函数之后，下面就轮到读取文件和写入文件的API函数讲解了。在本小节将进行读文件read()函数的讲解。

本小节代码在配套资料“ iTOP-3588开发板\\03\_【iTOP-RK3588开发板】指南教程\\03\_系统编程配套程序 \\ 04 ”目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/9aa566e846423adfec819ba33533320b\_MD5.png](assets/第2章%20文件IO/9aa566e846423adfec819ba33533320b_MD5.png)

****学习前的疑问：****

1.读取文件要使用哪个系统调用API？

2.read()函数要怎样进行使用？

read()函数用于对文件或者设备进行读取，函数功能较为单一，所使用的头文件和函数原型，如下所示：

|  | 所需头文件 | 函数原型 |
| --- | --- | --- |
| 1 | #include <unistd.h> | ssize\_t read **(**int fd**,**void **\*** buf**,**size\_t count**);** |

返回值大于0，表示读取到的字节数；等于0在阻塞模式下表示到达文件末尾或没有数据可读（EOF），并调用阻塞；等于-1表示出错，并设置error值（关于error值在之后的小节会进行讲解）。在非阻塞模式下表示没有数据可读。

read()函数三个参数含义如下所示：

|  | 参数名称 | 参数含义 |
| --- | --- | --- |
| 1 | fd参数 | 文件描述符 |
| 2 | buf参数 | 存储读取数据的缓冲区 |
| 3 | count参数 | 读取的字节数 |

至此关于read()函数的相关讲解就完成了，下面进行相应的实验。

****实验要求：****

读取test文件中的内容，并对文件内容和返回值字节数进行打印。

****实验步骤：****

首先进入到ubuntu的终端界面输入以下命令来创建demo04\_read.c文件，如下图所示：

> vim demo04\_read.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/f773ae4eed9c1cfba0f7c249bea6d93e\_MD5.png](assets/第2章%20文件IO/f773ae4eed9c1cfba0f7c249bea6d93e_MD5.png) 然后向该文件中添加以下内容：

```cpp
#include <stdio.h>

#include <stdlib.h>

#include <sys/types.h>

#include <sys/stat.h>

#include <fcntl.h>

#include <unistd.h>

 

int main(int argc, char *argv[])

{

    int fd; // 定义文件描述符

    char buf[32] = {0}; // 定义缓冲区，用于存储读取到的数据

    ssize_t ret; // 定义读取到的字节数

 

    // 以 O_CREAT | O_RDWR 的方式打开文件，权限为 0666，如果文件不存在则创建

    fd = open("test", O_CREAT | O_RDWR, 0666);

if (fd < 0) // 打开文件失败

{ 

        perror("open is error\n"); // 输出错误信息

        return -1; // 返回错误码 -1

    }

 

    printf("fd is %d\n", fd); // 输出文件描述符

 

    // 读取文件内容到缓冲区中，最多读取 32 个字节

    ret = read(fd, buf, 32);

if (ret < 0) // 读取文件失败

{ 

        perror("read is error\n"); // 输出错误信息

        return -2; // 返回错误码 -2

    }

 

    printf("buf is %s\n", buf); // 输出读取到的内容

    printf("ret is %ld\n", ret); // 输出读取到的字节数

 

    close(fd); // 关闭文件

    return 0; // 返回正常退出码 0

}
cpp
```

上述代码在2.3小节实验的基础上，加入了第25行的read()函数，对test文件进行读取，读到的数据被保存在创建的缓冲区buf\[32\]中,读取字节数为32,返回值为ret，如果read函数调用成功，会返回读取到的字节数。

保存退出之后，使用以下命令对demo04\_read.c进行编译，编译完成如下图所示：

> gcc -o demo04\_read demo04\_read.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/13ca892a2042b8030a4a9c6d98b7dda3\_MD5.png](assets/第2章%20文件IO/13ca892a2042b8030a4a9c6d98b7dda3_MD5.png) 然后直接使用命令“./demo04\_read ”来运行，运行成功如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/f0dc717c09843818f5f8c2053bc7a07b\_MD5.png](assets/第2章%20文件IO/f0dc717c09843818f5f8c2053bc7a07b_MD5.png) 由于test文件是我们刚刚创建的，文件内容为空，所以buf为空，ret为0，接下来对test文件进行编辑，添加完成如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/9547c3b3d6f0e818b5ed38cbb271bc3e\_MD5.png](assets/第2章%20文件IO/9547c3b3d6f0e818b5ed38cbb271bc3e_MD5.png) 保存退出之后，然后再使用命令“./demo04\_read ”来运行，运行成功如下图所示，成功读取到test文件中的hello world！！，返回的字节数为14。

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/8843bc3239ee246c6bf3997167da9fa2\_MD5.png](assets/第2章%20文件IO/8843bc3239ee246c6bf3997167da9fa2_MD5.png)

至此，关于read()函数的相关实验就完成了。

### 2.5写文件

在上一小节讲解了系统编程中的读文件函数，在本小节将对写文件函数进行讲解。

本小节代码在配套资料“ iTOP-3588开发板\\03\_【iTOP-RK3588开发板】指南教程\\03\_系统编程配套程序 \\05 ”目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/eb1aa37c9d0a9a8e1cb67324f45c8c1d\_MD5.png](assets/第2章%20文件IO/eb1aa37c9d0a9a8e1cb67324f45c8c1d_MD5.png)

****学习前的疑问：****

1.写入文件要使用哪个系统调用API？

2.write()函数要怎样进行使用？

write()函数用于对文件或者设备进行数据写入，函数功能较为单一，所使用的头文件和函数原型，如下所示：

|  | 所需头文件 | 函数原型 |
| --- | --- | --- |
| 1 | #include <unistd.h> | ssize\_t write **(**int fd**,**const void **\*** buf**,**size\_t count**);** |

大于或等于0表示执行成功，返回写入的字节数，返回-1代表出错，并设置error值（关于error值在之后的小节会进行讲解）。

write()函数三个参数含义如下所示：

|  | 参数名称 | 参数含义 |
| --- | --- | --- |
| 1 | fd参数 | 文件描述符 |
| 2 | buf参数 | 写入数据的缓冲区 |
| 3 | count参数 | 写入的字节数 |

至此关于write()函数的相关讲解就完成了，下面进行相应的实验。

****实验1：****

****实验要求：****

将“hello”打印到输出设备上（即将写入的文件描述符设置为1）

****实验步骤：****

首先进入到ubuntu的终端界面输入以下命令来创建demo05\_write\_01.c文件，如下图所示：

> vim demo05\_write\_01.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/0f06669b69c919af5bc26891d71980d8\_MD5.png](assets/第2章%20文件IO/0f06669b69c919af5bc26891d71980d8_MD5.png)

向该文件中添加以下内容

```cpp
#include <stdio.h>

#include <unistd.h>

 

int main(int argc, char *argv[])

{

    char buf[32] = {"hello\n"}; // 定义缓冲区，存放要写入的数据

    ssize_t ret; // 定义写入的字节数

 

    ret = write(1, buf, 6); // 将 buf 中的前 6 个字节写入到标准输出（屏幕）中

    printf("ret = %ld\n", ret); // 输出写入的字节数

    return 0; // 返回正常退出码 0

}
cpp
```

上述内容的9行调用了write()函数，设备描述符参数被设置为了 1 ，1代表标准输出（在这里为显示屏终端），第二个参数为要写入的字符串，而最后一个参数表示写入数据字节数为6。

保存退出之后，使用以下命令对demo05\_write\_01.c进行编译，编译完成如下图所示：

> gcc -o demo05\_write\_01 demo05\_write\_01.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/074ee7624f9753a1f96482f5e6e904a0\_MD5.png](assets/第2章%20文件IO/074ee7624f9753a1f96482f5e6e904a0_MD5.png) 然后使用命令“./demo05\_write\_01 ”来运行，运行成功如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/1c7bdc977cab834d356c6086036a8e9b\_MD5.png](assets/第2章%20文件IO/1c7bdc977cab834d356c6086036a8e9b_MD5.png)

可以看到“hello”就被输出到了终端界面。

****实验2：****

****实验要求：****

创建一个可读可写的文件名称为“test”的文件，并将“hello”字符串内容写入到test文件中。

****实验步骤：****

首先进入到ubuntu的终端界面输入以下命令来创建demo05\_write\_02.c文件，如下图所示：

> vim demo05\_write\_02.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/c533f8fc3b1f4ed846b5a5bf8442ece2\_MD5.png](assets/第2章%20文件IO/c533f8fc3b1f4ed846b5a5bf8442ece2_MD5.png) 向该文件中添加以下内容：

```cpp
#include <stdio.h>

#include <stdlib.h>

#include <sys/types.h>

#include <sys/stat.h>

#include <fcntl.h>

#include <unistd.h>

 

int main(int argc, char *argv[])

{

    int fd; // 定义文件描述符

    char buf[32] = {"hello\n"}; // 定义缓冲区，存放要写入的数据

    ssize_t ret; // 定义写入的字节数

 

    fd = open("test", O_CREAT|O_RDWR, 0666); // 打开或创建一个名为 test 的文件，并返回其文件描述符

    if (fd < 0) // 打开或创建文件失败

    {

        perror("open is error\n"); // 输出错误信息

        return -1; // 返回错误码

    }

 

    write(fd, buf, 6); // 将 buf 中的前 6 个字节写入到 test 文件中

    close(fd); // 关闭文件

    return 0; // 返回正常退出码 0

}
cpp
```

相较于实验1，write()函数的文件描述符参数从标准输出1更换为了test文件的文件描述符fd，函数执行后字符就会写入test文件。

保存退出之后，使用以下命令对demo05\_write\_02.c进行编译，编译完成如下图所示：

> gcc -o demo05\_write\_02 demo05\_write\_02.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/6028f58a0908cff87fad6b9d3028eb79\_MD5.png](assets/第2章%20文件IO/6028f58a0908cff87fad6b9d3028eb79_MD5.png) 然后使用命令“./demo05\_write\_02 ”来运行，运行成功如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/fc759c31eb6b91e8361832e4f574f91d\_MD5.png](assets/第2章%20文件IO/fc759c31eb6b91e8361832e4f574f91d_MD5.png)

程序运行成功之后，test文件被创建，然后使用cat命令对文件内容进行查看，可以看到“hello”已经被写入了。

至此，关于write()函数的实验就结束了。

### 2.6 lseek

文件读写指针是一个指针变量，它用于标识文件读写时的当前位置。在进行文件读写操作时，文件读写指针会随着读写操作的进行而移动。使用open()函数打开一个文件时读写指针默认在文件头，那如果想要读取文件尾的数据要怎样做呢，这时候就轮到lseek函数出场了（ 当然lseek的功能不仅仅有读取文件尾的数据 ）。

本小节代码在配套资料“ iTOP-3588开发板\\03\_【iTOP-RK3588开发板】指南教程\\03\_系统编程配套程序 \\06 ”目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/7feb0bea4c197df7e58d9cae3ab66380\_MD5.png](assets/第2章%20文件IO/7feb0bea4c197df7e58d9cae3ab66380_MD5.png)

****学习前的疑问：****

1.控制文件读写指针位置要使用哪个系统调用API呢？

2.lseek函数要怎样进行使用？

lseek() 用于设置文件指针位置。所使用的头文件和函数原型，如下所示：

|  | 所需头文件 | 函数原型 |
| --- | --- | --- |
| 1  2 | #include <sys/types.h>  #include <unistd.h> | off\_t lseek **(**int fd**,** off\_t offset**,**int whence**);** |

lseek()函数执行成功会返回当前位移大小，失败返回-1，并设置error值（关于error值在之后的小节会进行讲解）。

lseek()函数三个参数含义如下所示：

|  | 参数名称 | 参数含义 |
| --- | --- | --- |
| 1 | fd参数 | 文件描述符 |
| 2 | off\_t offset参数 | 偏移量，单位是字节的数量，可以正负，如果是负值表示向前移动；如果是正值，表示向后移动 |
| 3 | whence参数 | 当前位置的基点，可以使用以下三组值:  SEEK\_SET：相对于文件开头  SEEK\_CUR:相对于当前的文件读写指针位置  SEEK\_END:相对于文件末尾 |

****案例：****

1. 把文件位置指针设置为5 lseek(fd,5,SEEK\_SET);
2. 把文件位置设置成文件末尾 lseek(fd,0,SEEK\_END);
3. 确定当前的文件位置 lseek(fd,0,SEEK\_CUR);

至此关于lseek()函数的相关讲解就完成了，下面进行相应的实验。

****实验**** ****要求**** ****：****

对比使用lseek函数使用前后，read()函数返回值的变化。

****实验步骤：****

首先进入到ubuntu的终端界面输入以下命令来创建test文件，如下图所示：

> vim test

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/717bed8690932e41ef2b6460a32fa520\_MD5.png](assets/第2章%20文件IO/717bed8690932e41ef2b6460a32fa520_MD5.png) 然后向test文件中写入以下内容，写入完成如下图所示：

保存退出，输入以下命令来创建demo06\_lseek.c文件，如下图所示：

> vim demo06\_lseek.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/eaf41dac816ecba5f0ab82aa695faa9e\_MD5.png](assets/第2章%20文件IO/eaf41dac816ecba5f0ab82aa695faa9e_MD5.png) 然后向该文件中添加以下内容

```cpp
#include <stdio.h>

#include <stdlib.h>

#include <sys/types.h>

#include <sys/stat.h>

#include <fcntl.h>

#include <unistd.h>

 

int main(int argc, char *argv[])

{

    int fd;                         // 文件描述符

    char buf[32] = {0};             // 读写缓冲区

    ssize_t ret;                    // read() 返回值类型，代表读取的字节数

 

    fd = open("test", O_CREAT | O_RDWR, 0666); // 打开文件 "test"，如果不存在则创建该文件，同时以读写方式打开

    if (fd < 0)                     // 如果文件打开失败

    {

        perror("open is error\n");  // 打印错误信息

        return -1;                  // 退出程序

    }

 

    ret = read(fd, buf, 32);        // 从文件中读取最多 32 个字节到 buf 中

    if (ret < 0)                    // 如果读取失败

    {

        perror("read is error\n");  // 打印错误信息

        return -2;                  // 退出程序

    }

    printf("buf is %s\n", buf);     // 打印读取到的字符串

    printf("ret is %ld\n", ret);    // 打印读取到的字节数

 

    lseek(fd, 5, SEEK_SET);         // 将文件指针移动到偏移量为 5 的位置，从文件开头计算偏移量

    ret = read(fd, buf, 32);        // 再次从文件中读取最多 32 个字节到 buf 中

    printf("buf is %s\n", buf);     // 打印读取到的字符串

    printf("ret is %ld\n", ret);    // 打印读取到的字节数

 

    close(fd);                      // 关闭文件

    return 0;                       // 程序正常结束

}
cpp
```

22行和33行都使用了read()函数对test文件进行读取，不同的是在31行使用了lseek函数将读写指针以文件头为参照向后移动了5个字节。

保存退出之后，使用以下命令对demo06\_lseek.c进行编译，编译完成如下图所示：

> gcc -o demo06\_lseek demo06\_lseek.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/d4fdd0c05edb0ec108a737efc2c8ebe4\_MD5.png](assets/第2章%20文件IO/d4fdd0c05edb0ec108a737efc2c8ebe4_MD5.png) 然后使用命令“./demo06\_lseek ”来运行，运行成功如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/f4920130cbb382dbb85060eda4eef34c\_MD5.png](assets/第2章%20文件IO/f4920130cbb382dbb85060eda4eef34c_MD5.png) 可以看到程序运行成功之后，会将test文件中的内容打印出来，且第一次返回的字符数量为15，在使用lseek进行字符偏移5之后，就只会打印test文件中hello之后的部分，返回的字符数量变为了10。

至此关于lseek函数的实验就完成了。

### 2.7综合练习（一）

本小节代码在配套资料“ iTOP-3588开发板\\03\_【iTOP-RK3588开发板】指南教程\\03\_系统编程配套程序 \\ 07 ”目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/2d2a4342df05f6fed56a9c8941bd0d5a\_MD5.png](assets/第2章%20文件IO/2d2a4342df05f6fed56a9c8941bd0d5a_MD5.png)

****实验要求****

实现文件的拷贝，通过demo7\_test可执行程序，将把文件1中的内容写到2中，具体格式如下：

demo7\_test 源文件 目标文件

****实验代码****

```cpp
#include <stdio.h>

#include <stdlib.h>

#include <sys/types.h>

#include <sys/stat.h>

#include <fcntl.h>

#include <unistd.h>

 

int main(int argc, char *argv[])

{

    // 步骤一：判断命令行的参数

    if (argc != 3)

    {

        printf("Usage:%s <src file> <obj file>\n", argv[0]);

        return -1; // 如果命令行参数不正确，则退出程序

    }

 

    // 步骤二：定义变量

    int fd_src, fd_obj;             // 源文件和目标文件的文件描述符

    char buf[32] = {0};             // 读写缓冲区

    ssize_t ret;                    // read() 返回值类型，代表读取的字节数

 

    // 步骤三：打开文件获得文件描述符

    fd_src = open(argv[1], O_RDWR); // 以读写方式打开源文件

    if (fd_src < 0)                 // 如果打开源文件失败

    {

        perror("open is error\n");  // 打印错误信息

        return -2;                  // 退出程序

    }

    fd_obj = open(argv[2], O_CREAT | O_RDWR, 0666); // 创建目标文件，如果不存在则创建，以读写方式打开

    if (fd_obj < 0)                 // 如果打开目标文件失败

    {

        perror("open is error\n");  // 打印错误信息

        return -3;                  // 退出程序

    }

 

    // 步骤四：读写操作

    while ((ret = read(fd_src, buf, 32)) != 0) // 反复从源文件读取数据到缓冲区中

    {

        write(fd_obj, buf, ret);    // 将缓冲区中的数据写入目标文件

    }

 

    // 步骤五：关闭文件描述符

    close(fd_src);                  // 关闭源文件

    close(fd_obj);                  // 关闭目标文件

 

    return 0;                       // 程序正常结束

}
cpp
```

保存退出之后，使用以下命令对demo7\_test.c进行编译，编译完成如下图所示：

> gcc -o demo7\_test demo7\_test.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/a73c767b21d130a70a1077e371985e90\_MD5.png](assets/第2章%20文件IO/a73c767b21d130a70a1077e371985e90_MD5.png)

进入到ubuntu的终端界面输入以下命令来创建test文件，如下图所示：

> vim test

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/bfdc252d499ebe71e7e6215d08310983\_MD5.png](assets/第2章%20文件IO/bfdc252d499ebe71e7e6215d08310983_MD5.png) 然后向test文件中写入以下内容，写入完成如下图所示：

保存退出，然后使用命令“./demo7\_test test test1 ”，将test中的内容复制到test1中，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/d15ff0894667aae90b359d7b3770c27f\_MD5.png](assets/第2章%20文件IO/d15ff0894667aae90b359d7b3770c27f_MD5.png)

可以看到test1文件已经被成功创建了。然后使用“ cat test1 ”命令来查看test1文件内容可以看到test源文件的内容已经被成功复制了。

至此关于第二章节的练习就结束了。

微信公众号

内容来源：csdn.net

作者昵称：北京迅为

原文链接：https://blog.csdn.net/BeiJingXunWei/article/details/137345732

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

隐藏侧栏 ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/90bd0cbf3aff8fdff8bf9b011b581e20\_MD5.png](assets/第2章%20文件IO/90bd0cbf3aff8fdff8bf9b011b581e20_MD5.png)

程序员都在用的中文IT技术交流社区

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/08a47e60886378fe60a3d9c8f4ae8bc6\_MD5.png](assets/第2章%20文件IO/08a47e60886378fe60a3d9c8f4ae8bc6_MD5.png)

专业的中文 IT 技术社区，与千万技术人共成长

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/a51be6c085b867a5bd82d8dc1cea9b46\_MD5.png](assets/第2章%20文件IO/a51be6c085b867a5bd82d8dc1cea9b46_MD5.png)

关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！

客服 返回顶部

微信公众号

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/efb7921311640694e61fee00900550d6\_MD5.jpg](assets/第2章%20文件IO/efb7921311640694e61fee00900550d6_MD5.jpg) 公众号名称：迅为电子 微信扫码关注或搜索公众号名称

复制公众号名称

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/a6e50043a5540b1c1754623c1c614997\_MD5.png](assets/第2章%20文件IO/a6e50043a5540b1c1754623c1c614997_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/a4aa329921c6bf5d4b63dc129846838c\_MD5.png](assets/第2章%20文件IO/a4aa329921c6bf5d4b63dc129846838c_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/a4f6d07e973e3208a0ae93b806142987\_MD5.png](assets/第2章%20文件IO/a4f6d07e973e3208a0ae93b806142987_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/996fafc484346bda133c71f8908b5be1\_MD5.png](assets/第2章%20文件IO/996fafc484346bda133c71f8908b5be1_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/847a589955a9935f514a9d1d49f7645d\_MD5.png](assets/第2章%20文件IO/847a589955a9935f514a9d1d49f7645d_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/4c5d7c27605c5bbe060160bcb10308f5\_MD5.png](assets/第2章%20文件IO/4c5d7c27605c5bbe060160bcb10308f5_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/2d6c969b3b70dd03e4693c285e4cc8c0\_MD5.png](assets/第2章%20文件IO/2d6c969b3b70dd03e4693c285e4cc8c0_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/c4c0a6966a3412ac4d49b7d08839f0ac\_MD5.png](assets/第2章%20文件IO/c4c0a6966a3412ac4d49b7d08839f0ac_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/9aa566e846423adfec819ba33533320b\_MD5.png](assets/第2章%20文件IO/9aa566e846423adfec819ba33533320b_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/f773ae4eed9c1cfba0f7c249bea6d93e\_MD5.png](assets/第2章%20文件IO/f773ae4eed9c1cfba0f7c249bea6d93e_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/13ca892a2042b8030a4a9c6d98b7dda3\_MD5.png](assets/第2章%20文件IO/13ca892a2042b8030a4a9c6d98b7dda3_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/f0dc717c09843818f5f8c2053bc7a07b\_MD5.png](assets/第2章%20文件IO/f0dc717c09843818f5f8c2053bc7a07b_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/9547c3b3d6f0e818b5ed38cbb271bc3e\_MD5.png](assets/第2章%20文件IO/9547c3b3d6f0e818b5ed38cbb271bc3e_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/8843bc3239ee246c6bf3997167da9fa2\_MD5.png](assets/第2章%20文件IO/8843bc3239ee246c6bf3997167da9fa2_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/eb1aa37c9d0a9a8e1cb67324f45c8c1d\_MD5.png](assets/第2章%20文件IO/eb1aa37c9d0a9a8e1cb67324f45c8c1d_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/0f06669b69c919af5bc26891d71980d8\_MD5.png](assets/第2章%20文件IO/0f06669b69c919af5bc26891d71980d8_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/074ee7624f9753a1f96482f5e6e904a0\_MD5.png](assets/第2章%20文件IO/074ee7624f9753a1f96482f5e6e904a0_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/1c7bdc977cab834d356c6086036a8e9b\_MD5.png](assets/第2章%20文件IO/1c7bdc977cab834d356c6086036a8e9b_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/c533f8fc3b1f4ed846b5a5bf8442ece2\_MD5.png](assets/第2章%20文件IO/c533f8fc3b1f4ed846b5a5bf8442ece2_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/6028f58a0908cff87fad6b9d3028eb79\_MD5.png](assets/第2章%20文件IO/6028f58a0908cff87fad6b9d3028eb79_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/fc759c31eb6b91e8361832e4f574f91d\_MD5.png](assets/第2章%20文件IO/fc759c31eb6b91e8361832e4f574f91d_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/7feb0bea4c197df7e58d9cae3ab66380\_MD5.png](assets/第2章%20文件IO/7feb0bea4c197df7e58d9cae3ab66380_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/717bed8690932e41ef2b6460a32fa520\_MD5.png](assets/第2章%20文件IO/717bed8690932e41ef2b6460a32fa520_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/eaf41dac816ecba5f0ab82aa695faa9e\_MD5.png](assets/第2章%20文件IO/eaf41dac816ecba5f0ab82aa695faa9e_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/d4fdd0c05edb0ec108a737efc2c8ebe4\_MD5.png](assets/第2章%20文件IO/d4fdd0c05edb0ec108a737efc2c8ebe4_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/f4920130cbb382dbb85060eda4eef34c\_MD5.png](assets/第2章%20文件IO/f4920130cbb382dbb85060eda4eef34c_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/2d2a4342df05f6fed56a9c8941bd0d5a\_MD5.png](assets/第2章%20文件IO/2d2a4342df05f6fed56a9c8941bd0d5a_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/a73c767b21d130a70a1077e371985e90\_MD5.png](assets/第2章%20文件IO/a73c767b21d130a70a1077e371985e90_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/bfdc252d499ebe71e7e6215d08310983\_MD5.png](assets/第2章%20文件IO/bfdc252d499ebe71e7e6215d08310983_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第2章 文件IO/d15ff0894667aae90b359d7b3770c27f\_MD5.png](assets/第2章%20文件IO/d15ff0894667aae90b359d7b3770c27f_MD5.png)