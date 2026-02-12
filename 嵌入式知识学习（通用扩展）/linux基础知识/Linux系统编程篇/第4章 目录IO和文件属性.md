---
title: "【北京迅为】《iTOP-3588开发板系统编程手册》第4章 目录IO和文件属性"
source: "https://blog.csdn.net/BeiJingXunWei/article/details/137584869"
author:
  - "[[BeiJingXunWei]]"
published: 2024-04-15
created: 2025-09-11
description: "文章浏览阅读1k次，点赞15次，收藏16次。RK3588是一款低功耗、高性能的处理器，适用于基于arm的PC和Edge计算设备、个人移动互联网设备等数字多媒体应用，RK3588支持8K视频编解码，内置GPU可以完全兼容OpenGLES 1.1、2.0和3.2。RK3588引入了新一代完全基于硬件的最大4800万像素ISP，内置NPU，支持INT4/INT8/INT16/FP16混合运算能力，支持安卓12和、Debian11、Build root、Ubuntu20和22版本登系统。了解更多信息可点击【粉丝群】824412014。_itop如何定义文件类型"
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

## 第4章 目录IO和文件属性

第2章和第3章的内容都是文件操作相关的，主要包括文件的打开、关闭、读写等操作，在本章节首先对目录相关的系统调用进行讲解，然后对文件属性相关的系统调用API进行讲解。

### 4.1创建目录

本小节代码在配套资料“ iTOP-3588开发板\\03\_【iTOP-RK3588开发板】指南教程\\03\_系统编程配套程序 \\15 ”目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/a1841f166717d53b677779eb28e3e3e4\_MD5.png](assets/第4章%20目录IO和文件属性/a1841f166717d53b677779eb28e3e3e4_MD5.png)

****学习前的疑问：****

1.创建文件要使用哪个系统调用呢？

2.mkdir()函数要怎样进行使用？

mkdir()用来创建一个目录，所使用的头文件和函数原型，如下所示：

|  | 所需头文件 | 函数原型 |
| --- | --- | --- |
| 1  2 | #include <sys/stat.h>  #include <sys/types.h> | int mkdir **(**const char **\*** pathname**,** mode\_t mode**);** |

mkdir()执行成功会返回0，出错时返回-1。并设置error值

mkdir()函数参数含义如下所示：

|  | 参数名称 | 参数含义 |
| --- | --- | --- |
| 1 | pathname | 路径和文件名 |
| 2 | mode | 权限掩码，对不同用户和组设置可执行，读，写权限，使用八进制数表示，此参数可不写。 |

mkdir的使用较为简单，至此关于mkdir()函数的相关讲解就完成了，下面进行相应的实验。

****实验要求：****

使用mkdir()函数创建一个名为test的文件夹。

****实验步骤：****

首先进入到 ubuntu 的终端界面输入以下命令来创建demo15\_mkdir.c文件，如下图所示：

> vim demo15\_mkdir.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/9459e5bea1c4519217e220fd8973d906\_MD5.png](assets/第4章%20目录IO和文件属性/9459e5bea1c4519217e220fd8973d906_MD5.png) 然后向该文件中添加以下内容

```cpp
#include <stdio.h>

#include <stdlib.h>

#include <sys/stat.h>

#include <sys/types.h>

 

int main(int argc, char *argv[])

{

    int ret;                     // 声明一个整型变量，用于保存函数返回值

    if (argc != 2)             // 判断命令行参数是否正确，如果不正确，则输出提示信息并返回-1

    {

        printf("Usage:%s <name file>\n", argv[0]);

        return -1;

    }

    ret = mkdir(argv[1], 0666);  // 创建目录，使用指定的权限

    if (ret < 0)                 // 如果创建目录失败，返回-2，输出错误信息

    {

        perror("mkdir is error\n");

        return -2;

    }

    printf("mkdir is ok\n");     // 输出创建目录成功的提示信息

    return 0;                    // 返回0，表示程序运行成功

}
cpp
```

上述代码用到了main()函数来进行参数的传递，argv\[1\]参数来设置创建的文件夹名称，第14行用到了mkdir()函数，第一个参数就是要创建的文件夹名称，第二个参数为创建的文件夹权限，最后根据mkdir()函数的返回值来判断目录是否创建。

保存退出之后，使用以下命令对demo15\_mkdir.c进行编译，编译完成如下图所示：

> gcc -o demo15\_mkdir demo15\_mkdir.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/6d158a28f105388f527de90abaf9343f\_MD5.png](assets/第4章%20目录IO和文件属性/6d158a28f105388f527de90abaf9343f_MD5.png)

可以看到程序运行成功之后，mkdir is ok被打印，然后查看文件夹内容发现test文件已经被成功创建了。

### 4.2打开和关闭目录

本小节代码在配套资料“ iTOP-3588开发板\\03\_【iTOP-RK3588开发板】指南教程\\03\_系统编程配套程序 \\16 ”目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/ed9df847e525a93deb412e552b3de758\_MD5.png](assets/第4章%20目录IO和文件属性/ed9df847e525a93deb412e552b3de758_MD5.png)

****学习前的疑问：****

1.目录的打开和关闭要使用哪个系统调用呢？

2.opendir()函数和closedir()函数要怎样进行使用？

在 Linux 操作系统中使用opendir()打开指定的目录，使用closedir()函数关闭目录流。所使用的头文件和函数原型，如下所示：

<table><tbody><tr><td></td><td><p>所需头文件</p></td><td><p>函数原型</p></td></tr><tr><td><p><span><span>1</span></span></p></td><td rowspan="2"><p><span><span>#include &lt;sys/types.h&gt;</span></span></p><p><span><span>#include &lt;dirent.h&gt;</span></span></p></td><td><p><span><span>DIR </span></span><strong><span><span>*</span></span></strong> <span><span>opendir</span></span> <strong><span><span>(</span></span></strong><span><span>const</span></span> <span><span>char</span></span> <strong><span><span>*</span></span></strong> <span><span>name</span></span><strong><span><span>);</span></span></strong></p></td></tr><tr><td><p><span><span>2</span></span></p></td><td><p><span><span>int</span></span> <span><span>closedir</span></span> <strong><span><span>(</span></span></strong><span><span>DIR </span></span><strong><span><span>*</span></span></strong> <span><span>dirp</span></span><strong><span><span>);</span></span></strong></p></td></tr></tbody></table>

opendir调成功返回打开的目录流，失败返回 NULL，closedir 调用成功返回0，调用失败返回-1，两个函数的相关参数含义如下所示

|  | 参数名称 | 参数含义 |
| --- | --- | --- |
| 1 | name | 路径名字。 |
| 2 | dirp | 要关闭的目录流指针。 |

至此，关于打开和关闭目录的系统调用API函数就讲解完成了，下面进行相应的实验。

****实验要求：****

使用打开opendir()函数打开指定的目录，然后使用closedir()关闭目录。

****实验步骤:****

首先进入到ubuntu的终端界面输入以下命令来创建demo16\_dir.c文件，如下图所示：

> vim demo16\_dir.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/e628b79944a869adf9aa815f67ed939f\_MD5.png](assets/第4章%20目录IO和文件属性/e628b79944a869adf9aa815f67ed939f_MD5.png) 然后向该文件中添加以下内容:

```cpp
#include <stdio.h>

#include <stdlib.h>

#include <sys/stat.h>

#include <sys/types.h>

#include <dirent.h>

 

int main(int argc, char *argv[])

{

    int ret;

    DIR *dp;                        // 声明一个指向DIR结构体的指针

    if (argc != 2)                  // 判断命令行参数是否正确，如果不正确，则输出提示信息并返回-1

    {

        printf("Usage:%s <name file>\n", argv[0]);

        return -1;

    }

    dp = opendir(argv[1]);          // 打开指定的目录

    if (dp == NULL)                 // 如果打开目录失败，返回-1，输出错误信息

    {

        perror("opendir is error\n");

        return -1;

    }

    printf("opendir is ok\n");      // 输出打开目录成功的提示信息

    closedir(dp);                   // 关闭打开的目录流

    return 0;                       // 返回0，表示程序运行成功

}
cpp
```

述代码同样用到了main()函数来进行参数的传递，第17行调用了opendir()函数来打开文件夹，argv\[1\]参数来设置要打开的文件夹名称，第24行用到了closedir()函数，来对目录进行关闭。

保存退出之后，使用以下命令对demo16\_dir.c进行编译，编译完成如下图所示：

> gcc -o demo16\_dir demo16\_dir.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/e3dbc15c4bbb592d23d77762c7b54ebb\_MD5.png](assets/第4章%20目录IO和文件属性/e3dbc15c4bbb592d23d77762c7b54ebb_MD5.png) 然后使用命令“ mkdir test ”来创建测试文件夹test，创建完成如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/bbd26a9517cdb52751a75dde20233e38\_MD5.png](assets/第4章%20目录IO和文件属性/bbd26a9517cdb52751a75dde20233e38_MD5.png)

然后使用命令“./demo16\_dir./test ”来运行，运行成功如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/172f2128ac7092b4ff88abaa41a0fdf3\_MD5.png](assets/第4章%20目录IO和文件属性/172f2128ac7092b4ff88abaa41a0fdf3_MD5.png)

可以看到程序运行成功之后，对应的test文件夹被打开，“opendir is ok”就被成功打印了。

### 4.3读取目录内容

本小节代码在配套资料“ iTOP-3588开发板\\03\_【iTOP-RK3588开发板】指南教程\\03\_系统编程配套程序 \\17 ”目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/6e10484de92a15192beb3b7bbaf08eba\_MD5.png](assets/第4章%20目录IO和文件属性/6e10484de92a15192beb3b7bbaf08eba_MD5.png)

****学习前的疑问：****

1.读取目录内容使用哪个系统调用呢？

2.readdir()函数要怎样进行使用？

readdir()函数用于读取打开的目录中的文件和子目录，所使用的头文件和函数原型，如下所示：

|  | 所需头文件 | 函数原型 |
| --- | --- | --- |
| 1 | #include <dirent.h> | struct dirent **\*** readdir **(**DIR **\*** dirp**);** |

函数返回指向dirent类型结构体的指针，该结构体包含了文件和子目录的信息，如文件名、文件类型等，失败返回 NULL

readdir()函数参数含义如下所示：

|  | 参数名称 | 参数含义 |
| --- | --- | --- |
| 1 | dirp | 即指向DIR类型结构体的指针dirp，该指针通常是由opendir函数返回的 |

至此关于readdir()函数的相关讲解就完成了，下面进行相应的实验。

****实验要求：****

通过readdir()函数读取test目录的目录信息。

****实验步骤：****

首先进入到ubuntu的终端界面输入以下命令来创建demo17\_readdir.c文件，如下图所示：

> vim demo17\_readdir.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/db075fef63be7eeb147fbe85878fd0de\_MD5.png](assets/第4章%20目录IO和文件属性/db075fef63be7eeb147fbe85878fd0de_MD5.png) 然后向该文件中添加以下内容：

```cpp
#include <stdio.h>

#include <stdlib.h>

#include <sys/stat.h>

#include <sys/types.h>

#include <dirent.h>

 

int main(int argc, char *argv[])

{

    int ret;

    DIR *dp;                    // 声明一个指向DIR结构体的指针

    struct dirent *dir;         // 声明一个指向dirent结构体的指针

    if (argc != 2)           // 判断命令行参数是否正确，如果不正确，则输出提示信息并返回-1

    {

        printf("Usage:%s <name file>\n", argv[0]);

        return -1;

    }

    dp = opendir(argv[1]);      // 打开指定的目录

    if (dp == NULL)             // 如果打开目录失败，返回-2，输出错误信息

    {

        perror("opendir is error\n");

        return -2;

    }

    printf("opendir is ok\n");  // 输出打开目录成功的提示信息

    

    while (1)                   // 循环遍历目录中的所有文件

    {

        dir = readdir(dp);      // 读取目录下的一个文件

        if (dir != NULL)        // 如果文件读取成功

        {

            printf("file name is %s\n", dir->d_name);  // 输出文件名

        }

        else                    // 文件读取失败

            break;              // 跳出循环

    }

    closedir(dp);               // 关闭打开的目录流

    return 0;                   // 返回0，表示程序运行成功

}
cpp
```

上述内容和4.2小节相比，添加了一个while循环，会调用27行的readdir()函数进行目录信息的读取，读取完成之后跳出循环，调用closedir()函数对目录进行关闭。

保存退出之后，使用以下命令对demo17\_readdir.c进行编译，编译完成如下图所示：

> gcc -o demo17\_readdir demo17\_readdir.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/117cffdd858b111af728bba7f374422c\_MD5.png](assets/第4章%20目录IO和文件属性/117cffdd858b111af728bba7f374422c_MD5.png)

随后我们使用以下命令建立test测试文件夹，然后在test文件夹下建立test1文件，如下图所示：

> mkdir test
> 
> cd test/
> 
> touch test1

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/866143712f50edd33a05a6749571c02f\_MD5.png](assets/第4章%20目录IO和文件属性/866143712f50edd33a05a6749571c02f_MD5.png) 然后使用命令“./demo17\_readdir./test ”来运行，运行成功如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/e30480de106b60b81aceee36d8b4f535\_MD5.png](assets/第4章%20目录IO和文件属性/e30480de106b60b81aceee36d8b4f535_MD5.png)

可以看到已经成功读取到了test目录下的子目录。

### 4.4综合练习（二）

本小节完整代码在配套资料“ iTOP-3588开发板\\03\_【iTOP-RK3588开发板】指南教程\\03\_系统编程配套程序 \\18 ”目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/fd0a4c91e7390fae6d5b169c6710fa6c\_MD5.png](assets/第4章%20目录IO和文件属性/fd0a4c91e7390fae6d5b169c6710fa6c_MD5.png)

****实验要求****

在综合练习1的基础上，利用我们本阶段学习的知识，修改综合练习1的代码，增加以下需求：

1.打印我们要拷贝的目录下的所有文件名，并拷贝我们需要的文件。

2.通过键盘输入我们要拷贝的文件的路径和文件名等信息

****实验过程：****

首先进入到ubuntu的终端界面输入以下命令来创建demo18\_test.c文件，如下图所示：

> vim demo18\_test.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/753bd6ef8e181c698a4ee667ad31cc5c\_MD5.png](assets/第4章%20目录IO和文件属性/753bd6ef8e181c698a4ee667ad31cc5c_MD5.png) 然后向该文件中添加以下内容：

```cpp
#include <stdio.h>

#include <stdlib.h>

#include <sys/types.h>

#include <sys/stat.h>

#include <fcntl.h>

#include <unistd.h>

#include <dirent.h>

#include <string.h>

 

int main(int argc, char *argv[])

{

    // 步骤一：定义变量

    int fd_src;                 // 源文件描述符

    int fd_obj;                 // 目标文件描述符

    char buf[32] = {0};         // 缓冲区

    char file_path[32] = {0};   // 文件路径

    char file_name[32] = {0};   // 文件名字

    ssize_t ret;                // 读取的字节数

    struct dirent *dir;         // 目录项

    DIR *dp;                    // 目录流指针

 

    // 步骤二：从键盘输入文件路径

    printf("Please enter the file path:\n");

    scanf("%s", file_path);

 

    // 步骤三：打开目录，获得目录流指针，并读取目录

    dp = opendir(file_path);    // 打开目录

    if (dp == NULL)

    {

        perror("opendir is error\n");

        return -1;

    }

    printf("opendir is ok\n");  // 输出提示信息

    while (1)                   // 循环读取目录项

    {

        dir = readdir(dp);      // 读取一个目录项

        if (dir != NULL)        // 如果目录项存在

        {

            printf("file name is %s\n", dir->d_name); // 输出目录项的名字

        }

        else                    // 如果目录项不存在

            break;              // 跳出循环

    }

 

    // 步骤四：获得文件的名字

    printf("Please enter the file name:\n");

    scanf("%s", file_name);

 

    // 步骤五：获得文件描述符

    fd_src = open(strcat(strcat(file_path, "/"), file_name), O_RDWR);  // 打开源文件

    if (fd_src < 0)

    {

        perror("open is error\n");

        return -2;

    }

    fd_obj = open(file_name, O_CREAT | O_RDWR, 0666);   // 打开或创建目标文件

    if (fd_obj < 0)

    {

        printf("open is error\n");

        return -3;

    }

 

    // 步骤六：读写操作

    while ((ret = read(fd_src, buf, 32)) != 0)    // 循环读取源文件

    {

        write(fd_obj, buf, ret);                 // 将读取到的数据写入目标文件

    }

 

    // 步骤七：关闭目录和文件

    close(fd_src);

    close(fd_obj);

    closedir(dp);

    return 0;

}
cpp
```

保存退出之后，使用以下命令对 demo18\_test.c进行编译，编译完成如下图所示：

> gcc -o demo18\_test demo18\_test.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/112d93e4044fdd1e65ee606e43b0ee28\_MD5.png](assets/第4章%20目录IO和文件属性/112d93e4044fdd1e65ee606e43b0ee28_MD5.png)

随后我们使用以下命令建立test测试文件夹，然后在test文件夹下建立test1、test2、test3三个文件，如下图所示：

> mkdir test
> 
> cd test/
> 
> touch test1
> 
> touch test2
> 
> touch test3

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/b48165695ea4ee11f7f5b413a812a40b\_MD5.png](assets/第4章%20目录IO和文件属性/b48165695ea4ee11f7f5b413a812a40b_MD5.png) 然后使用命令“./demo18\_test ”来运行，随后根据提示输入对应的路径和要复制的文件，运行成功如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/b5192e41291b3a182772878378afde3f\_MD5.png](assets/第4章%20目录IO和文件属性/b5192e41291b3a182772878378afde3f_MD5.png)

可以看到test1文件已经被成功复制到了当前目录下。

### 4.5获取文件属性

本小节代码在配套资料“ iTOP-3588开发板\\03\_【iTOP-RK3588开发板】指南教程\\03\_系统编程配套程序 \\19 ”目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/4664781991f58fd4b0864d908c7e789d\_MD5.png](assets/第4章%20目录IO和文件属性/4664781991f58fd4b0864d908c7e789d_MD5.png)

****学习前的疑问：****

1.获取文件属性要使用哪个系统调用呢？

2.stat()函数要怎样进行使用？

stat()函数用来获取文件属性，所使用的头文件和函数原型，如下所示：

|  | 所需头文件 | 函数原型 |
| --- | --- | --- |
| 1 | #include <sys/types.h>  #include <sys/stat.h>  #include <unistd.h> | int stat **(**const char **\*** pathname**,**struct stat **\*** buf**);** |

成功返回 0；失败返回-1，并设置 error。

stat()函数参数的含义如下所示：

|  | 参数名称 | 参数含义 |
| --- | --- | --- |
| 1 | pathname | 指定需要查看属性的文件路径。 |
| 2 | buf | 调用 stat 函数的时候需要传入 struct stat 变量的指针，获取到的文件属性信息就记录在 struct stat 结构体中。 |

struct stat 结构体中的所有元素加起来构成了文件的属性信息，结构体内容如下所示：

```cpp
struct stat

{

    dev_t st_dev; /* 文件所在设备的 ID */

    ino_t st_ino; /* 文件对应 inode 节点编号 */

    mode_t st_mode; /* 文件对应的模式 */

    nlink_t st_nlink; /* 文件的链接数 */    

    uid_t st_uid; /* 文件所有者的用户 ID */

    gid_t st_gid; /* 文件所有者的组 ID */

    dev_t st_rdev; /* 设备号（指针对设备文件） */

    off_t st_size; /* 文件大小（以字节为单位） */

    blksize_t st_blksize; /* 文件内容存储的块大小 */

    blkcnt_t st_blocks; /* 文件内容所占块数 */

    struct timespec st_atim; /* 文件最后被访问的时间 */

    struct timespec st_mtim; /* 文件内容最后被修改的时间 */

    struct timespec st_ctim; /* 文件状态最后被改变的时间 */

};
cpp
```

至此关于stat()函数的相关讲解就完成了，下面进行相应的实验。

****实验要求：****

使用stat()函数获取文件大小和 inode 编号并打印。

****实验步骤：****

首先进入到ubuntu的终端界面输入以下命令来创建demo19\_stat.c文件，如下图所示：

> vim demo19\_stat.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/dd506947de7cd5083b9d7e4f0a861f45\_MD5.png](assets/第4章%20目录IO和文件属性/dd506947de7cd5083b9d7e4f0a861f45_MD5.png) 然后向该文件中添加以下内容：

```cpp
#include <sys/types.h>   

#include <sys/stat.h>   

#include <unistd.h>     

#include <stdio.h>       

#include <stdlib.h>      

 

int main(int argc, char *argv[])

{

    struct stat file_stat;  // 声明一个用来存储文件状态的结构体变量

    int ret;                // 声明一个用来存储函数返回值的变量

    ret =stat("./test", &file_stat);   // 调用 stat 函数获取文件状态信息，并将结果存储到结构体变量中

    if (-1 == ret)         // 判断函数是否执行成功

    {

         printf("stat error");  // 如果执行失败，输出错误信息

         return -1;              // 并返回 -1

    }

    // 如果执行成功，输出文件大小和 inode 号

    printf("file size: %ld bytes\r\n inode number: %ld\n", file_stat.st_size,file_stat.st_ino);

    return 0;  // 返回 0，表示程序正常结束

}
cpp
```

第12行调用了stat()函数将文件属性保存到了file\_stat结构体中，在第19行对结构体中的inode值和size大小进行打印。

保存退出之后，使用以下命令对 demo19\_stat.c 进行编译，编译完成如下图所示：

> gcc -o demo19\_stat demo19\_stat.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/316645e987ec1c268cd4f501a0a1a204\_MD5.png](assets/第4章%20目录IO和文件属性/316645e987ec1c268cd4f501a0a1a204_MD5.png)

然后使用命令“ vim test ”创建test文件，并添加以下内容：

> hello world!!

添加完成如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074\_MD5.png](assets/第4章%20目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074_MD5.png)

> hello world!!

添加完成如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074\_MD5.png](assets/第4章%20目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074_MD5.png)

保存退出之后，使用“ ls -li ”命令查看文件属性，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/74ba65d7d14fd094a74d833b3714f445\_MD5.png](assets/第4章%20目录IO和文件属性/74ba65d7d14fd094a74d833b3714f445_MD5.png)

可以看到inode值为30155639，大小为14。然后使用命令“./demo19\_stat ”来运行，运行成功如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/a0eb434f30e9b7dcd14240e908660082\_MD5.png](assets/第4章%20目录IO和文件属性/a0eb434f30e9b7dcd14240e908660082_MD5.png)

可以看到程序运行成功之后，打印出了文件大小和inode值。

### 4.6检查文件权限

本小节代码在配套资料“ iTOP-3588开发板\\03\_【iTOP-RK3588开发板】指南教程\\03\_系统编程配套程序 \\20 ”目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/b0c3d529e2d0ded950046d831b2cd3fd\_MD5.png](assets/第4章%20目录IO和文件属性/b0c3d529e2d0ded950046d831b2cd3fd_MD5.png)

****学习前的疑问：****

1.检查文件权限要使用哪个系统调用呢？

2.access()函数要怎样进行使用？

access()函数用来对文件权限进行检查，所使用的头文件和函数原型，如下所示：

|  | 所需头文件 | 函数原型 |
| --- | --- | --- |
| 1 | #include <unistd.h> | int access **(**const char **\*** pathname**,**int mode**);** |

检查项通过则返回 0，表示拥有相应的权限并且文件存在；否则返回-1，如果多个检查项组合在一起，只要其中任何一项不通过都会返回-1。

access()函数参数含义如下所示：

|  | 参数名称 | 参数含义 |
| --- | --- | --- |
| 1 | pathname | 文件或目录的路径名 |
| 2 | mode | 是要检查的权限模式 |

mode参数可以取以下值之一：

|  | 取值 | 取值含义 |
| --- | --- | --- |
| 1 | F\_OK： | 检查文件或目录是否存在。 |
| 2 | R\_OK： | 检查文件或目录是否可读。 |
| 3 | W\_OK： | 检查文件或目录是否可写。 |
| 4 | X\_OK： | 检查文件或目录是否可执行。 |

至此关于access()函数的相关讲解就完成了，下面进行相应的实验。

****实验要求：****

通过 access 函数检查文件是否存在，若存在、则继续检查执行进程的用户对该文件是否有读、写、执行权限。

****实验步骤：****

首先进入到ubuntu的终端界面输入以下命令来创建demo20\_access.c文件，如下图所示：

> vim demo20\_access.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/4dbcfee75ff5fe678121e30f7ee84dd0\_MD5.png](assets/第4章%20目录IO和文件属性/4dbcfee75ff5fe678121e30f7ee84dd0_MD5.png)

然后向该文件中添加以下内容，

```cpp
#include <unistd.h>   

#include <stdio.h>   

#include <stdlib.h>   

 

int main(int argc,char *argv[])

{

    int ret;  // 声明一个用来存储函数返回值的变量

    ret = access("./test", F_OK);  // 调用 access 函数检查文件是否存在，并将结果存储到 ret 变量中

    if (-1 == ret)  // 判断文件是否存在

    {

        printf("file does not exist.\n");  // 如果文件不存在，输出相应的信息

        return -1;  // 并返回 -1

    }

    else

        printf("file exist\n");  // 如果文件存在，输出相应的信息

    ret = access("./test", R_OK);  // 检查文件是否具有读权限

    if (!ret)

        printf("是否有读权限: 有\n");

    else

        printf("是否有读权限: 无\n");

    ret = access("./test", W_OK);  // 检查文件是否具有写权限

    if (!ret)

        printf("是否有写权限: 有\n");

    else

        printf("是否有写权限: 无\n");

    ret = access("./test", X_OK);  // 检查文件是否具有执行权限

    if (!ret)

        printf("是否有执行权限: 有\n");

    else

        printf("是否有执行权限: 无\n");

    return 0;  // 返回 0，表示程序正常结束

}
cpp
```

第8行、第17行、第22行、第27行，分别调用了acces()函数，第一个参数为要检查属性的文件名，第二个属性为要检查的属性值，根据返回值来进行属性的判断。

保存退出之后，使用以下命令对demo20\_access.c进行编译，编译完成如下图所示：

> gcc -o demo20\_access demo20\_access.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/a9b77c4ac6dfbcc3c2644501abcd724f\_MD5.png](assets/第4章%20目录IO和文件属性/a9b77c4ac6dfbcc3c2644501abcd724f_MD5.png)

然后使用命令“ vim test ”创建test文件，并添加以下内容：

> hello world!!

添加完成如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074\_MD5.png](assets/第4章%20目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074_MD5.png) 然后使用命令“ ls -l ”来查看文件属性，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/f089eb6c1090ea027ff1b7d1d16dfd4b\_MD5.png](assets/第4章%20目录IO和文件属性/f089eb6c1090ea027ff1b7d1d16dfd4b_MD5.png)

从上图可以看到文件的读写权限为可读可写不具备执行权限，然后使用命令“./demo20\_access ”来运行，运行成功如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/b5f8a570582a9244ef158acdc3720a09\_MD5.png](assets/第4章%20目录IO和文件属性/b5f8a570582a9244ef158acdc3720a09_MD5.png)

可以看到程序运行成功之后，会打印对应的权限信息。

### 4.7修改文件权限

本小节代码在配套资料“ iTOP-3588开发板\\03\_【iTOP-RK3588开发板】指南教程\\03\_系统编程配套程序 \\21 ”目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/98cdbe009ecef62a72f04198c22a5039\_MD5.png](assets/第4章%20目录IO和文件属性/98cdbe009ecef62a72f04198c22a5039_MD5.png)

****学习前的疑问：****

1.修改文件权限要使用哪个系统调用呢？

2.chmod()函数要怎样进行使用？

chmod()函数用来对文件权限进行修改，所使用的头文件和函数原型，如下所示：

|  | 所需头文件 | 函数原型 |
| --- | --- | --- |
| 1 | #include <sys/stat.h> | int chmod **(**const char **\*** pathname**,** mode\_t mode**);** |

成功返回 0；失败返回-1，并设置 errno。

chmod()函数参数含义如下所示：

|  | 参数名称 | 参数含义 |
| --- | --- | --- |
| 1 | pathname | 需要进行权限修改的文件路径，若该参数所指为符号链接，实际改变权限的文件是符号链接所指向的文件，而不是符号链接文件本身 |
| 2 | mode | 权限掩码，对不同用户和组设置可执行，读，写权限，使用八进制数表示 |

至此关于chmod()函数的相关讲解就完成了，下面进行相应的实验。

****实验要求：****

通过标准IO创建一个可以读写名为test的文件，并使用chmod()函数修改其权限为777。

****实验步骤：****

首先进入到ubuntu的终端界面输入以下命令来创建demo21\_chmod.c文件，如下图所示：

> vim demo21\_chmod.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/6424d736d928e76501972438122f8d4b\_MD5.png](assets/第4章%20目录IO和文件属性/6424d736d928e76501972438122f8d4b_MD5.png) 然后向该文件中添加以下内容，

```cpp
#include <stdio.h>

#include <sys/stat.h>

 

int main(int argc, char *argv[])

{

    int ret;

    ret = chmod("./test", 0777);    // 将指定文件的权限设置为 0777，即读、写、执行权限都为最高

 

    if (ret == -1)    // 如果修改权限失败，则输出错误信息并返回 -1，表示程序异常终止

    {

        perror("chmod error");

        return -1;

    }

 

    return 0;    // 修改权限成功，返回 0，表示程序正常结束

}
cpp
```

需要注意的地方只有第7行，调用了chmod()函数，对test文件进行权限的修改，修改权限为777。

保存退出之后，使用以下命令对demo21\_chmod.c进行编译，编译完成如下图所示：

> gcc -o demo21\_chmod demo21\_chmod.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/6d6c49d4fb500951fda42228157a38d4\_MD5.png](assets/第4章%20目录IO和文件属性/6d6c49d4fb500951fda42228157a38d4_MD5.png)

然后使用命令“ vim test ”创建test文件，并添加以下内容：

> hello world!!

添加完成如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074\_MD5.png](assets/第4章%20目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074_MD5.png) 然后使用命令“ ls -l ”来查看文件属性，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/19f68645e8f8a6a7c835d52f5b28285c\_MD5.png](assets/第4章%20目录IO和文件属性/19f68645e8f8a6a7c835d52f5b28285c_MD5.png)

然后使用命令“./demo21\_chmod ”来运行，运行成功如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/c65ba1155c925c1ffd2610aea76b950d\_MD5.png](assets/第4章%20目录IO和文件属性/c65ba1155c925c1ffd2610aea76b950d_MD5.png)

可以看到程序运行成功之后，test文件的权限已经被修改为了777。

### 4.8软链接与硬链接

软链接（Symbolic Link）和硬链接（Hard Link）都是用于在文件系统中创建一个文件或目录的方法。它们的作用是使多个文件或目录共享同一块数据，从而节省磁盘空间和提高效率。但是，它们的实现方式不同，因此它们的特点和用法也有所不同。

****软链接****

软链接是一种特殊的文件类型，它是一个指向另一个文件或目录的快捷方式。软链接文件本身并不包含任何实际的数据，而是指向另一个文件或目录的路径。软链接可以跨越文件系统边界，并且可以指向不存在的文件或目录。

软链接的创建方式是使用ln命令，并使用参数-s来指定创建软链接。例如，下面的命令创建了一个名为"link\_to\_file"的软链接，它指向名为"file.txt"的文件：

ln -s file.txt link\_to\_file

软链接的特点：

1）软链接文件本身并不包含任何实际的数据，只是一个指向其他文件或目录的路径。

2）软链接可以跨越文件系统边界，因此可以指向另一个文件系统中的文件或目录。

3）软链接可以指向不存在的文件或目录。

4）软链接的权限和所有权都由其指向的文件或目录决定。

****硬链接****

硬链接是一种通过文件系统中的索引节点（Inode）来创建的链接。硬链接的本质是在文件系统中为同一文件或目录创建多个名称，它们共享同一块数据。硬链接只能在同一文件系统中创建，并且不能指向目录。

硬链接的创建方式是使用ln命令，并不使用-s参数。例如，下面的命令创建了一个名为"link\_to\_file"的硬链接，它指向名为"file.txt"的文件：

ln file.txt link\_to\_file

硬链接的特点：

1）硬链接创建的是同一个文件或目录的多个名称，它们共享同一块数据。

2）硬链接只能在同一文件系统中创建，因为不同的文件系统使用不同的索引节点。

3）硬链接不能指向目录。

删除硬链接不会影响其指向的文件或目录，只有当所有硬链接和原文件或目录都被删除后，才会真正释放磁盘空间。

至此，对于软链接和硬链接的介绍就完成了，那如何在系统编程中对软链接和硬链接进行创建呢，下面让我们一起进入本章节的学习吧。

#### 4.8.1 创建硬链接

本小节代码在配套资料“ iTOP-3588开发板\\03\_【iTOP-RK3588开发板】指南教程\\03\_系统编程配套程序 \\22 ”目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/5669ebb87597415c191d4d2eafa9de76\_MD5.png](assets/第4章%20目录IO和文件属性/5669ebb87597415c191d4d2eafa9de76_MD5.png)

****学习前的疑问：****

1.硬链接的创建要使用哪个系统调用呢？

2.link()函数要怎样进行使用？

link()函数用来对硬链接进行创建，所使用的头文件和函数原型，如下所示：

|  | 所需头文件 | 函数原型 |
| --- | --- | --- |
| 1 | #include <unistd.h> | int link **(**const char **\*** oldpath**,**const char **\*** newpath**);** |

函数调用成功返回 0；失败将返回-1，并且会设置 errno。

link()函数参数含义如下所示：

|  | 参数名称 | 参数含义 |
| --- | --- | --- |
| 1 | oldpath | 用于指定被链接的源文件路径 |
| 2 | newpath | 用于指定硬链接文件路径，如果newpath指定的文件路径已存在，则会产生错误 |

至此关于link()函数的相关讲解就完成了，下面进行相应的实验。

****实验要求：****

通过 link函数创建test函数的硬链接hard。

****实验步骤：****

首先进入到ubuntu的终端界面输入以下命令来创建demo22\_link.c文件，如下图所示：

> vim demo22\_link.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/01f8a892c8de73f7a3f19842440a1fa7\_MD5.png](assets/第4章%20目录IO和文件属性/01f8a892c8de73f7a3f19842440a1fa7_MD5.png) 然后向该文件中添加以下内容，：

```cpp
#include <stdio.h>

#include <stdlib.h>

#include <unistd.h>

 

int main(int argc,char *argv[])

{

    int ret;

    ret = link("./test", "./hard");    // 创建一个硬链接，将 test 文件的链接名设置为 hard

 

    if (ret == -1)     // 如果创建链接失败，则输出错误信息并返回 -1，表示程序异常终止

    {

        perror("link error");

        return -1;

    }

 

    return 0;    // 创建链接成功，返回 0，表示程序正常结束

}
cpp
```

在第8行使用了link()函数，第一个参数为源文件名称，第二个参数为我们要创建的硬链接文件名称为hard。

保存退出之后，使用以下命令对demo22\_link.c进行编译，编译完成如下图所示：

> gcc -o demo22\_link demo22\_link.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/959169034358dac5eb74a9818a9c5bee\_MD5.png](assets/第4章%20目录IO和文件属性/959169034358dac5eb74a9818a9c5bee_MD5.png)

然后使用命令“ vim test ”创建test文件，并添加以下内容：

> hello world!!

添加完成如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074\_MD5.png](assets/第4章%20目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074_MD5.png) 保存退出之后，使用命令“./demo22\_link ”来运行，创建test文件的硬连接文件hard，运行成功如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/9cd60e051f6d5c1d74c51e884580549b\_MD5.png](assets/第4章%20目录IO和文件属性/9cd60e051f6d5c1d74c51e884580549b_MD5.png)

可以看到hard文件也被成功创建了，且test和hard的inode号相同，证明我们的硬链接创建成功了。

#### 4.8.2 创建软链接

本小节代码在配套资料“ iTOP-3588开发板\\03\_【iTOP-RK3588开发板】指南教程\\03\_系统编程配套程序 \\23 ”目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/c17057497b13759b71e2414120bc8fa5\_MD5.png](assets/第4章%20目录IO和文件属性/c17057497b13759b71e2414120bc8fa5_MD5.png)

****学习前的疑问：****

1.软链接的创建要使用哪个系统调用呢？

2.symlink()函数要怎样进行使用？

symlink()用来创建软链接，所使用的头文件和函数原型，如下所示：

|  | 所需头文件 | 函数原型 |
| --- | --- | --- |
| 1 | #include <unistd.h> | int symlink **(**const char **\*** target**,**const char **\*** linkpath**);** |

调用成功时返回 0；失败将返回-1，并会设置 errno。

symlink()函数参数含义如下所示：

|  | 参数名称 | 参数含义 |
| --- | --- | --- |
| 1 | target | 软链接指向的目标文件或目录的路径 |
| 2 | linkpath | 新创建的软链接的路径。 |

至此关于fread()函数的相关讲解就完成了，下面进行相应的实验。

****实验要求：****

通过symlink()函数创建test文件的软链接soft。

****实验步骤：****

首先进入到ubuntu的终端界面输入以下命令来创建demo23\_symlink.c文件，如下图所示：

> vim demo23\_symlink.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/b0cfae49fc1e0be646f5cf2dee228302\_MD5.png](assets/第4章%20目录IO和文件属性/b0cfae49fc1e0be646f5cf2dee228302_MD5.png) 然后向该文件中添加以下内容，

```cpp
#include <stdio.h>

#include <stdlib.h>

#include <unistd.h>

 

int main(int argc, char *argv[])

{

    int ret;

    ret = symlink("./test", "./soft");    // 创建一个软链接，将 test 文件的链接名设置为 soft

    

    if (ret == -1)     // 如果创建链接失败，则输出错误信息并返回 -1，表示程序异常终止

    {

        perror("link error\n");

        return -1;

    }

 

    return 0;    // 创建链接成功，返回 0，表示程序正常结束

}
cpp
```

保存退出之后，使用以下命令对demo23\_symlink.c进行编译，编译完成如下图所示：

> gcc -o demo23\_symlink demo23\_symlink.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/c85ae0de56d7605502bafe4192eb6403\_MD5.png](assets/第4章%20目录IO和文件属性/c85ae0de56d7605502bafe4192eb6403_MD5.png)

然后使用命令“ vim test ”创建test文件，并添加以下内容：

> hello world!!

添加完成如下图所示：

然后使用命令“./demo23\_symlink ”来运行创建test的软链接，运行成功如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/d267dda93a38e1e7e7d774a0c8f6f8aa\_MD5.png](assets/第4章%20目录IO和文件属性/d267dda93a38e1e7e7d774a0c8f6f8aa_MD5.png)

可以看到程序运行成功之后，soft文件被成功创建，使用“ ls -l ”查看文件属性，可以看到sotf文件是test文件的软链接。

#### 4.8.3 读取软链接文件路径

本小节代码在配套资料“ iTOP-3588开发板\\03\_【iTOP-RK3588开发板】指南教程\\03\_系统编程配套程序 \\24 ”目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/58a52bc16da55455f79f40f9ffa56776\_MD5.png](assets/第4章%20目录IO和文件属性/58a52bc16da55455f79f40f9ffa56776_MD5.png)

****学习前的疑问：****

1.读取软链接文件路径要使用哪个系统调用呢？

2.readlink()函数要怎样进行使用？

readlink()函数用来对软链接的源文件路径进行读取，所使用的头文件和函数原型，如下图所示：

|  | 所需头文件 | 函数原型 |
| --- | --- | --- |
| 1 | #include <unistd.h> | ssize\_t readlink **(**const char **\*** pathname**,**char **\*** buf**,**size\_t bufsiz**);** |

函数调用成功之后将返回读取到的字节数。失败将返回-1，并会设置 errno。

readlink()函数参数含义如下所示：

|  | 参数名称 | 参数含义 |
| --- | --- | --- |
| 1 | pathname | 需要读取的软链接文件路径。只能是软链接文件路径，不能是其它类型文件，否则调用函数将报错。 |
| 2 | buf | 用于存放路径信息的缓冲区。 |
| 3 | bufsiz | 读取大小，一般读取的大小需要大于链接文件数据块中存储的文件路径信息字节大小。 |

至此关于readlink()函数的相关讲解就完成了，下面进行相应的实验。

****实验要求：****

通过readlink()函数读取软链接源文件的路径并打印。

****实验步骤：****

首先进入到ubuntu的终端界面输入以下命令来创建demo24\_readlink.c文件，如下图所示：

> vim demo24\_readlink.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/48887453df5381f28486771bbad16ec4\_MD5.png](assets/第4章%20目录IO和文件属性/48887453df5381f28486771bbad16ec4_MD5.png) 然后向该文件中添加以下内容:

```cpp
#include <stdio.h>

#include <stdlib.h>

#include <unistd.h>

 

int main(int argc, char *argv[])

{

    char buf[50];  // 用于存储读取到的软链接文件内容

    int ret;

    ret = readlink("./soft", buf, sizeof(buf)); //读取软链接文件 "./soft" 的内容，存储到 buf 中

if (ret == -1)  // 如果读取失败，输出错误信息并返回 -1

{

    perror("readlink error");

    return -1;

}

printf("%s\n", buf);  // 打印读取到的软链接文件内容

return 0;

}
cpp
```

保存退出之后，使用以下命令对demo24\_readlink.c进行编译，编译完成如下图所示：

> gcc -o demo24\_readlink demo24\_readlink.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/8c315b74deecf4742d862b88f6629cbe\_MD5.png](assets/第4章%20目录IO和文件属性/8c315b74deecf4742d862b88f6629cbe_MD5.png)

然后使用命令“ vim test ”创建test文件，并添加以下内容：

> hello world!!

添加完成如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074\_MD5.png](assets/第4章%20目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074_MD5.png) 保存退出之后，使用以下命令来创建test文件的软链接文件soft，创建成功如下图所示:

> ln -s test soft

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/19c8624f1d535dcd666cd27fc6388b89\_MD5.png](assets/第4章%20目录IO和文件属性/19c8624f1d535dcd666cd27fc6388b89_MD5.png) 然后使用命令“./demo24\_ readlink ”来运行该程序，运行成功如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/5544c137a2b39adf25ac1ab6c7280fa5\_MD5.png](assets/第4章%20目录IO和文件属性/5544c137a2b39adf25ac1ab6c7280fa5_MD5.png)

可以看到程序运行成功之后，会打印soft软链接文件的本身文件test。

### 4.9文件删除

#### 4.9.1 删除文件(系统调用)

本小节代码在配套资料“ iTOP-3588开发板\\03\_【iTOP-RK3588开发板】指南教程\\03\_系统编程配套程序 \\25 ”目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/a0414ca6ab73c7958fe8050606bba175\_MD5.png](assets/第4章%20目录IO和文件属性/a0414ca6ab73c7958fe8050606bba175_MD5.png)

****学习前的疑问：****

1.文件删除要使用哪个系统调用呢？

2.unlink()函数要怎样进行使用？

unlink()函数用于删除指定的文件或目录，所使用的头文件和函数原型，如下所示：

|  | 所需头文件 | 函数原型 |
| --- | --- | --- |
| 1 | #include <unistd.h> | int unlink **(**const char **\*** pathname**);** |

函数调用成功时返回 0；失败将返回-1，并设置 errno。

unlink()函数的参数含义如下所示：

|  | 参数名称 | 参数含义 |
| --- | --- | --- |
| 1 | pathname | 要删除的文件或目录的路径 |

至此关于fread()函数的相关\`讲解就完成了，下面进行相应的实验。

****函数功能：****

unlink()系统调用，用于移除/删除一个硬链接（从其父级目录下删除该目录条目）。

****头文件和函数原型：****

| #include <unistd.h>  int unlink **(**const char **\*** pathname**);** |
| --- |

****参数含义：****

****pathname：**** 需要删除的文件路径，可使用相对路径、也可使用绝对路径，如果 pathname 参数指定的文件不存在，则调用 unlink()失败 。

****返回值**** ：

成功返回 0；失败将返回-1，并设置 errno。

****实验要求：****

通过unlink()函数删除test硬链接文件。

****实验步骤：****

首先进入到ubuntu的终端界面输入以下命令来创建demo25\_unlink.c文件，如下图所示：

> vim demo25\_unlink.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/060aeb88bfd08918a751d5cb6f015ec5\_MD5.png](assets/第4章%20目录IO和文件属性/060aeb88bfd08918a751d5cb6f015ec5_MD5.png) 然后向该文件中添加以下内容，、

```cpp
#include <stdio.h>

#include <stdlib.h>

#include <unistd.h>

 

int main(int argc, char *argv[])

{

    int ret;

 

    ret = unlink("./test");    // 使用unlink函数删除指定的文件

    if (ret == -1)

    {

        perror("unlink error");

        return -1;

    }

    return 0;

}
cpp
```

保存退出之后，使用以下命令对demo25\_unlink.c进行编译，编译完成如下图所示：

> gcc -o demo25\_unlink demo25\_unlink.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/a6a231453866e9bea3723f66cc361009\_MD5.png](assets/第4章%20目录IO和文件属性/a6a231453866e9bea3723f66cc361009_MD5.png)

然后使用命令“ vim test ”创建test文件，并添加以下内容：

> hello world!!

添加完成如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074\_MD5.png](assets/第4章%20目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074_MD5.png) 保存退出之后，使用命令“./demo25\_unlink ”来运行该程序，运行成功如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/6390bc9eb9e0ae3463fd156ce66e1693\_MD5.png](assets/第4章%20目录IO和文件属性/6390bc9eb9e0ae3463fd156ce66e1693_MD5.png)

程序运行成功之后，会发现test文件被删除了，至此，关于unlink函数的实验就完成了。

#### 4.9.2 删除文件(C库函数)

本小节代码在配套资料“ iTOP-3588开发板\\03\_【iTOP-RK3588开发板】指南教程\\03\_系统编程配套程序 \\26 ”目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/ec6cea19e049ea949f16fad927fbb484\_MD5.png](assets/第4章%20目录IO和文件属性/ec6cea19e049ea949f16fad927fbb484_MD5.png)

****学习前的疑问：****

1. remove()函数要怎样进行使用？
2. 为什么要学习remove()函数

remove函数与unlink函数类似，用于删除指定的文件。不同之处在于，remove函数可以删除指定路径下的任意类型的文件，包括普通文件、目录等。如果要删除非空目录，remove函数会自动递归删除其下的所有文件和子目录。

remove函数所使用的头文件和函数原型，如下所示：

|  | 所需头文件 | 函数原型 |
| --- | --- | --- |
| 1 | #include <stdio.h> | int remove **(**const char **\*** pathname**);** |

调用成功时成功返回 0，失败将返回-1，并设置 errno。

remove()函数参数含义如下所示：

|  | 参数名称 | 参数含义 |
| --- | --- | --- |
| 1 | pathname | 要删除的文件或目录的路径 |

需要注意的是，与unlink函数类似，删除文件操作也是不可逆的，因此在使用remove函数时，应该谨慎处理，避免误删重要文件。如果需要保留备份或是恢复删除的文件，可以在删除文件之前先备份文件。另外，需要注意的是，删除文件操作需要有足够的权限，否则会删除失败。

至此关于remove()函数的相关讲解就完成了，下面进行相应的实验。

****实验要求：****

本代码所要实现的目标为通过remove()函数删除test文件。

****实验步骤：****

首先进入到ubuntu的终端界面输入以下命令来创建demo26\_remove.c文件，如下图所示：

> vim demo26\_remove.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/473ef32dd0364617418ce8d104b0c60c\_MD5.png](assets/第4章%20目录IO和文件属性/473ef32dd0364617418ce8d104b0c60c_MD5.png) 然后向该文件中添加以下内容

```cpp
#include <stdio.h>

#include <stdlib.h>

#include <unistd.h>

 

int main(int argc, char *argv[])

{

    int ret; // 存储函数调用结果的变量

    ret = remove("./test"); // 调用 remove 函数删除名为 "test" 的文件

    if (ret == -1) // 如果返回值为 -1，说明删除文件失败

    {

        perror("remove error"); // 输出错误信息

        return -1; // 返回错误代码

    }

    return 0; // 删除成功，返回 0

}
cpp
```

保存退出之后，使用以下命令 对demo26\_remove.c进行编译，编译完成如下图所示：

> gcc -o demo26\_remove demo26\_remove.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/ff693507b85c8c1fb4d174eed8015741\_MD5.png](assets/第4章%20目录IO和文件属性/ff693507b85c8c1fb4d174eed8015741_MD5.png)

然后使用命令“ vim test ”创建test文件，并添加以下内容：

> hello world!!

添加完成如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074\_MD5.png](assets/第4章%20目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074_MD5.png) 保存退出之后，使用命令“./demo26\_remove ”来运行该程序，运行成功如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/c44ae3547943108fa5e4dfc9e5a535be\_MD5.png](assets/第4章%20目录IO和文件属性/c44ae3547943108fa5e4dfc9e5a535be_MD5.png)

程序运行成功之后，会发现test文件被删除了。

### 4.10文件重命名

本小节代码在配套资料“ iTOP-3588开发板\\03\_【iTOP-RK3588开发板】指南教程\\03\_系统编程配套程序 \\27 ”目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/7189e79c7ed3bfe59015a02f2285d1d5\_MD5.png](assets/第4章%20目录IO和文件属性/7189e79c7ed3bfe59015a02f2285d1d5_MD5.png)

****学习前的疑问：****

1.文件重命名要使用哪个C语言库函数？

2.rename()函数要怎样进行使用？

在系统编程中使用rename()函数对文件进行重命名，所使用的头文件和函数原型，如下所示：

|  | 所需头文件 | 函数原型 |
| --- | --- | --- |
| 1 | #include <stdio.h> | int rename **(**const char **\*** oldpath**,**const char **\*** newpath**);** |

函数调用成功返回 0，失败将返回-1，并设置 errno。

rename()函数参数含义如下所示：

|  | 参数名称 | 参数含义 |
| --- | --- | --- |
| 1 | oldpath | 原文件路径 |
| 2 | newpath | 新文件路径 |

至此关于rename()函数的相关讲解就完成了，下面进行相应的实验。

****实验要求：****

通过rename()函数将test文件名修改为new\_file。

****实验步骤：****

首先进入到ubuntu的终端界面输入以下命令来创建demo27\_rename.c文件，如下图所示：

> vim demo27\_rename.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/10b10f1393ed242241a260098ef77fcf\_MD5.png](assets/第4章%20目录IO和文件属性/10b10f1393ed242241a260098ef77fcf_MD5.png) 然后向该文件中添加以下内容：

```cpp
#include <stdio.h>

#include <stdlib.h>

#include <unistd.h>

 

int main(int argc, char *argv[])

{

 

    int ret;    // 定义一个变量 ret 来存储操作结果

    ret = rename("./test", "./new_file");    // 调用 rename 函数，将文件名为“test”的文件重命名为“new_file”

 

    if (ret == -1)    // 如果重命名失败，输出错误信息并返回 -1

    {

        perror("rename error");

        return -1;

    }

 

    return 0;    // 重命名成功，返回 0

}
cpp
```

保存退出之后，使用以下命令对demo27\_rename.c进行编译，编译完成如下图所示：

> gcc -o demo27\_rename demo27\_rename.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/6c2f1675e5c55ef33997e85bca825ee7\_MD5.png](assets/第4章%20目录IO和文件属性/6c2f1675e5c55ef33997e85bca825ee7_MD5.png)

然后使用命令“ vim test ”创建test文件，并添加以下内容：

> hello world!!

添加完成如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074\_MD5.png](assets/第4章%20目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074_MD5.png) 保存退出之后，使用命令“./demo27\_rename ”来运行该程序，运行成功如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/05173586784a7d2f22251c897d381583\_MD5.png](assets/第4章%20目录IO和文件属性/05173586784a7d2f22251c897d381583_MD5.png)

程序运行成功之后，会发现test文件已经更名为了new\_file。至此关于rename()函数的实验就完成了。

微信公众号

内容来源：csdn.net

作者昵称：北京迅为

原文链接：https://blog.csdn.net/BeiJingXunWei/article/details/137584869

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

隐藏侧栏 ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/90bd0cbf3aff8fdff8bf9b011b581e20\_MD5.png](assets/第4章%20目录IO和文件属性/90bd0cbf3aff8fdff8bf9b011b581e20_MD5.png)

程序员都在用的中文IT技术交流社区

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/08a47e60886378fe60a3d9c8f4ae8bc6\_MD5.png](assets/第4章%20目录IO和文件属性/08a47e60886378fe60a3d9c8f4ae8bc6_MD5.png)

专业的中文 IT 技术社区，与千万技术人共成长

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/a51be6c085b867a5bd82d8dc1cea9b46\_MD5.png](assets/第4章%20目录IO和文件属性/a51be6c085b867a5bd82d8dc1cea9b46_MD5.png)

关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！

客服 返回顶部

微信公众号

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/efb7921311640694e61fee00900550d6\_MD5.jpg](assets/第4章%20目录IO和文件属性/efb7921311640694e61fee00900550d6_MD5.jpg) 公众号名称：迅为电子 微信扫码关注或搜索公众号名称

复制公众号名称

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/a1841f166717d53b677779eb28e3e3e4\_MD5.png](assets/第4章%20目录IO和文件属性/a1841f166717d53b677779eb28e3e3e4_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/9459e5bea1c4519217e220fd8973d906\_MD5.png](assets/第4章%20目录IO和文件属性/9459e5bea1c4519217e220fd8973d906_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/6d158a28f105388f527de90abaf9343f\_MD5.png](assets/第4章%20目录IO和文件属性/6d158a28f105388f527de90abaf9343f_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/ed9df847e525a93deb412e552b3de758\_MD5.png](assets/第4章%20目录IO和文件属性/ed9df847e525a93deb412e552b3de758_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/e628b79944a869adf9aa815f67ed939f\_MD5.png](assets/第4章%20目录IO和文件属性/e628b79944a869adf9aa815f67ed939f_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/e3dbc15c4bbb592d23d77762c7b54ebb\_MD5.png](assets/第4章%20目录IO和文件属性/e3dbc15c4bbb592d23d77762c7b54ebb_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/bbd26a9517cdb52751a75dde20233e38\_MD5.png](assets/第4章%20目录IO和文件属性/bbd26a9517cdb52751a75dde20233e38_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/172f2128ac7092b4ff88abaa41a0fdf3\_MD5.png](assets/第4章%20目录IO和文件属性/172f2128ac7092b4ff88abaa41a0fdf3_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/6e10484de92a15192beb3b7bbaf08eba\_MD5.png](assets/第4章%20目录IO和文件属性/6e10484de92a15192beb3b7bbaf08eba_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/db075fef63be7eeb147fbe85878fd0de\_MD5.png](assets/第4章%20目录IO和文件属性/db075fef63be7eeb147fbe85878fd0de_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/117cffdd858b111af728bba7f374422c\_MD5.png](assets/第4章%20目录IO和文件属性/117cffdd858b111af728bba7f374422c_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/866143712f50edd33a05a6749571c02f\_MD5.png](assets/第4章%20目录IO和文件属性/866143712f50edd33a05a6749571c02f_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/e30480de106b60b81aceee36d8b4f535\_MD5.png](assets/第4章%20目录IO和文件属性/e30480de106b60b81aceee36d8b4f535_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/fd0a4c91e7390fae6d5b169c6710fa6c\_MD5.png](assets/第4章%20目录IO和文件属性/fd0a4c91e7390fae6d5b169c6710fa6c_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/753bd6ef8e181c698a4ee667ad31cc5c\_MD5.png](assets/第4章%20目录IO和文件属性/753bd6ef8e181c698a4ee667ad31cc5c_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/112d93e4044fdd1e65ee606e43b0ee28\_MD5.png](assets/第4章%20目录IO和文件属性/112d93e4044fdd1e65ee606e43b0ee28_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/b48165695ea4ee11f7f5b413a812a40b\_MD5.png](assets/第4章%20目录IO和文件属性/b48165695ea4ee11f7f5b413a812a40b_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/b5192e41291b3a182772878378afde3f\_MD5.png](assets/第4章%20目录IO和文件属性/b5192e41291b3a182772878378afde3f_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/4664781991f58fd4b0864d908c7e789d\_MD5.png](assets/第4章%20目录IO和文件属性/4664781991f58fd4b0864d908c7e789d_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/dd506947de7cd5083b9d7e4f0a861f45\_MD5.png](assets/第4章%20目录IO和文件属性/dd506947de7cd5083b9d7e4f0a861f45_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/316645e987ec1c268cd4f501a0a1a204\_MD5.png](assets/第4章%20目录IO和文件属性/316645e987ec1c268cd4f501a0a1a204_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074\_MD5.png](assets/第4章%20目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074\_MD5.png](assets/第4章%20目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/74ba65d7d14fd094a74d833b3714f445\_MD5.png](assets/第4章%20目录IO和文件属性/74ba65d7d14fd094a74d833b3714f445_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/a0eb434f30e9b7dcd14240e908660082\_MD5.png](assets/第4章%20目录IO和文件属性/a0eb434f30e9b7dcd14240e908660082_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/b0c3d529e2d0ded950046d831b2cd3fd\_MD5.png](assets/第4章%20目录IO和文件属性/b0c3d529e2d0ded950046d831b2cd3fd_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/4dbcfee75ff5fe678121e30f7ee84dd0\_MD5.png](assets/第4章%20目录IO和文件属性/4dbcfee75ff5fe678121e30f7ee84dd0_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/a9b77c4ac6dfbcc3c2644501abcd724f\_MD5.png](assets/第4章%20目录IO和文件属性/a9b77c4ac6dfbcc3c2644501abcd724f_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074\_MD5.png](assets/第4章%20目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/f089eb6c1090ea027ff1b7d1d16dfd4b\_MD5.png](assets/第4章%20目录IO和文件属性/f089eb6c1090ea027ff1b7d1d16dfd4b_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/b5f8a570582a9244ef158acdc3720a09\_MD5.png](assets/第4章%20目录IO和文件属性/b5f8a570582a9244ef158acdc3720a09_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/98cdbe009ecef62a72f04198c22a5039\_MD5.png](assets/第4章%20目录IO和文件属性/98cdbe009ecef62a72f04198c22a5039_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/6424d736d928e76501972438122f8d4b\_MD5.png](assets/第4章%20目录IO和文件属性/6424d736d928e76501972438122f8d4b_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/6d6c49d4fb500951fda42228157a38d4\_MD5.png](assets/第4章%20目录IO和文件属性/6d6c49d4fb500951fda42228157a38d4_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074\_MD5.png](assets/第4章%20目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/19f68645e8f8a6a7c835d52f5b28285c\_MD5.png](assets/第4章%20目录IO和文件属性/19f68645e8f8a6a7c835d52f5b28285c_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/c65ba1155c925c1ffd2610aea76b950d\_MD5.png](assets/第4章%20目录IO和文件属性/c65ba1155c925c1ffd2610aea76b950d_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/5669ebb87597415c191d4d2eafa9de76\_MD5.png](assets/第4章%20目录IO和文件属性/5669ebb87597415c191d4d2eafa9de76_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/01f8a892c8de73f7a3f19842440a1fa7\_MD5.png](assets/第4章%20目录IO和文件属性/01f8a892c8de73f7a3f19842440a1fa7_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/959169034358dac5eb74a9818a9c5bee\_MD5.png](assets/第4章%20目录IO和文件属性/959169034358dac5eb74a9818a9c5bee_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074\_MD5.png](assets/第4章%20目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/9cd60e051f6d5c1d74c51e884580549b\_MD5.png](assets/第4章%20目录IO和文件属性/9cd60e051f6d5c1d74c51e884580549b_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/c17057497b13759b71e2414120bc8fa5\_MD5.png](assets/第4章%20目录IO和文件属性/c17057497b13759b71e2414120bc8fa5_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/b0cfae49fc1e0be646f5cf2dee228302\_MD5.png](assets/第4章%20目录IO和文件属性/b0cfae49fc1e0be646f5cf2dee228302_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/c85ae0de56d7605502bafe4192eb6403\_MD5.png](assets/第4章%20目录IO和文件属性/c85ae0de56d7605502bafe4192eb6403_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/d267dda93a38e1e7e7d774a0c8f6f8aa\_MD5.png](assets/第4章%20目录IO和文件属性/d267dda93a38e1e7e7d774a0c8f6f8aa_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/58a52bc16da55455f79f40f9ffa56776\_MD5.png](assets/第4章%20目录IO和文件属性/58a52bc16da55455f79f40f9ffa56776_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/48887453df5381f28486771bbad16ec4\_MD5.png](assets/第4章%20目录IO和文件属性/48887453df5381f28486771bbad16ec4_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/8c315b74deecf4742d862b88f6629cbe\_MD5.png](assets/第4章%20目录IO和文件属性/8c315b74deecf4742d862b88f6629cbe_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074\_MD5.png](assets/第4章%20目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/19c8624f1d535dcd666cd27fc6388b89\_MD5.png](assets/第4章%20目录IO和文件属性/19c8624f1d535dcd666cd27fc6388b89_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/5544c137a2b39adf25ac1ab6c7280fa5\_MD5.png](assets/第4章%20目录IO和文件属性/5544c137a2b39adf25ac1ab6c7280fa5_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/a0414ca6ab73c7958fe8050606bba175\_MD5.png](assets/第4章%20目录IO和文件属性/a0414ca6ab73c7958fe8050606bba175_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/060aeb88bfd08918a751d5cb6f015ec5\_MD5.png](assets/第4章%20目录IO和文件属性/060aeb88bfd08918a751d5cb6f015ec5_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/a6a231453866e9bea3723f66cc361009\_MD5.png](assets/第4章%20目录IO和文件属性/a6a231453866e9bea3723f66cc361009_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074\_MD5.png](assets/第4章%20目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/6390bc9eb9e0ae3463fd156ce66e1693\_MD5.png](assets/第4章%20目录IO和文件属性/6390bc9eb9e0ae3463fd156ce66e1693_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/ec6cea19e049ea949f16fad927fbb484\_MD5.png](assets/第4章%20目录IO和文件属性/ec6cea19e049ea949f16fad927fbb484_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/473ef32dd0364617418ce8d104b0c60c\_MD5.png](assets/第4章%20目录IO和文件属性/473ef32dd0364617418ce8d104b0c60c_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/ff693507b85c8c1fb4d174eed8015741\_MD5.png](assets/第4章%20目录IO和文件属性/ff693507b85c8c1fb4d174eed8015741_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074\_MD5.png](assets/第4章%20目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/c44ae3547943108fa5e4dfc9e5a535be\_MD5.png](assets/第4章%20目录IO和文件属性/c44ae3547943108fa5e4dfc9e5a535be_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/7189e79c7ed3bfe59015a02f2285d1d5\_MD5.png](assets/第4章%20目录IO和文件属性/7189e79c7ed3bfe59015a02f2285d1d5_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/10b10f1393ed242241a260098ef77fcf\_MD5.png](assets/第4章%20目录IO和文件属性/10b10f1393ed242241a260098ef77fcf_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/6c2f1675e5c55ef33997e85bca825ee7\_MD5.png](assets/第4章%20目录IO和文件属性/6c2f1675e5c55ef33997e85bca825ee7_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074\_MD5.png](assets/第4章%20目录IO和文件属性/dee1fd9e65d2657251a51d017b1fc074_MD5.png) ![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第4章 目录IO和文件属性/05173586784a7d2f22251c897d381583\_MD5.png](assets/第4章%20目录IO和文件属性/05173586784a7d2f22251c897d381583_MD5.png)