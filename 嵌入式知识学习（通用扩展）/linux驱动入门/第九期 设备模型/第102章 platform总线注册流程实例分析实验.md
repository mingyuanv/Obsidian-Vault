---
title: "RK3568驱动指南｜第九篇 设备模型-第102章 platform总线注册流程实例分析实验"
source: "https://blog.csdn.net/BeiJingXunWei/article/details/135384934"
author:
  - "[[BeiJingXunWei]]"
published: 2024-01-04
created: 2025-09-14
description: "文章浏览阅读904次，点赞17次，收藏19次。然后使用调用device_register(platform_bus_type) 注册平台总线设备，将platform_bus结构体注册到设备子系统中。然后使用bus_register(&platform_bus_type)函数注册平台总线类型，将 platform_bus_type 结构体注册到总线子系统中。如果匹配成功，则返回匹配（非零）。如果存在，则调用platform_match_id(pdrv->id_table, pdev)函数来检查设备是否与ID表中的任何条目匹配。_平台总线注册"
tags:
  - "clippings"
---


# 备注(声明)：
> **进一步分析 platform 总线的注册流程**。本章节将深入研究 platform 总线注册的关键步骤。**揭示 platform 总线注册的内部机制。**

# 参考文章：




# 一、platform总线注册流程分析

## 从内核初始化出发
### 1 、内核在初始化的过程中，调用流程如下(❤️)
![[嵌入式知识学习（通用扩展）/linux驱动入门/第九期 设备模型/assets/第102章 platform总线注册流程实例分析实验/file-20260312104222988.png]]

### 2 、



## 分析platform_bus_init函数。
### 3 、内核driver/base/platform.c文件中注册了platform文件



### 4 、platform_bus_init函数如下(❤️)

> 函数首先清空总线early_platform_device_list上的所有节点。然后使用调用`device_register(platform_bus_type) `**注册平台总线设备**，将platform_bus结构体注册到设备子系统中。然后使用`bus_register(&platform_bus_type)`函数**注册平台总线类 型**，将 platform_bus_type 结构体注册到总线子系统中。



```c
int __init platform_bus_init(void)
{
	int error;
 
	early_platform_cleanup();  // 提前清理平台总线相关资源
 
	error = device_register(&platform_bus);  // 注册平台总线设备
	if (error) {
		put_device(&platform_bus);  // 注册失败，释放平台总线设备
		return error;  // 返回错误代码
	}
 
	error = bus_register(&platform_bus_type);  // 注册平台总线类型
	if (error) {
		device_unregister(&platform_bus);  // 注册失败，注销平台总线设备
		return error;  // 返回错误代码
	}
 
	of_platform_register_reconfig_notifier();  // 注册平台重新配置的通知器
 
	return error;  // 返回错误代码（如果有）
}
```


## platform_bus_type结构体如下
```c
struct bus_type platform_bus_type = {
	.name		= "platform",
	.dev_groups	= platform_dev_groups,
	.match		= platform_match,
	.uevent		= platform_uevent,
	.dma_configure	= platform_dma_configure,
	.pm		= &platform_dev_pm_ops,
};
```

### 6、表示平台总线类型。


### 7、成员解析
> .name = "platform"：指定平台总线类型的名称为"platform"。
> .dev_groups = platform_dev_groups：指定设备组的指针，用于定义与平台总线相关的设备属性组。
>` .match = platform_match：`**指定匹配函数的指针，用于确定设备是否与平台总线兼容。**
> .uevent = platform_uevent：指定事件处理函数的指针，用于处理与平台总线相关的事件。
> .dma_configure = platform_dma_configure：指定DMA配置函数的指针，用于配置平台总线上的DMA。
> .pm = &platform_dev_pm_ops：指定与电源管理相关的操作函数的指针，用于管理平台总线上的设备电源。


### 8、重点来看看platform_match函数

> platform_match是一个用于**判断设备和驱动程序是否匹配的函数**。它接受两个参数：dev表示设备对象指针，drv表示驱动程序对象指针。上述函数的主要逻辑如下：
> 
> 1首先，将dev和drv分别转换为struct platform_device和struct platform_driver类型的指针，以便后续使用。
> 
> 2 检查`pdev->driver_override是否设置`。如果**设置了，表示只要与指定的驱动程序名称匹配，即可认为设备和驱动程序匹配**。函数会比较pdev->driver_override和drv->name的字符串是否相等，如果相等则返回匹配（非零）。
> 
> 3 如果pdev->driver_override未设置，首先尝试进行`OF风格的匹配`（Open Firmware）。调用`of_driver_match_device(dev, drv)函数`，该函数会**检查设备是否与驱动程序匹配**。如果匹配成功，则返回匹配（非零）。
> 
> 4 如果OF风格的匹配失败，接下来尝试进行`ACPI风格的匹配`（Advanced Configuration and Power Interface）。调用`acpi_driver_match_device(dev, drv)函数`，该函数会**检查设备是否与驱动程序匹配**。如果匹配成功，则返回匹配（非零）。
> 
> 5 如果ACPI风格的匹配也失败，最后尝试`根据驱动程序的ID表进行匹配`。**检查pdrv->id_table是否存在**。如果存在，则调用platform_match_id(pdrv->id_table, pdev)函数来检查设备是否与ID表中的任何条目匹配。如果匹配成功，则返回匹配（非零）。
> 
> 6如果以上所有匹配尝试都失败，**最后使用驱动程序名称与设备名称进行比较**。比较pdev->name和drv->name的字符串是否相等，如果相等则返回匹配（非零）。


```c
static int platform_match(struct device *dev, struct device_driver *drv)
{
	struct platform_device *pdev = to_platform_device(dev);
	struct platform_driver *pdrv = to_platform_driver(drv);
 
	/* When driver_override is set, only bind to the matching driver */
	if (pdev->driver_override)
		return !strcmp(pdev->driver_override, drv->name);
 
	/* Attempt an OF style match first */
	if (of_driver_match_device(dev, drv))
		return 1;
 
	/* Then try ACPI style match */
	if (acpi_driver_match_device(dev, drv))
		return 1;
 
	/* Then try to match against the id table */
	if (pdrv->id_table)
		return platform_match_id(pdrv->id_table, pdev) != NULL;
 
	/* fall-back to driver name match */
	return (strcmp(pdev->name, drv->name) == 0);
}
```


#### 得知 platform总线匹配优先级(❤️)
- 1 of_match_table>id_table>name。




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


