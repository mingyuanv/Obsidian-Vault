---
title: "【北京迅为】《iTOP-3588开发板系统编程手册》-第14章 GPIO应用编程"
source: "https://blog.csdn.net/BeiJingXunWei/article/details/138004020"
author:
  - "[[BeiJingXunWei]]"
published: 2024-04-20
created: 2025-09-11
description: "文章浏览阅读1.3k次，点赞16次，收藏29次。RK3588是一款低功耗、高性能的处理器，适用于基于arm的PC和Edge计算设备、个人移动互联网设备等数字多媒体应用，RK3588支持8K视频编解码，内置GPU可以完全兼容OpenGLES 1.1、2.0和3.2。RK3588引入了新一代完全基于硬件的最大4800万像素ISP，内置NPU，支持INT4/INT8/INT16/FP16混合运算能力，支持安卓12和、Debian11、Build root、Ubuntu20和22版本登系统。了解更多信息可点击【粉丝群】824412014。_迅为rk3588资料"
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

## 第14章 GPIO应用编程

由于本章节要使用GPIO的方式来控制LED，所以需要在设备树中注释掉LED节点的相关内容，为了方便起见，已经将修改好的内核设备树放到了“ iTOP-3588开发板\\03\_【iTOP-RK3588开发板】指南教程\\03\_系统编程配套程序 \\ 62 ”目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第14章 GPIO应用编程/dd174083e957c3fa27a54931f5f8a437\_MD5.png](assets/第14章%20GPIO应用编程/dd174083e957c3fa27a54931f5f8a437_MD5.png)

将提供的boot.img文件根据 0 7 \_【北京迅为】itop-35 8 8开发板快速烧写手册.pdf 手册中的“ 单独烧写 Linux 固件 ”小节进行单独烧写，烧写完成之后就可以进行本章节的学习了。

### 14.1应用层如何操控GPIO

与 LED 设备一样，GPIO 同样也是通过 sysfs 方式进行操控的，首先使用以下命令进入到/sys/class/gpio 目录下，如下所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第14章 GPIO应用编程/5ace80f69981c7f4484f22130d27ca1e\_MD5.png](assets/第14章%20GPIO应用编程/5ace80f69981c7f4484f22130d27ca1e_MD5.png)

可以看到在当前目录下有两个文件 export、unexport 以及 5个 gpiochipX（X 等于 0、32、64、96、128）命名的文件夹。接下来将分别对 gpiochipX、export和unexport进行讲解：

****gpiochipX**** ：当前 SoC 所包含的 GPIO 控制器，iTOP-RK3588一共包含了 5 个 GPIO控制器，分别为 RK\_GPIO0、RK\_GPIO1、RK\_GPIO2、RK\_GPIO3、RK\_GPIO4，在这里分别对应 gpiochip0、gpiochip32、gpiochip64、gpiochip96、gpiochip128 这 5 个文件夹，每一个 gpiochipX 文件夹用来管理一组GPIO。

以gpiochip0文件夹为例，对gpiochipX目录中的内容进行讲解，进入gpiochip0目录下，gpiochip0目录内容如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第14章 GPIO应用编程/bacc78e20bd2beb944550454f82188fc\_MD5.png](assets/第14章%20GPIO应用编程/bacc78e20bd2beb944550454f82188fc_MD5.png)

分别为base、device、label、ngpio、power、subsystem、uevent，需要了解的是 base、label、ngpio 这三个属性文件，这三个属性文件均是只读、不可写。

****base：**** 与 gpiochipX 中的 X 相同，表示该控制器所管理的这组 GPIO 引脚中最小的编号。每一个 GPIO 引脚都会有一个对应的编号， Linux 下通过这个编号来操控对应的 GPIO 引脚。

使用cat命令对base文件信息进行查看如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第14章 GPIO应用编程/7429d0c7e0fe27386f106092139a87cf\_MD5.png](assets/第14章%20GPIO应用编程/7429d0c7e0fe27386f106092139a87cf_MD5.png)

****label：**** 对应该组 GPIO 标签，使用cat命令对label文件进行查看，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第14章 GPIO应用编程/8abbe5d2a2f71c813b290002770d83d6\_MD5.png](assets/第14章%20GPIO应用编程/8abbe5d2a2f71c813b290002770d83d6_MD5.png) ****ngpio：**** 该控制器所管理的 GPIO 引脚的数量（所以引脚编号范围是：base ~ base+ngpio-1），使用cat命令对ngpio文件进行查看，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第14章 GPIO应用编程/f58e3ddc1f65f4dab44c6a818ffd7f86\_MD5.png](assets/第14章%20GPIO应用编程/f58e3ddc1f65f4dab44c6a818ffd7f86_MD5.png) iTOP-RK3588有 5 组 GPIO bank：GPIO0~GPIO4，每组又以 A0~A7, B0~B7, C0~C7, D0~D7 作为编号区分,常用以下公式计算引脚：

```cpp
GPIO pin脚计算公式：pin = bank * 32 + number     //bank为组号，number为小组编号

GPIO 小组编号计算公式：number = group * 8 + X  
cpp
```

iTOP-RK3588有 5 组 GPIO bank：GPIO0~GPIO4，每组又以 A0~A7, B0~B7, C0~C7, D0~D7 作为编号区分,常用以下公式计算引脚：

```cpp
GPIO pin脚计算公式：pin = bank * 32 + number     //bank为组号，number为小组编号

GPIO 小组编号计算公式：number = group * 8 + X  
cpp
```

下面演示gpio座子5号引脚GPIO2\_PC4 pin脚计算方法：

```cpp
bank = 2;       //GPIO0_B7=> 2, bank ∈ [0,4]

group = 2;      //GPIO0_B7 => 2, group ∈ {(A=0), (B=1), (C=2), (D=3)}

X = 4;         //GPIO4_D7 => 4, X ∈ [0,7]

number = group * 8 + X = 2 * 8 + 4 =20

pin = bank*32 + number= 2 * 32 + 20 = 84;
cpp
```

****export**** ****：**** 用于将指定编号的 GPIO 引脚导出。在使用 GPIO 引脚之前，需要将其导出，导出成功之后才能使用它。注意 export 文件是只写文件，不能读取，将一个指定的编号写入到 export 文件中即可将对应的 GPIO 引脚导出，以GPIO2\_PC4为例（pin计算值为84）使用export 文件进行导出(如果没有更换本章开始部分的内核设备树镜像，会导出不成功)，导出成功如下图所示：

> echo 84 > export

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第14章 GPIO应用编程/27156a031eabaf25d5eec71279677042\_MD5.png](assets/第14章%20GPIO应用编程/27156a031eabaf25d5eec71279677042_MD5.png)

会发现在/sys/class/gpio 目录下生成了一个名为 gpio84 的文件夹（gpioX，X 表示对应的编号），该文件夹就是导出来的 GPIO 引脚对应的文件夹，用于管理、控制该 GPIO 引脚。

****unexport**** ****：**** 将导出的 GPIO 引脚删除。当使用完 GPIO 引脚之后，需要将导出的引脚删除，同样该文件也是只写文件、不可读，使用unexport 文件进行删除GPIO2\_PC4，删除成功如下图所示：

> echo 84 > unexport

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第14章 GPIO应用编程/4420a974abc20a9b1abd7cf79b40f90e\_MD5.png](assets/第14章%20GPIO应用编程/4420a974abc20a9b1abd7cf79b40f90e_MD5.png)

可以看到之前生成的 gpio84 文件夹就会消失！

需要注意的是，并不是所有 GPIO 引脚都可以成功导出，如果对应的 GPIO 已经被导出或者在内核中被使用了，那便无法成功导出，导出失败如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第14章 GPIO应用编程/ec6966ed2add8811d551174c7646e195\_MD5.png](assets/第14章%20GPIO应用编程/ec6966ed2add8811d551174c7646e195_MD5.png)

再次使用以下命令导出GPIO2\_PC3引脚，导出成功之后进入gpio84文件夹如下图所示：

> echo 84 > export

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第14章 GPIO应用编程/8da6fc1f5d8d90c719893cc89e1da22c\_MD5.png](assets/第14章%20GPIO应用编程/8da6fc1f5d8d90c719893cc89e1da22c_MD5.png)

可以看到gpio84文件夹下分别有active\_low、device、direction、edge、power、subsystem、uevent、value八个文件，需要关心的文件是 active\_low、direction、edge 以及 value 这四个属性文件，接下来分别介绍这四个属性文件的作用：

****direction**** ****：**** 配置 GPIO 引脚为输入或输出模式。该文件可读、可写，读表示查看 GPIO 当前是输入还是输出模式，写表示将 GPIO 配置为输入或输出模式；读取或写入操作可取的值为"out"（输出模式）和"in"（输入模式）。

在“/sys/class/gpio/gpio84”目录下使用cat命令查看direction输入输出模式，如下图所示：

> cat direction

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第14章 GPIO应用编程/b3e002f9111b35c79495a29d2319dde5\_MD5.png](assets/第14章%20GPIO应用编程/b3e002f9111b35c79495a29d2319dde5_MD5.png)

默认状态下的输入输出状态为“in”,由于direction为可读可写，可以使用以下命令将模式配置为输出，配置完成如下图所示

> echo out > direction
> 
> cat direction

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第14章 GPIO应用编程/34c8eede7bbb01d2a437ccb77610372e\_MD5.png](assets/第14章%20GPIO应用编程/34c8eede7bbb01d2a437ccb77610372e_MD5.png)

****active\_low**** ****：**** 用于控制极性得属性文件，可读可写，默认情况下为 0，使用cat命令进行文件内容的查看，如下图所示 ：

> cat active\_low

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第14章 GPIO应用编程/b2a67a2c9eaa38dd6a8432c6edcede0a\_MD5.png](assets/第14章%20GPIO应用编程/b2a67a2c9eaa38dd6a8432c6edcede0a_MD5.png)

当 active\_low 等于 0 时， value 值若为1则引脚输出高电平，value 值若为0则引脚输出低电平。当 active\_low 等于 1 时 ，value 值若为0则引脚输出高电平，value 值若为1则引脚输出低电平。

****edge**** ****：**** 控制中断的触发模式，该文件可读可写。在配置 GPIO 引脚的中断触发模式之前，需将其设置为输入模式，四种触发模式的设置如下所示：

| 非中断引脚： **echo** "none" **\>** edge  上升沿触发： **echo** "rising" **\>** edge  下降沿触发： **echo** "falling" **\>** edge  边沿触发： **echo** "both" **\>** edge |
| --- |

至此，关于GPIO的控制相关的知识就讲解完成了，下面将分别进行GPIO的输入和输出实验。

### 14.2 GPIO输出应用编程

本小节代码在配套资料“ iTOP-3588开发板\\03\_【iTOP-RK3588开发板】指南教程\\03\_系统编程配套程序 \\ 62 ”目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第14章 GPIO应用编程/7c34f4f42a8bbde51d192cf2efed2b0c\_MD5.png](assets/第14章%20GPIO应用编程/7c34f4f42a8bbde51d192cf2efed2b0c_MD5.png)

****实验要求：****

通过GPIO输出应用程序控制GPIO口输出高低电平，以此来控制LED灯的亮灭。

#### 14.2.1编写应用程序

****实验步骤：****

首先进入 ubuntu 的终端界面输入以下命令来创建 demo62\_gpioout.c文件，如下图所示：

> vim demo62\_gpioout.c

然后向该文件中添加以下内容：

```cpp
#include <stdio.h>

#include <stdlib.h>

#include <sys/types.h>

#include <sys/stat.h>

#include <fcntl.h>

#include <unistd.h>

#include <string.h>

 

char gpio_path[100];  // 存放GPIO路径

 

int gpio_ctrl(char *arg, char *val)  // 控制GPIO输出高低电平

{

    char file_path[100];  // 存放文件路径

    int fd, len, ret;

 

    sprintf(file_path, "%s/%s", gpio_path, arg);  // 将文件路径拼接起来

    fd = open(file_path, O_WRONLY);  // 以只写方式打开文件

    if (fd < 0) 

    {

        printf("无法打开文件: %s\n", file_path);  // 打开文件失败

        return -1;

    }

 

    len = strlen(val);

    ret = write(fd, val, len);  // 向文件中写入val内容

    if (ret < 0) 

    {

        printf("无法写入文件: %s\n", file_path);  // 写入文件失败

        close(fd);  // 关闭文件描述符

        return -1;

    }

 

    close(fd);  // 关闭文件描述符

    return 0;

}

 

int main(int argc, char *argv[])  // 主函数

{

    sprintf(gpio_path, "/sys/class/gpio/gpio%s", argv[1]);  // 将GPIO路径存放到gpio_path中

 

    // 如果 GPIO 没有被导出，则导出 GPIO

    if (access(gpio_path, F_OK))  // 判断是否存在gpio_path指向的路径

    {

        int fd, len, ret;

 

        fd = open("/sys/class/gpio/export", O_WRONLY);  // 打开export文件

        if (fd < 0) 

        {

            printf("无法打开文件: /sys/class/gpio/export\n");  // 打开文件失败

            return -1;

        }

 

        len = strlen(argv[1]);

        ret = write(fd, argv[1], len);  // 向文件中写入argv[1]的内容

        if (ret < 0) 

        {

            printf("无法写入文件: /sys/class/gpio/export\n");  // 写入文件失败

            close(fd);  // 关闭文件描述符

            return -1;

        }

 

        close(fd);  // 关闭文件描述符

    }

 

    gpio_ctrl("direction", "out");  // 配置GPIO为输出模式

    gpio_ctrl("active_low", "0");  // 设置极性

    gpio_ctrl("value", argv[2]);   // 控制GPIO输出高低电平

 

    return 0;  // 返回0表示程序正常退出

}
cpp
```

第35行首先会判断相应的gpio文件是否存在，不存在则进行gpio的导出，存在就继续运行，第67-79行为了方便通过gpio\_ctrl函数进行属性的配置。

保存退出之后，使用以下命令设置交叉编译器环境，并对demo62\_gpioout.c进行交叉编译，编译完成如下图所示：

> export PATH=/usr/local/ [arm64](https://so.csdn.net/so/search?q=arm64&spm=1001.2101.3001.7020) /gcc-arm-10.3-2021.07-x86\_64-aarch64-none-linux-gnu/bin:$PATH
> 
> aarch64-none-linux-gnu-gcc -o demo62\_gpioout demo62\_gpioout.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第14章 GPIO应用编程/66f4a614f987824ccd1f7d839667771a\_MD5.png](assets/第14章%20GPIO应用编程/66f4a614f987824ccd1f7d839667771a_MD5.png)

最后将交叉编译生成的demo62\_gpioout文件拷贝到/home/nfs共享目录下即可。

#### 14.2.2开发板测试

Buildroot系统启动之后，首先使用以下命令进行nfs共享目录的挂载（ 其中 192.168.1.7 为作者ubuntu的ip地址，需要根据自身ubuntu的ip来设置 ），如下图所示：

mount -t nfs -o nfsvers=3,nolock 192.168.1.7:/home/nfs /mnt

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第14章 GPIO应用编程/b4aad5c3877a8e546773194a6634e06a\_MD5.png](assets/第14章%20GPIO应用编程/b4aad5c3877a8e546773194a6634e06a_MD5.png) nfs共享目录挂载到了开发板的/mnt目录下，进入到/mnt目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第14章 GPIO应用编程/c75c38585426581c197cec43cf5f0e18\_MD5.png](assets/第14章%20GPIO应用编程/c75c38585426581c197cec43cf5f0e18_MD5.png)

可以看到/mnt目录下demo62\_gpioout文件已经存在了，然后使用以下命令导出LED的GPIO2\_PC4 pin脚，并设置为高电平，如下图所示：

> ./demo62\_gpioout 84 1

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第14章 GPIO应用编程/e448e6991159c941f2a27b370b86fc2a\_MD5.png](assets/第14章%20GPIO应用编程/e448e6991159c941f2a27b370b86fc2a_MD5.png)

使用命令之后会发现LED灯会亮起，然后使用以下命令关闭led灯，如下图所示：

> ./demo62\_gpioout 84 0

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第14章 GPIO应用编程/6cbdf73d8b3ad6b44c4b55d1b5d07f76\_MD5.png](assets/第14章%20GPIO应用编程/6cbdf73d8b3ad6b44c4b55d1b5d07f76_MD5.png)

命令运行成功之后，可以看到LED灯又熄灭了。至此，GPIO输出应用程序在开发板的测试就完成了。

### 14.3 GPIO输入应用编程

本小节代码在配套资料“ iTOP-3588开发板\\03\_【iTOP-RK3588开发板】指南教程\\03\_系统编程配套程序 \\ 63 ”目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第14章 GPIO应用编程/d5db6b859a812b270ea902f61aec8a76\_MD5.png](assets/第14章%20GPIO应用编程/d5db6b859a812b270ea902f61aec8a76_MD5.png)

****实验要求：****

通过GPIO输入应用程序来打印GPIO口当前输入的电平。

#### 14.3.1编写应用程序

****实验步骤：****

首先进入到ubuntu的终端界面输入以下命令来创建 demo63\_gpioin.c文件，如下图所示：

> vim demo63\_gpioin.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第14章 GPIO应用编程/bbaa1e48bbb2a185caddf36892ba164c\_MD5.png](assets/第14章%20GPIO应用编程/bbaa1e48bbb2a185caddf36892ba164c_MD5.png) 然后向该文件中添加以下内容：

```cpp
#include <stdio.h>

#include <stdlib.h>

#include <sys/types.h>

#include <sys/stat.h>

#include <fcntl.h>

#include <unistd.h>

#include <string.h>

 

char gpio_path[100];  // GPIO文件路径

 

int gpio_ctrl(char *arg, char *val) 

{

    char file_path[100];    // 文件路径

    int fd, len, ret;       // 文件描述符，写入字节数，返回值

 

    sprintf(file_path, "%s/%s", gpio_path, arg);  // 将GPIO文件路径和文件名拼接成文件路径

    fd = open(file_path, O_WRONLY);              // 以只写方式打开文件

    if (fd < 0) 

    {

        printf("open error\n");     // 打开文件错误

        return -1;

    }

    len = strlen(val);          // 获取字符串的长度

    ret = write(fd, val, len);  // 向文件中写入数据

    if (ret < 0) 

    {

        printf("write error\n");    // 写入数据错误

        return -1;

    }

    close(fd);          // 关闭文件

    return 0;

}

 

int main(int argc, char *argv[]) 

{

    char file_path[100], buf[1];    // 文件路径，读取缓冲区

    int fd, len, ret;               // 文件描述符，写入字节数，返回值

 

    sprintf(gpio_path, "/sys/class/gpio/gpio%s", argv[1]);    // 将GPIO文件路径和GPIO号拼接成GPIO文件路径

    if (access(gpio_path, F_OK))    // 检查GPIO文件是否存在

    {

        fd = open("/sys/class/gpio/export", O_WRONLY);       // 打开export文件

        if (fd < 0) 

        {

            printf("open error\n");     // 打开文件错误

            return -1;

        }

        len = strlen(argv[1]);          // 获取字符串的长度

        ret = write(fd, argv[1], len);  // 向文件中写入GPIO号

        if (ret < 0) 

        {

            printf("write error\n");    // 写入数据错误

            return -1;

        }

        close(fd);          // 关闭文件

    }

 

    gpio_ctrl("direction", "in");     // 配置为输入模式 

    gpio_ctrl("active_low", "0");     // 极性设置

    gpio_ctrl("edge", "none");        // 设置非中断输入

    sprintf(file_path, "%s/%s", gpio_path, "value"); // 将GPIO文件路径和value文件名拼接成文件路径

    fd = open(file_path, O_RDONLY);                // 以只读方式打开文件

    if (fd < 0) 

    {

        printf("open error\n");     // 打开文件错误

        return -1;

    }

    ret = read(fd, buf, 1);         // 从文件中读取1个字节的数据

    if (ret < 0) 

    {

        printf("write error\n");    // 读取数据错误

        return -1;

    }

    if (!strcmp(buf, "1"))      // 判断读取的数据是否为1

    {

        printf("the value is high\n");  // 数据为1，输出高电平

    } 

    else if (!strcmp(buf, "0")) // 判断读取的数据是否为0

    {

        printf("the value is low\n"); // 数据为0，输出低电平

    }

    close(fd);

    return 0;

}
cpp
```

第41行首先会判断相应的gpio文件是否存在，不存在则进行gpio的导出，存在就继续运行，第59-61行为了方便通过gpio\_ctrl函数进行属性的配置。

保存退出之后，使用以下命令设置交叉编译器环境，并对demo63\_gpioin.c进行交叉编译，编译完成如下图所示：

> export PATH=/usr/local/arm64/gcc-arm-10.3-2021.07-x86\_64-aarch64-none-linux-gnu/bin:$PATH
> 
> aarch64-none-linux-gnu-gcc -o demo63\_gpioin demo63\_gpioin.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第14章 GPIO应用编程/85c0f8c35d0e842627d6cc0b8616a19d\_MD5.png](assets/第14章%20GPIO应用编程/85c0f8c35d0e842627d6cc0b8616a19d_MD5.png)

最后将交叉编译生成的demo63\_gpioin文件拷贝到/home/nfs共享目录下即可。

#### 14.3.2开发板测试

Buildroot系统启动之后，首先使用以下命令进行nfs共享目录的挂载（ 其中 192.168.1.7 为作者ubuntu的ip地址，需要根据自身ubuntu的ip来设置 ），如下图所示：

mount -t nfs -o nfsvers=3,nolock 192.168.1.7:/home/nfs /mnt

![](https://i-blog.csdnimg.cn/blog_migrate/3528d6b603d88e8a0c2442fe2155eb87.png)

nfs共享目录挂载到了开发板的/mnt目录下，进入到/mnt目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第14章 GPIO应用编程/5756fc44e5ad810942a5b52a329c6d59\_MD5.png](assets/第14章%20GPIO应用编程/5756fc44e5ad810942a5b52a329c6d59_MD5.png)

可以看到/mnt目录下demo63\_gpioin文件已经存在了，然后使用以下命令导出LED的GPIO2\_PC4 pin脚，如下图所示：

> ./demo63\_gpioin 84

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第14章 GPIO应用编程/5b311992b75f5688031a5b75ea2a1ac3\_MD5.png](assets/第14章%20GPIO应用编程/5b311992b75f5688031a5b75ea2a1ac3_MD5.png)

可以看到LED的GPIO2\_PC4 pin脚打印的high值为高，而此时LED灯为点亮状态，所以gpio的状态打印正确。

为了测试输入底电平的状况，作者使用了杜邦线将GND接到了GPIO2\_PC4 pin脚上，然后再次使用以下命令来进行状态的检测，如下图所示：

> ./demo63\_gpioin 84

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第14章 GPIO应用编程/23de92656a8f6538014109a4b2e281d2\_MD5.png](assets/第14章%20GPIO应用编程/23de92656a8f6538014109a4b2e281d2_MD5.png)

可以看到LED的GPIO2\_PC4 pin脚打印的low值为低，而此时LED灯为熄灭状态，所以gpio的状态打印正确。

至此GPIO输入应用程序在开发板的测试就完成了。

### 14.4 GPIO输入中断编程

本小节代码在配套资料“ iTOP-3588开发板\\03\_【iTOP-RK3588开发板】指南教程\\03\_系统编程配套程序 \\ 64 ”目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第14章 GPIO应用编程/a603b864ec344d21867570f9bf462c7c\_MD5.png](assets/第14章%20GPIO应用编程/a603b864ec344d21867570f9bf462c7c_MD5.png)

****实验要求：****

通过GPIO的输入中断程序，将中断触发方式设置为边沿触发，每当触发中断会打印“get interrupt”字符串。

#### 14.4.1编写应用程序

****实验步骤：****

首先进入到ubuntu的终端界面输入以下命令来创建 demo64\_interrupt.c文件，如下图所示：

> vim demo64\_interrupt.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第14章 GPIO应用编程/95bfc1885012e9a3d4f8da1159fcb1b3\_MD5.png](assets/第14章%20GPIO应用编程/95bfc1885012e9a3d4f8da1159fcb1b3_MD5.png) 然后向该文件中添加以下内容：

```cpp
#include <stdio.h>

#include <stdlib.h>

#include <sys/types.h>

#include <sys/stat.h>

#include <fcntl.h>

#include <unistd.h>

#include <string.h>

#include <poll.h>

 

char gpio_path[100];

 

// 控制GPIO的函数

int gpio_ctrl(char *arg, char *val) 

{

    char file_path[100];

    int fd, len, ret;

 

    // 根据参数和GPIO路径生成要控制的文件路径

    sprintf(file_path, "%s/%s", gpio_path, arg);

 

    // 打开文件

    fd = open(file_path, O_WRONLY);

    if (fd < 0) 

    {

        printf("open error\n");

        return -1;

    }

 

    // 计算要写入的值的长度，并将值写入文件

    len = strlen(val);

    ret = write(fd, val, len);

    if (ret < 0) 

    {

        printf("write error\n");

        return -1;

    }

 

    // 关闭文件并返回成功

    close(fd);

    return 0;

}

 

int main(int argc, char *argv[]) 

{

    char file_path[100], buff[10];

    int fd, len, ret;

    struct pollfd fds[1];

 

    // 根据命令行参数生成GPIO路径

    sprintf(gpio_path, "/sys/class/gpio/gpio%s", argv[1]);

 

    // 如果该GPIO未导出，则导出该GPIO

    if (access(gpio_path, F_OK)) 

    {

        fd = open("/sys/class/gpio/export", O_WRONLY);

        if (fd < 0) 

        {

            printf("open error\n");

            return -1;

        }

        len = strlen(argv[1]);

        ret = write(fd, argv[1], len);

        if (ret < 0) 

        {

            printf("write error\n");

            return -1;

        }

        close(fd);

    }

 

    // 配置GPIO为输入模式、极性为正、边沿触发中断

    gpio_ctrl("direction", "in");

    gpio_ctrl("active_low", "0");

    gpio_ctrl("edge", "both");

 

    // 打开GPIO的值文件并将其文件描述符赋给pollfd结构体

    sprintf(file_path, "%s/%s", gpio_path, "value");

    fd = open(file_path, O_RDONLY);

    if (fd < 0) 

    {

        printf("open error\n");

        return -1;

    }

    fds[0].fd = fd;

    fds[0].events = POLLPRI; // 只关心高优先级数据可读（中断）

    read(fd, buff, 10); // 先读取一次清除状态

 

    // 进入循环，等待GPIO中断

    while (1) 

    {

        ret = poll(fds, 1, -1); // 等待事件发生

        if (ret == -1) 

        {

            printf("poll fail\n");

        }

        if (fds[0].revents & POLLPRI) 

        { // 如果高优先级数据可读（中断触发）

            printf("get interrupt\n");

        }

    }

 

    // 关闭文件并返回成功

    close(fd);

    return 0;

}
cpp
```

第53行首先会判断相应的gpio文件是否存在，不存在则进行gpio的导出，存在就继续运行，第72-74行为了方便通过gpio\_ctrl函数进行属性的配置，将中断模式设置为边沿触发，之后使用poll函数进行中断的判断，并打印相应的信息。

保存退出之后，使用以下命令设置交叉编译器环境，并对demo99\_gpioin.c进行交叉编译，编译完成如下图所示：

> export PATH=/usr/local/arm64/gcc-arm-10.3-2021.07-x86\_64-aarch64-none-linux-gnu/bin:$PATH
> 
> aarch64-none-linux-gnu-gcc -o demo64\_interrupt demo64\_interrupt.c

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第14章 GPIO应用编程/7feb7699ac0d8f4806f211de86ec03ed\_MD5.png](assets/第14章%20GPIO应用编程/7feb7699ac0d8f4806f211de86ec03ed_MD5.png)

最后将交叉编译生成的demo64\_interrupt文件拷贝到/home/nfs共享目录下即可。

#### 14.4.2开发板测试

Buildroot系统启动之后，首先使用以下命令进行nfs共享目录的挂载（ 其中 192.168.1.7 为作者ubuntu的ip地址，需要根据自身ubuntu的ip来设置 ），如下图所示：

mount -t nfs -o nfsvers=3,nolock 192.168.1.7:/home/nfs /mnt

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第14章 GPIO应用编程/b4aad5c3877a8e546773194a6634e06a\_MD5.png](assets/第14章%20GPIO应用编程/b4aad5c3877a8e546773194a6634e06a_MD5.png) nfs共享目录挂载到了开发板的/mnt目录下，进入到/mnt目录下，如下图所示：

可以看到/mnt目录demo64\_interrupt文件已经存在了，然后使用以下命令导出LED的GPIO2\_PC4 pin脚，并设置中断触发模式，如下图所示：

> ./demo100\_interrupt 84

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第14章 GPIO应用编程/8a9cdf75059309990b93877222e561b1\_MD5.png](assets/第14章%20GPIO应用编程/8a9cdf75059309990b93877222e561b1_MD5.png)

由于中断并没有被触发，所以程序会阻塞，等待中断的进行，然后使用杜邦线将GND接到GPIO2\_PC4 pin脚，进行中断的测试，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第14章 GPIO应用编程/d35b1fa13dab0ae2931de5855523d210\_MD5.png](assets/第14章%20GPIO应用编程/d35b1fa13dab0ae2931de5855523d210_MD5.png)

可以看到中断就被触发了，相应的字符串也被打印了。至此GPIO输入中断应用程序在开发板的测试就完成了。

微信公众号

内容来源：csdn.net

作者昵称：北京迅为

原文链接：https://blog.csdn.net/BeiJingXunWei/article/details/138004020

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

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第14章 GPIO应用编程/90bd0cbf3aff8fdff8bf9b011b581e20\_MD5.png](assets/第14章%20GPIO应用编程/90bd0cbf3aff8fdff8bf9b011b581e20_MD5.png)

程序员都在用的中文IT技术交流社区

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第14章 GPIO应用编程/08a47e60886378fe60a3d9c8f4ae8bc6\_MD5.png](assets/第14章%20GPIO应用编程/08a47e60886378fe60a3d9c8f4ae8bc6_MD5.png)

专业的中文 IT 技术社区，与千万技术人共成长

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第14章 GPIO应用编程/a51be6c085b867a5bd82d8dc1cea9b46\_MD5.png](assets/第14章%20GPIO应用编程/a51be6c085b867a5bd82d8dc1cea9b46_MD5.png)

关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！

客服 返回顶部

微信公众号

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第14章 GPIO应用编程/efb7921311640694e61fee00900550d6\_MD5.jpg](assets/第14章%20GPIO应用编程/efb7921311640694e61fee00900550d6_MD5.jpg) 公众号名称：迅为电子 微信扫码关注或搜索公众号名称

复制公众号名称