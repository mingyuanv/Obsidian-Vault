---
title: "LInux驱动开发笔记（十）SPI子系统及其驱动_linux spi驱动开发-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/139804156?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读2.2k次，点赞34次，收藏28次。前章我们已经学习了iic子系统驱动，这部分我们继续spi子系统驱动的学习。_linux spi驱动开发"
tags:
  - "clippings"
---
---

## 前言

  前章我们已经学习了 [iic](https://so.csdn.net/so/search?q=iic&spm=1001.2101.3001.7020) 子系统驱动，这部分我们继续spi子系统驱动的学习。

---

## 一、SPI驱动框架

  SPI同样可分为 [spi总线](https://so.csdn.net/so/search?q=spi%E6%80%BB%E7%BA%BF&spm=1001.2101.3001.7020) 驱动和spi设备驱动， 我们也只需要进行spi设备驱动的编写。SPI设备驱动涉及到SPI设备驱动、SPI核心层、SPI主机驱动，具体功能如下：  
**SPI核心层** ：SPI核心层是SPI子系统的中间层，提供了一个通用的接口以便设备驱动可以与SPI主机驱动交互。核心层负责管理SPI总线上的所有设备，并提供基本的数据传输功能。提供SPI控制器驱动和设备驱动的注册方法、注销方法，SPI Core提供操作接口 函数 ，允许一个spi master，spi driver 和spi device初始化。  
**SPI主机驱动** ：SPI主机驱动与具体的 硬件 SPI控制器直接交互，负责实际的数据传输和控制操作，它实现了SPI核心层定义的接口，并提供对硬件的抽象。其主要包含SPI硬件体系结构中适配器(spi控制器)的控制，实现spi总线的硬件访问操作。  
**SPI设备驱动** ：SPI设备驱动是针对特定SPI从设备的驱动程序，负责与特定的硬件设备交互，主要职责包括设备的初始化、配置以及数据传输。设备驱动通常会调用SPI核心层提供的接口来完成这些任务。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a395f8d39c950231e37f29b94ed65fb2.png#pic_center)

## 二、总线驱动

### 2.1 SPI总线的运行机制

linux 系统在开机的时候就会自动执行spi\_init函数，进行spi总线注册。当总线注册成功之后，会在sys/bus下面生成一个spi总线，然后在系统中新增一个设备类，sys/class/目录下会可以找到spi\_master类。

```c
//注册SPI总线
static int __init spi_init(void)
{
    int     status;
    ...
    status = bus_register(&spi_bus_type);
    ...
    status = class_register(&spi_master_class);
    ...
}

struct bus_type spi_bus_type = {
    .name           = "spi",
    .dev_groups     = spi_dev_groups,
    .match          = spi_match_device,
    .uevent         = spi_uevent,
};

//匹配规则，同IIC子系统，常用设备树匹配的方法
static int spi_match_device(struct device *dev, struct device_driver *drv)
{
    const struct spi_device *spi = to_spi_device(dev);
    const struct spi_driver *sdrv = to_spi_driver(drv);

    /* Attempt an OF style match */
    if (of_driver_match_device(dev, drv))
        return 1;

    /* Then try ACPI */
    if (acpi_driver_match_device(dev, drv))
        return 1;

    if (sdrv->id_table)
        return !!spi_match_id(sdrv->id_table, spi);

    return strcmp(spi->modalias, drv->name) == 0;
}
1234567891011121314151617181920212223242526272829303132333435363738
```

  使用的rk3568芯片有4个spi控制器，对应的设备树存在4个节点，利用平台总线module\_platform\_driver(rockchip\_spi\_driver)， 间接调用platform\_driver\_register 和 platform\_driver\_unregister，实现平台驱动函数的注册和注销。  
  当匹配到对应驱动时时，调用rockchip\_spi\_probe函数，进行初始化，获取设备树节点信息，初始化spi时钟、dma、中断等。

### 2.2 重要数据结构

#### 2.2.1 spi\_controller

  spi\_controller 结构体用于表示一个SPI控制器，它包含了控制器的属性和方法。在Linux中，该结构体定义在 <linux/spi/spi.h> 头文件中。

```c
struct spi_controller {
    struct device            dev;
    ...
    struct list_head          list;
    s16                      bus_num;
    u16                      num_chipselect;
    ...
    struct spi_message       *cur_msg;
    ...
    int     (*setup)(struct spi_device *spi);
    int     (*transfer)(struct spi_device *spi,struct spi_message *mesg);
    void    (*cleanup)(struct spi_device *spi);
    struct kthread_worker    kworker;
    struct task_struct       *kworker_task;
    struct kthread_work      pump_messages;
    struct list_head         queue;
    struct spi_message       *cur_msg;
    ...
    int (*transfer_one)(struct spi_controller *ctlr, struct spi_device *spi,struct spi_transfer *transfer);
    int (*prepare_transfer_hardware)(struct spi_controller *ctlr);
    int (*transfer_one_message)(struct spi_controller *ctlr,struct spi_message *mesg);
    void (*set_cs)(struct spi_device *spi, bool enable);
    ...
    int                     *cs_gpios;
}
12345678910111213141516171819202122232425
```

成员说明：

- dev：该字段表示该SPI控制器对应的设备对象，继承自Linux内核中的设备模型。
- list： 这是一个链表节点，用于将SPI控制器连接到全局的SPI控制器链表中。
- bus\_num： spi控制器编号。
- num\_chipselect：支持的芯片选择线数量。
- cur\_msg：指向当前正在处理的SPI消息的指针。
- setup：函数指针，用于执行SPI设备的初始化和配置操作。
- transfer：指向数据传输函数的指针，用于把数据加入控制器的消息队列中,实现SPI数据的传输。
- cleanup：函数指针，用于执行SPI设备的清理和释放操作。
- kworker： 内核线程工人，spi可以使用异步传输方式发送数据。
- pump\_messages： 具体传输工作。
- queue： 所有等待传输的消息队列挂在该链表下。
- transfer\_one\_message： 发送一个spi消息，类似IIC适配器里的algo->master\_xfer，产生spi通信时序。
- cs\_gpios： 记录spi上具体的片选信号。

#### 2.2.2 spi\_driver

  spi\_driver 结构体用于表示一个SPI设备的驱动程序，在Linux中，该结构体定义在 <linux/spi/spi.h> 头文件中。

```c
struct spi_driver {
    const struct spi_device_id *id_table;
    int                     (*probe)(struct spi_device *spi);
    int                     (*remove)(struct spi_device *spi);
    void                    (*shutdown)(struct spi_device *spi);
    struct device_driver    driver;
};
1234567
```

成员说明：

- id\_table：匹配表
- driver：设备驱动的基本信息，如驱动名字、所属的模块等。
- probe：指向探测函数的指针，用于初始化并注册SPI设备。
- shutdown：指向关闭函数的函数指针，用于关闭SPI设备。当系统关闭或卸载设备驱动时，会调用该函数。
- remove：指向移除函数的指针，用于卸载SPI设备。

#### 2.2.3 spi\_device

  spi\_device 结构体用于表示一个具体的SPI设备，它与硬件设备相对应。在Linux中，该结构体定义在 <linux/spi/spi.h> 头文件中。

```c
struct spi_device {
    struct device           dev;
    struct spi_controller   *controller;
    struct spi_controller   *master;        /* compatibility layer */
    u32                     max_speed_hz;
    u8                      chip_select;
    u8                      bits_per_word;
    u16                     mode;
   #define  SPI_CPHA        0x01                    /* clock phase */
   #define  SPI_CPOL        0x02                    /* clock polarity */
   #define  SPI_MODE_0      (0|0)                   /* (original MicroWire) */
   #define  SPI_MODE_1      (0|SPI_CPHA)
   #define  SPI_MODE_2      (SPI_CPOL|0)
   #define  SPI_MODE_3      (SPI_CPOL|SPI_CPHA)
   #define  SPI_CS_HIGH     0x04                    /* chipselect active high? */
   #define  SPI_LSB_FIRST   0x08                    /* per-word bits-on-wire */
   #define  SPI_3WIRE       0x10                    /* SI/SO signals shared */
   #define  SPI_LOOP        0x20                    /* loopback mode */
   #define  SPI_NO_CS       0x40                    /* 1 dev/bus, no chipselect */
   #define  SPI_READY       0x80                    /* slave pulls low to pause */
   #define  SPI_TX_DUAL     0x100                   /* transmit with 2 wires */
   #define  SPI_TX_QUAD     0x200                   /* transmit with 4 wires */
   #define  SPI_RX_DUAL     0x400                   /* receive with 2 wires */
   #define  SPI_RX_QUAD     0x800                   /* receive with 4 wires */
    int                     irq;
    void                    *controller_state;
    void                    *controller_data;
    char                    modalias[SPI_NAME_SIZE];
    int                     cs_gpio;        /* chip select gpio */

    /* the statistics */
    struct spi_statistics   statistics;
};
123456789101112131415161718192021222324252627282930313233
```

成员说明：

- controller：指向控制器的指针，表示该设备所属的SPI控制器。
- master：指向主机的指针，表示该设备所属的SPI主机。
- chip\_select：芯片选择线的编号。
- max\_speed\_hz：设备支持的最大时钟频率。
- mode：设备的SPI模式（CPOL、CPHA）。
- bits\_per\_word：每个数据字的位数。
- mode： SPI工作模式，工作模式如以上代码中的宏定义。
- irq： 如果使用了中断，它用于指定中断号

#### 2.2.4 spi\_transfer

  spi\_transfer 结构体用于表示SPI数据传输的信息，包括要发送和接收的数据、数据长度等。在Linux中，该结构体定义在 <linux/spi/spi.h> 头文件中。

```c
struct spi_transfer {
    const void      *tx_buf;
    void            *rx_buf;
    unsigned        len;

    dma_addr_t      tx_dma;
    dma_addr_t      rx_dma;
    struct sg_table tx_sg;
    struct sg_table rx_sg;

    unsigned        cs_change:1;
    unsigned        tx_nbits:3;
    unsigned        rx_nbits:3;
#define     SPI_NBITS_SINGLE        0x01 /* 1bit transfer */
#define     SPI_NBITS_DUAL          0x02 /* 2bits transfer */
#define     SPI_NBITS_QUAD          0x04 /* 4bits transfer */
    u8              bits_per_word;
    u16             delay_usecs;
    u32             speed_hz;

    struct list_head transfer_list;
};
12345678910111213141516171819202122
```

成员说明：

- tx\_buf：指向要发送数据的缓冲区。
- rx\_buf：指向接收数据的缓冲区。
- len：数据长度。
- tx\_dma、rx\_dma： 如果使用了DAM，用于指定tx或rx DMA地址。
- speed\_hz：数据传输的时钟频率。
- bits\_per\_word：每个数据字的位数。
- delay\_usecs：传输完成后的延迟时间。

#### 2.2.5 spi\_message

  spi\_message 结构体用于表示一个SPI数据传输的完整消息，包含了一个或多个 spi\_transfer 结构体。在Linux中，该结构体定义在 <linux/spi/spi.h> 头文件中。

```c
struct spi_message {
      ...
    struct list_head        transfers;
    struct spi_device       *spi;
    unsigned                is_dma_mapped:1;
    struct list_head        queue;
    void                     *state;
      ...
};
123456789
```

成员说明：

- spi：指向SPI设备的指针。
- is\_dma\_mapped：表示数据是否已经进行DMA映射。
- transfers：一个链表，包含了多个 spi\_transfer 结构体，表示要进行的多个数据传输。
- queue：用于在 SPI 控制器内部排队等待处理的消息队列，通常由 SPI 主控制器驱动程序使用。
- state：当前驱动程序的状态指针，用于在传输过程中保存和恢复状态。

## 三、设备驱动的编写

### 3.1 设备树的修改

  相关瑞芯微官方给出的ic3控制器的设备树代码这里就不再赘述了，如下所示：

```bash
spi3 {
    spi3m1_pins: spi3m1-pins {
        rockchip,pins =
            /* spi3_clkm1 */
            <4 RK_PC2 2 &pcfg_pull_none>,
            /* spi3_misom1 */
            <4 RK_PC5 2 &pcfg_pull_none>,
            /* spi3_mosim1 */
            <4 RK_PC3 2 &pcfg_pull_none>;
    };

    spi3m1_cs0: spi3m1-cs0 {
        rockchip,pins =
            /* spi3_cs0m1 */
            <4 RK_PC6 2 &pcfg_pull_none>;
    };

    spi3m1_cs1: spi3m1-cs1 {
        rockchip,pins =
            /* spi3_cs1m1 */
            <4 RK_PD1 2 &pcfg_pull_none>;
    };
};

spi3-hs {
            spi3m1_pins_hs: spi3m1-pins {
                    rockchip,pins =
                            /* spi3_clkm1 */
                            <4 RK_PC2 2 &pcfg_pull_up_drv_level_1>,
                            /* spi3_misom1 */
                            <4 RK_PC5 2 &pcfg_pull_up_drv_level_1>,
                            /* spi3_mosim1 */
                            <4 RK_PC3 2 &pcfg_pull_up_drv_level_1>;
            };

            spi3m1_cs0_hs: spi3m1-cs0 {
                    rockchip,pins =
                            /* spi3_cs0m1 */
                            <4 RK_PC6 2 &pcfg_pull_up_drv_level_1>;
            };

            spi3m1_cs1_hs: spi3m1-cs1 {
                    rockchip,pins =
                            /* spi3_cs1m1 */
                            <4 RK_PD1 2 &pcfg_pull_up_drv_level_1>;
            };
    };
1234567891011121314151617181920212223242526272829303132333435363738394041424344454647
```

  以下是我们需要修改的部分：

```bash
&spi3{
    status = "okay";
    
    //定义引脚控制的状态名称，用于选择引脚配置
    pinctrl-names = "default", "high_speed";
    
    //引脚控制的默认状态，引用了 spi3m1_cs0 和 spi3m1_pins 引脚配置
    pinctrl-0 = <&spi3m1_cs0 &spi3m1_pins>;
    
    //高速模式下的引脚控制状态，引用了 spi3m1_cs0 和 spi3m1_pins_hs 引脚配置
    pinctrl-1 = <&spi3m1_cs0 &spi3m1_pins_hs>;
    
    //定义芯片选择（CS）引脚的GPIO配置。这里使用了GPIO4的PC6引脚，并且是低电平有效（GPIO_ACTIVE_LOW）
    cs-gpios = <&gpio4 RK_PC6 GPIO_ACTIVE_LOW>;

    spi_oled@0 {
        status = "okay";
        compatible = "company,myspi";
        
        //SPI设备的地址，即芯片选择（CS）编号,这里是CS0
        reg = <0>;
        
        //SPI设备的最大时钟频率，单位为赫兹（Hz）                        
        spi-max-frequency = <24000000>;   
        
        //定义一个数据/命令控制引脚，使用GPIO3的PA7引脚，并且是高电平有效（GPIO_ACTIVE_HIGH）
        dc_control_pin = <&gpio3 RK_PA7 GPIO_ACTIVE_HIGH>;
        
        //定义引脚控制的状态名称，用于选择引脚配置
        pinctrl-names = "default";
        
        //引脚控制的默认状态，引用了 spi_oled_pin 引脚配置
        pinctrl-0 = <&myspi>;
    };
};

&pinctrl {
    myspi {
        myspi: myspi {
            rockchip,pins = <3 RK_PA7 RK_FUNC_GPIO &pcfg_pull_none>;
        };
    };
}; 
12345678910111213141516171819202122232425262728293031323334353637383940414243
```

### 3.2 相关API函数

#### 3.2.1 spi\_setup( )

  函数设置spi设备的片选信号、传输单位、最大传输速率等，函数中调用spi控制器的成员controller->setup()， 也就是master->setup,在前面的函数rockchip\_spi\_probe()中初始化了“ctlr->setup = rockchip\_spi\_setup;”。

```c
int spi_setup(struct spi_device *spi)
1
```
- 参数：
	- spi spi\_device spi设备结构体
- 返回值：
	- 成功： 0
	- 失败： 其他任何值都为错误码

#### 3.2.2 spi\_message\_init( )

```c
//初始化spi_message
static inline void spi_message_init(struct spi_message *m)
{
    memset(m, 0, sizeof *m);
    spi_message_init_no_memset(m);
}
123456
```
- 参数：
	- m：spi\_message 结构体指针，spi\_message结构体定义和介绍可在前面关键数据结构中找到。
- 返回值： 无。

#### 3.2.3 spi\_message\_add\_tail( )

  这个函数很简单就是将将spi\_transfer结构体添加到spi\_message队列的末尾。

```c
//
static inline void spi_message_add_tail(struct spi_transfer *t, struct spi_message *m)
{
    list_add_tail(&t->transfer_list, &m->transfers);
}
12345
```
1. 参数：
	- t：指向要添加的SPI传输结构体的指针。
	- m：指向SPI消息结构体的指针。

**注：从 Linux 内核版本 4.6 开始，spi\_transfer\_init 函数已经被废弃，并且其初始化工作被整合到了 spi\_message\_init 和 spi\_message\_add\_tail 函数中。**

#### 3.2.4 spi\_sync( )和spi\_async( )

  这两个函数都用于阻塞当前线程进行数据传输，spi\_sync()内部调用\_\_spi\_sync()/\_\_spi\_async函数，mutex\_lock()和mutex\_unlock()为互斥锁的加锁和解锁，互斥锁这部分内容在之前应用层 TCP /UDP协议中提及到过。

```c
//进行同步SPI数据传输
int spi_sync(struct spi_device *spi, struct spi_message *message)
{
    int ret;
    //上锁
    mutex_lock(&spi->controller->bus_lock_mutex);
    //
    ret = __spi_sync(spi, message);
    //解锁
    mutex_unlock(&spi->controller->bus_lock_mutex);

    return ret;
}
12345678910111213
```
1. 参数：
	- spi：指向SPI设备的指针。
	- message：包含要传输的数据的SPI消息结构体。  
		返回值：成功时返回0，失败时返回负错误代码。
```c
//进行异步SPI数据传输
int spi_async(struct spi_device *spi, struct spi_message *message)
{
    ...
    ret = __spi_async(spi, message);
    ...
}
1234567
```
1. 参数：
	- spi：指向SPI设备的指针。
	- message：包含要传输的数据的SPI消息结构体。
2. 返回值：
	- 0：成功
	- 负数：错误码

#### 3.2.5 spi\_register\_driver( )

```c
//注册一个SPI设备驱动程序
int spi_register_driver(struct spi_driver *sdrv);
12
```
1. 参数：
	- sdrv：指向要注册的SPI设备驱动程序的指针。
2. 返回值：
	- 0：成功
	- 负数：错误码

#### 3.2.6 spi\_unregister\_driver( )

```c
//从系统中注销一个SPI设备驱动程序
void spi_unregister_driver(struct spi_driver *sdrv);
12
```
1. 参数：
2. sdrv：指向要注销的SPI设备驱动程序的指针

### 3.3 SPI驱动的信息传递

  spi\_message通过成员变量queue将一系列的spi\_message串联起来，第一个spi\_message挂在spi\_controller结构体的queue下面。除此之外， spi\_message中的transfers\_list成员变量也可以在不同的spi\_transfer之间相互串联。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3eabc275ad27f6695cb66ecd8d2e63ed.png)  
**结构体之间的关系**  
  spi\_transfer 和 spi\_message：一个 spi\_message 结构体包含多个 spi\_transfer 结构体，通过 transfers\_list将它们串联起来。这表示一个 SPI 事务中可以包含多个数据传输操作。  
  spi\_message 和 spi\_controller：一个 spi\_message 通过 SPI 控制器（spi\_controller）进行处理。spi\_controller 的 transfer 函数会接收一个 spi\_message，并按照 spi\_message 中定义的顺序执行所有 spi\_transfer 操作。  
**数据传输流程**  
流程示例

1. 创建一个 spi\_message 结构体，并添加多个 spi\_transfer 到这个 spi\_message 中。
2. 将 spi\_message 提交给 SPI 子系统。
3. SPI 子系统找到合适的 spi\_controller，并调用其transfer 函数来处理 spi\_message。
4. spi\_controller 按顺序处理 spi\_message 中的每个spi\_transfer，并进行实际的数据传输。
5. 当所有 spi\_transfer 完成后，调用 spi\_message 的complete 回调函数（如果有的话）。  
	**数据结构体切换的问题**  
	  在 SPI 子系统中，通过 spi\_sync/spi\_async函数进行消息传输时，每次调用 spi\_sync/spi\_async都会处理一个完整的 spi\_message 结构体，包含多个 spi\_transfer 结构体。这意味着如果你需要在传输过程中切换不同的 spi\_message传输操作，需要通过多个spi\_sync/spi\_async来实现，而不能像 spi\_transfer 那样提前多次利用spi\_message\_add\_tail来制定顺序，然后使用spi\_sync/spi\_async统一进行数据输出。
```c
//示例
static int spi_example_transfer(struct spi_device *spi)
{
    int ret;

    // 第一个 spi_message
    struct spi_message msg1;
    u8 tx_buf1[] = {0x01, 0x02, 0x03, 0x04};
    struct spi_transfer tx_transfer1 = {
        .tx_buf = tx_buf1,
        .rx_buf = NULL,
        .len = sizeof(tx_buf1),
        .cs_change = 1,    // 在传输完成后改变 CS 线
        .delay_usecs = 10, // 传输完成后延迟 10 微秒
        .speed_hz = spi->max_speed_hz,
        .bits_per_word = 8,
    };

    spi_message_init(&msg1);
    spi_message_add_tail(&tx_transfer1, &msg1);

    // 提交第一个 spi_message
    ret = spi_sync(spi, &msg1);
    if (ret) {
        dev_err(&spi->dev, "SPI transfer 1 failed: %d\n", ret);
        return ret;
    }

    // 第二个 spi_message
    struct spi_message msg2;
    u8 tx_buf2[] = {0x05, 0x06, 0x07, 0x08};
    u8 rx_buf2[4];
    struct spi_transfer tx_transfer2 = {
        .tx_buf = tx_buf2,
        .rx_buf = NULL,
        .len = sizeof(tx_buf2),
        .cs_change = 0,
        .delay_usecs = 0,
        .speed_hz = spi->max_speed_hz,
        .bits_per_word = 8,
    };
    struct spi_transfer rx_transfer2 = {
        .tx_buf = NULL,
        .rx_buf = rx_buf2,
        .len = sizeof(rx_buf2),
        .cs_change = 0,
        .delay_usecs = 0,
        .speed_hz = spi->max_speed_hz,
        .bits_per_word = 8,
    };

    spi_message_init(&msg2);
    spi_message_add_tail(&tx_transfer2, &msg2);
    spi_message_add_tail(&rx_transfer2, &msg2);

    // 提交第二个 spi_message
    ret = spi_sync(spi, &msg2);
    if (ret) {
        dev_err(&spi->dev, "SPI transfer 2 failed: %d\n", ret);
        return ret;
    }

    // 处理接收到的数据
    for (int i = 0; i < sizeof(rx_buf2); i++) {
        pr_info("Received byte %d: %02x\n", i, rx_buf2[i]);
    }

    return 0;
}

12345678910111213141516171819202122232425262728293031323334353637383940414243444546474849505152535455565758596061626364656667686970
```

### 3.4 SPI驱动的设计框架

  本次实验大致采用SPI驱动和字符设备，这里着重讲一下这部分的设计思路：

1. 本实验采用设备树匹配的方式进行匹配，故而需要设置spi\_driver结构体。
```c
//指定ID匹配表
static const struct spi_device_id oled_device_id[] = {
    {"fire,spi_oled", 0},
    {}
};

//指定设备树匹配表
static const struct of_device_id oled_of_match_table[] = {
    {.compatible = "fire,spi_oled"},
    {}
};

//spi总线设备结构体
struct spi_driver oled_driver = {
    .probe = oled_probe,
    .remove = oled_remove,
    .id_table = oled_device_id,
    .driver = {
            .name = "myspi",
            .owner = THIS_MODULE,
            .of_match_table = of_match_ptr(oled_of_match_table),
    },
};
1234567891011121314151617181920212223
```
1. 出入口函数的编写，这里我们采用字符设备的写法，需要编写module\_init和module\_exti，并且在其中分别使用spi\_register\_driver( )函数和spi\_unregister\_driver( )函数进行spi总线的注册和注销。
2. 字符设备相关内容的编写，即在module\_init进行alloc\_chrdev\_region(内存申请)、cdev\_init(字符设备的申请)，cdev\_add(字符设备的添加)、class\_create(类的创建)、device\_create(设备的创建)；在module\_exti中进行device\_destroy(设备删除)、class\_destroy(清除类)、cdev\_del(清除设备号)、unregister\_chrdev\_region(注销字符设备)；及各种资源的释放。
3. probe函数的编写，这部分主要是利用of\_get\_named\_gpio( )进行申请gpio、gpio\_request( )和gpio\_direction\_output( )进行函数控制D/C引脚、以及通过spi\_setup( )初始化spi。
4. remove函数的编写，这部分与probe函数对应即可，利用gpio\_free( )释放gpio资源。
5. 编写operations结构体相关函数，包括open、write、read、release。

### 3.5 具体功能的实现

#### 3.5.1 \_init函数和\_exit函数

```c
static int __init oled_driver_init(void)
{
    int ret = 0;
    printk("\t driver has entered! \n");

    ret = alloc_chrdev_region(&oled_devno, 0, DEV_CNT, DEV_NAME);
    if (ret < 0) {
        printk("\t alloc_chrdev_region err! \n");
        goto alloc_err;
    }

    oled_chr_dev.owner = THIS_MODULE;
    cdev_init(&oled_chr_dev, &oled_chr_dev_fops);

    ret = cdev_add(&oled_chr_dev, oled_devno, DEV_CNT);
    if (ret < 0) {
        printk("\t cdev_add err! \n");
        goto add_err;
    }

    class_oled = class_create(THIS_MODULE, DEV_NAME);
    if (IS_ERR(class_oled)) {
        ret = PTR_ERR(class_oled);
        printk("\t class_create err! \n");
        goto class_err;
    }

    device_oled = device_create(class_oled, NULL, oled_devno, NULL, DEV_NAME);
    if (IS_ERR(device_oled)) {
        ret = PTR_ERR(device_oled);
        printk("\t device_create err! \n");
        goto device_err;
    }

    ret = spi_register_driver(&oled_driver);
    if (ret < 0) {
        printk("\t spi_register_driver err! \n");
        goto spi_err;
    }

    return 0;

spi_err:
    device_destroy(class_oled, oled_devno);
device_err:
    class_destroy(class_oled);
class_err:
    cdev_del(&oled_chr_dev);
add_err:
    unregister_chrdev_region(oled_devno, DEV_CNT);
alloc_err:
    return ret;
}
module_init(oled_driver_init);

static void __exit oled_driver_exit(void)
{
    spi_unregister_driver(&oled_driver);
    device_destroy(class_oled, oled_devno);         //清除设备
    class_destroy(class_oled);                      //清除类
    cdev_del(&oled_chr_dev);                        //清除设备号
    unregister_chrdev_region(oled_devno, DEV_CNT);  //取消注册字符设备
    printk("\t driver has exited! \n");
}
module_exit(oled_driver_exit);
1234567891011121314151617181920212223242526272829303132333435363738394041424344454647484950515253545556575859606162636465
```

#### 3.5.2.probe函数

```c
static int oled_probe(struct spi_device *spi_device)
{
    int ret;
    struct device_node *node = spi_device->dev.of_node;
    printk("\t device has matched! \n");

    spi_cs = of_get_named_gpio(node, "dc_control_pin", 0); //进行申请gpio
    printk("\t spi_cs is %d \n", spi_cs);

    ret = gpio_request(spi_cs, "spi_cs");
    if (ret < 0) {
        printk("\t gpio_request err! \n");
        return ret;
    }

    gpio_direction_output(spi_cs, 1);

    /*初始化spi*/
    spi_bus_device = spi_device;
    spi_bus_device->mode = SPI_MODE_0;
    spi_bus_device->max_speed_hz = 2000000;
    ret = spi_setup(spi_bus_device);
    if (ret < 0) {
        printk("\t spi_setup err! \n");
        goto spi_err;
    }

    printk("spibus has init successfully\n");
    printk("max_speed_hz = %d\n", spi_bus_device->max_speed_hz);
    printk("chip_select = %d\n", (int)spi_bus_device->chip_select);
    printk("bits_per_word = %d\n", (int)spi_bus_device->bits_per_word);
    printk("mode = %02X\n", spi_bus_device->mode);
    printk("cs_gpio = %02X\n", spi_bus_device->cs_gpio);
    return 0;

spi_err:
    gpio_free(spi_cs);
    return ret;
}
123456789101112131415161718192021222324252627282930313233343536373839
```

#### 3.5.3.remove函数

```c
static int oled_remove(struct spi_device *spi_device)
{
    printk("device has removed!\n");
    gpio_free(spi_cs);
    return 0;
}
123456
```

#### 3.5.4 数据传输函数

```c
//向 oled 发送一个字节
static int oled_send_one_u8(struct spi_device *spi_device, u8 data)
{
    int error = 0;
    u8 tx_data = data;
    struct spi_message message;   //定义发送的消息
    struct spi_transfer *transfer; //定义传输结构体

    //设置 D/C引脚为高电平
    gpio_direction_output(spi_cs, 1);

    //申请空间
    transfer = kzalloc(sizeof(struct spi_transfer), GFP_KERNEL);
    if (!transfer) {
        printk("kzalloc error!\n");
        return -ENOMEM;
    }

    //填充message和transfer结构体
    transfer->tx_buf = &tx_data;
    transfer->len = 1;
    spi_message_init(&message);
    spi_message_add_tail(transfer, &message);
    
    //同步发送 SPI 消息
    error = spi_sync(spi_device, &message);
    kfree(transfer);
    if (error != 0)
    {
        printk("spi_sync error! \n");
        return -1;
    }
    return 0;
}
12345678910111213141516171819202122232425262728293031323334
```

---

**免责声明：本内容部分参考野火科技及其他相关公开资料，若有侵权或者勘误请联系作者。**

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/139804156

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