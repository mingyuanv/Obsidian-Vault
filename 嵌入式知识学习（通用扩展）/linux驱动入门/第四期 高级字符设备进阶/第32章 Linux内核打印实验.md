---
title: "{{title}}"
aliases: 
tags: 
description: 
source:
---

# 备注(声明)：




# 一、 查看Linux内核打印

## dmesg 命令（获取内核打印信息）
### 1 、命令讲解
> 英文全称：display message（显示信息）
> 
> 作用：kernel 会将打印信息存储在 ring buffer
> 中。可以利用 dmesg命令来查看内核打印信息。
> 
> 常用参数:
> 
> -C，–clear**清除**内核环形缓冲区
> 
> -c，—-read-clear**读取并清除**所有消息
> 
> -T，–**显示时间戳**
> 
> 提示：dmesg命令也可以与grep命令组合使用。如查找待用usb关键字的打印信息，就可以使用如下命令:**dmseg | grep usb**


### 2 、终端实验
> [root@topeet:/]# `dmesg`
[    0.000000] Booting Linux on physical CPU 0x0000000000 [0x412fd050]
[    0.000000] Linux version 4.19.232 (topeet@ubuntu) (gcc version 6.3.1 20170404 (Linaro GCC 6.3-2017.05), GNU ld (Linaro_Binutils-2017.05) 2.27.0.20161019) #2 SMP Thu Jul 17 21:36:33 CST 2025
[    0.000000] Machine model: Rockchip RK3568 EVB1 DDR4 V10 Board
[    0.000000] earlycon: uart8250 at MMIO32 0x00000000fe660000 (options '')
[    0.000000] bootconsole [uart8250] enabled
[    0.000000] cma: Reserved 16 MiB at 0x000000007ec00000
[    0.000000] On node 0 totalpages: 519680
[    0.000000]   DMA32 zone: 8184 pages used for memmap
[    0.000000]   DMA32 zone: 0 pages reserved
[    0.000000]   DMA32 zone: 519680 pages, LIFO batch:63
[    0.000000] psci: probing for conduit method from DT.
.........
> [root@topeet:/]# `dmesg | grep usb`
[    1.618772] reg-fixed-voltage vcc5v0-usb: Looking up vin-supply from device tree
[    1.618779] vcc5v0_usb: supplied by dc_12v
[    1.618831] vcc5v0_usb: 5000 mV
[    1.618987] reg-fixed-voltage vcc5v0-usb: vcc5v0_usb supplying 5000000uV
[    1.619177] vcc5v0_host: supplied by vcc5v0_usb
[    1.619197] vcc5v0_usb: could not add device link regulator.5 err -2
[    1.619653] vcc5v0_otg: supplied by vcc5v0_usb





### 3 、



### 4 、



### 5、


### 6、


### 7、


### 8、



## 查看kmsg文件
### 1 、kmsg文件原理
> 内核所有的打印信息都会输出到循环缓冲区 ‘log_buf’，为了能够方便的在用户空间读取 内核打印信息，Linux内核驱动将**该循环缓冲区映射到了/proc目录下的文件节点kmsg**。通过 cat或者其他应用程序读取Log Buffer的时候可以不断的等待新的log，所以访问/proc/kmsg 的方式适合**长时间的读取log，一旦有新的log就可以被打印出来。**


### 2 、实验 - 查看新的内核打印信息
> [root@topeet:/]# `cat /proc/kmsg`
> 
- 2 在没有新的内核打印信息时会阻塞


- 1 然后在该设备的其他终端加载任意有打印信息的驱动文件（这里使用的是ssh）
- 2 在串口终端中可以看到对应驱动的打印信息就被打印了出来
[[嵌入式知识学习（通用扩展）/linux驱动入门/第四期 高级字符设备进阶/assets/第32章 Linux内核打印实验/9a169dde66757296c21c6be35d69fe2a_MD5.jpeg|Open: file-20250827152513601.png]]
![嵌入式知识学习（通用扩展）/linux驱动入门/第四期 高级字符设备进阶/assets/第32章 Linux内核打印实验/9a169dde66757296c21c6be35d69fe2a\_MD5.jpeg](assets/第32章%20Linux内核打印实验/9a169dde66757296c21c6be35d69fe2a_MD5.jpeg)



### 3 、


### 4 、


### 5、


### 6、


### 7、


### 8、



## 调整内核打印等级
### 1 、查看当前默认打印等级
```shell
cat /proc/sys/kernel/printk
```

> [root@topeet:/]# cat /proc/sys/kernel/printk
>` 7       4       1       7`


### 2 、终端打印类型与说明（`console_loglevel`）
> “7 4 1 7” 分别对应console_loglevel、default_message_loglevel、minimum_c onsole_loglevel、default_console_loglevel

| 终端打印类型                     | 对应类型说明                                                |
| -------------------------- | ----------------------------------------------------- |
| console\_loglevel          | 只有当printk打印消息的log优先级**高于console\_loglevel时，才能输出到终端上** |
| default\_message\_loglevel | printk打印消息时默认的log等级                                   |
| minimum\_console\_loglevel | console\_loglevel可以被设置的最小值                            |
| default\_console\_loglevel | console\_loglevel的缺省值                                 |
- 1 意味着只有优先级高于KERN_DEBUG(7)的打印消息才能输出到终端
- 2 数字越小，优先级越高

### 3 、文件打印等级定义 （kernel/include/linux/kern_levels.h）

```d
/*
 * 以下宏定义了不同级别的内核日志前缀。
 * 每个日志级别都有一个对应的字符串，由SOH字符和一个特定的字符组成。
 */

// 系统不可用时使用的紧急级别日志
#define KERN_EMERG	KERN_SOH "0"	/* system is unusable */

// 需要立即采取行动的警告级别日志
#define KERN_ALERT	KERN_SOH "1"	/* action must be taken immediately */

// 关键条件的日志，例如硬件错误
#define KERN_CRIT	KERN_SOH "2"	/* critical conditions */

// 错误条件的日志
#define KERN_ERR	KERN_SOH "3"	/* error conditions */

// 警告条件的日志
#define KERN_WARNING	KERN_SOH "4"	/* warning conditions */

// 正常但需要注意的情况的日志
#define KERN_NOTICE	KERN_SOH "5"	/* normal but significant condition */

// 提供信息性消息的日志
#define KERN_INFO	KERN_SOH "6"	/* informational */

// 调试级别消息的日志
#define KERN_DEBUG	KERN_SOH "7"	/* debug-level messages */

// 默认内核日志级别
#define KERN_DEFAULT	KERN_SOH "d"	/* the default kernel loglevel */

```




### 4 、printk在打印信息前，可以加入相应的打印等级宏定义（设置打印等级）
```c
#include <linux/module.h>
#include <linux/kernel.h>
static int __init helloworld_init(void)
{
    printk(KERN_EMERG " 0000 KERN_EMERG\n");
    printk(KERN_ALERT " 1111 KERN_ALERT\n");
    printk(KERN_CRIT " 2222 KERN_CRIT\n");
    printk(KERN_ERR " 3333 KERN_ERR\n");
    printk(KERN_WARNING " 4444 KERN_WARNING\n");
    printk(KERN_NOTICE " 5555 KERN_NOTICE\n");
    printk(KERN_INFO " 6666 KERN_INFO\n");
    printk(KERN_DEBUG " 7777 KERN_DEBUG\n");
    printk(" 8888 no_fix\n");
    return 0;
}
static void __exit helloworld_exit(void)
{
    printk(KERN_EMERG "helloworld_exit\r\n");
}

module_init(helloworld_init);
module_exit(helloworld_exit);
MODULE_LICENSE("GPL v2");
MODULE_AUTHOR("topeet");

```

#### 实验结果及分析
> 加载该驱动之后，第5-11行0-6等级的打印信息就被打印了出来，第13行由于**没有设置打印等级，所以会被赋予默认打印等级4**，高于console_loglevel打印等级，所以也会被打印出来，最后只有第12行打印等级为7的信息，和console_loglevel**打印等级相同，所以不会被打印出来**，如下图（图 32-8）所示：



#### 扩展实验 - 更改console_loglevel打印等级
```c
echo 4 4 1 7 > /proc/sys/kernel/printk
```
- 1 卸载驱动之后，再一次加载驱动，发现只有打印等级高于4的相关信息被打印了出来
[[嵌入式知识学习（通用扩展）/linux驱动入门/第四期 高级字符设备进阶/assets/第32章 Linux内核打印实验/1036dc1f6aa92a970450e74b2802a7a5_MD5.jpeg|Open: file-20250827162738343.png]]
![嵌入式知识学习（通用扩展）/linux驱动入门/第四期 高级字符设备进阶/assets/第32章 Linux内核打印实验/1036dc1f6aa92a970450e74b2802a7a5\_MD5.jpeg](assets/第32章%20Linux内核打印实验/1036dc1f6aa92a970450e74b2802a7a5_MD5.jpeg)




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


