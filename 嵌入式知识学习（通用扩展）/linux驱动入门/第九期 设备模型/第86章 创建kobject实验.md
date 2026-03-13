---
title: "RK3568驱动指南｜第九篇 设备树模型-第86章 创建kobject实验_rk3568的sdk中怎么为一个板子新建一个设备树-CSDN博客"
source: "https://blog.csdn.net/BeiJingXunWei/article/details/135286066"
author:
  - "[[成就一亿技术人!]]"
  - "[[hope_wisdom 发出的红包]]"
published:
created: 2025-09-14
description: "文章浏览阅读987次，点赞25次，收藏20次。本章介绍了两种创建kobject的方法，一种是使用kobject_create_and_add函数，另一种是使用kzalloc和kobject_init_and_add函数，还介绍了如何释放创建的kobject。最后，实验演示了将驱动程序加载到开发板上，并验证了创建的kobject是否成功。我们编写驱动代码演示如何在Linux内核模块中创建和管理kobject对象，其中包括俩种方法创建kobject对象，分别使用kobject_create_and_add和kobject_init_and_add函数。_rk3568的sdk中怎么为一个板子新建一个设备树"
tags:
  - "clippings"
---


# 备注(声明)：


# 参考文章：




# 一、创建kobject实验

##  驱动程序编写
### 1 、网盘资料
> 本实验对应的网盘路径为：iTOP-RK3568开发板【底板V1.7版本】\03_【iTOP-RK3568开发板】指南教程\02_Linux驱动配套资料\04_Linux驱动例程\66_make_kobj\module。



### 2 、实验介绍：
> 本章介绍了两种创建kobject的方法，一种是使用**kobject_create_and_add**函数，另一种是使用**kzalloc和kobject_init_and_add**函数，还介绍了如何释放创建的kobject。最后，实验演示了将驱动程序加载到开发板上，并验证了创建的kobject是否成功。
> 
> 我们编写驱动代码**演示如何在Linux内核模块中创建和管理kobject对象**，其中包括俩种方法创建kobject对象，分别使用kobject_create_and_add和kobject_init_and_add函数。通过这些操作，可以创建具有层次关系的kobject对象，并在模块初始化和退出时进行相应的管理的释放。





### 3 、编写完成的make_kobj.c代码如下(❤️)
```c
#include <linux/module.h>
#include <linux/init.h>
#include <linux/slab.h>
#include <linux/configfs.h>
#include <linux/kernel.h>
#include <linux/kobject.h>
 
// 定义了三个kobject指针变量：mykobject01、mykobject02、mykobject03
struct kobject *mykobject01;
struct kobject *mykobject02;
struct kobject *mykobject03;
 
// 定义了一个kobj_type结构体变量mytype，用于描述kobject的类型。
struct kobj_type mytype;
// 模块的初始化函数
static int mykobj_init(void)
{
    int ret;
    // 创建kobject的第一种方法
    // 创建并添加了名为"mykobject01"的kobject对象，父kobject为NULL
    mykobject01 = kobject_create_and_add("mykobject01", NULL);
    // 创建并添加了名为"mykobject02"的kobject对象，父kobject为mykobject01。
    mykobject02 = kobject_create_and_add("mykobject02", mykobject01);
 
    // 创建kobject的第二种方法
    // 1 使用kzalloc函数分配了一个kobject对象的内存
    mykobject03 = kzalloc(sizeof(struct kobject), GFP_KERNEL);
    // 2 初始化并添加到内核中，名为"mykobject03"。
    ret = kobject_init_and_add(mykobject03, &mytype, NULL, "%s", "mykobject03");
 
    return 0;
}
 
// 模块退出函数
static void mykobj_exit(void)
{
    // 释放了之前创建的kobject对象
    kobject_put(mykobject01);
    kobject_put(mykobject02);
    kobject_put(mykobject03);
}
 
module_init(mykobj_init); // 指定模块的初始化函数
module_exit(mykobj_exit); // 指定模块的退出函数
 
MODULE_LICENSE("GPL");   // 模块使用的许可证
MODULE_AUTHOR("topeet"); // 模块的作者
```


### 4 、

## 运行测试

### 5、驱动模块的加载
![[嵌入式知识学习（通用扩展）/linux驱动入门/第九期 设备模型/assets/第86章 创建kobject实验/file-20260309115441994.png]]

### 6、进入/sys/目录下查看：
![[嵌入式知识学习（通用扩展）/linux驱动入门/第九期 设备模型/assets/第86章 创建kobject实验/file-20260309115505940.png]]

> 我们发现kobject01，kobject03创建在系统根目录/sys目录下，kobject02的父节点是kobject01，所以被创建在mykobject02目录下。现在我们**成功验证了创建kobject就是在系统根目录/sys目录下创建一个文件夹**，他们是一一对应的关系。
> 


#### 创建kobject就是在系统根目录/sys目录下创建一个文件夹(❤️)

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


