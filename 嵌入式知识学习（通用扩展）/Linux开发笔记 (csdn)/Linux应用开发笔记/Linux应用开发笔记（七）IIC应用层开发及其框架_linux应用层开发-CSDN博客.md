---
title: "Linux应用开发笔记（七）IIC应用层开发及其框架_linux应用层开发-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/137697219?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读1.6k次，点赞31次，收藏40次。本文介绍了Linux平台下的IIC通信体系，重点讲解了i2c-tools工具集的作用，包括i2cdetect、i2cget、i2cset等命令的用途。同时详细剖析了IIC框架结构，涉及i2c_adapter、i2c_algorithm、i2c_client和i2c_msg等关键结构体。文章还展示了如何在应用层使用ioctl函数进行设备配置和读写操作，如OLED初始化示例。"
tags:
  - "clippings"
---
本文介绍了Linux平台下的IIC通信体系，重点讲解了i2c-tools工具集的作用，包括i2cdetect、i2cget、i2cset等命令的用途。同时详细剖析了IIC框架结构，涉及i2c\_adapter、i2c\_algorithm、i2c\_client和i2c\_msg等关键结构体。文章还展示了如何在应用层使用ioctl函数进行设备配置和读写操作，如OLED初始化示例。

摘要生成于 [C知道](https://ai.csdn.net/?utm_source=cknow_pc_ai_abstract) ，由 DeepSeek-R1 满血版支持， [前往体验 >](https://ai.csdn.net/?utm_source=cknow_pc_ai_abstract)

---

## 前言

  之前笔者在 STM32 和FPGA中已经多次讲述了 [IIC](https://so.csdn.net/so/search?q=IIC&spm=1001.2101.3001.7020) 的基础知识，这里不在展开“扫盲”，感兴趣的朋友可以看一下往期笔记，此次仅仅带大家简单回顾并展开Linux下的IIC体系的学习。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/70ed9114f0eba960e2b50921624429d7.png)  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/169cbe6073ee58867f0c8a131d402b37.png)

## 一、IIC 第三方工具- i2c-tools

  i2c-tools是一个专门用于调试I2C的开源工具集。它提供了一组 命令行工具 ，使得用户可以在应用层实现对I2C设备的扫描、读取、写入等操作，常用于对I2C设备进行交互、调试和测试。这些工具在Linux操作系统上广泛使用，并由于Android系统的内核也是Linux，因此也可以方便地移植到Android中使用。

```c
//安装iic-tools
sudo apt install i2c-tools wget gcc -y
12
```

  i2c-tools工具集中的一些主要工具包括：

- i2cdetect：用于扫描I2C总线并列出已连接的设备及其地址。

| 参数名称 | 功能 |
| --- | --- |
| \-F i2cbus | 查询i2c总线的功能，参数i2cbus表示i2c总线 |
| \-V | 打印软件 |
| \-l | 检测当前系统有几组i2c总线 |

- i2cget：用于从指定I2C设备的寄存器中读取数据。  
	格式：i2cget \[-f\] \[-y\] i2cbus chip-address \[data-address \[mode\]\]

| 参数名称 | 功能 |
| --- | --- |
| \-f | 强制访问设备 |
| \-y i2cbus | 关闭交互模式，使用该参数时，不会提示警告信息 |
| \-i2cbus | 指定i2c总线的编号 |
| \-chip-address | i2c设备地址 |
| \-data-address | 设备的寄存器的地址 |
| \-mode | 设备的寄存器的地址 |
| \-y | 关闭交互模式，使用该参数时，不会提示警告信息 |

- i2cset：用于向指定I2C设备的寄存器中写入数据。  
	格式：i2cset \[-f\] \[-y\] \[-m mask\] \[-r\] i2cbus chip-address data-address \[value\] … \[mode\]
- i2cdump：用于以十六进制格式显示I2C设备的寄存器内容，即读取某个I2C设备所有寄存器的值。  
	格式：i2cdump \[-f\] \[-r first-last\] \[-y\] i2cbus address \[mode \[bank \[bankreg\]\]\]
- i2ctransfer：用于执行复杂的I2C传输操作，如一次性读写多个字节。

  这些工具在调试新的设备驱动时特别有用，因为它们允许用户直接修改和读取设备寄存器的值，从而观察结果现象。与传统的修改驱动代码、编译、下载、运行和查看结果的方法相比，使用i2c-tools可以大大节省时间，尤其是当每次只需要修改一个位（bit）时。

## 二、IIC框架

  和TTY框架类似，IIC的框架下也分为应用层，设备驱动和控制器驱动，其中APP只负责“单纯的用”，而设备驱动则主要编写地址格式、数据格式、判别标准及一些指令信号，最后由控制驱动需要判断向什么地址(设备/存储)发什么数据。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3daa8f831dd10c4205a2d6af38683190.png)  
如果再细化一下，可以分为以下四层：

- 第一层：提供i2c adapter的 硬件 驱动，探测，初始化i2c adapter（如申请i2c的io地址和中断号）驱动soc控制的i2c adapter在硬件上产生信号（stop，start，ack）以及处理I2c中断。覆盖图中硬件实现层。
- 第二层：提供i2c adapter 的algorithm，用具体适配器的xxx\_xferf()函数来填充i2c\_algorithm的master\_xfer函数指针，并把赋值后的i2c\_algorithm再赋值给i2c\_adapter的algo指针。覆盖图中的访问抽象层、i2c核心层。
- 第三层：实现i2c设备驱动中的i2c\_driver接口，用具体的i2c device设备attch\_adapter();detach\_adapter();方法赋值给i2c\_driver的成员函数指针。实现设备device与总线（或者叫adapter）的挂接。覆盖图中driver驱动层。
- 第四层：实现i2c设备所对应的具体device的驱动，i2c\_driver只是实现设备与总线的挂接，而挂接在总线上的设备则是千差万别的，所以要实现具体的设备device的read（），write（），ioctl();等方法，赋值给file\_operations,然后注册字符设备（多数是字符设备），覆盖图中的driver驱动层。

  其中第一层和第二层又叫i2c总线驱动（bus），第三第四属于i2c设备驱动（device driver）。

## 三、IIC的几个重要结构体

  上一小节中提到了几个重要的结构体，这部分将展开讲述一下。

### 1\. i2c\_adapter

  i2c\_adapter结构体用于表示一个I2C适配器，即I2C总线控制器，具体对应的结构体如下：

```c
struct i2c_adapter {
    struct module *owner;
    unsigned int class;               /* classes to allow probing for */
    const struct i2c_algorithm *algo; /* the algorithm to access the bus */
    void *algo_data;

    /* data fields that are valid for all devices   */
    struct rt_mutex bus_lock;

    int timeout;                    /* in jiffies */
    int retries;
    struct device dev;              /* the adapter device */

    int nr;
    char name[48];
    struct completion dev_released;

    struct mutex userspace_clients_lock;
    struct list_head userspace_clients;

    struct i2c_bus_recovery_info *bus_recovery_info;
    const struct i2c_adapter_quirks *quirks;
12345678910111213141516171819202122
```
- algo：指向i2c\_algorithm结构体的指针，该结构体包含了I2C适配器的算法和函数实现，如读写操作等。
- dev：表示与I2C适配器关联的设备。这个字段通常包含了设备的名称、设备树节点、父设备等信息。
- name：适配器的名称，通常用于调试和日志记录。
- class：适配器的类，用于区分不同类型的适配器。
- features：适配器支持的特性标志位，如中断处理、DMA等。
- quirks：适配器的特殊行为或限制，用于处理某些特定硬件的异常情况。

### 2\. i2c\_algorithm

  i2c\_algorithm结构体包含了I2C适配器的 算法 和函数实现，以下是一些关键的字段：

```c
struct i2c_algorithm {
    /* If an adapter algorithm can't do I2C-level access, set master_xfer
       to NULL. If an adapter algorithm can do SMBus access, set
       smbus_xfer. If set to NULL, the SMBus protocol is simulated
       using common I2C messages */
    /* master_xfer should return the number of messages successfully
       processed, or a negative value on error */
    int (*master_xfer)(struct i2c_adapter *adap, struct i2c_msg *msgs,
                       int num);
    int (*smbus_xfer) (struct i2c_adapter *adap, u16 addr,
                       unsigned short flags, char read_write,
                       u8 command, int size, union i2c_smbus_data *data);

    /* To determine what the adapter supports */
    u32 (*functionality) (struct i2c_adapter *);

#if IS_ENABLED(CONFIG_I2C_SLAVE)
    int (*reg_slave)(struct i2c_client *client);
    int (*unreg_slave)(struct i2c_client *client);
#endif
};
123456789101112131415161718192021
```
- master\_xfer：I2C适配器的传输函数，用于执行与I2C设备之间的通信。
- smbus\_xfer：SMBus（系统管理总线）的传输函数，用于执行SMBus协议下的通信。

### 3\. i2c\_client

  i2c\_client结构体用于表示一个连接到I2C总线的设备，包含：

```c
struct i2c_client {
            unsigned short flags;           /* div., see below              */
            unsigned short addr;            /* chip address - NOTE: 7bit    */

            char name[I2C_NAME_SIZE];
            struct i2c_adapter *adapter;    /* the adapter we sit on        */
            struct device dev;              /* the device structure         */
            int init_irq;                   /* irq set at initialization    */
            int irq;                        /* irq issued by device         */
            struct list_head detected;
            #if IS_ENABLED(CONFIG_I2C_SLAVE)
                    i2c_slave_cb_t slave_cb;        /* callback for slave mode      */
            #endif
    };
1234567891011121314
```
- adapter：指向与设备关联的I2C适配器的指针。
- addr：设备的I2C地址。
- name\[I2C\_NAME\_SIZE\]：设备的名称。
- dev：表示与I2C设备关联的设备，包含了设备树节点、驱动等信息。
- driver：指向与设备关联的驱动程序的指针。
- init\_irq： 作为从设备时的发送函数。
- irq： 表示该设备生成的中断号。
- detected： struct list\_head i2c的成员\_驱动程序.客户端列表或i2c核心的用户空间设备列表。
- slave\_cb： 使用适配器的I2C从模式时回调。适配器调用它来将从属事件传递给从属驱动程序。i2c\_客户端识别连接到i2c总线的单个设备(即芯片)。暴露在Linux下的行为是由管理设备的驱动程序定义的。

### 4\. i2c\_msg

  i2c\_msg结构体用于描述在I2C总线上传输的单条消息，以下是一些关键的字段：

```c
struct i2c_msg {
    __u16 addr;               /* slave address                        */
    __u16 flags;
    __u16 len;              /* msg length                           */
    __u8 *buf;              /* pointer to msg data                  */
        ...
};
1234567
```
- \_\_u16 addr：目标设备的I2C地址。
- \_\_u16 flags：消息的标志位，如读/写操作、是否使用SMBus协议等。
- \_\_u16 len：消息的长度，即要发送或接收的数据字节数。
- \_\_u8 \*buf：指向要发送或接收的数据的缓冲区的指针。

## 四、应用层代码

  与 FPGA 和STM32类似，在应用层上我们主要编写读写函数，然后根据不同的外设进行组合，例如：OLED的初始化就是一堆write函数的组合，这里便不具体编写项目了。  
  在编写应用程序时需要使用ioctl函数设置i2c相关配置，其函数原型如下

```c
//执行设备特定的操作
 #include <sys/ioctl.h>
 int ioctl(int fd, unsigned long request, ...);
123
```

  其中， request 的参数可选项如下所示：

| 参数名称 | 功能 |
| --- | --- |
| I2C\_RETRIES | 设置收不到ACK时的重试次数，默认为1 |
| I2C\_TIMEOUT | 设置超时时限的jiffies |
| I2C\_SLAVE | 设置从机地址 |
| I2C\_SLAVE\_FORCE | 强制设置从机地址 |
| I2C\_TENBIT | 选择地址长度0为7位地址，非0为10位 |

- i2c\_write( )函数
```c
static int i2c_write(int fd, unsigned char addr,unsigned char reg,unsigned char val)
{
   int retries;
   unsigned char data[2];

   data[0] = reg;
   data[1] = val;

   //设置地址长度：0为7位地址
   ioctl(fd,I2C_TENBIT,0);

   //设置从机地址
   if (ioctl(fd,I2C_SLAVE,addr) < 0){
      printf("fail to set i2c device slave address!\n");
      close(fd);
      return -1;
   }

   //设置收不到ACK时的重试次数
   ioctl(fd,I2C_RETRIES,5);

   if (write(fd, data, 2) == 2){
      return 0;
   }
   else{
      return -1;
   }
}
12345678910111213141516171819202122232425262728
```
- i2c\_read( )函数
```c
static int i2c_read(int fd, uint8_t addr,uint8_t reg,uint8_t * val)
{
    int retries;

    //设置地址长度：0为7位地址
    ioctl(fd,I2C_TENBIT,0);

    //设置从机地址
    if (ioctl(fd,I2C_SLAVE,addr) < 0){
        printf("fail to set i2c device slave address!\n");
        close(fd);
        return -1;
    }

    //设置收不到ACK时的重试次数
    ioctl(fd,I2C_RETRIES,5);

    if (write(fd, &reg, 1) == 1){
        if (read(fd, val, 1) == 1){
                return 0;
        }
    }
    else{
        return -1;
    }
}
1234567891011121314151617181920212223242526
```

**注：需要区分write和read中参数的不同，这里的最后一项分别为要写入的数据和拷贝数据的地址。val是一个uint8\_t类型的变量，你通过取它的地址&val作为参数传递给i2c\_read函数。如果读取成功，val将会包含从IIC设备读取的数据。**

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/137697219

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