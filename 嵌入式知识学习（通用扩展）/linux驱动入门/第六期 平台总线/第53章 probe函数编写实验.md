---
title: "RK3568驱动指南｜第六篇-平台总线-第53章 probe函数编写实验_驱动 probe函数参数-CSDN博客"
source: "https://blog.csdn.net/BeiJingXunWei/article/details/133824251"
author:
  - "[[成就一亿技术人!]]"
  - "[[hope_wisdom 发出的红包]]"
published:
created: 2025-09-14
description: "文章浏览阅读450次。在上面的两个章节中分别注册了platform设备和platform驱动，匹配成功之后会进入在注册platform驱动程序中编写的probe函数，在上个章节只是为了验证是否匹配成功，所以只是在probe中加入了一句相关打印，而驱动是要控制硬件的，但是平台总线模型对硬件的描述写在了platform_device.c中,platform设备和platform驱动匹配成功之后，那我们如何在驱动platform_driver.c的probe函数中，得到platform_device.c中编写的硬件资源呢。_驱动 probe函数参数"
tags:
  - "clippings"
---

# 备注(声明)：


# 参考文章：




# 一、 probe函数编写实验

## 获取device资源
### 1 、直接访问 platform_device 结构体的资源数组
> struct platform_driver 结构体继承了 struct device_driver 结构体，因此可以直接访问 struct device_driver 中定义的成员。实例代码如下所示：

```c
  if (pdev->num_resources >= 2) {
        struct resource *res_mem = &pdev->resource[0];
        struct resource *res_irq = &pdev->resource[1];
 
        // 使用获取到的硬件资源进行处理
        printk("Method 1: Memory Resource: start = 0x%lld, end = 0x%lld\n",
                res_mem->start, res_mem->end);
        printk("Method 1: IRQ Resource: number = %lld\n", res_irq->start);
    }
```


> 在这种方法中，直接访问platform_device结构体的资源数组来获取硬件资源。pdev->resource是一个资源数组，其中存储了设备的硬件资源信息。通过访问数组的不同索引，可以获取到特定的资源。
> 
> 在这个示例中，假设资源数组的第一个元素是内存资源，第二个元素是中断资源。所以我们将第一个元素的指针赋值给res_mem，第二个元素的指针赋值给res_irq。
> 


### 2 、使用 platform_get_resource() 获取硬件资源（💌）

- 1 声明位于<linux/platform_device.h>头文件中, 获取设备的资源信息

```c
函数原型：

struct resource *platform_get_resource(struct platform_device *pdev,                                       unsigned int type, unsigned int num);

参数说明：

pdev：指向要获取资源的平台设备（platform_device）结构体的指针。

type：指定资源的类型，可以是以下值之一：

IORESOURCE_MEM：表示内存资源。

IORESOURCE_IO：表示I/O资源。

IORESOURCE_IRQ：表示中断资源。

其他资源类型的宏定义可在<linux/ioport.h>和<linux/irq.h>头文件中找到。

num：指定要获取的资源的索引。在一个设备中可能存在多个相同类型的资源，通过索引可以选择获取特定的资源。

返回值：

如果成功获取资源，则返回指向资源（struct resource）的指针。

如果获取资源失败，或者指定的资源不存在，则返回NULL。
```

- 2 从平台设备的资源数组中获取指定类型和索引的资源
> 每个元素都是一个struct resource结构体，描述了一个资源的信息，如起始地址、结束地址、中断号等。


#### 示例用法：
```c
struct platform_device *pdev;
struct resource *res;
 
res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
if (!res) {
    // 处理获取内存资源失败的情况
}
 
// 使用获取到的内存资源进行处理
unsigned long start = res->start;
unsigned long end = res->end;
...
```

> 在上述示例中，首先通过platform_get_resource()函数获取平台设备的第一个内存资源（索引为0）。如果获取资源失败（返回NULL），则可以根据实际情况进行错误处理。如果获取资源成功，则可以使用返回的资源指针来访问资源的信息，如起始地址和结束地址。
> 
> 通过platform_get_resource()函数，可以方便地在驱动程序中获取平台设备的资源信息，并根据这些信息进行后续的操作和配置。



### 3 、



### 4 、

## 实验程序的编写
> 本实验对应的网盘路径为：iTOP-RK3568开发板【底板V1.7版本】\03_【iTOP-RK3568开发板】指南教程\02_Linux驱动配套资料\04_Linux驱动例程\42_probe。

### 5、添加第一小节两种获取设备资源的方式并打印出来


### 6、编写完成的probe.c代码如下
```c
#include <linux/module.h>
#include <linux/platform_device.h>
#include <linux/ioport.h>
 
static int my_platform_driver_probe(struct platform_device *pdev)
{
    struct resource *res_mem, *res_irq;
 
    // 方法1：直接访问 platform_device 结构体的资源数组
    if (pdev->num_resources >= 2) {
        struct resource *res_mem = &pdev->resource[0];
        struct resource *res_irq = &pdev->resource[1];
 
        // 使用获取到的硬件资源进行处理
        printk("Method 1: Memory Resource: start = 0x%llx, end = 0x%llx\n",
                res_mem->start, res_mem->end);
        printk("Method 1: IRQ Resource: number = %lld\n", res_irq->start);
    }
 
    // 方法2：使用 platform_get_resource() 获取硬件资源
    res_mem = platform_get_resource(pdev, IORESOURCE_MEM, 0);
    if (!res_mem) {
        dev_err(&pdev->dev, "Failed to get memory resource\n");
        return -ENODEV;
    }
 
    res_irq = platform_get_resource(pdev, IORESOURCE_IRQ, 0);
    if (!res_irq) {
        dev_err(&pdev->dev, "Failed to get IRQ resource\n");
        return -ENODEV;
    }
 
    // 使用获取到的硬件资源进行处理
    printk("Method 2: Memory Resource: start = 0x%llx, end = 0x%llx\n",
            res_mem->start, res_mem->end);
    printk("Method 2: IRQ Resource: number = %lld\n", res_irq->start);
 
    return 0;
}
 
static int my_platform_driver_remove(struct platform_device *pdev)
{
    // 设备移除操作
    return 0;
}
 
static struct platform_driver my_platform_driver = {
    .driver = {
        .name = "my_platform_device", // 与 platform_device.c 中的设备名称匹配
        .owner = THIS_MODULE,
    },
    .probe = my_platform_driver_probe,
    .remove = my_platform_driver_remove,
};
 
static int __init my_platform_driver_init(void)
{
    int ret;
 
    ret = platform_driver_register(&my_platform_driver); // 注册平台驱动
    if (ret) {
        printk("Failed to register platform driver\n");
        return ret;
    }
 
    printk("Platform driver registered\n");
    return 0;
}
 
static void __exit my_platform_driver_exit(void)
{
    platform_driver_unregister(&my_platform_driver); // 注销平台驱动
    printk("Platform driver unregistered\n");
}
 
module_init(my_platform_driver_init);
module_exit(my_platform_driver_exit);
 
MODULE_LICENSE("GPL");
MODULE_AUTHOR("topeet");
```

### 7、关键代码：（💌）
```c

static int my_platform_driver_probe(struct platform_device *pdev)：：

    struct resource *res_mem, *res_irq;
 
    // 方法1：直接访问 platform_device 结构体的资源数组
    if (pdev->num_resources >= 2) {
        struct resource *res_mem = &pdev->resource[0];
        struct resource *res_irq = &pdev->resource[1];
    }
 
    // 方法2：使用 platform_get_resource() 获取硬件资源
    res_mem = platform_get_resource(pdev, IORESOURCE_MEM, 0);
    res_irq = platform_get_resource(pdev, IORESOURCE_IRQ, 0);


```

### 8、



## 运行测试
### 1 、驱动来源
> 本小节的测试要使用两个ko文件，第一个ko文件为第53章编译出来的platform_device.ko驱动，第二个ko文件为在上一小节编译出的probe.ko驱动文件。

### 2 、platform设备的注册
![嵌入式知识学习（通用扩展）/linux驱动入门/第六期 平台总线/assets/第53章 probe函数编写实验/file-20251212121011409.png](assets/第53章%20probe函数编写实验/file-20251212121011409.png)

### 3 、加载probe.ko驱动（💌）
![嵌入式知识学习（通用扩展）/linux驱动入门/第六期 平台总线/assets/第53章 probe函数编写实验/file-20251212121034852.png](assets/第53章%20probe函数编写实验/file-20251212121034852.png)

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




# 二、

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


