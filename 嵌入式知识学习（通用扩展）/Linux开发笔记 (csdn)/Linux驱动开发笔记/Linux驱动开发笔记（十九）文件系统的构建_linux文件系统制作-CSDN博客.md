---
title: "Linux驱动开发笔记（十九）文件系统的构建_linux文件系统制作-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/140445672?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读1.3k次，点赞20次，收藏32次。上节我们在mdev实验进行配置时，利用了busybox，这里着重对这部分进行学习。文件系统可直观的理解为Windows上的文件资源管理器，Linux启动后一定要挂载一个文件系统，这样程序才能被执行。文件系统可大可小，通过构造文件系统可衍生QT,ubuntu,android等系统。Linux还有一个重要思想：一切皆文件，像串口，led,按键等这些硬件设备，都可以归结为像文件一样的操作，如read,write,open,close。_linux文件系统制作"
tags:
  - "clippings"
---
---

## 前言

  上节我们在mdev实验进行配置时，利用了 [busybox](https://so.csdn.net/so/search?q=busybox&spm=1001.2101.3001.7020) ，这里着重对这部分进行学习。

---

## 一、文件系统

### 1.1 Linux系统的组成

  一个完整的嵌入式Linux系统包括uboot， kernel ，根文件系统三个部分。其启动顺序为：系统上电时，先执行uboot，由其引导kernel，根最后挂载根文件系统。

### 1.2 什么是文件系统

  文件系统可直观的理解为 Windows 上的文件资源管理器，Linux启动后一定要挂载一个文件系统，这样程序才能被执行。文件系统可大可小，通过构造文件系统可衍生QT,ubuntu,android等系统。Linux还有一个重要思想：一切皆文件，像串口，led,按键等这些硬件设备，都可以归结为像文件一样的操作，如read,write,open,close。  
  根文件系统也是文件系统的一个，是挂载在根目录，有特定目录构成的文件系统，如下图所示。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/754efa0322d84e9f98d3468d34547eb4.png#pic_center)

- /bin：包含基本用户命令的二进制可执行文件，例如：ls, cp, mv, rm 等。
- /boot：存放启动加载程序及其配置文件以及Linux内核映像文件。
- /dev：包含设备文件，每个文件代表系统中的一个设备，例如：硬盘、终端、打印机等。
- /etc：系统的配置文件和脚本存放目录，包括启动脚本、网络配置文件、用户密码文件等。
- /home：用户的主目录，每个用户都有一个单独的目录，存放用户的个人文件和配置。
- /lib：存放系统和应用程序所需的共享库文件以及内核模块。
- /media：自动挂载的可移动媒体设备（如CD-ROM、USB驱动器）目录。
- /mnt：临时挂载文件系统的挂载点，用于手动挂载文件系统。
- /opt：可选的应用程序包存放目录，通常用于安装第三方软件。
- /proc：一个虚拟文件系统，提供系统进程和内核信息。
- /root：超级用户（root）的主目录。
- /run：存放应用程序和服务启动时创建的临时文件。
- /sbin：包含系统管理的二进制可执行文件，通常只有超级用户可以运行，例如：ifconfig, reboot, shutdown 等。
- /sys：一个虚拟文件系统，提供设备和内核模块信息。
- /tmp：存放临时文件，系统重启后该目录下的文件通常会被删除。
- /usr：用户二进制文件和只读数据的目录，包含子目录：
	- /usr/bin：用户命令的二进制可执行文件。
	- /usr/lib：库文件。
	- /usr/sbin：超级用户的系统管理命令。
	- /usr/share：共享数据文件。
	- /usr/local：本地自定义安装的软件和文件。
- /var：可变数据文件目录，例如日志文件、邮件、缓存等。

## 二、根文件系统的制作工具

  制作根文件系统（Root Filesystem，RootFS）是构建 嵌入式系统 或定制操作系统的重要步骤。根文件系统包含系统启动所需的所有文件和目录，包括内核模块、系统库、应用程序和配置文件。在Linux开发中，最常用的制作工具为以下5种：

| 工具名称 | 优点 | 缺点 |
| --- | --- | --- |
| busybox | 体积小，支持常用命令，定制小系统 | 功能不全，无包管理工具 |
| buildroot | 结构简单，容易理解，可产生完整镜像 | 无包管理工具 |
| yocto | 支持的框架较多，可产生完整镜像 | 配置复杂，不利用新手 |
| Ubuntu | 结构简单，有包管理工具，支持ROS 1x等机器人操作系统 | 构建文件系统较大 |
| Debian | 结构简单，有包管理工具，支持可视化界面 | 构建文件系统较大 |

## 三、busybox

### 3.1 什么是busybox

  BusyBox 是一个用于嵌入式系统的通用工具包，它将许多常见的Linux实用程序组合成一个小巧的可执行文件。BusyBox 提供了许多与大型 GNU Core Utilities 相同的功能，但它们经过优化以尽量减少可执行文件和所需内存的大小。

- 主要特性
	- 集成度高：  
		BusyBox 将众多 UNIX 工具整合为一个单一的可执行文件，这使得它非常适合资源受限的嵌入式系统。  
		它支持包括 ls, cp, mv, rm, cat, echo, grep, awk 等在内的多种命令。
	- 可配置性强：  
		可以通过配置选项选择需要的功能，从而裁剪出适合特定需求的 BusyBox 二进制文件。  
		支持静态编译和动态编译，适应不同的系统需求。
	- 小巧高效：  
		由于其小巧的体积和高效的设计，BusyBox 非常适合用于嵌入式系统，如路由器、嵌入式 Linux 设备等。
	- 广泛的指令集支持：  
		支持多种处理器架构，包括 ARM、x86、MIPS、PowerPC 等，适应不同的硬件平台。
- 常见用法
	- 系统初始化：  
		BusyBox 常被用作系统启动过程中初始化脚本的核心工具，通过提供基础命令来挂载文件系统、启动服务等。
	- 救援系统：  
		在系统崩溃或故障时，BusyBox 可以作为紧急救援系统使用，提供基本的系统修复工具。
	- 嵌入式系统：  
		由于其小巧和高效，BusyBox 广泛用于各种嵌入式 Linux 系统，如路由器、智能家居设备、工业控制系统等。

### 3.2 制作流程

1. 下载BusyBox
```bash
wget https://busybox.net/downloads/busybox-1.33.1.tar.bz2
tar xvjf busybox-1.33.1.tar.bz2
cd busybox-1.33.1
123
```
1. 配置交叉编译工具和相关设置
```bash
//打开图形界面
make defconfig
make menuconfig

//输入交叉编译工具位置,大致是这样的格式，和你具体的位置有关
.../prebuilts/gcc/linux-x86/aarch64/gcc-linaro-6.3.1-2017.05-x86_64_aarch64-linux-gnu/bin/aarch64-linux-gnu-
123456
```

  打开图形界面后，在设置里找到Cross compiler prefix ，设置交叉编译工具地址  
![图形界面](https://i-blog.csdnimg.cn/direct/5feee1adbdd0408eb14443edf12ed3c8.png#pic_center)

1. 创建根文件系统目录
```bash
mkdir -p rootfs/{bin,sbin,etc,usr,lib,var,dev,proc,sys,tmp}
1
```
1. 安装BusyBox
```bash
make CONFIG_PREFIX=./rootfs install
1
```
1. 完善固件库文件
```bash
//进入生成的rootfs目录下的lib目录
cd lib
//将交叉编译文件里面的lib复制过来
cp .../prebuilts/gcc/linux-x86/aarch64/gcc-linaro-6.3.1-2017.05-x86_64_aarch64-linux-gnu/aarch64-linux-gnu/libc/lib* . -rffd
1234
```
1. 创建启动脚本
```bash
mkdir -p rootfs/etc/init.d
sudo sh -c 'echo "#!/bin/sh\nmount -t proc none /proc\nmount -t sysfs none /sys\nexec /bin/sh" > rootfs/etc/init.d/rcS'
sudo chmod +x rootfs/etc/init.d/rcS
123
```

**注：init.d/rcS 文件是系统启动时执行的初始化脚本，通常会在这里编写需要的启动项和初始化步骤。你可以在这个文件中添加任何需要在系统启动时执行的命令，例如挂载文件系统、启动服务、设置网络等。**

1. 配置启动文件
```bash
sudo sh -c 'echo "::sysinit:/etc/init.d/rcS" > rootfs/etc/inittab'
1
```
1. 打包根文件系统
- 方案一：压缩包形式
```bash
cd rootfs
sudo tar -czf ../rootfs.tar.gz .
12
```

将 rootfs.tar.gz 解压到目标文件系统中，并在启动时挂载。

- 方案二：镜像形式
```bash
dd if=/dev/zero of=rootfs.img bs=1M count=64  # 创建一个空的 64MB 文件
mkfs.ext4 rootfs.img                          # 格式化为 ext4 文件系统
mkdir -p /mnt/rootfs
sudo mount -o loop rootfs.img /mnt/rootfs     # 挂载
sudo cp -r rootfs/* /mnt/rootfs               # 复制文件系统内容
sudo umount /mnt/rootfs                       # 卸载
123456
```

将 rootfs.img烧录到设备中，并在启动时挂载。

## 四、buildroot

### 4.1 什么是Buildroot

  Buildroot 是一个用于构建 [嵌入式 Linux](https://so.csdn.net/so/search?q=%E5%B5%8C%E5%85%A5%E5%BC%8F%20Linux&spm=1001.2101.3001.7020) 系统的开源项目。它通过提供简便的配置接口和 自动化 工具，能够从源码生成一个完整的嵌入式 Linux 系统，包括引导加载程序、Linux 内核和根文件系统。由于 Buildroot 提供了自动化的配置和生成过程，所以在使用 Buildroot 构建嵌入式 Linux 系统时，通常不需要手动编写启动项或者创建目录文件。

### 4.2 制作流程

1. 获取 Buildroot
```bash
git clone https://git.busybox.net/buildroot
cd buildroot
12
```
1. 配置 Buildroot  
	同样使用 `make menuconfig` 命令配置 Buildroot。该命令会打开一个基于菜单的配置界面：  
	在配置界面中，可以配置以下内容：
	- 目标架构（Target Architecture）
	- 目标架构变种（Target Architecture Variant）
	- 工具链（Toolchain）
	- 包管理器（Target Packages）
	- 系统配置（System Configuration）
2. 构建系统  
	配置完成后，使用 `make` 命令开始构建整个系统：  
	Buildroot 会根据配置下载、解压、编译并安装所有所需的软件包。这一过程可能需要一些时间，取决于所选择的软件包和系统的性能。
3. 生成的输出  
	构建完成后，生成的输出文件位于 output/images 目录中，包含以下文件：
	- 引导加载程序（如 U-Boot）
	- Linux 内核镜像（如 zImage 或 uImage）
	- 根文件系统映像（如 rootfs.ext2、rootfs.tar.gz 等）
4. 烧录到设备

---

**免责声明：本实验基于网络上的公开资料若有侵权请联系作者删除。**

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/140445672

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