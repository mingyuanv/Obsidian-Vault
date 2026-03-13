---
title: "RK3568驱动指南｜第九篇 设备模型-第105章 platform总线设备注册流程实例分析实验"
source: "https://blog.csdn.net/BeiJingXunWei/article/details/135387116"
author:
  - "[[BeiJingXunWei]]"
published: 2024-01-04
created: 2025-09-14
description: "文章浏览阅读1k次，点赞23次，收藏22次。RK3568 支持安卓 11 和 linux 系统，主要面向物联网网关、NVR 存储、工控平板、工业检测、工控盒、卡拉 OK、云终端、车载中控等行业。在平台设备驱动中，我们使用platform_device_register函数注册平台总线设备。在上个章节中，我们详细分析了设备是如何注册到总线上的过程，在本章节中，我们将进一步探讨platform设备是如何注册到platform总线上的。【粉丝群】824412014（加群获取驱动文档+例程）到此，platform总线设备注册流程分析完毕。_platform总线注册"
tags:
  - "clippings"
---

# 备注(声明)：探讨platform设备是如何注册到platform总线上的


# 参考文章：



# 一、platform总线设备注册流程实例分析实验

## platform_device_register函数
### 1 、注册平台总线设备。


### 2 、函数实现如下
```c
int platform_device_register(struct platform_device *pdev)
{
	device_initialize(&pdev->dev);
	arch_setup_pdev_archdata(pdev);
	return platform_device_add(pdev);
}
```

- 1 重点来看platform_device_add函数


### 3 、platform_device_add函数实现如下
```c
int platform_device_add(struct platform_device *pdev)
{
	u32 i;
	int ret;
 
	// 检查输入的平台设备指针是否为空
	if (!pdev)
		return -EINVAL;
 
	// 如果平台设备的父设备为空，将父设备设置为 platform_bus
	if (!pdev->dev.parent)
		pdev->dev.parent = &platform_bus;
 
	// 将平台设备的总线设置为 platform_bus_type
	pdev->dev.bus = &platform_bus_type;
 
	// 根据平台设备的 id 进行不同的处理
	switch (pdev->id) {
	default:
		// 根据设备名和 id 设置设备的名字
		dev_set_name(&pdev->dev, "%s.%d", pdev->name, pdev->id);
		break;
	case PLATFORM_DEVID_NONE:
		// 如果 id 为 PLATFORM_DEVID_NONE，则只使用设备名作为设备的名字
		dev_set_name(&pdev->dev, "%s", pdev->name);
		break;
	case PLATFORM_DEVID_AUTO:
		/*
		 * 自动分配的设备 ID。将其标记为自动分配的，以便我们记住它需要释放，
		 * 并且为了避免与显式 ID 的命名空间冲突，我们附加一个后缀。
		 */
		ret = ida_simple_get(&platform_devid_ida, 0, 0, GFP_KERNEL);
		if (ret < 0)
			goto err_out;
		pdev->id = ret;
		pdev->id_auto = true;
		dev_set_name(&pdev->dev, "%s.%d.auto", pdev->name, pdev->id);
		break;
	}
 
	// 遍历平台设备的资源列表，处理每个资源
	for (i = 0; i < pdev->num_resources; i++) {
		struct resource *p, *r = &pdev->resource[i];
 
		// 如果资源的名称为空，则将资源的名称设置为设备的名字
		if (r->name == NULL)
			r->name = dev_name(&pdev->dev);
 
		p = r->parent;
		if (!p) {
			// 如果资源没有指定父资源，则根据资源类型设置默认的父资源
			if (resource_type(r) == IORESOURCE_MEM)
				p = &iomem_resource;
			else if (resource_type(r) == IORESOURCE_IO)
				p = &ioport_resource;
		}
 
		// 如果父资源存在，并且将资源插入到父资源中失败，则返回错误
		if (p && insert_resource(p, r)) {
			dev_err(&pdev->dev, "failed to claim resource %d: %pR\n", i, r);
			ret = -EBUSY;
			goto failed;
		}
	}
 
	// 打印调试信息，注册平台设备
	pr_debug("Registering platform device '%s'. Parent at %s\n",
		 dev_name(&pdev->dev), dev_name(pdev->dev.parent));
 
	// 添加设备到设备层级中，注册设备
	ret = device_add(&pdev->dev);
	if (ret == 0)
		return ret;
 
failed:
	// 如果设备 ID 是自动分配的，需要移除已分配的 ID
	if (pdev->id_auto) {
		ida_simple_remove(&platform_devid_ida, pdev->id);
		pdev->id = PLATFORM_DEVID_AUTO;
	}
 
	// 在失败的情况下，释放已插入的资源
	while (i--) {
		struct resource *r = &pdev->resource[i];
		if (r->parent)
			release_resource(r);
	}
 
err_out:
	// 返回错误码
	return ret;
}
```

#### 向平台总线中添加平台设备


#### 函数的执行过程及注释：(❤️)
> 第6~8行代码中，检查传入的平台设备指针是否为空，如果为空则返回无效参数错误码。
> 第11行代码中，如果平台设备的`父设备为空`，则**将父设备设置为 platform_bus**。将平台设备的总线设置为 platform_bus_type。

> 第17行~39行代码中，根据平台设备的ID进行不同的处理：默认情况下，根据设备名称和ID设置设备的名称。如果`ID为PLATFORM_DEVID_NONE`，则**只使用设备名称作为设备的名称**。如果`ID为PLATFORM_DEVID_AUTO`，则**自动分配设备ID**。使用ida_simple_get函数获取一个可用的ID，并将设备ID标记为自动分配。**设备名称将附加一个后缀以避免与显式ID的命名空间冲突**。

> 第42行~64行代码中，遍历平台设备的资源列表，`处理每个资源`。如果资源的名称为空，则将资源的名称设置为设备的名称。如果资源没有指定父资源，则根据资源类型设置默认的父资源。如果父资源存在，并且将资源插入到父资源中失败，则返回忙碌错误码。
>     在Linux操作系统中，为了方便管理设备资源，**所有设备资源都会添加到资源树中。每个设备资      源都会有一个父资源，用于表示该设备资源所属的资源的根。**

> 第67行代码，打印调试信息，注册平台设备。
> 第71行代码，`调用device_add函数`**将设备添加到设备层级结构中进行设备注册**。如果注册成功，则返回0。
> 


#### 设置设备的名字，名字有三种格式：(❤️)
![[嵌入式知识学习（通用扩展）/linux驱动入门/第九期 设备模型/assets/第105章 platform总线设备注册流程实例分析实验/file-20260312144600468.png]]

![[嵌入式知识学习（通用扩展）/linux驱动入门/第九期 设备模型/assets/第105章 platform总线设备注册流程实例分析实验/file-20260312144624056.png]]



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


