---
title: "Linux驱动开发笔记（六）中断子系统及实验_linux中断框架-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/139434955?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读1.3k次，点赞24次，收藏23次。本章我们将讲解下和中断相关的知识，了解内核中断的框架和中断的概念，对于arm的中断控制器(GIC v3)相关内容，主要是借鉴参考手册简单解释下。_linux中断框架"
tags:
  - "clippings"
---
---

## 前言

  本章我们将讲解下和中断相关的知识，了解内核中断的框架和中断的概念，对于 [arm](https://so.csdn.net/so/search?q=arm&spm=1001.2101.3001.7020) 的中断控制器(GIC v3)相关内容，主要是借鉴参考手册简单解释下。

---

## 一、中断子系统框架

Linux 中的中断相似于之前STM32的中断，是 硬件 在需要时向CPU发出的一种信号，导致CPU暂时停止当前正在执行的程序，转而处理这个硬件请求的一种机制。  
  中断发生在CPU正常运行期间，由于内外部事件或由程序预先安排的事件引起的CPU暂时停止正在运行的程序，转而去为该内部或外部事件或预先安排的事件服务，服务完毕后再返回继续执行原来的程序。

### 1\. 中断硬件简单描述

  中断硬件主要有三种器件参与，各个外设、中断控制器和CPU。之间的关系可以简单看下下面图片：  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c34b75e13017229bb4b9ee660f9a895d.png)

### 2\. 中断的软件描述

  一个完整的中断子系统框架可以分为四个层次，由上到下分别为用户层、通用层、硬件相关层和硬件层，每个层相关的介绍如下所示：

- 用户层：用户层是中断的使用者，主要包括各类设备驱动。这些驱动程序通过中断相关的接口进行中断的申请和注册。当外设触发中断时，用户层驱动程序会进行相应的回调处理，执行特定的操作。
- 通用层：通用层也可称为框架层，它是硬件无关的层次。通用层的代码在所有硬件平台上都是通用的，不依赖于具体的硬件架构或中断控制器。通用层提供了统一的接口和功能，用于管理和处理中断，使得驱动程序能够在不同的硬件平台上复用。
- 硬件相关层：硬件相关层包含两部分代码。一部分是与特定处理器架构相关的代码，比如ARM64处理器的中断处理相关代码。这些代码负责处理特定架构的中断机制，包括中断向量表、中断处理程序等。另一部分是中断控制器的驱动代码，用于与中断控制器进行通信和配置。这些代码与具体的中断控制器硬件相关。
- 硬件层：硬件层位于最底层，与具体的硬件连接相关。它包括外设与SoC（系统片上芯片）的物理连接部分。中断信号从外设传递到中断控制器，由中断控制器统一管理和路由到处理器。硬件层的设计和实现决定了中断信号的传递方式和硬件的中断处理能力。

## 二、GIC v3中断控制器

  ARM多核处理器里最常用的中断控制器是GIC， GIC是Generic Interrupt Controller的缩写，提供了灵活的和可扩展的中断管理方法，支持单核系统到数百个大型多芯片设计的核心。 主要作用就是接受硬件中断信号，通过一定的设置策略，然后分发给对应的CPU进行处理。  
  GIC v3中断控制器是ARM公司推出的一款与cortex-A和cortex-R处理器配合使用的中断控制器，广泛应用于基于armv8的SOC设计中。GIC v3为CPU处理所有连接到其上的中断，包括管理所有的中断源、中断行为、中断分组以及中断路由方式等。同时，它还提供相应的寄存器接口用于软件对这些行为的控制。

### 1\. GIC v3基本结构

  GIC v3包含了SPI（Shared Peripheral Interrupt）、PPI（Private Peripheral Interrupt）、SGI（Software Generated Interrupt）和LPI（Locality-Specific Peripheral Interrupt）四种中断类型，以及distributor、redistributor、ITS（Interrupt Translation Service）和CPU interface四大 组件 。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/63341f1a17551c5874dd11dd1652fe18.png)  
   GIC v3中，将cpu interface从GIC中抽离，放入到了cpu中，cpu interface通过AXI Stream，与gic进行通信。 当GIC要发送中断，GIC通过AXI stream接口，给cpu interface发送中断命令，cpu interface收到中断命令后，根据中断线映射配置，决定是通过IRQ还是FIQ管脚，向cpu发送中断。

#### 1.1 Distributor

  Distributor是GIC v3中用于管理共享外设中断（SPI）的关键组件。它负责接收来自外设的SPI中断请求，并根据配置决定中断的优先级以及将中断路由到哪个Redistributor。

- 关键特性：
	- 中断分发：Distributor根据中断的优先级、亲和性（affinity）等配置，将SPI中断路由到适当的Redistributor。
	- 优先级管理：Distributor为每个SPI中断设置优先级，确保高优先级的中断能够优先得到处理。
	- 中断状态管理：Distributor维护中断的状态信息，如中断是否激活、是否挂起等。
- 寄存器接口：
	- GICD\_系列寄存器（如GICD\_ISENABLER、GICD\_ICENABLER、GICD\_IPRIORITYR等）用于配置Distributor的行为，包括启用/禁用中断、设置中断优先级等。

#### 1.2 Redistributor

  Redistributor与CPU接口连接，负责将来自Distributor的中断路由到正确的CPU。在多核系统中，Redistributor确保中断被正确地分发到目标CPU或CPU组。

- 关键特性：
	- 中断路由：Redistributor根据配置将中断路由到相应的CPU接口。
	- 亲和性管理：Redistributor支持中断的亲和性配置，允许中断被路由到特定的CPU或CPU组。
- 寄存器接口：
	- GICR\_系列寄存器（如GICR\_ISENABLER、GICR\_ICENABLER等）用于配置Redistributor的行为，包括启用/禁用中断、设置中断路由等。

#### 1.3 ITS

  ITS是GIC v3中用于处理基于消息的中断（LPI）的组件。它提供LPI中断的转换服务，将来自虚拟中断源的LPI中断转换为物理中断源，并将其路由到适当的Redistributor。

- 关键特性：
	- 中断转换：ITS将LPI中断转换为物理中断，以便在物理世界中进行处理。
	- 中断路由：ITS负责将LPI中断路由到正确的Redistributor。

#### 1.4 CPU interface

  CPU interface是GIC v3与CPU之间的接口，负责将中断传递到它所连接到的处理器元素（PE，即CPU）。当Redistributor将中断路由到某个CPU接口时，该接口会将中断信号发送到相应的CPU。

- 关键特性：
	- 中断传递：CPU interface将来自Redistributor的中断信号传递给CPU。
	- 中断状态管理：CPU interface可能还负责维护中断的状态信息，如中断是否已被CPU接收、是否正在处理等。

### 2\. 中断类型与特点

- SPI：共享外设中断，不与特定的CPU绑定，可以根据affinity配置被路由到任意CPU或一组特定的CPU上。
- PPI：私有外设中断，每个处理器私有的中断类型，即一个特定的中断只会被路由到特定的处理器上。
- SGI：软件生成中断，没有实际的物理连线，而是由软件通过写寄存器方式触发，只支持边沿触发。
- LPI：基于消息的中断，LPI相关的配置保存在内存中而非寄存器。

| NTID范围 | 中断类型 | 备注 |
| --- | --- | --- |
| 0 - 15 | SGI（软件生成中断） 文本居右 | 每个核心分别存储 |
| 16 - 31 | PPI（私有外设中断） | 每个核心分别存储 |
| 32 - 1019 | SPI（共享外设中断） |  |
| 1020 - 1023 | 特殊中断号 | 用于表示特殊情况 |
| 1024 - 8191 | 保留 |  |
| 8192及更大 | LPI（特定局部外设中断） | 上限由实现定义 |

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7023832bda19da21b75a0afa845a115c.png)

- Inactive（非活动状态）：中断源当前未被触发。
- Pending（等待状态）：中断源已被触发，但尚未被处理器核心确认。
- Active（活动状态）：中断源已被触发，并且已被处理器核心确认。
- Active and Pending（活动且等待状态）：已确认一个中断实例，同时另一个中断实例正在等待处理。

每个外设中断可以是以下两种类型之一：

- 边沿触发（Edge-triggered）：  
	这是一种在检测到中断信号上升沿时触发的中断，然后无论信号状态如何，都保持触发状态，直到满足本规范定义的条件来清除中断。
- 电平触发（Level-sensitive）：  
	这是一种在中断信号电平处于活动状态时触发的中断，并且在电平不处于活动状态时取消触发。

### 3\. 中断号

  在 [linux 内核](https://so.csdn.net/so/search?q=linux%20%E5%86%85%E6%A0%B8&spm=1001.2101.3001.7020) 中，我们使用IRQ number和HW interrupt ID两个ID来标识一个来自外设的中断：

- IRQ number：CPU需要为每一个外设中断编号，我们称之IRQ Number。这个IRQ number是一个虚拟的interrupt ID，和硬件无关，仅仅是被CPU用来标识一个外设中断。
- HW interrupt ID：对于GIC中断控制器而言，它收集了多个外设的interrupt request line并向上传递，因此，GIC中断控制器需要对外设中断进行编码。GIC中断控制器用HW interrupt ID来标识外设的中断。如果只有一个GIC中断控制器，那IRQ number和HW interrupt ID是可以一一对应的，如下图所示：  
	![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ac4fa3674ec21ff68cd2b5c5fbd52210.png)  
	  但如果是在GIC中断控制器级联的情况下，仅仅用HW interrupt ID就不能唯一标识一个外设中断，还需要知道该HW interrupt ID所属的GIC中断控制器（HW interrupt ID在不同的Interrupt controller上是会重复编码的）。

## 三、函数编写

### 3.1 相关API函数

| 函数名 | 描述 |
| --- | --- |
| irq\_of\_parse\_and\_map( ) | 解析得到软中断号 |
| request\_irq( ) | 注册中断 |
| devm\_request\_irq( ) | 注册中断,申请的是内核“managed”的资源 |
| free\_irq( ) | 释放中断 |
| \*irq\_handler\_t( ) | 指定一个中断处理函数 |
| enable\_irq( ) | 中断的使能 |
| disable\_irq( ) | 中断的屏蔽 |
| gpio\_to\_irq( ) | 将 GPIO 引脚映射到对应中断号的函数 |

```c
//解析得到软中断号
unsigned int irq_of_parse_and_map(struct device_node *np, int index)
12
```
- 参数：
	- np:节点指针
	- index:设备树节点中interrupts键对应值的下标
- 返回值：成功返回软中断号，失败返回0
```c
//注册中断
static inline int __must_check request_irq(unsigned int irq, irq_handler_t 
    handler,unsigned long flags, const char *name, void *dev);
123
```
- 参数：
	- irq:软中断号(内核中用到的中断号全部都是软中断号)（设备树获取）
	- handler:中断处理函数指针
	- flags:中断触发方式
		- IRQF\_TRIGGER\_RISING //上升沿
		- IRQF\_TRIGGER\_FALLING //下降沿
		- IRQF\_TRIGGER\_HIGH //高电平
		- IRQF\_TRIGGER\_LOW //低电平
		- IRQF\_SHARED //共享中断
	- name:中断的名字  
		cat /proc/interrupts 命令查看(设备号的查看方式 cat /proc/device)
	- dev:给中断处理函数传递的参数
- 返回值：成功返回0，失败返回错误码

  此函数与request\_irq()的区别是devm\_开头的API申请的是内核“managed”的资源，一般不需要在出错处理和 remove()接口里再显式的释放。

```c
int devm_request_irq(struct device *dev, unsigned int irq, irq_handler_t 
    handler,unsigned long irqflags, const char *devname, void *dev_id);
12
```
- 参数：
	- dev：指向您的设备的 struct device 结构体指针。这个结构体包含了设备的各种信息，并且允许设备管理器跟踪与该设备相关的所有资源。
	- irq：要请求的中断号。
	- handler：当中断触发时要调用的处理函数。
	- irqflags：标志位，用于指定中断处理函数的行为，如 IRQF\_SHARED 允许多个处理程序共享同一个中断。
	- devname：与中断关联的名称，通常用于调试和日志记录。
	- dev\_id：传递给中断处理函数的参数，允许您在中断处理程序中区分不同的中断源或设备实例。
- 返回值：
	- 如果成功请求了中断，则返回 0。
	- 如果失败（例如，由于中断号无效、中断已被占用且未标记为可共享等），则返回负的错误码。

**注：这里简单介绍一下中断处理函数指针**

```c
//typedef irqreturn_t (*irq_handler_t)(int, void *);
irqreturn_t key_irq_handle(int irqno,void *dev)
{
   //中断的处理---中断处理函数中不能加延时耗时的操作
    return IRQ_NONE;    //失败
    return IRQ_HANDLED; //成功
}
1234567
```
```c
//释放中断
const void *free_irq(unsigned int irq, void *dev_id);
12
```
- 参数：
	- irq:软中断号
	- dev\_id:给中断处理函数传递的参数
- 返回值:返回设备的名字
```c
//在中断申请时需要指定一个中断处理函数
irqreturn_t (*irq_handler_t)(int irq, void * dev);
12
```
- 参数：
	- int irq：表示触发中断的中断号（IRQ number）
	- void \*dev：一个指向任何类型数据的指针，通常由 request\_irq 或 devm\_request\_irq 函数的调用者提供，并传递给中断处理函数。这个指针通常用于传递与中断相关的设备或驱动程序的上下文信息
- 返回值：
	- irqreturn\_t类型：枚举类型变量
		- IRQ\_NONE(0 << 0)： 中断没有被处理
		- IRQ\_HANDLED (1 << 0)：中断被成功处理
		- IRQ\_WAKE\_THREAD(1 << 1)：在中断服务函数是使用“上半部分”和“下半部分”实现
```c
//中断的屏蔽和使能
void enable_irq(unsigned int irq);
void disable_irq(unsigned int irq);
123
```
- 参数：
	- irq：指定的“内核中断号”
- 返回值：无
```c
//将 GPIO 引脚映射到对应中断号的函数,它的作用是根据给定的 GPIO 引脚号，获取与之关联的中断号。
#include <linux/gpio.h>
unsigned int gpio_to_irq(unsigned int gpio);
123
```
- 参数：
	- gpio：要映射的 GPIO 引脚号。
- 返回值：
	- 成功：返回值为该 GPIO 引脚所对应的中断号。
	- 失败：返回值为负数，表示映射失败或无效的 GPIO 引脚号。

### 3.2 驱动初始化函数

```c
static int __init button_driver_init(void)
{
    int error = -1;

    //采用动态分配的方式，获取设备编号，次设备号为0，
    error = alloc_chrdev_region(&button_devno, 0, DEV_CNT, DEV_NAME);
    if (error < 0)
    {
        printk("fail to alloc button_devno\n");
        goto alloc_err;
    }

    //关联字符设备结构体cdev与文件操作结构体file_operations
    button_chr_dev.owner = THIS_MODULE;
    cdev_init(&button_chr_dev, &button_chr_dev_fops);

    //添加设备至cdev_map散列表中
    error = cdev_add(&button_chr_dev, button_devno, DEV_CNT);
    if (error < 0) 
    {
        printk("fail to add cdev\n");
        goto add_err;
    }

    class_button = class_create(THIS_MODULE, DEV_NAME); //创建类
    //创建设备 DEV_NAME 指定设备名
    device_button = device_create(class_button, NULL, button_devno, NULL, DEV_NAME);

    return 0;

add_err:
    // 添加设备失败时，需要注销设备号
    unregister_chrdev_region(button_devno, DEV_CNT);    
    printk("\n error! \n");
    
alloc_err:
    return -1;
}

123456789101112131415161718192021222324252627282930313233343536373839
```

### 3.3 operations函数

#### 3.3.1 open函数

```c
static int button_open(struct inode *inode, struct file *filp)
{
    int res = -1;

    //获取按键 设备树节点
    button_device_node = of_find_node_by_path("/button_interrupt");
    if(NULL == button_device_node)
    {
            printk("of_find_node_by_path error!");
            return -1;
    }

    //获取按键使用的GPIO
    button_GPIO_number = of_get_named_gpio(button_device_node ,"button-gpios", 0);
    if(0 == button_GPIO_number)
    {
            printk("of_get_named_gpio error");
            return -1;
    }

    //申请GPIO，记得释放
    res = gpio_request(button_GPIO_number, "button_gpio");
    if(error < 0)
    {
            printk("gpio_request error");
            gpio_free(button_GPIO_number);
            return -1;
    }
    
    //设置为输入模式
    res = gpio_direction_input(button_GPIO_number);

    //获取中断号
    interrupt_number = irq_of_parse_and_map(button_device_node, 0);
    printk("\n interrupt_number =  %d \n",interrupt_number);

    //申请中断, 记得释放
    res = request_irq(interrupt_number,button_irq_hander,IRQF_TRIGGER_RISING,"button_interrupt",NULL);
    if(error != 0)
    {
            printk("request_irq error");
            free_irq(interrupt_number, NULL);
            return -1;
    }
    return 0;
}
12345678910111213141516171819202122232425262728293031323334353637383940414243444546
```

#### 3.3.2.read

```c
static int button_read(struct file *filp, char __user *buf, size_t cnt, loff_t *offt)
{
    int error = -1;
    int button_countervc = 0;

    //读取按键状态值
    button_countervc = atomic_read(&button_status);

    //结果拷贝到用户空间
    error = copy_to_user(buf, &button_countervc, sizeof(button_countervc));
    if(error < 0)
    {
            printk_red("copy_to_user error");
            return -1;
    }
    //清零按键状态值
    atomic_set(&button_status,0);
    return 0;
}
12345678910111213141516171819
```

#### 3.3.3.release

```c
static int button_release(struct inode *inode, struct file *filp)
{
    
    //释放申请的引脚,和中断
    gpio_free(button_GPIO_number);
    free_irq(interrupt_number, device_button);
    printk("release over!");
    return 0;
}
123456789
```

### 3.4 中断函数

```c
//定义整型原子变量，保存按键状态 ，设置初始值为0
atomic_t   button_status = ATOMIC_INIT(0);  

static irqreturn_t button_irq_hander(int irq, void *dev_id)
{
    printk("hander has entered!");
    //按键状态加一
    atomic_inc(&button_status);
    return IRQ_HANDLED;
}
12345678910
```

## 四、设备树的编辑

### 1\. 设备树插件格式

  设备树插件（Device Tree Overlay）是一种用于设备树（Device Tree）的扩展机制，它在Linux内核的 嵌入式系统 中发挥着重要作用。设备树插件允许在运行时动态修改设备树的内容，以便添加、修改或删除设备节点和属性。它提供了一种灵活的方式来配置和管理硬件设备，而无需重新编译整个设备树。通过使用设备树插件，开发人员可以在不重新启动系统的情况下对硬件进行配置更改。

```bash
#用于指定dts的版本
 /dts-v1/;
 
#表示允许使用未定义的引用并记录它们，设备树插件中可以引用主设备树中的节点
#这些“引用的节点”对于设备树插件来说就是未定义的，所以设备树插件应该加上“/plugin/”
/plugin/;

&{/} {
    /*此处在根节点"/"下,添加要插入的节点或者属性*/
};

&XXXXX {
    /*此处在节点"XXXXX"下,添加要插入的节点或者属性*/
};
    .......
123456789101112131415
```

### 2\. 设备树插件的编写

```bash
#触发方式
#define IRQ_TYPE_NONE           0
#define IRQ_TYPE_EDGE_RISING    1
#define IRQ_TYPE_EDGE_FALLING   2
#define IRQ_TYPE_EDGE_BOTH      (IRQ_TYPE_EDGE_FALLING | IRQ_TYPE_EDGE_RISING)
#define IRQ_TYPE_LEVEL_HIGH     4
#define IRQ_TYPE_LEVEL_LOW      8

&{/} {
        #新增的button_interrupt节点
        button_interrupt: button_interrupt {
            status = "okay";
            compatible = "button_interrupt";
            #配置按键引脚
            button-gpios = <&gpio0 RK_PB0 GPIO_ACTIVE_LOW>;
            #插件按键引脚的复用信息
            pinctrl-names = "default";
            pinctrl-0 = <&button_interrupt_pin>;
            #表示父中断控制节点是gpio0
            interrupt-parent = <&gpio0>;
            #表示中断引脚，触发方式
            interrupts = <RK_PB0 IRQ_TYPE_LEVEL_LOW>;
        };
    };

&{/pinctrl} {
    pinctrl_button {
        button_interrupt_pin: button_interrupt_pin {
            rockchip,pins = <0 RK_PB0 RK_FUNC_GPIO &pcfg_pull_none>;
        };
    };
};
1234567891011121314151617181920212223242526272829303132
```

**免责声明：本文参考了野火的部分资料，仅供学习参考使用，若有侵权或勘误请联系笔者。**

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/139434955

作者主页：https://blog.csdn.net/sincerelover

实付 元

[使用余额支付](https://blog.csdn.net/sincerelover/article/details/)

点击重新获取

扫码支付

钱包余额 0

抵扣说明：

1.余额是钱包充值的虚拟货币，按照1:1的比例进行支付金额的抵扣。  
2.余额无法直接购买下载，可以购买VIP、付费专栏及课程。

[余额充值](https://i.csdn.net/#/wallet/balance/recharge)

举报

![程序员都在用的中文IT技术交流社区](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_app.png)

程序员都在用的中文IT技术交流社区

程序员都在用的中文IT技术交流社区

![专业的中文 IT 技术社区，与千万技术人共成长](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_wechat.png)

专业的中文 IT 技术社区，与千万技术人共成长

专业的中文 IT 技术社区，与千万技术人共成长

![关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_video.png)

关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！

关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！

客服 返回顶部