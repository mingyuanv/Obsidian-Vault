---
title: "【北京迅为】《iTOP-3588开发板系统编程手册》-第17章 PWM应用编程"
source: "https://blog.csdn.net/BeiJingXunWei/article/details/138081310"
author:
  - "[[BeiJingXunWei]]"
published: 2024-04-22
created: 2025-09-11
description: "文章浏览阅读1.2k次，点赞17次，收藏12次。PWM，即脉冲宽度调制（Pulse Width Modulation），是一种通过改变信号的脉冲宽度来控制电路的输出信号的方法。在PWM中，周期不变，但是脉冲宽度随时间改变，从而控制电路的输出。PWM技术最初被广泛应用于模拟电路，用于调节电路的电压、电流、功率等。随着数字技术的发展，PWM技术被广泛应用于数字电路、控制系统和嵌入式系统等领域。在PWM信号中，每个周期包含一个高电平和一个低电平，它们之间的时间称为脉冲周期，通常用T表示。_itop rk3588 pwm"
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

## 第17章 PWM应用编程

由于本章节要进行PWM章节的实验，所以使用gpio座子其中的1号引脚来做PWM的实验管脚，所以需要在设备树中注释掉此引脚的相关内容，并使能PWM13。

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第17章 PWM应用编程/ce21d24070173754907130a2438c68f7\_MD5.png](assets/第17章%20PWM应用编程/ce21d24070173754907130a2438c68f7_MD5.png)

为了方便起见，已经将修改好的内核设备树放到了“ iTOP-3588开发板\\03\_【iTOP-RK3588开发板】指南教程\\03\_系统编程配套程序 \\ 67 ”目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第17章 PWM应用编程/4dd4b2e6932797b6823f88aa6b33d8af\_MD5.png](assets/第17章%20PWM应用编程/4dd4b2e6932797b6823f88aa6b33d8af_MD5.png)

将提供的boot.img文件根据 0 7 \_【北京迅为】itop-35 8 8开发板快速烧写手册.pdf 手册中的“ 单独烧写 Linux 固件 ”小节进行单独烧写，烧写完成之后就可以进行本章节的学习了。

### 17.1 PWM介绍

PWM，即脉冲宽度调制（Pulse Width Modulation），是一种通过改变信号的脉冲宽度来控制电路的输出信号的方法。在PWM中，周期不变，但是脉冲宽度随时间改变，从而控制电路的输出。

PWM技术最初被广泛应用于模拟电路，用于调节电路的电压、电流、功率等。随着数字技术的发展，PWM技术被广泛应用于数字电路、控制系统和 嵌入式系统 等领域。

在PWM信号中，每个周期包含一个高电平和一个低电平，它们之间的时间称为脉冲周期，通常用T表示。脉冲的宽度称为占空比，表示高电平持续的时间与一个周期的时间的比例，通常用D表示，D的取值范围是0到1之间。

PWM信号的输出可以通过多种方式实现，包括硬件PWM和软件PWM。硬件PWM通常是通过专用的PWM模块实现的，它可以在一个固定的频率下生成PWM信号，并且可以配置占空比和其他参数。软件PWM通常是在控制器的程序中实现的，它通过周期性地改变输出引脚的状态来实现PWM信号。

PWM技术可以用于许多应用，例如调节电机的转速、控制LED亮度、控制电磁阀的开关等。在这些应用中，PWM信号可以提供精确的控制和调节，从而实现更高的效率和更精确的控制。在本章将会使用PWM对LED灯的亮度进行控制。

### 17.2应用层操控PWM

PWM和之前讲解的LED、GPIO相同，都是通过 sysfs 方式进行操控的。开发板系统启动之后进入到/sys/class/pwm 目录下，如下所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第17章 PWM应用编程/38cc87764505a133ef014d469f2d6856\_MD5.png](assets/第17章%20PWM应用编程/38cc87764505a133ef014d469f2d6856_MD5.png)

在pwm目录下存在 4个以 pwmchipX（X 表示数字）命名的文件夹。在本章节的开始部分，重新烧写了设备树内核镜像，该设备树中总共使能了四个PWM，分别为PWM1,PWM3,PWM13和PWM15,系统会根据PWM的编号大小进行排序，在这里PWM1对应 pwmchip0、PWM3对应pwmchip1，PWM13对应pwmchip2，PWM15对应pwmchip3。

通过查询网盘“ TOP-35 8 8开发板\\01\_【iTOP-RK35 8 8开发板】基础资料\\01\_iTOP-RK35 8 8硬件资料\\03\_芯片数据手册\\01\_rk35 8 8数据手册和参考手册 ”路径下的Rockchip RK3588 Datasheet V1.1-20220124.pdf数据手册得知，RK3588总共有16个 PWM 控制器（具体的查询会在之后的驱动手册中进行讲解，本章节只是学习PWM的使用），本章节将会以GPIO3\_B6对应的PWM13为例进行讲解和演示。使用以下命令进入 PWM13对应的 pwmchip2目录下如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第17章 PWM应用编程/0f921932dc3d78717f9cec3c45842a24\_MD5.png](assets/第17章%20PWM应用编程/0f921932dc3d78717f9cec3c45842a24_MD5.png)

在这个目录下总共有七个文件分别为device、export、npwm、power、subsystem、uevent 和unexport。需要关注的是 export、npwm 以及 unexport 这三个属性文件，下面一一进行介绍：

****npwm：**** 是一个只读属性，读取该文件可以得知该 PWM 控制器下共有几路 PWM 输出，如下所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第17章 PWM应用编程/1b40317eb3a991579d927d7dcc80b3c7\_MD5.png](assets/第17章%20PWM应用编程/1b40317eb3a991579d927d7dcc80b3c7_MD5.png)

****export：**** 在使用 PWM 之前，通过 export 属性进行导出，以下所示：

echo 0 > export

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第17章 PWM应用编程/d588824b0177b298c7e5b2fb07dce419\_MD5.png](assets/第17章%20PWM应用编程/d588824b0177b298c7e5b2fb07dce419_MD5.png)

****unexport**** ：当使用完 PWM 之后，需要将导出的 PWM 删除，譬如：

echo 0 > unexport

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第17章 PWM应用编程/e42986f1870f979947436d0849e928ac\_MD5.png](assets/第17章%20PWM应用编程/e42986f1870f979947436d0849e928ac_MD5.png)

写入到 unexport 文件中的编号与写入到 export 文件中的编号是相对应的；需要注意的是，export 文件 和 unexport 文件都是只写的、没有读权限。

再次使用以下命令导出pwm0目录，导出成功之后进入该文件夹如下图所示：

> echo 0 > export
> 
> cd pwm0

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第17章 PWM应用编程/a0cd74228d4baa39e57acc5ad248a606\_MD5.png](assets/第17章%20PWM应用编程/a0cd74228d4baa39e57acc5ad248a606_MD5.png)

可以看到pwm0文件夹下分别有capture、duty\_cycle、enable、output\_type、period、polarity、power、uevent七个文件，而需要了解的文件是 duty\_cycle、enable、period 以及 polarity 这四个属性文件，接下来分别介绍这四个属性文件的作用：

****polarity：**** 用于PWM极性的查看，只读属性，这里为inversed表示极性反转，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第17章 PWM应用编程/7f62c6832f0e9acafb73e4d368d2b2cc\_MD5.png](assets/第17章%20PWM应用编程/7f62c6832f0e9acafb73e4d368d2b2cc_MD5.png)

****period：**** 用于配置 PWM 周期，可读可写；写入一个字符串数字值，以 ns（纳秒）为单位，譬如配置 PWM 周期为 10us（微秒）：

> echo 10000 > period

****duty\_cycle：**** 用于配置 PWM 的占空比，可读可写；写入一个字符串数字值，同样也是以 ns 为单位，譬如：

> echo 5000 > duty\_cycle

****enable：**** 使能 PWM 输出通常配置好 PWM 之后，再使能 PWM。可读可写，写入"0"表示禁止 PWM；写入"1"表示使能 PWM。

允许PWM输出：

> echo 1 > enable

禁止 PWM 输出：

> echo 0 > enable

### 17.3 PWM应用编程

本小节代码在配套资料“ iTOP-3588开发板\\03\_【iTOP-RK3588开发板】指南教程\\03\_系统编程配套程序 \\ 67 ”目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第17章 PWM应用编程/7c3e337aa6e9635523614071a7005b59\_MD5.png](assets/第17章%20PWM应用编程/7c3e337aa6e9635523614071a7005b59_MD5.png)

****实验要求：****

通过PWM输入应用程序来控制引脚GPIO3\_B6的占空比，以此来实现呼吸灯的效果。

#### 17.3.1编写应用程序

****实验步骤：****

首先进入到 ubuntu 的终端界面输入以下命令来创建 demo67\_pwm.c文件，如下图所示：

> vim demo67\_pwm.c

然后向该文件中添加以下内容：

```cpp
#include <stdio.h>

#include <sys/types.h>

#include <sys/stat.h>

#include <fcntl.h>

#include <unistd.h>

#include <string.h>

 

char pwm_path[100];

#define PWM13_PATH "/sys/class/pwm/pwmchip2/pwm0"

 

// PWM控制函数，arg为控制参数，val为参数值

int pwm_ctrl(char *arg, char *val)

{

    char file_path[100];

    int fd, len, ret;

    // 拼接文件路径

    sprintf(file_path, "%s/%s", PWM13_PATH, arg);

    // 打开文件

    fd = open(file_path, O_WRONLY);

    if (fd < 0)

    {

        // 打开文件失败

        printf("打开文件%s失败\n", file_path);

        return -1;

    }

    // 写入参数值

    len = strlen(val);

    ret = write(fd, val, len);

    if (ret < 0)

    {

        // 写入文件失败

        printf("写入文件%s失败\n", file_path);

        return -1;

    }

    // 关闭文件

    close(fd);

    return 0;

}

 

int main(int argc, int *argv[])

{

    int fd, len, ret;

    char buf[100];

    // 检测PWM0_PATH路径是否存在，不存在则创建

    if (access(PWM13_PATH, F_OK))

    {

        fd = open("/sys/class/pwm/pwmchip2/export", O_WRONLY);

        if (fd < 0)

        {

            // 打开文件失败

            printf("打开文件%s失败\n", "/sys/class/pwm/pwmchip2/export");

            return -1;

        }

        // 写入0到export文件，创建PWM设备

        len = 1;

        ret = write(fd, "0", len);

        if (ret < 0)

        {

            // 写入文件失败

            printf("写入文件%s失败\n", "/sys/class/pwm/pwmchip2/export");

            return -1;

        }

        // 关闭文件

        close(fd);

    }

 

    // 配置PWM周期、占空比并使能PWM输出

    pwm_ctrl("period", "10000"); // 设置周期为10000纳秒

    pwm_ctrl("duty_cycle", "10000"); // 设置占空比为10000纳秒，即100%

    pwm_ctrl("enable", "1"); // 使能PWM输出

 

    // 循环改变PWM占空比，实现LED呼吸灯效果

    while (1)

    {

        for (int i = 10000; i >= 0; i--) // 减小PWM占空比，LED变暗

        {

            sprintf(buf, "%d", i);

            pwm_ctrl("duty_cycle", buf);

            usleep(5); // 延时5微秒

        }

        for (int i = 0; i <= 10000; i++) // 增加PWM占空比，LED变亮

        {

            sprintf(buf, "%d", i);

            pwm_ctrl("duty_cycle", buf);

            usleep(5); // 延时5微秒

        }

    }

 

    return 0;

}
cpp
```

第45-65行首先会判断相应的pwm文件是否存在，不存在则进行gpio的导出，存在就继续运行，第68-70行分别确定了PWM的周期、PWM占空比，并对PWM进行使能。75-80和81-87为两个for循环，第一个for循环为占空比降低，LED灯的亮度由亮变暗，第二个for循环为占空比降增加，LED灯的亮度由暗变亮。

保存退出之后，使用以下命令设置交叉编译器环境，并对demo67\_pwm.c进行交叉编译，编译完成如下图所示：

> export PATH=/usr/local/ [arm64](https://so.csdn.net/so/search?q=arm64&spm=1001.2101.3001.7020) /gcc-arm-10.3-2021.07-x86\_64-aarch64-none- linux -gnu/bin:$PATH
> 
> aarch64-none-linux-gnu-gcc -o demo67\_pwm demo67\_pwm.c

最后将交叉编译生成的demo67\_pwm文件拷贝到/home/nfs共享目录下即可。

#### 17.3.2开发板测试

Buildroot系统启动之后，首先使用以下命令进行nfs共享目录的挂载（ 其中 192.168.1.7 为作者ubuntu的ip地址，需要根据自身ubuntu的ip来设置 ），如下图所示：

> mount -t nfs -o nfsvers=3,nolock 192.168.1.7:/home/nfs /mnt

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第17章 PWM应用编程/b4aad5c3877a8e546773194a6634e06a\_MD5.png](assets/第17章%20PWM应用编程/b4aad5c3877a8e546773194a6634e06a_MD5.png)

nfs共享目录挂载到了开发板的/mnt目录下，进入到/mnt目录下，如下图所示：

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第17章 PWM应用编程/bf0c0f192329cda7c527f690b0ff3544\_MD5.png](assets/第17章%20PWM应用编程/bf0c0f192329cda7c527f690b0ff3544_MD5.png)

可以看到/mnt目录下demo67\_pwm文件已经存在了，然后使用以下命令运行该程序如下图所示：

> ./demo67\_pwm

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第17章 PWM应用编程/bdffb6fa415d2227f8be10bed6291f43\_MD5.png](assets/第17章%20PWM应用编程/bdffb6fa415d2227f8be10bed6291f43_MD5.png) 程序运行之后，会看到GPIO3\_B6引脚外接的LED小灯会进行呼吸式亮度变化。至此我们的PWM实验就完成了。

微信公众号

内容来源：csdn.net

作者昵称：北京迅为

原文链接：https://blog.csdn.net/BeiJingXunWei/article/details/138081310

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

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第17章 PWM应用编程/90bd0cbf3aff8fdff8bf9b011b581e20\_MD5.png](assets/第17章%20PWM应用编程/90bd0cbf3aff8fdff8bf9b011b581e20_MD5.png)

程序员都在用的中文IT技术交流社区

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第17章 PWM应用编程/08a47e60886378fe60a3d9c8f4ae8bc6\_MD5.png](assets/第17章%20PWM应用编程/08a47e60886378fe60a3d9c8f4ae8bc6_MD5.png)

专业的中文 IT 技术社区，与千万技术人共成长

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第17章 PWM应用编程/a51be6c085b867a5bd82d8dc1cea9b46\_MD5.png](assets/第17章%20PWM应用编程/a51be6c085b867a5bd82d8dc1cea9b46_MD5.png)

关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！

客服 返回顶部

微信公众号

![嵌入式知识学习（通用扩展）/linux基础知识/Linux系统编程篇/assets/第17章 PWM应用编程/efb7921311640694e61fee00900550d6\_MD5.jpg](assets/第17章%20PWM应用编程/efb7921311640694e61fee00900550d6_MD5.jpg) 公众号名称：迅为电子 微信扫码关注或搜索公众号名称

复制公众号名称