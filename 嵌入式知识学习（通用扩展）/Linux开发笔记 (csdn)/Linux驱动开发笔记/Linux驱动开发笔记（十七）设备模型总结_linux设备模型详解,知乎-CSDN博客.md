---
title: "Linux驱动开发笔记（十七）设备模型总结_linux设备模型详解,知乎-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/140327038?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读1.9k次，点赞47次，收藏28次。本文是对设备模型的一次总结，笔者回顾最近的笔记时发现一直缺少这部分内容，这期是对前面内容的查漏补缺。kobject是Linux内核中用于管理内核对象的基础组件,它提供了引用计数、层次结构、sysfs集成和uevent支持等功能，帮助开发者更好地管理和操作内核对象。我们可以将kobject结构体类比为一个组织中的员工记录系统，每个员工记录包含员工的基本信息、职位信息、部门信息以及一些管理功能。在设备模型中，kobject起到了核心作用，使得设备和驱动的管理变得更加系统化和灵活。_linux设备模型详解,知乎"
tags:
  - "clippings"
---
---

## 前言

本文是对设备 模型 的一次总结，笔者回顾最近的笔记时发现一直缺少这部分内容，这期是对前面内容的查漏补缺。

## 一、设备模型

### 1.1 设备模型的引入

  相信大家通过这么长时间学习已经发现了 Linux 的驱动和 [MCU](https://so.csdn.net/so/search?q=MCU&spm=1001.2101.3001.7020) 的编程最大的不同就是其强大的兼容性，例如不同型号的stm32，他们的程序不一定可以兼容；但是对于Linux的驱动来说，无论是常见的6u还是我们的rk3568几乎不需要进行过大的改动。设备模型的引入是为了提供一种统一和系统化的方式来管理和表示Linux系统中的 硬件 设备，主要用于解决以下几个问题：

- 设备管理复杂化：早期的Linux设备管理主要通过字符设备和块设备来进行管理，每种设备都有各自的管理方式，导致代码复杂且不易维护。
- 统一接口：不同类型的设备（如PCI、USB、I2C等）之间缺乏统一的管理接口，开发者需要针对不同的设备类型编写不同的代码。
- 热插拔支持：随着热插拔设备的普及，需要一种动态管理设备的机制，能够在设备插入和移除时自动进行处理。
- 设备层次结构：需要一种层次结构来表示设备之间的依赖关系和连接方式，方便系统管理和驱动开发。

### 1.2 设备模型的主要组成部分

  设备模型通过以下几个主要组件来实现对系统中硬件设备的管理，这部分在sysfs文件系统中我们讲述过：

- 设备 (device)：表示系统中的一个具体硬件设备。每个设备在系统中都有一个唯一的标识符，并且包含设备的各种属性信息。
- 总线 (bus)：表示设备之间的连接方式，例如PCI总线、USB总线等。总线负责管理连接在其上的设备，并处理设备的枚举和驱动绑定，如果没有总线会虚拟出一个platform总线。
- 驱动 (driver)：表示控制和管理具体设备的驱动程序。驱动程序负责与设备进行通信，并提供设备的操作接口。
- 类 (class)：表示设备的功能类型。例如，所有网络设备都属于网络设备类，所有块设备都属于块设备类。类提供了一种抽象层次，使得相同类型的设备可以通过统一的接口进行操作。

## 二、kobject详解

### 2.1 到底什么是kobject

  kobject是Linux内核中用于管理内核对象的基础组件,它提供了引用计数、层次结构、sysfs集成和uevent支持等功能，帮助开发者更好地管理和操作内核对象。我们可以将kobject结构体类比为一个组织中的员工记录系统，每个员工记录包含员工的基本信息、职位信息、部门信息以及一些管理功能。在设备模型中，kobject起到了核心作用，使得设备和驱动的管理变得更加系统化和灵活。

- 引用计数：kobject通过引用计数机制来管理对象的生命周期。当对象的引用计数为0时，表示对象不再被使用，可以安全地释放。
- 层次结构：kobject支持父子层次结构，允许内核对象之间建立层次关系。这在表示设备拓扑结构时特别有用，例如表示一个PCI总线上的多个设备。
- sysfs支持：kobject提供与sysfs的集成，允许将内核对象的信息导出到用户空间。每个kobject可以在sysfs中创建一个目录，包含对象的属性文件。
- uevent支持：kobject可以发送用户空间事件（uevent），通知用户空间有关对象的创建、删除和状态变化。这在设备热插拔和动态管理中非常重要。

  但在实际的使用中，我们一般都将它嵌套在一个数据结构中，例如：cdev、platform\_device等，这样就可以把高级设备对象接入到设备模型中。此外，我们也可以把总线、设备、驱动看作是kobject的派生类，一个kobject对应产生/sys目录下的一个子目录,以iic2为例。  
![请添加图片描述](https://i-blog.csdnimg.cn/direct/5a087f5d60a840e2a1848b49f834678a.png#pic_center)

```bash
//iic2进行设备、驱动程序和总线注册后，/sys产生的相应子文件结构
/sys
├── bus
│   ├── i2c
│   │   ├── devices
│   │   │   └── iic2
│   │   │       ├── driver -> ../../../../bus/i2c/drivers/i2c_driver_name
│   │   │       └── ···
│   │   └── ···
├── class
│   └── i2c-adapter
│       ├── ···
│       └── i2c-2 -> ../../devices/platform/iic2
├── devices
│   ├── platform
│   │   └── iic2
│   └── ···
└── kernel
123456789101112131415161718
```

### 2.2 kobject的实现流程

  前面我们已经知道了当创建注册kobject之后会自动在/sys下创建一个子目录，那么kobject和sys是怎么连接起来的呢？

1. kobject 的创建、初始化及添加：创建一个 kobject 的通常使用 kobject\_create\_and\_add 函数，该函数会创建一个 kobject，并将其添加到父对象（如果有的话）中。
2. 在 sysfs 中创建文件：kobject 与 sysfs 集成，使用 sysfs\_create\_file 函数在 sysfs 中为 kobject 创建文件。
3. kobject 的引用计数：kobject 使用引用计数管理其生命周期，kobject\_get 和 kobject\_put 函数用于增加和减少 kobject 的引用计数。
4. kobject 的释放：kobject 的释放通过 kobject\_release 函数完成，该函数会调用 kobj\_type 结构体中定义的释放函数：

  在创建kobject的时候有以下四种可能性：

1. 无父目录，无kset，在sysfs的根目录下创建文件（/sys）
2. 无父目录，有kset，在kset下创建目录，并把kobj加入到kset.list
3. 有父目录，无kset，在parent下创建目录
4. 有父目录，有kset，在parent下创建目录，并把kobj加入到kset.list

### 2.3 kset的使用方法

  在sysfs一章的学习中，我们简单介绍了kset，这部分我们讲述一下它的使用方法。

1. 定义 kset 结构
2. 创建 kset：使用 kset\_create\_and\_add 函数创建并初始化一个 kset，并将其添加到指定的父 kobject 中。
3. 注销和释放 kset：kset\_unregister 函数用于将 kset 从系统中移除，并释放其占用的资源。
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
struct kset *example_kset;

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
    int retval;

    /* 创建并添加一个 kset */
    example_kset = kset_create_and_add("example_kset", NULL, kernel_kobj);
    if (!example_kset) {
        pr_err("创建 kset 失败.....\n");
        return -ENOMEM;
    }

    /* 创建并添加一个 kobject，挂载到 kset */
    kobj_01 = kobject_create_and_add("kobj_01", &example_kset->kobj);
    if (!kobj_01) {
        pr_err("创建 kobject01 失败.....\n");
        kset_unregister(example_kset);
        return -ENOMEM;
    }

    kobj_02 = kobject_create_and_add("kobj_02",  &example_kset->kobj);
    if (!kobj_02) {
        pr_err("创建 kobject02 失败.....\n");
        kobject_put(kobj_01);
        kset_unregister(example_kset);
        return -ENOMEM;
    }

    /* 在 kobj_02 目录下创建一个文件 */
    retval = sysfs_create_file(kobj_02, &sysfs_test_attr.attr);
    if (retval) {
        pr_err("创建 sysfs 文件失败.....\n");
        kobject_put(kobj_02);
        kobject_put(kobj_01);
        kset_unregister(example_kset);
        return retval;
    }

    pr_info("驱动模块初始化完成!\n");
    return 0;
}

/* 模块退出函数 */
static void __exit sysfs_test_driver_exit(void)
{
    sysfs_remove_file(kobj_02, &sysfs_test_attr.attr);
    kobject_put(kobj_02);
    kobject_put(kobj_01);
    kset_unregister(example_kset);
    pr_info("设备驱动模块移除!\n");
}

module_init(sysfs_test_driver_init);
module_exit(sysfs_test_driver_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Y.YX");
12345678910111213141516171819202122232425262728293031323334353637383940414243444546474849505152535455565758596061626364656667686970717273747576777879808182838485868788
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/10e3597e8ac3432c870736c25953fea4.png#pic_center)

### 2.4 kobj\_type

  kobj\_type是 Linux 内核中用于描述 kobject 类型的结构体。它定义了 kobject 的属性和操作，包括引用计数的管理、sysfs 文件的创建和删除等。kobj\_type 结构体通常与 kobject 结合使用，帮助开发者更好地管理内核对象及其生命周期。kobj\_type 的定义如下：

```c
struct kobj_type {
    void (*release)(struct kobject *kobj);
    const struct sysfs_ops *sysfs_ops;
    struct attribute **default_attrs;
};
12345
```
- release：当 kobject 的引用计数减为零时调用的释放函数。
- sysfs\_ops：指向一个 sysfs\_ops 结构体的指针，定义了读写 sysfs 文件的操作。
- default\_attrs：指向一个 attribute 指针数组，定义了默认的 sysfs 属性。  
	**注：当我们在使用kobject\_creat\_and\_init函数是会自动进行内存申请和ktype的实现，所以不需要手动实现这一部分，这里仅简单参考。**

## 三、kref详解

### 2.1 kref的引入

  在前面的学习中我们知道在创建字符设备的时候，系统会自动在/sys的相关子目录下创建一个设备节点，这个节点容许我们对设备进行操作。但是当我需要注销断开链接的时候，系统是什么时候释放资源的？这里其实是有一个计数器的概念——kref。  
  kref 是 Linux 内核的一种引用计数机制，用于管理内存中的 对象生命周期 。它帮助确保对象在没有被引用时被释放，从而避免内存泄漏或使用已经释放的内存。kref 主要在内核开发中使用，尤其是在需要共享或传递对象的情况下。我们一般定义初始化为1，每引用一次+1，取消一次-1，如果引用计数减少到 0，则调用 release 函数来释放对象。  
  kref 结构体的基本结构如下，其一般都是嵌套在其他结构体之中的，例如kobject。

```c
struct kref {
    atomic_t refcount;
};
123
```

### 2.2 相关函数

- 初始化 kref
```c
//该函数将 kref 的引用计数初始化为 1
void kref_init(struct kref *kref);
12
```
- 增加引用计数
```c
//该函数增加 kref 的引用计数
void kref_get(struct kref *kref);
12
```
- 释放引用计数
```c
//该函数减少 kref 的引用计数。
void kref_put(struct kref *kref, void (*release)(struct kref *kref));
12
```

#### 2.3 实验示例

  在下面示例中，kref\_init 初始化引用计数为 1。每当我们获取对 my\_struct 的引用时，调用 kref\_get 增加引用计数；每当我们释放对 my\_struct 的引用时，调用 kref\_put 减少引用计数。如果引用计数减少到 0，kref\_put 将调用 my\_struct\_release 来释放对象。

```c
struct my_struct {
    struct kref refcount;
        ...
};

void my_struct_release(struct kref *ref) {
    struct my_struct *obj = container_of(ref, struct my_struct, refcount);
    // 释放其他资源
    kfree(obj);
}

void create_my_struct(void) {
    struct my_struct *obj = kmalloc(sizeof(*obj), GFP_KERNEL);
    kref_init(&obj->refcount);
    // 初始化其他字段
}

void get_my_struct(struct my_struct *obj) {
    kref_get(&obj->refcount);
}

void put_my_struct(struct my_struct *obj) {
    kref_put(&obj->refcount, my_struct_release);
}
123456789101112131415161718192021222324
```

**注：这个例子只是方便大家理解，实际上由于kref是内嵌到其他结构体上的，所以对应计数的操作不需要我们手动进行。**

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/140327038

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