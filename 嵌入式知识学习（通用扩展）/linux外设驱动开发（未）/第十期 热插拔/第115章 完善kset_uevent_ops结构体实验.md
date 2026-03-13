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
url: https://blog.csdn.net/BeiJingXunWei/article/details/135505440?spm=1001.2101.3001.10752
title: "RK3568驱动指南｜第十篇 热插拔-第115章 完善kset_uevent_ops结构体实验_rk3568 调用npu-CSDN博客"
description: "文章浏览阅读1.1k次，点赞24次，收藏21次。然后，我们可以定义一个包含所需事件处理逻辑的函数，并将其赋值给uevent字段，这样当事件发生时，内核就会调用我们定义的处理函数。通过分析代码，我们知道在内核中，通过kset数据结构来组织kobject，并通过kset_uevent_ops结构体来定义uevent事件的处理函数。总结起来，通过实验和完善`kset_uevent_ops`结构体，我们可以扩展内核的uevent事件处理能力，使其更加灵活和适应各种应用场景。通过填充这个结构体中的字段，我们可以定义自己的事件处理函数，从而响应特定的事件。_rk3568 调用npu"
host: blog.csdn.net
```



# 一、完善kset_uevent_ops结构体实验

## kset_uevent_ops 作用：
### 1 、通过kset数据结构来组织kobject


### 2 、通过kset_uevent_ops结构体来定义uevent事件的处理函数。(❤️)


### 3 、

## 驱动程序编写

### 4 、实验了解：(❤️)
> 本实验对应的网盘路径为：iTOP-RK3568开发板【底板V1.7版本】\03_【iTOP-RK3568开发板】指南教程\02_Linux驱动配套资料\04_Linux驱动例程\79_uevent_ops\module。

> 我们编写驱动程序，首先，需要创建一个自定义的kset对象，并将其与相应的kobject关联起来。然后，我们可以**定义一个包含所需事件处理逻辑的函数，并将其赋值给uevent字段，这样当事件发生时，内核就会调用我们定义的处理函数**。在处理函数中，可以根据特定的事件类型执行我们想要的操作，例如读取设备信息、处理设备状态变化等。我们还可以**使用add_uevent_var函数向uevent环境中添加自定义的键值对，以提供额外的信息给用户空间**。通过这种方式，我们可以定制内核中的uevent事件处理机制，使其适应特定需求。这种定制化的事件处理机制可以用于各种场景，例如设备驱动程序、模块加载和卸载等。

> 总结起来，通过实验和完善`kset_uevent_ops`结构体，我们可以**扩展内核的uevent事件处理能力**，使其更加灵活和适应各种应用场景。这为我们提供了在内核和用户空间之间进行通信和交互的强大工具。

### 5、编写完成的uevent_ops.c代码如下

```c
#include <linux/module.h>
#include <linux/init.h>
#include <linux/slab.h>
#include <linux/configfs.h>
#include <linux/kernel.h>
#include <linux/kobject.h>
 
struct kobject *mykobject01;
struct kobject *mykobject02;
struct kset *mykset;
struct kobj_type mytype;
 
// 定义一个回调函数，返回kset的名称
const char *myname(struct kset *kset, struct kobject *kobj)
{
    return "my_kset";
};
 
// 定义一个回调函数，处理kset的uevent事件
int myevent(struct kset *kset, struct kobject *kobj, struct kobj_uevent_env *env)
{
    add_uevent_var(env, "MYDEVICE=%s", "TOPEET");
    return 0;
};
 
// 定义一个回调函数，用于过滤kset中的kobject
int myfilter(struct kset *kset, struct kobject *kobj)
{
    if (strcmp(kobj->name, "mykobject01") == 0){
        return 0; // 返回0表示通过过滤
    }else{
        return 1; // 返回1表示过滤掉
    }
};
 
struct kset_uevent_ops my_uevent_ops = {
    .filter = myfilter,
    .uevent = myevent,
    .name = myname,
};
 
// 模块的初始化函数
static int mykobj_init(void)
{
    int ret;
 
    // 创建并添加一个kset
    mykset = kset_create_and_add("mykset", &my_uevent_ops, NULL);
 
    // 分配并初始化一个kobject
    mykobject01 = kzalloc(sizeof(struct kobject), GFP_KERNEL);
    mykobject01->kset = mykset;
 
    // 初始化并添加kobject到kset
    ret = kobject_init_and_add(mykobject01, &mytype, NULL, "%s", "mykobject01");
 
    // 分配并初始化一个kobject
    mykobject02 = kzalloc(sizeof(struct kobject), GFP_KERNEL);
    mykobject02->kset = mykset;
 
    // 初始化并添加kobject到kset
    ret = kobject_init_and_add(mykobject02, &mytype, NULL, "%s", "mykobject02");
 
    // 触发一个uevent事件，表示mykobject01的属性发生了变化
    ret = kobject_uevent(mykobject01, KOBJ_CHANGE);
    // 触发一个uevent事件，表示mykobject02被添加
    ret = kobject_uevent(mykobject02, KOBJ_ADD);
 
    return 0;
}
 
// 模块退出函数
static void mykobj_exit(void)
{
    // 释放kobject
    kobject_put(mykobject01);
    kobject_put(mykobject02);
    kset_unregister(mykset);
}
 
module_init(mykobj_init); // 指定模块的初始化函数
module_exit(mykobj_exit); // 指定模块的退出函数
 
MODULE_LICENSE("GPL");   // 模块使用的许可证
MODULE_AUTHOR("topeet"); // 模块的作者
```

### 6、关键代码：(❤️)
```c

// 定义一个回调函数，返回kset的名称
const char *myname(struct kset *kset, struct kobject *kobj)
{
    return "my_kset";
};
// 定义一个回调函数，处理kset的uevent事件
int myevent(struct kset *kset, struct kobject *kobj, struct kobj_uevent_env *env)
{
    add_uevent_var(env, "MYDEVICE=%s", "TOPEET");
    return 0;
};
// 定义一个回调函数，用于过滤kset中的kobject
int myfilter(struct kset *kset, struct kobject *kobj)
{
    if (strcmp(kobj->name, "mykobject01") == 0){
        return 0; // 返回0表示通过过滤
    }else{
        return 1; // 返回1表示过滤掉
    }
};



struct kset_uevent_ops my_uevent_ops = {
    .filter = myfilter,
    .uevent = myevent,
    .name = myname,
};

// 模块的初始化函数
static int mykobj_init(void)：：

    // 创建并添加一个kset
    mykset = kset_create_and_add("mykset", &my_uevent_ops, NULL);

    // 触发一个uevent事件，表示mykobject01的属性发生了变化
    ret = kobject_uevent(mykobject01, KOBJ_CHANGE);
    // 触发一个uevent事件，表示mykobject02被添加
    ret = kobject_uevent(mykobject02, KOBJ_ADD);



```


### 7、


### 8、



## 运行测试
### 1 、驱动模块的加载
> ![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第115章 完善kset_uevent_ops结构体实验/file-20260313121229072.png]]
> 
> ![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第115章 完善kset_uevent_ops结构体实验/file-20260313121240072.png]]




### 2 、驱动的卸载
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第115章 完善kset_uevent_ops结构体实验/file-20260313121304736.png]]

### 3 、





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


