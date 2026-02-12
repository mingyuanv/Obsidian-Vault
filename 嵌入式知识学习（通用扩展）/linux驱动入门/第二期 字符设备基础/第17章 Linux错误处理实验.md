---
title: "RK3568驱动指南｜第二篇 字符设备基础-第17章 Linux错误处理实验_linux 驱动 错误指针-CSDN博客"
source: "https://blog.csdn.net/BeiJingXunWei/article/details/132755346"
author:
  - "[[成就一亿技术人!]]"
  - "[[hope_wisdom 发出的红包]]"
published:
created: 2025-09-08
description: "文章浏览阅读456次。在编写驱动程序时，驱动程序应该提供函数执行失败后处理的能力。如果驱动程序中函数执行失败了，必须取消掉所有失败前的注册，否则内核会处于一个不稳定的状态，因为它包含了不存在代码的内部指针。int err;在以上代码中试图注册3个虚构设备，goto语句在失败情况下使用，对之前已经成功注册的设施进行注销。_linux 驱动 错误指针"
tags:
  - "clippings"
---

> 在前面章节进行的字符设备驱动实验中，即使是最简单的注册字符设备，也存在注册失败的可能性，因此在之前编写的驱动代码中采用检查函数返回值的方式，确认函数是否成功执行，而在本章节中将采用**goto语句对Linux错误处理进行更进一步的处理**。

# 17.1 goto语句简介

> 在编写驱动程序时，驱动程序应该提供函数执行失败后处理的能力。**如果驱动程序中函数执行失败了，必须取消掉所有失败前的注册**，否则内核会处于一个不稳定的状态，因为它包含了不存在代码的内部指针。在处理Linux错误时，最好使用goto语句，

## goto语句的使用示例如下：

```c
int   init my_init_function(void)
{
int err;
err = register_this(ptr1, "skull"); 
if (err)
    goto fail_this;

err = register_that(ptr2, "skull");
if (err)
    goto fail_that;

err = register_those(ptr3, "skull");
if (err)
    goto fail_those;

return 0;        
 
fail_those:
    unregister_that(ptr2, "skull"); 
fail_that:
    unregister_this(ptr1, "skull");
fail_this:
    return err;      
}
```

> 在以上代码中试图注册3个虚构设备，goto语句在失败情况下使用，对之前已经成功注册的设施进行注销。使用goto语句处理的时候，应该**遵循“先进后出”的原则**，如下图（图 17-1）所示：

![嵌入式知识学习（通用扩展）/linux驱动入门/第二期 字符设备基础/assets/第17章 Linux错误处理实验/37ba0b84be04e2d256f6c9b2b177dc45\_MD5.jpg](assets/第17章%20Linux错误处理实验/37ba0b84be04e2d256f6c9b2b177dc45_MD5.jpg)

> 如果在驱动代码中初始化和卸载函数比较复杂，goto方法可能变得难于管理，为了使代码重复性最小以及流程化，Linux提供了更简便的方法，我们接着来学习下一小节。

# 17.2 IS\_ERR()简介

## 指针来说，必然存在三种情况
> 对于任何一个指针来说，必然存在三种情况，一种是**合法指针**，一种是**NULL**(也就是空指针)，一种是**错误指针**(也就是无效指针)。
> 
> 在Linux内核中，所谓的`错误指针`已经指向了内核空间的最后一页，例如，对于一个64位系统来说，内核空间最后地址为0xffffffffffffffff，
> 那么**最后一页的地址是0xfffffffffffff000~0xffffffffffffffff**，这段地址是**被保留的，如果指针落在这段地址之内，说明是错误的无效指针。**


## 指针错误的处理机制
- 1 相关的函数接口主要有IS\_ERR()、PTR\_ERR()、ERR\_PTR()等，
- 2 其函数的源码在include/linux/err.h文件中，如下所示：

![嵌入式知识学习（通用扩展）/linux驱动入门/第二期 字符设备基础/assets/第17章 Linux错误处理实验/47117555b2e8baab1ba915958de75111\_MD5.jpg](assets/第17章%20Linux错误处理实验/47117555b2e8baab1ba915958de75111_MD5.jpg)

> 如上图所示，在Linux源码中**IS\_ERR()函数其实就是判断指针是否出错**，如果指针指向了内核空间的最后一页，就说明指针是一个无效指针，如果指针并不是落在内核空间的最后一页，就说明这指针是有效的。
**无效的指针能表示成一种负数的错误码**，
如果想知道这个指针是哪个错误码，使**用PTR\_ERR函数转化**。
0xfffffffffffff000~0xffffffffffffffff这段地址和Linux错误码是一一对应的，

## Linux内核错误码
- 1 内核错误码保存在errno-base.h文件中。如下所示：
- 2 kernel/include/uapi/asm-generic/errno-base.h

```d
/* SPDX-License-Identifier: GPL-2.0 WITH Linux-syscall-note */
// 声明这是一个遵循GPL 2.0协议以及包含Linux系统调用注意事项的文件。
#ifndef _ASM_GENERIC_ERRNO_BASE_H
#define _ASM_GENERIC_ERRNO_BASE_H

// 操作不允许。通常是请求的操作需要有更高的权限级别。
#define    EPERM         1    /* Operation not permitted */

// 没有该文件或目录。尝试访问不存在的文件或目录时返回。
#define    ENOENT        2    /* No such file or directory */

// 没有此进程。给定的进程ID无效或对应进程不存在。
#define    ESRCH         3    /* No such process */

// 系统调用被中断。由于接收到信号导致系统调用被中断。
#define    EINTR         4    /* Interrupted system call */

// I/O错误。输入输出过程中出现错误。
#define    EIO           5    /* I/O error */

// 没有这个设备或地址。指定的设备或地址不可用。
#define    ENXIO        6    /* No such device or address */

// 参数列表太长。传递给程序的参数列表超过了系统的限制。
#define    E2BIG         7    /* Argument list too long */

// 执行格式错误。试图执行一个格式不正确的可执行文件。
#define    ENOEXEC       8    /* Exec format error */

// 文件号错误。指定的文件描述符无效。
#define    EBADF         9    /* Bad file number */

// 没有子进程。尝试操作子进程但没有子进程存在。
#define    ECHILD       10    /* No child processes */

// 资源暂时不可用。请重试。例如资源被锁定或繁忙。
#define    EAGAIN       11    /* Try again */

// 内存不足。无法分配内存。
#define    ENOMEM       12    /* Out of memory */

// 权限被拒绝。对所请求的操作无足够权限。
#define    EACCES       13    /* Permission denied */

// 地址错误。尝试访问非法或未映射的内存地址。
#define    EFAULT       14    /* Bad address */

// 需要块设备。操作需要在块设备上进行，但提供的不是块设备。
#define    ENOTBLK      15    /* Block device required */

// 设备或资源忙。设备或资源当前正被使用。
#define    EBUSY        16    /* Device or resource busy */

// 文件已存在。尝试创建已存在的文件。
#define    EEXIST       17    /* File exists */

// 跨设备链接。尝试在不同文件系统之间建立链接。
#define    EXDEV        18    /* Cross-device link */

// 没有此设备。请求的设备不存在。
#define    ENODEV       19    /* No such device */

// 不是目录。期望的是目录但实际并非如此。
#define    ENOTDIR      20    /* Not a directory */

// 是目录。期望的是非目录文件但实际上是一个目录。
#define    EISDIR       21    /* Is a directory */

// 无效参数。传递给函数的参数无效。
#define    EINVAL       22    /* Invalid argument */

// 文件表溢出。系统打开的文件过多。
#define    ENFILE       23    /* File table overflow */

// 打开的文件过多。进程打开的文件数超过了允许的最大值。
#define    EMFILE       24    /* Too many open files */

// 不是终端设备。操作要求目标是一个终端设备，但不是。
#define    ENOTTY       25    /* Not a typewriter */

// 文本文件忙。尝试修改正在使用的可执行文件。
#define    ETXTBSY      26    /* Text file busy */

// 文件太大。文件大小超出了系统允许的最大值。
#define    EFBIG        27    /* File too large */

// 设备上没有剩余空间。磁盘或存储设备已满。
#define    ENOSPC       28    /* No space left on device */

// 非法的seek操作。尝试在一个不允许seek的文件上执行seek操作。
#define    ESPIPE       29    /* Illegal seek */

// 只读文件系统。尝试修改只读文件系统中的文件。
#define    EROFS        30    /* Read-only file system */

// 链接太多。文件的硬链接数达到了系统允许的最大值。
#define    EMLINK       31    /* Too many links */

// 管道破裂。管道的写入端关闭，无法再写入数据。
#define    EPIPE        32    /* Broken pipe */

// 数学参数超出函数的定义域。数学运算中的参数无效。
#define    EDOM         33    /* Math argument out of domain of func */

// 数学结果不能表示。计算的结果超出了可以表示的范围。
#define    ERANGE       34    /* Math result not representable */

#endif
```

## IS_ERR()的使用实例代码如下：
- 1 判断函数返回的指针是有效地址还是错误码
```c
myclass = class_create(THIS_MODULE, "myclass");
if (IS_ERR(myclass)) {
　　ret = PTR_ERR(myclass);
   goto fail;
}
    
mydevice = device_create(myclass, NULL, MKDEV(major, 0), NULL, "simple-device");
if (IS_ERR(mydevice)) {
　　class_destroy(myclass);
　　ret = PTR_ERR(mydevice);
　　goto fail;
}
```

> 在上述代码中，调用了class\_create()和device\_create()函数，必须使用IS\_ERR()函数判断返回的指针是否是有效的，**如果是无效的，需要调用PTR\_ERR()函数将无效指针转换为错误码**，**并进行错误码的返回**。

# 17.3 实验程序编写

## 17.3.1 驱动程序编写

本驱动程序对应的网盘路径为：iTOP-RK3568开发板【底板V1.7版本】\\03\_【iTOP-RK3568开发板】指南教程\\02\_Linux驱动配套资料\\04\_Linux驱动例程\\12\\module。

> 本实验在15章的驱动程序基础上进行编写，进行Linux错误处理实验。当创建设备号，初始化cdev，注册字符设备，创建类，创建设备的这些函数执行失败时，应该怎么处理呢，

### 编写好的驱动程序如下所示：

```c
#include <linux/init.h>
#include <linux/module.h>
#include <linux/kdev_t.h>
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/uaccess.h>

struct device_test{
   
    dev_t dev_num;  //设备号
     int major ;  //主设备号
    int minor ;  //次设备号
    struct cdev cdev_test; // cdev
    struct class *class;   //类
    struct device *device; //设备
    char kbuf[32];  //定义缓存区kbuf
};

struct  device_test dev1;   //定义一个device_test结构体变量

/*打开设备函数*/
static int cdev_test_open(struct inode *inode, struct file *file)
{
  
    file->private_data=&dev1;  //设置私有数据
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
    printk("This is cdev_test_write\r\n");
    printk("kbuf is %s\r\n", test_dev->kbuf);
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
    /*5创建设备*/
  dev1.device = device_create(dev1.class, NULL, dev1.dev_num, NULL, "test");
    if(IS_ERR(dev1.device))
    {
        ret=PTR_ERR(dev1.device);
        goto err_device_create;
    }

    return 0;

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
    device_destroy(dev1.class, dev1.dev_num);       //删除设备
    class_destroy(dev1.class);                 //删除类
}
module_init(chr_fops_init);
module_exit(chr_fops_exit);
MODULE_LICENSE("GPL v2");
MODULE_AUTHOR("topeet");
```

### 关键代码
```c
    /*5创建设备*/
  dev1.device = device_create(dev1.class, NULL, dev1.dev_num, NULL, "test");
    if(IS_ERR(dev1.device))
    {
        ret=PTR_ERR(dev1.device);
        goto err_device_create;
    }
```


## 17.3.2 编写测试 APP

本应用程序对应的网盘路径为：iTOP-RK3568开发板【底板V1.7版本】\\03\_【iTOP-RK3568开发板】指南教程\\02\_Linux驱动配套资料\\04\_Linux驱动例程\\12\\app。

### 完成的应用程序app.c代码如下
应用程序只是起简单的测试作用。

```c
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

int main(int argc, char *argv[]) //主函数
{
    int fd;
    char buf1[32] = "nihao";  //定义写入缓存区buf1
    fd = open("/dev/test", O_RDWR); //打开/dev/test设备
    if (fd < 0)
    {
        perror("open error \n");
        return fd;
    }
    write(fd,buf1,sizeof(buf1)); //向/dev/test设备写入数据
    close(fd);
    return 0;
}
```

# 17.4 运行测试

驱动模块file.ko和测试程序app都已经准备好了，接下来就是运行测试。

输入以下命令，加载驱动程序，如下图（图17-6）所示：

![嵌入式知识学习（通用扩展）/linux驱动入门/第二期 字符设备基础/assets/第17章 Linux错误处理实验/5b916101430d63f89567def6201a9c82\_MD5.jpg](assets/第17章%20Linux错误处理实验/5b916101430d63f89567def6201a9c82_MD5.jpg)

运行应用程序如下（图17-7）所示：

![嵌入式知识学习（通用扩展）/linux驱动入门/第二期 字符设备基础/assets/第17章 Linux错误处理实验/2ddb72ef015f7ef613a5df0ad4689443\_MD5.jpg](assets/第17章%20Linux错误处理实验/2ddb72ef015f7ef613a5df0ad4689443_MD5.jpg)

卸载驱动程序，如下图（图17-8）所示：

![嵌入式知识学习（通用扩展）/linux驱动入门/第二期 字符设备基础/assets/第17章 Linux错误处理实验/82f8500e2485bd4d8b2010291cfdd1fe\_MD5.jpg](assets/第17章%20Linux错误处理实验/82f8500e2485bd4d8b2010291cfdd1fe_MD5.jpg)





