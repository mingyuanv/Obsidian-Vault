---
title: "{{title}}"
aliases:
tags:
description:
source: https://blog.csdn.net/BeiJingXunWei/article/details/134370618?spm=1001.2101.3001.10796
---

# 备注(声明)：




# 一、基础知识

## of_match_table
### 1 、设备树能够与驱动程序进行匹配要求
> 在前面平台总线相关章节的学习中，了解到只有platform_device结构体中的name 属性与platform_driver结构体中嵌套的driver结构体name属性或者id_table相同才能加载probe初始化函数。

> 而为了使设备树能够与驱动程序进行匹配，需要在platform_driver驱动程序中**添加driver结构体的of_match_table 属性**。这个属性**是一个指向 const struct of_device_id 结构的指针**，用于描述设备树节点和驱动程序之间的匹配规则。


### 2 、of_device_id 结构体(❤️)
- 1 定义在内核源码的“/include/linux/mod_devicetable.h”文件中
```c
struct of_device_id {
	char name[32];
	char type[32];
	char compatible[128]；
	const void *data;
};
```
> truct of_device_id 结构体**通常作为一个数组**在驱动程序中定义，用于描述设备树节点和驱动程序之间的匹配规则。数组的**最后一个元素必须是一个空的结构体**，以标记数组的结束。




### 3 、示例，展示了如何在驱动程序中使用 struct of_device_id 进行设备树匹配：
```c
static const struct of_device_id my_driver_match[]={
	{.compatible="vendor,device-1"},
	{.compatible="vendor,device-2"},
	{},
};

```
> 在上述示例中，my_driver_match 是一个 struct of_device_id 结构体数组。每个数组元素都包含了一个 compatible 字段，用于指定设备树节点的兼容性字符串。驱动程序将根据这些兼容性字符串与设备树中的节点进行匹配。



### 4 、




# 二、实验 - 设备树下platform_device和platform_driver匹配

## 设备树的编写
### 1 、设备树描述下面的内存资源：
> ****内存资源：****
> 
> 起始地址：0xFDD60000
> 
> 结束地址：0xFDD60004

> 然后编写对应的platform_driver驱动程序，要求跟上述内存资源所创建的节点进行匹配，从而验证 上一小节讲解的of_match_table 属性。

### 2 、rk3568的设备树结构
- 1 根据sdk源码目录下的“device/rockchip/rk356x/BoardConfig-rk3568-evb1-ddr4-v10.mk”默认配置文件可以了解

- 2 编译的设备树为rk3568-evb1-ddr4-v10-linux.dts,设备树之间的包含关系如下表

<table><tbody><tr><td><p>顶层设备树</p></td><td colspan="2" rowspan="1"><p>rk3568-evb1-ddr4-v10-linux.dts</p></td></tr><tr><td><p>第二级设备树</p></td><td><p>rk3568-evb1-ddr4-v10.dtsi</p></td><td><p>rk3568-linux.dtsi</p></td></tr><tr><td><p>第三级设备树</p></td><td><p>rk3568.dtsi</p><p>rk3568-evb.dtsi</p><p>topeet_screen_choose.dtsi</p><p>topeet_rk3568_lcds.dtsi</p></td><td></td></tr></tbody></table>

#### rk3568默认配置文件解析
```shell
#!/bin/bash

# 设置目标架构为arm64，指定了编译器工具链和其他相关设置将针对64位ARM架构
export RK_ARCH=arm64

# 设置U-Boot的默认配置为rk3568，这通常指向一个特定硬件平台的配置文件
export RK_UBOOT_DEFCONFIG=rk3568

# 指定U-Boot镜像格式类型为fit（Flattened Image Tree），这是一种用于存储多个二进制文件的格式
export RK_UBOOT_FORMAT_TYPE=fit

# 定义内核的默认配置为rockchip_linux_defconfig，这是Rockchip平台Linux内核的一个预设配置
export RK_KERNEL_DEFCONFIG=rockchip_linux_defconfig

# 内核默认配置片段，这里为空，表示没有额外的配置片段要应用
export RK_KERNEL_DEFCONFIG_FRAGMENT=

# 设置内核设备树源(DTS)文件为rk3568-evb1-ddr4-v10-linux，对应于特定硬件版本的设备树描述
export RK_KERNEL_DTS=rk3568-evb1-ddr4-v10-linux

# 定义boot镜像类型为boot.img，这是Android系统中使用的引导映像格式
export RK_BOOT_IMG=boot.img

# 指定内核镜像路径，这里的路径是相对于构建环境根目录下的kernel模块生成的Image文件位置
export RK_KERNEL_IMG=kernel/arch/arm64/boot/Image

# 内核镜像格式类型同样设置为fit
export RK_KERNEL_FIT_ITS=boot.its

# GPT分区表参数，指定用于创建GPT分区表的配置文件
export RK_PARAMETER=parameter-buildroot-fit.txt

# Buildroot配置名称，Buildroot是一个简化嵌入式Linux系统开发的工具
export RK_CFG_BUILDROOT=rockchip_rk3568

# Recovery模式配置名称，Recovery模式允许用户执行系统修复和更新操作
export RK_CFG_RECOVERY=rockchip_rk356x_recovery

# Recovery镜像格式类型设置为fit
export RK_RECOVERY_FIT_ITS=boot4recovery.its

# Ramboot配置，此处未定义具体值，Ramboot是指完全在RAM中运行的操作系统
export RK_CFG_RAMBOOT=

# Pcba配置，Pcba可能指的是电路板自动测试，但在此上下文中未定义具体值
export RK_CFG_PCBA=

# 目标产品芯片系列，这里是rk356x系列
export RK_TARGET_PRODUCT=rk356x

# 根文件系统类型设置为ext4，一种日志文件系统，适用于大多数Linux发行版
export RK_ROOTFS_TYPE=ext4

# 设置Debian版本为buster（即Debian 10），用于基于Debian的Linux发行版
export RK_DEBIAN_VERSION=buster

# Yocto项目机器名称，Yocto Project是一个开源协作项目，用于创建自定义Linux系统
export RK_YOCTO_MACHINE=rockchip-rk3568-evb

# 根文件系统镜像路径，根据前面定义的RK_ROOTFS_TYPE决定实际文件扩展名
export RK_ROOTFS_IMG=rockdev/rootfs.${RK_ROOTFS_TYPE}

# Ramboot镜像类型未定义具体值
export RK_RAMBOOT_TYPE=

# OEM分区类型设置为ext2，一种早期的Linux文件系统格式
export RK_OEM_FS_TYPE=ext2

# 用户数据分区类型设置为ext2，同上
export RK_USERDATA_FS_TYPE=ext2

# OEM配置目录，默认配置为oem_normal
export RK_OEM_DIR=oem_normal

# 注释掉的行表示是否使用Buildroot来构建OEM部分，默认不启用
#export RK_OEM_BUILDIN_BUILDROOT=YES

# 用户数据配置目录，默认配置为userdata_normal
export RK_USERDATA_DIR=userdata_normal

# 杂项镜像，可能是用于清除或初始化某些系统状态的特殊镜像
export RK_MISC=wipe_all-misc.img

# 分发模块启用选项，当前未定义任何分发模块
export RK_DISTRO_MODULE=

# 定义此板卡的预构建脚本，这个脚本将在构建过程开始前执行
export RK_BOARD_PRE_BUILD_SCRIPT=app-build.sh
```





### 3 、编写的设备树节点添加到rk3568-evb1-ddr4-v10-linux.dts中（顶层设备树）(❤️)
```d
/{
	topeet {
		#address-cells = <1>;
		#size-cells = <1>;
		compatible = "simple-bus";

		myled {
			compatible = "my devicestree";
			reg = <0xFDD60000 0x00000004>;

		};

	};

};
```
> 为了避免#address-cells = <1>; 和 #size-cells = <1>;这两个属性改变根节点其他的节点的属性，所以在这里创建了一个topeet节点。在这个示例中，**#address-cells 设置为 1表示地址使用一个32位的单元**，#size-cells 也设置为 1 表示大小使用一个32位的单元。
> 
> 第5行：将compatible属性设置为`"simple-bus"`用于表示 topeet 节点的兼容性，指明它是一个**简单总线设备**，**在转换platform_device的过程中，会继续查找该节点的子节点。**
> 
> 第8行：myLed 节点下的compatible属性为"my devicetree"，表明该节点将会被转换为platform_device。
> 
> 第9行：这个属性用于描述 myLed 节点的寄存器信息。reg 属性的值 <0xFDD60000 0x00000004> 表示 myLed 设备的寄存器起始地址为 0xFDD60000，大小为 0x00000004。



### 4 、





## 驱动程序的编写
### 1 、匹配设备树、字符设备、平台总线
```c
#include <linux/module.h>
#include <linux/platform_device.h>
#include <linux/mod_devicetable.h>

#include <linux/init.h>
#include <linux/kdev_t.h>
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/uaccess.h>
#include <linux/io.h>
#include <linux/wait.h>


struct device_test{

    dev_t dev_num;//设备号
    int major;  
    int minor;

    struct cdev cdev_test;  // 字符设备结构体
    struct class *class;    // 类指针
    struct device *device;  // 设备指针

    char kbuf[32];  // 内核缓冲区,存放数据
    int flag;  // 标志位，表示是否有数据可读

};

struct device_test dev1;



static int cdev_test_open(struct inode *inode,struct file *file){

    // 设置私有数据为设备结构体地址，方便其他函数使用
    file->private_data=&dev1;

    printk("This is cdev_test_open\r\n");

    return 0;
}

static int cdev_test_release(struct inode *inode, struct file *file)
{
    printk("This is cdev_test_release\r\n");
    return 0;
}


static ssize_t cdev_test_write (struct file *file,const char __user *buf,size_t size,loff_t *off){

    struct device_test *test_dev=(struct device_test *)file->private_data;

    if(copy_from_user(test_dev->kbuf,buf,size)!=0){

        printk("copy_from_user  error\r\n");

        return -1;
    }

    return 0;
}


static ssize_t cdev_test_read (struct file *file, char __user *buf,size_t size,loff_t *off){

    struct device_test *test_dev=(struct device_test *)file->private_data;

    if(copy_to_user(buf,test_dev->kbuf,strlen(test_dev->kbuf))!=0){

        printk("copy_from_user  error\r\n");

        return -1;
    }

    printk("This is cdev_test_read\r\n");

    return 0;
}



//文件操作集
struct file_operations cdev_test_fops={

    .owner = THIS_MODULE, //将owner字段指向本模块，可以避免在模块的操作正在被使用时卸载该模块
    .open=cdev_test_open,
    .read=cdev_test_read,
    .write=cdev_test_write,
    .release=cdev_test_release,

};




static int my_platform_probe(struct platform_device *pdev)
{
    int ret;

    printk(KERN_INFO "my_platform_probe: Probing platform device\n");

    /*1 创建设备号*/
    ret=alloc_chrdev_region(&dev1.dev_num,0,1,"alloc_name");
    if(ret<0){
        goto err_chrdev;
    }
    printk("alloc_chrdev_region is ok\n");

    //打印设备号
    dev1.major=MAJOR(dev1.dev_num);
    dev1.minor=MINOR(dev1.dev_num);
    printk("major is %d \r\n", dev1.major); //打印主设备号
    printk("minor is %d \r\n", dev1.minor); //打印次设备号

    /*2 初始化cdev*/
    dev1.cdev_test.owner=THIS_MODULE;
    cdev_init(&dev1.cdev_test,&cdev_test_fops);

    /*3 添加一个cdev,完成字符设备注册到内核*/
   ret=cdev_add(&dev1.cdev_test,dev1.dev_num,1);
    if(ret<0)
    {
        goto  err_chr_add;
    }

    /*4 创建类*/
    dev1.class=class_create(THIS_MODULE,"device-tree");
    if(IS_ERR(dev1.class)){

        ret=PTR_ERR(dev1.class);
        goto err_class_create;
    }

    /*5  创建设备*/
    dev1.device=device_create(dev1.class,NULL,dev1.dev_num,NULL,"device-tree");
    if(IS_ERR(dev1.device))
    {
        ret=PTR_ERR(dev1.device);
        goto err_device_create;
    }

return 0;

//错误处理
err_device_create:
    class_destroy(dev1.class);

err_class_create:
    cdev_del(&dev1.cdev_test);

err_chr_add:
    unregister_chrdev_region(dev1.dev_num,1);

err_chrdev:
    return ret;
}


static int my_platform_remove(struct platform_device *pdev)
{
    printk(KERN_INFO "my_platform_remove: Removing platform device\n");


    unregister_chrdev_region(dev1.dev_num, 1); 
    cdev_del(&dev1.cdev_test);                 
    device_destroy(dev1.class, dev1.dev_num);       
    class_destroy(dev1.class);                

    return 0;
}

//描述设备树节点和驱动程序之间的匹配规则
static const struct of_device_id of_match_table_id[]={
	{.compatible="my devicestree"},
	{},
};

// 定义平台驱动结构体
static struct platform_driver my_platform_driver = {
    .probe = my_platform_probe,
    .remove = my_platform_remove,
    .driver = {
        .name = "my_platform_device",
        .owner = THIS_MODULE,
        .of_match_table = of_match_table_id,
    },

};

// 模块初始化函数
static int __init my_platform_driver_init(void)
{
    int ret;
    ret = platform_driver_register(&my_platform_driver);
    if(ret){
        printk(KERN_ERR "Failed to register platform driver\n");

        return ret;
    }

    printk(KERN_INFO "my_platform_driver: Platform driver initialized\n");

    return 0;
}


// 模块退出函数
static void __exit my_platform_driver_exit(void)
{
    platform_driver_unregister(&my_platform_driver);
    printk(KERN_INFO "my_platform_driver: Platform driver exited\n");
}


module_init(my_platform_driver_init);
module_exit(my_platform_driver_exit);

MODULE_LICENSE("GPL v2");
MODULE_AUTHOR("topeet");

```

### 2 、关键代码 - 平台设备注册与匹配(❤️)
```c
static int my_platform_probe(struct platform_device *pdev)
{

	return 0;
}

//描述设备树节点和驱动程序之间的匹配规则
static const struct of_device_id of_match_table_id[]={
	{.compatible="my devicestree"},
	{},
};


// 定义平台驱动结构体
static struct platform_driver my_platform_driver = {
    .probe = my_platform_probe,
    .remove = my_platform_remove,
    .driver = {
        .name = "my_platform_device",
        .owner = THIS_MODULE,
        .of_match_table = of_match_table_id,
    },

};

    ret = platform_driver_register(&my_platform_driver);

    platform_driver_unregister(&my_platform_driver);

```

### 3 、




##  测试
### 1 、通过sys系统查看设备树结构(❤️)
> [root@topeet:/sys/firmware/devicetree/base]# cd topeet
> [root@topeet:/sys/firmware/devicetree/base/topeet]# ls
> '#address-cells'  '#size-cells'   compatible   myled   name
> [root@topeet:/sys/firmware/devicetree/base/topeet]# cd myled
> [root@topeet:/sys/firmware/devicetree/base/topeet/myled]# ls
> compatible  name  reg
[root@topeet:`/sys/firmware/devicetree/base/topeet/myled`]# `cat compatible`
**my devicestree**[root@topeet:/sys/firmware/devicetree/base/topeet/myled]#



### 2 、驱动模块的加载
> [root@topeet:~]# `insmod device_tree.ko`
[  462.621106] device_tree: loading out-of-tree module taints kernel.
[  462.623022] **my_platform_probe**: Probing platform device
[  462.623066] a[root@topeet:~]# lloc_chrdev_region is ok
[  462.623080] major is 236
[  462.623090] minor is 0
[  462.626459] my_platform_driver: Platform driver initialized
> 
> [root@topeet:~]# `ls /dev/device-tree`
> **/dev/device-tree**
> [root@topeet:~]#
> 
> [root@topeet:`/sys/class/device-tree]# ls`
**device-tree**



### 3 、




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


