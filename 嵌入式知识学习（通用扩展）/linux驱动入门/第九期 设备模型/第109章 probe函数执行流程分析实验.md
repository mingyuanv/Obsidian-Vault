---
title: "RK3568驱动指南｜第九篇 设备模型-第109章 probe函数执行流程分析实验"
source: "https://blog.csdn.net/BeiJingXunWei/article/details/135389470"
author:
  - "[[BeiJingXunWei]]"
published: 2024-01-04
created: 2025-09-14
description: "文章浏览阅读1.1k次，点赞21次，收藏23次。drv->bus->match(dev, drv)表示调用总线对象的 match函数，并将设备对象和驱动程序对象作为参数传递给该函数。总的来说， bus_for_each_dev() 函数主要是提供了一个遍历指定总线上的设备对象列表，并对每个设备对象进行特定操作的快捷方式，可以用于驱动程序中需要管理和操作大量设备实例的场景。这个函数的作用是遍历指定总线上的所有设备，并对每个设备执行指定的函数 fn。2. 如果 match`函数存在，则调用总线对象的 match函数，传入设备对象和驱动程序对象作为参数。_驱动函数执行流程"
tags:
  - "clippings"
---

# 备注(声明)：


# 参考文章：




# 一、probe函数执行流程分析实验

## 分析bus_add_driver 函数（1--->）
### 1 、bus_add_driver 函数实现如下

```c
int bus_add_driver(struct device_driver *drv)
{
	struct bus_type *bus;
	struct driver_private *priv;
	int error = 0;
 
	// 获取总线对象
	bus = bus_get(drv->bus);
	if (!bus)
		return -EINVAL;  // 返回无效参数错误码
 
	pr_debug("bus: '%s': add driver %s\n", bus->name, drv->name);
 
	// 分配并初始化驱动程序私有数据
	priv = kzalloc(sizeof(*priv), GFP_KERNEL);
	if (!priv) {
		error = -ENOMEM;
		goto out_put_bus;
	}
	klist_init(&priv->klist_devices, NULL, NULL);
	priv->driver = drv;
	drv->p = priv;
	priv->kobj.kset = bus->p->drivers_kset;
	// 初始化并添加驱动程序的内核对象
	error = kobject_init_and_add(&priv->kobj, &driver_ktype, NULL,
				     "%s", drv->name);
	if (error)
		goto out_unregister;
 
	// 将驱动程序添加到总线的驱动程序列表
	klist_add_tail(&priv->knode_bus, &bus->p->klist_drivers);
	// 如果总线启用了自动探测，则尝试自动探测设备
	if (drv->bus->p->drivers_autoprobe) {
		error = driver_attach(drv);
		if (error)
			goto out_unregister;
	}
	// 将驱动程序添加到模块
	module_add_driver(drv->owner, drv);
 
	// 创建驱动程序的uevent属性文件
	error = driver_create_file(drv, &driver_attr_uevent);
	if (error) {
		printk(KERN_ERR "%s: uevent attr (%s) failed\n",
			__func__, drv->name);
	}
	// 添加驱动程序的组属性
	error = driver_add_groups(drv, bus->drv_groups);
	if (error) {
		/* How the hell do we get out of this pickle? Give up */
		printk(KERN_ERR "%s: driver_create_groups(%s) failed\n",
			__func__, drv->name);
	}
 
	// 如果驱动程序不禁止绑定属性文件，则添加绑定属性文件
	if (!drv->suppress_bind_attrs) {
		error = add_bind_files(drv);
		if (error) {
			/* Ditto */
			printk(KERN_ERR "%s: add_bind_files(%s) failed\n",
				__func__, drv->name);
		}
	}
 
	return 0;  // 返回成功
 
out_unregister:
	kobject_put(&priv->kobj);
	/* drv->p is freed in driver_release()  */
	drv->p = NULL;
out_put_bus:
	bus_put(bus);
	return error;  // 返回错误码
}
```
### 2 、函数功能解析：(❤️)
> l 第31行~37行代码 自动探测设备：
> 
>` 如果总线启用了自动探测（drivers_autoprobe 标志）`，则**调用 driver_attach 函数尝试自动探测设备。**
> 
> 如果自动探测失败，则跳转到 out_unregister 进行错误处理。
> 

> **变量drivers_autoprobe也可以在用户空间通过属性文件drivers_autoprobe来控制**，再次体现属性文件的作用。
> ![[嵌入式知识学习（通用扩展）/linux驱动入门/第九期 设备模型/assets/第109章 probe函数执行流程分析实验/file-20260312161248172.png]]

>  第39行代码将驱动程序添加到模块：
> 
> 调`用 module_add_driver 函数`**将驱动程序添加到模块中。**

> l 第42行~46行代码创建驱动程序的 uevent 属性文件：
> 
> 调用 `driver_create_file 函数`**为驱动程序创建 uevent 属性文件**。如果创建失败，则打印错误消息。

> l 第48行~53行代码添加驱动程序的组属性：
> 
>` 调用 driver_add_groups `函数**将驱动程序的组属性添加到驱动程序中**。如果添加失败，则打印错误消息。

> l 第56行~63行添加绑定属性文件：
> 
> 如果驱动程序没有禁止绑定属性文件（suppress_bind_attrs 标志），则`调用 add_bind_files` 函数**添加绑定属性文件**。如果添加失败，则打印错误消息。
> 



### 3 、

## 使用driver_attach函数来探测设备

### 4 、driver_attach函数定义：（2<---）
```c
int driver_attach(struct device_driver *drv)
{
	return bus_for_each_dev(drv->bus, NULL, drv, __driver_attach);
}
EXPORT_SYMBOL_GPL(driver_attach);
```


### 5、bus_for_each_dev函数实现如下：（3<---）
```c
int bus_for_each_dev(struct bus_type *bus, struct device *start,
		     void *data, int (*fn)(struct device *, void *))
{
	struct klist_iter i;
	struct device *dev;
	int error = 0;

	// 检查总线对象是否存在
	if (!bus || !bus->p)
		return -EINVAL;  // 返回无效参数错误码

	// 初始化设备列表迭代器
	klist_iter_init_node(&bus->p->klist_devices, &i,
			     (start ? &start->p->knode_bus : NULL));

	// 遍历设备列表并执行指定的函数
	while (!error && (dev = next_device(&i)))
		error = fn(dev, data);

	// 退出设备列表迭代器
	klist_iter_exit(&i);

	return error;  // 返回执行过程中的错误码（如果有）
}
```

#### 函数的参数：
```c
bus：指定要遍历的总线对象。

start：指定开始遍历的设备对象。如果为 NULL，则从总线的第一个设备开始遍历。

data：传递给函数 fn 的额外数据。

fn：指定要执行的函数，该函数接受一个设备对象和额外数据作为参数，并返回一个整数错误码。
```


#### 函数的功能解释：(❤️)
> l 第9行代码中，首先，检查传入的总线对象是否存在以及与该总线相关的私有数据是否存在。如果总线对象或其私有数据不存在，返回 -EINVAL 表示无效的参数错误码。
> 
> l 第13行~14行代码中，接下来，**初始化设备列表迭代器，以便遍历总线上的设备**。 使用 klist_iter_init_node 函数初始化一个设备列表迭代器。传递总线对象的设备列表 klist_devices、迭代器对象 i，以及可选的起始设备的节点指针。然后，在一个循环中遍历设备列表并执行指定的函数。
> 
> l 第17行代码中`，使用 next_device 函数`**从迭代器中获取下一个设备**。**如果存在下一个设备，则调用传入的函数指针 fn**，并将当前设备和额外的数据参数传递给它。如果执行函数时出现错误，将错误码赋值给 error。
> 
> l 第21行代码中，最后，退出设备列表迭代器，释放相关资源。使用 klist_iter_exit 函数退出设备列表的迭代器。
> 
> 总的来说， bus_for_each_dev() 函数主要是提供了一个遍历指定总线上的设备对象列表，并对每个设备对象进行特定操作的快捷方式，**可以用于驱动程序中需要管理和操作大量设备实例的场景。**
> 

#### 遍历指定总线上的所有设备，并对每个设备执行指定的函数 fn(❤️)



### 6、


### 7、


### 8、



## fn要执行的函数为__driver_attach函数（4<---）
### 1 、函数实现如下
```c
static int __driver_attach(struct device *dev, void *data)
{
	struct device_driver *drv = data;  // 传入的数据参数作为设备驱动对象
	int ret;

	/*
	 * Lock device and try to bind to it. We drop the error
	 * here and always return 0, because we need to keep trying
	 * to bind to devices and some drivers will return an error
	 * simply if it didn't support the device.
	 *
	 * driver_probe_device() will spit a warning if there
	 * is an error.
	 */

	ret = driver_match_device(drv, dev);  // 尝试将驱动程序绑定到设备上
	if (ret == 0) {
		/* no match */
		return 0;  // 如果没有匹配，则返回 0
	} else if (ret == -EPROBE_DEFER) {
		dev_dbg(dev, "Device match requests probe deferral\n");
		driver_deferred_probe_add(dev);  // 请求推迟探测设备
	} else if (ret < 0) {
		dev_dbg(dev, "Bus failed to match device: %d", ret);
		return ret;  // 总线无法匹配设备，返回错误码
	} /* ret > 0 means positive match */

	if (driver_allows_async_probing(drv)) {
		/*
		 * Instead of probing the device synchronously we will
		 * probe it asynchronously to allow for more parallelism.
		 *
		 * We only take the device lock here in order to guarantee
		 * that the dev->driver and async_driver fields are protected
		 */
		dev_dbg(dev, "probing driver %s asynchronously\n", drv->name);
		device_lock(dev);  // 锁定设备以保护 dev->driver 和 async_driver 字段
		if (!dev->driver) {
			get_device(dev);
			dev->p->async_driver = drv;  // 设置设备的异步驱动程序
			async_schedule(__driver_attach_async_helper, dev);  // 异步调度驱动程序的附加处理函数
		}
		device_unlock(dev);  // 解锁设备
		return 0;
	}

	device_driver_attach(drv, dev);  // 同步探测设备并绑定驱动程序

	return 0;  // 返回 0 表示成功执行驱动程序附加操作
}
```

### 2 、driver_match_device函数：(5<---)

#### 尝试将驱动程序绑定到设备上(❤️)

> 这是一个内联函数 driver_match_device的代码片段。该函数用于**检查设备是否与驱动程序匹配**。以下是对代码的解释：
> 
> drv：指向设备驱动程序对象的指针。
> 
> dev：指向设备对象的指针。

```c
static inline int driver_match_device(struct device_driver *drv,
				      struct device *dev)
{
	return drv->bus->match ? drv->bus->match(dev, drv) : 1;
}
```

#### 函数的执行过程如下：(❤️)
> 1. 首先，检查驱动程序对象的 bus字段是否为 NULL，以及 bus字段的 match函数是否存在。驱动程序对象的 bus字段表示该驱动程序所属的总线。**match函数是总线对象中的一个函数指针，用于检查设备与驱动程序是否匹配。**
> 
> 2.` 如果 match函数存在`，则**调用总线对象的 match函数，传入设备对象和驱动程序对象作为参数。**
> 
> drv->bus->match(dev, drv)表示调用总线对象的 match函数，并将设备对象和驱动程序对象作为参数传递给该函数。dev是用于匹配的设备对象。drv是用于匹配的驱动程序对象。
> 
> 3. 如果总线对象的 match函数返回 0，则表示设备与驱动程序不匹配，函数将返回 0。返回值为 0 表示不匹配
> 
> 4. 如果总线对象的 match函数`返回非零值（大于 0）`，**则表示设备与驱动程序匹配**，函数将返回 1。返回值为 1 表示匹配。
> 
> 5. `如果总线对象的 match函数不存在（为 NULL）`，**则默认认为设备与驱动程序匹配**，函数将返回 1。
> 
> 这段代码使用了条件运算符 `? :` 来判断总线对象的 match函数是否存在，以便选择执行相应的逻辑。如果总线对象没有提供 match 函数，那么默认认为设备与驱动程序匹配，返回值为 1。



### 3 、
## 执行device_driver_attach函数（6<---）

### 4 、如果设备和驱动匹配上


### 5、函数解析如下
```c
int device_driver_attach(struct device_driver *drv, struct device *dev)
{
	int ret = 0;

	__device_driver_lock(dev, dev->parent);

	/*
	 * If device has been removed or someone has already successfully
	 * bound a driver before us just skip the driver probe call.
	 */
	if (!dev->p->dead && !dev->driver)
		ret = driver_probe_device(drv, dev);

	__device_driver_unlock(dev, dev->parent);

	return ret;
}

```

### 6、调用driver_probe_device函数（7<---）

```c
int driver_probe_device(struct device_driver *drv, struct device *dev)
{
	int ret = 0;

	// 检查设备是否已注册，如果未注册则返回错误码 -ENODEV
	if (!device_is_registered(dev))
		return -ENODEV;

	// 打印调试信息，表示设备与驱动程序匹配
	pr_debug("bus: '%s': %s: matched device %s with driver %s\n",
		 drv->bus->name, __func__, dev_name(dev), drv->name);

	// 获取设备供应商的运行时引用计数
	pm_runtime_get_suppliers(dev);

	// 如果设备有父设备，获取父设备的同步运行时引用计数
	if (dev->parent)
		pm_runtime_get_sync(dev->parent);

	// 等待设备的运行时状态达到稳定
	pm_runtime_barrier(dev);

	// 根据初始化调试标志选择调用真实的探测函数
	if (initcall_debug)
		ret = really_probe_debug(dev, drv);
	else
		ret = really_probe(dev, drv);

	// 请求设备进入空闲状态（省电模式）
	pm_request_idle(dev);

	// 如果设备有父设备，释放父设备的运行时引用计数
	if (dev->parent)
		pm_runtime_put(dev->parent);

	// 释放设备供应商的运行时引用计数
	pm_runtime_put_suppliers(dev);

	// 返回探测函数的执行结果
	return ret;
}
```


### 7、probe函数的执行，我们来分析really_probe函数。(8<---)
```c
static int really_probe(struct device *dev, struct device_driver *drv)
{
	int ret = -EPROBE_DEFER;  // 初始化返回值为延迟探测
	int local_trigger_count = atomic_read(&deferred_trigger_count);  // 获取当前延迟探测计数
	bool test_remove = IS_ENABLED(CONFIG_DEBUG_TEST_DRIVER_REMOVE) &&  // 判断是否启用了驱动移除测试
			   !drv->suppress_bind_attrs;

	if (defer_all_probes) {
		/*
		 * defer_all_probes 的值只能通过 device_defer_all_probes_enable() 设置，
		 * 而该函数会紧接着调用 wait_for_device_probe()，以避免任何竞争情况。
		 */
		dev_dbg(dev, "Driver %s 强制延迟探测\n", drv->name);
		driver_deferred_probe_add(dev);
		return ret;
	}

	ret = device_links_check_suppliers(dev);  // 检查设备的供应者链路
	if (ret == -EPROBE_DEFER)
		driver_deferred_probe_add_trigger(dev, local_trigger_count);  // 将设备添加到延迟探测触发列表
	if (ret)
		return ret;

	atomic_inc(&probe_count);  // 增加探测计数
	pr_debug("bus: '%s': %s: 正在使用设备 %s 探测驱动程序 %s\n",
		 drv->bus->name, __func__, drv->name, dev_name(dev));
	if (!list_empty(&dev->devres_head)) {
		dev_crit(dev, "探测之前存在资源\n");
		ret = -EBUSY;
		goto done;
	}

re_probe:
	dev->driver = drv;

	/* 如果使用了 pinctrl，绑定引脚 */
	ret = pinctrl_bind_pins(dev);
	if (ret)
		goto pinctrl_bind_failed;

	ret = dma_configure(dev);  // 配置 DMA
	if (ret)
		goto probe_failed;

	if (driver_sysfs_add(dev)) {  // 添加驱动的 sysfs
		printk(KERN_ERR "%s: driver_sysfs_add(%s) 失败\n",
			__func__, dev_name(dev));
		goto probe_failed;
	}

	if (dev->pm_domain && dev->pm_domain->activate) {  // 如果设备有电源管理域并且存在激活函数，激活电源管理域
		ret = dev->pm_domain->activate(dev);
		if (ret)
			goto probe_failed;
	}

	if (dev->bus->probe) {  // 如果总线有探测函数，调用总线的探测函数
		ret = dev->bus->probe(dev);
		if (ret)
			goto probe_failed;
	} else if (drv->probe) {  // 否则调用驱动的探测函数
		ret = drv->probe(dev);
		if (ret)
			goto probe_failed;
	}

	if (test_remove) {  // 如果启用了驱动移除测试
		test_remove = false;

		if (dev->bus->remove)  // 如果总线有移除函数，调用总线的移除函数
			dev->bus->remove(dev);
		else if (drv->remove)  // 否则调用驱动的移除函数
			drv->remove(dev);

		devres_release_all(dev);  // 释放设备的资源
		driver_sysfs_remove(dev);  // 移除驱动的 sysfs
		dev->driver = NULL;
		dev_set_drvdata(dev, NULL);
		if (dev->pm_domain && dev->pm_domain->dismiss)  // 如果设备有电源管理域并且存在解除函数，解除电源管理域
			dev->pm_domain->dismiss(dev);
		pm_runtime_reinit(dev);  // 重新初始化电源管理运行时

		goto re_probe;  // 重新进行探测
	}

	pinctrl_init_done(dev);  // 完成 pinctrl 的初始化

	if (dev->pm_domain && dev->pm_domain->sync)  // 如果设备有电源管理域并且存在同步函数，同步电源管理域
		dev->pm_domain->sync(dev);

	driver_bound(dev);  // 驱动绑定成功
	ret = 1;
	pr_debug("bus: '%s': %s: %s: 将设备 %s 绑定到驱动程序 %s\n",
		 drv->bus->name, __func__, dev_name(dev), drv->name);
	goto done;

probe_failed:
	if (dev->bus)
		blocking_notifier_call_chain(&dev->bus->p->bus_notifier,
					     BUS_NOTIFY_DRIVER_NOT_BOUND, dev);
pinctrl_bind_failed:
	device_links_no_driver(dev);  // 将设备与驱动解除绑定
	devres_release_all(dev);  // 释放设备的资源
	dma_deconfigure(dev);  // 取消 DMA 配置
	driver_sysfs_remove(dev);  // 移除驱动的 sysfs
	dev->driver = NULL;
	dev_set_drvdata(dev, NULL);
	if (dev->pm_domain && dev->pm_domain->dismiss)  // 如果设备有电源管理域并且存在解除函数，解除电源管理域
		dev->pm_domain->dismiss(dev);
	pm_runtime_reinit(dev);  // 重新初始化电源管理运行时
	dev_pm_set_driver_flags(dev, 0);  // 设置设备的驱动标志为0

	switch (ret) {
	case -EPROBE_DEFER:
		/* 驱动程序请求延迟探测 */
		dev_dbg(dev, "Driver %s 请求延迟探测\n", drv->name);
		driver_deferred_probe_add_trigger(dev, local_trigger_count);  // 将设备添加到延迟探测触发列表
		break;
	case -ENODEV:
	case -ENXIO:
		pr_debug("%s: 对 %s 的探测拒绝匹配 %d\n",
			 drv->name, dev_name(dev), ret);
		break;
	default:
		/* 驱动程序匹配但探测失败 */
		printk(KERN_WARNING
		       "%s: 对 %s 的探测失败，错误码 %d\n",
		       drv->name, dev_name(dev), ret);
	}
	/*
	 * 忽略 ->probe 返回的错误，以便下一个驱动程序可以尝试运行。
	 */
	ret = 0;
done:
	atomic_dec(&probe_count);  // 减少探测计数
	wake_up_all(&probe_waitqueue);  // 唤醒等待探测的进程
	return ret;
}
```

### 8、



## 总结设备和驱动匹配流程函数(❤️)
![[嵌入式知识学习（通用扩展）/linux驱动入门/第九期 设备模型/assets/第109章 probe函数执行流程分析实验/file-20260312165320513.png]]


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


