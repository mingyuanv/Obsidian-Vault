---
title: "{{title}}"
aliases: 
tags: 
description: 
source:
---

# 备注(声明)：引脚的复用关系是在什么时候被设置的？


# 参考文章：

```cardlink
url: https://blog.csdn.net/BeiJingXunWei/article/details/135553492?spm=1001.2101.3001.10796
title: "RK3568驱动指南｜第十一篇 pinctrl 子系统-第124章pinctrl_bind_pins函数_rk3568 pinctrl配置-CSDN博客"
description: "文章浏览阅读1.5k次，点赞19次，收藏22次。到这里关于pinctrl_bind_pins函数的第二阶段讲解就完成了，在该阶段大多都是关于赋值的操作并将节点加入到链表中，但分析到这里我们仍旧没有找到struct pinctrl_state *default_state和pinctrl_map结构体是在什么地方进行的绑定，所以在下个章节我们将继续分析124.2 小节中create_pinctrl函数接下来的部分。使用 devm_pinctrl_get 函数获取设备的pinctrl句柄，并将其赋值给 dev->pins->p。_rk3568 pinctrl配置"
host: blog.csdn.net
```


# 一、pinctrl_bind_pins函数分析

## dev_pin_info结构体引入
### 1 、以485控制引脚的设备树节点和对应的pinctrl设备树节点进行举例：
```c
    rk_485_ctl: rk-485-ctl {
        compatible = "topeet,rs485_ctl";
        gpios = <&gpio0 22 GPIO_ACTIVE_HIGH>;
        pinctrl-names = "default";
        pinctrl-0 = <&rk_485_gpio>;
    };
 
&pinctrl {
    rk_485{
        rk_485_gpio:rk-485-gpio {
            rockchip,pins = <3 13 RK_FUNC_GPIO &pcfg_pull_none>;
        };
    };
};
```




### 2 、pinctrl子系统已提前复用，追踪probe函数执行：
> 当上面编写的485设备树跟驱动匹配成功之后，就会进入相应驱动中的probe函数，在probe函数中就可以对设备树中描述的485使能引脚进行拉高和拉低的操作，从而控制485的接收和发送。所以可以猜测**在进入驱动的probe函数之前就已经使用pinctrl子系统对引脚进行了复用**，在前面设备模型的学习中，我们已经知道了**驱动中的probe函数是在内核源码目录下的“drivers/base/dd.c”文件中加载执行的**，然后找到`really _probe函数`中与probe函数加载相关的代码，具体内容如下所示：



#### `really _probe函数`解析：(❤️)
> 根据注释可以了解到，如果**使用了pinctrl就会调用第5行的pinctrl_bind_pins()函数进行设备引脚的绑定**，然后根据线索跳转到pinctrl_bind_pins函数，该函数定义在内核源码目录下的“drivers/base/pinctrl.c”文件中


```c
re_probe:
	dev->driver = drv;  // 将设备的驱动程序指针设置为当前驱动
 
	/* 如果使用了 pinctrl，在探测之前绑定引脚 */
	ret = pinctrl_bind_pins(dev);  // 绑定设备的引脚
	if (ret)
		goto pinctrl_bind_failed;
 
	ret = dma_configure(dev);  // 配置 DMA
	if (ret)
		goto probe_failed;
 
	if (driver_sysfs_add(dev)) {  // 添加驱动程序的 sysfs 接口
		printk(KERN_ERR "%s: driver_sysfs_add(%s) failed\n",
			__func__, dev_name(dev));
		goto probe_failed;
	}
 
	if (dev->pm_domain && dev->pm_domain->activate) {
		ret = dev->pm_domain->activate(dev);  // 激活电源管理域
		if (ret)
			goto probe_failed;
	}
 
	if (dev->bus->probe) {
		ret = dev->bus->probe(dev);  // 如果总线的探测函数存在，则调用总线的探测函数
		if (ret)
			goto probe_failed;
	} else if (drv->probe) {
		ret = drv->probe(dev);  // 否则调用驱动程序的探测函数
		if (ret)
			goto probe_failed;
	}
 
	if (test_remove) {
		test_remove = false;
 
		if (dev->bus->remove)  // 如果总线的移除函数存在，则调用总线的移除函数
			dev->bus->remove(dev);
		else if (drv->remove)  // 否则调用驱动程序的移除函数
			drv->remove(dev);
 
		devres_release_all(dev);  // 释放设备资源
		driver_sysfs_remove(dev);  // 移除驱动程序的 sysfs 接口
		dev->driver = NULL;
		dev_set_drvdata(dev, NULL);
		if (dev->pm_domain && dev->pm_domain->dismiss)
			dev->pm_domain->dismiss(dev);  // 解除电源管理域的激活状态
		pm_runtime_reinit(dev);  // 重新初始化电源管理运行时
 
		goto re_probe;  // 重新进行设备的探测
	}
 
	pinctrl_init_done(dev);  // 完成引脚控制器的初始化
 
	if (dev->pm_domain && dev->pm_domain->sync)
		dev->pm_domain->sync(dev);  // 同步电源管理域
 
	driver_bound(dev);  // 驱动程序与设备绑定成功
	ret = 1;
	pr_debug("bus: '%s': %s: bound device %s to driver %s\n",
		 drv->bus->name, __func__, dev_name(dev), drv->name);
	goto done;
 
done:
	// 执行完成后的处理逻辑
```

#### `really_probe` 函数机制：(❤️)
- 1 通用的核心机制，负责管理所有驱动程序的加载和设备的匹配过程

> 在 drivers/base/dd.c 文件中，有一个非常关键的静态函数叫做 really_probe()。
> 核心职责：当内核发现某个“驱动”和某个“设备”匹配成功（例如通过设备树中的 compatible 字符串匹配）后，**内核并不直接调用驱动代码里写的 probe 函数，而是先调用这个通用的 really_probe() 函数。**
> 执行流程：
> **绑定设备与驱动：将 device 结构和 driver 结构关联起来。**
> **调用驱动的 probe**：really_probe() 内部会通过函数指针，去调用你驱动程序代码中具体实现的那个 xxx_probe() 函数（例如 rs485_probe）。
> 错误处理：如果你的 probe 函数返回失败，really_probe() 负责清理资源并解除绑定。
> 


### 3 、pinctrl_bind_pins函数定义：
```c
int pinctrl_bind_pins(struct device *dev)
{
	int ret;
 
	// 检查设备是否重用了节点
	if (dev->of_node_reused)
		return 0;
 
	// 为设备的引脚分配内存空间
	dev->pins = devm_kzalloc(dev, sizeof(*(dev->pins)), GFP_KERNEL);
	if (!dev->pins)
		return -ENOMEM;
 
	// 获取设备的 pinctrl 句柄
	dev->pins->p = devm_pinctrl_get(dev);
	if (IS_ERR(dev->pins->p)) {
		dev_dbg(dev, "没有 pinctrl 句柄\n");
		ret = PTR_ERR(dev->pins->p);
		goto cleanup_alloc;
	}
 
	// 查找设备的默认 pinctrl 状态
	dev->pins->default_state = pinctrl_lookup_state(dev->pins->p, PINCTRL_STATE_DEFAULT);
	if (IS_ERR(dev->pins->default_state)) {
		dev_dbg(dev, "没有默认的 pinctrl 状态\n");
		ret = 0;
		goto cleanup_get;
	}
 
	// 查找设备的初始化 pinctrl 状态
	dev->pins->init_state = pinctrl_lookup_state(dev->pins->p, PINCTRL_STATE_INIT);
	if (IS_ERR(dev->pins->init_state)) {
		/* 不提供此状态是完全合法的 */
		dev_dbg(dev, "没有初始化的 pinctrl 状态\n");
 
		// 选择默认的 pinctrl 状态
		ret = pinctrl_select_state(dev->pins->p, dev->pins->default_state);
	} else {
		// 选择初始化的 pinctrl 状态
		ret = pinctrl_select_state(dev->pins->p, dev->pins->init_state);
	}
 
	if (ret) {
		dev_dbg(dev, "无法激活初始的 pinctrl 状态\n");
		goto cleanup_get;
	}
 
#ifdef CONFIG_PM
	/*
	 * 如果启用了电源管理，我们还会寻找可选的睡眠和空闲的引脚状态，其语义在
	 * <linux/pinctrl/pinctrl-state.h> 中定义
	 */
	dev->pins->sleep_state = pinctrl_lookup_state(dev->pins->p, PINCTRL_STATE_SLEEP);
	if (IS_ERR(dev->pins->sleep_state))
		/* 不提供此状态是完全合法的 */
		dev_dbg(dev, "没有睡眠的 pinctrl 状态\n");
 
	dev->pins->idle_state = pinctrl_lookup_state(dev->pins->p, PINCTRL_STATE_IDLE);
	if (IS_ERR(dev->pins->idle_state))
		/* 不提供此状态是完全合法的 */
		dev_dbg(dev, "没有空闲的 pinctrl 状态\n");
#endif
 
	return 0;
 
	/*
	 * 如果对于此设备没有找到 pinctrl 句柄或默认状态，
	 * 让我们明确释放设备中的引脚容器，因为保留它没有意义。
	 */
cleanup_get:
	devm_pinctrl_put(dev->pins->p);
cleanup_alloc:
	devm_kfree(dev, dev->pins);
	dev->pins = NULL;
 
	/* 返回延迟 */
	if (ret == -EPROBE_DEFER)
		return ret;
	/* 返回严重错误 */
	if (ret == -EINVAL)
		return ret;
	/* 我们忽略诸如 -ENOENT 的错误，表示没有 pinctrl 状态 */
 
	return 0;
}
```



### 4 、`struct device 结构体`包含 dev_pin_info 结构体(❤️)
```c
struct device {
	struct device		*parent;		// 指向父设备的指针
 
	struct device_private	*p;			// 私有数据指针
 
	struct kobject kobj;					// 内核对象，用于设备的管理
	const char		*init_name;			// 设备的初始名称
	const struct device_type *type;		// 设备类型
 
	struct mutex		mutex;				// 互斥锁，用于同步对驱动程序的调用
 
	struct bus_type	*bus;				// 设备所在的总线类型
	struct device_driver *driver;			// 分配该设备的驱动程序
	void		*platform_data;				// 平台特定的数据，设备核心不会修改它
	void		*driver_data;				// 驱动程序的数据，使用 dev_set/get_drvdata 来设置和获取
	....
#ifdef CONFIG_GENERIC_MSI_IRQ_DOMAIN
	struct irq_domain	*msi_domain;		// 设备的通用 MSI IRQ 域
#endif
#ifdef CONFIG_PINCTRL
	struct dev_pin_info	*pins;			// 设备的引脚信息
#endif
......
```

> 在第21-23行有这样一个恒定义，如果定义了CONFIG_PINCTRL那记录设备引脚信息的结构体`struct dev_pin_info *pins`就会**被使能**，到这里本小节要讲解的重点终于出现了


### 5、struct dev_pin_info结构体定义
```c
struct dev_pin_info {
	struct pinctrl *p;  // 引脚控制器指针
	struct pinctrl_state *default_state;  // 默认状态指针
	struct pinctrl_state *init_state;  // 初始化状态指针
#ifdef CONFIG_PM
	struct pinctrl_state *sleep_state;  // 睡眠状态指针（仅在支持电源管理时可用）
	struct pinctrl_state *idle_state;  // 空闲状态指针（仅在支持电源管理时可用）
#endif
};
```

#### 结构体中的成员变量进行详细介绍：(❤️)
> （1）struct pinctrl `*p`;：引脚控制器指针。该指针指向设备所使用的引脚控制器对象，用于对设备的引脚进行控制和配置。
> 
> （2）struct pinctrl_state `*default_state`;：默认状态指针。该指针指向设备的默认引脚配置状态，表示设备在**正常操作时的引脚配置。**
> 
> （3）struct pinctrl_state `*init_state`;：初始化 状态指针。该指针指向设备的初始化引脚配置状态，表示设备在初始化阶段的引脚配置。
> 
> （4）struct pinctrl_state `*sleep_state`;：睡眠状态指针（仅在支持电源管理时可用）。该指针指向设备的引脚配置状态，表示设备在进入睡眠状态时的引脚配置。
> 
> （5）struct pinctrl_state `*idle_state`;：空闲状态指针（仅在支持电源管理时可用）。该指针指向设备的引脚配置状态，表示设备在空闲状态时的引脚配置。

### 6、仍旧以485的控制引脚进行举例
```c
    rk_485_ctl: rk-485-ctl {
        compatible = "topeet,rs485_ctl";
        gpios = <&gpio0 22 GPIO_ACTIVE_HIGH>;
        pinctrl-names = "default";
        pinctrl-0 = <&rk_485_gpio>;
    };
 
&pinctrl {
    rk_485{
        rk_485_gpio:rk-485-gpio {
            rockchip,pins = <3 13 RK_FUNC_GPIO &pcfg_pull_none>;
        };
    };
};
```

> 其中第4行的**pinctrl-names属性指定了设备所使用的引脚控制器为default**，即第5行的pinctrl-0，而 pinctrl-0的值为pinctrl节点中的rk_485_gpio，所以`struct pinctrl_state *default_state`这一默认状态结构体指针会用来存放11行的引脚复用信息，而在上一章节中也提到了设备树中的**pinctrl节点会转换为pinctrl_map结构体**，那么`struct pinctrl_state *default_state`**必然会跟pinctrl_map结构体建立联系**，那这个联系是如何建立的呢？就让我们一起进入pinctrl_bind_pins函数的学习吧。

#### pinctrl节点会转换为pinctrl_map结构体，default_state必会与其建立联系(❤️)


### 7、


### 8、



## pinctrl_bind_pins函数分析1
### 1 、函数的具体内容如下（1--->）
```c
int pinctrl_bind_pins(struct device *dev)
{
	int ret;
 
	// 检查设备是否重用了节点
	if (dev->of_node_reused)
		return 0;
 
	// 为设备的引脚分配内存空间
	dev->pins = devm_kzalloc(dev, sizeof(*(dev->pins)), GFP_KERNEL);
	if (!dev->pins)
		return -ENOMEM;
 
	// 获取设备的 pinctrl 句柄
	dev->pins->p = devm_pinctrl_get(dev);
	if (IS_ERR(dev->pins->p)) {
		dev_dbg(dev, "没有 pinctrl 句柄\n");
		ret = PTR_ERR(dev->pins->p);
		goto cleanup_alloc;
	}
 
	// 查找设备的默认 pinctrl 状态
	dev->pins->default_state = pinctrl_lookup_state(dev->pins->p, PINCTRL_STATE_DEFAULT);
	if (IS_ERR(dev->pins->default_state)) {
		dev_dbg(dev, "没有默认的 pinctrl 状态\n");
		ret = 0;
		goto cleanup_get;
	}
 
	// 查找设备的初始化 pinctrl 状态
	dev->pins->init_state = pinctrl_lookup_state(dev->pins->p, PINCTRL_STATE_INIT);
	if (IS_ERR(dev->pins->init_state)) {
		/* 不提供此状态是完全合法的 */
		dev_dbg(dev, "没有初始化的 pinctrl 状态\n");
 
		// 选择默认的 pinctrl 状态
		ret = pinctrl_select_state(dev->pins->p, dev->pins->default_state);
	} else {
		// 选择初始化的 pinctrl 状态
		ret = pinctrl_select_state(dev->pins->p, dev->pins->init_state);
	}
 
	if (ret) {
		dev_dbg(dev, "无法激活初始的 pinctrl 状态\n");
		goto cleanup_get;
	}
 
#ifdef CONFIG_PM
	/*
	 * 如果启用了电源管理，我们还会寻找可选的睡眠和空闲的引脚状态，其语义在
	 * <linux/pinctrl/pinctrl-state.h> 中定义
	 */
	dev->pins->sleep_state = pinctrl_lookup_state(dev->pins->p, PINCTRL_STATE_SLEEP);
	if (IS_ERR(dev->pins->sleep_state))
		/* 不提供此状态是完全合法的 */
		dev_dbg(dev, "没有睡眠的 pinctrl 状态\n");
 
	dev->pins->idle_state = pinctrl_lookup_state(dev->pins->p, PINCTRL_STATE_IDLE);
	if (IS_ERR(dev->pins->idle_state))
		/* 不提供此状态是完全合法的 */
		dev_dbg(dev, "没有空闲的 pinctrl 状态\n");
#endif
 
	return 0;
 
	/*
	 * 如果对于此设备没有找到 pinctrl 句柄或默认状态，
	 * 让我们明确释放设备中的引脚容器，因为保留它没有意义。
	 */
cleanup_get:
	devm_pinctrl_put(dev->pins->p);
cleanup_alloc:
	devm_kfree(dev, dev->pins);
	dev->pins = NULL;
 
	/* 返回延迟 */
	if (ret == -EPROBE_DEFER)
		return ret;
	/* 返回严重错误 */
	if (ret == -EINVAL)
		return ret;
	/* 我们忽略诸如 -ENOENT 的错误，表示没有 pinctrl 状态 */
 
	return 0;
}
```

#### 解析：
> （1）第5-7行：函数检查设备是否重用了节点（dev->of_node_reused）。如果设备重用了节点，则直接返回0，表示绑定成功。
> 
> （2）第9-12行：如果设备没有重用节点，则为设备的引脚分配内存空间。使用 devm_kzalloc 函数分配了大小为 `sizeof(*(dev->pins))` 的内存空间，并将其赋值给 dev->pins。如果内存分配失败，则返回-ENOMEM。
> 
> （3）第14-20行：获取设备的pinctrl句柄。`使用 devm_pinctrl_get 函数`**获取设备的pinctrl句柄，并将其赋值给 dev->pins->p**。如果获取失败，函数会打印一条调试信息，并返回获取失败的错误码。（关于pinctrl_bind_pins函数分析还没有完成，会在后面的章节继续分析）





### 2 、devm_pinctrl_get 函数(2<---)
- 1 内核源码目录下的“drivers/pinctrl/core .c”文件中
- 2 获取设备的pinctrl句柄

```c
struct pinctrl *devm_pinctrl_get(struct device *dev)
{
	struct pinctrl **ptr, *p;
 
	// 为存储引脚控制器句柄的指针分配内存
	ptr = devres_alloc(devm_pinctrl_release, sizeof(*ptr), GFP_KERNEL);
	if (!ptr)
		return ERR_PTR(-ENOMEM);
 
	// 获取设备的引脚控制器句柄
	p = pinctrl_get(dev);
	if (!IS_ERR(p)) {
		// 如果获取成功，将引脚控制器句柄存储在指针中
		*ptr = p;
		// 将指针添加到设备资源中
		devres_add(dev, ptr);
	} else {
		// 如果获取失败，释放之前分配的指针内存
		devres_free(ptr);
	}
 
	// 返回引脚控制器句柄或错误码指针
	return p;
}
```


- 1 最重要的内容为第10行，使用pinctrl_get函数获取引脚控制器句柄
### 3 、pinctrl_get函数(3<---)
```c
struct pinctrl *pinctrl_get(struct device *dev)
{
	struct pinctrl *p;
 
	// 检查设备指针是否为空
	if (WARN_ON(!dev))
		return ERR_PTR(-EINVAL);
 
	/*
	 * 查看是否有其他组件（如设备核心）已经获取了此设备的引脚控制器句柄。
	 * 在这种情况下，返回对该句柄的另一个指针。
	 */
	p = find_pinctrl(dev);
	if (p) {
		dev_dbg(dev, "obtain a copy of previously claimed pinctrl\n");
		kref_get(&p->users);
		return p;
	}
 
	// 创建并返回设备的引脚控制器句柄
	return create_pinctrl(dev, NULL);
}
```


### 4 、create_pinctrl的函数(4<---)
- 2 创建并返回设设备的引脚控制器句柄

```c
static struct pinctrl *create_pinctrl(struct device *dev,
				      struct pinctrl_dev *pctldev)
{
	struct pinctrl *p;
	const char *devname;
	struct pinctrl_maps *maps_node;
	int i;
	const struct pinctrl_map *map;
	int ret;
 
	/*
	 * 为每个映射创建状态 cookie 持有者 struct pinctrl。
	 * 这是当使用 pinctrl_get() 请求引脚控制句柄时消费者将获得的对象。
	 */
	p = kzalloc(sizeof(*p), GFP_KERNEL);
	if (!p)
		return ERR_PTR(-ENOMEM);
	p->dev = dev;
	INIT_LIST_HEAD(&p->states);
	INIT_LIST_HEAD(&p->dt_maps);
 
	ret = pinctrl_dt_to_map(p, pctldev);
	if (ret < 0) {
		kfree(p);
		return ERR_PTR(ret);
	}
 
	devname = dev_name(dev);
 
	mutex_lock(&pinctrl_maps_mutex);
	/* 遍历引脚控制映射以定位正确的映射 */
	for_each_maps(maps_node, i, map) {
		/* 映射必须适用于此设备 */
		if (strcmp(map->dev_name, devname))
			continue;
		/*
		 * 如果 pctldev 不为空，我们正在声明它的独占使用权，
		 * 这意味着它自己提供了该设置。
		 *
		 * 因此，我们必须跳过适用于此设备但由其他设备提供的映射。
		 */
		if (pctldev &&
		    strcmp(dev_name(pctldev->dev), map->ctrl_dev_name))
			continue;
 
		ret = add_setting(p, pctldev, map);
		/*
		 * 在这一点上，添加设置可能会导致：
		 *
		 * - 延迟，如果引脚控制设备尚不可用
		 * - 失败，如果引脚控制设备尚不可用，
		 *   并且该设置是一个独占设置。我们不能推迟它，因为
		 *   该独占设置会在设备注册后立即生效。
		 *
		 * 如果返回的错误不是 -EPROBE_DEFER，则我们将
		 * 累积错误，以查看是否最终得到 -EPROBE_DEFER，
		 * 因为那是最糟糕的情况。
		 */
		if (ret == -EPROBE_DEFER) {
			pinctrl_free(p, false);
			mutex_unlock(&pinctrl_maps_mutex);
			return ERR_PTR(ret);
		}
	}
	mutex_unlock(&pinctrl_maps_mutex);
 
	if (ret < 0) {
		/* 如果发生了除推迟以外的其他错误，则在此处返回 */
		pinctrl_free(p, false);
		return ERR_PTR(ret);
	}
 
	kref_init(&p->users);
 
	/* 将引脚控制句柄添加到全局列表 */
	mutex_lock(&pinctrl_list_mutex);
	list_add_tail(&p->node, &pinctrl_list);
	mutex_unlock(&pinctrl_list_mutex);
 
	return p;
}
```


#### 函数解析：(❤️)

> 第4行-第9行：函数声明了需要用到的变量和指针，其中 **struct pinctrl类型的变量p用于表示创建的引脚控制器句柄**，struct pinctrl 结构体用于表示引脚控制器

> （2）第15-17行：使用 kzalloc 函数为 p 分配内存，大小为 `sizeof(*p)`，并将分配的内存清零。检查内存分配是否成功，如果失败则返回错误码 -ENOMEM。
> 
> （3）第18行：**将 dev 赋值给 p->dev，表示引脚控制器与设备关联**。
> 
> （3）第19-20行：使用 INIT_LIST_HEAD 宏初始化 p->states 和 p->dt_maps 字段，它们是链表头，用于存储引脚配置的状态和设备树映射。
> 
> （4）第22-26行：`调用 pinctrl_dt_to_map 函数`**将设备树中定义的引脚映射信息转换为 struct pinctrl_map 结构，并将其添加到 p->dt_maps 链表中**。如果转换过程中出现错误（返回值小于 0），则释放之前分配的内存，并返回对应的错误码（关于create_pinctrl函数的讲解在后面的章节会继续，这里要先跳转到他的子函数进行讲解）。





#### pinctrl 结构体定义：表示引脚控制器(❤️)
- 1 内核源码目录下的“drivers/pinctrl/core.h”文件中
- 2 引脚控制器是硬件系统中管理和控制引脚（GPIO）的组件，它负责配置引脚的功能、电气属性等
```c
struct pinctrl {
	struct list_head node;      // 用于将引脚控制器添加到全局列表的链表节点
	struct device *dev;         // 关联的设备
	struct list_head states;    // 存储引脚配置状态的链表，用于跟踪不同的引脚配置状态
	struct pinctrl_state *state; // 当前应用的引脚配置状态
	struct list_head dt_maps;   // 存储设备树中定义的引脚映射信息的链表
	struct kref users;          // 引脚控制器的引用计数，用于跟踪引脚控制器的引用数量
};
```

#### pinctrl_maps 结构体：用于遍历引脚控制映射(❤️)
- 1 定义在内核源码目录下的“drivers/pinctrl/core.h”文件中
- 2 引脚控制器映射描述了不同引脚控制器的功能和配置与实际硬件引脚之间的对应关系
```c
struct pinctrl_maps {
	struct list_head node;            // 引脚控制器映射链表节点，用于将该映射添加到全局列表
	const struct pinctrl_map *maps;  // 指向引脚控制器映射数组的指针
	unsigned num_maps;                // 引脚控制器映射数组中的映射数量
};
```




### 5、pinctrl_dt_to_map函数(5<---)

```c
int pinctrl_dt_to_map(struct pinctrl *p, struct pinctrl_dev *pctldev)
{
    struct device_node *np = p->dev->of_node;  // 获取引脚控制器关联设备的设备树节点
    int state, ret;
    char *propname;
    struct property *prop;
    const char *statename;
    const __be32 *list;
    int size, config;
    phandle phandle;
    struct device_node *np_config;
 
    /* 如果 CONFIG_OF 启用，且 p->dev 不是从设备树实例化而来 */
    if (!np) {
        if (of_have_populated_dt())
            dev_dbg(p->dev, "no of_node; not parsing pinctrl DT\n");
        return 0;
    }
 
    /* 节点内部存储属性名称的指针 */
    of_node_get(np);
 
    /* 对于每个定义的状态 ID */
    for (state = 0;; state++) {
        /* 获取 pinctrl-* 属性 */
        propname = kasprintf(GFP_KERNEL, "pinctrl-%d", state);
        prop = of_find_property(np, propname, &size);
        kfree(propname);
        if (!prop) {
            if (state == 0) {
                of_node_put(np);
                return -ENODEV;
            }
            break;
        }
        list = prop->value;
        size /= sizeof(*list);
 
        /* 判断 pinctrl-names 属性是否命名了该状态 */
        ret = of_property_read_string_index(np, "pinctrl-names", state, &statename);
        /*
         * 如果未命名，则 statename 仅是整数状态 ID。但是，为了避免动态分配和之后要释放的麻烦，
         * 可以直接将 statename 指向属性名称的一部分。
         */
        if (ret < 0) {
            /* strlen("pinctrl-") == 8 */
            statename = prop->name + 8;
        }
 
        /* 对于其中的每个引用的引脚配置节点 */
        for (config = 0; config < size; config++) {
            phandle = be32_to_cpup(list++);
 
            /* 查找引脚配置节点 */
            np_config = of_find_node_by_phandle(phandle);
            if (!np_config) {
                dev_err(p->dev, "prop %s index %i invalid phandle\n", prop->name, config);
                ret = -EINVAL;
                goto err;
            }
 
            /* 解析节点 */
            ret = dt_to_map_one_config(p, pctldev, statename, np_config);
            of_node_put(np_config);
            if (ret < 0)
                goto err;
        }
 
        /* 如果在设备树中没有条目，则生成一个虚拟状态表条目 */
        if (!size) {
            ret = dt_remember_dummy_state(p, statename);
            if (ret < 0)
                goto err;
        }
    }
 
    return 0;
 
err:
    pinctrl_dt_free_maps(p);
    return ret;
}
```

#### 函数解析：
> （1）第3行：获取与引脚控制器关联设备的设备树节点。
> 
> （2）第13-18行：如果设备树节点为空，表示没有设备树信息可供解析。如果内核配置中启用了CONFIG_OF选项，并且设备并非从设备树实例化，函数会打印一条调试信息并立即返回0。
> 
> （3）第21行：增加设备树节点的引用计数，以确保在解析过程中节点不会被释放。
> 
> （4）第24-76行：对于每个定义的状态ID，循环解析引脚控制器的映射信息具体会执行以下步骤：
> 
> ·第26行构造属性名称字符串 propname，例如 "pinctrl-0"、"pinctrl-1" 等等。
> 
> ·第27-35行：使用 of_find_property 函数获取设备树节点 np 中的属性 propname 的值，并得到属性值的大小 size。如果属性不存在，则判断是否是第一个状态 ID，如果是，则释放节点引用并返回 -ENODEV 表示设备树节点中没有有效的 pinctrl 描述。否则，跳出循环。
> 
> ·第36-37行：将属性值转换为指针列表 list，并计算列表的大小。
> 
> ·第40-49行：如果设备树中的 pinctrl-names 属性命名了该状态，则使用 of_property_read_string_index 函数读取属性值，并将状态名称存储在 statename 变量中。否则，将 statename 指向属性名称的一部分，即去除 "pinctrl-" 前缀。
> 
> ·第51-76行：对于每个引用的引脚配置节点，执行以下步骤：
> 
> ·第53行：将 list 指针指向的 phandle 值转换为本地字节序。
> 
> ·第56行-61行：`使用 of_find_node_by_phandle 函数`**根据 phandle 查找引脚配置节点，并将其存储在 np_config 变量中**。如果找不到引脚配置节点，则打印错误信息并返回 -EINVAL。
> 
> ·第64行：`调用 dt_to_map_one_config 函数`，**将引脚配置节点的信息解析为 pinctrl 映射，并存储在 pctldev 中**。
> 
> ·第65行：递减引脚配置节点的引用计数。
> 
> ·第70-75行如果在设备树中没有条目，则生成一个虚拟状态表条目，以便后续处理。

- 1 第64行 dt_to_map_one_config 函数需要特别注意


### 6、dt_to_map_one_config 函数(6<--)
- 1 从设备树节点中解析出引脚控制器的映射表，并将其存储起来

```c
static int dt_to_map_one_config(struct pinctrl *p,
				struct pinctrl_dev *hog_pctldev,
				const char *statename,
				struct device_node *np_config)
{
	struct pinctrl_dev *pctldev = NULL;
	struct device_node *np_pctldev;
	const struct pinctrl_ops *ops;
	int ret;
	struct pinctrl_map *map;
	unsigned num_maps;
	bool allow_default = false;
 
	/* 查找包含 np_config 的引脚控制器 */
	np_pctldev = of_node_get(np_config);
	for (;;) {
		/* 如果不允许默认配置，则读取 pinctrl-use-default 属性 */
		if (!allow_default)
			allow_default = of_property_read_bool(np_pctldev,
							      "pinctrl-use-default");
 
		/* 获取 np_pctldev 的父节点 */
		np_pctldev = of_get_next_parent(np_pctldev);
		/* 如果没有父节点或者父节点是根节点，则释放 np_pctldev 引用并返回 */
		if (!np_pctldev || of_node_is_root(np_pctldev)) {
			of_node_put(np_pctldev);
			/* 检查是否延迟探测驱动程序状态 */
			ret = driver_deferred_probe_check_state(p->dev);
			/* 如果启用了模块并且不允许默认配置，并且返回值是 -ENODEV，则延迟探测 */
			if (IS_ENABLED(CONFIG_MODULES) && !allow_default && ret == -ENODEV)
				ret = -EPROBE_DEFER;
 
			return ret;
		}
		/* 如果正在创建一个 hog，可以使用传递的 pctldev */
		if (hog_pctldev && (np_pctldev == p->dev->of_node)) {
			pctldev = hog_pctldev;
			break;
		}
		/* 通过 np_pctldev 获取 pinctrl_dev 结构体 */
		pctldev = get_pinctrl_dev_from_of_node(np_pctldev);
		/* 如果获取到了 pinctrl_dev 结构体，则跳出循环 */
		if (pctldev)
			break;
		/* 不要推迟探测 hogs（循环） */
		if (np_pctldev == p->dev->of_node) {
			of_node_put(np_pctldev);
			return -ENODEV;
		}
	}
	of_node_put(np_pctldev);
 
	/*
	 * 调用 pinctrl 驱动程序解析设备树节点，并生成映射表条目
	 */
	ops = pctldev->desc->pctlops;
	/* 检查 pinctrl 驱动程序是否支持设备树 */
	if (!ops->dt_node_to_map) {
		dev_err(p->dev, "pctldev %s doesn't support DT\n",
			dev_name(pctldev->dev));
		return -ENODEV;
	}
	/* 调用 pinctrl 驱动程序的 dt_node_to_map 方法 */
	ret = ops->dt_node_to_map(pctldev, np_config, &map, &num_maps);
	if (ret < 0)
		return ret;
 
	/* 将映射表块存储起来以供后续使用 */
	return dt_remember_or_free_map(p, statename, pctldev, map, num_maps);
}
```

#### 函数解析：(❤️)
> 第15-51行：通过循环查找包含指定设备树节点 np_config 的引脚控制器。在循环中，会获取当前节点的父节点，并判断是否满足终止条件。如果找到了引脚控制器，将其赋值给变量 pctldev，否则返回错误码。
> 
> 第53-62行：检查引脚控制器是否支持设备树操作，即是否实现了 dt_node_to_map 方法。如果不支持，返回错误码。
> 
> 第63-67行：`调用引脚控制器的 dt_node_to_map 方法`，**将设备树节点 np_config 转换为映射表条目**。该方法会解析设备树节点，并根据节点信息生成映射表条目。具体的转换过程由各个引脚控制器的驱动程序实现。
> 
> 第69行：**将生成的映射表条目存储起来，以供后续使用**。存储的操作由函数 dt_remember_or_free_map 完成。
> 

### 7、


### 8、设备树节点转换为pinctrl_map的流程(❤️)



## pinctrl_bind_pins函数分析2

### 1 、 dt_remember_or_free_map 函数(7<---)
- 1 存储的操作由函数 dt_remember_or_free_map 完成

```c
static int dt_remember_or_free_map(struct pinctrl *p, const char *statename,
				   struct pinctrl_dev *pctldev,
				   struct pinctrl_map *map, unsigned num_maps)
{
	int i;
	struct pinctrl_dt_map *dt_map;
 
	/* 初始化公共映射表条目字段 */
	for (i = 0; i < num_maps; i++) {
		const char *devname;
 
		/* 复制设备名称 */
		devname = kstrdup_const(dev_name(p->dev), GFP_KERNEL);
		if (!devname)
			goto err_free_map;
 
		/* 设置映射表条目的设备名称、状态名称和控制器设备名称 */
		map[i].dev_name = devname;
		map[i].name = statename;
		if (pctldev)
			map[i].ctrl_dev_name = dev_name(pctldev->dev);
	}
 
	/* 记录转换后的映射表条目 */
	dt_map = kzalloc(sizeof(*dt_map), GFP_KERNEL);
	if (!dt_map)
		goto err_free_map;
 
	dt_map->pctldev = pctldev;
	dt_map->map = map;
	dt_map->num_maps = num_maps;
	list_add_tail(&dt_map->node, &p->dt_maps);
 
	/* 注册映射表条目 */
	return pinctrl_register_mappings(map, num_maps);
 
err_free_map:
	/* 释放映射表条目内存 */
	dt_free_map(pctldev, map, num_maps);
	return -ENOMEM;
}
```

#### 函数传递参数：
> `·p`：指向 struct pinctrl 结构体的指针，表示**引脚控制器的上下文**。
> 
> ·`statename`：指向**状态名称的指针**，表示要设置的状态的名称。
> 
> ·`pctldev`：指向 struct **pinctrl_dev 结构体**的指针，表示**引脚控制器设备**。
> 
> ·`map`：指向 struct pinctrl_map 结构体数组的指针，表示解析得到的**映射表条目**。
> 
> `·num_maps：`表示映射表条目的数量。
> 


#### 函数解析：(❤️)
> （1）第9-22行：通过**循环遍历映射表条目数组，为每个条目初始化公共字段**。
> 
> ·首先，通过 kstrdup_const 函数复制引脚控制器设备的名称，并将返回的指针赋值给 devname。
> 
> ·然后，将设备名称、状态名称和控制器设备名称分别赋值给映射表条目的对应字段。
> 
> （2）第25-32行：分配并**初始化一个 struct pinctrl_dt_map 结构体，用于存储映射表的相关信息，并将其添加到 p->dt_maps 链表的尾部**。
> 
> ·使用 kzalloc 分配内存空间，并将返回的指针赋值给 dt_map。
> 
> ·将传入的 pctldev、map 和 num_maps 分别赋值给 dt_map 的对应字段
> 
> ·使用 list_add_tail 函数将 dt_map 添加到 p->dt_maps 链表中。
> 
（3）第35行：`用 pinctrl_register_mappings 函数`注册映射表条目。该函数**将映射表条目注册到 pinctrl 子系统**，以便后续可以通过相关接口进行引脚配置和管理。



#### struct pinctrl_dt_map 结构体
```c
struct pinctrl_dt_map {
	struct list_head node;//用于将映射表结构体添加到 pinctrl 的 dt_maps 链表中
	struct pinctrl_dev *pctldev;// 引脚控制器设备
	struct pinctrl_map *map;// 映射表条目数组
	unsigned num_maps;//映射表条目数量
};
```


### 2 、pinctrl_register_mappings 函数(8<---)
- 1 将映射表条目注册到 pinctrl 子系统
- 2 内核源码目录下的”drivers/pinctrl/core.c“文件中

```c
/**
 * pinctrl_register_mappings - 注册引脚控制器映射表
 *
 * @maps: 指向映射表条目数组的指针
 * @num_maps: 映射表条目数量
 *
 * 返回值：0 表示注册成功，负值表示注册失败
 */
int pinctrl_register_mappings(const struct pinctrl_map *maps,
			      unsigned num_maps)
{
	int i, ret;
	struct pinctrl_maps *maps_node;
 
	pr_debug("add %u pinctrl maps\n", num_maps);
 
	/* 首先对新映射表进行合法性检查 */
	for (i = 0; i < num_maps; i++) {
		// 检查设备名称是否存在
		if (!maps[i].dev_name) {
			pr_err("failed to register map %s (%d): no device given\n",
			       maps[i].name, i);
			return -EINVAL;
		}
 
		// 检查映射表名称是否存在
		if (!maps[i].name) {
			pr_err("failed to register map %d: no map name given\n",
			       i);
			return -EINVAL;
		}
 
		// 对于引脚映射类型和配置映射类型，检查引脚控制设备名称是否存在
		if (maps[i].type != PIN_MAP_TYPE_DUMMY_STATE &&
				!maps[i].ctrl_dev_name) {
			pr_err("failed to register map %s (%d): no pin control device given\n",
			       maps[i].name, i);
			return -EINVAL;
		}
 
		switch (maps[i].type) {
		case PIN_MAP_TYPE_DUMMY_STATE:
			// 对于虚拟状态映射类型，不进行验证
			break;
		case PIN_MAP_TYPE_MUX_GROUP:
			// 对于复用组映射类型，进行引脚复用映射验证
			ret = pinmux_validate_map(&maps[i], i);
			if (ret < 0)
				return ret;
			break;
		case PIN_MAP_TYPE_CONFIGS_PIN:
		case PIN_MAP_TYPE_CONFIGS_GROUP:
			// 对于配置映射类型，进行引脚配置映射验证
			ret = pinconf_validate_map(&maps[i], i);
			if (ret < 0)
				return ret;
			break;
		default:
			// 对于无效的映射类型，返回错误
			pr_err("failed to register map %s (%d): invalid type given\n",
			       maps[i].name, i);
			return -EINVAL;
		}
	}
 
	// 分配映射表节点内存
	maps_node = kzalloc(sizeof(*maps_node), GFP_KERNEL);
	if (!maps_node)
		return -ENOMEM;
 
	// 设置映射表节点的映射表和映射表数量
	maps_node->maps = maps;
	maps_node->num_maps = num_maps;
 
	// 加锁并将映射表节点插入映射表链表末尾
	mutex_lock(&pinctrl_maps_mutex);
	list_add_tail(&maps_node->node, &pinctrl_maps);
	mutex_unlock(&pinctrl_maps_mutex);
 
	return 0;
}
```

#### 函数解析：
> （1）第18-64行：进行一些**合法性检查**。对于每一个映射表条目，会进行以下的检查操作：
> 
> ·第20-24行：检查设备名称是否存在
> 
> ·第26-31行：检查映射表名称是否存在，如果不存在则返回一个错误码。
> 
> ·第33-39行：对于引脚映射类型和配置映射类型，检查引脚控制设备名称是否存在，如果不存在则返回一个错误码。
> 
> ·第41-63行：根据映射表的类型做对应的验证操作：
> 
> ·如果类型是PIN_MAP_TYPE_DUMMY_STATE，表示是虚拟状态映射类型，不进行验证。
> 
> ·如果类型是PIN_MAP_TYPE_MUX_GROUP，表示是复用组映射类型，需要进行引脚复用映射的验证。
> 
> ·如果类型是PIN_MAP_TYPE_CONFIGS_PIN或PIN_MAP_TYPE_CONFIGS_GROUP，表示是配置映射类型，需要进行引脚配置映射的验证。
> 
> ·如果类型不是以上这些有效的类型，则返回一个错误码。
> 
> （2）第66-73行：函数会分配映射表节点的内存，并将映射表和映射表数量设置到映射表节点中。
> 
> （3）第75-78行：函数会获取一个互斥锁，**将映射表节点插入到映射表链表的末尾**，并释放互斥锁。
> 
> pinctrl_register_mappings 函数的作用是注册一个引脚控制器的映射表，进行了一些参数合法性检查和验证，并将映射表节点插入到映射表链表中。


### 3 、



### 4 、该阶段大多都是关于赋值的操作并将节点加入到链表中(❤️)



### 5、问题还没解决：
> 但分析到这里我们**仍旧没有找到`struct pinctrl_state *default_state和pinctrl_map结构体`是在什么地方进行的绑定**，所以在下个章节我们将继续分析124.2 小节中create_pinctrl函数接下来的部分。

### 6、





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


