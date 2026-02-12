---
title: "Linux驱动开发笔记（三）平台设备驱动_linux 平台设备-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/139082852?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读1.5k次，点赞31次，收藏20次。随着科技的飞速发展，平台设备已成为现代计算机系统不可或缺的重要组成部分。无论是智能手机、平板电脑，还是嵌入式系统、数据中心服务器，平台设备都承载着系统运行的核心功能。因此，平台设备驱动的开发与优化，对于保障系统稳定性、提升性能以及满足用户日益增长的需求具有至关重要的作用。在接下来的章节中，我们将详细介绍该驱动的设计思路、实现原理、功能特性以及使用方法，希望能够为广大读者提供有价值的参考和借鉴。//定义一个resource结构体，用于存放上述的寄存器地址，提供给驱动使用。_linux 平台设备"
tags:
  - "clippings"
---
---

## 前言

  随着科技的飞速发展，平台设备已成为现代 计算机系统 不可或缺的重要 [组成部分](https://so.csdn.net/so/search?q=%E7%BB%84%E6%88%90%E9%83%A8%E5%88%86&spm=1001.2101.3001.7020) 。无论是智能手机、平板电脑，还是嵌入式系统、数据中心服务器，平台设备都承载着系统运行的核心功能。因此，平台设备驱动的开发与优化，对于保障系统稳定性、提升 性能 以及满足用户日益增长的需求具有至关重要的作用。  
  在接下来的章节中，我们将详细介绍该驱动的设计思路、实现原理、功能特性以及使用方法，希望能够为广大读者提供有价值的参考和借鉴。

---

## 一、Linux的设备模型

  在前面写的驱动中，我们发现编写驱动有个固定的模式只有往里面套代码就可以了，它们之间的大致流程可以总结如下：

- 实现入口函数xxx\_init()和卸载函数xxx\_exit()
- 申请设备号 register\_chrdev\_region()
- 初始化字符设备，cdev\_init函数、cdev\_add函数
- 硬件初始化，如时钟寄存器配置使能，GPIO设置为输入输出模式等。
- 构建file\_operation结构体内容，实现硬件各个相关的操作
- 在终端上使用mknod根据设备号来进行创建设备文件(节点)或者自动创建 (驱动使用class\_create创建设备类、在类的下面device\_create创建设备节点)  
	  Linux引入了设备驱动模型分层的概念， 将我们编写的驱动代码分成了两块：设备与驱动。设备负责提供硬件资源而驱动代码负责去使用这些设备提供的硬件资源。 并由总线将它们联系起来。这样子就构成以下图形中的关系。  
	![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/232570093245e2f5d99ea718f30c1b8c.png)  
	**设备(device)** ：挂载在某个总线的物理设备；  
	**驱动(driver)** ：与特定设备相关的软件，负责初始化该设备以及提供一些操作该设备的操作方式；  
	**总线(bus)** ：负责管理挂载对应总线的设备以及驱动；  
	**类(class)** ：对于具有相同功能的设备，归结到一种类别，进行分类管理；

### 1\. 总线

  总线是连接处理器和设备之间的桥梁，总线代表着同类设备需要共同遵守的工作时序，我们接触到的设备大部分是依靠总线来进行通信的。总线驱动则负责实现总线的各种行为，其管理着两个链表，分别是添加到该总线的设备链表以及注册到该总线的驱动链表。当你向总线添加(移除)一个设备(驱动)时，便会在对应的列表上添加新的节点， 同时对挂载在该总线的驱动以及设备进行匹配，在匹配过程中会忽略掉那些已经有驱动匹配的设备。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/01213df87e326dbd3363e3144d9301ee.png)

#### 1.1 bus\_type结构体

  在内核中使用结构体bus\_type来表示总线，

```c
struct bus_type {
    const char              *name;
    const struct attribute_group **bus_groups;
    const struct attribute_group **dev_groups;
    const struct attribute_group **drv_groups;

    int (*match)(struct device *dev, struct device_driver *drv);
    int (*uevent)(struct device *dev, struct kobj_uevent_env *env);
    int (*probe)(struct device *dev);
    int (*remove)(struct device *dev);

    int (*suspend)(struct device *dev, pm_message_t state);
    int (*resume)(struct device *dev);

    const struct dev_pm_ops *pm;

    struct subsys_private *p;

};
12345678910111213141516171819
```
- 参数
	- name:指定总线的名称，当新注册一种总线类型时，会在/sys/bus目录创建一个 新的目录，目录名就是该参数的值；
	- drv\_groups、dev\_groups、bus\_groups:分别表示驱动、设备以及总线的属性。这些属性可以是内部变量、字符串等等。通常会在对应的/sys目录下在以文件的形式存在，这些文件一般是可读写的，用户可以通过读写操作来获取和设置这些attribute的值。
	- match:当向总线注册一个新的设备或者是新的驱动时，会调用该回调函数。该回调函数主要负责判断是否有注册了的驱动适合新的设备，或者新的驱动能否驱动总线上已注册但没有驱动匹配的设备；
	- uevent:总线上的设备发生添加、移除或者其它动作时，就会调用该函数，来通知驱动做出相应的对策。
	- probe:当总线将设备以及驱动相匹配之后，执行该回调函数,最终会调用驱动提供的probe函数。
	- remove:当设备从总线移除时，调用该回调函数；
	- suspend、resume:电源管理的相关函数，当总线进入睡眠模式时，会调用suspend回调函数；而resume回调函数则是在唤醒总线的状态下执行；
	- pm:电源管理的结构体，存放了一系列跟总线电源管理有关的函数，与device\_driver结构体中的pm\_ops有关；
	- p:该结构体用于存放特定的私有数据，其成员klist\_devices和klist\_drivers记录了挂载在该总线的设备和驱动；

#### 1.2 注册/注销总线

  Linux内核已经为我们写好了大部分总线驱动，正常情况下我们一般不会去注册一个新的总线， 内核中提供了bus\_register 函数 来注册总线，以及bus\_unregister函数来注销总线，其函数原型如下：

```c
//注册总线API
int bus_register(struct bus_type *bus);
12
```
- 参数： bus: bus\_type类型的结构体指针
- 返回值
	- 成功： 0
	- 失败： 负数
```c
//注销总线API(内核源码/drivers/base/bus.c)
void bus_unregister(struct bus_type *bus);
12
```
- 参数： bus:bus\_type类型的结构体指针
- 返回值： 无

  当我们成功注册总线时，会在/sys/bus/目录下创建一个新目录，目录名为我们新注册的总线名。

### 2\. 设备

  我们编写驱动的目的，最终就是为了使设备可以正常工作。在Linux中，一切都是以文件的形式存在， 设备也不例外。

#### 2.1 device结构体

  在内核使用device结构体来描述我们的物理设备，其原型如下：

```c
struct device {
const char *init_name;
        struct device           *parent;
        struct bus_type *bus;
        struct device_driver *driver;
        void            *platform_data;
        void            *driver_data;
        struct device_node      *of_node;
        dev_t                   devt;
        struct class            *class;
void (*release)(struct device *dev);
        const struct attribute_group **groups;  /* optional groups */
struct device_private   *p;
........
};
123456789101112131415
```
- init\_name:指定该设备的名称，总线匹配时，一般会根据比较名字，来进行配对；
- parent:表示该设备的父对象，前面提到过，旧版本的设备之间没有任何关联，引入Linux设备模型之后，设备之间呈树状结构，便于管理各种设备；
- bus:表示该设备依赖于哪个总线，当我们注册设备时，内核便会将该设备注册到对应的总线。
- of\_node:存放设备树中匹配的设备节点。当内核使能设备树，总线负责将驱动的of\_match\_table以及设备树的compatible属性进行比较之后，将匹配的节点保存到该变量。
- platform\_data:一个指针，用于保存具体的平台相关的数据。具体的driver模块，可以将一些私有的数据，暂存在这里，需要使用的时候，再拿出来，因此设备模型并不关心该指针得实际含义。
- driver\_data:同上，驱动层可通过dev\_set/get\_drvdata函数来获取该成员；
- class:指向了该设备对应类，开篇我们提到的触摸，鼠标以及键盘等设备，对于计算机而言，他们都具有相同的功能，都归属于输入设备。我们可以在/sys/class目录下对应的类找到该设备，如input、leds、pwm等目录;
- dev:dev\_t类型变量，字符设备章节提及过，它是用于标识设备的设备号，该变量主要用于向/sys目录中导出对应的设备。
- release:回调函数，当设备被注销时，会调用该函数。如果我们没定义该函数时，移除设备时，会提示“Device ‘xxxx’ does not have a release() function, it is broken and must be fixed”的错误。
- group:指向struct attribute\_group类型的指针，指定该设备的属性；
- \*\*p \*\*:是私有数据结构指针，该指针中会保存子设备链表、用于添加到bus/driver/prent等设备中的链表头等等。

#### 2.2 内核注册/注销设备

  内核也提供相关的API来注册和注销设备，如下所示：

```c
内核注册设备
int device_register(struct device *dev);
12
```
- 参数： dev:struct device结构体类型指针
- 返回值：  
	\- 成功： 0  
	\- 失败： 负数
```c
内核注销设备
void device_unregister(struct device *dev);
12
```
- 参数： dev:struct device结构体类型指针
- 返回值： 无

  当成功注册总线时，会在/sys/bus目录下创建对应总线的目录，该目录下有两个子目录，分别是drivers和devices， 我们使用device\_register注册的设备从属于某个总线时，该总线的devices目录下便会存在该设备文件。

### 3\. 驱动

  设备能否正常工作，取决于驱动。驱动需要告诉内核， 自己可以驱动哪些设备，如何初始化设备。

#### 3.1 device\_driver结构体

  在内核中，使用device\_driver结构体来描述我们的驱动，如下所示：

```c
struct device_driver {
        const char              *name;
        struct bus_type         *bus;
        struct module           *owner;
        const char              *mod_name;      /* used for built-in modules */
        bool suppress_bind_attrs;       /* disables bind/unbind via sysfs */
        const struct of_device_id       *of_match_table;
        const struct acpi_device_id     *acpi_match_table;
        int (*probe) (struct device *dev);
        int (*remove) (struct device *dev);
        const struct attribute_group **groups;
        struct driver_private *p;
};
12345678910111213
```
- 参数
	- name:指定驱动名称，总线进行匹配时，利用该成员与设备名进行比较；
	- bus:表示该驱动依赖于哪个总线，内核需要保证在驱动执行之前，对应的总线能够正常工作；
	- suppress\_bind\_attrs:布尔量，用于指定是否通过sysfs导出bind与unbind文件，bind与unbind文件是驱动用于绑定/解绑关联的设备。
	- owner:表示该驱动的拥有者，一般设置为THIS\_MODULE；
	- of\_match\_table:指定该驱动支持的设备类型。当内核使能设备树时，会利用该成员与设备树中的compatible属性进行比较。
	- remove:当设备从操作系统中拔出或者是系统重启时，会调用该回调函数；
	- probe:当驱动以及设备匹配后，会执行该回调函数，对设备进行初始化。通常的代码，都是以main函数开始执行的，但是在内核的驱动代码，都是从probe函数开始的。
	- group:指向struct attribute\_group类型的指针，指定该驱动的属性；

#### 3.2 注册/注销驱动

```c
//注册 驱动
int driver_register(struct device_driver *drv);
12
```
- 参数： drv:struct device\_driver结构体类型指针
- 返回值：
	- 成功： 0
	- 失败： 负数
```c
//注销驱动
void driver_unregister(struct device_driver *drv);
12
```
- 参数： drv:struct device\_drive结构体类型指针
- 返回值： 无  
	![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/28cb288b768a11cd6fc289a17a7227a6.png#pic_center)

### 4\. attribute属性文件

  /sys目录有各种子目录以及文件，前面讲过当我们注册新的总线、设备或驱动时，内核会在对应的地方创建一个新的目录，目录名为各自结构体的name成员， 每个子目录下的文件，都是内核导出到用户空间，用于控制我们的设备的。内核中以attribute结构体来描述/sys目录下的文件，如下所示：

```c
struct attribute {
    const char              *name;
    umode_t                 mode;
};
1234
```
- 参数
	- name:指定文件的文件名；
	- mode:指定文件的权限，

#### 4.1 attribute\_group结构体

  bus\_type、device、device\_driver结构体中都包含了一种数据类型struct attribute\_group，如下所示，它是多个attribute文件的集合， 利用它进行初始化，可以避免一个个注册attribute。

```c
struct attribute_group {
    const char              *name;
    umode_t                 (*is_visible)(struct kobject *,
                        struct attribute *, int);
    struct attribute        **attrs;
    struct bin_attribute    **bin_attrs;
};
1234567
```

#### 4.2 设备属性文件

  在开发单片机的时候，如果想要读取某个寄存器的值，你可能需要加入一些新的代码，并重新编译。但对于Linux内核来讲，每次都需要编译一遍源码， 实在太浪费时间和精力了。为此，Linux提供以下接口，来注册和注销一个设备属性文件。我们可以通过这些接口直接在用户层进行查询/修改，避免了重新编译内核的麻烦。

```c
//设备属性文件接口
struct device_attribute {
    struct attribute        attr;
    ssize_t (*show)(struct device *dev, struct device_attribute *attr,
            char *buf);
    ssize_t (*store)(struct device *dev, struct device_attribute *attr,
            const char *buf, size_t count);
};

#define DEVICE_ATTR(_name, _mode, _show, _store) \
        struct device_attribute dev_attr_##_name = __ATTR(_name, _mode, _show, _store)
extern int device_create_file(struct device *device,
                const struct device_attribute *entry);
extern void device_remove_file(struct device *dev,
                const struct device_attribute *attr);
123456789101112131415
```
- DEVICE\_ATTR宏：定义用于定义一个device\_attribute类型的变量，## 表示将 ## 左右两边的标签拼接在一起，因此， 我们得到变量的名称应该是带有dev\_attr\_前缀的。该宏定义需要传入四个参数\_name，\_mode，\_show，\_store，分别代表了文件名， 文件权限，show回调函数，store回调函数。show回调函数以及store回调函数分别对应着用户层的cat和echo命令， 当我们使用cat命令，来获取/sys目录下某个文件时，最终会执行show回调函数；使用echo命令，则会执行store回调函数。 参数\_mode的值，可以使用S\_IRUSR、S\_IWUSR、S\_IXUSR等宏定义，更多选项可以查看读写文件章节关于文件权限的内容。
- device\_create\_file：用于创建文件，它有两个参数成员，第一个参数表示的是设备，前面讲解device结构体时，其成员中有个bus\_type变量， 用于指定设备挂载在某个总线上，并且会在总线的devices子目录创建一个属于该设备的目录，device参数可以理解为在哪个设备目录下，创建设备文件。 第二个参数则是我们自己定义的device\_attribute类型变量。
- device\_remove\_file：用于删除文件，当我们的驱动注销时，对应目录以及文件都需要被移除。 其参数和device\_create\_file函数的参数是一样。

#### 4.3 驱动属性文件

 &Emsp;驱动属性文件，和设备属性文件的作用是一样，唯一的区别在于函数参数的不同，函数接口如下：

```c
//驱动属性文件接口
struct driver_attribute {
    struct attribute attr;
    ssize_t (*show)(struct device_driver *driver, char *buf);
    ssize_t (*store)(struct device_driver *driver, const char *buf,
            size_t count);
};

#define DRIVER_ATTR_RW(_name) \
    struct driver_attribute driver_attr_##_name = __ATTR_RW(_name)
#define DRIVER_ATTR_RO(_name) \
    struct driver_attribute driver_attr_##_name = __ATTR_RO(_name)
#define DRIVER_ATTR_WO(_name) \
    struct driver_attribute driver_attr_##_name = __ATTR_WO(_name)

extern int __must_check driver_create_file(struct device_driver *driver,
                                    const struct driver_attribute *attr);
extern void driver_remove_file(struct device_driver *driver,
                const struct driver_attribute *attr);
12345678910111213141516171819
```
- DRIVER\_ATTR\_RW、DRIVER\_ATTR\_RO 以及 DRIVER\_ATTR\_WO 宏定义用于定义一个driver\_attribute类型的变量，带有driver\_attr\_的前缀，区别在于文件权限不同， RW后缀表示文件可读写，RO后缀表示文件仅可读，WO后缀表示文件仅可写。而且你会发现， DRIVER\_ATTR类型的宏定义没有参数来设置show和store回调函数， 那如何设置这两个参数呢？在写驱动代码时，只需要你提供xxx\_store以及xxx\_show这两个函数， 并确保两个函数的xxx和DRIVER\_ATTR类型的宏定义中名字是一致的即可。  
	driver\_create\_file 和 driver\_remove\_file 函数用于创建和移除文件，使用driver\_create\_file函数， 会在/sys/bus//drivers//目录下创建文件。

#### 4.4 总线属性文件

  同样的，Linux也为总线通过了相应的函数接口，如下所示：

```c
struct bus_attribute {
    struct attribute        attr;
    ssize_t (*show)(struct bus_type *bus, char *buf);
    ssize_t (*store)(struct bus_type *bus, const char *buf, size_t count);
};
//用于定义一个bus_attribute变量
#define BUS_ATTR(_name, _mode, _show, _store)       \
        struct bus_attribute bus_attr_##_name = __ATTR(_name, _mode, _show, _store)
//在/sys/bus/<bus-name>下创建对应的文件
extern int __must_check bus_create_file(struct bus_type *,
                    struct bus_attribute *);
//用于移除该文件
extern void bus_remove_file(struct bus_type *, struct bus_attribute *);
12345678910111213
```

## 二、平台设备

### 1\. 平台设备的引入

  平台设备驱动作为连接硬件设备与操作系统之间的桥梁，负责实现硬件设备的抽象化，使得操作系统能够通过统一的接口与各种硬件设备进行交互。在驱动开发过程中，我们需要深入理解硬件设备的工作原理、通信协议以及操作系统的内核机制，确保驱动程序的正确性、高效性和稳定性。  
  在之前的字符设备程序中驱动程序，我们只要调用open()函数打开了相应的设备文件，就可以使用read()/write()函数， 通过file\_operations这个文件操作接口来进行硬件的控制。这种驱动开发方式简单直观，但是从 软件 设计的角度看，却是一种十分糟糕的方式。驱动中总线的概念是软件层面的一种抽象，与我们SOC中物理总线的概念并不严格相等：  
  物理总线：芯片与各个功能外设之间传送信息的公共通信干线，其中又包括数据总线、地址总线和控制总线，以此来传输各种通信时序。  
  驱动总线：负责管理设备和驱动。制定设备和驱动的匹配规则，一旦总线上注册了新的设备或者是新的驱动，总线将尝试为它们进行配对。  
  一般对于I2C、SPI、USB这些常见类型的物理总线来说，Linux内核会自动创建与之相应的驱动总线，因此I2C设备、SPI设备、 USB设备自然是注册挂载在相应的总线上。但是，实际项目开发中还有很多结构简单的设备，对它们进行控制并不需要特殊的时序， 它们也就没有相应的物理总线，比如led等，Linux内核将不会为它们创建相应的驱动总线。 为了使这部分设备的驱动开发也能够遵循设备驱动 模型 ，Linux内核引入了一种 **虚拟的总线** ——平台总线(platform bus)。

### 2\. 平台设备的工作原理

  平台设备的一大特点就是将一个驱动程序分化成两部分，及描述硬件设备的device.c和控制驱动的driver.c。之后平台总线通过字符匹配将name相同的部分在绑定到一起控制设备。简单概况下来就是 **先分离，再搭档** 。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f5ac317494f8e4d5621c9c266deda404.png#pic_center)

### 3\. 相关结构体

  platform\_device 是 Linux 内核中用于表示平台设备的结构体，通常在 嵌入式系统 或平台相关的设备驱动中使用。这个结构体用于描述一个平台相关的设备，如 CPU、内存控制器、总线等。

#### 3.1 platform\_device结构体

```c
struct platform_device {
     const char *name;
     int id;
     struct device dev;
     u32 num_resources;
     struct resource *resource;
     const struct platform_device_id *id_entry;
     /* 省略部分成员 */
 };
123456789
```
- name：设备的名称，用于在内核中标识该设备。
- id：设备的ID，对于可以存在多个实例的设备，此ID用于区分不同的实例。
- dev：设备的通用部分，包含设备的引用计数、设备树信息、父设备等信息。这里必须要实习device结构体的release函数，否则会报错。
- resource：指向资源列表的指针，资源列表包含设备的 I/O 内存地址、中断号等信息。
- platform\_data：指向特定于平台的数据的指针，这些数据通常用于设备驱动与设备硬件之间的交互。

#### 3.2 resource结构体

  对于硬件信息，使用结构体struct resource来保存设备所提供的资源，比如设备使用的中断编号，寄存器物理地址等，结构体原型如下：

```c
struct resource {
    resource_size_t start;
    resource_size_t end;
    const char *name;
    u32 num_resources;
    unsigned long flags;
    /* 省略部分成员 */
};
12345678
```
- start：资源的起始地址或编号。对于内存资源，这通常是内存的物理地址或虚拟地址的起始点；对于I/O端口或中断，这可以是端口号或中断号。
- end：资源的结束地址或编号。这定义了资源范围的结束点。
- name：资源的名称。这通常是一个描述性字符串，用于在调试或日志中标识资源。
- num\_resources：设备资源个数，定义几个就设置为几个。
- flags：资源的标志位。这些标志位用于描述资源的类型和特性。例如，一个标志位可能表示资源是一个I/O端口，而另一个标志位可能表示资源是可共享的。  
	![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/6d1a77b5eca7d60eaf80f5dd84d9188a.png#pic_center)

#### 3.3 platform\_device结构体

  对于软件信息，这种特殊信息需要我们以私有数据的形式进行封装保存，我们注意到platform\_device结构体中， 有个device结构体类型的成员dev。在前面章节，我们提到过Linux设备模型使用device结构体来抽象物理设备， 该结构体的成员platform\_data可用于保存设备的私有数据。platform\_data是void \*类型的万能指针， 无论你想要提供的是什么内容，只需要把数据的地址赋值给platform\_data即可， 还是以GPIO引脚号为例，示例代码如下：

```c
unsigned int pin = 10;

struct platform_device pdev = {
    .dev = {
        .platform_data = &pin;
    }
}
1234567
```

#### 3.4 platform\_driver结构体

  内核中使用platform\_driver结构体来描述平台驱动，结构体原型如下所示：

```c
struct platform_driver {

    int (*probe)(struct platform_device *);
    int (*remove)(struct platform_device *);
    struct device_driver driver;
    const struct platform_device_id *id_table;
    .......
};
12345678
```
- probe： 函数指针，驱动开发人员需要在驱动程序中初始化该函数指针，当总线为设备和驱动匹配上之后，会回调执行该函数。我们一般通过该函数，对设备进行一系列的初始化。
- remove： 函数指针，驱动开发人员需要在驱动程序中初始化该函数指针，当我们移除某个平台设备时，会回调执行该函数指针，该函数实现的操作，通常是probe函数实现操作的逆过程。
- driver： Linux设备模型中用于抽象驱动的device\_driver结构体，platform\_driver继承该结构体，也就获取了设备模型驱动对象的特性；
- id\_table： 表示该驱动能够兼容的设备类型。

#### 3.5 platform\_device\_id结构体

  我们可以注意到上面所提到的platform\_driver结构体中含有一个platform\_device\_id结构体，它主要被用于保存设备配置的。

```c
struct platform_device_id {
    char name[PLATFORM_NAME_SIZE];
    kernel_ulong_t driver_data;

};
12345
```
- name：用于指定驱动的名称，总线进行匹配时，会依据该结构体的name成员与platform\_device中的变量name进行比较匹配
- driver\_data，则是用于来保存设备的配置。

#### 3.6 platform\_bus\_type结构体

  每当有新的设备或者是新的驱动加入到总线时， 总线便会调用platform\_match函数对新增的设备或驱动，进行配对。内核中使用bus\_type来抽象描述系统中的总线，平台总线结构体原型如下所示：

```c
struct bus_type platform_bus_type = {

    .name           = "platform",
    .dev_groups     = platform_dev_groups,
    .match          = platform_match,
    .uevent         = platform_uevent,
    .pm             = &platform_dev_pm_ops,

};

EXPORT_SYMBOL_GPL(platform_bus_type);
1234567891011
```
- name:这指定了总线类型的名称为
- dev\_groups:这是一个指向 platform\_dev\_groups 的指针，它可能是一个包含多个属性组的数组。
- match:这是一个回调函数指针，指向 platform\_match 函数。这个函数用于确定一个特定的驱动程序是否可以绑定到给定的设备。它通常会比较设备的 ID（如果存在）与驱动程序支持的 ID 列表。
- uevent:这是一个回调函数指针，指向 platform\_uevent 函数。当设备发生某些事件（如添加、删除或更改）时，这个函数会被调用。
- pm:这是一个指向电源管理操作集的指针,包含了一组用于处理设备电源管理（如挂起、恢复等）的函数指针。

#### 小结

  看到这想必你也已经头晕了，这里简单捋一捋各个结构体之间的关系。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a0cf2161e003c7f5b9eb16705ad09a9d.png#pic_center)  
  首先是橙色部分，platform\_device结构体是继承自device结构体，用于关联硬件设备。  
  其次是绿色部分，platform\_driver结构体是继承自driver结构体，用于重新构建probe函数，当与platform\_device匹配后则执行新的probe函数。  
  platform\_bus\_type中的match( )函数用于将上述二者进行匹配，值得注意的是对于platform总线来说不需要向Linux内核收到注册，当进入驱动后会自动进行platform\_bus\_init( )函数

## 三、设计思路

### 1\. 注册/注销平台驱动

  当我们初始化了platform\_driver之后，通过platform\_driver\_register()函数来注册我们的平台驱动，该函数原型如下：

```c
//放置于module_INIT
int platform_driver_register(struct platform_driver *drv);
12
```
- 参数： drv: platform\_driver类型结构体指针
- 返回值  
	\- 成功： 0  
	\- 失败： 负数

  当卸载的驱动模块时，需要注销掉已注册的平台驱动，platform\_driver\_unregister()函数用于注销已注册的平台驱动，该函数原型如下：

```c
//放置于module_EXTI
void platform_driver_unregister(struct platform_driver *drv);
12
```
- 参数： drv: platform\_driver类型结构体指针
- 返回值： 无  
	  上面所讲的内容是最基本的平台驱动框架，只需要实现probe函数、remove函数，初始化platform\_driver结构体，并调用platform\_driver\_register进行注册即可。

### 2\. 平台驱动获取设备信息

  platform\_get\_resource()函数通常会在驱动的probe函数中执行，用于获取平台设备提供的资源结构体，最终会返回一个struct resource类型的指针，该函数原型如下：

```c
struct resource *platform_get_resource(struct platform_device *dev, unsigned int type, unsigned int num);
1
```
- 参数
	- dev： 指定要获取哪个平台设备的资源；
	- type： 指定获取资源的类型，如IORESOURCE\_MEM、IORESOURCE\_IO等；
	- num： 指定要获取的资源编号。每个设备所需要资源的个数是不一定的，为此内核对这些资源进行了编号，对于不同的资源，编号之间是相互独立的。  
		**注：这里的num指的是同类型中的第几个，而不是总设备数的第几个，例如只有一个I/O和一个中断类型，他们俩在调用的时候均是自己类别的第一个。**
- 返回值  
	\- 成功： struct resource结构体类型指针
	- 失败： NULL

  假若资源类型为IORESOURCE\_IRQ，平台设备驱动还提供platform\_get\_irq函数接口，来获取中断引脚。

```c
int platform_get_irq(struct platform_device *pdev, unsigned int num);
1
```
- 参数
	- pdev： 指定要获取哪个平台设备的资源；
	- num： 指定要获取的资源编号。
- 返回值：
	- 成功： 可用的中断号
	- 失败： 负数

  对于存放在device结构体中成员platform\_data的软件信息，我们可以使用dev\_get\_platdata函数来获取，函数原型如下所示：

```c
static inline void *dev_get_platdata(const struct device *dev)
{
    return dev->platform_data;
}
1234
```
- 参数：dev： struct device结构体类型指针
- 返回值： device结构体中成员platform\_data指针

  以上几个函数接口就是如何从平台设备中获取资源的常用的几个函数接口，到这里平台驱动部分差不多就结束了。总结一下平台驱动需要 实现probe函数，当平台总线成功匹配驱动和设备时，则会调用驱动的probe函数，在该函数中使用上述的函数接口来获取资源， 以初始化设备，最后填充结构体platform\_driver，调用platform\_driver\_register进行注册。

### 3\. 平台总线注册和匹配方式

  内核用platform\_bus\_type来描述平台总线，该总线在linux内核启动的时候自动进行注册。

```c
int __init platform_bus_init(void)
{
    int error;
    ...
    error =  bus_register(&platform_bus_type);
    ...
    return error;
}
12345678
```

  这里重点是platform总线的match函数指针，该函数指针指向的函数将负责实现平台总线和平台设备的匹配过程。对于每个驱动总线， 它都必须实例化该函数指针。platform总线提供了四种匹配方式，并且这四种方式存在着优先级：设备树机制>ACPI匹配模式>id\_table方式>字符串比较。platform\_match的函数原型如下：

```c
static int platform_match(struct device *dev, struct device_driver *drv)
{
    //对container_of的封装
    struct platform_device *pdev = to_platform_device(dev);
    struct platform_driver *pdrv = to_platform_driver(drv);

    /* When driver_override is set, only bind to the matching driver */
    if (pdev->driver_override)
        return !strcmp(pdev->driver_override, drv->name);

    /* Attempt an OF style match first */
    if (of_driver_match_device(dev, drv))
        return 1;

    /* Then try ACPI style match */
    if (acpi_driver_match_device(dev, drv))
        return 1;

    /* Then try to match against the id table */
    if (pdrv->id_table)
        return platform_match_id(pdrv->id_table, pdev) != NULL;

    /* fall-back to driver name match */
    return (strcmp(pdev->name, drv->name) == 0);
}
12345678910111213141516171819202122232425
```

  平台总线id\_table匹配方式，在定义结构体platform\_driver时，我们需要提供一个id\_table的数组，该数组说明了当前的驱动能够支持的设备。当加载该驱动时，总线的match函数发现id\_table非空， 则会比较id\_table中的name成员和平台设备的name成员，若相同，则会返回匹配的条目，具体的实现过程如下：

```c
static const struct platform_device_id *platform_match_id(
            const struct platform_device_id *id,
            struct platform_device *pdev)
{
    while (id->name[0]) {
        if (strcmp(pdev->name, id->name) == 0) {
            pdev->id_entry = id;
            return id;
        }
        id++;
    }
    return NULL;
}
12345678910111213
```
- 参数
	- \*id: 要匹配的id\_table
	- \*pdev: 待匹配的平台设备
- 返回值
	- 成功：platform\_device中的id\_entry
	- 失败：空指针

  其示意图如下所示： ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7b1ac03b2ec1962ec46b458cd1c5c97e.png#pic_center)

## 四、实验代码

### 1\. 编程思路

1）编写第一个内核模块led\_pdev.c  
2）在内核模块中定义一个平台设备，并填充LED灯相关设备信息  
3）在该模块入口函数，注册/挂载这个平台设备  
4）编写第二个内核模块led\_pdrv.c  
5）在内核模块中定义一个平台驱动，在probe函数中完成字符设备驱动的创建  
6）在该模块入口函数，注册/挂载这个平台驱动

### 2\. 定义platform\_device类型的变量

```c
//定义一个resource结构体，用于存放上述的寄存器地址，提供给驱动使用
static struct resource rled_resource[] = {
    [0] = DEFINE_RES_MEM(GPIO1_DR, 4),
    [1] = DEFINE_RES_MEM(GPIO1_DDR, 4)
};

//使用一个数组led_hwinfo，来记录寄存器的偏移量
unsigned int led_hwinfo[1] = { 8 };

//声明了led_cdev_release函数，目的为了防止卸载模块，内核提示报错
static int led_cdev_release(struct inode *inode, struct file *filp)
{
    return 0;
}

//定义了一个设备名为“led_pdev”的设备
static struct platform_device rled_pdev = {
    .name = "led_pdev",
    .id = 0,
    //用于计算数组长度
    .num_resources = ARRAY_SIZE(led_resource),
    //将上面实现好的rled_resource数组赋值给resource成员
    .resource = led_resource,
    //对dev中的成员进行赋值，将rled_hwinfo存储到platform_data中
    .dev = {
        .release = led_release,
        .platform_data = led_hwinfo,
        },
};
1234567891011121314151617181920212223242526272829
```

### 3\. 模块初始化

```c
//入口函数，打印信息并注册平台设备
static __init int led_pdev_init(void)
{
    printk("pdev init\n");
    platform_device_register(&rled_pdev);
    return 0;

}
module_init(led_pdev_init);

//实现模块的出口函数，打印信息并注销设备
static __exit void led_pdev_exit(void)
{
    printk("pdev exit\n");
    platform_device_unregister(&rled_pdev);

}
module_exit(led_pdev_exit);

MODULE_AUTHOR("Embedfire");
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("the example for platform driver");
12345678910111213141516171819202122
```

### 4\. 定义平台驱动

```c
static struct platform_device_id led_pdev_ids[] = {
    {.name = "led_pdev"},
    {}
};
//这个宏让驱动程序公开其ID表，该表描述它可以支持哪些设备，用于匹配设备
MODULE_DEVICE_TABLE(platform, led_pdev_ids);
123456
```

### 5\. probe( )函数指针

```c
//使用结构体led_data来管理我们LED灯的硬件信息，定义时钟寄存器的虚拟地址变量
struct led_data {
    unsigned int led_pin;
    unsigned int __iomem *va_MODER;
    unsigned int __iomem *va_OTYPER;

    struct cdev led_cdev;
};

static int led_pdrv_probe(struct platform_device *pdev)
{
    struct led_data *cur_led;
    unsigned int *led_hwinfo;
    struct resource *mem_DR;
    struct resource *mem_DDR;
    int ret = 0;

    printk("led platform driver probe\n");

    cur_led = devm_kzalloc(&pdev->dev, sizeof(struct led_data), GFP_KERNEL);
    if (!cur_led)
        return -ENOMEM;
    led_hwinfo = devm_kzalloc(&pdev->dev, sizeof(unsigned int), GFP_KERNEL);
    if (!led_hwinfo)
        return -ENOMEM;

    led_hwinfo = dev_get_platdata(&pdev->dev);
    if (!led_hwinfo) {
        dev_err(&pdev->dev, "Failed to get platform data\n");
        return -EINVAL;
    }

    cur_led->led_pin = led_hwinfo[0];

    mem_DR = platform_get_resource(pdev, IORESOURCE_MEM, 0);
    mem_DDR = platform_get_resource(pdev, IORESOURCE_MEM, 1);
    if (!mem_DR || !mem_DDR) {
        dev_err(&pdev->dev, "Failed to get platform resources\n");
        return -ENODEV;
    }

    cur_led->va_DR = devm_ioremap(&pdev->dev, mem_DR->start, resource_size(mem_DR));
    cur_led->va_DDR = devm_ioremap(&pdev->dev, mem_DDR->start, resource_size(mem_DDR));
    if (!cur_led->va_DR || !cur_led->va_DDR) {
        dev_err(&pdev->dev, "Failed to map platform resources\n");
        return -ENOMEM;
    }

    ret = alloc_chrdev_region(&cur_led->dev_num, 0, 1, "led_cdev");
    if (ret < 0) {
        dev_err(&pdev->dev, "Failed to allocate char device region\n");
        return ret;
    }

    cdev_init(&cur_led->led_cdev, &led_cdev_fops);
    ret = cdev_add(&cur_led->led_cdev, cur_led->dev_num, 1);
    if (ret < 0) {
        dev_err(&pdev->dev, "Failed to add char device\n");
        goto add_err;
    }

    device_create(led_test_class, NULL, cur_led->dev_num, NULL, DEV_NAME "%d", pdev->id);

    platform_set_drvdata(pdev, cur_led);

    return 0;

add_err:
    unregister_chrdev_region(cur_led->dev_num, 1);
    return ret;
}
1234567891011121314151617181920212223242526272829303132333435363738394041424344454647484950515253545556575859606162636465666768697071
```

### 6\. 驱动注销

  当驱动的内核模块被卸载时，我们需要将注册的驱动注销，相应的字符设备也同样需要注销，具体的实现代码如下：

```c
static int led_pdrv_remove(struct platform_device *pdev)
{
    dev_t cur_dev;
    //platform_get_drvdata，获取当前LED灯对应的结构体
    struct led_data *cur_data = platform_get_drvdata(pdev);

    printk("led platform driver remove\n");

    cur_dev = MKDEV(DEV_MAJOR, pdev->id);

    //cdev_del删除对应的字符设备
    cdev_del(&cur_data->led_cdev);

    //删除/dev目录下的设备
    device_destroy(led_test_class, cur_dev);

    //unregister_chrdev_region， 注销掉当前的字符设备编号
    unregister_chrdev_region(cur_dev, 1);

    return 0;
}
123456789101112131415161718192021
```

### 7\. open\_operations接口函数

  这里我们使用到kstrtoul\_from\_user( )函数，该函数相比kstrtoul()多了一个参数count，因为用户空间是不可以直接访问内核空间的，所以内核提供了kstrtoul\_from\_user()函数以实现用户缓冲区到内核缓冲区的拷贝，与之相似的还有copy\_to\_user()，copy\_to\_user() 完成的是内核空间缓冲区到用户空io间的拷贝。如果你使用的内存类型没那么复杂，便可以选择使用put\_user()或者get\_user()函数。其原型如下：

```c
int __must_check kstrtoul_from_user(const char __user *s, size_t count, unsigned int base, unsigned long *res);
1
```
- 参数
	- s： 字符串的起始地址，该字符串必须以空字符结尾；
	- count： count为要转换数据的大小；
	- base： 转换基数，如果base=0，则函数会自动判断字符串的类型，且按十进制输出，比如“0xa”就会被当做十进制处理(大小写都一样)，输出为10。如果是以0开头则会被解析为八进制数，否则将会被解析成小数；
	- res： 一个指向被转换成功后的结果的地址。
- 返回值：
```c
static int led_cdev_open(struct inode *inode, struct file *filp)
{
    unsigned int val = 0;
    struct led_data *cur_led = container_of(inode->i_cdev, struct led_data, led_cdev);

    printk("led_cdev_open() \n");

    // 设置引脚输出
    val = readl(cur_led->va_DDR);
    val |= ((unsigned int)0X1 << (cur_led->led_pin+16));
    val |= ((unsigned int)0X1 << (cur_led->led_pin));
    writel(val,cur_led->va_DDR);

    //设置默认输出高电平
    val = readl(cur_led->va_DR);
    val |= ((unsigned int)0X1 << (cur_led->led_pin+16));
    val |= ((unsigned int)0x1 << (cur_led->led_pin));
    writel(val, cur_led->va_DR);

    filp->private_data = cur_led;

    return 0;
}

static int led_cdev_release(struct inode *inode, struct file *filp)
{
    return 0;
}

static ssize_t led_cdev_write(struct file *filp, const char __user * buf,
                size_t count, loff_t * ppos)
{
    unsigned long val = 0;
    unsigned long ret = 0;

    int tmp = count;

    struct led_data *cur_led = (struct led_data *)filp->private_data;

    val = kstrtoul_from_user(buf, tmp, 10, &ret);

    val = readl(cur_led->va_DR);
    if (ret == 0)
    {
        val |= ((unsigned int)0x1 << ((cur_led->led_pin)+16));
        val &= ~((unsigned int)0X1 << (cur_led->led_pin));
    }
    else
    {
        val |= ((unsigned int)0x1 << (cur_led->led_pin+16));
        val |= ((unsigned int)0X1 << (cur_led->led_pin));
    }
    writel(val, cur_led->va_DR);

    *ppos += tmp;

    return tmp;
}

static struct file_operations led_cdev_fops = {
    .open = led_cdev_open,
    .release = led_cdev_release,
    .write = led_cdev_write,

};
1234567891011121314151617181920212223242526272829303132333435363738394041424344454647484950515253545556575859606162636465
```

### 8\. 注册平台驱动

```c
//根据id_table中的name值进行匹配
static struct platform_driver led_pdrv = {
    .probe = led_pdrv_probe,
    .remove = led_pdrv_remove,
    .driver.name = "led_pdev",
    .id_table = led_pdev_ids,
};

static __init int led_pdrv_init(void)
{
    printk("led platform driver init\n");
    //调用函数class_create，来创建一个led类，并注册平台驱动结构
    led_test_class = class_create(THIS_MODULE, "test_leds");
    platform_driver_register(&led_pdrv);

    return 0;
}
module_init(led_pdrv_init);

//注销函数led_pdrv_exit
static __exit void led_pdrv_exit(void)
{
    printk("led platform driver exit\n");
    platform_driver_unregister(&led_pdrv);
    class_destroy(led_test_class);
}
module_exit(led_pdrv_exit);

12345678910111213141516171819202122232425262728
```

  实验结果同上章字符设备I/O驱动，这里不在展示，需要源码可以私信作者。  
**免责声明：本文参考了野火和讯为的部分资料，仅供学习参考使用，若有侵权或勘误请联系笔者。**

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/139082852

作者主页：https://blog.csdn.net/sincerelover

实付 元

[使用余额支付](https://blog.csdn.net/sincerelover/article/details/)

点击重新获取

扫码支付

钱包余额 0

抵扣说明：

1.余额是钱包充值的虚拟货币，按照1:1的比例进行支付金额的抵扣。  
2.余额无法直接购买下载，可以购买VIP、付费专栏及课程。

[余额充值](https://i.csdn.net/#/wallet/balance/recharge)

举报

 [![](https://csdnimg.cn/release/blogv2/dist/pc/img/toolbar/Group-dark.png) 点击体验  
DeepSeekR1满血版](https://ai.csdn.net/?utm_source=cknow_pc_blogdetail&spm=1001.2101.3001.10583) 隐藏侧栏

![程序员都在用的中文IT技术交流社区](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_app.png)

程序员都在用的中文IT技术交流社区

程序员都在用的中文IT技术交流社区

![专业的中文 IT 技术社区，与千万技术人共成长](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_wechat.png)

专业的中文 IT 技术社区，与千万技术人共成长

专业的中文 IT 技术社区，与千万技术人共成长

![关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_video.png)

关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！

关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！

客服 返回顶部

![](https://i-blog.csdnimg.cn/blog_migrate/232570093245e2f5d99ea718f30c1b8c.png)