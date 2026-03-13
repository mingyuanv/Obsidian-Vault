---
title: "RK3568驱动指南｜第九篇 设备树模型-第85章设备模型基本框架-kobject和kset_rk nvr源码 linux-CSDN博客"
source: "https://blog.csdn.net/BeiJingXunWei/article/details/135226684"
author:
  - "[[成就一亿技术人!]]"
  - "[[hope_wisdom 发出的红包]]"
published:
created: 2025-09-14
description: "文章浏览阅读1.4k次，点赞19次，收藏22次。一个kobject可以有一个父kobject和多个子kobject，通过parent指针可以将它们连接起来形成一个层次化的结构，类似于目录结构中，一个目录可以有一个父目录和多个子目录，通过目录的路径可以表示目录之间的层次关系。对于一些常见的硬件设备，如USB、i2c和平台设备，内核已经提供了相应的设备模型和相关驱动，开发人员可以基于这些模型来编写驱动，从而更快地实现特定设备的功能，并且可以借助内核的电源管理和热插拔事件管理功能。通过kset和kobject之间的关系，可以实现对内核对象的层次化管理和操作。_rk nvr源码 linux"
tags:
  - "clippings"
---


# 备注(声明)：


# 参考文章：




# 一、设备模型初入

## 什么是设备模型
### 1 、允许开发人员以更高级的方式来描述硬件设备和它们之间的关系


### 2 、提供一组通用API和机制来处理设备的注册，热插拔事件，电源管理等。(❤️)


### 3 、高级和模块化



### 4 、

## 设备模型的好处

### 5、统一的方式来描述硬件设备和它们之间的关系


### 6、代码复用：
> 设备模型**允许多个设备复用同一个驱动**。通过在设备树或总线上定义不同的设备节点，这些设备可以使用相同的驱动进行初始化和管理。这样可以减少代码的冗余，提高驱动的复用性和维护性。


### 7、资源的动态申请和释放：
> 设备模型**提供了一种机制来动态申请和释放设备所需的资源，如内存，中断等**。驱动可以使用这些机制来管理设备所需的资源，确保在设备初始化和关闭时进行正确的资源分配和释放。




### 8、简化驱动编写: 
> 设备模型提供了一组**通用API和机制，使得驱动编写更加简化和模块化**。开发人员可以使用这些API来注册设备，处理设备事件，进行设备的读写操作等，而无需重复实现这些通用功能。


### 热插拔机制：
> 设备模型**支持热插拔机制，能够在运行时动态添加或移除设备** 。当设备插入或拔出时，内核会生成相应的热插拔事件，驱动可以通过监听这些事件来执行相应的操作，如设备的初始化或释放。


###  驱动的面向对象思想：
> 设备模型的设计借鉴了面向对象编程（OOP）的思想。**每个设备都被看作是一个对象，具有自己的属性和方法**，并且可以通过设备模型的机制进行继承和扩展。这种设计使得驱动的编写更加模块化和可扩展，可以更好地应对不同类型的设备和功能需求。




### 总之，(❤️)
> 设备模型在内核驱动中扮演着关键的角色，通过提供统一的设备描述和管理机制，**简化了驱动的编写和维护过程，提高了代码的复用性和可维护性，并支持热插拔和动态资源管理等重要功能。**



# 二、kobject和kset基本概念


## 用于管理内核对象的基本概念


## kobject(内核对象)
### 1 、内核中抽象出来的通用对象模型


### 2 、表示内核中的各种实体


### 3 、包含了一些描述该对象的属性和方法(❤️)


### 4 、提供了一种统一的接口和机制，用于管理和操作内核对象


### 5、kobject结构体(❤️)
- 1 在内核源码kernel/include/linux/kobject.h文件中
```C
struct kobject {
	const char		*name;
	struct list_head	entry;
	struct kobject		*parent;
	struct kset		*kset;
	struct kobj_type	*ktype;
	struct kernfs_node	*sd; /* sysfs directory entry */
	struct kref		kref;
#ifdef CONFIG_DEBUG_KOBJECT_RELEASE
	struct delayed_work	release;
#endif
	unsigned int state_initialized:1;
	unsigned int state_in_sysfs:1;
	unsigned int state_add_uevent_sent:1;
	unsigned int state_remove_uevent_sent:1;
	unsigned int uevent_suppress:1;
 
	ANDROID_KABI_RESERVE(1);
	ANDROID_KABI_RESERVE(2);
	ANDROID_KABI_RESERVE(3);
	ANDROID_KABI_RESERVE(4);
};
```

#### 主要字段的解释：
```C
- const char *name：表示kobject的名称，通常用于在/sys目录下创建对应的目录。

- struct list_head entry：用于将kobject链接到父kobject的子对象列表中，以建立层次关系。

- struct kobject *parent：指向父kobject，表示kobject的层次关系。

- struct kset *kset：指向包含该kobject的kset，用于进一步组织和管理kobject。

- struct kobj_type *ktype：指向定义kobject类型的kobj_type结构体，描述kobject的属性和操作。

- struct kernfs_node *sd：指向sysfs目录中对应的kernfs_node，用于访问和操作sysfs目录项。

- struct kref kref：用于对kobject进行引用计数，确保在不再使用时能够正确释放资源。

- unsigned int 字段：表示一些状态标志和配置选项，例如是否已初始化、是否在sysfs中、是否发送了add/remove uevent等。
```

![[嵌入式知识学习（通用扩展）/linux驱动入门/第九期 设备模型/assets/第85章 设备模型基本框架- kobject和kset/file-20260309110606808.png]]
### 6、/sys/bus目录
![[嵌入式知识学习（通用扩展）/linux驱动入门/第九期 设备模型/assets/第85章 设备模型基本框架- kobject和kset/file-20260309112749822.png]]

- 2 和总线相关的目录，比如amba总线，CPU总线，platform 总线


### 7、kobject表示系统/sys下的一个目录


### 8、kobject的树状关系如下(❤️)
![[嵌入式知识学习（通用扩展）/linux驱动入门/第九期 设备模型/assets/第85章 设备模型基本框架- kobject和kset/file-20260309112857055.png]]

> **一个kobject可以有一个父kobject和多个子kobject**，通过parent指针可以将它们连接起来形成一个层次化的结构，类似于目录结构

## kset(内核对象集合 )
### 1 、组织和管理一组相关kobject的容器


### 2 、是kobject的一种扩展


### 3 、提供了一种层次化的组织结构，可以将一组相关的kobject组织在一起



### 4 、struct kset结构体(❤️)
- 1 定义在include/linux/kobject.h头文件中
```c
struct kset {
	struct list_head list;
	spinlock_t list_lock;
	struct kobject kobj;
	const struct kset_uevent_ops *uevent_ops;
	
	//与特定配置相关的保留字段
	ANDROID_KABI_RESERVE(1);
	ANDROID_KABI_RESERVE(2);
	ANDROID_KABI_RESERVE(3);
	ANDROID_KABI_RESERVE(4);
} __randomize_layout;
```


#### 主要字段的解释：
```c
- struct list_head list：用于将kset链接到全局kset链表中，以便对kset进行遍历和管理。
- spinlock_t list_lock：用于保护对kset链表的并发访问，确保线程安全性。

- struct kobject kobj：作为kset的kobject表示，用于在/sys目录下创建对应的目录，并与kset关联。

- const struct kset_uevent_ops *uevent_ops：指向kset的uevent操作的结构体，用于处理与kset相关的uevent事件。
```







### 5、kset通过包含一个kobject作为其成员，将kset本身表示为一个kobject


### 6、使用kobj来管理和操作kset


### 7、kset提供了一种层次化的组织结构，并与sysfs目录相对应，方便对kobject进行管理和操作。(❤️)


### 8、





##  kset和kobject的关系
### 1 、层次化的关系(❤️)
![[嵌入式知识学习（通用扩展）/linux驱动入门/第九期 设备模型/assets/第85章 设备模型基本框架- kobject和kset/file-20260309113648264.png]]

### 2 、kset可以被看作是kobject的一种特殊形式，它扩展了kobject并提供了一些额外的功能(❤️)


### 3 、每个kobject都属于一个kset



### 4 、kobject结构体中的`struct kset *kset`字段指向所属的kset。(❤️)



### 5、kset提供了对kobject的集合管理接口，可以通过kset来迭代、查找、添加或删除kobject。


### 6、





## 总结起来
### 1 、一个kset可以包含多个kobject(❤️)


### 2 、而一个kobject只能属于一个kset


### 3 、kset提供了对kobject的集合管理和操作接口，用于组织和管理具有相似特性或关系的kobject。(❤️)



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


