---
title: "RK3568驱动指南｜第九篇 设备模型-第94章 引入并完善kobject_type结构体"
source: "https://blog.csdn.net/BeiJingXunWei/article/details/135358514"
author:
  - "[[BeiJingXunWei]]"
published: 2024-01-03
created: 2025-09-14
description: "文章浏览阅读1k次，点赞17次，收藏15次。瑞芯微RK3568芯片是一款定位中高端的通用型SOC，采用22nm制程工艺，搭载一颗四核Cortex-A55处理器和Mali G52 2EE 图形处理器。RK3568 支持4K 解码和 1080P 编码，支持SATA/PCIE/USB3.0 外围接口。RK3568内置独立NPU，可用于轻量级人工智能应用。RK3568 支持安卓 11 和 linux 系统，主要面向物联网网关、NVR 存储、工控平板、工业检测、工控盒、卡拉 OK、云终端、车载中控等行业。​【公众号】迅为电子。"
tags:
  - "clippings"
---

# 备注(声明)：


# 参考文章：




# 一、引入并完善kobject_type结构体

## 驱动程序编写
### 1 、实验介绍：
> 本实验对应的网盘路径为：iTOP-RK3568开发板【底板V1.7版本】\03_【iTOP-RK3568开发板】指南教程\02_Linux驱动配套资料\04_Linux驱动例程\69_ktype\module。
> 
> 我们编写驱动代码，该代码实现了一个简单的内核模块，**创建了一个自定义的 kobject 对象，并定义了相应的初始化和释放函数。**

### 2 、编写完成的ktype.c代码如下所示：(❤️)
```c
#include <linux/module.h>
#include <linux/init.h>
#include <linux/slab.h>
#include <linux/configfs.h>
#include <linux/kernel.h>
#include <linux/kobject.h>
 
// 定义了kobject指针变量：mykobject03
struct kobject *mykobject03;
 
// 定义kobject的释放函数
static void dynamic_kobj_release(struct kobject *kobj)
{
    printk("kobject: (%p): %s\n", kobj, __func__);
    kfree(kobj);
}
 
// 定义了一个kobj_type结构体变量mytype，用于描述kobject的类型。
struct kobj_type mytype = {
    .release = dynamic_kobj_release,
};
 
// 模块的初始化函数
static int mykobj_init(void)
{
    int ret;
 
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
    kobject_put(mykobject03);
}
 
module_init(mykobj_init); // 指定模块的初始化函数
module_exit(mykobj_exit); // 指定模块的退出函数
 
MODULE_LICENSE("GPL");   // 模块使用的许可证
MODULE_AUTHOR("topeet"); // 模块的作者
```



### 3 、


## 运行测试
### 4 、驱动模块的加载
![[嵌入式知识学习（通用扩展）/linux驱动入门/第九期 设备模型/assets/第94章 引入并完善kobject_type结构体/file-20260310102206043.png]]


### 5、




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


