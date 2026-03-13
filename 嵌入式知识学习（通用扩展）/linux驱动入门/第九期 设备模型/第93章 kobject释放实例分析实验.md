---
title: "RK3568驱动指南｜第九篇 设备模型-第93章 kobject释放实例分析实验"
source: "https://blog.csdn.net/BeiJingXunWei/article/details/135346414"
author:
  - "[[BeiJingXunWei]]"
published: 2024-01-03
created: 2025-09-14
description: "文章浏览阅读1k次，点赞28次，收藏17次。kobject_create_and_add()函数首先调用 kobject_create()函数，该函数使用 kzalloc()为 kobject分配内存空间。接下来，kobject_create_and_add()函数调用 kobject_add()函数将 kobject添加到系统中，使其可见。kobject_add()函数内部调用了kobject_add_internal()函数，该函数负责将 kobject添加到父对象的子对象列表中，并创建相应的 sysfs 文件系统条目。_rk3568 kobject"
tags:
  - "clippings"
---


# 备注(声明)：


# 参考文章：




# 一、Kobj是如何释放的？

## 先明白kobj是如何创建的
### 1 、使用 kobject_create_and_add()函数创建 kobject：(❤️)
>  kobject_create_and_add()函数`首先调用 kobject_create()函数`，该函数使用 **kzalloc()为 kobject分配内存空间**。在 kobject_create()函数中，`调用 kobject_init()函数`**对分配的内存进行初始化**，并**指定了默认的 ktype**。

> 接下来，kobject_create_and_add()函数`调用 kobject_add()函数`**将 kobject添加到系统中**，使其可见。
> 
> kobject_add()函数内部调用了kobject_add_internal()函数，该函数负责将 kobject添加到父对象的子对象列表中，并创建相应的 sysfs 文件系统条目。


### 2 、使用 kobject_init_and_add()函数创建 kobject：
>  kobject_init_and_add()函数**需要手动分配内存**，并`通过 kobject_init()函数`**对分配的内存进行初始化** 。此时**需要自己实现 ktype结构体**。初始化完成后，

> `调用 kobject_add()函数`**将 kobject 添加到系统中。**



### 3 、最终都会调用 kobject_add()函数将 kobject添加到系统中(❤️)



### 4 、


## 追踪释放函数——kobject_put()函数的实现。

### 5、当引用计数器的值变为0以后，会调用release函数执行释放的操作(❤️)
![[嵌入式知识学习（通用扩展）/linux驱动入门/第九期 设备模型/assets/第93章 kobject释放实例分析实验/file-20260309170253515.png]]

### 6、Linux系统帮我们实现好了释放函数
![[嵌入式知识学习（通用扩展）/linux驱动入门/第九期 设备模型/assets/第93章 kobject释放实例分析实验/file-20260309170430530.png|697]]

- 1 该函数最终会去调用kobject_cleanup函数


## kobject_cleanup函数
### 7、kobject_cleanup函数实现如下

> 如上图所示，函数定义了一个名叫kobject_cleanup的静态函数，参数为一个指向 struct kobject 结构体的指针 kobj。函数**内部定义了一个指向 struct kobj_type 结构体的指针 t，用于获取 kobj 的类型信息**。还定义了一个指向常量字符的指针 name，用于保存 kobj 的名称。接下来，使用 pr_debug 打印调试信息，显示 kobject 的名称、地址、函数名称和父对象的地址。
> 
> ![[嵌入式知识学习（通用扩展）/linux驱动入门/第九期 设备模型/assets/第93章 kobject释放实例分析实验/file-20260309170512302.png|0]]


> 然后，检查 kobj 的类型信息 t 是否存在，并且检查 t->release 是否为 NULL。如下图所示：
> ![[嵌入式知识学习（通用扩展）/linux驱动入门/第九期 设备模型/assets/第93章 kobject释放实例分析实验/file-20260309170628437.png]]


> 如果 t 存在但 t->release 为 NULL，表示 kobj 的类型没有定义释放函数，会打印调试信息指示该情况。
> 
> **接下来，检查 kobj 的状态变量** state_add_uevent_sent 和 state_remove_uevent_sent。如果 state_add_uevent_sent 为真而 state_remove_uevent_sent 为假，表示调用者没有发送 "remove" 事件，会自动发送 "remove" 事件。
> 
> 然后，检查 kobj 的状态变量 state_in_sysfs。如果为真，表示调用者没有从 sysfs 中删除 kobj，会自动调用 kobject_del() 函数将其从 sysfs 中删除。
> 
> 接下来，再次检查 t 是否存在，并且**检查 t->release 是否存在。如果存在，表示 kobj 的类型定义了释放函数，会调用该释放函数进行资源清理**。如下图所示：
> ![[嵌入式知识学习（通用扩展）/linux驱动入门/第九期 设备模型/assets/第93章 kobject释放实例分析实验/file-20260309170647831.png]]
> 

> 最后，**检查 name 是否存在。如果存在，表示 kobj 的名称是动态分配的，会释放该名称的内存**。这就是 kobject_cleanup() 函数的实现。，


### 8、它负责执行 kobject 的资源清理和释放操作(❤️)
> 包括处理类型信息、发送事件、删除 sysfs 中的对象以及调用释放函数。
> 
> kobject_cleanup() 函数的实现表明，**最终调用的释放函数是在 kobj_type 结构体中定义的**。这解释了为什么在使用 kobject_init_and_add() 函数时，kobj_type 结构体不能为空的原因。因为释放函数是在 kobj_type 结构体中定义的，如果不实现释放函数，就无法进行正确的资源释放。



## dynamic_kobj_ktype
### 1 、是一个 kobj_type 结构体对象
![[嵌入式知识学习（通用扩展）/linux驱动入门/第九期 设备模型/assets/第93章 kobject释放实例分析实验/file-20260309181732788.png]]

### 2 、用于定义动态创建的 kobject 的类型。它指定了释放函数和 sysfs 操作。


### 3 、dynamic_kobj_release函数如下
![[嵌入式知识学习（通用扩展）/linux驱动入门/第九期 设备模型/assets/第93章 kobject释放实例分析实验/file-20260309181744002.png]]


#### 确保在释放 kobject 时执行必要的资源清理和释放操作(❤️)


### 4 、




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


