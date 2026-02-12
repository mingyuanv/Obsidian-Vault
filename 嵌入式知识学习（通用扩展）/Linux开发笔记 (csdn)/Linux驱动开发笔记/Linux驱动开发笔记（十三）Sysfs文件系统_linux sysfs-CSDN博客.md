---
title: "Linux驱动开发笔记（十三）Sysfs文件系统_linux sysfs-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/139882450?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读2.5k次，点赞41次，收藏48次。前面章节驱动学习中，我们测试驱动时经常使用/sys目录下文件，我们本章就简单介绍下Sysfs文件系统。_linux sysfs"
tags:
  - "clippings"
---
---

## 前言

  前面章节驱动学习中，我们测试驱动时经常使用/sys目录下文件，我们本章就简单介绍下Sysfs文件系统。

## 一、Sysfs

### 1.1 Sysfs的引入

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c4b166a8a17934ab2f772435cef6f0be.png)  
  sysfs则是 Linux 内核中的一种特殊虚拟文件系统，它用来向用户空间提供内核设备和 [驱动程序](https://so.csdn.net/so/search?q=%E9%A9%B1%E5%8A%A8%E7%A8%8B%E5%BA%8F&spm=1001.2101.3001.7020) 的信息。因此，sysfs是一种具体的文件系统实现，它利用了VFS提供的抽象接口来展示内核数据。Sysfs在Linux内核2.6版本中引入，旨在替代和扩展早期的proc文件系统。它提供了一种统一的接口，用于查看和操作设备、驱动程序、文件系统等内核对象。Sysfs采用层次化的目录结构，反映了内核对象之间的关系，目录和文件分别表示内核对象及其属性。  
  内核对象（如设备、驱动程序等）在sysfs中被表示为目录，目录下的文件表示对象的属性。这些文件通常是只读的，但有些也可以通过写操作进行配置。  
  通过sysfs，用户可以统一地访问不同类型的内核信息，而不需要关心底层实现细节。Sysfs内容会随着系统硬件配置的变化动态更新。例如，插拔设备会导致相应的sysfs目录和文件创建或删除。

### 1.2 Sysfs的目录结构

  Sysfs文件系统是一种虚拟文件系统，也就是文件系统中文件不对应硬盘上任何文件，存在于内存中，其通常挂载在/sys目录下，主要目录包括：

```bash
/sys/devices：表示系统中的物理设备，每个子目录对应一个设备。
/sys/class：表示系统中的设备类别（如网络设备、块设备等），子目录按类别分类。
/sys/block：表示块设备（如硬盘、USB存储设备等）。
/sys/bus：表示系统总线类型（如PCI、USB等），每个子目录对应一个总线。
/sys/kernel：表示内核参数和信息，如调度器参数、内核模块等。
/sys/module：表示加载的内核模块，每个子目录对应一个模块，包含模块参数和状态信息。
123456
```

  Sysfs是通过内核中的 对象模型 （kobject）实现的。每个kobject都可以在sysfs中创建一个对应的目录，kobject的属性（kobj\_attribute）则映射为sysfs中的文件。通过定义和注册kobject和kobj\_attribute，内核模块可以在sysfs中创建自己的条目。这些目录是在子系统注册kobject核心的系统启动时刻产生的, 当它们被初始化以后, 它们开始搜寻在各自的目录内注册了的对象。 一个kobject对应一个目录，包含的对象属性对应一个文件，文件只支持 目录、 普通文件 (文本或二进制文件)和 符号链接文件三种类型。

### 1.2 Sysfs的目录详解

#### 1.2.1 devices

  devices目录反映系统中所有物理设备及其层次结构，设备按照硬件拓扑结构组织，表示设备的物理连接关系。/sys/devices是内核对系统中所有设备的分层次表达模型， 也是/sys文件系统管理设备的最重要的目录结构。其目录结构如下：

- 系统设备：如 CPU、系统内存等。
- 总线设备：例如 PCI、USB、SCSI 等设备。
- 虚拟设备：如虚拟网络设备。

#### 1.2.2 bus

  bus目录包含系统中所有已注册总线类型的子目录，每个子目录表示一种总线类型，例如 PCI、USB、I2C 等。这里是设备按照总线类型分层放置的目录结构， 每个子目录(总线类型)下包含两个子目录——devices和drivers文件夹；其中devices下是该总线类型下的所有设备， 而这些设备都是符号链接，它们分别指向真正的设备(/sys/devices/下)；如下图bus下的usb总线中的device则是Devices目 录下/pci()/dev 0:10/usb2的符号链接。而drivers下是所有注册在这个总线上的驱动，每个driver子目录下 是一些可以观察和修改的driver参数。其目录结构如下：

- devices：列出所有连接到该总线的设备。
- drivers：列出与该总线相关的所有驱动程序。
- drivers\_autoprobe 和 drivers\_probe：用于自动或手动驱动程序绑定。
- uevent：用于触发 uevent 事件。

#### 1.2.3 class

  class 目录按设备类型对设备进行分类，每个子目录表示一种设备类型，例如网络设备、块设备、字符设备等。其目录结构如下：

- net：表示所有网络接口。
- block：表示所有块设备。
- tty：表示所有终端设备。

**注：大家可能注意到在/sys/class目录下也存在一个block子目录，这是由于历史遗留因素而导致的。 块设备现在是已经移到/sys/class/block, 旧的接口/sys/block为了向后兼容保留存在，现在该目录下的都是链接文件**

#### 1.2.4 devices、bus、class目录之间的关系

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a42b4fed9f2fadaaf6a0292eae999fd6.png)

- /sys/devices 目录表示设备的物理连接和层次结构，而 /sys/class 目录按设备功能或类型对设备进行逻辑分类。
- /sys/bus 目录表示系统中的各种总线类型，每种总线都有一个子目录，包含该总线上的设备（链接到 /sys/devices）和驱动程序信息。
- /sys/devices 中的设备可能会在 /sys/bus/<bus\_type>/devices 下有一个符号链接，反映设备与总线的关系。/sys/class 提供了按设备类型的视图，使用户能够方便地找到特定类型的设备，而无需了解设备的具体物理连接位置。

  以USB 存储设备插入系统为例，以下是目录之间关系的具体示例：

```bash
//表示 USB 存储设备的物理连接路径
ls /sys/devices/pci0000:00/0000:00:14.0/usb1/1-1

//目录中包含指向上述设备的符号链接，表示它是一个 USB 设备
ls /sys/bus/usb/devices

//目录中包含该设备的逻辑分类信息，表示它是一个块设备
ls /sys/class/block/sda
12345678
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e169850c9833ecd989d89b78b13edab0.png)

#### 1.2.5 其他子目录

  在Sysfs文件系统中最重要的就是以上三个子目录，其他子目录我们简单了解即可。  
**firmware目录**  
  该目录包含具有固件对象和属性的子目录，关于内核的固件加载和 firmware 驱动，有兴趣可以自己去了解下。其目录结构如下：

- devicetree：描述加载设备树信息，根节点对应base目录，每一个设备树节点对应一个目录，每个属性对应一个文件
- fdt：原始dtb文件，是uboot传给内核的设备树文件，可以使用hexdump -C查看

**fs目录**  
  这里按照设计是用于描述系统中所有文件系统，包括文件系统本身和按文件系统分类存放的已挂载点，描述已注册的文件系统视图， 但目前只有 fuse,ext4 等少数文件系统支持 sysfs 接口，一些传统的虚拟文件系统(VFS)层次控制参数仍然在sysctl(/proc/sys/fs) 接口中。  
**kernel目录**  
  该目录是内核所有可调整参数的位置，有些内核可调整参数仍然位于sysctl(/proc/sys/ kernel)接口中。  
**module目录**  
  该目录有系统中所有模块的信息，不论这些模块是以 内联 (inlined)方式编译到内核映像文件(vmlinuz)中还是编译为外部模块(.ko文件)， 都可能会出现在/sys/module目录下。  
  编译为外部模块(.ko文件)在加载后，会/sys/module/出现对应的模块文件夹,在这个文件夹下会出现一些属性文件和属性目录， 表示此外部模块的一些信息，如版本号、加载状态、所提供的驱动程序等。  
  编译进内核的模块则只在当它有非0属性的模块参数时会出现对应的/sys/module/, 这些模块的可用参数会出现在/sys/modules/parameters/中， 如：/sys/module/printk/parameters/time 这个可读写参数控制着内联模块printk在打印内核消息时是否加上时间前缀。  
**power目录**  
  该目录下是系统中电源选项，包含电源管理子系统提供的统一接口文件。 一些属性文件可以用于控制整个机器的电源状态，如可以向其中写入控制命令进行关机、重启等操作。

## 二、Sysfs使用

### 2.1 核心数据结构

**kobject** 是 [Linux内核](https://so.csdn.net/so/search?q=Linux%E5%86%85%E6%A0%B8&spm=1001.2101.3001.7020) 中的一个核心数据结构，用于表示内核中的对象并支持内核对象的引用计数、生命周期管理和对象间关系管理。它主要用于内核的设备模型（device model）以及 sysfs 文件系统的实现。kobject 提供了一个通用的机制来管理对象，这样不同的子系统可以共享一些通用的代码来处理对象。  
  可以理解为一个kobject就是在/sys下的一个目录,如图所示：  
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/863c2a37f03544f7956e27c01d682d2f.png#pic_center)

```c
struct kobject {
    const char        *name;
    struct list_head  entry;
    struct kobject    *parent;
    struct kset       *kset;
    struct kobj_type  *ktype;
    struct kernfs_node *sd;
    struct kref       kref;
    unsigned int      state_initialized:1;
    unsigned int      state_in_sysfs:1;
    unsigned int      state_add_uevent_sent:1;
    unsigned int      state_remove_uevent_sent:1;
    unsigned int      uevent_suppress:1;
};
1234567891011121314
```
- 关键成员解释
	- name：kobject 的名字，用于在 sysfs 文件系统中表示对象的名字。
	- parent：指向父对象的指针，用于形成层次结构，表示对象之间的包含关系。
	- kref：内核引用计数机制的对象，用于确保 kobject 在引用计数为零之前不会被释放。
	- ktype：指向 kobj\_type 结构体的指针，kobj\_type 定义了 kobject 的特定操作，如释放函数、sysfs 文件操作等。
	- kset：指向 kset 结构体的指针，一个 kset 是一组相关 kobject 的集合，可以用来组织和管理一组相关的对象。  
		**注：kset是kobject的一个集合体，它将多个kset结合起来，此外kset结构体中也包含kobject。kset中的list元素和kobject中的entry相链接；kset中的kobj元素是对kobject的索引。**
	- sd：指向 kernfs\_node 结构体的指针，表示 sysfs 中的目录项。
	- state\_initialized 等标志位：用于跟踪对象的状态，如是否已初始化、是否已添加到 sysfs 中等。

**kobj\_attribute** 是一个用于为kobject（内核对象）创建属性的 结构体 。这些属性可以通过sysfs文件系统进行读取或写入，sysfs提供了一种机制，让内核子系统、设备驱动程序和其他内核模块可以向用户空间导出信息。kobj\_attribute结构体定义在linux/kobject.h中，包含以成员：

- struct attribute attr: 一个通用的属性结构体，包含属性的名称和权限模式。
```c
struct attribute {
    const char *name;//属性的名称，在 sysfs 文件系统中为文件名
    umode_t mode;    //属性的权限模式，定义了用户对这个属性的访问权限
};
1234
```
- ssize\_t (\*show)(struct kobject \*kobj, struct kobj\_attribute \*attr, char \*buf): 指向显示方法的函数指针，当读取属性时调用该方法。
- ssize\_t (\*store)(struct kobject \*kobj, struct kobj\_attribute \*attr, const char \*buf, size\_t count): 指向存储方法的函数指针，当写入属性时调用该方法。

**\_\_ATTR宏** 用于方便地定义struct attribute类型的结构体成员。它通常与kobj\_attribute结构体一起使用，来定义sysfs属性。

```c
#define __ATTR(_name, _mode, _show, _store) { \
    .attr = { .name = __stringify(_name), .mode = _mode }, \
    .show   = _show, \
    .store  = _store, \
}
12345
```
- 参数说明
	- \_name：属性的名称。
	- \_mode：属性的权限模式，如0644，表示所有者可读写，组和其他用户可读。
	- \_show：指向显示函数的指针，该函数在读取属性时被调用。
	- \_store：指向存储函数的指针，该函数在写入属性时被调用。

**Sysfs 和 Kobject 的关系**

- 交互:  
	  kobject 是 sysfs 文件系统的核心组成部分。每个 kobject 通常对应于 sysfs 中的一个目录。kobject 中的属性（通过 kobj\_attribute 定义）可以映射为 sysfs 中的文件，这些文件允许用户空间进行读写操作，从而实现与内核对象的交互。
- 生命周期管理:  
	  当创建一个 kobject 时，它会自动在 sysfs 中创建对应的目录。当 kobject 的引用计数变为零时，它会被销毁，sysfs 中的对应目录和文件也会被删除。

### 2.2 相关函数

  更多的函数可以参考内核源码include/linux/sysfs.h文件。

#### 2.2.1 kobject\_create\_and\_add

```c
//函数用于创建、初始化并将kobject添加到系统中
struct kobject *kobject_create_and_add ( const char *name, struct kobject *parent);
12
```
- 参数
	- name：创建kobj的名字
	- parent：指定父kobject，实际就是在那个目录下创建一个目录。比如为kernel\_kobj，将在/sys/kernel目录下创建目录，如果为NULL，将在/sys下创建。
- 返回值
	- 成功：指向新创建并添加的 kobject 结构体的指针
	- 失败：NULL

#### 2.2.2 kobject\_put()

```c
//用于减少kobject的引用计数，当引用计数降为零时会释放该对象。
void kobject_put(struct kobject *kobj);
12
```
- 参数：
	- kobj：指向要减少引用计数的 kobject 结构体。

#### 2.2.3 kobject\_get()

```c
//用于增加kobject的引用计数
struct kobject *kobject_get(struct kobject *kobj);
12
```
- 参数：
	- kobj：指向要增加引用计数的 kobject 结构体。
- 返回值：
	- 成功：返回 kobj，或者如果 kobj 为 NULL 则返回 NULL。

#### 2.2.4 sysfs\_create\_file

```c
//创建一个文件
int sysfs_create_file ( struct kobject *  kobj, const struct attribute * attr);
12
```
- 参数：
	- kobj：我们创建的kobject
	- attr：属性描述
- 返回值：
	- 成功：0
	- 错误：错误码

### 2.3 设计思路

  在内核中，创建和使用 kobject 通常需要以下步骤：

- 初始化并添加到 sysfs：使用 kobject\_create\_and\_add函数创建kobject并添加到sysfs文件系统中。
- 增加引用计数：使用 kobject\_get() 增加引用计数。
- 减少引用计数并释放：使用 kobject\_put() 减少引用计数，当引用计数降到零时，kobject 会被释放。
```c
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/module.h>
#include <linux/fs.h>
#include <linux/sysfs.h>
#include <linux/kobject.h>
#include <linux/err.h>

volatile int test_value = 0;
struct kobject *kobj_01;
struct kobject *kobj_02;

/* sysfs 文件读操作 */ 
static ssize_t sysfs_show(struct kobject *kobj, struct kobj_attribute *attr, char *buf)
{
    pr_info("读sysfs!\n");
    return sprintf(buf, "test_value = %d\n", test_value);
}

/* sysfs 文件写操作 */
static ssize_t sysfs_store(struct kobject *kobj, struct kobj_attribute *attr, const char *buf, size_t count)
{
    pr_info("写sysfs!\n");
    sscanf(buf, "%d", &test_value);
    return count;
}

/* 定义 sysfs 属性 */
struct kobj_attribute sysfs_test_attr = __ATTR(test_value, 0664, sysfs_show, sysfs_store);

/* 模块初始化函数 */
static int __init sysfs_test_driver_init(void)
{
    /* 创建并添加一个 kobject */
    kobj_01 = kobject_create_and_add("kobj_01", kernel_kobj); // 改为kernel_kobj
    if (!kobj_01) {
        pr_err("创建 kobject01 失败.....\n");
        return -ENOMEM;
    }

    kobj_02 = kobject_create_and_add("kobj_02", kobj_01);
    if (!kobj_02) {
        pr_err("创建 kobject02 失败.....\n");
        kobject_put(kobj_01); // 确保释放 kobj_01
        return -ENOMEM;
    }

    /* 在 kobj_02 目录下创建一个文件 */
    if (sysfs_create_file(kobj_02, &sysfs_test_attr.attr)) {
        pr_err("创建 sysfs 文件失败.....\n");
        kobject_put(kobj_02);
        kobject_put(kobj_01);
        return -1;
    }

    pr_info("驱动模块初始化完成!\n");
    return 0;
}
module_init(sysfs_test_driver_init);

/* 模块退出函数 */
static void __exit sysfs_test_driver_exit(void)
{
    sysfs_remove_file(kobj_02, &sysfs_test_attr.attr); // 移除 sysfs 文件
    kobject_put(kobj_02); // 确保按顺序释放 kobj_02
    kobject_put(kobj_01);
    pr_info("设备驱动模块移除!\n");
}
module_exit(sysfs_test_driver_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Y.YX");
123456789101112131415161718192021222324252627282930313233343536373839404142434445464748495051525354555657585960616263646566676869707172
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/daec93d1177d48bfbdb6e2260a9220cd.png#pic_center)

**免责声明：本内容部分参考野火科技及其他相关公开资料，若有侵权或者勘误请联系作者。**

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/139882450

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