---
title: "RK3568驱动指南｜第九篇 设备模型-第111章 platform总线注册驱动流程实例分析实验"
source: "https://blog.csdn.net/BeiJingXunWei/article/details/135415376"
author:
  - "[[BeiJingXunWei]]"
published: 2024-01-06
created: 2025-09-14
description: "文章浏览阅读1.1k次，点赞22次，收藏24次。此行将指定的platform_drv_remove函数赋值给drv->driver.remove，表示驱动程序的移除函数。1 首先，将传递给驱动程序的设备指针 _dev 转换为 platform_driver 结构体指针 drv，将传递给驱动程序的设备指针 _dev 转换为 platform_device 结构体指针 dev。此行将指定的platform_drv_probe函数赋值给drv->driver.probe，表示驱动程序的探测函数。这个函数会根据设备的电源管理需求，将设备与相应的电源域进行关联。_platform总线设备驱动模型"
tags:
  - "clippings"
---


# 备注(声明)：


# 参考文章：




# 一、platform总线注册驱动流程实例分析实验

## platform_driver_register函数跟踪(1 --->)
### 1 、platform_driver_register函数实现如下
```c
#define platform_driver_register(drv) \
	__platform_driver_register(drv, THIS_MODULE)
```

### 2 、`__platform_driver_register函数`(2<---)
```c
int __platform_driver_register(struct platform_driver *drv,
				struct module *owner)
{
	drv->driver.owner = owner;
	drv->driver.bus = &platform_bus_type;
	drv->driver.probe = platform_drv_probe;
	drv->driver.remove = platform_drv_remove;
	drv->driver.shutdown = platform_drv_shutdown;
 
	return driver_register(&drv->driver);
}
```

#### 完成平台驱动程序的注册，并将其与平台总线类型进行关联。(❤️)

> 1. drv->driver.owner = owner; 此行将指定的owner参数赋值给drv->driver.owner，表示驱动程序的所有者模块。
> 
> 2. `drv->driver.bus = &platform_bus_type;`此行将指向平台总线类型的指针&platform_bus_type赋值给drv->driver.bus，**将驱动程序与平台总线进行关联。**
> 
> 3. drv->driver.probe = platform_drv_probe;此行将指定的platform_drv_probe函数赋值给drv->driver.probe，表示驱动程序的探测函数。
> 
> 4. `drv->driver.remove = platform_drv_remove;`此行**将指定的platform_drv_remove函数赋值给drv->driver.remove，表示驱动程序的移除函数。**
> 
> 5. drv->driver.shutdown = platform_drv_shutdown;此行将指定的platform_drv_shutdown函数赋值给drv->driver.shutdown，表示驱动程序的关机函数。
> 
> 6. return driver_register(&drv->driver);此行`调用driver_register函数`，将驱动程序的struct driver结构体作为参数进行注册。driver_register函数会**将驱动程序添加到内核的驱动程序列表中，并进行相应的初始化。**
> 


#### driver_register函数在之前的章节已经学习过了

### 3 、




## 看看platform总线的probe函数是如何执行的

### 4 、platform_drv_probe函数(3<---)

```c
static int platform_drv_probe(struct device *_dev)
{
	// 将传递给驱动程序的设备指针转换为 platform_driver 结构体指针
	struct platform_driver *drv = to_platform_driver(_dev->driver);
	// 将传递给驱动程序的设备指针转换为 platform_device 结构体指针
	struct platform_device *dev = to_platform_device(_dev);
	int ret;
 
	// 设置设备节点的默认时钟属性
	ret = of_clk_set_defaults(_dev->of_node, false);
	if (ret < 0)
		return ret;
 
	// 将设备附加到电源域
	ret = dev_pm_domain_attach(_dev, true);
	if (ret)
		goto out;
 
	// 调用驱动程序的探测函数（probe）
	if (drv->probe) {
		ret = drv->probe(dev);
		if (ret)
			dev_pm_domain_detach(_dev, true);
	}
 
out:
	// 处理探测延迟和错误情况
	if (drv->prevent_deferred_probe && ret == -EPROBE_DEFER) {
		dev_warn(_dev, "probe deferral not supported\n");
		ret = -ENXIO;
	}
 
	return ret;
}
```


### 5、调用驱动程序的 probe 函数(❤️)
- 2 并处理探测延迟和错误情况。

> 1 首先，将传递给驱动程序的设备指针` _dev` 转换为 platform_driver 结构体指针 drv，将传递给驱动程序的设备指针 `_dev` 转换为 platform_device 结构体指针 dev。
> 
> 2  使用 of_clk_set_defaults() 函数设置设备节点的默认时钟属性。这个函数会根据设备节点的属性信息配置设备的时钟。
> 
> 3 调用 dev_pm_domain_attach() 将设备附加到电源域。这个函数会根据设备的电源管理需求，将设备与相应的电源域进行关联。
> 
> 4` 如果驱动程序的 probe 函数存在`，**调用它来执行设备的探测操作**。drv->probe(dev) 表示调用驱动程序的 probe 函数，并传递 platform_device 结构体指针 dev 作为参数。如果探测失败，会调用 dev_pm_domain_detach() 分离设备的电源域。
> 
> 5 处理探测延迟和错误情况。如果驱动程序设置了 prevent_deferred_probe 标志，并且返回值为 -EPROBE_DEFER，则表示探测被延迟。在这种情况下如果驱动程序设置了 prevent_deferred_probe 标志，并且返回值为 -EPROBE_DEFER，则表示探测被延迟。在这种情况下，代码会打印一个警告信息 probe deferral not supported，并将返回值设置为 -ENXIO，表示设备不存在。





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


