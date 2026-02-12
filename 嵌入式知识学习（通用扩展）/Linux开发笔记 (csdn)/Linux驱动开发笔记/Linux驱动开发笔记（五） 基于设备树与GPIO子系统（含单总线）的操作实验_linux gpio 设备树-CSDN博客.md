---
title: "Linux驱动开发笔记（五） 基于设备树与GPIO子系统（含单总线）的操作实验_linux gpio 设备树-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/139328317?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读1.3k次，点赞20次，收藏13次。前两章我们学习了平台设备和设备树的相关内容，接下来将对这部分进行结合学习。本章分为两部分，即有、无通过平台设备借由设备树对GPIO进行操作，大家可以自行比对。注册平台驱动时会用到平台设备结构体，在平台设备结构体主要作用是指定平台驱动的.probe函数、指定与平台驱动匹配的平台设备， 使用了设备树后就是指定与平台驱动匹配的设备树节点。//定义匹配表},//定义平台设备结构体。_linux gpio 设备树"
tags:
  - "clippings"
---
---

## 前言

  前两章我们学习了平台设备和 [设备树](https://so.csdn.net/so/search?q=%E8%AE%BE%E5%A4%87%E6%A0%91&spm=1001.2101.3001.7020) 的相关内容，接下来将对这部分进行结合学习。本章分为两部分，即有、无通过平台设备借由设备树对GPIO进行操作，大家可以自行比对。

---

## 一、设备树的GPIO操作实验

### 1\. 修改设备树

#### 1.1 添加princtrl的设备树节点

  新增的节点名为“led\_test”，名字任意选取(在同一节点下不要同名)，长度不要超过32个字符，最好能表达出节点的信息。 “led\_test\_pin”节点标签，“ rockchip,pins”是固定的格式，后面的内容自定义的，我们将通过这个标签引用这个节点。

```c
&pinctrl {
    /*----------新添加的内容--------------*/
    led_test {
        led_test_pin: led_test_pin {
            rockchip,pins = <3 RK_PB4 RK_FUNC_GPIO &pcfg_pull_none>;
        };
    };
};
12345678
```

#### 1.2 添加RGB灯的设备树节点

  由于该引脚默认设置为GPIO模式，这里就不再使用princtrl进行复用功能的设置了。这里简单写一下即可，之后到 kernel 目录下进行编译。

```c
myled:myled{
    status = "okay";
    compatible = "company,led";
    gpios = <&gpio3 RK_PB4 GPIO_ACTIVE_LOW>;
    default-state = "on";
    pinctrl-names = "default";
    pinctrl-0 = <&led_test_pin>;
}
12345678
```

### 2.驱动代码编写

  这部分内容很简单，这里就不展开说了，感兴趣可以参考： [实验参考](https://www.bilibili.com/video/BV1VM4m1r7nG/?spm_id_from=333.999.0.0&vd_source=937f3264dce76f586bc0a69ee24dfafa) ，  
这里着重说一下gpio\_init和gpio\_deinit两个 函数 ，其他的operation相关函数和之前的大同小异。

```c
int gpio_init(void)
{
    //获取节点
    led_node = of_find_node_by_path(LED_NODE_PATH);
    if(led_node == NULL)
    {
        printk("find node %s failed!\n",LED_NODE_PATH );
        return -ENODEV;
    }
 
    //获取gpio编号
    gpionum = of_get_named_gpio(led_node, LED_NODE_PROPERTY, 0);
    if(gpionum < 0)
    {
        printk("get property %s failed!\n",LED_NODE_PROPERTY );
        return -EINVAL;
    }
 
    //申请GPIO
    if(gpio_request(gpionum,NULL))
    {
        printk("request gpio failed!\n");
        return -EINVAL;
    }
 
     
    //设置GPIO为输出
    if(gpio_direction_output(gpionum, 0))
    {
        printk("set gpio direction failed!\n");
        return -EINVAL;
    }
    return 0;
}
12345678910111213141516171819202122232425262728293031323334
```
```c
void gpio_deinit(void)
{
    gpio_set_value(gpionum,0);
    gpio_free(gpionum);
}
12345
```

  值得注意的是，这里的gpio\_init和gpio\_deinit分别放置于module\_init和module\_deinit中。

## 二、基于设备树的平台设备匹配实验

  之前在讲平台设备的时候，我们提到其匹配方式有四种：设备树机制、ACPI [匹配模式](https://so.csdn.net/so/search?q=%E5%8C%B9%E9%85%8D%E6%A8%A1%E5%BC%8F&spm=1001.2101.3001.7020) 、id\_table方式、字符串比较。之前已经讲过id\_table的方式，这里讲一下设备树机制。

### 1\. 四种匹配方式的比较

  设备树机制、ACPI匹配模式、id\_table方式和字符串比较在 Linux 系统中各有其应用场景和优缺点，在实际应用中，可以根据具体需求选择合适的匹配方式。

|  | 设备树 | ACPI | id\_table | 字符串 |
| --- | --- | --- | --- | --- |
| 优点 | 高灵活性、可移植性、自动化 | 标准化、高兼容性 | 简洁性、灵活性 | 通用性、准确性 |
| 缺点 | 有一定复杂性和学习成本 | 规范复杂、需要BIOS和操作系统的支持 | 只适用于已知设备ID的情况 | 只适用于字符串、资源消耗大 |
| 匹配过程 | 内核解析dtb文件，创建相应的设备对象 | 通过ACPI命名空间中的设备对象与驱动程序中的ACPI处理函数进行 | 内核会检查id\_table中的每个ID，并将其与设备ID进行匹配 | 字符串比较通常通过比较两个字符串中字符的编码值来实现 |
| 使用场景 | 为操作系统提供硬件设备的拓扑结构和属性信息 | 用于操作系统和平台硬件之间的电源管理和配置 | 用于从剥离的设备树条目（无供应商部分）中查找匹配项 | 用于比较两个字符串是否相等或确定它们之间的顺序关系 |

### 2\. princtrl的编写

  新增的节点名为“led\_test”，名字任意选取(在同一节点下不要同名)，长度不要超过32个字符，最好能表达出节点的信息。 “led\_test\_pin”节点标签，“rockchip,pins”是固定的格式，后面的内容自定义的，我们将通过这个标签引用这个节点。

```c
&pinctrl {
    /*----------新添加的内容--------------*/
    led_test {
        led_test_pin: led_test_pin {
            rockchip,pins = <3 RK_PB4 RK_FUNC_GPIO &pcfg_pull_none>;
        };
    };
};
12345678
```

### 2\. 定义平台设备结构体

  注册平台驱动时会用到平台设备结构体，在平台设备结构体主要作用是指定平台驱动的.probe函数、指定与平台驱动匹配的平台设备， 使用了设备树后就是指定与平台驱动匹配的设备树节点。

```c
//定义匹配表
static const struct of_device_id led_ids[] = {
    {.compatible = "company,led";},
    {/* sentinel */}
    };

//定义平台设备结构体
struct platform_driver led_platform_driver = {
    .probe = led_probe,
    .driver = {
            .name = "leds-platform",
            .owner = THIS_MODULE,
            .of_match_table = led_ids,
    }
    };
123456789101112131415
```

  这里只定义了一个匹配值“.compatible = “company,led”，这个驱动将会和设备树中“compatible =“company,led”的节点匹配”，准确的说是和““compatible = “company,led””的相对根节点的子节点匹配。

### 3\. probe函数

  之前说过，当驱动和设备树节点匹配成功后会自动执行.probe函数，所以我们在.probe函数中实现一些初始化工作。

```c
/*----------------平台驱动函数集-----------------*/
static int led_probe(struct platform_device *pdv)
{
    
    int ret = 0;  //用于保存申请设备号的结果

    printk("match successed\n");
    /*获取RGB的设备树节点*/
    led_device_node = of_find_node_by_path(LED_NODE_PATH);
    if(led_device_node == NULL)
    {
        printk(KERN_EMERG "\t  get nodepath failed!  \n");
    }
    led = of_get_named_gpio(led_device_node, LED_NODE_PROPERTY, 0);
    printk("led = %d \n",led);  
    /*设置gpio输出高电平*/
    gpio_direction_output(led, 1);
    /*---------------------注册 字符设备部分-----------------*/
    //采用动态分配的方式，获取设备编号，次设备号为0，
    ret = alloc_chrdev_region(&led_devno, 0, DEV_CNT, DEV_NAME);
    if(ret < 0){
        printk("fail to alloc led_devno\n");
        goto alloc_err;
    }
    //关联字符设备结构体cdev与文件操作结构体file_operations
    led_chr_dev.owner = THIS_MODULE;
    cdev_init(&led_chr_dev, &led_chr_dev_fops);
    //添加设备至cdev_map散列表中
    ret = cdev_add(&led_chr_dev, led_devno, DEV_CNT);
    if(ret < 0)
    {
        printk("fail to add cdev\n");
        goto add_err;
    }
    /*创建类 */
    class_led = class_create(THIS_MODULE, DEV_NAME);
    /*创建设备*/
    device = device_create(class_led, NULL, led_devno, NULL, DEV_NAME);
    return 0;
    /*******************************错误符****************************/
add_err:
    //添加设备失败时，需要注销设备号
    unregister_chrdev_region(led_devno, DEV_CNT);
    printk("\n error! \n");
alloc_err:
    return -1;
}
1234567891011121314151617181920212223242526272829303132333435363738394041424344454647
```

### 4\. operations结构体函数编写

```c
/*------------------第一部分---------------*/
/*字符设备操作函数集*/
static struct file_operations  led_chr_dev_fops =
{
    .owner = THIS_MODULE,
    .open = led_chr_dev_open,
    .write = led_chr_dev_write,
};

/*------------------第二部分---------------*/
/*字符设备操作函数集，open函数*/
static int led_chr_dev_open(struct inode *inode, struct file *filp)
{
    printk("open \n");
    return 0;
}

/*------------------第三部分---------------*/
/*字符设备操作函数集，write函数*/
static ssize_t led_chr_dev_write(struct file *filp, const char __user *buf, size_t cnt, loff_t *offt)
{
    unsigned char write_data; //用于保存接收到的数据

    int error = copy_from_user(&write_data, buf, cnt);
    if(error < 0) {
            return -1;
    }

    /*设置led的引脚输出电平*/
    if(write_data)
    {
        gpio_direction_output(led, 1);  // 引脚输出高电平，红灯灭
    }
    else
    {
        gpio_direction_output(led, 0);    //引脚输出底电平，红灯亮
    }

    return 0;
}
12345678910111213141516171819202122232425262728293031323334353637383940
```

## 三、DHT11的驱动实验

  DHT11传感器是 **单总线** 通信协议的传感器，利用单根数据线在设备与主机之间传输数据。单总线协议的设计使得它具有较低的通信速率和较简单的实现方式，适合资源受限的场景。在Linux内核中， **单总线通信的控制通常使用GPIO子系统来实现** ，可以说单总线通信本质上是GPIO的一种特殊应用，利用了GPIO的分时双向控制特点来实现数据的双向传输。GPIO提供了位级别的控制，可以将单个引脚设置为输入或输出，并可以读写高低电平，这非常适合单总线协议的控制。  
  首先是dht11字符设备的结构体，这部分忘了的可以看一下字符设备那节。

```c
#define DHT11DEV_CNT 1              /* 设备号长度 */
#define DHT11DEV_NAME "dht11"       /* 设备名字 */

struct dht11dev_dev {
    dev_t devid;                  /* 设备号 */
    struct cdev cdev;             /* cdev */
    struct class *class;          /* 类 */
    struct device *device;        /* 设备 */ 
    struct device_node *node;     /* dht11dev 设备节点 */
    int gpios;                    /* GPIO 标号 */
};

struct dht11dev_dev dht11dev;     /* dht11dev 设备 */
12345678910111213
```

  DHT11相关函数，可以用于后续operation函数的封装。

```c
// dht11_release，用于释放总线
static void dht11_release(void) {
    // 将GPIO设置为输出高电平，释放DHT11总线
    gpio_direction_output(dht11dev.gpios, 1);
}
 
// dht11_start，用于向DHT11发送起始信号
static void dht11_start(void) {
    gpio_direction_output(dht11dev.gpios, 1);
    mdelay(30);
    
    gpio_set_value(dht11dev.gpios, 0);
    mdelay(20);
    
    gpio_set_value(dht11dev.gpios, 1);
    udelay(40);
    
    gpio_direction_input(dht11dev.gpios);
}
 
// dht11_wait_ack，用于等待DHT11的响应信号
static int dht11_wait_ack(void) {
    long timeout_us = 50000;

    while (gpio_get_value(dht11dev.gpios) && --timeout_us) {
        udelay(1);
    }
    if (!timeout_us) {
        return -1;
    }

    timeout_us = 50000;
    while (!gpio_get_value(dht11dev.gpios) && --timeout_us) {
        udelay(1);
    }
    if (!timeout_us) {
        return -1;
    }

    timeout_us = 20000;
    while (gpio_get_value(dht11dev.gpios) && --timeout_us) {
        udelay(1);
    }
    if (!timeout_us) {
        return -1;
    }

    return 0;
}
 
// dht11_read_byte，用于读取温湿度数据
static int dht11_read_byte(unsigned char datalist) {
    int i;
    unsigned char data = 0;
    int timeout_us = 20000;
    u64 pre = 0, last = 0;
    // 通过检测高低电平的持续时间来判断该位的值（1或0）
    for (i = 0; i < 8; i++) {
        timeout_us = 20000;
        while (!gpio_get_value(dht11dev.gpios) && --timeout_us) {
            udelay(1);
        }
        
        if (!timeout_us) {
            return -1;
        }

        pre = ktime_get_boot_ns();
        while (1) {
            last = ktime_get_boot_ns();
            if (last - pre >= 40000)
                break;
        }
      
        if (gpio_get_value(dht11dev.gpios)) {
            data = (data << 1) | 1;
            timeout_us = 20000;
            while (gpio_get_value(dht11dev.gpios) && --timeout_us) {
                udelay(1);
            }
            if (!timeout_us) {
                return -1;
            }
        } else {
            data = (data << 1) | 0;
        }
    }
    // 将读取的数据存入getdata数组中
    getdata[datalist] = data;
    
    return 0;
}

// dht11_get_value，执行DHT11的完整数据读取流程
static int dht11_get_value(void) {
    unsigned long flags;
    int i;
    
    local_irq_save(flags);  // 关中断
    dht11_start();
    if (dht11_wait_ack()) {
        local_irq_restore(flags);
        return -EAGAIN;
    }

    for (i = 0; i < 5; i++) {
        dht11_read_byte(i); 
    }
    
    dht11_release();
    local_irq_restore(flags);

    if (getdata[4] != (getdata[0] + getdata[1] + getdata[2] + getdata[3])) {
        getdata[0] = 0xff;
        getdata[1] = 0xff;
        getdata[2] = 0xff;
        getdata[3] = 0xff;
        return -1;
    }    
    
    return 0;
}
123456789101112131415161718192021222324252627282930313233343536373839404142434445464748495051525354555657585960616263646566676869707172737475767778798081828384858687888990919293949596979899100101102103104105106107108109110111112113114115116117118119120121122
```

  相关operation函数，为应用层的操作提供接口。

```c
static int dht11_open(struct inode *inode, struct file *filp) {
    return 0;
}

static ssize_t dht11_drv_read(struct file *file, char __user *buf, size_t size, loff_t *offset) {
    int ret = 0;
    if (!dht11_get_value()) {
        ret = copy_to_user(buf, getdata, sizeof(getdata));
        return ret;
    }
    return ret;
}

static ssize_t dht11_write(struct file *filp, const char __user *buf, size_t cnt, loff_t *offt) {
    return 0;
}

static int dht11_drv_close(struct inode *node, struct file *file) {
    dht11_get_value();
    return 0;
}
123456789101112131415161718192021
```

  剩下的部分就是probe函数和remove函数了，这两部分和上面的led实现过程一样就不再赘述了。最后加一个应用层的代码就可以实现功能了：

```c
#include <sys/types.h>
#include <sys/stat.h>
#include <linux/types.h>
#include <linux/i2c-dev.h>
#include <linux/i2c.h>
#include <sys/ioctl.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <stdlib.h>
#include <linux/fs.h>
#include <errno.h>
#include <assert.h>
#include <string.h>
#include <time.h>
 
#define DEV_FILE    "/dev/dht11" // 这是你申请出来的设备
 
 
int main(void)
{
    int fd;
    int count_run = 0;
    int ret = 0;
    unsigned char data[4];
 
    fd = open(DEV_FILE, 0);    // 打开设备
    if (fd == -1){
        printf("can not open file: %s \n", DEV_FILE);
        return -1;
    }
    
    // 每5s读取一次
    while( count_run < 50000)
    {
        count_run++;

        if (read(fd, &data[0], 4) == 0) 
        {
        // 切记，是先湿度后温度
            printf("get humidity  : %d.%d\n", data[0], data[1]);
            printf("get temprature: %d.%d\n", data[2], data[3]);
        } 
        else 
        {
            printf("read dht11 device fail!\n");
        }
        
        sleep(1);  // 1毫秒
    }
 
    close(fd);
 
    return 0;
}

123456789101112131415161718192021222324252627282930313233343536373839404142434445464748495051525354555657
```

---

**免责声明：本文参考了野火的部分资料，仅供学习参考使用，若有侵权或勘误请联系笔者。**

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/139328317

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