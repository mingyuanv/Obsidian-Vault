---
title: Linux SD卡驱动开发(二) —— SD 卡驱动分析HOST篇-CSDN博客
source: https://blog.csdn.net/zqixiao_09/article/details/51039595
author: 
published: 
created: 2025-04-15
description: 文章浏览阅读2.5w次，点赞35次，收藏134次。本文详细探讨了Linux系统中SD卡驱动的HOST部分，包括mmc_host结构体的描述、初始化过程、设备注册和功能函数。重点分析了mmc_host_ops在SD卡控制器驱动中的作用，以及中断处理和数据传输的实现。内容涉及mmc_add_host函数、中断注册和响应，为理解SD卡驱动的底层工作机制提供了深入见解。
tags:
  - clippings
---
# 随记：





# 回顾一下前面的知识
MMC 子系统范围三个部分：

<span style="background:#b1ffff">**HOST 部分** 是针对不同主机的驱动程序，这一部是驱动程序工程师需要根据自己的特点平台来完成的。</span>

**CORE 部分**: 这是整个MMC 的核心存，这部分完成了不同协议和规范的实现，并为HOST 层的驱动提供了接口 函数 。

**CARD 部分** ：因为这些记忆卡都是块设备，当然需要提供块设备的驱动程序，这部分就是实现了将你的SD 卡如何实现为块设备的。

它们分布于下面的文件夹中 Linux /drivers/mmc中

![](https://img-blog.csdn.net/20160401215304831?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)  

其中，<span style="background:#affad1">card（区块层） 与core（核心层）是linux系统封装好了部分，我们不需要修改</span>，host（主控制器层）中提供与各芯片构架相关的文件，这才是我们所要开发的部分

核心层根据需要构造各种MMC/SD命令， 这些命令怎么发送给MMC/SD卡呢？这通过主机控制器层来实现 。这层是架构相关的，里面针对各款CPU提供一个文件，目前支持的CPU还很少。

以本节即将移植的s3cmci.c为例，它首先进行一些低层设置，比如 设置MMC/SD/SDIO控制器使用到的CPIO引脚 、 使能控制器 、 注册中断处理函数 等，然后向上面的核心层增加一个主机（Host），这样核心层就能调用s3cmci.c提供的函数来识别、使用具体存储卡了。

<span style="background:#b1ffff">在向核心层增加主机之前，s3cmci.c 设置了一个 mmc\_host\_ops结构体</span> ，它实现两个函数：

<span style="background:#affad1">**a -- 发起访问请求的request函数**</span>

<span style="background:#affad1">**b --** **进行一些属性设置（时钟频率、数据线位宽等）的set\_ios函数** 。</span>

下面列出识别存储卡、区块层发起操作请求两种情况下函数的主要调用关系：

**1）识别存储卡**

 **![](https://img-blog.csdn.net/20160402153829762?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center) ![](https://img-blog.csdn.net/20160402153936887?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)**

**2）区块层发起操作请求**

**![](https://img-blog.csdn.net/20160402154214373?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)  
**

以后上次对存储卡的操作都通过调用这两个函数来完成<span style="background:#fdbfff">。下面对HOST层进行分析（ **Linux内核版本:Linux-3.14** ）。</span>

# **一、struct mmc\_host 结构体（？？？？）**

主要用来描述卡控制器位 ， **结构体mmc\_host** 定义于/include/linux/mmc/host.c，可以认为是linux<span style="background:#d3f8b6">为SD卡控制器专门准备的一个类</span>，该类里面的成员是所有SD卡控制器都需要的，放之四海而皆准的数据结构，在本例芯片控制器的驱动程序s3cmci.c中，则 **为该类具体化了一个对象`struct mmc_host *mmc，`此mmc指针即指代着该ARM芯片SD卡控制器的一个 **具体化对象** （可以看出虽然C是面向过程的语言，但还是用到了一些面向对象思想的）。

在 linux/driver/mmc/host/s3cmci.h 下定义

```cpp
struct s3cmci_host {

    struct platform_device    *pdev;

    struct s3c24xx_mci_pdata *pdata;

    struct mmc_host        *mmc;

    struct resource        *mem;

    struct clk        *clk;

    void __iomem        *base;

    int            irq;

    int            irq_cd;

    int            dma;

 

    unsigned long        clk_rate;

    unsigned long        clk_div;

    unsigned long        real_rate;

    u8            prescaler;

 

    int            is2440;

    unsigned        sdiimsk;

    unsigned        sdidata;

    int            dodma;

    int            dmatogo;

 

    bool            irq_disabled;

    bool            irq_enabled;

    bool            irq_state;

    int            sdio_irqen;

 

    struct mmc_request    *mrq;

    int            cmd_is_stop;

 

    spinlock_t        complete_lock;

    enum s3cmci_waitfor    complete_what;

 

    int            dma_complete;

 

    u32            pio_sgptr;

    u32            pio_bytes;

    u32            pio_count;

    u32            *pio_ptr;

#define XFER_NONE 0

#define XFER_READ 1

#define XFER_WRITE 2

    u32            pio_active;

 

    int            bus_width;

 

    char             dbgmsg_cmd[301];

    char             dbgmsg_dat[301];

    char            *status;

 

    unsigned int        ccnt, dcnt;

    struct tasklet_struct    pio_tasklet;

 

#ifdef CONFIG_DEBUG_FS

    struct dentry        *debug_root;

    struct dentry        *debug_state;

    struct dentry        *debug_regs;

#endif

 

#ifdef CONFIG_CPU_FREQ

    struct notifier_block    freq_transition;

#endif

};
```

其中 **struct mmc\_host** （linux/include/linux/mmc/host.h) **用于与core层的命令请求，数据 传输等信息,**这里代码较长，展示部分

```cpp
struct mmc_host 

{

    const struct mmc_host_ops *ops;     // SD卡主控制器的操作函数，即该控制器所具备的驱动能力

    const struct mmc_bus_ops *bus_ops; // SD总线驱动的操作函数，即SD总线所具备的驱动能力

    struct mmc_ios  ios;  // 配置时钟、总线、电源、片选、时序等

    struct mmc_card  *card;  // 连接到此主控制器的SD卡设备

    ... ...

};
```

本文中 struct mmc\_host\_ops \*ops 定义

```cpp
static struct mmc_host_ops s3cmci_ops = {

    .request    = s3cmci_request,

    .set_ios    = s3cmci_set_ios,

    .get_ro        = s3cmci_get_ro,

    .get_cd        = s3cmci_card_present,

    .enable_sdio_irq = s3cmci_enable_sdio_irq,

};
```
  
  

# 二、SD控制器之初始化（linux/driver/mmc/host）

这一层讲述 硬件 与硬件之间将要发生的故事，也是最底层驱动的核心。通常所谓的驱动程序设计的任务将落实到这一层上，所以关注host故事的发展也将成为移植整个SD类设备驱动的核心。在host 目录中有各种平台下SD 卡主机驱动器的实例，这里我们选择s3c2440平台作为分析的重点。参看Kconfig和Makefile即可获得相应信息，这里对应的文件即是s3cmci.c。

**1、设备的注册**

旧瓶装新酒，还是那个module\_init，不一样的是其中的入口函数。在s3cmci.c中对应的是 **module\_init(s3cmci\_init)**;

```cpp
module_platform_driver(s3cmci_driver);
```

这里是不是很奇怪，不应该是module\_init 与 module\_exit 吗？module\_platform\_driver其实是一个宏定义，定义在 include/linux/platform\_device.h 文件中：

```cpp
/* module_platform_driver() - Helper macro for drivers that don't do

 * anything special in module init/exit.  This eliminates a lot of

 * boilerplate.  Each module may only use this macro once, and

 * calling it replaces module_init() and module_exit()

 */

#define module_platform_driver(__platform_driver) \

    module_driver(__platform_driver, platform_driver_register, \

            platform_driver_unregister)
```

宏module\_driver定义在 include/linux/device.h 文件中，其内容如下：

```cpp
/**

 * module_driver() - Helper macro for drivers that don't do anything

 * special in module init/exit. This eliminates a lot of boilerplate.

 * Each module may only use this macro once, and calling it replaces

 * module_init() and module_exit().

 *

 * @__driver: driver name

 * @__register: register function for this driver type

 * @__unregister: unregister function for this driver type

 * @...: Additional arguments to be passed to __register and __unregister.

 *

 * Use this macro to construct bus specific macros for registering

 * drivers, and do not use it on its own.

 */

#define module_driver(__driver, __register, __unregister, ...) \

static int __init __driver##_init(void) \

{ \

    return __register(&(__driver) , ##__VA_ARGS__); \

} \

module_init(__driver##_init); \

static void __exit __driver##_exit(void) \

{ \

    __unregister(&(__driver) , ##__VA_ARGS__); \

} \

module_exit(__driver##_exit);
```
可以看出，最终还是调用 **module\_init 与 module\_exit** 。这里注册了一个平台驱动，这个前面分析的串口驱动等是一样的原理。这是新版内核中引入的一个虚拟的平台总线。对应的平台设备早在内核启动时通过platform\_add\_devices加入到了内核，相关的具体内容前面已经分析的挺多了，这里就不在详细说明。 **该句调用的结果会导致s3cmci\_driver中的probe方法得以调用** ，由此也就把我们引入了host的世界。

**2、probe函数**

在驱动的接口函数中s3cmci\_probe() 函数， **用于分配mmc\_host ，s3cmci\_host结构体** ，并对结构体进行设置 ， 在SDI主机控制器操作接口函数 **mmc\_host\_ops** 中会调用s3cmci\_host结构体，申请中断并设置中断服务函数，将结构体mmc\_host添加到主机。

SD主控制器驱动程序的初始化函数probe(struct platform\_device \*pdev)，概括地讲，主要完成五大任务，

- 初始化设备的数据结构，并将数据挂载到pdev->dev.driver\_data下
- **实现设备驱动的功能函数，如mmc->ops = &s3cmci\_ops**;
- **申请中断函数request\_irq()**
- 注册设备，即注册kobject，建立sys文件，发送uevent等
- 其他需求，如在/proc/driver下建立用户交互文件等

首先还是来大致看一下s3cmci\_driver中所对应的具体内容

```cpp
static struct platform_driver s3cmci_driver = {

    .driver    = {

        .name    = "s3c-sdi",

        .owner    = THIS_MODULE,

    },

    .id_table    = s3cmci_driver_ids,

    .probe        = s3cmci_probe,

    .remove        = s3cmci_remove,

    .shutdown    = s3cmci_shutdown,

};
```
其中probe是我们关注的核心，由于host与硬件是直接相关的， **probe接下来将做部分关于硬件初始化的工作** ，因此在分析下面一部分代码之前，最好能对s3c2440的sdi相关的内容有所了解。下面进入到probe的相关内容，整个函数洋洋洒洒三百多行，就分段说明吧。  

先看这几行

```cpp
static int s3cmci_probe(struct platform_device *pdev)

{

    struct s3cmci_host *host;

    struct mmc_host    *mmc;

    int ret;

    int is2440;

    int i;

 

    is2440 = platform_get_device_id(pdev)->driver_data;

 

    mmc = mmc_alloc_host(sizeof(struct s3cmci_host), &pdev->dev);

    if (!mmc) {

        ret = -ENOMEM;

        goto probe_out;

    }
```

这里， **mmc = mmc\_alloc\_host(sizeof(struct s3cmci\_host), &pdev->dev);****分配一个mmc的控制器** ， 同时struct s3cmci\_host 结构作为一个私有数据类型将添加到struct mmc\_host的private域 。

**a -- mmc\_alloc\_host**  

mmc\_alloc\_host相应的代码如下： linux/drivers/mmc/core/host.c

```cpp
struct mmc_host *mmc_alloc_host(int extra, struct device *dev)

{

    int err;

    struct mmc_host *host;

 

    host = kzalloc(sizeof(struct mmc_host) + extra, GFP_KERNEL);

    if (!host)

        return NULL;

 

    /* scanning will be enabled when we're ready */

    host->rescan_disable = 1;

    idr_preload(GFP_KERNEL);

    spin_lock(&mmc_host_lock);

    err = idr_alloc(&mmc_host_idr, host, 0, 0, GFP_NOWAIT);

    if (err >= 0)

        host->index = err;

    spin_unlock(&mmc_host_lock);

    idr_preload_end();

    if (err < 0)

        goto free;

 

    dev_set_name(&host->class_dev, "mmc%d", host->index);

 

    host->parent = dev;

    host->class_dev.parent = dev;

    host->class_dev.class = &mmc_host_class;

    device_initialize(&host->class_dev);

 

    mmc_host_clk_init(host);

 

    mutex_init(&host->slot.lock);

    host->slot.cd_irq = -EINVAL;

 

    spin_lock_init(&host->lock);

    init_waitqueue_head(&host->wq);

    INIT_DELAYED_WORK(&host->detect, mmc_rescan);

#ifdef CONFIG_PM

    host->pm_notify.notifier_call = mmc_pm_notify;

#endif

 

    /*

     * By default, hosts do not support SGIO or large requests.

     * They have to set these according to their abilities.

     */

    host->max_segs = 1;

    host->max_seg_size = PAGE_CACHE_SIZE;

 

    host->max_req_size = PAGE_CACHE_SIZE;

    host->max_blk_size = 512;

    host->max_blk_count = PAGE_CACHE_SIZE / 512;

 

    return host;

 

free:

    kfree(host);

    return NULL;

}
```
14行是内核的高效搜索树，将host->index与host结构相关联，方便以后查找。  
24-27行主要是初始化host->class\_dev，这个日后会通过device\_register注册进系统。  
35行前面已经在这个等待队列上花了不少笔墨，主要是同步对host资源的竞争的。  
45-50行这些个都是设置host的一些属性的，是与block.c中请求队列的设置相对应的。  
  
重新回到s3cmci\_probe....
```cpp
for (i = S3C2410_GPE(5); i <= S3C2410_GPE(10); i++) {

        ret = gpio_request(i, dev_name(&pdev->dev));

        if (ret) {

            dev_err(&pdev->dev, "failed to get gpio %d\n", i);

 

            for (i--; i >= S3C2410_GPE(5); i--)

                gpio_free(i);

 

            goto probe_free_host;

        }

    }
```

上面这一段 申请SD卡驱动器所需的GPIO资源 。

继续分析...

```cpp
host = mmc_priv(mmc);

    host->mmc     = mmc;

    host->pdev    = pdev;

    host->is2440    = is2440;
```
上面这段代码就是 **对struct s3cmci\_host \*host这个 私有结构 的配置** ， **对于core或block层见到的只有struct mmc\_host** 。 从另外的一个角度可以理解struct mmc\_host实际上是struct s3cmci\_host的 **基类** ，有着所有控制器所必须具有的属性。struct s3cmci\_host还 **包含了与host硬件平台相关的特征** 。
```cpp
host->pdata = pdev->dev.platform_data;

    if (!host->pdata) {

        pdev->dev.platform_data = &s3cmci_def_pdata;

        host->pdata = &s3cmci_def_pdata;

    }
```

这是 **平台设备注册时platform\_device所具有的属性**.

```cpp
spin_lock_init(&host->complete_lock);

    tasklet_init(&host->pio_tasklet, pio_tasklet, (unsigned long) host);
```

tasklet就象一个 **内核定时器,** 在一个"软中断"的上下文中执行(以原子模式),常用在硬件中断处理中，使得可以使得复杂的任务安全地延后到以后的时间处理。t ask\_init 建立一个tasklet，然后调用函数 tasklet\_schedule将这个tasklet放在 tasklet\_vec链表的头部，并唤醒后台线程 ksoftirqd 。当后台线程ksoftirqd 运行调用\_\_do\_softirq 时，会执行在中断向量表softirq\_vec里中断号TASKLET\_SOFTIRQ对应的 tasklet\_action函数，然后 tasklet\_action遍历 tasklet\_vec链表，调用每个 tasklet的函数完成软中断操作，上面例子中即是pio\_tasklet函数，另外软中断处理函数只能传递一个long型变量。这里是直接使用 **host的地址** ，作为传递参数。关于这个pio\_tasklet现在说他还为时过早，等时辰一到自然会对他大书特书。

```cpp
if (is2440) {

        host->sdiimsk    = S3C2440_SDIIMSK;

        host->sdidata    = S3C2440_SDIDATA;

        host->clk_div    = 1;

    } else {

        host->sdiimsk    = S3C2410_SDIIMSK;

        host->sdidata    = S3C2410_SDIDATA;

        host->clk_div    = 2;

    }
```

host->sdiimsk 、host->sdidata分别用来存放host控制器 **SDI中断屏蔽寄存器** 和 **SDI数据寄存器相对SDI 寄存器的偏移地址** 。对于s3c2440 根据芯片手册SDIIntMsk 偏移地址为0x3C，SDIDAT偏移地址为0x40。最后host->clk\_div就是指的SDI使用的时钟分频系数了。

```cpp
host->complete_what     = COMPLETION_NONE;

    host->pio_active     = XFER_NONE;
```

host->complete\_what 是一个枚举类型变量，实际上用以标示传输完成的状态；host->pio\_active标示数据传输的方向，所以在这里一起初始化为空。关于传输完成的标示为了后面分析方便还是一起列举出来：

```cpp
enum s3cmci_waitfor {

    COMPLETION_NONE,

    COMPLETION_FINALIZE,

    COMPLETION_CMDSENT,

    COMPLETION_RSPFIN,

    COMPLETION_XFERFINISH,

    COMPLETION_XFERFINISH_RSPFIN,

};
```

继续分析

```cpp
#ifdef CONFIG_MMC_S3C_PIODMA

    host->dodma        = host->pdata->use_dma;

#endif
```
上面是同时使能了PIO和DMA模式的情况，这里我们对两种传输方式都做相应的分析，所以host->dodma默认为1。
```cpp
host->mem = platform_get_resource(pdev, IORESOURCE_MEM, 0);

    if (!host->mem) {

        dev_err(&pdev->dev,

            "failed to get io memory region resource.\n");

 

        ret = -ENOENT;

        goto probe_free_gpio;

    }

 

    host->mem = request_mem_region(host->mem->start,

                       resource_size(host->mem), pdev->name);

 

    if (!host->mem) {

        dev_err(&pdev->dev, "failed to request io memory region.\n");

        ret = -ENOENT;

        goto probe_free_gpio;

    }

 

    host->base = ioremap(host->mem->start, resource_size(host->mem));

    if (!host->base) {

        dev_err(&pdev->dev, "failed to ioremap() io memory region.\n");

        ret = -EINVAL;

        goto probe_free_mem_region;

    }
```
上面的一段代码相对比较简单，都是平台驱动设计过程中常用的几个处理函数，就不一一展开了。 首先是获取IO 资源 ， 这当然即使mach-mini2440.c 中所注册的IORESOURCE\_MEM,

这段代码会申请这个资源并检查是否可用，当然只要之前没有使用过SDI寄存器空间，这里都会申请成功。最后就是 IO映射 ，将实地址映射为内核虚拟地址使用。最后，host->base将保持SDI寄存器基地址所对应的内核虚拟地址。  

```cpp
host->irq = platform_get_irq(pdev, 0);

    if (host->irq == 0) {

        dev_err(&pdev->dev, "failed to get interrupt resource.\n");

        ret = -EINVAL;

        goto probe_iounmap;

    }

 

    if (request_irq(host->irq, s3cmci_irq, 0, DRIVER_NAME, host)) {

        dev_err(&pdev->dev, "failed to request mci interrupt.\n");

        ret = -ENOENT;

        goto probe_iounmap;

    }
```

上面一段是 **对中断资源的申请** ，并 通过 **request\_irq** 安装了中断处理函数，使能了SDI中断 。在上段最为关心的是 **s3cmci\_irq** 中断处理函数及其传入的dev\_id。关于这个处理函数的分析后面讲述数据传输的时候会进行细致分析。接着向下....

```cpp
/* We get spurious interrupts even when we have set the IMSK

     * register to ignore everything, so use disable_irq() to make

     * ensure we don't lock the system with un-serviceable requests. */

 

    disable_irq(host->irq);

    host->irq_state = false;
```
前面我们强调了request\_irq调用的结果会使能host->irq，但此时系统初始化尚未完成这时候出现的中断可能将处理器带入一个异常状态，所以5行屏蔽中断1650行将中断状态置位无效都是有必要的。
```cpp
if (!host->pdata->no_detect) {

        ret = gpio_request(host->pdata->gpio_detect, "s3cmci detect");

        if (ret) {

            dev_err(&pdev->dev, "failed to get detect gpio\n");

            goto probe_free_irq;

        }
```

如果SD卡存在的检查一般是通过读取专用引脚状态来实现的，这里如果需要做detect相关的工作的话就必须重新分配一个管脚，在当前系统中前面定义了以GPG8作为检测引脚

```cpp
host->irq_cd = gpio_to_irq(host->pdata->gpio_detect);
```

s3c2410\_gpio\_getirq 是获取这个GPIO的外部中断向量号，可见后面的SD卡的检测可能会用到这个引脚的外部中断。

```cpp
if (host->irq_cd >= 0) {

            if (request_irq(host->irq_cd, s3cmci_irq_cd,

                    IRQF_TRIGGER_RISING |

                    IRQF_TRIGGER_FALLING,

                    DRIVER_NAME, host)) {

                dev_err(&pdev->dev,

                    "can't get card detect irq.\n");

                ret = -ENOENT;

                goto probe_free_gpio_cd;

            }

        } else {

            dev_warn(&pdev->dev,

                 "host detect has no irq available\n");

            gpio_direction_input(host->pdata->gpio_detect);

        }

    } else

        host->irq_cd = -1;
```

上面的这段代码意图很明显就是要申请这个中断了，s3cmci\_irq\_cd是其处理函数。对像SD卡这种可移出设备来作为块设备存储介质的话，大多会涉及到媒体切换，具体这方面的内容后面用到的时候也会有个详细分析。

```cpp
if (!host->pdata->no_wprotect) {

        ret = gpio_request(host->pdata->gpio_wprotect, "s3cmci wp");

        if (ret) {

            dev_err(&pdev->dev, "failed to get writeprotect\n");

            goto probe_free_irq_cd;

        }

 

        gpio_direction_input(host->pdata->gpio_wprotect);

    }

 

    /* depending on the dma state, get a dma channel to use. */

 

    if (s3cmci_host_usedma(host)) {

        host->dma = s3c2410_dma_request(DMACH_SDI, &s3cmci_dma_client,

                        host);

        if (host->dma < 0) {

            dev_err(&pdev->dev, "cannot get DMA channel.\n");

            if (!s3cmci_host_canpio()) {

                ret = -EBUSY;

                goto probe_free_gpio_wp;

            } else {

                dev_warn(&pdev->dev, "falling back to PIO.\n");

                host->dodma = 0;

            }

        }

    }
```

1行这个我们之前就默认为TURE了，所以接下来的几行代码是免不了。

14 行s3c2410\_dma\_request 申请DMA 通道，对s3c2440 平台有4 通道的DMA。而DMACH\_SDI 是一个虚拟的通道号，由于这部分代码是和硬件紧密相关的，而且整个DMA的管理相对来讲比较复杂，所以这里只是粗略了解一下。

```cpp
host->clk = clk_get(&pdev->dev, "sdi");

    if (IS_ERR(host->clk)) {

        dev_err(&pdev->dev, "failed to find clock source.\n");

        ret = PTR_ERR(host->clk);

        host->clk = NULL;

        goto probe_free_dma;

    }

 

    ret = clk_enable(host->clk);

    if (ret) {

        dev_err(&pdev->dev, "failed to enable clock source.\n");

        goto clk_free;

    }

 

    host->clk_rate = clk_get_rate(host->clk);
```

以上是关于 **sdi时钟和波特率的有关设置** ，都是内核提供的一些简单的函数调用，相关的内容不是现在研究的重点就不再详细分析了。

```cpp
mmc->ops     = &s3cmci_ops;

    mmc->ocr_avail    = MMC_VDD_32_33 | MMC_VDD_33_34;

#ifdef CONFIG_MMC_S3C_HW_SDIO_IRQ

    mmc->caps    = MMC_CAP_4_BIT_DATA | MMC_CAP_SDIO_IRQ;

#else

    mmc->caps    = MMC_CAP_4_BIT_DATA;

#endif

    mmc->f_min     = host->clk_rate / (host->clk_div * 256);

    mmc->f_max     = host->clk_rate / host->clk_div;

 

    if (host->pdata->ocr_avail)

        mmc->ocr_avail = host->pdata->ocr_avail;

 

    mmc->max_blk_count    = 4095;

    mmc->max_blk_size    = 4095;

    mmc->max_req_size    = 4095 * 512;

    mmc->max_seg_size    = mmc->max_req_size;

 

    mmc->max_segs        = 128;

 

    dbg(host, dbg_debug,

        "probe: mode:%s mapped mci_base:%p irq:%u irq_cd:%u dma:%u.\n",

        (host->is2440?"2440":""),

        host->base, host->irq, host->irq_cd, host->dma);
```

上面就是对这个将要出嫁的 **mmc\_host进行最后的设置** ， **mmc->ops = &s3cmci\_ops; 就是一直以来向core层提供的接口函数集** 。后面的分析可能部分是围绕它其中的函数展开的。

```cpp
ret = s3cmci_cpufreq_register(host);

    if (ret) {

        dev_err(&pdev->dev, "failed to register cpufreq\n");

        goto free_dmabuf;

    }
```

这里使用的是Linux的通告机制，s3cmci\_cpufreq\_register相对应的代码如下：

static inline int s3cmci\_cpufreq\_register( [struct](https://so.csdn.net/so/search?q=struct&spm=1001.2101.3001.7020) s3cmci\_host \*host) {

host->freq\_transition.notifier\_call = s3cmci\_cpufreq\_transition;

return cpufreq\_register\_notifier(&host->freq\_transition,

CPUFREQ\_TRANSITION\_NOTIFIER);  
}

cpufreq\_register\_notifier cpu是将host->freq\_transition注册到CPU频率通告链上，这个是由内核维护的，当cpu频率改变时将会调用上面注册的s3cmci\_cpufreq\_transition的内容。

```cpp
ret = mmc_add_host(mmc);

    if (ret) {

        dev_err(&pdev->dev, "failed to add mmc host.\n");

        goto free_cpufreq;

    }
```

**b -- mmc\_add\_host**

这是core层的函数，他保存了所有平台通用的代码。同时看上去简简单单的一个mmc\_add\_host，可能蕴藏着天大的玄机。为此我们将为mmc\_add\_host另分一章，作为core层的续集，专门讲述mmc\_add\_host过程中发生的点点滴滴....在开始分析mmc\_add\_host之前，让我们还是结束SD主机控制器的probe函数，接下来

```cpp
s3cmci_debugfs_attach(host);

 

    platform_set_drvdata(pdev, mmc);

    dev_info(&pdev->dev, "%s - using %s, %s SDIO IRQ\n", mmc_hostname(mmc),

         s3cmci_host_usedma(host) ? "dma" : "pio",

         mmc->caps & MMC_CAP_SDIO_IRQ ? "hw" : "sw");

 

    return 0;

 

 free_cpufreq:

    s3cmci_cpufreq_deregister(host);

 

 free_dmabuf:

    clk_disable(host->clk);

 

 clk_free:

    clk_put(host->clk);

 

 probe_free_dma:

    if (s3cmci_host_usedma(host))

        s3c2410_dma_free(host->dma, &s3cmci_dma_client);

 

 probe_free_gpio_wp:

    if (!host->pdata->no_wprotect)

        gpio_free(host->pdata->gpio_wprotect);

 

 probe_free_gpio_cd:

    if (!host->pdata->no_detect)

        gpio_free(host->pdata->gpio_detect);

 

 probe_free_irq_cd:

    if (host->irq_cd >= 0)

        free_irq(host->irq_cd, host);

 

 probe_free_irq:

    free_irq(host->irq, host);

 

 probe_iounmap:

    iounmap(host->base);

 

 probe_free_mem_region:

    release_mem_region(host->mem->start, resource_size(host->mem));

 

 probe_free_gpio:

    for (i = S3C2410_GPE(5); i <= S3C2410_GPE(10); i++)

        gpio_free(i);

 

 probe_free_host:

    mmc_free_host(mmc);

 

 probe_out:

    return ret;

}

 

static void s3cmci_shutdown(struct platform_device *pdev)

{

    struct mmc_host    *mmc = platform_get_drvdata(pdev);

    struct s3cmci_host *host = mmc_priv(mmc);

 

    if (host->irq_cd >= 0)

        free_irq(host->irq_cd, host);

 

    s3cmci_debugfs_remove(host);

    s3cmci_cpufreq_deregister(host);

    mmc_remove_host(mmc);

    clk_disable(host->clk);

}
```

上面的基本都是出错的处理了，那么也就没有必要纠结于此了，赶快开启新的生活吧....  

再多说一句，可以看到probe函数里面，大量的工作是对 host 结构体 mmc结构体的填充，类似于USB probe函数中对 usb\_skel 结构体的填充， 向上提供接口函数 。

  

# **三、 设备驱动的功能函数**

一般情况下，设备驱动里都有一个行为函数结构体，比如字符设备驱动里的struct file\_operations \*fops，该结构描述了设备所具备的工作能力，比如open, read, write等，

struct file\_operations {  
struct module \*owner;  
ssize\_t (\*read) (struct file \*, char \_\_user \*, size\_t, loff\_t \*);  
ssize\_t (\*write) (struct file \*, const char \_\_user \*, size\_t, loff\_t \*);  
int (\*open) (struct inode \*, struct file \*);  
......  
};

同理，SD主控制器驱动程序里也有一个类似的结构 struct mmc\_host\_ops \*ops ，它描述了该控制器所具备驱动的能力。

```cpp
static struct mmc_host_ops s3cmci_ops = {

    .request    = s3cmci_request,

    .set_ios    = s3cmci_set_ios,

    .get_ro        = s3cmci_get_ro,

    .get_cd        = s3cmci_card_present,

    .enable_sdio_irq = s3cmci_enable_sdio_irq,

};
```
其中， (\*set\_ios)为主控制器设置总线和时钟等配置 ， **(\*get\_ro)得到只读属性** ， **(\*enable\_sdio\_irq)开启sdio中断** ，本文重点讨论 (\*request)这个回调函数 ，它是整个SD主控制器驱动的核心，实现了SD主控制器能与SD卡进行通信的能力。
```cpp
static void s3cmci_request(struct mmc_host *mmc, struct mmc_request *mrq)

{

    struct s3cmci_host *host = mmc_priv(mmc);

 

    host->status = "mmc request";

    host->cmd_is_stop = 0;

    host->mrq = mrq;

 

    if (s3cmci_card_present(mmc) == 0) {

        dbg(host, dbg_err, "%s: no medium present\n", __func__);

        host->mrq->cmd->error = -ENOMEDIUM;

        mmc_request_done(mmc, mrq);

    } else

        s3cmci_send_request(mmc);

}
```

可以看到这里调用了s3cmci\_send\_request(mmc) 函数，定义如下：

```cpp
static void s3cmci_send_request(struct mmc_host *mmc)

{

    struct s3cmci_host *host = mmc_priv(mmc);

    struct mmc_request *mrq = host->mrq;

    struct mmc_command *cmd = host->cmd_is_stop ? mrq->stop : mrq->cmd;

 

    host->ccnt++;

    prepare_dbgmsg(host, cmd, host->cmd_is_stop);

 

    /* Clear command, data and fifo status registers

       Fifo clear only necessary on 2440, but doesn't hurt on 2410

    */

    writel(0xFFFFFFFF, host->base + S3C2410_SDICMDSTAT);

    writel(0xFFFFFFFF, host->base + S3C2410_SDIDSTA);

    writel(0xFFFFFFFF, host->base + S3C2410_SDIFSTA);

 

    if (cmd->data) {

        int res = s3cmci_setup_data(host, cmd->data);

 

        host->dcnt++;

 

        if (res) {

            dbg(host, dbg_err, "setup data error %d\n", res);

            cmd->error = res;

            cmd->data->error = res;

 

            mmc_request_done(mmc, mrq);

            return;

        }

 

        if (s3cmci_host_usedma(host))

            res = s3cmci_prepare_dma(host, cmd->data);

        else

            res = s3cmci_prepare_pio(host, cmd->data);

 

        if (res) {

            dbg(host, dbg_err, "data prepare error %d\n", res);

            cmd->error = res;

            cmd->data->error = res;

 

            mmc_request_done(mmc, mrq);

            return;

        }

    }

 

    /* Send command */

    s3cmci_send_command(host, cmd);

 

    /* Enable Interrupt */

    s3cmci_enable_irq(host, true);

}
```

其中有两个重要的结构体 s3cmci\_setup\_data(host, cmd->data)实现数据传输 及 s3cmci\_send\_command(host, cmd)实现指令传输 ，至此，我们需要接触SD主控制器的芯片手册了。

首先，SD主控制器由一系列32位寄存器组成。通过软件的方式，即对寄存器赋值，来控制SD主控制器，进而扮演SD主控制器的角色与SD卡取得通信。 ![](https://img-blog.csdn.net/20160402141150854?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)  

**1) cmdat**

根据主控制器的芯片手册，寄存器MMC\_CMDAT控制命令和数据的传输，具体内容如下

![](https://img-blog.csdn.net/20160402141351683?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)

结合对寄存器MMC\_CMDAT的描述，分析代码

```cpp
host->cmdat &= ~CMDAT_INIT;               // 非初始化状态

if (mrq->data) {                                       // 如果存在数据需要传输

  pxamci_setup_data(host, mrq->data);  // 实现主控制器与SD卡之间数据的传输

  cmdat &= ~CMDAT_BUSY;                      // 没有忙碌busy信号

  cmdat |= CMDAT_DATAEN | CMDAT_DMAEN;   // 有数据传输，使用DMA

  if (mrq->data->flags & MMC_DATA_WRITE)    

   cmdat |= CMDAT_WRITE;                               // 设置为写数据

  if (mrq->data->flags & MMC_DATA_STREAM)

   cmdat |= CMDAT_STREAM;                             // 设置为数据流stream模式

}
```

  

**2) s3cmci\_setup\_data**

通过DMA实现主控制器与SD卡之间数据的传输

```cpp
static int s3cmci_setup_data(struct s3cmci_host *host, struct mmc_data *data)

{

    u32 dcon, imsk, stoptries = 3;

 

    /* write DCON register */

 

    if (!data) {

        writel(0, host->base + S3C2410_SDIDCON);

        return 0;

    }

 

    if ((data->blksz & 3) != 0) {

        /* We cannot deal with unaligned blocks with more than

         * one block being transferred. */

 

        if (data->blocks > 1) {

            pr_warning("%s: can't do non-word sized block transfers (blksz %d)\n", __func__, data->blksz);

            return -EINVAL;

        }

    }

 

    while (readl(host->base + S3C2410_SDIDSTA) &

           (S3C2410_SDIDSTA_TXDATAON | S3C2410_SDIDSTA_RXDATAON)) {

 

        dbg(host, dbg_err,

            "mci_setup_data() transfer stillin progress.\n");

 

        writel(S3C2410_SDIDCON_STOP, host->base + S3C2410_SDIDCON);

        s3cmci_reset(host);

 

        if ((stoptries--) == 0) {

            dbg_dumpregs(host, "DRF");

            return -EINVAL;

        }

    }

 

    dcon  = data->blocks & S3C2410_SDIDCON_BLKNUM_MASK;

 

    if (s3cmci_host_usedma(host))

        dcon |= S3C2410_SDIDCON_DMAEN;

 

    if (host->bus_width == MMC_BUS_WIDTH_4)

        dcon |= S3C2410_SDIDCON_WIDEBUS;

 

    if (!(data->flags & MMC_DATA_STREAM))

        dcon |= S3C2410_SDIDCON_BLOCKMODE;

 

    if (data->flags & MMC_DATA_WRITE) {

        dcon |= S3C2410_SDIDCON_TXAFTERRESP;

        dcon |= S3C2410_SDIDCON_XFER_TXSTART;

    }

 

    if (data->flags & MMC_DATA_READ) {

        dcon |= S3C2410_SDIDCON_RXAFTERCMD;

        dcon |= S3C2410_SDIDCON_XFER_RXSTART;

    }

 

    if (host->is2440) {

        dcon |= S3C2440_SDIDCON_DS_WORD;

        dcon |= S3C2440_SDIDCON_DATSTART;

    }

 

    writel(dcon, host->base + S3C2410_SDIDCON);

 

    /* write BSIZE register */

 

    writel(data->blksz, host->base + S3C2410_SDIBSIZE);

 

    /* add to IMASK register */

    imsk = S3C2410_SDIIMSK_FIFOFAIL | S3C2410_SDIIMSK_DATACRC |

           S3C2410_SDIIMSK_DATATIMEOUT | S3C2410_SDIIMSK_DATAFINISH;

 

    enable_imask(host, imsk);

 

    /* write TIMER register */

 

    if (host->is2440) {

        writel(0x007FFFFF, host->base + S3C2410_SDITIMER);

    } else {

        writel(0x0000FFFF, host->base + S3C2410_SDITIMER);

 

        /* FIX: set slow clock to prevent timeouts on read */

        if (data->flags & MMC_DATA_READ)

            writel(0xFF, host->base + S3C2410_SDIPRE);

    }

 

    return 0;

}
```
for()循环里的内容是整个SD卡主控制器设备驱动的实质，通过DMA的方式实现主控制器与SD卡之间数据的读写操作。  
  

**3) m3cmci\_start\_cmd**

实现主控制器与SD卡之间指令的传输

```cpp
static void s3cmci_send_command(struct s3cmci_host *host,

                    struct mmc_command *cmd)

{

    u32 ccon, imsk;

 

    imsk  = S3C2410_SDIIMSK_CRCSTATUS | S3C2410_SDIIMSK_CMDTIMEOUT |

        S3C2410_SDIIMSK_RESPONSEND | S3C2410_SDIIMSK_CMDSENT |

        S3C2410_SDIIMSK_RESPONSECRC;

 

    enable_imask(host, imsk);

 

    if (cmd->data)

        host->complete_what = COMPLETION_XFERFINISH_RSPFIN;

    else if (cmd->flags & MMC_RSP_PRESENT)

        host->complete_what = COMPLETION_RSPFIN;

    else

        host->complete_what = COMPLETION_CMDSENT;

 

    writel(cmd->arg, host->base + S3C2410_SDICMDARG);

 

    ccon  = cmd->opcode & S3C2410_SDICMDCON_INDEX;

    ccon |= S3C2410_SDICMDCON_SENDERHOST | S3C2410_SDICMDCON_CMDSTART;

 

    if (cmd->flags & MMC_RSP_PRESENT)

        ccon |= S3C2410_SDICMDCON_WAITRSP;

 

    if (cmd->flags & MMC_RSP_136)

        ccon |= S3C2410_SDICMDCON_LONGRSP;

 

    writel(ccon, host->base + S3C2410_SDICMDCON);

}
```

**\> response类型**

根据SD卡的协议，当SD卡收到从控制器发来的cmd指令后，SD卡会发出response相应，而response的类型分为R1,R1b,R2,R3,R6,R7，这些类型分别对应不同的指令，各自的数据包结构也不同(具体内容参考SD卡协议)。这里，通过RSP\_TYPE对指令cmd的opcode的解析得到相对应的reponse类型，再通过swich赋给寄存器MMC\_CMDAT对应的\[1:0\]位。

**\-> 将指令和参数写入寄存器**

4行writel()是整个SD卡主控制器设备驱动的实质，通过对主控制器芯片寄存器MMC\_CMD,MMC\_ARGH,MMC\_ARGL,MMC\_CMDAT的设置，实现主控制器发送指令到SD卡的功能。  

  

# **四、申请中断**

这里对前面的中断函数进行详细描述：

s3cmci\_probe(struct platform\_device \*pdev)中有两个中断， 一个为SD主控制器芯片内电路固有的内部中断 ， 另一个为探测引脚的探测到外部有SD卡插拔引起的中断

**1) 由主控芯片内部电路引起的中断**

(request\_irq(host->irq, s3cmci\_irq, 0, DRIVER\_NAME, host） ；

回顾一下，host->irq就是刚才从platform\_device里得到的中断号，

irq = platform\_get\_irq(pdev, 0);

host->irq = irq;

接下来，s3cmci\_irq便是为该中断host->irq申请的中断函数

```cpp
/*

 * ISR for SDI Interface IRQ

 * Communication between driver and ISR works as follows:

 *   host->mrq             points to current request

 *   host->complete_what    Indicates when the request is considered done

 *     COMPLETION_CMDSENT      when the command was sent

 *     COMPLETION_RSPFIN          when a response was received

 *     COMPLETION_XFERFINISH      when the data transfer is finished

 *     COMPLETION_XFERFINISH_RSPFIN both of the above.

 *   host->complete_request    is the completion-object the driver waits for

 *

 * 1) Driver sets up host->mrq and host->complete_what

 * 2) Driver prepares the transfer

 * 3) Driver enables interrupts

 * 4) Driver starts transfer

 * 5) Driver waits for host->complete_rquest

 * 6) ISR checks for request status (errors and success)

 * 6) ISR sets host->mrq->cmd->error and host->mrq->data->error

 * 7) ISR completes host->complete_request

 * 8) ISR disables interrupts

 * 9) Driver wakes up and takes care of the request

 *

 * Note: "->error"-fields are expected to be set to 0 before the request

 *       was issued by mmc.c - therefore they are only set, when an error

 *       contition comes up

 */

 

static irqreturn_t s3cmci_irq(int irq, void *dev_id)

{

    struct s3cmci_host *host = dev_id;

    struct mmc_command *cmd;

    u32 mci_csta, mci_dsta, mci_fsta, mci_dcnt, mci_imsk;

    u32 mci_cclear = 0, mci_dclear;

    unsigned long iflags;

 

    mci_dsta = readl(host->base + S3C2410_SDIDSTA);

    mci_imsk = readl(host->base + host->sdiimsk);

 

    if (mci_dsta & S3C2410_SDIDSTA_SDIOIRQDETECT) {

        if (mci_imsk & S3C2410_SDIIMSK_SDIOIRQ) {

            mci_dclear = S3C2410_SDIDSTA_SDIOIRQDETECT;

            writel(mci_dclear, host->base + S3C2410_SDIDSTA);

 

            mmc_signal_sdio_irq(host->mmc);

            return IRQ_HANDLED;

        }

    }

 

    spin_lock_irqsave(&host->complete_lock, iflags);

 

    mci_csta = readl(host->base + S3C2410_SDICMDSTAT);

    mci_dcnt = readl(host->base + S3C2410_SDIDCNT);

    mci_fsta = readl(host->base + S3C2410_SDIFSTA);

    mci_dclear = 0;

 

    if ((host->complete_what == COMPLETION_NONE) ||

        (host->complete_what == COMPLETION_FINALIZE)) {

        host->status = "nothing to complete";

        clear_imask(host);

        goto irq_out;

    }

 

    if (!host->mrq) {

        host->status = "no active mrq";

        clear_imask(host);

        goto irq_out;

    }

 

    cmd = host->cmd_is_stop ? host->mrq->stop : host->mrq->cmd;

 

    if (!cmd) {

        host->status = "no active cmd";

        clear_imask(host);

        goto irq_out;

    }

 

    if (!s3cmci_host_usedma(host)) {

        if ((host->pio_active == XFER_WRITE) &&

            (mci_fsta & S3C2410_SDIFSTA_TFDET)) {

 

            disable_imask(host, S3C2410_SDIIMSK_TXFIFOHALF);

            tasklet_schedule(&host->pio_tasklet);

            host->status = "pio tx";

        }

 

        if ((host->pio_active == XFER_READ) &&

            (mci_fsta & S3C2410_SDIFSTA_RFDET)) {

 

            disable_imask(host,

                      S3C2410_SDIIMSK_RXFIFOHALF |

                      S3C2410_SDIIMSK_RXFIFOLAST);

 

            tasklet_schedule(&host->pio_tasklet);

            host->status = "pio rx";

        }

    }

 

    if (mci_csta & S3C2410_SDICMDSTAT_CMDTIMEOUT) {

        dbg(host, dbg_err, "CMDSTAT: error CMDTIMEOUT\n");

        cmd->error = -ETIMEDOUT;

        host->status = "error: command timeout";

        goto fail_transfer;

    }

 

    if (mci_csta & S3C2410_SDICMDSTAT_CMDSENT) {

        if (host->complete_what == COMPLETION_CMDSENT) {

            host->status = "ok: command sent";

            goto close_transfer;

        }

 

        mci_cclear |= S3C2410_SDICMDSTAT_CMDSENT;

    }

 

    if (mci_csta & S3C2410_SDICMDSTAT_CRCFAIL) {

        if (cmd->flags & MMC_RSP_CRC) {

            if (host->mrq->cmd->flags & MMC_RSP_136) {

                dbg(host, dbg_irq,

                    "fixup: ignore CRC fail with long rsp\n");

            } else {

                /* note, we used to fail the transfer

                 * here, but it seems that this is just

                 * the hardware getting it wrong.

                 *

                 * cmd->error = -EILSEQ;

                 * host->status = "error: bad command crc";

                 * goto fail_transfer;

                */

            }

        }

 

        mci_cclear |= S3C2410_SDICMDSTAT_CRCFAIL;

    }

 

    if (mci_csta & S3C2410_SDICMDSTAT_RSPFIN) {

        if (host->complete_what == COMPLETION_RSPFIN) {

            host->status = "ok: command response received";

            goto close_transfer;

        }

 

        if (host->complete_what == COMPLETION_XFERFINISH_RSPFIN)

            host->complete_what = COMPLETION_XFERFINISH;

 

        mci_cclear |= S3C2410_SDICMDSTAT_RSPFIN;

    }

 

    /* errors handled after this point are only relevant

       when a data transfer is in progress */

 

    if (!cmd->data)

        goto clear_status_bits;

 

    /* Check for FIFO failure */

    if (host->is2440) {

        if (mci_fsta & S3C2440_SDIFSTA_FIFOFAIL) {

            dbg(host, dbg_err, "FIFO failure\n");

            host->mrq->data->error = -EILSEQ;

            host->status = "error: 2440 fifo failure";

            goto fail_transfer;

        }

    } else {

        if (mci_dsta & S3C2410_SDIDSTA_FIFOFAIL) {

            dbg(host, dbg_err, "FIFO failure\n");

            cmd->data->error = -EILSEQ;

            host->status = "error:  fifo failure";

            goto fail_transfer;

        }

    }

 

    if (mci_dsta & S3C2410_SDIDSTA_RXCRCFAIL) {

        dbg(host, dbg_err, "bad data crc (outgoing)\n");

        cmd->data->error = -EILSEQ;

        host->status = "error: bad data crc (outgoing)";

        goto fail_transfer;

    }

 

    if (mci_dsta & S3C2410_SDIDSTA_CRCFAIL) {

        dbg(host, dbg_err, "bad data crc (incoming)\n");

        cmd->data->error = -EILSEQ;

        host->status = "error: bad data crc (incoming)";

        goto fail_transfer;

    }

 

    if (mci_dsta & S3C2410_SDIDSTA_DATATIMEOUT) {

        dbg(host, dbg_err, "data timeout\n");

        cmd->data->error = -ETIMEDOUT;

        host->status = "error: data timeout";

        goto fail_transfer;

    }

 

    if (mci_dsta & S3C2410_SDIDSTA_XFERFINISH) {

        if (host->complete_what == COMPLETION_XFERFINISH) {

            host->status = "ok: data transfer completed";

            goto close_transfer;

        }

 

        if (host->complete_what == COMPLETION_XFERFINISH_RSPFIN)

            host->complete_what = COMPLETION_RSPFIN;

 

        mci_dclear |= S3C2410_SDIDSTA_XFERFINISH;

    }

 

clear_status_bits:

    writel(mci_cclear, host->base + S3C2410_SDICMDSTAT);

    writel(mci_dclear, host->base + S3C2410_SDIDSTA);

 

    goto irq_out;

 

fail_transfer:

    host->pio_active = XFER_NONE;

 

close_transfer:

    host->complete_what = COMPLETION_FINALIZE;

 

    clear_imask(host);

    tasklet_schedule(&host->pio_tasklet);

 

    goto irq_out;

 

irq_out:

    dbg(host, dbg_irq,

        "csta:0x%08x dsta:0x%08x fsta:0x%08x dcnt:0x%08x status:%s.\n",

        mci_csta, mci_dsta, mci_fsta, mci_dcnt, host->status);

 

    spin_unlock_irqrestore(&host->complete_lock, iflags);

    return IRQ_HANDLED;

 

}
```

当调用(\* request )，即host->ops->request(host, mrq)，即上文中的s3cmci\_request()后，控制器与SD卡之间开始进行一次指令或数据传输，通信完毕后，主控芯片将产生一个内部中断，以告知此次指令或数据传输完毕。这个中断的具体值将保存在一个名为MMC\_I\_REG的中断寄存器中以供读取，中断寄存器MMC\_I\_REG中相关描述如下  

![](https://img-blog.csdn.net/20160402143118314?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)  

  

如果中断寄存器MMC\_I\_REG中的第0位有值，则意味着数据传输完成，执行s3cmci\_cmd\_done(host, stat);

如果中断寄存器MMC\_I\_REG中的第2位有值，则意味着指令传输完成，执行s3cmci\_data\_done(host, stat);

其中stat是从状态寄存器MMC\_STAT中读取的值，在代码里主要起到处理错误状态的作用。

\-> **s3cmci\_cmd\_done** 收到结束指令的内部中断信号，主控制器从SD卡那里得到response，结束这次指令传输

这里需要注意，寄存器MMC\_RES里已经存放了来自SD卡发送过来的response，以供读取。  

  

**2、探测引脚引起的中断**

![](https://img-blog.csdn.net/20160402143328112?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)  

```cpp
host->irq_cd = gpio_to_irq(host->pdata->gpio_detect);

 

        if (host->irq_cd >= 0) {

            if (request_irq(host->irq_cd, s3cmci_irq_cd,

                    IRQF_TRIGGER_RISING |

                    IRQF_TRIGGER_FALLING,

                    DRIVER_NAME, host)) {

                dev_err(&pdev->dev,

                    "can't get card detect irq.\n");

                ret = -ENOENT;

                goto probe_free_gpio_cd;

            }

        } else {

            dev_warn(&pdev->dev,

                 "host detect has no irq available\n");

            gpio_direction_input(host->pdata->gpio_detect);

        }
```

其中，irq\_cd是通过GPIO转换得到的中断号， s3cmci\_irq\_cd 便是该中断实现的函数

```cpp
static irqreturn_t s3cmci_irq_cd(int irq, void *dev_id)

{

    struct s3cmci_host *host = (struct s3cmci_host *)dev_id;

 

    dbg(host, dbg_irq, "card detect\n");

 

    mmc_detect_change(host->mmc, msecs_to_jiffies(500));

 

    return IRQ_HANDLED;

}
```

之前已经提到过 mmc\_detect\_change ，它将最终调用queue\_delayed\_work执行工作队列里的 mmc\_rescan函数 。

当有SD卡插入或拔出时，硬件主控制器芯片的探测pin脚产生外部中断，进入中断处理函数，执行工作队列里的mmc\_rescan，扫描SD总线，对插入或拔出SD卡作相应的处理。 下文协议层将讨论mmc\_rescan()。