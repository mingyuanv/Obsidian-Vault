---
title: "RK3568驱动指南｜第六篇-平台总线-第54章 点亮LED灯实验_rk3568 qt 读取led状态-CSDN博客"
source: "https://blog.csdn.net/BeiJingXunWei/article/details/133858560"
author:
  - "[[成就一亿技术人!]]"
  - "[[hope_wisdom 发出的红包]]"
published:
created: 2025-09-14
description: "文章浏览阅读1k次。在上个章节中，我们成功在platform驱动程序中读取到了设备资源信息，在本章节将进行具体的项目实践，要求在上节platform驱动程序的基础上，加入控制LED灯相关的代码（这部分代码可以参考“第18章 点亮LED灯实验”）。本小节的测试要使用两个ko文件和一个测试应用程序，第一个ko文件为第53章编译出来的platform_device.ko驱动，第二个ko文件为在上一小节编译出的probe.ko驱动文件，应用程序为上一小节编译出来的app。至此，使用平台总线的点亮LCD灯实验就完成了。_rk3568 qt 读取led状态"
tags:
  - "clippings"
---

# 备注(声明)：


# 参考文章：




# 一、实验

## 驱动程序编写
> 本实验对应的网盘路径为：iTOP-RK3568开发板【底板V1.7版本】\03_【iTOP-RK3568开发板】指南教程\02_Linux驱动配套资料\04_Linux驱动例程\43_platform_led\module。


### 1 、platform_led.c代码如下:
```c
#include <linux/module.h>
#include <linux/platform_device.h>
#include <linux/ioport.h>
#include <linux/kdev_t.h>
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/uaccess.h>
#include <linux/io.h>
 
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
    }
    else if(test_dev->kbuf[0]==0)  //如果应用层传入的数据是0，则关闭灯
    {
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
 
static int my_platform_driver_probe(struct platform_device *pdev)
{
    struct resource *res_mem;
	int ret;
	res_mem = platform_get_resource(pdev, IORESOURCE_MEM, 0);
    if (!res_mem) {
        dev_err(&pdev->dev, "Failed to get memory resource\n");
        return -ENODEV;
    }
 
	/*注册字符设备驱动*/
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
    dev1.vir_gpio_dr=ioremap(res_mem->start,4);  //将物理地址转化为虚拟地址
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
 
static int my_platform_driver_remove(struct platform_device *pdev)
{
    // 设备移除操作
    return 0;
}
 
static struct platform_driver my_platform_driver = {
    .driver = {
        .name = "my_platform_device", // 与 platform_device.c 中的设备名称匹配
        .owner = THIS_MODULE,
    },
    .probe = my_platform_driver_probe,
    .remove = my_platform_driver_remove,
};
 
static int __init my_platform_driver_init(void)
{
    int ret;
 
    ret = platform_driver_register(&my_platform_driver); // 注册平台驱动
    if (ret) {
        printk("Failed to register platform driver\n");
        return ret;
    }
 
    printk("Platform driver registered\n");
    return 0;
}
 
static void __exit my_platform_driver_exit(void)
{
        /*注销字符设备*/
    unregister_chrdev_region(dev1.dev_num, 1); //注销设备号
    cdev_del(&dev1.cdev_test);                 //删除cdev
    device_destroy(dev1.class, dev1.dev_num);       //删除设备
    class_destroy(dev1.class);                 //删除类
	platform_driver_unregister(&my_platform_driver); // 注销平台驱动
    printk("Platform driver unregistered\n");
}
 
module_init(my_platform_driver_init);
module_exit(my_platform_driver_exit);
 
MODULE_LICENSE("GPL");
MODULE_AUTHOR("topeet");

```


### 2 、字符设备+平台总线框架：（💌）
```c
#include <linux/module.h>
#include <linux/platform_device.h>
#include <linux/ioport.h>
#include <linux/kdev_t.h>
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/uaccess.h>
#include <linux/io.h>
 
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
    return 0;
}
 
/*向设备写入数据函数*/
static ssize_t cdev_test_write(struct file *file, const char __user *buf, size_t size, loff_t *off)
{
    return 0;
}
/**从设备读取数据*/
static ssize_t cdev_test_read(struct file *file, char __user *buf, size_t size, loff_t *off)
{
    return 0;
}
 
static int cdev_test_release(struct inode *inode, struct file *file)
{
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

static int my_platform_driver_probe(struct platform_device *pdev)
{
    struct resource *res_mem;
	int ret;
	res_mem = platform_get_resource(pdev, IORESOURCE_MEM, 0);
 
/*注册字符设备驱动*/
    /*1 创建设备号*/
    ret = alloc_chrdev_region(&dev1.dev_num, 0, 1, "alloc_name"); //动态分配设备号

    dev1.major = MAJOR(dev1.dev_num); //获取主设备号
    dev1.minor = MINOR(dev1.dev_num); //获取次设备号

     /*2 初始化cdev*/
    dev1.cdev_test.owner = THIS_MODULE;
    cdev_init(&dev1.cdev_test, &cdev_test_fops);
 
    /*3 添加一个cdev,完成字符设备注册到内核*/
   ret =  cdev_add(&dev1.cdev_test, dev1.dev_num, 1);
    /*4 创建类*/
   dev1. class = class_create(THIS_MODULE, "test");
    /*5  创建设备*/
   dev1.device = device_create(dev1.class, NULL, dev1.dev_num, NULL, "test");
  
//将物理地址转化为虚拟地址
    dev1.vir_gpio_dr=ioremap(res_mem->start,4);  
return 0;
}



static int my_platform_driver_remove(struct platform_device *pdev)
{
    // 设备移除操作
    return 0;
}

static struct platform_driver my_platform_driver = {
    .driver = {
        .name = "my_platform_device", // 与 platform_device.c 中的设备名称匹配
        .owner = THIS_MODULE,
    },
    .probe = my_platform_driver_probe,
    .remove = my_platform_driver_remove,
};


static int __init my_platform_driver_init(void)
{
    int ret;
    ret = platform_driver_register(&my_platform_driver); // 注册平台驱
    return 0;
}
 
static void __exit my_platform_driver_exit(void)
{
    /*注销字符设备*/
    unregister_chrdev_region(dev1.dev_num, 1); //注销设备号
    cdev_del(&dev1.cdev_test);                 //删除cdev
    device_destroy(dev1.class, dev1.dev_num);       //删除设备
    class_destroy(dev1.class);                 //删除类
	platform_driver_unregister(&my_platform_driver); // 注销平台驱动
}

module_init(my_platform_driver_init);
module_exit(my_platform_driver_exit);
 
MODULE_LICENSE("GPL");
MODULE_AUTHOR("topeet");
```


### 3 、led相关关键代码：（💌）

```c

/*打开设备函数*/
static int cdev_test_open(struct inode *inode, struct file *file)：：

    file->private_data=&dev1;//设置私有数据


/*向设备写入数据函数*/
static ssize_t cdev_test_write(struct file *file, const char __user *buf, size_t size, loff_t *off)：：

     struct device_test *test_dev=(struct device_test *)file->private_data;
	 
	// copy_from_user:用户空间向内核空间传数据
    if (copy_from_user(test_dev->kbuf, buf, size) != 0) 

    if(test_dev->kbuf[0]==1){   //如果应用层传入的数据是1，则打开灯
			//设置数据寄存器的地址
            *(test_dev->vir_gpio_dr) = 0x8000c040;   
    }
    else if(test_dev->kbuf[0]==0)  //如果应用层传入的数据是0，则关闭灯
    {
            *(test_dev->vir_gpio_dr) = 0x80004040; //设置数据寄存器的地址
    }

/**从设备读取数据*/
static ssize_t cdev_test_read(struct file *file, char __user *buf, size_t size, loff_t *off)：：

    struct device_test *test_dev=(struct device_test *)file->private_data;
    if (copy_to_user(buf, test_dev->kbuf, strlen( test_dev->kbuf)) != 0) // copy_to_user:内核空间向用户空间传数据



```

### 4 、





## 编写测试 APP
> 本应用程序对应的网盘路径为：iTOP-RK3568开发板【底板V1.7版本】\03_【iTOP-RK3568开发板】指南教程\02_Linux驱动配套资料\04_Linux驱动例程\43_platform_led\app。
### 1 、实验介绍（💌）
> 编写测试app,led驱动加载成功之后会生成/dev/test节点，**应用程序APP通过操作/dev/test文件来完成对LED设备的控制**。向/dev/test文件写入0表示关闭LED灯，**写入1表示打开LED灯**。编写完成的应用程序app.c代码如下所示：

### 2 、app.c代码如下
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

### 3 、


### 4 、




## 运行测试
### 1 、文件来源：
> 本小节的测试要使用两个ko文件和一个测试应用程序，第一个ko文件为第53章编译出来的platform_device.ko驱动，第二个ko文件为在上一小节编译出的probe.ko驱动文件，应用程序为上一小节编译出来的app。

### 2 、platform设备的注册
![嵌入式知识学习（通用扩展）/linux驱动入门/第六期 平台总线/assets/第54章 点亮LED灯实验/file-20251212142752046.png](assets/第54章%20点亮LED灯实验/file-20251212142752046.png)

### 3 、加载platform_led.ko驱动
![嵌入式知识学习（通用扩展）/linux驱动入门/第六期 平台总线/assets/第54章 点亮LED灯实验/file-20251212142804355.png](assets/第54章%20点亮LED灯实验/file-20251212142804355.png)

### 4 、test节点也成功创建了
![嵌入式知识学习（通用扩展）/linux驱动入门/第六期 平台总线/assets/第54章 点亮LED灯实验/file-20251212142829423.png](assets/第54章%20点亮LED灯实验/file-20251212142829423.png)


### 5、“./app 0”命令LED灯熄灭
- 2 默认情况下led灯的状态为常亮

![嵌入式知识学习（通用扩展）/linux驱动入门/第六期 平台总线/assets/第54章 点亮LED灯实验/file-20251212142856037.png](assets/第54章%20点亮LED灯实验/file-20251212142856037.png)
![嵌入式知识学习（通用扩展）/linux驱动入门/第六期 平台总线/assets/第54章 点亮LED灯实验/file-20251212142940687.png](assets/第54章%20点亮LED灯实验/file-20251212142940687.png)




### 6、输入“./app 1”，LED灯点亮
![嵌入式知识学习（通用扩展）/linux驱动入门/第六期 平台总线/assets/第54章 点亮LED灯实验/file-20251212142949980.png](assets/第54章%20点亮LED灯实验/file-20251212142949980.png)

![嵌入式知识学习（通用扩展）/linux驱动入门/第六期 平台总线/assets/第54章 点亮LED灯实验/file-20251212142955377.png](assets/第54章%20点亮LED灯实验/file-20251212142955377.png)
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


