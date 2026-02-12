---
title: "【北京迅为】《iTOP-3588开发板开发板系统编程手册》第3章 标准IO"
source: "https://blog.csdn.net/BeiJingXunWei/article/details/137559128"
author:
  - "[[BeiJingXunWei]]"
published: 2024-04-10
created: 2025-09-11
description: "文章浏览阅读922次，点赞17次，收藏12次。RK3588是一款低功耗、高性能的处理器，适用于基于arm的PC和Edge计算设备、个人移动互联网设备等数字多媒体应用，RK3588支持8K视频编解码，内置GPU可以完全兼容OpenGLES 1.1、2.0和3.2。RK3588引入了新一代完全基于硬件的最大4800万像素ISP，内置NPU，支持INT4/INT8/INT16/FP16混合运算能力，支持安卓12和、Debian11、Build root、Ubuntu20和22版本登系统。了解更多信息可点击【粉丝群】824412014。_itop执行标准"
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

## 第3章 标准IO

标准IO（Standard I/O）是一种抽象层，用于在程序和底层操作系统I/O接口之间提供一个标准化的、可移植的I/O接口。标准IO提供了对文件、终端、套接字等不同类型的I/O设备的统一访问接口。标准IO主要包括以下三个文件流：

stdin：标准输入流，通常关联着键盘输入。

stdout：标准输出流，通常关联着控制台显示器。

stderr：标准错误流，通常关联着控制台显示器，用于输出错误信息。

标准IO提供了一组函数来读写这三个文件流，包括fopen()、fclose()、fread()、fwrite()、fseek()等。

标准IO的主要优点是：

1. 与底层的系统调用相比，标准IO函数更加容易使用和掌握，可以大大降低编程的难度。
2. 标准IO函数可以自动进行缓冲，从而提高IO效率。缓冲可以是全缓冲、行缓冲或无缓冲，可以通过setvbuf()函数进行设置（关于缓存相关的知识会在第五章进行讲解）。
3. 标准IO函数是可移植的，可以在不同的操作系统上使用相同的代码进行编译和运行。

标准IO也有一些缺点：

1. 标准IO函数的效率相对较低，因为需要进行多次函数调用和缓冲区的复制。
2. 标准IO函数有时不能提供足够的控制力，比如无法直接控制文件描述符或进行底层的操作。

下面就跟随我一起进入标准IO的学习吧。

### 3.1 FILE指针

FILE指针是C语言中用来处理文件的重要概念，它指向文件中的某个位置，可以用来进行文件的读取和写入操作。在C语言中，所有的文件I/O操作都通过FILE结构体来实现，FILE指针则是指向这个结构体的指针。

使用FILE指针进行文件操作的基本流程如下：

1. 打开文件：使用fopen函数打开文件，并返回一个FILE指针，该指针指向打开的文件。
2. 对文件进行读写操作：可以使用fscanf、fprintf等函数对文件进行读写操作。
3. 关闭文件：使用fclose函数关闭文件，释放资源，并将FILE指针设置为NULL。

会在接下来的几个小节中对打开文件、关闭文件、文件的读写等相关C语言库函数进行讲解。

### 3.2打开文件

本小节代码在配套资料“ iTOP-3588开发板\\03\_【iTOP-RK3588开发板】指南教程\\03\_系统编程配套程序 \\08 ”目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/8a44dfdf28f066de3a03f56f5974c639\_MD5.png](assets/第3章%20标准IO/8a44dfdf28f066de3a03f56f5974c639_MD5.png)

****学习前的疑问：****

1.打开文件要使用哪个C语言库函数？

2.fopen()函数要怎样进行使用？

fopen()是C库函数中用来打开文件的函数，所使用的头文件和函数原型，如下所示：

|  | 所需头文件 | 函数原型 |
| --- | --- | --- |
| 1 | #include <stdio.h> | FILE **\*** fopen **(**const char **\*** pathname**,**const char **\*** mode**);** |

fopen 的返回值是 FILE 类型的文件流，当它的值不为 NULL 时表示正常，后续的 fread、fwrite 等函数可通过文件流访问对应的文件。

fopen()函数两个参数含义如下所示：

|  | 参数名称 | 参数含义 |
| --- | --- | --- |
| 1 | pathname | 字符串类型，用于标识需要打开或创建的文件路径和文件名。 |
| 2 | mode | 该参数是一个字符串类型，用于指定文件的打开方式 |

常用的mode参数如下：

| 标志 | 用途 |
| --- | --- |
| "r" | 以只读方式打开，文件指针位于文件的开头 |
| "r+" | 以可读、可写方式打开文件。 |
| "w" | 以只写方式打开文件，如果参数 path 指定的文件存在，将文件长度截断为 0；如果指定文件不存在则创建该文件。 |
| "w+" | 以可读、可写方式打开文件，如果参数 path 指定的文件存在，将文件长度截断为 0；如果指定文件不存在则创建该文件。 |
| "a" | 以只写方式打开文件，打开以进行追加内容（在文件末尾写入），如果文件不存在则创建该文件。 |
| "a+" | 以可读、可写方式打开文件，以追加方式写入 （在文件末尾写入），如果文件不存在则创建该文件。 |

至此关于fopen()函数的相关讲解就完成了，下面进行相应的实验。

****实验要求：****

通过C语言库函数fopen()，创建一个可读可写名称为test的文件

****实验步骤：****

首先进入到 ubuntu 的终端界面输入以下命令来创建demo08\_fopen.c文件，如下图所示：

> vim demo08\_fopen.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/0a71eb4b034ab83d5bd539d5dcb9daa7\_MD5.png](assets/第3章%20标准IO/0a71eb4b034ab83d5bd539d5dcb9daa7_MD5.png)

然后向该文件中添加以下内容：

```cpp
#include<stdio.h>

 

int main(int argc,char *argv[])

{

    FILE *fp;          // 定义文件指针变量

    int ret;           // 定义返回值变量

 

    fp = fopen("test", "w+");  // 打开文件 test，以读写方式打开

    if (fp == NULL)    // 如果文件打开失败，fp 的值为 NULL

    {

        perror("File open error\r\n");  // 打印错误信息

    }

    printf("File open success\r\n");   // 如果文件打开成功，则打印成功信息

 

    return 0;   // 程序正常结束

}
cpp
```

上述内容中，第8行调用了标准IO库函数fopen(),第一个参数为要打开或者创建的文件名称，第二个参数为w+，代表如果文件不存在就创建，存在或者创建成功之后以可读可写的方式打开文件。

保存退出之后，使用以下命令对demo08\_fopen.c进行编译，编译完成如下图所示：

> gcc -o demo08\_fopen demo08\_fopen.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/3776cf24eae9579de3cfd61721ec1707\_MD5.png](assets/第3章%20标准IO/3776cf24eae9579de3cfd61721ec1707_MD5.png)

然后使用命令“./demo08\_fopen ”来运行，运行成功如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/e8125fe9570e8390f9e7c5c569dce683\_MD5.png](assets/第3章%20标准IO/e8125fe9570e8390f9e7c5c569dce683_MD5.png) 可以看到程序运行成功之后，test文件就被创建成功了，然后再使用“ ls -l ”命令查看文件属性，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/393c7cad2cef3c68b6c3d1276078d089\_MD5.png](assets/第3章%20标准IO/393c7cad2cef3c68b6c3d1276078d089_MD5.png)

可以看到test文件的属性为可读可写，至此关于fopen函数的实验就完成了。

### 3.3关闭文件

本小节代码在配套资料“ iTOP-3588开发板\\03\_【iTOP-RK3588开发板】指南教程\\03\_系统编程配套程序 \\ 09 ”目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/c29a11df8eb5208e557a94b3c75d3a26\_MD5.png](assets/第3章%20标准IO/c29a11df8eb5208e557a94b3c75d3a26_MD5.png)

****学习前的疑问：****

1.关闭文件要使用哪个C语言库函数呢？

2.fclose()函数要怎样进行使用？

fclose()函数用于关闭已经打开的文件指针，所使用的头文件和函数原型，如下所示：

|  | 所需头文件 | 函数原型 |
| --- | --- | --- |
| 1 | #include < stdio.h> | int close **((**FILE **\*** stream**);** |

fclose函数返回0表示成功关闭文件，返回EOF表示关闭失败。fclose函数会将所有的缓冲区中的数据写入文件中，关闭文件并释放相应的资源。如果在写入数据时发生错误，fclose函数会返回EOF并设置相应的错误标志。

fclose()函数参数含义如下所示：

|  | 参数名称 | 参数含义 |
| --- | --- | --- |
| 1 | stream | FILE 类型指针。 |

至此关于fclose()函数的相关讲解就完成了，下面进行相应的实验。

****实验要求：****

创建一个可读可写名为test的文件，使用fopen函数打开文件之后使用fclose()函数对打开的文件流进行关闭。

****实验步骤：****

首先进入到ubuntu的终端界面输入以下命令来创建demo09\_fclose.c文件，如下图所示：

> vim demo09\_fclose.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/91df9826be79c2465495c1c102fb37d2\_MD5.png](assets/第3章%20标准IO/91df9826be79c2465495c1c102fb37d2_MD5.png)

然后向该文件中添加以下内容：

```cpp
#include <stdio.h>

 

int main(int argc, char *argv[])

{

    FILE *fp; // 定义文件指针变量

    int ret;

    fp = fopen("test", "w+");  // 打开文件

    if(fp == NULL)

    {

        perror("文件打开失败\n");  // 打开文件失败，输出错误信息

    }

    printf("文件打开成功\n");

 

    ret = fclose(fp);  // 关闭文件

    if(ret != 0)

    {

        perror("文件关闭失败\n");  // 关闭文件失败，输出错误信息

    }

    printf("文件关闭成功\n");

 

    return 0;

}
cpp
```

相较于3.2小节的实验代码，只是多了第14行标准IO函数fclose(),用来关闭文件流，随后对fclose()函数的返回值进行判断。

保存退出之后，使用以下命令对demo09\_close.c进行编译，编译完成如下图所示：

> gcc -o demo09\_fclose demo09\_fclose.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/837cb5fcaa8a400acb4d45de596bc859\_MD5.png](assets/第3章%20标准IO/837cb5fcaa8a400acb4d45de596bc859_MD5.png) 然后使用命令“./demo09\_ f close ”来运行，运行成功如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/66ca7408648bcdd174a56f6d3820659b\_MD5.png](assets/第3章%20标准IO/66ca7408648bcdd174a56f6d3820659b_MD5.png)

可以看到程序运行成功之后，test文件被创建成功了，且打开文件和关闭文件的信息也成功打印，至此关于fclose()函数实验就完成了。

### 3.4读文件

本小节代码在配套资料“ iTOP-3588开发板\\03\_【iTOP-RK3588开发板】指南教程\\03\_系统编程配套程序 \\10 ”目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/886779bd93d0a89e8d1f0f9a46869876\_MD5.png](assets/第3章%20标准IO/886779bd93d0a89e8d1f0f9a46869876_MD5.png)

****学习前的疑问：****

1.读取文件要使用哪个C语言库函数呢？

2.fread()函数要怎样进行使用？

fread()函数从文件中读取数据，所使用的头文件和函数原型，如下所示：

|  | 所需头文件 | 函数原型 |
| --- | --- | --- |
| 1 | #include <stdio.h> | size\_t fread **(**void **\*** ptr**,**size\_t size**,**size\_t nmemb**,**FILE **\*** stream**);** |

调用成功时返回读取到的数据项数目（数据项数目并不等于实际读取的字节数，除非参数size 等于 1）；如果发生错误或到达文件末尾，则 fread()返回的值将小于参数 nmemb，那么到底发生了错误还是到达了文件末尾，fread()并不能对此进行区分，具体是哪一种情况，此时可以使用 ferror()或 feof()函数来判断（ 这两个函数会在3.7小节进行讲解 ）。

fread()函数参数含义如下所示：

|  | 参数名称 | 参数含义 |
| --- | --- | --- |
| 1 | ptr | fread()将读取到的数据存放在参数 ptr 指向的缓冲区中 |
| 2 | size | fread()从文件读取 nmemb 个数据项，每一个数据项的大小为 size 个字节，所以总共读取的数据大小为 nmemb \* size 个字节 |
| 3 | nmemb | 参数 nmemb 指定了读取数据项的个数 |
| 4 | stream | FILE 指针 |

至此关于fread()函数的相关讲解就完成了，下面进行相应的实验。

****实验要求：****

读取test文件中的内容，并打印出来。

****实验步骤：****

首先进入到ubuntu的终端界面输入以下命令来创建demo10\_fread.c文件，如下图所示：

> vim demo10\_fread.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/c73232705ae3cc4ef43503cec3dbf214\_MD5.png](assets/第3章%20标准IO/c73232705ae3cc4ef43503cec3dbf214_MD5.png) 然后向该文件中添加以下内容：

```cpp
#include<stdio.h>

 

int main(int argc,char *argv[])

{

    FILE *fp; //定义文件指针变量

    int ret; //定义返回值变量

    char buffer[1024] = {0}; //定义字符数组变量，并初始化为0

    fp = fopen("test", "r+"); //打开文件，以读写方式打开，若文件不存在则创建文件

    if(fp == NULL) //判断文件是否打开成功

    {

        perror("File open error\n"); //输出错误信息

        return -1; //返回错误代码

    }

    fread(buffer, sizeof(char), sizeof(buffer), fp); //从文件中读取数据到buffer数组中

    printf("buffer = %s\n", buffer); //输出buffer数组中的数据

    ret = fclose(fp); //关闭文件

    if(ret != 0) //判断文件是否关闭成功

    {

        perror("File close error\n"); //输出错误信息

        return -2; //返回错误代码

    }

    printf("File close success\n"); //输出文件关闭成功信息

    return 0; //返回正常代码

}
cpp
```

上述内容相较于3.3小节实验，添加了第14行和第15行内容，第14行使用了fread()函数对文件test进行数据的读取，并将读到的数据写入了buffer缓冲区 中，第11行对buffer内容进行打印。

保存退出之后，使用以下命令对demo10\_fread.c进行编译，编译完成如下图所示：

> gcc -o demo10\_fread demo10\_fread.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/80f0b33b671ff120004832ed5372bc7a\_MD5.png](assets/第3章%20标准IO/80f0b33b671ff120004832ed5372bc7a_MD5.png)

然后使用命令“ vim test ”创建test文件，并添加以下内容：

> hello world!!

添加完成如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/dee1fd9e65d2657251a51d017b1fc074\_MD5.png](assets/第3章%20标准IO/dee1fd9e65d2657251a51d017b1fc074_MD5.png) 然后使用命令“./demo10\_fread ”来运行，运行成功如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/6332f09790370297a51787be13e67ec1\_MD5.png](assets/第3章%20标准IO/6332f09790370297a51787be13e67ec1_MD5.png)

可以看到已经test文件中的“hello world!!”数据就被打印了出来，数据读取完成之后，文件流被关闭了。

至此关于fread()函数的实验就完成了。

### 3.5写文件

本小节代码在配套资料“ iTOP-3588开发板\\03\_【iTOP-RK3588开发板】指南教程\\03\_系统编程配套程序 \\11 ”目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/7bbf6a90fdbb3b5f13183d8d684ad19b\_MD5.png](assets/第3章%20标准IO/7bbf6a90fdbb3b5f13183d8d684ad19b_MD5.png)

****学习前的疑问：****

1.读取文件要使用哪个C语言库函数呢？

2.fwrite()函数要怎样进行使用？

fwrite()函数从文件中读取数据，所使用的头文件和函数原型，如下所示：

|  | 所需头文件 | 函数原型 |
| --- | --- | --- |
| 1 | #include <stdio.h> | size\_t fwrite **(**const void **\*** ptr**,**size\_t size**,**size\_t count**,**FILE **\*** stream**);** |

调用成功时返回写入的数据项的数目（数据项数目并不等于实际写入的字节数，除非参数 size 等于 1）；如果发生错误，则 fwrite()返回的值将小于参数 nmemb（或者等于 0）。由此可知，库函数 fread()、fwrite()中指定读取或写入数据大小的方式与系统调用 read()、write()不同，前者通过nmemb（数据项个数）\*size（每个数据项的大小）的方式来指定数据大小，而后者则直接通过一个 size 参数指定数据大小。

fwrite()函数参数含义如下所示：

|  | 参数名称 | 参数含义 |
| --- | --- | --- |
| 1 | ptr | fread()将读取到的数据存放在参数 ptr 指向的缓冲区中 |
| 2 | size | fread()从文件读取 nmemb 个数据项，每一个数据项的大小为 size 个字节，所以总共读取的数据大小为 nmemb \* size 个字节 |
| 3 | nmemb | 参数 nmemb 指定了读取数据项的个数 |
| 4 | stream | FILE 指针 |

至此关于fwrite()函数的相关讲解就完成了，下面进行相应的实验。

****实验要求：****

本代码所要实现的目标为创建一个可以读写名为test的文件，并写入字符“hello world”。

****实验步骤：****

首先进入到ubuntu的终端界面输入以下命令来创建demo11\_fwrite.c文件，如下图所示：

> vim demo11\_fwrite.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/1a294900c6ecd229095dee46bbfa640d\_MD5.png](assets/第3章%20标准IO/1a294900c6ecd229095dee46bbfa640d_MD5.png) 然后向该文件中添加以下内容

```cpp
#include<stdio.h>

 

int main(int argc,char *argv[])

{

    FILE *fp; //定义文件指针变量

    int ret; //定义返回值变量

    char buffer[11] = {"hello world"}; //定义字符数组变量，并初始化为"hello world"

    fp = fopen("test", "a"); //打开文件，以追加写入方式打开，若文件不存在则创建文件

    if(fp == NULL) //判断文件是否打开成功

    {

        perror("File open error\r\n"); //输出错误信息

        return -1; //返回错误代码

    }

    fwrite(buffer, sizeof(char), sizeof(buffer), fp); //将buffer数组中的数据写入文件中

    printf("buffer = %s\n", buffer); //输出buffer数组中的数据

    ret = fclose(fp); //关闭文件

    if(ret != 0) //判断文件是否关闭成功

    {

        perror("File close error\r\n"); //输出错误信息

        return -2; //返回错误代码

    }

    printf("File close success\r\n"); //输出文件关闭成功信息

    return 0; //返回正常代码

}
cpp
```

上述内容相较于3.3小节实验，添加了第14行和第15行内容，第15行使用了fwrite()函数将缓冲区buffer\[\]中的内容写入到test文件中，第15行对buffer缓冲区中的数据进行打印。

保存退出之后，使用以下命令对demo11\_fwrite.c进行编译，编译完成如下图所示：

> gcc -o demo11\_fwrite demo11\_fwrite.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/b990d3a878590b2c61e35a46031f997f\_MD5.png](assets/第3章%20标准IO/b990d3a878590b2c61e35a46031f997f_MD5.png) 然后使用命令“./demo11\_fwrite ”来运行，运行成功如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/71781d2219f6651aa2307d0b48911441\_MD5.png](assets/第3章%20标准IO/71781d2219f6651aa2307d0b48911441_MD5.png)

可以看到test文件已经被成功创建了，然后使用以下命令对test文件进行查看，如下图所示：

> cat test

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/8f9ad1bcb48badf278c3974d11ccf135\_MD5.png](assets/第3章%20标准IO/8f9ad1bcb48badf278c3974d11ccf135_MD5.png)

可以看到“hello world”已经被写入test文件了。至此，关于fwrite()函数的相关实验就完成了。

### 3.6 fseek

和2.6小节lseek系统调用的作用相同，在C语言库函数中使用fseek函数设置文件指针的位置，在本小节将对fseek函数进行讲解。

本小节代码在配套资料“ iTOP-3588开发板\\03\_【iTOP-RK3588开发板】指南教程\\03\_系统编程配套程序 \\12 ”目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/852b06a6e2e0062a9b77ca2a83708591\_MD5.png](assets/第3章%20标准IO/852b06a6e2e0062a9b77ca2a83708591_MD5.png)

fseek()函数用于设置文件读写位置偏移量，所使用的头文件和函数原型，如下所示：

|  | 所需头文件 | 函数原型 |
| --- | --- | --- |
| 1 | #include <stdio.h> | int fseek **(**FILE **\*** stream**,**long offset**,**int whence**);** |

fseek函数返回0表示设置成功，返回非0值表示设置失败。

fseek()函数参数含义如下所示：

|  | 参数名称 | 参数含义 |
| --- | --- | --- |
| 1 | stream | 要设置读写位置的文件指针 |
| 2 | offset | 相对于whence参数指定的位置的偏移量 |
| 3 | whence | 指定偏移量的起始位置。 |

至此关于fseek()函数的相关讲解就完成了，下面进行相应的实验。

****实验要求：****

测试fseek函数移动文件读写位置的功能。

****实验步骤：****

首先进入到ubuntu的终端界面输入以下命令来创建demo12\_fseek.c文件，如下图所示：

> vim demo12\_fseek.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/f1d712b322746e86150e4519edc8d6e0\_MD5.png](assets/第3章%20标准IO/f1d712b322746e86150e4519edc8d6e0_MD5.png) 然后向该文件中添加以下内容：

```cpp
#include <stdio.h>

 

int main(int argc,char *argv[])

{

    FILE *fp; //定义文件指针变量

    int ret; //定义返回值变量

    char buffer[1024] = {0}; //定义字符数组变量，并初始化为0

    fp = fopen("test", "r+"); //以读写方式打开文件，若文件不存在则创建文件

    if(fp == NULL) //判断文件是否打开成功

    {

        perror("File open error\r\n"); //输出错误信息

        return -1; //返回错误代码

    }

 

    fseek(fp, 5, SEEK_SET); //将文件指针指向文件的第6个字节处

    fread(buffer, sizeof(char), sizeof(buffer), fp); //从文件中读取数据到buffer数组中

    printf("buffer = %s\n", buffer); //输出buffer数组中的数据

 

    ret = fclose(fp); //关闭文件

    if(ret != 0) //判断文件是否关闭成功

    {

        perror("File close error\r\n"); //输出错误信息

        return -2; //返回错误代码

    }

 

    printf("File close success\r\n"); //输出文件关闭成功信息

    return 0; //返回正常代码

}
cpp
```

上述内容和3.4小节的相比只是多了第15行的内容，将读写指针偏移了五个字节。然后使用fread()函数进行数据读取，并打印读取到的内容。

保存退出之后，使用以下命令对demo12\_fseek.c进行编译，编译完成如下图所示：

> gcc -o demo12\_fseek demo12\_fseek.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/f3e1aa171970ed9e19ee4193e117a3fa\_MD5.png](assets/第3章%20标准IO/f3e1aa171970ed9e19ee4193e117a3fa_MD5.png)

然后使用命令“ vim test ”创建test文件，并添加以下内容：

> hello world!!

添加完成如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/dee1fd9e65d2657251a51d017b1fc074\_MD5.png](assets/第3章%20标准IO/dee1fd9e65d2657251a51d017b1fc074_MD5.png) 然后使用命令“./demo12\_fseek ”来运行，运行成功如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/7a1b6575f7042dded15d238d6c4728ab\_MD5.png](assets/第3章%20标准IO/7a1b6575f7042dded15d238d6c4728ab_MD5.png)

可以看到程序运行成功之后，只会打印第五个字节之后的字符“world！！”，证明文件读写指针发生了变化，至此关于feek()函数相关的实验就完成了。

### 3.7 perror

经过了前面12个实验，大家会发现每个实验代码中都会有perror函数，用来进行错误信息的输出。perror是一个标准C库函数，其作用是将当前errno的值作为参数，输出对应的错误信息到标准错误输出（stderr）上。perror函数可以帮助我们快速定位程序运行时出现的错误，便于进行调试和排错。

perror函数的函数原型如下：

|  | 所需头文件 | 函数原型 |
| --- | --- | --- |
| 1 | #include <stdio.h> | void perror **(**const char **\*** s**);** |

其中，参数s是一个字符串，表示我们希望在输出错误信息前输出的一段文本，通常是一些提示信息或者函数名。如果s为NULL，则只输出错误信息而不添加前缀。

perror函数的使用非常简单，只需要在程序中调用它即可，以判断fopen函数返回值为例，perror的使用如下所示：

| 1  2  3  4  5  6  7  8  9  10  11  12  13  14 | #include <stdio.h>  int main **(**int argc**,**char **\*** argv **\[\])**  **{**  FILE **\*** fp**;**//定义文件指针变量  fp **\=** fopen **(**"test"**,**"a"**);**//以追加写入方式打开文件，若文件不存在则创建文件  **if** **(**fp **\==** **NULL****)** //判断文件是否打开成功  **{**  perror **(**"File open error\\r\\n"**);**//输出错误信息  **return** **\-** 1**;**//返回错误代码  **}**  **return** 0**;**//返回正常代码  **}** |
| --- | --- |

如果fopen函数调用失败，首先会打印“File open error”，然后会打印系统定义的错误信息，由于在之后的小节中仍旧会使用该函数，就不在此进行具体实验了。

### 3.8检查和复位状态

在调用 fread()进行文件数据读取时，如果返回值小于参数 nmemb 所指定的值，表示发生了错误或者已经到了文件末尾（文件结束 end-of-file），但 fread()无法具体确定是哪一种情况，在本小节将学习两个函数对该问题进行解决。

#### 3.8.1 feof()函数

feof()函数实验代码在配套资料“ iTOP-3588开发板\\03\_【iTOP-RK3588开发板】指南教程\\03\_系统编程配套程序 \\13 ”目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/4001ea7c278c79f6c70ea33b3f45f7e9\_MD5.png](assets/第3章%20标准IO/4001ea7c278c79f6c70ea33b3f45f7e9_MD5.png)

feof()函数是C标准库中的一个函数，用于判断文件指针所指向的文件是否已经到达文件结尾。所使用的头文件和函数原型，如下所示：

|  | 所需头文件 | 函数原型 |
| --- | --- | --- |
| 1 | #include <stdio.h> | int feof **(**FILE **\*** stream**);** |

如果 end-of-file 标志被设置了，则调用 feof()函数将返回一个非零值，如果 end-of-file 标志没有被设置，则返回 0。当文件的读写位置移动到了文件末尾时，end-of-file 标志将会被设置。

feof()函数参数含义如下所示：

|  | 参数名称 | 参数含义 |
| --- | --- | --- |
| 1 | stream | FILE 指针 |

至此关于fread()函数的相关讲解就完成了，下面进行相应的实验。

****实验要求：****

使用feof()函数，分别测试读写位置移动到文件末尾和没有移动到文件末尾两种情况。

****实验步骤：****

首先进入到ubuntu的终端界面输入以下命令来创建demo13\_feof.c文件，如下图所示：

> vim demo13\_feof.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/1c3fb289a06becd8eaea0c89d668285e\_MD5.png](assets/第3章%20标准IO/1c3fb289a06becd8eaea0c89d668285e_MD5.png) 然后向该文件中添加以下内容：

| 1  2  3  4  5  6  7  8  9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31  32  33 | #include <stdio.h>  int main **(**int argc**,**char **\*** argv **\[\])**  **{**  FILE **\*** fp**;**// 声明一个文件指针变量  int ret**;**// 声明一个整型变量用于保存函数返回值  char buffer **\[**20**\]** **\=** **{** 0 **};**// 声明一个大小为20的字符数组，用于存储从文件中读取的内容  fp **\=** fopen **(**"test"**,**"r+"**);**// 打开名为“test”的文件，使用“读写”模式  **if** **(**fp **\==** **NULL****)** // 如果文件指针为空，说明打开文件失败  **{**  perror **(**"File open error\\r\\n"**);**// 输出错误信息  **return** **\-** 1**;**// 返回-1，表示程序运行失败  **}**  fread **(**buffer**,****sizeof** **(**char**),****sizeof** **(**buffer**),** fp**);**// 从文件中读取数据，并存储到buffer数组中  printf **(**"buffer = %s\\n"**,** buffer**);**// 输出从文件中读取的内容  **if** **(**feof **(**fp**))** // 判断文件指针是否已经移动到文件末尾  **{**  printf **(**"Moved to end of file\\r\\n"**);**// 如果是，输出相应的提示信息  **}**  **else** // 否则说明还没有到文件末尾或者读取文件出错  **{**  printf **(**"Not moved to end of file or error occurred\\r\\n"**);**// 输出相应的提示信息  **}**  ret **\=** fclose **(**fp**);**// 关闭文件  **if** **(**ret **!=** 0**)** // 如果关闭文件失败，返回-2  **{**  perror **(**"File close error\\r\\n"**);**// 输出错误信息  **return** **\-** 2**;**  **}**  printf **(**"File close success\\r\\n"**);**// 输出文件关闭成功的提示信息  **return** 0**;**// 返回0，表示程序运行成功  **}** |
| --- | --- |

上述代码在3.4小节中的实验基础上添加了17-24行feof()函数的判断，通过修改buffer\[\]缓冲区大小，测试读写位置移动到文件末尾和没有移动到文件末尾两种情况。

保存退出之后，使用以下命令对demo13\_feof.c进行编译，编译完成如下图所示：

> gcc -o demo13\_feof demo13\_feof.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/26b1aace1487b4ea0d168b3f57f51dce\_MD5.png](assets/第3章%20标准IO/26b1aace1487b4ea0d168b3f57f51dce_MD5.png)

然后使用命令“ vim test ”创建test文件，并添加以下内容：

> hello world!!

添加完成如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/dee1fd9e65d2657251a51d017b1fc074\_MD5.png](assets/第3章%20标准IO/dee1fd9e65d2657251a51d017b1fc074_MD5.png) 然后使用命令“./demo13\_feof ”来运行，运行成功如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/c4648801dd19b47151551b2f489a336c\_MD5.png](assets/第3章%20标准IO/c4648801dd19b47151551b2f489a336c_MD5.png)

可以看到程序运行成功之后，会打印“Moved to end of file”证明读写指针已经移动到了文件的末尾，如果我们将第6行的buffer值进行修改，修改为10，再次运行对应的可执行文件之后，打印信息如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/7581d9a91e4237bb8cf945df0015d9c2\_MD5.png](assets/第3章%20标准IO/7581d9a91e4237bb8cf945df0015d9c2_MD5.png)

可以看到上图的打印信息为“Not moved to end of file or error occurred”，证明读写指针并没有到达文件末尾，至此feof()函数就测试成功了。

#### 3.8.2 ferror()函数

ferror()函数实验代码在配套资料“ iTOP-3588开发板\\03\_【iTOP-RK3588开发板】指南教程\\03\_系统编程配套程序 \\14 ”目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/d63dea45af3a8f5939b9f513008fda19\_MD5.png](assets/第3章%20标准IO/d63dea45af3a8f5939b9f513008fda19_MD5.png)

ferror()函数是C标准库中的一个函数，如果错误标志被设置了，则ferror()函数会被调用，用于检查文件流的错误状态。所使用的头文件和函数原型，如下所示：

|  | 所需头文件 | 函数原型 |
| --- | --- | --- |
| 1 | #include <stdio.h> | int ferror **(**FILE **\*** stream**);** |

如果错误标志被设置了则返回1，否则返回0。

ferror()函数参数含义如下所示：

|  | 参数名称 | 参数含义 |
| --- | --- | --- |
| 1 | stream | FILE 指针 |

至此关于fread()函数的相关讲解就完成了，下面进行相应的实验。

****实验要求：****

测试ferror()函数。

****实验步骤：****

首先进入到ubuntu的终端界面输入以下命令来创建demo14\_ferror.c文件，如下图所示：

> vim demo14\_ferror.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/dadbfdd2a7851843e165aef54d61ca90\_MD5.png](assets/第3章%20标准IO/dadbfdd2a7851843e165aef54d61ca90_MD5.png) 然后向该文件中添加以下内容

```cpp
#include <stdio.h>

 

int main(int argc, char *argv[])

{

    FILE *fp;                     // 声明一个文件指针变量

    int ret, num;                 // 声明整型变量用于保存函数返回值和读取的字符数

    char buffer[1024] = {0};      // 声明一个大小为1024的字符数组，用于存储从文件中读取的内容

    fp = fopen("test", "r+");     // 打开名为“test”的文件，使用“读写”模式

    if (fp == NULL)               // 如果文件指针为空，说明打开文件失败

    {

        perror("File open error\r\n");   // 输出错误信息

        return -1;                // 返回-1，表示程序运行失败

    }

    num = fread(buffer, sizeof(char), sizeof(buffer), fp);  // 从文件中读取数据，并存储到buffer数组中

    printf("buffer = %s\n", buffer);  // 输出从文件中读取的内容

    if (ferror(fp))              // 判断文件读取过程中是否出错

    {

        printf("Error to read the file\r\n");  // 如果有错误，输出相应的提示信息

    }

    else                          // 如果没有错误，说明读取文件成功

    {

        printf("No error in reading\r\n");    // 输出相应的提示信息

    }

    ret = fclose(fp);            // 关闭文件

    if (ret != 0)                // 如果关闭文件失败，返回-2

    {

        perror("File close error\r\n");     // 输出错误信息

        return -2;

    }

    printf("File close success\r\n");  // 输出文件关闭成功的提示信息

    return 0;                    // 返回0，表示程序运行成功

}
cpp
```

保存退出之后，使用以下命令对demo14\_ferror.c进行编译，编译完成如下图所示：

> gcc -o demo14\_ferror demo14\_ferror.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/3fc005999e919bfdb76d257f4248be93\_MD5.png](assets/第3章%20标准IO/3fc005999e919bfdb76d257f4248be93_MD5.png)

然后使用命令“ vim test ”创建test文件，并添加以下内容：

> hello world!!

添加完成如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/dee1fd9e65d2657251a51d017b1fc074\_MD5.png](assets/第3章%20标准IO/dee1fd9e65d2657251a51d017b1fc074_MD5.png) 然后使用命令“./demo14\_ferror ”来运行，运行成功如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/0428d8fb9e2b39a91b0628fb02bad361\_MD5.png](assets/第3章%20标准IO/0428d8fb9e2b39a91b0628fb02bad361_MD5.png)

可以看到程序运行成功之后，会打印“No error in reading”证明读写没有错误，至此我们的feof()函数就测试成功了。

#### 3.8.3 clearerr()函数

当调用 feof()或 ferror()校验这些标志后，通常需要清除这些标志，避免下次校验时使用到的是上一次设置的值，此时可以手动调用 clearerr()函数清除标志。

clearerr()函数所使用的头文件和函数原型，如下所示：

|  | 所需头文件 | 函数原型 |
| --- | --- | --- |
| 1 | #include <stdio.h> | void clearerr **(**FILE **\*** stream**);** |

此函数类型为void，没有返回值，所以函数调用总是会成功。

clearerr()函数参数含义如下所示：

|  | 参数名称 | 参数含义 |
| --- | --- | --- |
| 1 | stream | FILE 指针 |

至此，关于clearerr()函数的讲解就完成了。由于clearerr()函数的使用较为简单，只要在 feof()或 ferror()函数后调用clearerr()函数即可，所以本小节不再进行相应的测试。

微信公众号

内容来源：csdn.net

作者昵称：北京迅为

原文链接：https://blog.csdn.net/BeiJingXunWei/article/details/137559128

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

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/90bd0cbf3aff8fdff8bf9b011b581e20\_MD5.png](assets/第3章%20标准IO/90bd0cbf3aff8fdff8bf9b011b581e20_MD5.png)

程序员都在用的中文IT技术交流社区

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/08a47e60886378fe60a3d9c8f4ae8bc6\_MD5.png](assets/第3章%20标准IO/08a47e60886378fe60a3d9c8f4ae8bc6_MD5.png)

专业的中文 IT 技术社区，与千万技术人共成长

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/a51be6c085b867a5bd82d8dc1cea9b46\_MD5.png](assets/第3章%20标准IO/a51be6c085b867a5bd82d8dc1cea9b46_MD5.png)

关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！

客服 返回顶部

微信公众号

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第3章 标准IO/efb7921311640694e61fee00900550d6\_MD5.jpg](assets/第3章%20标准IO/efb7921311640694e61fee00900550d6_MD5.jpg) 公众号名称：迅为电子 微信扫码关注或搜索公众号名称

复制公众号名称