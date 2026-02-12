---
title: "Linux驱动开发笔记（十一）tty子系统及其驱动_linux tty子系统-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/139844828?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读1.4k次，点赞15次，收藏31次。之前已经讲过应用层的应用，接下来我们继续进行驱动的学习。其实实际上我们很少主动进行串口的驱动编写，通常情况下只需要进行应用层的应用就可以了，网络上相关的驱动内容介绍也较少，这里仅作了解并简单了解一下架构即可。_linux tty子系统"
tags:
  - "clippings"
---
---

## 前言

  之前已经讲过应用层的应用，接下来我们继续进行驱动的学习。其实实际上我们很少主动进行串口的驱动编写，通常情况下只需要进行应用层的应用就可以了，网络上相关的驱动内容介绍也较少，这里仅作了解并简单了解一下架构即可。

---

## 一、串口驱动框架

  串口驱动没有什么主机端和设备端之分，就只有一个串口驱动，而且这个驱动也已经由厂商已经编写好了，我们真正要做的就是在 [设备树](https://so.csdn.net/so/search?q=%E8%AE%BE%E5%A4%87%E6%A0%91&spm=1001.2101.3001.7020) 中添加所要使用的串口节点信息。当系统启动以后串口驱动和设备匹配成功，相应的串口就会被驱动起来，生成/dev/ttymxcX(X=0….n)文件。  
  这部分内容还是比较多的，笔者发现这个文章讲述的还是很详细的，感兴趣可以自行查阅，这里不再赘述： [框架详细介绍](https://blog.csdn.net/lf282481431/article/details/135278043?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522171895498116800180692772%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=171895498116800180692772&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~rank_v31_ecpm-11-135278043-null-null.142%5Ev100%5Epc_search_result_base4&utm_term=linux%E4%B8%B2%E5%8F%A3%E9%A9%B1%E5%8A%A8&spm=1018.2226.3001.4187)

### 1.1 核心数据结构

  对于串口驱动来说，实际上重要的 结构体 只有uart\_drive和uart\_port，这里可能根据不同的厂商所采用的名称不大一样，但内容差不多，比如在rk3568中，官方提供的uart驱动程序位8250通用串口程序，其为uart\_port结构体提供了扩展后的uart\_8250\_port，包含8250 UART特有的属性和操作。  
  这部分内容保存于内核中的下列文件中，感兴趣可以自行查阅：

- serial\_core.c：包含UART核心层的实现。
- 8250.c：包含8250 UART特定操作的实现。
- 8250\_port.c：包含8250 UART端口的具体实现。

  uart\_driver结构体用于描述一个UART驱动程序，它通常包含一些基础的信息和操作函数。

```c
struct uart_driver {
    struct module *owner;               // 设备驱动模块的所有者
    const char *driver_name;            // 驱动程序的名称
    const char *dev_name;               // 设备名称
    int major;                          // 设备主设备号
    int minor;                          // 设备次设备号
    int nr;                             // 该驱动程序支持的设备数量
    struct console *cons;               // 控制台相关信息
    struct uart_ops *ops;               // UART操作函数集合
    
    struct uart_state *state;
    struct tty_driver *tty_driver;
};
12345678910111213
```

  uart\_8250\_port结构体用于描述8250 UART端口的具体信息和操作方法。

```c
struct uart_8250_port {
    struct uart_port port;              // 通用UART端口结构体
    struct timer_list timer;            // 定时器用于处理超时
    unsigned int capabilities;          // 硬件能力
    unsigned int mcr;                   // 调制解调器控制寄存器
    unsigned int lsr;                   // 线路状态寄存器
    unsigned int msr;                   // 调制解调器状态寄存器
    unsigned int icr;                   // 中断控制寄存器
    unsigned int lcr;                   // 线路控制寄存器
    unsigned int fcr;                   // FIFO控制寄存器
    unsigned int ier;                   // 中断使能寄存器
    unsigned char mcr_mask;             // 调制解调器控制寄存器掩码
    unsigned char mcr_force;            // 调制解调器控制寄存器强制值
    unsigned char lsr_break_flag;       // 断开标志
    unsigned char bugs;                 // 硬件错误标志
    unsigned int tx_loadsz;             // 发送FIFO加载大小
    unsigned int acr;                   // 额外控制寄存器
    unsigned int ier_mask;              // 中断使能寄存器掩码
    unsigned int ier_force;             // 中断使能寄存器强制值
    unsigned int lsr_mask;              // 线路状态寄存器掩码
    unsigned int lsr_break_flag_mask;   // 断开标志掩码
};

//通用结构体，但比较鸡肋
struct uart_port {
 spinlock_t lock; /* port lock */
 unsigned long iobase; /* in/out[bwl] */
 unsigned char __iomem *membase; /* read/write[bwl] */
......
 const struct uart_ops *ops;
 unsigned int custom_divisor;
 unsigned int line; /* port index */
 unsigned int minor;
 resource_size_t mapbase; /* for ioremap */
 resource_size_t mapsize;
 struct device *dev; /* parent device */
123456789101112131415161718192021222324252627282930313233343536
```

  这里补充一下在uart\_driver提到的实现控制台打印功能必须要注册的结构体 console 和将uart\_port与对应的circ\_buf联系起来的uart\_state结构体。

```c
struct console {
      char name[16];
      void(*write)(struct console *，const char *, unsigined);
      int (*read)(struct console *, char *, unsigned);
      struct tty_driver *(struct console *,int*);
      void (*unblank)(void);
      int  (*setup)(struct console *, char *);
      int  (*early_setup)(void);
      short  flags;
      short  index; /*用来指定该console使用哪一个uart port (对应的uart_port中的line),如果为-1,kernel会自动选择第一个uart port*/
      int   cflag;
      void  *data;
      struct   console *next;
};

/*uart_state有两个成员在底层串口驱动会用到，即xmit和port。
用户空间程序通过串口发送数据时，上层驱动将用户数据保存在xmit;而串口发送中断处理函数就是通过xmit获取到用户数据并将它们发送出去。
串口接收中断处理函数需要通过port将接收到的数据传递给线路规程层。
*/
struct uart_state {
       struct  tty_port  port;
       
       enum uart_pm_state   pm_state;
       struct circ_buf     xmit;
       
       struct uart_port     *uart_port; /*对应于一个串口设备*/
}；
123456789101112131415161718192021222324252627
```

  uart\_ops结构体几乎涵盖了驱动可对串口的所有操作：

```c
struct uart_ops {
        unsigned int    (*tx_empty)(struct uart_port *);
        void            (*set_mctrl)(struct uart_port *, unsigned int mctrl);
        unsigned int    (*get_mctrl)(struct uart_port *);
        void            (*stop_tx)(struct uart_port *);
        void            (*start_tx)(struct uart_port *);
        void            (*throttle)(struct uart_port *);
        void            (*unthrottle)(struct uart_port *);
        void            (*send_xchar)(struct uart_port *, char ch);
        void            (*stop_rx)(struct uart_port *);
        void            (*enable_ms)(struct uart_port *);
        void            (*break_ctl)(struct uart_port *, int ctl);
        int             (*startup)(struct uart_port *);
        void            (*shutdown)(struct uart_port *);
        void            (*flush_buffer)(struct uart_port *);
        void            (*set_termios)(struct uart_port *, struct ktermios *new,
                                       struct ktermios *old);
        void            (*set_ldisc)(struct uart_port *, int new);
        void            (*pm)(struct uart_port *, unsigned int state,
                              unsigned int oldstate);
        int             (*set_wake)(struct uart_port *, unsigned int state);
 
        /*
         * Return a string describing the type of the port
         */
        const char      *(*type)(struct uart_port *);
 
        /*
         * Release IO and memory resources used by the port.
         * This includes iounmap if necessary.
         */
        void            (*release_port)(struct uart_port *);
 
        /*
         * Request IO and memory resources used by the port.
         * This includes iomapping the port if necessary.
         */
        int             (*request_port)(struct uart_port *);
        void            (*config_port)(struct uart_port *, int);
        int             (*verify_port)(struct uart_port *, struct serial_struct *);
        int             (*ioctl)(struct uart_port *, unsigned int, unsigned long);
#ifdef CONFIG_CONSOLE_POLL
        int             (*poll_init)(struct uart_port *);
        void            (*poll_put_char)(struct uart_port *, unsigned char);
        int             (*poll_get_char)(struct uart_port *);
#endif
};
1234567891011121314151617181920212223242526272829303132333435363738394041424344454647
```

### 1.2 数据处理流程

  相较于前面学习的spi子系统和iic子系统，uart驱动通常情况不需要根据协议的时序额外编写新的传输函数，这里可以直接提供write函数和read函数实现数据的互传。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/4f771aad098af6a068730c9fc896a843.png)  
  这部分的内容我们在应用层实验的时候已经详细介绍过了，感兴趣可以回顾一下。

## 二、驱动编写

  我们这里采用的8250通用驱动，对于不同驱动其函数名称和入口参数可能有所不同，这里我们简单学习梳理一下框架即可，通常来说我们是只需要进行应用层的编写。

### 1\. 设备树的修改

代码如下（示例）：

```bash
uart3: serial@fe670000 {
         compatible = "rockchip,rk3568-uart", "snps,dw-apb-uart";
         reg = <0x0 0xfe670000 0x0 0x100>;
         interrupts = <GIC_SPI 119 IRQ_TYPE_LEVEL_HIGH>;
         clocks = <&cru SCLK_UART3>, <&cru PCLK_UART3>;
         clock-names = "baudclk", "apb_pclk";
         reg-shift = <2>;
         reg-io-width = <4>;
         dmas = <&dmac0 6>, <&dmac0 7>;
         pinctrl-names = "default";
         pinctrl-0 = <&uart3m0_xfer>;
         status = "disabled";
     };

//uart3的复用
uart3 {
         /omit-if-no-ref/
        uart3m0_xfer: uart3m0-xfer {
             rockchip,pins =
                 /* uart3_rxm0 */
                 <1 RK_PA0 2 &pcfg_pull_up>,
                 /* uart3_txm0 */
                 <1 RK_PA1 2 &pcfg_pull_up>;
        };
 
         /omit-if-no-ref/
         uart3m0_ctsn: uart3m0-ctsn {
             rockchip,pins =
                /* uart3m0_ctsn */
                <1 RK_PA3 2 &pcfg_pull_none>;
         };

         /omit-if-no-ref/
         uart3m0_rtsn: uart3m0-rtsn {
             rockchip,pins =
                 /* uart3m0_rtsn */
                  <1 RK_PA2 2 &pcfg_pull_none>;
        };
 
         /omit-if-no-ref/
         uart3m1_xfer: uart3m1-xfer {
             rockchip,pins =
                 /* uart3_rxm1 */
                 <3 RK_PC0 4 &pcfg_pull_up>,
                 /* uart3_txm1 */
                 <3 RK_PB7 4 &pcfg_pull_up>;
         };
     };

12345678910111213141516171819202122232425262728293031323334353637383940414243444546474849
```

  接着根据我们的需要继续编写即可，泰山派这里已经默认将uart3配置好了，这里可以直接调用。

```bash
//用户串口3
&uart3 {
    status = "okay";
    pinctrl-names = "default";
    pinctrl-0 = <&uart3m1_xfer>;
     ...
 };

12345678
```

### 2\. 相关API函数

```c
//注册 uart_driver
int uart_register_driver(struct uart_driver *drv)
12
```
- 参数
	- drv ：要注册的 uart\_driver
- 返回值
	- 成功：0
	- 失败：负值
```c
//注销uart_driver
void uart_unregister_driver(struct uart_driver *drv)
12
```
- 参数
	- drv ：要注销的 uart\_driver
- 返回值：无
```c
//
int serial8250_register_8250_port(struct uart_8250_port *up);
12
```
- 参数
	- up：指向 uart\_8250\_port 结构体的指针，该结构体包含了要注册的 8250 UART 端口的所有必要信息。
- 返回值
	- 成功：端口的线路号（line）
	- 失败：错误码
```c
void serial8250_unregister_port(int line);
1
```
- 参数
	- line：要注销的 UART 端口的线路号（line），通常是在调用 serial8250\_register\_8250\_port 时返回的值。
- 返回值：无

### 3\. 驱动框架

  实际上，我们可以简单地将uart驱动理解为是一个 platform 驱动在驱动入口函数中调用uart\_register\_driver 函数向 Linux 内核注册 uart\_driver，在驱动出口函数中调用uart\_unregister\_driver 函数注销掉前面注册的 uart\_driver，当设备和驱动匹配成功以后进入probe 函数，此函数的重点工作就是初始化uart\_8250\_port(uart\_port)，然后将其添加到对应的uart\_driver 中。在初始化uart\_port过程中，设置 uart\_ops 为对应的 XXX\_ops即可。

### 4\. 具体功能的实现

#### 4.1 出入口函数的编写

```c
static int __init my_uart_init(void)
{
    int ret;

    // 初始化uart_driver结构体
    my_uart_driver = (struct uart_driver) {
        .owner      = THIS_MODULE,
        .driver_name= DRIVER_NAME,
        .dev_name   = "ttyMY",
        .major      = TTY_MAJOR,
        .minor      = 64,
        .nr         = 1,
    };

    // 注册UART驱动
    ret = uart_register_driver(&my_uart_driver);
    if (ret)
        return ret;

    // 初始化uart_8250_port结构体
    my_uart_port.port = (struct uart_port) {
        .iotype     = UPIO_PORT,
        .mapbase    = UART_BASE,
        .irq        = UART_IRQ,
        .uartclk    = UART_CLOCK,
        .fifosize   = 16,
        .ops        = &my_uart_ops,
        .line       = 0,
    };

    // 注册8250 UART端口
    line = serial8250_register_8250_port(&my_uart_port);
    if (line)
        uart_unregister_driver(&my_uart_driver);

    return line;
}

static void __exit my_uart_exit(void)
{
    serial8250_unregister_port(line);
    uart_unregister_driver(&my_uart_driver);
}

module_init(my_uart_init);
module_exit(my_uart_exit);
12345678910111213141516171819202122232425262728293031323334353637383940414243444546
```

#### 4.2 读写函数

```c
static void my_uart_start_tx(struct uart_port *port)
{
    struct uart_8250_port *up = (struct uart_8250_port *)port;
    unsigned int ier;

    spin_lock_irq(&up->port.lock);

    // 启用发送中断
    ier = serial_in(up, UART_IER);
    serial_out(up, UART_IER, ier | UART_IER_THRI);

    spin_unlock_irq(&up->port.lock);
}

static void my_uart_stop_tx(struct uart_port *port)
{
    struct uart_8250_port *up = (struct uart_8250_port *)port;
    unsigned int ier;

    spin_lock_irq(&up->port.lock);

    // 禁用发送中断
    ier = serial_in(up, UART_IER);
    serial_out(up, UART_IER, ier & ~UART_IER_THRI);

    spin_unlock_irq(&up->port.lock);
}

static irqreturn_t my_uart_interrupt(int irq, void *dev_id)
{
    struct uart_8250_port *up = dev_id;
    unsigned int iir = serial_in(up, UART_IIR);

    // 检查中断类型并处理
    if (!(iir & UART_IIR_NO_INT)) {
        if (iir & UART_IIR_RDI)
            serial8250_rx_chars(up);
        if (iir & UART_IIR_THRI)
            serial8250_tx_chars(up);
        return IRQ_HANDLED;
    }

    return IRQ_NONE;
}
1234567891011121314151617181920212223242526272829303132333435363738394041424344
```

---

**免责声明：本内容部分参考野火科技及其他相关公开资料，若有侵权或者勘误请联系作者。**

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/139844828

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