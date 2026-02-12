---
title: "RK3568驱动指南｜第六篇-平台总线-第52章 注册platform驱动实验_平台驱动注册-CSDN博客"
source: "https://blog.csdn.net/BeiJingXunWei/article/details/133793491"
author:
  - "[[成就一亿技术人!]]"
  - "[[hope_wisdom 发出的红包]]"
published:
created: 2025-09-14
description: "文章浏览阅读529次。本文详细介绍了瑞芯微RK3568芯片的特性，包括其处理器、图形处理器、接口支持和AI功能。重点讲解了如何在Linux内核中注册platform驱动，涉及platform_driver_register函数、platform_device_unregister函数以及platform_driver结构体的使用，展示了开发平台驱动的基本流程和实验示例。"
tags:
  - "clippings"
---

# 备注(声明)：


# 参考文章：
[RK3568驱动指南｜第六篇-平台总线-第52章 注册platform驱动实验\_平台驱动注册-CSDN博客](https://blog.csdn.net/BeiJingXunWei/article/details/133793491)



# 一、注册platform驱动

## platform_driver_register 函数
### 1 、在 Linux 内核中注册一个平台驱动程序


### 2 、函数定义：（💌）
- 1 内核源码目录下的“/include/linux/platform_device.h”文件中
```c
#define platform_driver_register(drv) \
	__platform_driver_register(drv, THIS_MODULE)
extern int __platform_driver_register(struct platform_driver *,					struct module *);
```

> 这个宏用于简化平台驱动程序的注册过程。它将实际的注册函数 `__platform_driver_register` 与当前模块（驱动程序）关联起来。宏的参数 drv 是一个指向 struct platform_driver 结构体的指针，描述了要注册的平台驱动程序的属性和回调函数。**THIS_MODULE 是一个宏，用于获取当前模块的指针**。
> 


> 函数原型：
> 
> int platform_driver_register(struct platform_driver * driver);
> 
> 头文件：
> 
> #include <linux/platform_device.h>
> 
> 函数作用：
> 
> platform_driver_register 函数用于将一个平台驱动程序注册到内核中。通过注册平台驱动程序，内核可以识别并与特定的平台设备进行匹配，并在需要时调用相应的回调函数。
> 
> 参数含义：
> 
> driver：指向 struct platform_driver 结构体的指针，描述了要注册的平台驱动程序的属性和回调函数（会在下面的小节对该结构体进行详细的讲解）。
> 
> 返回值：
> 
> 返回一个整数值，表示函数的执行状态。**如果注册成功，返回 0**；如果注册失败，返回一个负数错误码。



### 3 、`__platform_driver_register`函数
- 1 定义在“/drivers/base/platform.c”文件中
```c
int __platform_driver_register(struct platform_driver *drv, struct module *owner)
{
    drv->driver.owner = owner;                   // 将平台驱动程序的所有权设置为当前模块
    drv->driver.bus = &platform_bus_type;    // 将平台驱动程序的总线类型设置为平台总线
    drv->driver.probe = platform_drv_probe;      // 设置平台驱动程序的探测函数
    drv->driver.remove = platform_drv_remove;    // 设置平台驱动程序的移除函数
    drv->driver.shutdown = platform_drv_shutdown;// 设置平台驱动程序的关机函数
 
    return driver_register(&drv->driver);        // 将平台驱动程序注册到内核
}
```

> 第3行：将指向当前模块的指针 owner 赋值给平台驱动程序的 owner 成员。这样做是为了将当前模块与平台驱动程序关联起来，以确保模块的生命周期和驱动程序的注册和注销相关联。
> 
> 第4行：将指向平台总线类型的指针 &platform_bus_type 赋值给平台驱动程序的 bus 成员。这样做是为了指定该驱动程序所属的总线类型为平台总线，以便内核能够将平台设备与正确的驱动程序进行匹配。
> 
> 第5行：将指向平台驱动程序探测函数 platform_drv_probe 的指针赋值给平台驱动程序的 probe 成员。这样做是为了指定当内核发现与驱动程序匹配的平台设备时，要调用的驱动程序探测函数。
> 
> 第6行：将指向平台驱动程序移除函数 platform_drv_remove 的指针赋值给平台驱动程序的 remove 成员。这样做是为了指定当内核需要从系统中移除与驱动程序匹配的平台设备时，要调用的驱动程序移除函数。
> 
> 第7行 = platform_drv_shutdown;：将指向平台驱动程序关机函数 platform_drv_shutdown 的指针赋值给平台驱动程序的 shutdown 成员。这样做是为了指定当系统关机时，要调用的驱动程序关机函数。
> 
> 第9行：调用 driver_register 函数，将平台驱动程序的 driver 成员注册到内核中。该函数负责将驱动程序注册到相应的总线上，并在注册成功时返回 0，注册失败时返回一个负数错误码。
> 
> 通过这些操作，`__platform_driver_register `函数**将平台驱动程序与内核关联起来**，并**确保内核能够正确识别和调用驱动程序的各种回调函数，以实现与平台设备的交互和管理**。函数的返回值表示注册过程的执行状态，以便在需要时进行错误处理。



### 4 、

## platform_device_unregister 函数

### 5、取消注册已经注册的平台设备，即从内核中移除设备


### 6、函数定义
- 1 在内核源码目录下的“/include/linux/platform_device.h”文件中
```c
extern void platform_driver_unregister(struct platform_driver *);
```

> 函数原型：
> 
> void platform_device_unregister(struct platform_device * pdev);
> 
> 头文件：
> 
> #include <linux/platform_device.h>
> 
> 函数作用：
> platform_device_unregister 函数用于从内核中注销平台设备。通过调用该函数，可以将指定的平台设备从系统中移除。
> 
> 参数含义：
> 
> pdev：指向要注销的平台设备的指针。
> 
> 返回值：
> 无返回值。



### 7、函数实际定义：
- 1 实际定义在“/drivers/base/platform.c”文件中
```c
void platform_driver_unregister(struct platform_driver *drv)
{
	driver_unregister(&drv->driver);
}
```


- 1 追踪之后找到定义在“/drivers/base/driver.c”目录下的driver_unregister函数
```c
void driver_unregister(struct device_driver *drv)
{
    // 检查传入的设备驱动程序指针和 p 成员是否有效
    if (!drv || !drv->p) {
        WARN(1, "Unexpected driver unregister!\n");
        return;
    }
 
    driver_remove_groups(drv, drv->groups); // 移除与设备驱动程序关联的属性组
    bus_remove_driver(drv);    // 从总线中移除设备驱动程序
}
```

> 函数内部有三个主要的操作：
> 
> 第4-7行：检查传入的设备驱动程序指针 drv 是否为空，或者驱动程序的 p 成员是否为空。如果其中任何一个条件为真，表示**传入的参数无效，会发出警告并返回**。
> 
> 第9行：调用 driver_remove_groups 函数，用于**从内核中移除与设备驱动程序关联的属性组**。drv->groups 是指向属性组的指针，指定了要移除的属性组列表。
> 
> 第10行：调用 bus_remove_driver 函数，用于从总线中移除设备驱动程序。该函数会执行以下操作：
> 
> （1）从总线驱动程序列表中移除指定的设备驱动程序。
> 
> （2）调用与设备驱动程序关联的 remove 回调函数（如果有定义）。
> 
> （3）释放设备驱动程序所占用的资源和内存。
> 
> （4）最终销毁设备驱动程序的数据结构。
> 
> 通过调用 driver_unregister 函数，可以正确地注销设备驱动程序，并在注销过程中进行必要的清理工作。这样可以避免资源泄漏和其他问题。在调用该函数后，应避免继续使用已注销的设备驱动程序指针，因为该驱动程序已不再存在于内核中。






### 8、



## platform_driver结构体
### 1 、与平台设备驱动相关的函数和数据成员


### 2 、结构体定义：（💌）
- 1 内核的“/include/linux/platform_device.h”文件中
```c
struct platform_driver {
	int (*probe)(struct platform_device *); /* 平台设备的探测函数指针 */
	int (*remove)(struct platform_device *); /* 平台设备的移除函数指针 */
	void (*shutdown)(struct platform_device *);/* 平台设备的关闭函数指针 */
	int (*suspend)(struct platform_device *, pm_message_t state);/* 平台设备的挂起函数指针 */
	int (*resume)(struct platform_device *);/* 平台设备的恢复函数指针 */
	struct device_driver driver;/* 设备驱动程序的通用数据 */
	const struct platform_device_id *id_table;/* 平台设备与驱动程序的关联关系表 */
	bool prevent_deferred_probe; /* 是否阻止延迟探测 */
};
```

> probe：平台设备的探测函数指针。当系统检测到一个平台设备与该驱动程序匹配时，该函数将被调用以初始化和配置设备。
> 
> remove：平台设备的移除函数指针。当平台设备从系统中移除时，该函数将被调用以执行清理和释放资源的操作。
> 
>` shutdown`：平台设备的关闭函数指针。**当系统关闭时，该函数将被调用以执行与平台设备相关的关闭操作**。
> 
> suspend：平台设备的挂起函数指针。当系统进入挂起状态时，该函数将被调用以执行与平台设备相关的挂起操作。
> 
> resume：平台设备的恢复函数指针。当系统从挂起状态恢复时，该函数将被调用以执行与平台设备相关的恢复操作。
> 
> driver：包含了与设备驱动程序相关的通用数据，它是 struct device_driver 类型的实例。其中包括驱动程序的名称、总线类型、模块拥有者、属性组数组指针等信息，该结构体的name参数需要与上个章节的platform_device的.name参数相同才能匹配成功，从而进入probe函数。
> 
> id_table：指向 struct platform_device_id 结构体数组的指针，用于匹配平台设备和驱动程序之间的关联关系。通过该关联关系，可以确定哪个平台设备与该驱动程序匹配，和.driver.name起到相同的作用，但是优先级高于.driver.name。
> 
> prevent_deferred_probe：一个布尔值，用于确定是否阻止延迟探测。如果设置为 true，则延迟探测将被禁用。





### 3 、注意：
> 使用 struct platform_driver 结构体，开发人员可以定义平台设备驱动程序，并将其注册到内核中。当系统检测到与该驱动程序匹配的平台设备时，内核将调用相应的函数来执行设备的初始化、配置、操作和管理。驱动程序可以利用提供的函数指针和通用数据与平台设备进行交互，并提供必要的功能和服务。

> 需要注意的是，struct platform_driver 结构体继承了 struct device_driver 结构体，因此**可以直接访问 struct device_driver 中定义的成员**。这使得平台驱动程序可以利用**通用的驱动程序机制**，并与其他类型的设备驱动程序共享代码和功能。

### 4 、


### 5、





# 二、实验

> 本实验对应的网盘路径为：iTOP-RK3568开发板【底板V1.7版本】\03_【iTOP-RK3568开发板】指南教程\02_Linux驱动配套资料\04_Linux驱动例程\41。


## platform驱动的一个大体框架
### 1 、platform_driver.c代码如下（💌）
```c
#include <linux/module.h>
#include <linux/platform_device.h>
 
// 平台设备的探测函数
static int my_platform_probe(struct platform_device *pdev)
{
    printk(KERN_INFO "my_platform_probe: Probing platform device\n");
 
    // 添加设备特定的操作
    // ...
 
    return 0;
}
 
// 平台设备的移除函数
static int my_platform_remove(struct platform_device *pdev)
{
    printk(KERN_INFO "my_platform_remove: Removing platform device\n");
 
    // 清理设备特定的操作
    // ...
 
    return 0;
}
 
// 定义平台驱动结构体
static struct platform_driver my_platform_driver = {
    .probe = my_platform_probe,
    .remove = my_platform_remove,
    .driver = {
        .name = "my_platform_device",
        .owner = THIS_MODULE,
    },
};
 
// 模块初始化函数
static int __init my_platform_driver_init(void)
{
    int ret;
 
    // 注册平台驱动
    ret = platform_driver_register(&my_platform_driver);
    if (ret) {
        printk(KERN_ERR "Failed to register platform driver\n");
        return ret;
    }
 
    printk(KERN_INFO "my_platform_driver: Platform driver initialized\n");
 
    return 0;
}
 
// 模块退出函数
static void __exit my_platform_driver_exit(void)
{
    // 注销平台驱动
    platform_driver_unregister(&my_platform_driver);
 
    printk(KERN_INFO "my_platform_driver: Platform driver exited\n");
}
 
module_init(my_platform_driver_init);
module_exit(my_platform_driver_exit);
 
MODULE_LICENSE("GPL");
MODULE_AUTHOR("topeet");
```

### 2 、


### 3 、




## 运行测试
### 1 、驱动模块的加载
![嵌入式知识学习（通用扩展）/linux驱动入门/第六期 平台总线/assets/第52章 注册platform驱动实验/file-20251212104159108.png](assets/第52章%20注册platform驱动实验/file-20251212104159108.png)



### 2 、查看创建的my_platform_driver驱动文件夹（💌）

- 1 /sys/bus/plateform/drivers
![嵌入式知识学习（通用扩展）/linux驱动入门/第六期 平台总线/assets/第52章 注册platform驱动实验/file-20251212104241755.png](assets/第52章%20注册platform驱动实验/file-20251212104241755.png)



### 3 、加载注册platform设备ko文件
![嵌入式知识学习（通用扩展）/linux驱动入门/第六期 平台总线/assets/第52章 注册platform驱动实验/file-20251212104321672.png](assets/第52章%20注册platform驱动实验/file-20251212104321672.png)


> 进入probe函数，显示出了相应的打印（加载上述两个ko文件不分先后顺序）。




### 4 、




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


