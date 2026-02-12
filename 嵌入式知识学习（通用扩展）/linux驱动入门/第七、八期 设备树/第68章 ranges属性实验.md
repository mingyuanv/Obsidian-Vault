---
title: "{{title}}"
aliases: 
tags: 
description: 
source:
---

# 备注(声明)：




# 一、platform_get_resource 获取设备树资源


## 驱动程序编写
### 1 、总代码
```c
#include <linux/module.h>
#include <linux/platform_device.h>
#include <linux/mod_devicetable.h>


struct resource *myresources;


// 平台设备的初始化函数
static int my_platform_probe(struct platform_device *pdev)
{
    printk(KERN_INFO "my_platform_probe: Probing platform device\n");

    // 获取平台设备的资源
    myresources=platform_get_resource(pdev,IORESOURCE_MEM,0);
    if(myresources == NULL){

            printk("platform_get_resource get resource error\n");

    }

    printk("reg start is %llx",myresources->start);


    return 0;

}


static int my_platform_remove(struct platform_device *pdev)
{
    printk(KERN_INFO "my_platform_remove: Removing platform device\n");


    return 0;
}

//描述设备树节点和驱动程序之间的匹配规则
static const struct of_device_id of_match_table_id[]={
	{.compatible="my devicestree"},
	{},
};

// 定义平台驱动结构体
static struct platform_driver my_platform_driver = {
    .probe = my_platform_probe,
    .remove = my_platform_remove,
    .driver = {
        .name = "my_platform_device",
        .owner = THIS_MODULE,
        .of_match_table = of_match_table_id,
    },

};

// 模块初始化函数
static int __init my_platform_driver_init(void)
{
    int ret;
    ret = platform_driver_register(&my_platform_driver);
    if(ret){
        printk(KERN_ERR "Failed to register platform driver\n");

        return ret;
    }

    printk(KERN_INFO "my_platform_driver: Platform driver initialized\n");

    return 0;
}


// 模块退出函数
static void __exit my_platform_driver_exit(void)
{
    platform_driver_unregister(&my_platform_driver);
    printk(KERN_INFO "my_platform_driver: Platform driver exited\n");
}


module_init(my_platform_driver_init);
module_exit(my_platform_driver_exit);

MODULE_LICENSE("GPL v2");
MODULE_AUTHOR("topeet");
```



### 2 、关键代码
```c
struct resource *myresources;

// 平台设备的初始化函数
static int my_platform_probe(struct platform_device *pdev)
{
    printk(KERN_INFO "my_platform_probe: Probing platform device\n");

    // 获取平台设备的资源
    myresources=platform_get_resource(pdev,IORESOURCE_MEM,0);
    if(myresources == NULL){

            printk("platform_get_resource get resource error\n");

    }

    printk("reg start is %llx",myresources->start);


    return 0;

}
```




### 3 、实验测试 - 失败
> [root@topeet:~]#` insmod device_tree.ko`
> [   92.798610] device_tree: loading out-of-tree module taints kernel.
> [   92.800431] my_platform_probe: Probing platform device
> [   92.800464] **platform_get_resource get resource error**
> [   92.800498] Unable to handle kernel NULL pointer dereference at virtual address 0000000000000000
> [   92.823849] Mem abort info:
> [   92.826666]   ESR = 0x96000006






### 4 、







## 获取资源失败源码分析
### 1 、platform_get_resource函数分析
- 1 定义在内核源码目录下的"/drivers/base/platform.c"目录
```c
struct resource *platform_get_resource(struct platform_device *dev,
				       unsigned int type, unsigned int num)
{
	u32 i;

	for (i = 0; i < dev->num_resources; i++) {
		struct resource *r = &dev->resource[i];

		if (type == resource_type(r) && num-- == 0)
			return r;
	}
	return NULL;
}
EXPORT_SYMBOL_GPL(platform_get_resource);
```

> 该函数返回NULL符合第一小节中的情况，返回NULL的情况有两种可能性，一种是没进入上面的for循环直接返回了NULL，另外一种是进入了for循环，但是类型匹配不正确，跳出for循环之后再返回NULL。**这里的类型一定是匹配的，所以我们就来寻找为什么没有进入for循环**，这里只有一种可能，也**就是dev->num_resources为0**。


### 2 、探究转换有没有问题（没有问题）

> [root@topeet:`/sys/bus/platform/devices]# ls topeet*`
> **topeet:**
> driver_override  modalias  of_node  power  subsystem  topeet:myled  uevent
> 
> **'topeet:myled':**
> driver_override  modalias  of_node  power  subsystem  uevent
> [root@topeet:/sys/bus/platform/devices]#

- 2 对应目录下也有了相应的节点,证明转换是没问题的

### 3 、寻找中间转换过程中有关资源数量的相关函数

#### of_platform_device_create_pdata函数
- 1 定位到了of_platform_device_create_pdata函数
- 2 定义在内核源码目录下的“drivers/of/platform.c”文件
```c
static struct platform_device *of_platform_device_create_pdata(
					struct device_node *np,
					const char *bus_id,
					void *platform_data,
					struct device *parent)
{
	struct platform_device *dev;
 
........................
 
	/* 分配平台设备结构体 */
	dev = of_device_alloc(np, bus_id, parent);
	if (!dev)
		goto err_clear_flag;
 .......................
 
	return dev;
 
err_clear_flag:
	/* 清除设备节点的已填充标志 */
	of_node_clear_flag(np, OF_POPULATED);	return NULL;
}
```

> 第11行：函数调用 `of_device_alloc `**分配一个平台设备结构体**，并将设备节点指针、设备标识符和父设备指针传递给它，正是该函数**决定的resource.num**,然后找到该函数的定义，如下所示：

##### of_device_alloc函数
```c
struct platform_device *of_device_alloc(struct device_node *np,
				  const char *bus_id,
				  struct device *parent)
{
	struct platform_device *dev;
	int rc, i, num_reg = 0, num_irq;
	struct resource *res, temp_res;
............................
	/* count the io and irq resources */
	while (of_address_to_resource(np, num_reg, &temp_res) == 0)
		num_reg++;
	num_irq = of_irq_count(np);
............................

		dev->num_resources = num_reg + num_irq;
.......................
	return dev;
}
```
> 在第15行出现了for循环的**dev->num_resources = num_reg + num_irq**;reg的number和irq的number，由于在设备树中并没有添加中断相关的属性num_irq为0，那这里的**num_reg在10、11行确定**。
> 
> 我们向上找到10、11行，然后跳转到while循环中的**of_address_to_resource函数**，该函数定义在内核源码目录的drivers/of/address.c文件中，具体内容如下所示：

- 1 若of_address_to_resource函数返回非零，则num_reg=0;

###### of_address_to_resource函数
- 1 定义在内核源码目录的drivers/of/address.c文件
```c
int of_address_to_resource(struct device_node *dev, int index,
			   struct resource *r)
{
	const __be32	*addrp;
	u64		size;
	unsigned int	flags;
	const char	*name = NULL;
 
	addrp = of_get_address(dev, index, &size, &flags);
	if (addrp == NULL)
		return -EINVAL;
 
	/* Get optional "reg-names" property to add a name to a resource */
	of_property_read_string_index(dev, "reg-names",	index, &name);
 
	return __of_address_to_resource(dev, addrp, size, flags, name, r);
}
```
> **第9行，获取reg属性的地址、大小和类型，在设备树中reg属性已经存在了，所以这里会正确返回**。
> 
> 第14行，读取reg-names属性，由于设备树中没有定义这个属性，所以该函数不会有影响。
> 
> 最后**具有决定性作用的函数就是返回的__of_address_to_resource函数**了


- 1 若__of_address_to_resource函数返回非零，则num_reg=0;
######  `__of_address_to_resource`函数
```c
static int __of_address_to_resource(struct device_node *dev,
		const __be32 *addrp, u64 size, unsigned int flags,
		const char *name, struct resource *r)
{
	u64 taddr;

	if (flags & IORESOURCE_MEM)
		taddr = of_translate_address(dev, addrp);
......................
	if (taddr == OF_BAD_ADDR)
		return -EINVAL;
.................................
	return 0;
}
```
> **reg属性的flags为IORESOURCE_MEM**，所以又会执行第9行的of_translate_address函数，跳转到该函数

- 1 若of_translate_address函数返回`OF_BAD_ADDR`，则num_reg=0;
###### of_translate_address函数
```c
u64 of_translate_address(struct device_node *dev, const __be32 *in_addr)
{
	struct device_node *host;
	u64 ret;
 
	ret = __of_translate_address(dev, in_addr, "ranges", &host);
	if (host) {
		of_node_put(host);
		return OF_BAD_ADDR;
	}
 
	return ret;
}
```
> 该函数的重点在第6行，上述函数实际上是__of_translate_address函数的封装，其中传入的第三个**参数“ranges”是我们要关注的重点**，继续跳转到该函数的定义，具体内容如下所示：

- 1 若`__of_translate_address`函数返回`OF_BAD_ADDR`，则num_reg=0;
###### `__of_translate_address`函数
```c
static u64 __of_translate_address(struct device_node *dev,
				  const __be32 *in_addr, const char *rprop,
				  struct device_node **host)
{
	struct device_node *parent = NULL;
	struct of_bus *bus, *pbus;
	__be32 addr[OF_MAX_ADDR_CELLS];
	int na, ns, pna, pns;
	u64 result = OF_BAD_ADDR;
 .....................
	/* Get parent & match bus type */
	parent = of_get_parent(dev);
	if (parent == NULL)
		goto bail;
	bus = of_match_bus(parent);
 
	/* Count address cells & copy address locally */
	bus->count_cells(dev, &na, &ns);
	if (!OF_CHECK_COUNTS(na, ns)) {
		pr_debug("Bad cell count for %pOF\n", dev);
		goto bail;
	}
...............................	
	/* Translate */
	for (;;) {
		struct logic_pio_hwaddr *iorange;
 
		/* Switch to parent bus */
		of_node_put(dev);
		dev = parent;
		parent = of_get_parent(dev);
 ...........................................
		/* Apply bus translation */
		if (of_translate_one(dev, bus, pbus, addr, na, ns, pna, rprop))
			break;
 ....................................
	}
 bail:
	of_node_put(parent);
	of_node_put(dev);
 
	return result;
}
```
> 第12行，获取父节点和匹配的总线类型
> 
> 第18行，获取address-cell和size-cells
> 
> 然后是一个for循环，在34行使用**of_translate_one函数进行转换**，其中**rprop**参数表示要转换的资源属性，**该参数的值为传入的“ranges”**，然后我们继续跳转到该函数，该函数的具体内容如下所示：


- 1 若of_translate_one函数返回非零，则跳出循环，返回result = OF_BAD_ADDR。则num_reg=0;
###### `of_translate_one`函数
```c
static int of_translate_one(struct device_node *parent, struct of_bus *bus,
			    struct of_bus *pbus, __be32 *addr,
			    int na, int ns, int pna, const char *rprop)
{
	const __be32 *ranges;
	unsigned int rlen;
	int rone;
	u64 offset = OF_BAD_ADDR;
...........................................
	ranges = of_get_property(parent, rprop, &rlen);
	if (ranges == NULL && !of_empty_ranges_quirk(parent)) {
		pr_debug("no ranges; cannot translate\n");
		return 1;
	}
	............................................
}
```

> 在该函数的第10行使用of_get_property函数获取“ranges”属性，但**由于在我们添加的设备树节点中并没有该属性**，所以这里的ranges值就为NULL，第27行的条件判断成立，也就会**返回1,则num_reg=0;**。

#### 梳理num_reg =0的返回值过程
> of_translate_one函数返回1之后，上一级的_of_translate_address的返回值就为OF BAD ADDR，再上一级的of_translate_address返回值也是`OF BAD _ADDR`，继续向上查找_of_address_to_resource函数会返回EINVAL，of address_ to resource 返回EINVAL，所以num_reg 为0;




### 4 、总结 - platform_get_resource函数获取资源失败的原因
> 到这里关于为什么platform_get_resource函数获取资源失败的问题就找到了，只是**因为在设备树中并没有这个名为ranges这个属性**，所以只需要对设备树进行ranges属性的添加即可，要修改的设备树为arch/arm64/boot/dts/rockchip/rk3568-evb1-ddr4-v10-linux.dts，

#### 对设备树进行ranges属性的添加即可
```d
/{
	topeet {
		#address-cells = <1>;
		#size-cells = <1>;
		compatible = "simple-bus";
		ranges;
		
		myled {
			compatible = "my devicestree";
			reg = <0xFDD60000 0x00000004>;

		};

	};


};
```

#### 为什么 `ranges` 应该写在 `"simple-bus"` 这一总线节点上？
> `ranges` 是用于定义“**总线层级之间”的地址映射**，因此它必须放在描述总线结构的节点上，而不是放在某个具体的设备节点（如 `myled`）上。

> 这里 `topeet` 节点就是一个简单总线（**simple-bus**），它作为 `myled` 的父节点。在 `topeet` 节点中添加 `ranges;`，就**意味着 `myled` 的 `reg` 所指定的地址（例如 `0xFDD60000`）将直接映射到父总线（SoC 总线）中，即内核或平台可以通过该地址访问这个设备**。


### 5、重新编译内核-实验
- 1 可以看到之前获取失败的打印就消失了，而且成功打印出了reg属性的第一个值

> [root@topeet:~]# `insmod device_tree.ko`
> [   27.138324] device_tree: loading out-of-tree module taints kernel.
> [root@topeet:~]# [   27.140116] my_platform_probe: Probing platform device
> [   27.140153] **reg start is fdd60000**
> [   27.141866] my_platform_driver: Platform driver initialized




### 6、


### 7


# 二、ranges属性

## ranges属性介绍
### 1 、ranges属性作用
> anges 属性是一种用于描述设备之间地址映射关系的属性。它在设备树（Device Tree）中使用，用于**描述子设备地址空间如何映射到父设备地址空间**。设备树是一种硬件描述语言，用于描述嵌入式系统中的硬件组件和它们之间的连接关系。


### 2 、常见的格式
- 1 设备树中的每个设备节点都可以具有 ranges 属性，其中包含了地址映射的信息。

```d
ranges = <child-bus-address parent-bus-address length>;

或者
ranges;
```


#### 参数解述
> hild-bus-address：**子设备地址空间的起始地址**。它指定了子设备在父设备地址空间中的位置。具体的字长由 ranges 所在节点的 #address-cells 属性决定。
> 
> parent-bus-address：**父设备地址空间的起始地址**。它指定了父设备中用于映射子设备的地址范围。具体的字长由 ranges 的父节点的 #address-cells 属性决定。
> 
> length：映射的大小。它指定了**子设备地址空间在父设备地址空间中的长度**。具体的字长由 ranges 的父节点的 #size-cells 属性决定。



> 当` ranges 属性的值为空`时，表示子设备地址空间和父设备地址空间具有完全相同的映射，即**1:1映射**。这通常用于描述内存区域，其中子设备和父设备具有相同的地址范围。
> 
> 当` ranges 属性的值不为空`时，**按照指定的映射规则将子设备地址空间映射**到父设备地址空间。具体的映射规则取决于设备树的结构和设备的特定要求。


### 3 、举例分析
```d
/dts-v1/;
 
/ {
  compatible = "acme,coyotes-revenge";
  #address-cells = <1>;
  #size-cells = <1>;
  ....
  external-bus {
    #address-cells = <2>;
    #size-cells = <1>;
    ranges = <0 0 0x10100000 0x10000
              1 0 0x10160000 0x10000
              2 0 0x30000000 0x30000000>;
    // Chipselect 1, Ethernet
    // Chipselect 2, i2c controller
    // Chipselect 3, NOR Flash
.......
```

> 在 external-bus **节点中#address-cells 属性值为2表示child-bus-address由两个值表示**，也就是0和0，
> **父节点的 # address-cells 属性值和#size-cells 属性值为1，表示parent-bus-address和length都由一个表示**，也就是0x10100000和0x10000

- 1 根据 `ranges` 的结构，可以理解为：
> - 子空间从 child-bus-address = 0x0开始，
> - 映射到父空间的 parent-bus-address = 0x10100000
> - 映射区域长度为 length = 0x10000。
> - 
> 因此，子空间 `0x0 + 0x10000 – 1 = 0xFFFF`，**映射**到父空间 `0x10100000 + 0x10000 – 1 = 0x1010FFFF`。


#### 多个hild-bus-address值的处理问题
```d
ranges =<2 0 0x30000000 0x1000000>;
```
- 1 具体把 child 两格当“CS + 偏移”还是“64 位地址”，要看该总线的 **binding 文档**；对外部总线/EBI，通常是“CS + 偏移”。

- 2 CS（片选） + 偏移
```c
这条 ranges 的 子总线起点 是：CS2 内偏移 0
```



### 4 、总结
> 在嵌入式系统中，**不同的设备可能连接到相同的总线或总线控制器上，它们需要在物理地址空间中进行正确的映射**，以便进行数据交换和通信。例如，一个设备可能通过总线连接到主处理器或其他设备，而这些设备的物理地址范围可能不同。**ranges 属性就是用来描述这种地址映射关系**的。


### 5、


### 6、



## 设备分类
- 1 根据上面讲解的映射关系可以将设备分为两类
### 1 、内存映射型设备：
> 内存映射型设备是指**可以通过内存地址进行直接访问的设备**。
> 这类设备<span style="background:#d3f8b6">在物理地址空间中的一部分被映射到系统的内存地址空间中</span>，使得CPU可以通过读写内存地址的方式与设备进行通信和控制。

#### 特点：
> （1）直接访问：内存映射型设备**可以被CPU直接访问**，类似于访问内存中的数据。这种直接访问方式提供了高速的数据传输和低延迟的设备操作。
> 
> （2）内存映射：设备的<span style="background:#d3f8b6">寄存器、缓冲区等资源被映射到系统的内存地址空间中</span>，使用**读写内存的方式与设备进行通信**。
> 
> （3）读写操作：CPU可以通过读取和写入映射的内存地址来与设备进行数据交换和控制操作。

#### 内存映射型设备的设备树举例
```d
/dts-v1/;
/ {
    #address-cells = <1>;
    #size-cells = <1>;
    ranges;
 
    serial@101f0000 {
        compatible = "arm,pl011";
        reg = <0x101f0000 0x1000>;
    };
 
    gpio@101f3000 {
        compatible = "arm,pl061";
        reg = <0x101f3000 0x1000
                0x101f4000 0x10>;
    };
 
    spi@10115000 {
        compatible = "arm,pl022";
        reg = <0x10115000 0x1000>;
    };
};
```
- 1 第5行的ranges属性表示该设备树中会进行1：1的地址范围映射。


### 2 、非内存映射型设备：
> 非内存映射型设备是指**不能通过内存地址直接访问的设备**。这类设备可能采用其他方式与CPU进行通信，例如<span style="background:#d3f8b6">可通过I/O端口、专用总线或特定的通信协议</span>。

#### 特点：

> （1）非内存访问：非内存映射型设备不能像内存映射型设备那样直接通过内存地址进行访问。它们可能使用独立的I/O端口或专用总线进行通信。
> 
> （2）特定接口：设备通常使用特定的接口和协议与CPU进行通信和控制，例如<span style="background:#d3f8b6">SPI、I2C、UART</span>等。
> 
> （3）驱动程序：非内存映射型设备**通常需要特定的设备驱动程序来实现与CPU的通信和控制**。

#### 非内存映射型设备的设备树举例如下所示：
```d
/dts-v1/;
 
/ {
  compatible = "acme,coyotes-revenge";
  #address-cells = <1>;
  #size-cells = <1>;
  ....
  external-bus {
    #address-cells = <2>;
    #size-cells = <1>;
    ranges = <0 0 0x10100000 0x10000
              1 0 0x10160000 0x10000
              2 0 0x30000000 0x30000000>;
    // Chipselect 1, Ethernet
    // Chipselect 2, i2c controller
    // Chipselect 3, NOR Flash
 
    ethernet@0,0 {
      compatible = "smc,smc91c111";
      reg = <0 0 0x1000>;
    };
 
    i2c@1,0 {
      compatible = "acme,a1234-i2c-bus";
      #address-cells = <1>;
      #size-cells = <0>;
      reg = <1 0 0x1000>;
 
      rtc@58 {
        compatible = "maxim,ds1338";
        reg = <0x58>;
      };
    };
  } ;
}; 
```





### 3 、







## 映射地址计算
### 1 、以上面列举的非内存映射型设备的设备树中的ethernet@0节点为例，计算该网卡设备的映射地址。


### 2 、计算ethernet@0节点的物理起始地址和结束地址
> 首先，找到ethernet@0所在的节点，并查看其reg属性。在给定的设备树片段中，ethernet@0的reg属性为<0 0 0x1000>。在根节点中，#address-cells的值为1，表示地址由一个单元格组成。


> 接下来，根据ranges属性进行地址映射计算。在external-bus节点的ranges属性中，有三个映射条目：
> 第一个映射条目为“`0 0 0x10100000 0x10000`”，表示外部总线的地址范围为0x10100000到0x1010FFFF。**该映射条目的第一个值为0，表示与external-bus节点的第一个子节点**（ethernet@0,0）相关联。
> 
> 第二个映射条目：“1 0 0x10160000 0x10000”，表示外部总线的地址范围为0x10160000到0x1016FFFF。该映射条目的第一个值为1，表示与external-bus节点的第二个子节点（i2c@1,0）相关联。
> 
> 第三个映射条目：“2 0 0x30000000 0x30000000”，表示外部总线的地址范围为0x30000000到0x5FFFFFFF。该映射条目的第一个值为2，表示与external-bus节点的第三个子节点相关联。

> 由于ethernet@0与external-bus的第一个子节点相关联，并且它的reg属性为<0 0 0x1000>，我们可以进行以下计算：


> ethernet@0的**物理起始地址 = 外部总线地址起始值 + ethernet@0的reg属性的第二个值**
> = 0x10100000 + 0x1000
> = 0x10101000
> 因此，ethernet@0的物理起始地址为0x10101000，又**根据0x1000(reg属性的第二个值)的地址范围可以确定ethernet@0的结束地址为0x10101FFF**，至此，关于映射地址的计算就讲解完成了，大家可以根据同样的方法计算i2c@1的物理地址。

### 3 、



### 4 、



# 三、扩展

## 各种地址的了解
### 1 、物理地址（Physical Address）
> - **Definition**：物理地址是直接**映射到硬件主存或内存映射设备（如 MMIO）上的真实地址**，由内存控制器通过地址总线访问。
>     
> - **Usage**：只有系统软件（例如操作系统内核、DMA 控制器等）或 I/O 设备才直接使用物理地址

### 2 、映射地址
> - 在内核或设备驱动中，有时会看到“映射地址”（例如映射到内核虚拟地址空间的物理或 MMIO 区域）。
>     
> - 在 Linux 上，bus address 是设备或外设看到的地址，可能通过设备树中 `ranges` 或 IOMMU 进行了映射。
>     
> - CSDN 上的一篇文章指出，这一类地址是：
>     
>     > **“总线地址：设备看到的地址**”[CSDN博客](https://blog.csdn.net/woyimibayi/article/details/79163179?utm_source=chatgpt.com)
>     
> 
> 也就是说：
> 
> - **物理地址是 CPU 或内存控制器看到的地址；**
> - **总线地址／映射地址则是设备（如 PCIe 设备）通过总线访问时所看到的地址。**



### 3 、虚拟地址 / 内存地址（Virtual / Logical Address）
> - Virtual Address（又称 Logical Address）：这是**程序所使用的地址**，由 CPU 在运行时生成，并由操作系统通过 MMU 转换为物理地址。[GeeksforGeeks](https://www.geeksforgeeks.org/operating-systems/logical-and-physical-address-in-operating-system/?utm_source=chatgpt.com)[图解计算机基础](https://xiaolincoding.com/os/3_memory/vmem.html?utm_source=chatgpt.com)
>     
> - Translation Mechanism：**虚拟地址通过 MMU（Memory Management Unit）和页表映射到物理地址，从而实现地址空间隔离**、多进程并发等功能。[GeeksforGeeks](https://www.geeksforgeeks.org/operating-systems/memory-allocation-techniques-mapping-virtual-addresses-to-physical-addresses/?utm_source=chatgpt.com)[维基百科](https://en.wikipedia.org/wiki/Memory_management_unit?utm_source=chatgpt.com)
>     
> - Advantages：
>     
>     - 各进程拥有独立的地址空间；
>         
>     - 增加安全性与稳定性；
>         
>     - 支持虚拟内存超出物理内存上限。[](https://medium.com/%40karthix25/understanding-memory-management-from-physical-addressing-to-virtual-addressing-65c8ff3ac96b?utm_source=chatgpt.com)


### 4 、区别总结对比表

| 类型       | 所在位置 / 使用主体     | 作用与意义                          |
| -------- | --------------- | ------------------------------ |
| **虚拟地址** | 应用程序 / 操作系统内核   | **CPU 使用的地址，需要通过 MMU 映射到物理地址** |
| **物理地址** | 内存控制器 / 硬件      | **实际访问物理内存或设备寄存器的位置**          |
| **映射地址** | 设备 / 总线 / IOMMU | 用于**设备访问的地址空间**，可能需要映射或翻译      |


### 5、举例说明

> 假设有一个网络设备 `ethernet@0`：
> 
> - 在 Device Tree 中，它的 **`reg` 属性可能表示子总线地址（映射地址）；**
>     
> - **通过 `ranges`，这些地址被映射到 物理地址空间；**
>     
> - 在驱动里，**驱动通常再使用 `ioremap()` 将这些物理地址映射到 内核虚拟地址；**
> - **最终驱动通过该虚拟地址访问设备寄存器**。


### 6、内存地址
> 内存映射型设备（Memory-Mapped I/O，简称 MMIO）才会有“内存地址”这一概念。**这种设备的寄存器或控制区域被映射到系统的虚拟内存空间中，操作系统和驱动程序可以通过指针直接访问这些地址，就像访问普通内存一样**。

### 7、



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


