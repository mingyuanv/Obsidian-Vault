---
title: "RK3568驱动指南｜第二篇 字符设备基础-第7章 menuconfig图形化配置实验-CSDN博客"
source: "https://blog.csdn.net/BeiJingXunWei/article/details/132755074"
author:
  - "[[成就一亿技术人!]]"
  - "[[hope_wisdom 发出的红包]]"
published:
created: 2025-09-08
description: "文章浏览阅读1.5k次，点赞2次，收藏8次。上一小节我们打开的图形化配置界面是如何生成的呢？图形化配置界面中的每一个界面都会对应一个Kconfig文件。所以图形化配置界面的每一级菜单是由Kconfig文件来决定的。图形化配置界面有很多菜单。所以就会有很多Kconfig文件，这也就是为什么我们会在内核源码的每个子目录下，都会看到Kconfig文件的原因，那掌握Kconfig文件相关的知识是不是就非常重要呢。所以这一小节我们来看下如何编写Kconfig文件来生成图形化配置界面，也就是Kconfig文件的语法是什么。Mainmenu。_rk3568驱动"
tags:
  - "clippings"
---

## 7.1图形化界面的操作

### 安装ncurses库

> menuconfig图形化的配置工具需要 ncurses 库支持。ncurses库提供了一系列的API函数供调用者生成基于文本的图形界面，因此在使用menuconfig图形化配置界面之前需要先在 Ubuntu 中安装ncurses库，命令如下：

```shell
sudo apt-get install build-essential

sudo apt-get install libncurses5-dev

```

### 图形化配置界面主要有以下四种
> 在这四种方式中，最推荐的是 **make menuconfig**，它不依赖于 QT 或 GTK+，且非常直观。

```shell
make config （基于文本的最为传统的配置界面，不推荐使用）

make menuconfig （基于文本菜单的配置界面）

make xconfig （要求 QT 被安装）

make gconfig （要求 GTK+ 被安装）
shell1234567```


### 打开menuconfig图形化配置界面

以RK3568为例，在内核源码目录下输入以下命令，打开图形化配置界面。

```shell
export ARCH=arm64

make rockchip_linux_defconfig

make menuconfig

```

![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/8f8b3660be8563c4ffd5ade649ea3b0f\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/8f8b3660be8563c4ffd5ade649ea3b0f_MD5.jpg)

打开后界面如下所（图7-2）示：

![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/416627f0f5189eb078c57091694504f8\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/416627f0f5189eb078c57091694504f8_MD5.jpg)

### 图形化配置界面操作方式

| 上下键           | 选择不同的行，即移动到不同的（每一行的）选项上                                                                                                                                                                                               |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 空格键           | 用于在选择该选项，取消选择该选项之间来回切换                                                                                                                                                                                                |
| 选择该（行所在的）选项   | 则对应的该选项前面就变成了 \[ \* \]，表示被选中了。**把驱动编译编译成模块，用 M** 来表示。**把驱动编译到内核里面，用\***来表示。                                                                                                                                           |
| 取消该选项         | 则对应的该选项变成了只有一个中括号，里面是空的，即：\[ \]                                                                                                                                                                                       |
| 左右键           | 用于在 Select/Exit/Help 之前切换                                                                                                                                                                                             |
| 回车键           | 左右键切换到了某个键上，此时回车键，就执行相应的动作                                                                                                                                                                                            |
| Select        | 此时一般都是所在（的行的）选项，后面有三个短横线加上一个右箭头，即 —>，表示此项下面还有子选项，即进入子菜单                                                                                                                                                               |
| Exit          | 直接退出当前的配置。所以，当你更改了一些配置，但是又没有去保存，此时一般都会询问你是否要保存当前（已修改后的最新的）配置，然后再退出。                                                                                                                                                   |
| Help          | **针对你当前所在某个（行的）选项，查看其帮助信息**。一般来说，其帮助信息，都包含针对该选项的很详细的解释。换句话说：如果你对某个选项的功能，不是很清楚，那么就应该认真仔细的去看看其 Help，往往都会找到详细解释，以便你更加了解此配置的含义。另外一般也会写出，此选项所对应的宏。该宏，就是写出到配置文件中的那个宏，对于写 makefile 的人来说，往往也是利用此相关的宏，在 makefile 中，实现对应的不同的控制。 |
| 快捷键快速跳转到对应的选项 | menuconfig 中的每一行的选项，都有一个用特殊颜色标记出来的字母，很明显，**此字母，就是该行的快捷字母**。注意：此类快捷字母，一般都是大写的，且是大小写区分的                                                                                                                                 |
| / 键           | 输入“/”即可**弹出搜索界面**，然后输入我们想要搜索的内容即可。                                                                                                                                                                                    |
|               |                                                                                                                                                                                                                       |

## 7.2 Kconfig 语法简介

> 上一小节我们打开的图形化配置界面是如何生成的呢？图形化配置界面中的**每一个界面都会对应一个Kconfig文件**。所以图形化配置界面的每一级菜单是由Kconfig文件来决定的。

> 图形化配置界面有很多菜单。所以就会有很多Kconfig文件，这也就是为什么我们会在**内核源码的每个子目录下，都会看到Kconfig文件**的原因，那掌握Kconfig文件相关的知识是不是就非常重要呢。


### 1. Mainmenu：设置主菜单的标题

mainmenu顾名思义就是主菜单，也就是我们输入完“make menuconfig”以后默认打开的界面，mainmenu用来设置主菜单的标题，如下所示：

> mainmenu “Linux/$(ARCH) $(KERNELVERSION) Kernel Configuration”

此行代码是设置菜单的名字为“Linux/$(ARCH) $(KERNELVERSION) Kernel Configuration”。如下图（图7-4）所示，ARCH变量是通过“export ARCH=arm64”设置的，内核版本KERNELVERSION为4.19.232。

![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/dc21f77073c721b1bc3bbf3b3895e343\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/dc21f77073c721b1bc3bbf3b3895e343_MD5.jpg)

### 2.source：读取另一个kconfig文件

source用于读取另一个Kconfig文件，比如“source “init/Kconfig””就是读取init目录下的Kconfig文件。

### 3.menu/endmenu：生成菜单

> menu/endmenu条目用于生成菜单，如下（图7-5）所示，生成了Watchdog Timer Support的菜单。

```makefile
menu "Watchdog Timer Support"
 
config HW_WATCHDOG
    bool
 
config WDT
    bool "Enable driver model for watchdog timer drivers"
    depends on DM
    help
      Enable driver model for watchdog timer. At the moment the API.
......
endmenu
```

> menu之后的字符串是菜单名，“menu”是菜单开始的标志，“endmenu”是菜单结束的标志，这俩个是成对出现的**menu和endmenu之间有很多config条目**。在kernel目录下输入make menuconfig，如下图（图7-6）所示，可以看到上述代码描述的"Watchdog Timer Support"菜单。

![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/8ed026ae97e9a9c3a5ef0ce8d8cfd134\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/8ed026ae97e9a9c3a5ef0ce8d8cfd134_MD5.jpg)

进入“ Watchdog Timer Support —> ”可以看到很多config定义的条目，如下（图7-7）所示：

![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/addb491d1366d5f29de7575f6dfd080f\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/addb491d1366d5f29de7575f6dfd080f_MD5.jpg)

### 4.if/endif

if/endif 语句是一个条件判断，定义了一个 if 结构，Kconfig中代码如下（图7-8）所示：

```makefile
menu "Hardware Drivers Config"
    menuconfig BSP_USING_CAN
        bool "Enable CAN"
        default n
        select RT_USING_CAN
        if BSP_USING_CAN
            config BSP_USING_CAN1
                bool "Enable CAN1"
                default n
        endif
endmenu
makefile1234567891011
```

图 7-8

当没有选中 “Enable CAN” 选项时，下面通过 if 判断的 Enable CAN1 选项并不会显示出来。当上一级菜单选中 “Enable CAN” 时，Enable CAN1 选项才会显示。

### 5. choice/endchooice：可选择项

choice条目将多个类似的配置选项组合到一起，供用户选择，用户选择是从“choice”开始，从“endchoice”结束，“choice”和“endchoice”之间有很多的config条目，这些config条目是提供用户选择的，如下（图7-9）所示：

```makefile
choice
        bool "Parade TrueTouch Gen5 MultiTouch Protocol"
        depends on TOUCHSCREEN_CYPRESS_CYTTSP5
        default TOUCHSCREEN_CYPRESS_CYTTSP5_MT_B
        help
          This option controls which MultiTouch protocol will be used to
          report the touch events.
config TOUCHSCREEN_CYPRESS_CYTTSP5_MT_A
        bool "Protocol A"
        help
          Select to enable MultiTouch touch reporting using protocol A
          on Parade TrueTouch(tm) Standard Product Generation4 touchscreen
          controller.
 
config TOUCHSCREEN_CYPRESS_CYTTSP5_MT_B
        bool "Protocol B"
        help
          Select to enable MultiTouch touch reporting using protocol B
          on Parade TrueTouch(tm) Standard Product Generation4 touchscreen
          controller.
 
endchoice
makefile12345678910111213141516171819202122
```

我们在内核目录下输入make menuconfig可以看到，如下（图7-10）所示，“Parade TrueTouch Gen5 MultiTouch Protocol”是choice选项名称，“Protocol B”是Kconfig里面默认选择的。“–>”代表此菜单能进入，需要键盘操作进入。

![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/33525b0d69c3ebd0aad366330c2ea259\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/33525b0d69c3ebd0aad366330c2ea259_MD5.jpg)

进入“Parade TrueTouch Gen5 MultiTouch Protocol”后，可以看到多选项提供给用户进行选择，如下（图7-11）所示：

![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/eeccd0168c91cdd3c7e5543ce167780f\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/eeccd0168c91cdd3c7e5543ce167780f_MD5.jpg)

### 6.comment：注释

comment 语句出现在界面的第一行，用于定义一些提示信息。

comment “Compiler: $(CC\_VERSION\_TEXT)”

以上代码的配置界面如下（图7-12）所示：

![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/97f8475778ab756f09371e3fe24dd685\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/97f8475778ab756f09371e3fe24dd685_MD5.jpg)

### 7.config：配置选项

使用关键字config来定义一个新的选项，如下（图7-13）所示

```shell
config helloworld
    bool “hello world support”
    default y
    help
        hello world
12345
```

如上所示，使用config关键字定义了一个“helloworld”选项，每个选项都必须指定类型，类型包括bool，tristate,string,hex,int。最常见的是bool,tristate,string这三个。

- bool类型取值只有“y”和“n”
- tristate类型的变量取值有3种：“y”,“n”,“m”
- string类型取值为字符串
- hex类型取值为十六进制的数据
- int类型取值为十进制的数据
- help表示帮助信息，当我们在图形化界面按下h按键，弹出来的就是help的内容。

### 8.depends on

Kconfig中depends on关键字用来指定依赖关系，当依赖的选项被选中时，当前的配置选项的信息才会在菜单中显示出来，才能操作该选项的内容。举例来说，如下所示，选项A依赖选项B，只有当选项B被选中时，选项A才可以被选中。

```shell
config A

depends on B
```

### 9.select

Kconfig中select关键字用来表示反向依赖关系，当指定当前选项被选中时，此时select后面的选项也会被自动选中。举个例子来说，如下所示，在选项A被选中的情况下，选项B自动被选中。

```shell
config A

select on B
123
```

### 10. menuconfig

menuconfig可以认为是config 中的升级版。menuconfig也是一个正常的配置项，通过自己的配置值来决定另外一组配置项是否作为子菜单的形式显示出来并供用户配置。代码如下（图7-14）所示。

```makefile
menuconfig NETDEVICES
    default y if UML
    depends on NET
    bool "Network device support"
    ---help---
if NETDEVICES
config MII
    tristate

config NET_CORE
    default y
    bool "Network core driver support"
    ---help---
      You can say N here if you do not intend to use any of the
      networking core drivers (i.e. VLAN, bridging, bonding, etc.)
makefile123456789101112131415
```

以上代码中通过menuconfig配置了一个bool类型的配置项，在图形化配置界面中显示（图7-15）如下：

![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/0ed0f50d7e9c51bc6d93ed48e78f54a8\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/0ed0f50d7e9c51bc6d93ed48e78f54a8_MD5.jpg)

当我们选中"Network device support"配置项时，其子菜单被显示出来，如下图（图7-16）所示：

![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/aa2f5f7dc91f842a35c63f4c0f221c7d\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/aa2f5f7dc91f842a35c63f4c0f221c7d_MD5.jpg)

## 7.3.config配置文件介绍

我们在图形化配置界面配置好了以后，会得到一个.config配置文件。在编译内核的时候会根据这个.config文件来编译内核。这样是不是就实现了通过图像化界面的配置来配置内核呀。
### 用通俗的话来说
> - `Kconfig 文件`：就像是电脑厂商提供的一个详细的、带逻辑判断的“配置清单”。**清单上列出了所有可选的部件**（CPU型号、内存大小、显卡型号、是否要光驱等），并且告诉你哪些部件是兼容的（比如选了某个主板，就只能选特定的CPU），选了某个高端显卡会自动给你配一个大功率电源。
> - `make menuconfig`: 就是你根据这份清单，在一个**交互界面**上勾选你想要的配置。
> - `.config` 文件：就是你**最终确认的、写下来的配置单**。
> - `Makefile`: 就是工厂的**生产流水线**，它会严格按照你的配置单（`.config`），去仓库（源代码）里拿对应的零件（源文件）来组装你的电脑（编译内核）。



### .config是如何产生的呢？
对应上面的例子就是要有服务员给我们点菜呀。

> 当我们使用make menuconfig的时候，会通过**mconf程序去解析Kconfig文件，然后生成对应的配置文件.config**。所以这个mconf就是服务员。

- 1 mconf程序源码在内核源码scripts/kconfig目录下
，如下图所示，这里不对Kconfig文件的解析流程进行分析，感兴趣的同学可以自行分析下mconf的源码。

![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/02920296d1ed7246b0ed601f4ffcd9ff\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/02920296d1ed7246b0ed601f4ffcd9ff_MD5.jpg)

### .config配置文件来编译内核的实现方式(💌)
，比如控制某些驱动编译进内核，或者控制某些驱动不编译内核。那他是怎么实现的呢？

> .config会**通过syncconfig**目标将.config作为输入然后**输出**需要文件，这里我们重点更关注**auto.conf和autoconf.h**。如下图（图7-19）所示：

![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/bf97c7a0b224fbbd68fa75311063f521\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/bf97c7a0b224fbbd68fa75311063f521_MD5.jpg)

#### auto.conf文件 - 存放的是配置信息

![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/aab72d856894a8d04f547017899cba1b\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/aab72d856894a8d04f547017899cba1b_MD5.jpg)

> 在内核源码的顶层**Makefile中会包含auto.conf**文件，以此**引用其中的变量来控制Makefile的动作**，如哪些驱动编译，哪些驱动不编译。如：

- 1 auto.conf文件中
```shell
include include/config/auto.conf
CONFIG _A=y
```

- 1 Makefile中包含auto.conf文件
```shell
ifeq ($(dot-config),1)
include include/config/auto.conf
Endif
```

- 2 内核源码下drivers/A/Makefile引用这个变量

```shell
obj-$(CONFIG _A) +=A.o
1
```

> 注：**obj-y就是编译进内核，obj-m就是编译成ko文件**。

#### autoconf.h文件 - 用来配合编译时的条件选择

![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/3db01570f39bc9779e3985a5cff528b0\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/3db01570f39bc9779e3985a5cff528b0_MD5.jpg)

## 7.4 defconfig配置文件（特色菜）

> defconfig文件和.config文件都是linux内核的配置文件，defconfig文件在内核源码的**arch/$(ARCH)/configs**目录下，是**Linux系统默认的配置文件**。
> 比如说瑞芯微平台Linux源码默认的配置文件为：kernel/arch/arm64/configs/rockchip\_linux\_defconfig。

.config文件位于Linux内核源码的顶层目录下，编译Linux内核时会使用.config文件里面的配置来编译内核镜像。

> 如果.config文件存在，**make menuconfig界面的默认配置也就是当前.config文件的配置**，如果修改了图形化配置界面的设置并保存，那么.config文件会被更新。

> 如果.config文件不存在，使用命令**make XXX\_defconfig**命令会根据arch/$(ARCH)/configs目录下的XXX\_defconfig**自动生成.config**。make menuconfig界面的默认配置则为defconfig文件中的默认配置，比如说瑞芯微平台Linux内核源码目录下输入“make rockchip\_linux\_defconfig”会自动生成.config文件。那么此时rockchip\_linux\_defconfig的配置项和.config的配置项是相同的。


[[嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/b7431161dc4d3afbf61b306ee1221f28_MD5.jpeg|Open: 1757341209954.jpg]]
![[嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/（废弃）扩展：menuconfig图形化配置界面/b7431161dc4d3afbf61b306ee1221f28_MD5.jpeg]]





## 7.5 自定义菜单实验

有了上面的理论基础后，我们就可以自己在图形化配置界面中来自定义一个菜单，要定义一个菜单，根据我们前面的分析，是不是就要从Kconfig文件入手呀。因为图形化配置界面是根据Kconfig文件来生成的！

1 在kernel目录下创建一个topeet的文件夹，如下（图7-22）所示：

![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/63da9882533d4a823f3d5c198fd1cfd0\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/63da9882533d4a823f3d5c198fd1cfd0_MD5.jpg)

2 打开kernel下的Kconfig文件，在里面加入以下代码：

source “topeet/Kconfig”

添加完成后如下（图7-23）所示：

![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/93fa2efc32ed69a544e12e129b7b0546\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/93fa2efc32ed69a544e12e129b7b0546_MD5.jpg)

3 然后进入到topeet文件夹，在此文件夹下创建一个Kconfig文件，创建完成如下（图7-24）所示：

![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/bd7de5ea5f9e90a66a312396f7c32547\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/bd7de5ea5f9e90a66a312396f7c32547_MD5.jpg)

4 打开创建好的Kconfig文件，写入以下（图7-25）内容：

```makefile
menu "test menu"
config TEST_CONFIG
    bool "test"
    default y
    help
        just test
    comment "just test"
endmenu
```

在上面的代码中，我们在主菜单中添加了一个名为 test menu 的子菜单，然后在这个子菜单里面我们添加了一个名为 TEST\_CONFIG 的配置项，这个配置项变量类型为 bool，默认配置为 Y，帮助信息为 just test，注释为 just test。添加完成如下图（图7-26）所示：

![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/820bf66a6131428eaf9ffede851431ca\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/820bf66a6131428eaf9ffede851431ca_MD5.jpg)

5 添加完成以后，打开图形化配置界面，如下图（图7-27）所示：

![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/4601031c0b42d1eca862dad65a35f42e\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/4601031c0b42d1eca862dad65a35f42e_MD5.jpg)

6子菜单中的配置项，默认为 y，注释信息为 just test。

![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/83e92542c8d9a87aa9068233d8fd1a6f\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/83e92542c8d9a87aa9068233d8fd1a6f_MD5.jpg)

7 在此界面输入？，显示帮助信息为 just test，如下（图7-29）所示：

![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/c8a2e489fb0345f8ed05d41a56b4a4a1\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/c8a2e489fb0345f8ed05d41a56b4a4a1_MD5.jpg)

8 保存退出后，打开内核源码目录下的.config 文件，如下图（图7-30）所示：

![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/9db7d2414ec125122cf0c711e0b68e7d\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/9db7d2414ec125122cf0c711e0b68e7d_MD5.jpg)

9 可以在这个.config 文件中找到添加的 TEST\_CONFIG（注意，我们需要在 make menuconfig 中保存才可以看到，否则是看不到我们添加的这个选项的），这样在编译内核的时候就可以根据这个配置信息来执行对应的操作了，就是我们下一章节要给大家讲的把驱动编译进内核，如下图所示：

![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/5dc2a751bed7b6cd1eeb22c39e5e4fe1\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/5dc2a751bed7b6cd1eeb22c39e5e4fe1_MD5.jpg)































![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/08a47e60886378fe60a3d9c8f4ae8bc6\_MD5.png](assets/第7章%20menuconfig图形化配置实验/08a47e60886378fe60a3d9c8f4ae8bc6_MD5.png)

专业的中文 IT 技术社区，与千万技术人共成长

![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/a51be6c085b867a5bd82d8dc1cea9b46\_MD5.png](assets/第7章%20menuconfig图形化配置实验/a51be6c085b867a5bd82d8dc1cea9b46_MD5.png)

关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！

客服 返回顶部

微信公众号

![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/efb7921311640694e61fee00900550d6\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/efb7921311640694e61fee00900550d6_MD5.jpg) 公众号名称：迅为电子 微信扫码关注或搜索公众号名称

复制公众号名称

![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/8f8b3660be8563c4ffd5ade649ea3b0f\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/8f8b3660be8563c4ffd5ade649ea3b0f_MD5.jpg) ![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/416627f0f5189eb078c57091694504f8\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/416627f0f5189eb078c57091694504f8_MD5.jpg) ![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/dc21f77073c721b1bc3bbf3b3895e343\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/dc21f77073c721b1bc3bbf3b3895e343_MD5.jpg) ![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/8ed026ae97e9a9c3a5ef0ce8d8cfd134\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/8ed026ae97e9a9c3a5ef0ce8d8cfd134_MD5.jpg) ![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/addb491d1366d5f29de7575f6dfd080f\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/addb491d1366d5f29de7575f6dfd080f_MD5.jpg) ![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/33525b0d69c3ebd0aad366330c2ea259\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/33525b0d69c3ebd0aad366330c2ea259_MD5.jpg) ![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/eeccd0168c91cdd3c7e5543ce167780f\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/eeccd0168c91cdd3c7e5543ce167780f_MD5.jpg) ![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/97f8475778ab756f09371e3fe24dd685\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/97f8475778ab756f09371e3fe24dd685_MD5.jpg) ![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/0ed0f50d7e9c51bc6d93ed48e78f54a8\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/0ed0f50d7e9c51bc6d93ed48e78f54a8_MD5.jpg) ![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/aa2f5f7dc91f842a35c63f4c0f221c7d\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/aa2f5f7dc91f842a35c63f4c0f221c7d_MD5.jpg) ![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/02920296d1ed7246b0ed601f4ffcd9ff\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/02920296d1ed7246b0ed601f4ffcd9ff_MD5.jpg) ![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/bf97c7a0b224fbbd68fa75311063f521\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/bf97c7a0b224fbbd68fa75311063f521_MD5.jpg) ![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/aab72d856894a8d04f547017899cba1b\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/aab72d856894a8d04f547017899cba1b_MD5.jpg) ![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/3db01570f39bc9779e3985a5cff528b0\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/3db01570f39bc9779e3985a5cff528b0_MD5.jpg) ![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/63da9882533d4a823f3d5c198fd1cfd0\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/63da9882533d4a823f3d5c198fd1cfd0_MD5.jpg) ![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/93fa2efc32ed69a544e12e129b7b0546\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/93fa2efc32ed69a544e12e129b7b0546_MD5.jpg) ![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/bd7de5ea5f9e90a66a312396f7c32547\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/bd7de5ea5f9e90a66a312396f7c32547_MD5.jpg) ![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/820bf66a6131428eaf9ffede851431ca\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/820bf66a6131428eaf9ffede851431ca_MD5.jpg) ![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/4601031c0b42d1eca862dad65a35f42e\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/4601031c0b42d1eca862dad65a35f42e_MD5.jpg) ![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/83e92542c8d9a87aa9068233d8fd1a6f\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/83e92542c8d9a87aa9068233d8fd1a6f_MD5.jpg) ![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/c8a2e489fb0345f8ed05d41a56b4a4a1\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/c8a2e489fb0345f8ed05d41a56b4a4a1_MD5.jpg) ![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/9db7d2414ec125122cf0c711e0b68e7d\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/9db7d2414ec125122cf0c711e0b68e7d_MD5.jpg) ![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第7章 menuconfig图形化配置实验/5dc2a751bed7b6cd1eeb22c39e5e4fe1\_MD5.jpg](assets/第7章%20menuconfig图形化配置实验/5dc2a751bed7b6cd1eeb22c39e5e4fe1_MD5.jpg)