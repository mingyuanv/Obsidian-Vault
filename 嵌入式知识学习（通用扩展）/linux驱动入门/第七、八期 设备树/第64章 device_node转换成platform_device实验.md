---
title: "{{title}}"
aliases:
tags:
description:
source: https://blog.csdn.net/BeiJingXunWei/article/details/134344871
---

# 备注(声明)：






# 一、device_node转换成platform_device实验

## 转换规格
### 1 、转换规则
> 在之前学习的平台总线模型中，device部分是用platform_device结构体来描述硬件资源的，所以内核最终会将内核认识的device_node树转换platform_ device，但是并不是所有的device_node都会被转换成platform_ device，只有满足要求的才会转换成platform_ device,**转换成platform_device的节点可以在/sys/bus/platform/devices下查看**，那device_node节点要满足什么要求才会被转换成platform_device呢?

#### 规则1(❤️)
- 1 转换成platform_device要满足的要求
> 根据规则1，首先遍历**根节点下包含 compatible 属性的子节点**，对于每个子节点，创建一个对应的 platform_device。



#### 规则2： "simple-bus"、"simple-mfd" 或 "isa"(❤️)
> 根据规则2，遍历包含 compatible 属性为 "simple-bus"、"simple-mfd" 或 "isa" 的节点以及它们的子节点。**如果子节点包含 compatible 属性值则会创建一个对应的platform_device。**

> 内核遍历设备树时，**不仅限于根节点下一级，任何层级中只要某节点本身符合匹配条件（如 `"simple-bus"` 等），就会被创建为 `platform_device`**，并由此继续递归处理其子孙节点。




#### 规则3： "arm" 或 "primecell"
> 根据规则3，检查节点的 **compatible 属性是否包含 "arm" 或 "primecell"**。如果是，**则不将该节点转换**为 platform_device，而是将其**识别为 AMBA 设备**。

####  其他规则(❤️)
- 2 I2C 或 SPI 总线下的子节点 **不会** 被转换为 `platform_device`，而是由对应的总线驱动处理。


### 2 、举例1：
- 1 cpu1       gpio@22020101
```d
/dts-v1/;
 
/ {
    model = "This is my devicetree!";
    #address-cells = <1>;
    #size-cells = <1>;
 
    chosen {
        bootargs = "root=/dev/nfs rw nfsroot=192.168.1.1 console=ttyS0, 115200";
    };
    
//适合规则三，不转化
    cpu1: cpu@1 {
        device_type = "cpu";
        compatible = "arm,cortex-a35", "arm,armv8";
        reg = <0x0 0x1>;
    };
 
    aliases {
        led1 = "/gpio@22020101";
    };
 
    node1 {
        #address-cells = <1>;
        #size-cells = <1>;
 
        gpio@22020102 {
            reg = <0x20220102 0x40>;
        };
    };
 
    node2 {
        node1-child {
            pinnum = <01234>;
        };
    };
 //适合规则一，转化
    gpio@22020101 {
        compatible = "led";
        reg = <0x20220101 0x40>;
        status = "okay";
    };
};
```


### 3 、举例2：
- 1 node1
```d
/dts-v1/;
 
/ {
    model = "This is my devicetree!";
    #address-cells = <1>;
    #size-cells = <1>;
 
    chosen {
        bootargs = "root=/dev/nfs rw nfsroot=192.168.1.1 console=ttyS0, 115200";
    };
 
    cpu1: cpu@1 {
        device_type = "cpu";
        compatible = "arm,cortex-a35", "arm,armv8";
        reg = <0x0 0x1>;
    };
 
    aliases {
        led1 = "/gpio@22020101";
    };
//compatible属性值为simple-bus，我们需要继续看他的子节点。
//子节点 gpio@22020102 并没有compatible属性值
//node1节点会被转换为 platform_device，而其子节点 gpio@22020102 不会被转换
    node1 {
        #address-cells = <1>;
        #size-cells = <1>;
		compatible = "simple-bus";
        gpio@22020102 {
            reg = <0x20220102 0x40>;
        };
    };
 
    node2 {
        node1-child {
            pinnum = <01234>;
        };
    };
 
    gpio@22020101 {
        compatible = "led";
        reg = <0x20220101 0x40>;
        status = "okay";
    };
};
```


### 4 、举例3：(❤️)
- 1 node1
```d
/dts-v1/;
 
/ {
    model = "This is my devicetree!";
    #address-cells = <1>;
    #size-cells = <1>;
 
    chosen {
        bootargs = "root=/dev/nfs rw nfsroot=192.168.1.1 console=ttyS0, 115200";
    };
 
    cpu1: cpu@1 {
        device_type = "cpu";
        compatible = "arm,cortex-a35", "arm,armv8";
        reg = <0x0 0x1>;
    };
 
    aliases {
        led1 = "/gpio@22020101";
    };
//compatible属性值为simple-bus，我们需要继续看他的子节点。
//子节点 gpio@22020102 的compatible属性值为gpio，所以这里的gpio@22020102节点会被转换成platform_device。
    node1 {
        #address-cells = <1>;
        #size-cells = <1>;
		compatible = "simple-bus";
        gpio@22020102 {
			compatible = "gpio";
            reg = <0x20220102 0x40>;
        };
    };
 
    node2 {
        node1-child {
            pinnum = <01234>;
        };
    };
 
    gpio@22020101 {
        compatible = "led";
        reg = <0x20220101 0x40>;
        status = "okay";
    };
};
```


### 5、举例4：
- 1 amba      dmac_peri     dmac_bus
```d
/dts-v1/;
 
/ {
    model = "This is my devicetree!";
    #address-cells = <1>;
    #size-cells = <1>;
 
    chosen {
        bootargs = "root=/dev/nfs rw nfsroot=192.168.1.1 console=ttyS0,115200";
    };
 
    cpul: cpu@1 {
        device_type = "cpu";
        compatible = "arm,cortex-a35", "arm,armv8";
        reg = <0x0 0x1>;
//amba 节点的compatible值为simple-bus，会被转换为 platform_device.
        amba {
            compatible = "simple-bus";
            #address-cells = <2>;
            #size-cells = <2>;
            ranges;
 //该节点的 compatible 属性包含 "arm,p1330" 和 "arm,primecell"
 //不会被转换为 platform_device，而是被识别为 AMBA 设备。
            dmac_peri: dma-controller@ff250000 {
                compatible = "arm,p1330", "arm,primecell";
                reg = <0x0 0xff250000 0x0 0x4000>;
                interrupts = <GIC_SPI 2 IRQ_TYPE_LEVEL_HIGH>,
                             <GIC_SPI 3 IRQ_TYPE_LEVEL_HIGH>;
                #dma-cells = <1>;
                arm,pl330-broken-no-flushp;
                arm,p1330-periph-burst;
                clocks = <&cru ACLK DMAC_PERI>;
                clock-names = "apb_pclk";
            };
  //该节点的 compatible 属性包含 "arm,p1330" 和 "arm,primecell"
 //不会被转换为 platform_device，而是被识别为 AMBA 设备。
            dmac_bus: dma-controller@ff600000 {
                compatible = "arm,p1330", "arm,primecell";
                reg = <0x0 0xff600000 0x0 0x4000>;
                interrupts = <GIC_SPI 0 IRQ_TYPE_LEVEL_HIGH>,
                             <GIC_SPI 1 IRQ_TYPE_LEVEL_HIGH>;
                #dma-cells = <1>;
                arm,pl330-broken-no-flushp;
                arm,pl330-periph-burst;
                clocks = <&cru ACLK_DMAC_BUS>;
                clock-names = "apb_pclk";
            };
        };
    };
};
```



### 6、



## 转换流程源码分析
### 1 、arch_initcall_sync(of_platform_default_populate_init)
- 1 内核源码目录下的“drivers/of/platform.c”文件中     第555行
```c
arch_initcall_sync(of_platform_default_populate_init);
```

> `arch_initcall_sync `是 Linux 内核中的一个函数，用于在内核初始化过程中执行**架构相关的初始化函数**。它属于内核的初始化调用机制，用于确保在系统启动过程中适时地调用特定架构的初始化函数。

> 在Linux**内核的初始化过程中，各个子系统和架构会注册自己的初始化函数**。这些初始化函数负责完成特定子系统或架构相关的初始化工作，例如<span style="background:#d3f8b6">初始化硬件设备、注册中断处理程序、设置内存映射</span>等。而 arch_initcall_sync 函数则用于调用与当前架构相关的初始化函数。

> 当**内核启动时，调用 rest_init() 函数来启动初始化过程**。在初始化过程中，arch_initcall_sync 函数会被调用，以确保所有与当前架构相关的初始化函数按照正确的顺序执行。这样可以保证在启动过程中，特定架构相关的初始化工作得到正确地完成。


### 2 、of_platform_default_populate_init(void)

> 而of_platform_default_populate_init函数的作用是在内核初始化过程中**自动解析设备树，并根据设备树中的设备节点创建对应的 platform_device 结构**。它会遍历设备树中的设备节点，并为每个设备节点创建一个对应的 platform_device 结构，然后将其注册到内核中，使得设备驱动程序能够识别和操作这些设备。该函数的具体内容如下所示：
```c
static int __init of_platform_default_populate_init(void)
{
    struct device_node *node;
 
    // 暂停设备链接供应商同步状态
    device_links_supplier_sync_state_pause();
 
    // 如果设备树尚未填充，则返回错误码
    if (!of_have_populated_dt())
        return -ENODEV;
 
    /*
     * 显式处理某些兼容性，因为我们不想为/reserved-memory中的每个具有“compatible”的节点创建platform_device。
     */
    for_each_matching_node(node, reserved_mem_matches)
        of_platform_device_create(node, NULL, NULL);
 
    // 查找节点 "/firmware"
    node = of_find_node_by_path("/firmware");
    if (node) {
        // 使用该节点进行设备树平台设备的填充
        of_platform_populate(node, NULL, NULL, NULL);
        of_node_put(node);
    }
 
    // 填充其他设备
    fw_devlink_pause();
    of_platform_default_populate(NULL, NULL, NULL);
    fw_devlink_resume();
 
    return 0;
}
```

> 第6行：暂停设备链接供应商的同步状态，确保设备链接的状态不会在此过程中被改变。
> 
> 第9行：检查设备树是否已经被填充。如果设备树尚未填充，则返回错误码 -ENODEV。
> 
> 第16行：**遍历设备树中与 reserved_mem_matches 匹配的节点**。这些节点是 /reserved-memory 中具有 "compatible" 属性的节点。
> 
> 第17行：为 /reserved-memory 中匹配的节点**创建 platform_device 结构**。这些节点不会为每个节点都创建 platform_device，而是根据需要进行显式处理。
> 
> 第20行：在设备树中**查找路径为 "/firmware" 的节点**。
> 
> 第23行：使用找到的节点**填充设备树中的平台设备**。这些节点可能包含与**固件相关**的设备。
> 
> 第28行：暂停固件设备链接，确保在填充其他设备时链接状态不会改变。
> 
> 第29行：**填充设备树中的其他设备**。
> 
> 第30行：恢复固件设备链接。


- 1 着重关注的是第29行的of_platform_default_populate(NULL, NULL, NULL)函数       
### 3 、of_platform_default_populate(NULL, NULL, NULL)函数
- 1 填充设备树中的其他设备
```c
int of_platform_default_populate(struct device_node *root,
				 const struct of_dev_auxdata *lookup,
				 struct device *parent)
{
	return of_platform_populate(root, of_default_bus_match_table, lookup,parent);
}
```

> 该函数的作用是调用 of_platform_populate 函数来填充设备树中的平台设备，并**使用默认的设备匹配表 of_default_bus_match_table**，设备匹配表内容如下所示：
```c
const struct of_device_id of_default_bus_match_table[] = {
	{ .compatible = "simple-bus", },
	{ .compatible = "simple-mfd", },
	{ .compatible = "isa", },
#ifdef CONFIG_ARM_AMBA
	{ .compatible = "arm,amba-bus", },
#endif /* CONFIG_ARM_AMBA */
	{} /* Empty terminated list */
};
```
> 上述的设备匹配表就是我们在第一小节中**第2条规则**，，函数将自动根据设备树节点的属性匹配相应的设备驱动程序，并填充内核的平台设备列表。


- 1  着重关注的是调用的 of_platform_populate 函数 
### 4 、of_platform_populate函数
```c
int of_platform_populate(struct device_node *root,
			const struct of_device_id *matches,
			const struct of_dev_auxdata *lookup,
			struct device *parent)
{
	struct device_node *child;
	int rc = 0;
 
	// 如果 root 不为空，则增加 root 节点的引用计数；否则，在设备树中根据路径查找 root 节点
	root = root ? of_node_get(root) : of_find_node_by_path("/");
	if (!root)
		return -EINVAL;
 
	pr_debug("%s()\n", __func__);
	pr_debug(" starting at: %pOF\n", root);
 
	// 暂停设备链接供应商同步状态
	device_links_supplier_sync_state_pause();
 
	// 遍历 root 节点的所有子节点
	for_each_child_of_node(root, child) {
		// 创建平台设备并添加到设备树总线
		rc = of_platform_bus_create(child, matches, lookup, parent, true);
		if (rc) {
			of_node_put(child);
			break;
		}
	}
 
	// 恢复设备链接供应商同步状态
	device_links_supplier_sync_state_resume();
 
	// 设置 root 节点的 OF_POPULATED_BUS 标志
	of_node_set_flag(root, OF_POPULATED_BUS);
 
	// 释放 root 节点的引用计数
	of_node_put(root);
 
	return rc;
}
```
> 第10行：检查给定的设备树节点 node 是否为有效节点。如果节点为空，函数将立即返回。
> 
> 第21行：**遍历设备树节点的子节点**，查找与平台设备相关的节点。这些节点通常具有 compatible 属性，用于匹配设备驱动程序。
> 
> 第23行：对于**每个找到的平台设备节点，创建一个 platform_device 结构**，并根据设备树节点的属性设置该结构的各个字段。
> 
> 第25行：将**创建的 platform_device 添加到内核的平台设备列表中**，以便设备驱动程序能够识别和操作这些设备。




- 1 对第23行核心代码进行讲解
### 5、of_platform_bus_create(child, matches, lookup, parent, true)函数
- 1 创建平台设备
```c
static int of_platform_bus_create(struct device_node *bus,
				  const struct of_device_id *matches,
				  const struct of_dev_auxdata *lookup,
				  struct device *parent, bool strict)
{
	const struct of_dev_auxdata *auxdata;
	struct device_node *child;
	struct platform_device *dev;
	const char *bus_id = NULL;
	void *platform_data = NULL;
	int rc = 0;
 
	/* 确保设备节点具有 compatible 属性 */
	if (strict && (!of_get_property(bus, "compatible", NULL))) {
		pr_debug("%s() - skipping %pOF, no compatible prop\n",
			 __func__, bus);
		return 0;
	}
 
	/* 跳过不想创建设备的节点 */
	if (unlikely(of_match_node(of_skipped_node_table, bus))) {
		pr_debug("%s() - skipping %pOF node\n", __func__, bus);
		return 0;
	}
 
 
	if (of_node_check_flag(bus, OF_POPULATED_BUS)) {
		pr_debug("%s() - skipping %pOF, already populated\n",
			__func__, bus);
		return 0;
	}
 
	auxdata = of_dev_lookup(lookup, bus);
	if (auxdata) {
		bus_id = auxdata->name;
		platform_data = auxdata->platform_data;
	}
 
	if (of_device_is_compatible(bus, "arm,primecell")) {
		/*
		 * 在此处不返回错误以保持与旧设备树文件的兼容性。
		 */
		of_amba_device_create(bus, bus_id, platform_data, parent);
		return 0;
	}
 
	dev = of_platform_device_create_pdata(bus, bus_id, platform_data, parent);
	if (!dev || !of_match_node(matches, bus))
		return 0;
 
	for_each_child_of_node(bus, child) {
		pr_debug("   create child: %pOF\n", child);
		rc = of_platform_bus_create(child, matches, lookup, &dev->dev, strict);
		if (rc) {
			of_node_put(child);
			break;
		}
	}
	of_node_set_flag(bus, OF_POPULATED_BUS);
	return rc;
}
```

> 第14行：如果 strict 为真且设备节点 bus 没有兼容性属性，则输出调试信息并返回 0。这个条件判断**确保设备节点具有 compatible 属性**，因为 compatible 属性用于匹配设备驱动程序，对应我们在上一小节的第1条规则。
> 
> 第21行：如果设备节点 bus 在被跳过的节点表中，则输出调试信息并返回 0。这个条件判断用于跳过不想创建设备的节点。
> 
> 第27行：如果设备节点 bus 的 OF_POPULATED_BUS 标志已经设置，则输出调试信息并返回 0。这个条件判断用于避免重复创建已经填充的设备节点。
> 
> 第34行：使用 lookup 辅助数据结构**查找设备节点 bus 的特定配置信息，并将其赋值给变量 bus_id 和 platform_data**。这个步骤用于获取设备节点的特定配置信息，以便在创建平台设备时使用，由于这里传入的参数为NULL，所以下面的条件判断并不会被执行。
> 
> 第39行：如果设备节点 bus **兼容于 "arm,primecell"，则调用 of_amba_device_create 函数创建 AMBA 设备**，并返回 0，对应我们在上一小节学习的**第3条规则**。
> 
> 第47行：调用` of_platform_device_create_pdata函数`**创建平台设备，并将其赋值给变量 dev**。然后，检查设备节点 bus是否与给定的匹配表 matches 匹配。如果平台设备创建失败或者设备节点不匹配，那么返回 0。
> 
> 第51行-第58行：**遍历设备节点 bus 的每个子节点 child，并递归调用 of_platform_bus_create 函数来创建子节点的平台设备**。




- 1 第47行 of_platform_device_create_pdata函数进行讲解
### 6、of_platform_device_create_pdata函数
```c
static struct platform_device *of_platform_device_create_pdata(
					struct device_node *np,
					const char *bus_id,
					void *platform_data,
					struct device *parent)
{
	struct platform_device *dev;
 
	/* 检查设备节点是否可用或已填充 */
	if (!of_device_is_available(np) ||
	    of_node_test_and_set_flag(np, OF_POPULATED))
		return NULL;
 
	/* 分配平台设备结构体 */
	dev = of_device_alloc(np, bus_id, parent);
	if (!dev)
		goto err_clear_flag;
 
	/* 设置平台设备的一些属性 */
	dev->dev.coherent_dma_mask = DMA_BIT_MASK(32);
	if (!dev->dev.dma_mask)
		dev->dev.dma_mask = &dev->dev.coherent_dma_mask;
	dev->dev.bus = &platform_bus_type;
	dev->dev.platform_data = platform_data;
	of_msi_configure(&dev->dev, dev->dev.of_node);
	of_reserved_mem_device_init_by_idx(&dev->dev, dev->dev.of_node, 0);
 
	/* 将平台设备添加到设备模型中 */
	if (of_device_add(dev) != 0) {
		platform_device_put(dev);
		goto err_clear_flag;
	}
 
	return dev;
 
err_clear_flag:
	/* 清除设备节点的已填充标志 */
	of_node_clear_flag(np, OF_POPULATED);
	return NULL;
```
> 第10行：函数会检查设备节点的可用性，即**检查设备树对应节点的status属性**。如果设备节点不可用或已经被填充，则直接返回 NULL。
> 
> 第15行：函数调用 of_device_alloc **分配一个平台设备结构体**，并将设备节点指针、设备标识符和父设备指针传递给它。如果分配失败，则跳转到 err_clear_flag 标签处进行错误处理。
> 
> 第19行，函数**设置平台设备的一些属性**。它将 coherent_dma_mask 属性设置为 32 位的 DMA 位掩码，并检查 dma_mask 属性是否为 NULL。如果 dma_mask 为 NULL，则将其指向 coherent_dma_mask。然后，函数设置平台设备的总线类型为 platform_bus_type，并将平台数据指针存储在 platform_data 属性中。接着，函数调用 of_msi_configure 和 of_reserved_mem_device_init_by_idx 来配置设备的 MSI 和保留内存信息。
> 
> 第29行：函数调用 of_device_add **将平台设备添加到设备模型中**。如果添加失败，则释放已分配的平台设备，并跳转到 err_clear_flag 标签处进行错误处理。



### 7、函数调用流程图(❤️)
[[嵌入式知识学习（通用扩展）/linux驱动入门/第七、八期 设备树/assets/第64章 device_node转换成platform_device实验/8460863ac8327779927191e379b464ae_MD5.jpeg|Open: file-20250902123016667.png]]
![嵌入式知识学习（通用扩展）/linux驱动入门/第七、八期 设备树/assets/第64章 device\_node转换成platform\_device实验/8460863ac8327779927191e379b464ae\_MD5.jpeg](assets/第64章%20device_node转换成platform_device实验/8460863ac8327779927191e379b464ae_MD5.jpeg)

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


