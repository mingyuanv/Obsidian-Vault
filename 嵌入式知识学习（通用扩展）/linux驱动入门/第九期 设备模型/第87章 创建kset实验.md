---
title: "{{title}}"
aliases: 
tags: 
description: 
source:
---

# 备注(声明)：


# 参考文章：


```cardlink
url: https://blog.csdn.net/BeiJingXunWei/article/details/135288750?spm=1001.2101.3001.10796
title: "RK3568驱动指南｜第九篇 设备模型-第87章 创建kset实验_rk3558连接sata-CSDN博客"
description: "文章浏览阅读1k次，点赞23次，收藏13次。我们编写驱动代码，这段代码用于定义并初始化两个自定义内核对象 mykobject01 和 mykobject02，并将它们添加到一个自定义内核对象集合 mykset 中。代码中的注释对各个部分进行了解释，帮助理解代码的功能。通过演示实验现象，讲解了kset是一组kobject的集合，并解释了kobject在sys目录下生成的原因。iTOP-RK3568开发板【底板V1.7版本】\\03_【iTOP-RK3568开发板】指南教程\\02_Linux驱动配套资料\\04_Linux驱动例程\\。_rk3558连接sata"
host: blog.csdn.net
```


# 一、

## 驱动程序编写
### 1 、实验介绍：
> 本实验对应的网盘路径为：iTOP-RK3568开发板【底板V1.7版本】\03_【iTOP-RK3568开发板】指南教程\02_Linux驱动配套资料\04_Linux驱动例程\67_make_kset\module。
> 
> 我们编写驱动代码，这段代码用于定义并初始化两个自定义内核对象 mykobject01 和 mykobject02，**并将它们添加到一个自定义内核对象集合 mykset 中**。这些自定义内核对象可以用于在Linux内核中**表示和管理特定的功能或资源**。代码中的注释对各个部分进行了解释，帮助理解代码的功能


### 2 、编写完成的make_kset.c代码如下
```c
#include <linux/module.h>
#include <linux/init.h>
#include <linux/slab.h>
#include <linux/configfs.h>
#include <linux/kernel.h>
#include <linux/kobject.h>
 
// 定义kobject结构体指针，用于表示第一个自定义内核对象
struct kobject *mykobject01;
// 定义kobject结构体指针，用于表示第二个自定义内核对象
struct kobject *mykobject02;
// 定义kset结构体指针，用于表示自定义内核对象的集合
struct kset *mykset;
// 定义kobj_type结构体，用于定义自定义内核对象的类型
struct kobj_type mytype;
 
// 模块的初始化函数
static int mykobj_init(void)
{
    int ret;
 
    // 创建并添加kset，名称为"mykset"，父kobject为NULL，属性为NULL
    mykset = kset_create_and_add("mykset", NULL, NULL);
 
    // 为mykobject01分配内存空间，大小为struct kobject的大小，标志为GFP_KERNEL
    mykobject01 = kzalloc(sizeof(struct kobject), GFP_KERNEL);
    // 将mykset设置为mykobject01的kset属性
    mykobject01->kset = mykset;
    // 初始化并添加mykobject01，类型为mytype，父kobject为NULL，格式化字符串为"mykobject01"
    ret = kobject_init_and_add(mykobject01, &mytype, NULL, "%s", "mykobject01");
 
    // 为mykobject02分配内存空间，大小为struct kobject的大小，标志为GFP_KERNEL
    mykobject02 = kzalloc(sizeof(struct kobject), GFP_KERNEL);
    // 将mykset设置为mykobject02的kset属性
    mykobject02->kset = mykset;
    // 初始化并添加mykobject02，类型为mytype，父kobject为NULL，格式化字符串为"mykobject02"
    ret = kobject_init_and_add(mykobject02, &mytype, NULL, "%s", "mykobject02");
 
    return 0;
}
 
// 模块退出函数
static void mykobj_exit(void)
{
    // 释放mykobject01的引用计数
    kobject_put(mykobject01);
 
    // 释放mykobject02的引用计数
    kobject_put(mykobject02);
}
 
module_init(mykobj_init); // 指定模块的初始化函数
module_exit(mykobj_exit); // 指定模块的退出函数
 
MODULE_LICENSE("GPL");   // 模块使用的许可证
MODULE_AUTHOR("topeet"); // 模块的作者
```

### 3 、关键代码：(❤️)
```c

// 定义kset结构体指针，用于表示自定义内核对象的集合
struct kset *mykset;

static int mykobj_init(void)：：

  // 将mykset设置为mykobject01的kset属性
    mykobject01->kset = mykset;

   // 将mykset设置为mykobject02的kset属性
    mykobject02->kset = mykset;


```



### 4 、

##  运行测试

### 5、驱动模块的加载(❤️)
![[嵌入式知识学习（通用扩展）/linux驱动入门/第九期 设备模型/assets/第87章 创建kset实验/file-20260309120519731.png]]

### 6、





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


