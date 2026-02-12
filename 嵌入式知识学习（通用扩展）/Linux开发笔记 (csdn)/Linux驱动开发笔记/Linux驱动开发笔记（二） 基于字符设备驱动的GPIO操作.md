---
title: "Linux驱动开发笔记（二） 基于字符设备驱动的GPIO操作_字符设备驱动读写寄存器-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/138665580?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读1.5k次，点赞30次，收藏23次。前段时间我们学习了字符驱动，并实现了字符的回环发送，这部分我们将进行I/O的操作学习，以万能的点亮LED为例。需要设置的寄存器的地址为base+offset，由下图可以知道GPIO1的基地址为：0xFE740000接下来就是确定GPIO的是输入还是输出，我们这里需要的是GPIO_SWPORT_DDR_L。可以看到GPIO_SWPORT_DDR_L的定义情况，这里我们可以重复上面提到的命令行，查看寄存器的设置情况，我们的b0应当是第1x7+1=8位。_字符设备驱动读写寄存器"
tags:
  - "clippings"
---
---

## 前言

  前段时间我们学习了 [字符驱动](https://so.csdn.net/so/search?q=%E5%AD%97%E7%AC%A6%E9%A9%B1%E5%8A%A8&spm=1001.2101.3001.7020) ，并实现了字符的回环发送，这部分我们将进行I/O的操作学习，以万能的点亮LED为例。

## 一、设备驱动的作用与本质

  直接操作 [寄存器](https://so.csdn.net/so/search?q=%E5%AF%84%E5%AD%98%E5%99%A8&spm=1001.2101.3001.7020) 点亮LED和通过驱动程序点亮LED最本质的区别就是有无使用操作系统。 有操作系统的存在则大大降低了应用 软件 与硬件平台的耦合度，它充当了我们硬件与应用软件之间的纽带， 使得应用软件只需要调用 [驱动程序](https://so.csdn.net/so/search?q=%E9%A9%B1%E5%8A%A8%E7%A8%8B%E5%BA%8F&spm=1001.2101.3001.7020) 接口API就可以让硬件去完成要求的开发，而应用软件则不需要关心硬件到底是如何工作的。

### 1\. 驱动的作用

  设备驱动与底层硬件直接打交道，按照硬件设备的具体工作方式读写设备寄存器， 完成设备的轮询、中断处理、DMA通信，进行物理内存向虚拟内存的映射，最终使通信设备能够收发数据， 使显示设备能够显示文字和画面，使存储设备能够记录文件和数据。

### 2\. 有无操作系统的区别

  无操作系统(即裸机)时的设备驱动也就是 **直接操作寄存器的方式控制硬件** ，在这样的系统中，虽然不存在操作系统，但是设备驱动是必须存在的。 一般情况下，对每一种设备驱动都会定义为一个软件模块，包含.h文件和.c文件，前者定义该设备驱动的数据结构并声明外部 函数 ， 后者进行设备驱动的具体实现。其他模块需要使用这个设备的时候，只需要包含设备驱动的头文件然后调用其中的外部接口函数即可。 比如我们在51或者 STM32 中直接看手册查找对应的寄存器，然后往寄存器相应的位写入数据0或1便可以实现LED的亮灭。  
  有操作系统时的设备驱动反观有操作系统。首先，驱动硬件工作的的部分仍然是必不可少的，其次，我们还需要将设备驱动融入内核。 为了实现这种融合，必须在所有的设备驱动中设计面向操作系统内核的接口，这样的接口由操作系统规定，对一类设备而言结构一致，独立于具体的设备，还是以led为例，我们就要将LED灯引脚对应的数据寄存器(物理地址)映射到程序的虚拟地址空间当中，然后我们就可以像操作寄存器一样去操作我们的虚拟地址啦！

## 二、内存管理单元MMU

  MMU是一个实际的硬件，为编程提供了方便统一的内存空间抽象，MMU内部有一个专门存放页表的页表地址寄存器，该寄存器存放着页表的具体位置，这使得只要程序在被分配的虚拟地址范围内进行读写操作，实际上就是对设备(寄存器)的访问，如下图所示。他的主要作用是将 **虚拟地址翻译成真实的物理地址** 同时管理和保护内存， 不同的进程有各自的虚拟地址空间，某个进程中的程序不能修改另外一个进程所使用的物理地址，以此 **使得进程之间互不干扰，相互隔离** 。 总体而言MMU具有如下功能：

- 保护内存： MMU给一些指定的内存块设置了读、写以及可执行的权限，这些权限存储在页表当中，MMU会检查CPU当前所处的是特权模式还是用户模式，如果和操作系统所设置的权限匹配则可以访问，如果CPU要访问一段虚拟地址，则将虚拟地址转换成物理地址，否则将产生异常，防止内存被恶意地修改。
- 提供方便统一的内存空间抽象，实现虚拟地址到物理地址的转换： CPU可以运行在虚拟的内存当中，虚拟内存一般要比实际的物理内存大很多，使得CPU可以运行比较大的应用程序。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/11c32ca53cc36b6a82ec5192292573bd.png#pic_center)  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c889608d6a39a922cdd405bb9f34a062.png#pic_center)

## 三、相关函数

  上面提到了物理地址到虚拟地址的 转换函数 。包括ioremap()地址映射和取消地址映射iounmap()函数。

### 1\. ioremap( )

```c
//用于将物理内存地址映射到内核的虚拟地址空间
void __iomem *ioremap(phys_addr_t phys_addr, unsigned long size)

//定义寄存器物理地址
#define GPIO0_BASE (0xFDD60000)
#define GPIO0_DR (GPIO0_BASE+0x0000)

va_dr = ioremap(GPIO0_DR, 4);    // 将物理地址GPIO0_DR，映射给虚拟地址指针，这段地址大小为4个字节
val = ioread32(va_dr);             //读取该地址的值，保存到临时变量，重新赋值
val |= (0x00400000);             // 设置GPIO0_A6引脚低电平
writel(val, va_dr);                 //把值重新写入到被映射后的虚拟地址当中，实际是往寄存器中写入了数据
1234567891011
```
- 参数：
	- phys\_addr：要映射的物理地址的起始地址
	- size：要映射的内存区域的大小（以字节为单位）
- 返回值：
	- 如果成功，ioremap返回一个指向映射区域的虚拟地址的指针
	- 如果失败，返回NULL

  在使用ioremap函数将物理地址转换成虚拟地址之后，理论上我们便可以直接读写I/O内存，但是为了符合驱动的跨平台以及可移植性， 我们应该使用 linux 中指定的函数(如：iowrite8()、iowrite16()、iowrite32()、ioread8()、ioread16()、ioread32()等)去读写I/O内存，如下表所示：

| 函数名 | 功能 |
| --- | --- |
| unsigned int ioread8(void \_\_iomem \*addr) | 读取一个字节(8bit) |
| unsigned int ioread16(void \_\_iomem \*addr) | 读取一个字(16bit) |
| unsigned int ioread32(void \_\_iomem \*addr) | 读取一个双字(32bit) |
| void iowrite8(u8 data, void \_\_iomem \*addr) | 写入一个字节(8bit) |
| void iowrite16(u16 data, void \_\_iomem \*addr) | 写入一个字(16bit) |
| void iowrite32(u32 data, void \_\_iomem \*addr) | 写入一个双字(32bit) |

### 2\. iounmap( )

```c
//取消地址映射
void iounmap(void *addr)

iounmap(va_dr);     //释放掉ioremap映射之后的起始地址(虚拟地址)
1234
```
- 参数
	- addr： 需要取消ioremap映射之后的起始地址(虚拟地址)。
- 返回值： 无

### 3\. class\_create( )

```c
//提交目录信息
#define class_create(owner, name) \
({
    static struct lock_class_key _key; \
    _class_create(owner, name, &_key); \
})
123456
```
- 参数
	- owner：THIS\_MODULE (struct module结构体的首地址这个结构体存放了驱动的出口入口)
	- name：kobject对象名称
- 返回值
	- 成功：返回结构体首地址
	- 失败：返回错误码指针

注：IS\_ERR(cls); 判断是否为错误指针  
  PTR\_ERR(cls); 将错误码指针转换为错误码

### 4\. class\_destroy( )

```c
//注销目录信息
void class_destroy(struct class *cls);
12
```
- 参数
	- cls：结构体首地址
- 返回值：无

## 四、GPIO的基本知识

### 1\. GPIO的寄存器进行读写操作流程

- 使能GPIO时钟(默认开启，不用设置)
- 设置引脚复用为GPIO(复位默认为GPIO，不用配置)
- 设置引脚属性(上下拉、速率、驱动能力,默认)
- 控制GPIO引脚为输出，并输出高低电平

### 2\. 引脚复用

  对于 rockchip 系类芯片，我们需要通过参考手册以及数据手册来确定引脚的复用功能。首先可以看到泰山派的小灯连接引脚，这里我们选择GPIO1\_B0\_d。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/fa5d57a4285396e32eb3c14fe09efeeb.png)  
  通过查询rk3568官方资料，可以看到该引脚的复用功能如下所示。 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/4c3163db6c5042b3736fe80f7f83890d.png)  
  再查找其复用功能存在于SYS\_GRF寄存器，和复用相关的总共8个寄存器，如下图所示：  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ea871e4f65399fbb316dde01e68c994b.png)

  查询 Rockchip\_RK3568\_TRM\_Part1 手册，GRF\_GPIO1B\_IOMUX\_L寄存器(由于GPIO1\_b0是在低八位，下同)，如下图所示：  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/458179d2b8143ccdafba65da1345882a.png#pic_center)  
  寄存器总共32位，高16位都是使能位，控制低16位的写使能，低16位对应4个引脚，每个引脚占用3bits，不同的值引脚复用为不同功能。与此同时由\[14:12\]进行具体功能的设定。  
  我们可以查看到SYS\_GRF寄存器的复用功能基地址为0xFDC60000。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3c8739443087d6b76160bfe5c1b7f278.png)  
  此时通过命令行输入可以查询到该寄存器的设置情况，可以看到默认为GPIO口模式。

```c
//目标地址为Address Base(0xfdc60000)+offset(0x0008)
io -r -4 0xfdc60008
12
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/45d144e2d92fe7e3fd438a671d9afd73.png)

### 2\. 定义GPIO寄存器物理地址

  需要设置的寄存器的地址为base+offset，由下图可以知道GPIO1的基地址为：0xFE740000  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/eef7d5f1eef792ecdee9d588d4ccec1c.png#pic_center)  
  接下来就是确定GPIO的是输入还是输出，我们这里需要的是GPIO\_SWPORT\_DDR\_L。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/2a66b7e692286e7aa1e6b70e91b43f84.png) ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c10a47205d2d5e8867e2c4dcf87b0f74.png)  
  可以看到GPIO\_SWPORT\_DDR\_L的定义情况，这里我们可以重复上面提到的命令行，查看寄存器的设置情况，我们的b0应当是第1x7+1=8位。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/de31e3cb220b05876b5bb2a4c8f604e2.png)  
  同样查看可以看到这里的值为0x00000700。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/aa16ef70f9f6c475f38d226bcea2d8e0.png)  
  数据寄存器选择GPIO\_SWPORT\_DR\_L，大致流程和上面一样就不再赘述了。这里便完成了对GPIO的设置。

## 五、实验代码

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/4c1683053ff15de0632fdc1f1c0374da.png)

### 1\. 宏定义出需要的地址

```c
#define GPIO1_BASE (0xFE740000)

//一个寄存器32位，其中高16位都是写使能位，控制低16位的写使能；低16位对应16个引脚，控制引脚的输出电平
#define GPIO1_DR_L (GPIO0_BASE + 0x0000)  // GPIO0的低十六位引脚的数据寄存器地址
#define GPIO1_DR_H (GPIO0_BASE + 0x0004)  // GPIO0的高十六位引脚的数据寄存器地址

//一个寄存器32位，其中高16位都是写使能位，控制低16位的写使能；低16位对应16个引脚，控制引脚的输入输出模式
#define GPIO1_DDR_L (GPIO0_BASE + 0x0008)   // GPIO0的低十六位引脚的数据方向寄存器地址
#define GPIO1_DDR_H (GPIO0_BASE + 0x000C)   // GPIO0的低十六位引脚的数据方向寄存器地址
123456789
```

### 2\. 编写LED字符设备结构体且初始化

```c
//led字符设备结构体
struct led_chrdev {
        struct cdev dev;
        unsigned int __iomem *va_dr;    // 数据寄存器虚拟地址保存变量
        unsigned int __iomem *va_ddr;   // 数据方向寄存器虚拟地址保存变量
        unsigned int led_pin;             // 引脚
};

static struct led_chrdev led_cdev[DEV_CNT] = {
        {
            .led_pin = 8                //CPIO1_B0的偏移为8+0=8
        },
};
12345678910111213
```

### 3\. container\_of( )函数

  在Linux驱动编程当中我们会经常和container\_of()这个函数打交道，其宏定义实现如下所示：

```c
#define container_of(ptr, type, member) ({                      \
        const typeof( ((type *)0)->member ) *__mptr = (ptr);    \
        (type *)( (char *)__mptr - offsetof(type,member) );})
123
```
- 参数：
	- ptr： 结构体变量中某个成员的地址
	- type： 结构体类型
	- member： 该结构体变量的具体名字
- 返回值： 结构体type的首地址

  原理其实很简单，就是通过已知类型type的成员member的地址ptr，计算出结构体type的首地址。 type的首地址 = ptr - size ，需要注意的是它们的大小都是以字节为单位计算的，container\_of( )函数的主要作用如下：

- 判断ptr 与 member 是否为同一类型
- 计算size大小，结构体的起始地址 = (type \*)((char \*)ptr - size) (注：强转为该结构体指针)

**注：文件私有数据**  
  一般很多的linux驱动都会将文件的私有数据private\_data指向设备结构体，其保存了用户自定义设备结构体的地址。 自定义结构体的地址被保存在private\_data后，可以通过读、写等操作通过该私有数据去访问设备结构体中的成员， 这样做体现了linux中面向对象的程序设计思想。

### 4\. file\_operations结构体成员函数的实现

```c
static int led_chrdev_open(struct inode *inode, struct file *filp)
{
    unsigned int val = 0;
    struct led_chrdev *led_cdev = (struct led_chrdev *)container_of(inode->i_cdev, struct led_chrdev, dev);
    filp->private_data = container_of(inode->i_cdev, struct led_chrdev, dev);

    printk("open\n");

    //读取数据方向寄存器
    val = ioread32(led_cdev->va_ddr);
    //设置数据方向寄存器为pin位可写
    val |= ((unsigned int)0x1 << (led_cdev->led_pin+16));    
    //设置数据方向寄存器为pin位输出
    val |= ((unsigned int)0X1 << (led_cdev->led_pin));
    //写入数据方向寄存器
    iowrite32(val,led_cdev->va_ddr);

    //读取数据寄存器
    val = ioread32(led_cdev->va_dr);
    //设置数据寄存器为pin位可写
    val |= ((unsigned int)0x1 << (led_cdev->led_pin+16));
       //设置数据寄存器为pin位高电平
    val |= ((unsigned int)0x1 << (led_cdev->led_pin));
    //写入数据寄存器
    iowrite32(val, led_cdev->va_dr);

    return 0;
}
12345678910111213141516171819202122232425262728
```

  这部分代码位open\_operations结构体的设置，其中container\_of（）函数和寄存器设置部分需要联系前节4.2的介绍反复理解（笔者这里看了很久才顿悟）。

### 5\. 实验效果

```c
#蓝灯亮
sudo sh -c 'echo 0 >/dev/led_chrdev0'
#蓝灯灭
sudo sh -c 'echo 1 >/dev/led_chrdev0'
1234
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0c069d9a9cedcf5e932ced447292c3df.jpeg#pic_center)

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f105c4c02171ba33eacd0774f7480e77.jpeg#pic_center)

**免责声明：本程序参考了野火和北京讯为科技的部分视频资料，不作商用仅供学习，若有侵权和错误请联系笔者删除**

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/138665580

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

 [![](https://csdnimg.cn/release/blogv2/dist/pc/img/toolbar/Group-dark.png) 点击体验  
DeepSeekR1满血版](https://ai.csdn.net/?utm_source=cknow_pc_blogdetail&spm=1001.2101.3001.10583) 隐藏侧栏

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

![](https://i-blog.csdnimg.cn/blog_migrate/11c32ca53cc36b6a82ec5192292573bd.png#pic_center)