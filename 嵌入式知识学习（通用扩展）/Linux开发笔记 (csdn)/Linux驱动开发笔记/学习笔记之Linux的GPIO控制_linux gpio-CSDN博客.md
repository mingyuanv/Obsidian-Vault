---
title: "学习笔记之Linux的GPIO控制_linux gpio-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/137020363?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读3.3k次，点赞32次，收藏32次。本文介绍了如何在rk3566主控芯片上通过GPIOsysfs接口和libgpiod库在Linux系统中控制GPIO，包括GPIO命名规则、导出与方向设置、输出控制以及使用libgpiod的高级功能和命令行操作示例。"
tags:
  - "clippings"
---
本文介绍了如何在rk3566主控芯片上通过GPIOsysfs接口和libgpiod库在Linux系统中控制GPIO，包括GPIO命名规则、导出与方向设置、输出控制以及使用libgpiod的高级功能和命令行操作示例。

摘要生成于 [C知道](https://ai.csdn.net/?utm_source=cknow_pc_ai_abstract) ，由 DeepSeek-R1 满血版支持， [前往体验 >](https://ai.csdn.net/?utm_source=cknow_pc_ai_abstract)

**目录**

[1\. GPIO命名规则](https://blog.csdn.net/sincerelover/article/details/?spm=1001.2014.3001.5502#1.%20GPIO%E5%91%BD%E5%90%8D%E8%A7%84%E5%88%99)

[2\. GPIO的控制方式](https://blog.csdn.net/sincerelover/article/details/?spm=1001.2014.3001.5502#t0)

[2.1 使用GPIO sysfs接口控制IO](https://blog.csdn.net/sincerelover/article/details/?spm=1001.2014.3001.5502#t1)

[2.2 使用libgpiod控制IO](https://blog.csdn.net/sincerelover/article/details/?spm=1001.2014.3001.5502#t2)

---

笔者在学习到点灯实验时，想到直接进行小灯的参数修改比较简单，于是想通过直接对GPIO进行操作从而达到相同的效果(这里可能需要修改 [设备树](https://so.csdn.net/so/search?q=%E8%AE%BE%E5%A4%87%E6%A0%91&spm=1001.2101.3001.7020) ，这块笔者也不是很懂不敢乱说，于是借用另一个32开发板的小灯进行测试)。泰山派所采用的主控芯片是rk3566，包含40pinGPIO口，具体接口信息如下图所示：

![](https://i-blog.csdnimg.cn/blog_migrate/602eb0f857bfcc33c9a7283b9ae4e830.png)

## 1\. GPIO命名规则

在rk3566中，GPIO口的引脚按照“控制器+端口+索引序号”的形式进行命名，例如GPIO1\_A4表示第一组控制器中A端口的4号引脚。在 硬件设计 中共有5个固定端口A，B，C和D（对应0，1，2，3），各端口有8个索引序号（0~7）。

## 2\. GPIO的控制方式

### 2.1 使用GPIO sysfs接口控制IO

在 Linux 中，最常见的读写GPIO方式就是用GPIO sysfs interface， 是通过操作 */sys/class/gpio*  目录下的  *export*  、  *unexport*  、 *gpio{N}/direction*, *gpio{N} /value* （用实际引脚号替代{N}）等文件实现的，经常出现shell脚本里面。这种方法不需要任何特殊的内核模块或驱动，只需通过用户空间的程序就可以访问和控制GPIO。

以下是一个基本的步骤指南，用于通过sysfs接口控制GPIO：

**1.导出GPIO**

首先，需要将GPIO从内核导出到用户空间。这可以通过向 `/sys/class/gpio/export` 文件写入GPIO编号来实现。例如，我们需要控制GPIO3\_B4 (32\*3+1\*8+4 = 108，详细规则可以看： [2\. GPIO控制 — 快速使用手册—基于LubanCat-RK356x系列板卡 文档](https://doc.embedfire.com/linux/rk356x/quick_start/zh/latest/quick_start/40pin/gpio/gpio.html#id1 "2. GPIO控制 — 快速使用手册—基于LubanCat-RK356x系列板卡  文档") ）的GPIO，可以这样做：

```cobol
echo 108 > /sys/class/gpio/export
```

**2.设置GPIO方向**

接下来，需要设置GPIO的方向（输入或输出）。这可以通过修改 `/sys/class/gpio/gpioX/direction` 文件来实现，其中 `X` 是你之前导出的GPIO的编号。

- 对于输入GPIO：
```cobol
echo in > /sys/class/gpio/gpio108/direction
```

这里也可以先查看一下此时的IO口状态：

```cobol
cat /sys/class/gpio/gpio108/value
```

可以看到此时是低电平，且小灯是亮着的

![](https://i-blog.csdnimg.cn/blog_migrate/88b90b3414b039ad64013e3db0322224.png)

![](https://i-blog.csdnimg.cn/blog_migrate/52448bb0e6e14799f99e50e9edd4c16e.jpeg)

- 对于输出GPIO：
```cobol
echo out > /sys/class/gpio/gpio108/direction
```

**3.控制输出GPIO**

如果你设置了GPIO为输出，你可以通过修改 `/sys/class/gpio/gpioX/value` 文件来控制其电平。写入 `1` 将设置GPIO为高电平，写入 `0` 将设置GPIO为低电平。 这里写入高电平，可以看到此时的小灯已经熄灭，证明我们实验成功了。

```cobol
echo 1 > /sys/class/gpio/gpio108/value
```

![](https://i-blog.csdnimg.cn/blog_migrate/52321bc126532693eb725058a7e705a1.jpeg)

**4.复位GPIO**

当你不再需要控制某个GPIO时，可以将其从用户空间取消导出。这可以通过向 `/sys/class/gpio/unexport` 文件写入GPIO编号来实现。

```cobol
echo 108 > /sys/class/gpio/unexpor
```

**5.程序编写**

首先介绍两个常用的 函数 ：access和open。

**`access` 函数：**

```bash
//用于检查进程是否有权限读取、写入或执行某个文件

#include <unistd.h>  

  

int access(const char *pathname, int mode);
```

其中：

- **`pathname`** 是你想要检查的文件的路径。
- **`mode`**  是一个标志，用于指定你想要检查的访问权限。它可以是以下值之一或它们的组合：
	- **`R_OK`** ：测试读权限
	- **`W_OK`** ：测试写权限
	- **`X_OK`** ：测试执行权限
	- **`F_OK`** ：测试文件是否存在

如果调用成功， **`access`**  返回0；如果失败，则返回-1，并设置 **`errno`** 以指示错误。

**open函数：**

open函数有两个或三个参数，具体形式如下：

```bash
//用于打开或创建文件

#include<sys/types.h>

#include<sys/stat.h>

#include<fcntl.h>

 

int open(const char *pathname, int flags);

int open(const char *pathname, int flags, mode_t mode);
```

其中， **`pathname`** 参数表示要打开或创建的文件名（含路径，缺省为当前路径）。 `flags` 参数用于指定打开文件的方式和权限，常用的标志位有：

- **`O_RDONLY`** ：只读方式打开文件。
- **`O_WRONLY`** ：只写方式打开文件。
- **`O_RDWR`** ：读写方式打开文件。
- **`O_CREAT`** ：如果文件不存在，则创建文件。
- **`O_EXCL`** ：与 **`O_CREAT`** 一起使用，如果文件已存在，则返回错误。
- **`O_TRUNC`** ：如果文件已存在，将其截断为0字节。
- **`O_APPEND`** ：在文件末尾追加写入。

当使用两个参数的open函数时，仅通过flags参数指定打开文件的方式和权限。而使用三个参数的open函数时，还需要通过mode参数指定新文件的存取许可权限。

open函数的返回值是一个文件描述符（file descriptor），它是一个非负整数，用于在后续的文件操作中标识该文件。如果操作成功，open函数将返回一个有效的文件描述符；如果操作失败，将返回-1。

在认识以上两个函数之后，我们就可以正式来写IO口的驱动函数了，这个过程执行的原理非常简单，这里以野火的程序为例 ：

- 把GPIO的编号写入到export文件，导出GPIO设备。
- 修改GPIO设备属性direction文件值为out，把GPIO设置为输出方向。
- 修改GPIO设备属性文件value的值为1或0，控制GPIO高电平或低电平。
```bash
#include <string.h>

#include <sys/stat.h>

#include <unistd.h>

#include <fcntl.h>

#include <stdio.h>

 

#define GPIO_INDEX "42"

static char gpio_path[75];

int gpio_init(char *name)

{

    int fd;

 

    sprintf(gpio_path, "/sys/class/gpio/gpio%s", name);

    //查询文件是否存在

    if (access("gpio_path", F_OK)){

        //只读方式打开

        fd = open("/sys/class/gpio/export", O_WRONLY);

        //打开文件失败

        if(fd < 0)

            return 1 ;

    

        write(fd, name, strlen(name));

        close(fd);

    

        //初始化gpio使用的引脚为输出模式

        sprintf(gpio_path, "/sys/class/gpio/gpio%s/direction", name);

        fd = open(gpio_path, O_WRONLY);

        if(fd < 0)

            return 2;

    

        write(fd, "out", strlen("out"));

        close(fd);

    }

 

    return 0;

}

//向unexport文件写入编号，取消导出

int gpio_deinit(char *name)

{

    int fd;

    fd = open("/sys/class/gpio/unexport", O_WRONLY);

    if(fd < 0)

        return 1;

 

    write(fd, name, strlen(name));

    close(fd);

 

    return 0;

}

 

//输出高电平

int gpio_high(char *name)

{

    int fd;

    sprintf(gpio_path, "/sys/class/gpio/gpio%s/value", name);

    fd = open(gpio_path, O_WRONLY);

    if(fd < 0){

        printf("open gpio%s wrong\n",name);

        return -1;

    }

        

    if(2 != write(fd, "1", sizeof("1")))

        printf("wrong set \n");

    close(fd);

    return 0;

}

 

//输出低电平

int gpio_low(char *name)

{

    int fd;

    sprintf(gpio_path, "/sys/class/gpio/gpio%s/value", name);

    fd = open(gpio_path, O_WRONLY);

    if(fd < 0){

        printf("open gpio%s wrong\n",name);

        return -1;

    }

        

    if(2 != write(fd, "0", sizeof("0")))

        printf("wrong set \n");

    close(fd);

    return 0;

}

 

int main(int argc, char *argv[])

{

    char buf[10];

    int res;

 

    /* 校验传参 */

    if (2 != argc) {

        printf( "usage: %s <PinNum>\n",argv[0]);

        return -1;

    }

    res = gpio_init(argv[1]);

    if(res){

        printf("gpio init error,code = %d",res);

        return 0;

    }

 

    while(1){

        printf("Please input the value : 0--low 1--high q--exit\n");

        scanf("%10s", buf);

 

        switch (buf[0]){

            case '0':

                gpio_low(argv[1]);

                break;

 

            case '1':

                gpio_high(argv[1]);

                break;

 

            case 'q':

                gpio_deinit(argv[1]);

                printf("Exit\n");

                return 0;

 

            default:

                break;

       }

    }

    return 0;

}
```

### 2.2 使用libgpiod控制IO

4.8版本的 Kernel 加入了libgpiod的支持，这里笔者的kernel版本不支持就不继续编译了，可以简单了解一下，详细可以访问野火的： [2\. GPIO控制 — 快速使用手册—基于LubanCat-RK356x系列板卡 文档](https://doc.embedfire.com/linux/rk356x/quick_start/zh/latest/quick_start/40pin/gpio/gpio.html#libgpiodio "2. GPIO控制 — 快速使用手册—基于LubanCat-RK356x系列板卡  文档")

先输入进行插件安装：

```
sudo apt install gpiod
```

下面是一些简单的常用命令：

| 命令 | 作用 | 使用举例 | 说明 |
| --- | --- | --- | --- |
| gpiodetect | 列出所有的 [GPIO控制](https://so.csdn.net/so/search?q=GPIO%E6%8E%A7%E5%88%B6&spm=1001.2101.3001.7020) 器 | gpiodetect(无参数) | 列出所有的GPIO控制器 |
| gpioinfo | 列出gpio控制器的引脚情况 | gpioinfo 1 | 列出第一组控制器引脚组情况 |
| gpioset | 设置gpio | gpioset 1 20=0 | 设置第一组控制器编号4引脚为低电平 |
| gpioget | 获取gpio引脚状态 | gpioget 1 20 | 获取第一组控制器编号4的引脚状态 |
| gpiomon | 监控gpio的状态 | gpiomon 1 20 | 监控第一组控制器编号4的引脚状态 |

**免责声明：本文所引用的各种资料均用于自己学习使用，这里感谢立创和正点原子官方的资料以及各位优秀的创作者。**

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/137020363

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

 [![](https://csdnimg.cn/release/blogv2/dist/pc/img/toolbar/Group-dark.png) 点击体验  
DeepSeekR1满血版](https://ai.csdn.net/?utm_source=cknow_pc_blogdetail&spm=1001.2101.3001.10583) 隐藏侧栏

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

![](https://i-blog.csdnimg.cn/blog_migrate/602eb0f857bfcc33c9a7283b9ae4e830.png)