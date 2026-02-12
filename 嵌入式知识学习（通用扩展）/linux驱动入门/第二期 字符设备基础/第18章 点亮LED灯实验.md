---
title: "RK3568驱动指南｜第二篇 字符设备基础-第18章 点亮LED灯实验_rk3568点灯-CSDN博客"
source: "https://blog.csdn.net/BeiJingXunWei/article/details/132755368"
author:
  - "[[成就一亿技术人!]]"
  - "[[hope_wisdom 发出的红包]]"
published:
created: 2025-09-08
description: "文章浏览阅读1.6k次，点赞2次，收藏12次。经过前面章节的学习，我们已经对字符设备相关的知识进行了学习和实验，但实际上并没有涉及到对硬件的操作，而在本小节中将通过字符设备驱动及相关的应用程序对LED灯进行控制，通过对硬件的实际操作，从而对之前学习到的知识进行整合与回顾。_rk3568点灯"
tags:
  - "clippings"
---

> 经过前面章节的学习，我们已经对字符设备相关的知识进行了学习和实验，但实际上并没有涉及到对硬件的操作，而在本小节中将**通过字符设备驱动及相关的应用程序对LED灯进行控制**，通过对硬件的实际操作，从而对之前学习到的知识进行整合与回顾。

# 18.1 查看原理图

- 1 首先打开底板原理图

![嵌入式知识学习（通用扩展）/linux驱动入门/第二期 字符设备基础/assets/第18章 点亮LED灯实验/6e957e6dc0577bc5848d9799357242a9\_MD5.jpg](assets/第18章%20点亮LED灯实验/6e957e6dc0577bc5848d9799357242a9_MD5.jpg)

> 由上图可以看出，LED灯是由GPIO0\_B7控制的。当**GPIO0\_B7为高电平时， 三极管 Q16导通，LED9点亮**。当GPIO0\_B7为低电平时，三极管Q16截止，LED9不亮。

# 18.2 查询寄存器地址

> 在上一小节，我们查询到了控制LED灯的GPIO为GPIO0\_B7。在接下来的实验中需要对GPIO进行配置，一般情况下需要**对GPIO的复用寄存器，方向寄存器，数据寄存器进行配置**。接下来我们打开RK3568的参考手册part1查找这几个寄存器的地址。

> [!PDF|important] [[芯片开发学习/RK3568（linux学习）/linux开发资料库/rk3568迅为开发pdf/00看视频教程用到的开发手册/Rockchip RK3568 TRM Part1 V1.1-20210301-核心板技术参考手册.pdf#page=10&selection=18,0,18,19&color=important|Rockchip RK3568 TRM Part1 V1.1-20210301-核心板技术参考手册, p.10]]
> > Warranty Disclaimer
> 
> 


## 1、查找复用寄存器（PMU_GRF）
- 1 打开参考手册part1的第三章，GPIOB的复用寄存器的偏移地址如下（图18-2）所示：

![嵌入式知识学习（通用扩展）/linux驱动入门/第二期 字符设备基础/assets/第18章 点亮LED灯实验/2f87a3a09eb13d83b0edce9555699a2a\_MD5.jpg](assets/第18章%20点亮LED灯实验/2f87a3a09eb13d83b0edce9555699a2a_MD5.jpg)

### 搜索gpio0b7：得知其复用寄存器地址
> **gpio0b7\_sel在PMU\_GRF\_GPIO0B\_IOMUX\_H上，所以偏移地址为0x000C**gpio0b7可以通过**控制\[14:12\]位来选择复用为哪个功能**，我们要控制led灯，所以功能要复用为gpio。

![嵌入式知识学习（通用扩展）/linux驱动入门/第二期 字符设备基础/assets/第18章 点亮LED灯实验/355b8c1672a0aea2dd984c1ff1a3b700\_MD5.jpg](assets/第18章%20点亮LED灯实验/355b8c1672a0aea2dd984c1ff1a3b700_MD5.jpg)

### 复用寄存器的基地址如下：

![嵌入式知识学习（通用扩展）/linux驱动入门/第二期 字符设备基础/assets/第18章 点亮LED灯实验/794588a2556b8ace2e3ecd6cc2a82978\_MD5.jpg](assets/第18章%20点亮LED灯实验/794588a2556b8ace2e3ecd6cc2a82978_MD5.jpg)

> 所以**复用寄存器地址=基地址+偏移地址=0xFDC2000C** 。

### 使用io命令查看此寄存器的值：
```c
io -r -4 0xFDC2000C
```
![嵌入式知识学习（通用扩展）/linux驱动入门/第二期 字符设备基础/assets/第18章 点亮LED灯实验/abd5ddc8d6fd70e4183661a40d14e09a\_MD5.jpg](assets/第18章%20点亮LED灯实验/abd5ddc8d6fd70e4183661a40d14e09a_MD5.jpg)

> 如上图(图 18-5)所示，寄存器值为00000001，**\[14:12\]位为000**，如下图（图 18-6）所示，所以**默认设置的为gpio功能**。

![嵌入式知识学习（通用扩展）/linux驱动入门/第二期 字符设备基础/assets/第18章 点亮LED灯实验/9a684d8e9536ca2cf55a93700b77cd91\_MD5.jpg](assets/第18章%20点亮LED灯实验/9a684d8e9536ca2cf55a93700b77cd91_MD5.jpg)

## 2、查找方向寄存器（Direction Register）

### 查找方向寄存器的偏移地址
- 1 打开参考手册part1的第16章节，方向寄存器的偏移地址如下图（图 18-7）所示：

![嵌入式知识学习（通用扩展）/linux驱动入门/第二期 字符设备基础/assets/第18章 点亮LED灯实验/ec70e0a242cb990b7a51587d42f9f97c\_MD5.jpg](assets/第18章%20点亮LED灯实验/ec70e0a242cb990b7a51587d42f9f97c_MD5.jpg)

> GPIO有四组GPIO，分别是GPIOA，GPIOB，GPIOC，GPIOD。每组又以 A0~A7, B0~B7, C0~C7, D0~D7 作为编号区分。**GPIO0B7在GPIO\_SWPORT\_DDR\_L上所以，方向寄存器的偏移地址为0x0008**。

### 查看GPIO\_SWPORT\_DDR\_L寄存器的具体描述
- 1 对应GPIO_A0~GPIO_B7

![嵌入式知识学习（通用扩展）/linux驱动入门/第二期 字符设备基础/assets/第18章 点亮LED灯实验/6a62cf63d2f7a5fead80c9ad821d9ce2\_MD5.jpg](assets/第18章%20点亮LED灯实验/6a62cf63d2f7a5fead80c9ad821d9ce2_MD5.jpg)

> 如上图（图 18-8）所示，**\[31:16\]位属性是WO，也就是只可写入**。
> 
> 这`[31:16]位`**是写标志位，是低16位的写使能。如果低16位中某一位要设置输入输入输出，则对应高位写标志也应该设置为1**。 
> 
> `[15：0] `是数据方向控制寄存器低位，如果要**设置某个GPIO为输出，则对应位置1**，如果要设置某个GPIO为输入，则对应位置0。那么GPIO0 B7 ，我们要设置第15位为输入还是输出，那么对应的\[31:16\]位写使能也要置1。

### 查找GPIO0的基地址（Address Mapping）
- 1 打开参考手册part1的1.1小节 Address Mapping。

![嵌入式知识学习（通用扩展）/linux驱动入门/第二期 字符设备基础/assets/第18章 点亮LED灯实验/816beaf6957773d88a0e25a10c16d058\_MD5.jpg](assets/第18章%20点亮LED灯实验/816beaf6957773d88a0e25a10c16d058_MD5.jpg)

![嵌入式知识学习（通用扩展）/linux驱动入门/第二期 字符设备基础/assets/第18章 点亮LED灯实验/93b728eb44bd9fff7ef2e3aaf403efa5\_MD5.jpg](assets/第18章%20点亮LED灯实验/93b728eb44bd9fff7ef2e3aaf403efa5_MD5.jpg)

### 计算方向寄存器的地址
> 如上图（图18-10）所示，GPIO0的基地址为0xFDD60000。
> **方向寄存器的地址=基地址+偏移地址=0xFDD60000+0x0008=0xFDD60008**

#### 然后使用IO命令查看该寄存器的值
![嵌入式知识学习（通用扩展）/linux驱动入门/第二期 字符设备基础/assets/第18章 点亮LED灯实验/6f8c15b5a1dedd7ea6f8d0df08bf52e6\_MD5.jpg](assets/第18章%20点亮LED灯实验/6f8c15b5a1dedd7ea6f8d0df08bf52e6_MD5.jpg)

- 1 如下图（图 18-11）所示，第15位默认为1，设置GPIO0\_B7为输出。

![嵌入式知识学习（通用扩展）/linux驱动入门/第二期 字符设备基础/assets/第18章 点亮LED灯实验/3ad652839ca5e8dba189f30f0846bfaf\_MD5.jpg](assets/第18章%20点亮LED灯实验/3ad652839ca5e8dba189f30f0846bfaf_MD5.jpg)

## 3、查找数据寄存器（Data Register）

### 查找GPIO0的基地址（Address Mapping）

- 1 打开参考手册part1的1.1小节Address Mapping。

![嵌入式知识学习（通用扩展）/linux驱动入门/第二期 字符设备基础/assets/第18章 点亮LED灯实验/a97317aab9701421bcdba738c8aee552\_MD5.jpg](assets/第18章%20点亮LED灯实验/a97317aab9701421bcdba738c8aee552_MD5.jpg)

![嵌入式知识学习（通用扩展）/linux驱动入门/第二期 字符设备基础/assets/第18章 点亮LED灯实验/93b728eb44bd9fff7ef2e3aaf403efa5\_MD5.jpg](assets/第18章%20点亮LED灯实验/93b728eb44bd9fff7ef2e3aaf403efa5_MD5.jpg)

- 2 如上图（图18-13）所示，GPIO0的基地址为0xFDD60000。

### 查找数据寄存器的偏移地址

![嵌入式知识学习（通用扩展）/linux驱动入门/第二期 字符设备基础/assets/第18章 点亮LED灯实验/efbe4d777ad0f76a8c8590ffca2e9dc0\_MD5.jpg](assets/第18章%20点亮LED灯实验/efbe4d777ad0f76a8c8590ffca2e9dc0_MD5.jpg)
- 2 0x0000


### 计算数据寄存器的地址
> 所以数据寄存器的地址为**基地址+偏移地址=0xFDD60000**。

#### 使用IO命令查看地址的值

![嵌入式知识学习（通用扩展）/linux驱动入门/第二期 字符设备基础/assets/第18章 点亮LED灯实验/b616dac32e85b56bdd87b34b10ae745a\_MD5.jpg](assets/第18章%20点亮LED灯实验/b616dac32e85b56bdd87b34b10ae745a_MD5.jpg)


### 查看数据寄存器（GPIO_SWPORT_DR_L）的描述

![嵌入式知识学习（通用扩展）/linux驱动入门/第二期 字符设备基础/assets/第18章 点亮LED灯实验/b5c299273a8ef751676ddb02728c9a5b\_MD5.jpg](assets/第18章%20点亮LED灯实验/b5c299273a8ef751676ddb02728c9a5b_MD5.jpg)

#### 点亮灯
> 分析上图的方法和在分析方向寄存器的方法同理，由上图可知，
> **如果要控制第15位为高电平（置1），需要设置31位为1**，
> 
> 需要**向数据寄存器写入0x8000c040**，如下图（图18-17）所示：

![嵌入式知识学习（通用扩展）/linux驱动入门/第二期 字符设备基础/assets/第18章 点亮LED灯实验/849c5edfb91ce36a37e77088026afda2\_MD5.jpg](assets/第18章%20点亮LED灯实验/849c5edfb91ce36a37e77088026afda2_MD5.jpg)

#### 要灭灯
> 需要**设置第15位为0 ，第31位为1，那么向数据寄存器中写入0x80004040**，如下图（图 18-18）所示：

![嵌入式知识学习（通用扩展）/linux驱动入门/第二期 字符设备基础/assets/第18章 点亮LED灯实验/d7cfbaad87eb7106a5b7ee94010c6d5f\_MD5.jpg](assets/第18章%20点亮LED灯实验/d7cfbaad87eb7106a5b7ee94010c6d5f_MD5.jpg)

## 4、地址总结

> - `复用关系寄存器`的基地址为0xFDC20000 ，偏移地址为000C ，所以要操作的地址为基地址+偏移地址=**0xFDC2000C**
> - 
> - GPIO的基地址为0xFDD60000，偏移地址为0x0008，所以`方向寄存器`要操作的地址为基地址+偏移地址=**0xFDD60008**
> - 
> - GPIO的基地址为0xFDD60000，偏移地址为0x0000，所以`数据寄存器`要操作的地址为基地址+偏移地址=**0xFDD60000**
> - 默认的数据寄存器的值：0x8000c040亮灯，0x80004040灭灯

## 5、查看寄存器手册总结
### 复用关系寄存器
#### 3.3 PMU_GRF Register Description（偏移地址）

#### Table 3-1GRF Adress Mapping Table（基地址）

### 方向寄存器
#### 16.4 Register Description（偏移地址）

#### 1.1 Address Mapping（基地址）

### 数据寄存器

#### 16.4 Register Description（偏移地址）

#### 1.1 Address Mapping（基地址）



# 18.3 实验程序编写

## 18.3.1 驱动程序编写

本驱动程序对应的网盘路径为：iTOP-RK3568开发板【底板V1.7版本】\\03\_【iTOP-RK3568开发板】指南教程\\02\_Linux驱动配套资料\\04\_Linux驱动例程\\13\\module。

> 本次实验在15章的驱动程序基础上进行编写，通过在应用层传入0/1数据到内核，**如果传入数据是1，则设置GPIO的数据寄存器值为0x8000c040**，如果应用层传入0，则设置GPIO的数据寄存器值为0x80004040，这样就可以达到控制led的效果

### 编写好的驱动程序file.c如下：

```c
#include <linux/init.h>
#include <linux/module.h>
#include <linux/kdev_t.h>
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/uaccess.h>
#include <linux/io.h>

#define  GPIO_DR 0xFDD60000

struct device_test{
   
    dev_t dev_num;  //设备号
    int major ;  //主设备号
    int minor ;  //次设备号
    struct cdev cdev_test; // cdev
    struct class *class;   //类
    struct device *device; //设备
    char kbuf[32];
    unsigned int *vir_gpio_dr;
};

struct  device_test dev1;  

/*打开设备函数*/
static int cdev_test_open(struct inode *inode, struct file *file)
{
    file->private_data=&dev1;//设置私有数据
    printk("This is cdev_test_open\r\n");
    return 0;
}

/*向设备写入数据函数*/
static ssize_t cdev_test_write(struct file *file, const char __user *buf, size_t size, loff_t *off)
{
     struct device_test *test_dev=(struct device_test *)file->private_data;

    if (copy_from_user(test_dev->kbuf, buf, size) != 0) // copy_from_user:用户空间向内核空间传数据
    {
        printk("copy_from_user error\r\n");
        return -1;
    }
    
    if(test_dev->kbuf[0]==1){   //如果应用层传入的数据是1，则打开灯
            *(test_dev->vir_gpio_dr) = 0x8000c040;   //设置数据寄存器的地址
            printk("test_dev->kbuf [0]  is %d\n",test_dev->kbuf[0]);  //打印传入的数据
    }else if(test_dev->kbuf[0]==0){  //如果应用层传入的数据是0，则关闭灯
        *(test_dev->vir_gpio_dr) = 0x80004040; //设置数据寄存器的地址
        printk("test_dev->kbuf [0]  is %d\n",test_dev->kbuf[0]); //打印传入的数据
	}
return 0;
}

/**从设备读取数据*/
static ssize_t cdev_test_read(struct file *file, char __user *buf, size_t size, loff_t *off)
{    
    struct device_test *test_dev=(struct device_test *)file->private_data;
    
    if (copy_to_user(buf, test_dev->kbuf, strlen( test_dev->kbuf)) != 0) // copy_to_user:内核空间向用户空间传数据
    {
        printk("copy_to_user error\r\n");
        return -1;
    }

    printk("This is cdev_test_read\r\n");
    return 0;
}

static int cdev_test_release(struct inode *inode, struct file *file)
{
    printk("This is cdev_test_release\r\n");
    return 0;
}

/*设备操作函数*/
struct file_operations cdev_test_fops = {
    .owner = THIS_MODULE, //将owner字段指向本模块，可以避免在模块的操作正在被使用时卸载该模块
    .open = cdev_test_open, //将open字段指向chrdev_open(...)函数
    .read = cdev_test_read, //将open字段指向chrdev_read(...)函数
    .write = cdev_test_write, //将open字段指向chrdev_write(...)函数
    .release = cdev_test_release, //将open字段指向chrdev_release(...)函数
};

static int __init chr_fops_init(void) //驱动入口函数
{
    /*注册字符设备驱动*/
    int ret;
    /*1 创建设备号*/
    ret = alloc_chrdev_region(&dev1.dev_num, 0, 1, "alloc_name"); //动态分配设备号
    if (ret < 0)
    {
       goto err_chrdev;
    }
    printk("alloc_chrdev_region is ok\n");

    dev1.major = MAJOR(dev1.dev_num); //获取主设备号
   dev1.minor = MINOR(dev1.dev_num); //获取次设备号

    printk("major is %d \r\n", dev1.major); //打印主设备号
    printk("minor is %d \r\n", dev1.minor); //打印次设备号
     /*2 初始化cdev*/
    dev1.cdev_test.owner = THIS_MODULE;
    cdev_init(&dev1.cdev_test, &cdev_test_fops);

    /*3 添加一个cdev,完成字符设备注册到内核*/
   ret =  cdev_add(&dev1.cdev_test, dev1.dev_num, 1);
    if(ret<0)
    {
        goto  err_chr_add;
    }
    /*4 创建类*/
  dev1. class = class_create(THIS_MODULE, "test");
    if(IS_ERR(dev1.class))
    {
        ret=PTR_ERR(dev1.class);
        goto err_class_create;
    }
    /*5  创建设备*/
  dev1.device = device_create(dev1.class, NULL, dev1.dev_num, NULL, "test");
    if(IS_ERR(dev1.device))
    {
        ret=PTR_ERR(dev1.device);
        goto err_device_create;
    }
/*本实验重点*****/
    dev1.vir_gpio_dr=ioremap(GPIO_DR,4);  //将物理地址转化为虚拟地址
    if(IS_ERR(dev1.vir_gpio_dr))
    {
        ret=PTR_ERR(dev1.vir_gpio_dr);  //PTR_ERR()来返回错误代码
        goto err_ioremap;
    }
return 0;

err_ioremap:
        iounmap(dev1.vir_gpio_dr);

 err_device_create:
        class_destroy(dev1.class);                 //删除类

err_class_create:
       cdev_del(&dev1.cdev_test);                 //删除cdev

err_chr_add:
        unregister_chrdev_region(dev1.dev_num, 1); //注销设备号

err_chrdev:
        return ret;
}

static void __exit chr_fops_exit(void) //驱动出口函数
{
    /*注销字符设备*/
    unregister_chrdev_region(dev1.dev_num, 1); //注销设备号
    cdev_del(&dev1.cdev_test);                 //删除cdev
    device_destroy(dev1.class, dev1.dev_num);    //删除设备
    class_destroy(dev1.class);                 //删除类
}
module_init(chr_fops_init);
module_exit(chr_fops_exit);
MODULE_LICENSE("GPL v2");
MODULE_AUTHOR("topeet");
```

### 关键代码：将物理地址转化为虚拟地址
```c
#define  GPIO_DR 0xFDD60000

struct device_test{
   
    dev_t dev_num;  //设备号
    int major ;  //主设备号
    int minor ;  //次设备号
    struct cdev cdev_test; // cdev
    struct class *class;   //类
    struct device *device; //设备
    char kbuf[32];
    unsigned int *vir_gpio_dr;
};



    if(test_dev->kbuf[0]==1){   //如果应用层传入的数据是1，则打开灯
            *(test_dev->vir_gpio_dr) = 0x8000c040;   //设置数据寄存器的地址
            printk("test_dev->kbuf [0]  is %d\n",test_dev->kbuf[0]);  //打印传入的数据
    }else if(test_dev->kbuf[0]==0){  //如果应用层传入的数据是0，则关闭灯
        *(test_dev->vir_gpio_dr) = 0x80004040; //设置数据寄存器的地址
        printk("test_dev->kbuf [0]  is %d\n",test_dev->kbuf[0]); //打印传入的数据
	}



/*本实验重点*****/
    dev1.vir_gpio_dr=ioremap(GPIO_DR,4);  //将物理地址转化为虚拟地址
```




## 18.3.2 编写测试 APP

本应用程序对应的网盘路径为：iTOP-RK3568开发板【底板V1.7版本】\\03\_【iTOP-RK3568开发板】指南教程\\02\_Linux驱动配套资料\\04\_Linux驱动例程\\13\\app。

> 编写测试app,led驱动加载成功之后会生成/dev/test节点，应用程序APP通过操作/dev/test文件来完成对LED设备的控制。**向/dev/test文件写入0表示关闭LED灯**，写入1表示打开LED灯。

### 编写完成的应用程序app.c代码如下：

```c
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>

int main(int argc, char *argv[])  
{
    int fd;
    char buf[32] = {0};   
    fd = open("/dev/test", O_RDWR);  //打开led驱动
    if (fd < 0)
    {
        perror("open error \n");
        return fd;
}
 // atoi()将字符串转为整型，这里将第一个参数转化为整型后，存放在 buf[0]中
buf[0] =atoi(argv[1]);  
write(fd,buf,sizeof(buf));  //向/dev/test文件写入数据
    close(fd);     //关闭文件
    return 0;
}
```

# 18.4 运行测试

驱动模块file.ko和测试程序app都已经准备好了，接下来就是运行测试。

输入以下命令加载驱动程序，如下（图 18-22）所示：

> insmod file.ko

![嵌入式知识学习（通用扩展）/linux驱动入门/第二期 字符设备基础/assets/第18章 点亮LED灯实验/0efa159c417b5a79a1ee21066898bc45\_MD5.jpg](assets/第18章%20点亮LED灯实验/0efa159c417b5a79a1ee21066898bc45_MD5.jpg)

> 然后运行测试程序，**输入“./app 1”，LED灯点亮**，如下图（图 18-24）所示：

![嵌入式知识学习（通用扩展）/linux驱动入门/第二期 字符设备基础/assets/第18章 点亮LED灯实验/d53be69810aad46018bbf0ea48f6886f\_MD5.jpg](assets/第18章%20点亮LED灯实验/d53be69810aad46018bbf0ea48f6886f_MD5.jpg)

![嵌入式知识学习（通用扩展）/linux驱动入门/第二期 字符设备基础/assets/第18章 点亮LED灯实验/abd274be42f678299c5aa53444d35136\_MD5.jpg](assets/第18章%20点亮LED灯实验/abd274be42f678299c5aa53444d35136_MD5.jpg)

输入“./app 0”,LED灯熄灭，如下图（图 18-26）所示：

![嵌入式知识学习（通用扩展）/linux驱动入门/第二期 字符设备基础/assets/第18章 点亮LED灯实验/adadaa437d5a29b09767c54b066581d5\_MD5.jpg](assets/第18章%20点亮LED灯实验/adadaa437d5a29b09767c54b066581d5_MD5.jpg)




