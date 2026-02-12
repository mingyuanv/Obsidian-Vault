---
title: "RK3568驱动指南｜第六期-平台总线-第51章 注册platform设备实验_mali device driver loaded-CSDN博客"
source: "https://blog.csdn.net/BeiJingXunWei/article/details/133773402"
author:
  - "[[成就一亿技术人!]]"
  - "[[hope_wisdom 发出的红包]]"
published:
created: 2025-09-14
description: "文章浏览阅读614次。瑞芯微RK3568芯片是一款定位中高端的通用型SOC，采用22nm制程工艺，搭载一颗四核Cortex-A55处理器和Mali G52 2EE 图形处理器。RK3568 支持4K 解码和 1080P 编码，支持SATA/PCIE/USB3.0 外围接口。RK3568内置独立NPU，可用于轻量级人工智能应用。RK3568 支持安卓 11 和 linux 系统，主要面向物联网网关、NVR 存储、工控平板、工业检测、工控盒、卡拉 OK、云终端、车载中控等行业。​【公众号】迅为电子。_mali device driver loaded"
tags:
  - "clippings"
---

# 备注(声明)：


# 参考文章：
[RK3568驱动指南｜第六期-平台总线-第51章 注册platform设备实验\_platform设备注册-CSDN博客](https://blog.csdn.net/BeiJingXunWei/article/details/133773402)



# 一、注册platform设备

## platform_device_register 函数
### 1 、将platform_device结构体描述的平台设备注册到内核中


### 2 、函数定义：(💌)
```c
函数原型：

int platform_device_register(struct platform_device *pdev);

头文件：

#include <linux/platform_device.h>

函数作用：
platform_device_register函数用于将platform_device结构体描述的平台设备注册到内核中，使其能够参与设备的资源分配和驱动的匹配。

参数含义：

pdev：指向platform_device结构体的指针，描述要注册的平台设备的信息。

返回值：

成功：返回0，表示设备注册成功。

失败：返回负数，表示设备注册失败，返回的负数值表示错误代码。
```

- 1 在内核源码目录下的“/include/linux/platform_device.h”文件中声明
```c
extern int platform_device_register(struct platform_device *);
```



### 3 、函数解析
- 1 实际定义在“/drivers/base/platform.c”文件中
```c
int platform_device_register(struct platform_device *pdev)
{
	device_initialize(&pdev->dev);
	arch_setup_pdev_archdata(pdev);
	return platform_device_add(pdev);
}
```

> 第3行：调用了device_initialize函数，用于**对pdev->dev进行初始化**。pdev->dev是struct platform_device结构体中的一个成员，它表示平台设备对应的struct device结构体。通过调用device_initialize函数，对pdev->dev进行一些基本的初始化工作，例如设置设备的引用计数、设备的类型等。
> 
> 第4行：调用了arch_setup_pdev_archdata函数，用于根据平台设备的架构数据来**设置pdev的架构相关数据**。这个函数的具体实现可能与具体的架构相关，它主要用于在不同的架构下对平台设备进行特定的设置。
> 
> 第5行：调用了platform_device_add函数，**将平台设备pdev添加到内核中**。platform_device_add函数会完成平台设备的添加操作，包括将设备添加到设备层级结构中、添加设备的资源等。它会返回一个int类型的结果，表示设备添加的结果。
> 
> platform_device_register函数的主要作用是**将platform_device结构体描述的平台设备注册到内核中**，包括设备的初始化、添加到platform总线和设备层级结构、添加设备资源等操作。通过该函数，平台设备被注册后，就能够参与设备的资源分配和驱动的匹配过程。函数的返回值可以用于判断设备注册是否成功。




### 4 、

##  platform_device_unregister 函数


### 5、取消注册已经注册的平台设备，即从内核中移除设备


### 6、详细介绍：
- 1 在内核源码目录下的“/include/linux/platform_device.h”文件中
```c
extern int platform_device_unregister(struct platform_device *);
```

```c
函数原型：

void platform_device_unregister(struct platform_device *pdev);

头文件：

#include <linux/platform_device.h>

函数作用：
platform_device_unregister函数用于取消注册已经注册的平台设备，从内核中移除设备。

参数含义：

pdev：指向要取消注册的平台设备的platform_device结构体指针。

返回值：
无返回值。
```



### 7、函数解析
- 1 实际定义在“/drivers/base/platform.c”文件中

```c
void platform_device_unregister(struct platform_device *pdev)
{
	platform_device_del(pdev);
	platform_device_put(pdev);
}
```

> 第3行：调用了platform_device_del函数，用于**将设备从platform总线的设备列表中移除**。它会将设备从设备层级结构中移除，停止设备的资源分配和驱动的匹配。
> 
> 第4行：这一步调用了platform_device_put函数，用于**减少对设备的引用计数**。这个函数会检查设备的引用计数，如果引用计数减为零，则会释放设备结构体和相关资源。通过减少引用计数，可以确保设备在不再被使用时能够被释放。
> 
> platform_device_unregister函数的作用是**取消注册已经注册的平台设备，从内核中移除设备**。它先调用platform_device_del函数将设备从设备层级结构中移除，然后调用platform_device_put函数减少设备的引用计数，确保设备在不再被使用时能够被释放。


### 8、



##  platform_device结构体
### 1 、描述平台设备的数据结构


### 2 、包含了平台设备的各种属性和信息，用于在内核中表示和管理平台设备


### 3 、结构体定义：(💌)
- 1 在内核的“/include/linux/platform_device.h”文件中
```c
struct platform_device {
	const char *name;  // 设备的名称，用于唯一标识设备
	int	id;        // 设备的ID，可以用于区分同一种设备的不同实例
	bool	 id_auto;  // 表示设备的ID是否自动生成
	struct device dev;  // 表示平台设备对应的 struct device 结构体，用于设备的基本管理和操作
	u32	num_resources;   // 设备资源的数量
	struct resource	*resource;   // 指向设备资源的指针
 
	const struct platform_device_id *id_entry; // 指向设备的ID表项的指针，用于匹配设备和驱动
	char *driver_override; // 强制设备与指定驱动匹配的驱动名称
 
	/* MFD cell pointer */
	struct mfd_cell *mfd_cell;   // 指向多功能设备（MFD）单元的指针，用于多功能设备的描述
 
	/* arch specific additions */
	struct pdev_archdata	archdata;    // 用于存储特定于架构的设备数据
};
```

- 1 下面对于几个重要的参数和结构体进行讲解

>` const char *name`：**设备的名称**，用于唯一标识设备。必须提供一个唯一的名称，以便内核能够正确识别和管理该设备。
> 
> `int id`：设备的ID，可以**用于区分同一种设备的不同实例**。这个参数是可选的，如果不需要使用ID进行区分，可以将其设置为-1，
> 
> struct device` dev`：表示平台设备**对应的struct device结构体**，用于设备的基本管理和操作。必须为该参数提供一个有效的struct device对象，该结构体的release方法必须要实现，否则在编译的时候会报错。
> 
> u32 `num_resources`：设备**资源的数量**。如果设备具有资源（如内存区域、中断等），则需要提供资源的数量。
> 
> `struct resource *resource`：**指向设备资源的指针**。如果设备具有资源，需要提供一个指向资源数组的指针，会在下个小节对该结构体进行详细的讲解。

### 4 、

## resource结构体
### 5、描述系统中的设备资源，包括内存区域、I/O 端口、中断等


### 6、结构体定义: (💌)
- 1 在内核的“/include/linux/ioport.h”文件中
```c
struct resource {
    resource_size_t start;          /* 资源的起始地址 */
    resource_size_t end;            /* 资源的结束地址 */
    const char *name;               /* 资源的名称 */
    unsigned long flags;            /* 资源的标志位 */
    unsigned long desc;             /* 资源的描述信息 */
    struct resource *parent;        /* 指向父资源的指针 */
    struct resource *sibling;       /* 指向同级兄弟资源的指针 */
    struct resource *child;         /* 指向子资源的指针 */
 
    /* 以下宏定义用于保留未使用的字段 */
    ANDROID_KABI_RESERVE(1);
    ANDROID_KABI_RESERVE(2);
    ANDROID_KABI_RESERVE(3);
    ANDROID_KABI_RESERVE(4);
};
```



### 7、参数介绍(💌)
> （1）resource_size_t start：资源的起始地址。它表示资源的起始位置或者起始寄存器的地址。
> 
> （2）resource_size_t end：资源的结束地址。它表示资源的结束位置或者结束寄存器的地址。
> 
> （3）const char `*name`：资源的名称。它是一个字符串，用于标识和描述资源。
> 
> （4）unsigned long f`lags`：资源的标志位。它包含了一些特定的标志，用于表示资源的属性或者特征。例如，可以用标志位来指示资源的可用性、共享性、缓存属性等。flags参数的具体取值和含义可以根据系统和驱动的需求进行定义和解释，但通常情况下，它用于**表示资源的属性、特征或配置选项**。下面是一些常见的标志位及其可能的含义：
> 

####  资源类型相关标志位：
```c
IORESOURCE_IO：表示资源是I/O端口资源。
IORESOURCE_MEM：表示资源是内存资源。
IORESOURCE_REG：表示资源是寄存器偏移量。
IORESOURCE_IRQ：表示资源是中断资源。
IORESOURCE_DMA：表示资源是DMA（直接内存访问）资源。
```

####  资源属性和特征相关标志位：
```c
IORESOURCE_PREFETCH：表示资源是无副作用的预取资源。
IORESOURCE_READONLY：表示资源是只读的。
IORESOURCE_CACHEABLE：表示资源支持缓存。
IORESOURCE_RANGELENGTH：表示资源的范围长度。
IORESOURCE_SHADOWABLE：表示资源可以被影子资源替代。
IORESOURCE_SIZEALIGN：表示资源的大小表示对齐。
IORESOURCE_STARTALIGN：表示起始字段是对齐的。
IORESOURCE_MEM_64：表示资源是64位内存资源。
IORESOURCE_WINDOW：表示资源由桥接器转发。
IORESOURCE_MUXED：表示资源是软件复用的。
IORESOURCE_SYSRAM：表示资源是系统RAM（修饰符）。
```

#### 其他状态和控制标志位
```c
IORESOURCE_EXCLUSIVE：表示用户空间无法映射此资源。
IORESOURCE_DISABLED：表示资源当前被禁用。
IORESOURCE_UNSET：表示尚未分配地址给资源。
IORESOURCE_AUTO：表示地址由系统自动分配。
IORESOURCE_BUSY：表示驱动程序将此资源标记为繁忙。
```




### 8、



# 二、实验
> 本实验对应的网盘路径为：iTOP-RK3568开发板【底板V1.7版本】\03_【iTOP-RK3568开发板】指南教程\02_Linux驱动配套资料\04_Linux驱动例程\40_platform_device\。



## 实验程序的编写
### 1 、实验介绍
> 本实验将注册一个名为 "my_platform_device" 的平台设备，当注册平台设备时，该驱动程序提供了两个资源：**一个内存资源和一个中断资源**。这些资源被定义在名为 my_resources 的结构体数组中,具体内容如下：
> 
> 内存资源：
> 
> 起始地址：MEM_START_ADDR（0xFDD60000）
> 
> 结束地址：MEM_END_ADDR（0xFDD60004）
> 
> 标记：IORESOURCE_MEM
> 
> 中断资源：
> 
> 中断资源号：IRQ_NUMBER（101）
> 
> 标记：IORESOURCE_IRQ

### 2 、platform_device.c代码如下
```c
#include <linux/module.h>
#include <linux/platform_device.h>
#include <linux/ioport.h>
 
#define MEM_START_ADDR 0xFDD60000
#define MEM_END_ADDR   0xFDD60004
#define IRQ_NUMBER     101
 
static struct resource my_resources[] = {
    {
        .start = MEM_START_ADDR,    // 内存资源起始地址
        .end = MEM_END_ADDR,        // 内存资源结束地址
        .flags = IORESOURCE_MEM,    // 标记为内存资源
    },
    {
        .start = IRQ_NUMBER,        // 中断资源号
        .end = IRQ_NUMBER,          // 中断资源号
        .flags = IORESOURCE_IRQ,    // 标记为中断资源
    },
};
 
static void my_platform_device_release(struct device *dev)
{
    // 释放资源的回调函数
}
 
static struct platform_device my_platform_device = {
    .name = "my_platform_device",                  // 设备名称
    .id = -1,                                      // 设备ID
    .num_resources = ARRAY_SIZE(my_resources),     // 资源数量
    .resource = my_resources,                      // 资源数组
    .dev.release = my_platform_device_release,     // 释放资源的回调函数
};
 
static int __init my_platform_device_init(void)
{
    int ret;
 
    ret = platform_device_register(&my_platform_device);   // 注册平台设备
    if (ret) {
        printk(KERN_ERR "Failed to register platform device\n");
        return ret;
    }
 
    printk(KERN_INFO "Platform device registered\n");
    return 0;
}
 
static void __exit my_platform_device_exit(void)
{
    platform_device_unregister(&my_platform_device);   // 注销平台设备
    printk(KERN_INFO "Platform device unregistered\n");
}
 
module_init(my_platform_device_init);
module_exit(my_platform_device_exit);
 
MODULE_LICENSE("GPL");
MODULE_AUTHOR("topeet");
```

### 3 、关键代码(💌)
```c
#define MEM_START_ADDR 0xFDD60000
#define MEM_END_ADDR   0xFDD60004
#define IRQ_NUMBER     101
 
static struct resource my_resources[] = {
    {
        .start = MEM_START_ADDR,    // 内存资源起始地址
        .end = MEM_END_ADDR,        // 内存资源结束地址
        .flags = IORESOURCE_MEM,    // 标记为内存资源
    },
    {
        .start = IRQ_NUMBER,        // 中断资源号
        .end = IRQ_NUMBER,          // 中断资源号
        .flags = IORESOURCE_IRQ,    // 标记为中断资源
    },
};

static struct platform_device my_platform_device = {
    .name = "my_platform_device",                  // 设备名称
    .id = -1,                                      // 设备ID
    .num_resources = ARRAY_SIZE(my_resources),     // 资源数量
    .resource = my_resources,                      // 资源数组
    .dev.release = my_platform_device_release,     // 释放资源的回调函数
};


static int __init my_platform_device_init(void)：：

    ret = platform_device_register(&my_platform_device);   // 注册平台设备



static void __exit my_platform_device_exit(void)：：

    platform_device_unregister(&my_platform_device);   // 注销平台设备

```





### 4 、




## 运行测试
### 1 、驱动模块的加载
![嵌入式知识学习（通用扩展）/linux驱动入门/第六期 平台总线/assets/第51章 注册platform设备实验/file-20251212093535476.png](assets/第51章%20注册platform设备实验/file-20251212093535476.png)

### 2 、查看我们创建的my_platform_device设备文件夹(💌)
- 1 /sys/bus/plateform/dedvices
![嵌入式知识学习（通用扩展）/linux驱动入门/第六期 平台总线/assets/第51章 注册platform设备实验/file-20251212093601270.png](assets/第51章%20注册platform设备实验/file-20251212093601270.png)


### 3 、






## 
### 1 、


### 2 、


### 3 、



### 4 、



### 5、


### 6、


### 7、


### 8、


# 三、

## 
### 1 、


### 2 、


### 3 、



### 4 、



### 5、


### 6、


### 7、


### 8、



## 
### 1 、


### 2 、


### 3 、



### 4 、


### 5、


### 6、


### 7、


### 8、



## 
### 1 、


### 2 、


### 3 、



### 4 、



### 5、


### 6、


### 7、


### 8、


# 四、

## 
### 1 、


### 2 、


### 3 、



### 4 、



### 5、


### 6、


### 7、


### 8、



## 
### 1 、


### 2 、


### 3 、



### 4 、


### 5、


### 6、


### 7、


### 8、



## 
### 1 、


### 2 、


### 3 、



### 4 、



### 5、


### 6、


### 7、


### 8、


# 五、

## 
### 1 、


### 2 、


### 3 、



### 4 、



### 5、


### 6、


### 7、


### 8、



## 
### 1 、


### 2 、


### 3 、



### 4 、


### 5、


### 6、


### 7、


### 8、



## 
### 1 、


### 2 、


### 3 、



### 4 、



### 5、


### 6、


### 7、


### 8、


