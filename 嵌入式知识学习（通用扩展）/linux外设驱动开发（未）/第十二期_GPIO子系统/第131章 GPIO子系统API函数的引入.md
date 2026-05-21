---
title: "{{title}}"
aliases: 
tags: 
description: 
source:
---

# 备注(声明)：

> 新版本GPIO子系统接口是**基于描述符（descriptor-based）来实现**的
> 使用了**以 "gpiod_"作为前缀**的函数命名约定

# 参考文章：

```cardlink
url: https://blog.csdn.net/beijingxunwei/article/details/135569658?ops_request_misc=elastic_search_misc&request_id=10325c9bb847f22070271274c44fb00d&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~ElasticSearch~search_v2-1-135569658-null-null.nonecase&utm_term=131&spm=1018.2226.3001.4450
title: "RK3568驱动指南｜第十二篇 GPIO子系统-第131章 GPIO子系统API函数的引入_rk3568 gpio 中断-CSDN博客"
description: "文章浏览阅读1.4k次，点赞16次，收藏12次。新版本GPIO子系统接口是基于描述符（descriptor-based）来实现的，而旧版本的GPIO子系统接口是基于整数（integer-based）来实现的，在Linux内核中为了保持向下的兼容性，旧版本的接口在最新的内核版本中仍然得到支持，而随着时间的推移，新版本的GPIO子系统接口会越来越完善，最终完全取代旧版本，所以在本课程中主要讲解新版本的GPIO子系统接口。（11）void *data: 指向与GPIO设备相关的数据的指针，用于存储和访问与GPIO设备相关的自定义数据。_rk3568 gpio 中断"
host: blog.csdn.net
```




# 一、API是基于描述符（descriptor-based）来实现的

## 描述符（descriptor-based）
### 1 、用struct  gpio_desc结构体来表示


### 2 、结构体定义(❤️)
- 1 内核源码的“drivers/gpio/gpiolib.h”目录下

```c
struct gpio_desc {
    struct gpio_device gdev;    // GPIO设备结构体
    unsigned long flags;        // 标志位，用于表示不同的属性
    /* 标志位符号对应的位号 */
    #define FLAG_REQUESTED 0        // GPIO已请求
    #define FLAG_IS_OUT 1           // GPIO用作输出
    #define FLAG_EXPORT 2           // 受sysfs_lock保护的导出标志
    #define FLAG_SYSFS 3            // 通过/sys/class/gpio/control导出的标志
    #define FLAG_ACTIVE_LOW 6       // GPIO值为低电平时激活
    #define FLAG_OPEN_DRAIN 7       // GPIO为开漏类型
    #define FLAG_OPEN_SOURCE 8      // GPIO为开源类型
    #define FLAG_USED_AS_IRQ 9      // GPIO连接到中断请求（IRQ）
    #define FLAG_IS_HOGGED 11       // GPIO被独占占用
    #define FLAG_TRANSITORY 12      // GPIO在休眠或复位时可能失去值
    /* 连接标签 */
    const char *label;            // GPIO的名称
    const char *name;             // GPIO的名称
};
```
> （1）struct gpio_device gdev是一个 struct gpio_device 类型的字段，用于表示 GPIO 设备的相关信息。`struct gpio_device 结构体` 通常**包含设备的底层硬件控制器等信息**。
> 
> （2）unsigned long flags:用于表示 GPIO 的标志位，以表示不同的属性。通过使用位操作，每个标志位可以单独设置或清除。
> 
> （3）第5-14行用于表示**不同标志位的符号常量，与 flags 字段中的位号相对应**。例如，在 flags 字段中的第 0 位表示 FLAG_REQUESTED，第 1 位表示 FLAG_IS_OUT，以此类推
> 
> （4）`const char *label: `这是一个指向字符串 的指针，表示 GPIO 的标签或名称。
> 
> （5）`const char *name:` 这是一个指向字符串的指针，表示 GPIO 的名称。
> 
> 


### 3 、struct gpio_device结构体（1<---）
- 1 定义在内核源码的“drivers/gpio/gpiolib.h”目录下

```c
struct gpio_device {
    int id;                             // GPIO设备ID
    struct device *dev;                 // 对应的设备结构体指针
    struct cdev chrdev;                 // 字符设备结构体
    struct device *mockdev;             // 模拟设备结构体指针
    struct module *owner;               // 拥有该GPIO设备的内核模块指针
    struct gpio_chip *chip;             // 对应的GPIO芯片结构体指针
    struct gpio_desc *descs;            // GPIO描述符数组指针
    int base;                           // GPIO编号的起始值
    u16 ngpio;                          // GPIO的数量
    const char *label;                  // GPIO设备的标签
    void *data;                         // 与GPIO设备相关的数据指针
    struct list_head list;              // 用于将GPIO设备结构体连接到链表中
#ifdef CONFIG_PINCTRL
    /*
     * 如果启用了CONFIG_PINCTRL选项，GPIO控制器可以选择描述它们在SoC中服务的实际引脚范围。
     * 此信息将由pinctrl子系统用于配置相应的GPIO引脚。
     */
    struct list_head pin_ranges;        // 描述GPIO控制器引脚范围的链表
#endif
};
```

#### 结构体解析：
> 该结构体是用来描述GPIO设备的数据结构，关于该结构体的参数介绍如下所示：
> 
> （1）int id:整型字段，表示GPIO设备的ID。每个GPIO设备可以有一个唯一的ID。
> 
> （2）`struct device *dev`:指向 struct device 的指针，表示与GPIO设备相关联的设备结构体。
> 
> （3）struct cdev chrdev: 字符设备结构体，用于实现GPIO设备的字符设备接口。
> 
> （4）`struct device *mockdev`: 指向 struct device 的指针，用于表示GPIO设备的模拟设备结构体。
> 
> （5）`struct module *owner: `指向拥有该GPIO设备的内核模块的指针。
> 
> （6）`struct gpio_chip *chip:` 指向 struct gpio_chip 的指针，表示与GPIO设备关联的GPIO芯片（GPIO控制器 ）结构体。
> 
> （7）`struct gpio_desc *descs`: **指向 struct gpio_desc 数组 的指针**，表示与GPIO设备关联的GPIO描述符。每个GPIO描述符用于描述GPIO的属性和状态。
> 
> （8）int base: 表示GPIO编号的起始值。
> 
> （9）u16 ngpio: 16位无符号整型字段，表示GPIO的数量。
> 
> （10）`const char *label`: 指向字符串的指针，表示GPIO设备的标签或名称。
> 
> （11）`void *data `: 指向与GPIO设备相关的数据的指针，用于存储和访问与GPIO设备相关的自定义数据。
> 
> （12）struct list_head list: 将GPIO设备结构体连接到链表中的字段，用于管理多个GPIO设备的列表。
> 
> （13）struct list_head pin_ranges (仅在启用CONFIG_PINCTRL 选项时存在): 用于描述GPIO控制器引脚范围的链表。如果配置了GPIO控制器的引脚范围，该链表将包含描述每个范围的元素。



### 4 、`struct gpio_chip *chip`结构体：（2<---）
- 1 内核源码目录下的“include/linux/gpio/driver.h”文件中

```c
struct gpio_chip {
    const char *label;                              // GPIO芯片标签
    struct gpio_device gpiodev;                      // GPIO设备
    struct device *parent;                           // 父设备指针
    struct module *owner;                            // 拥有者模块指针
    int (*request)(struct gpio_chip *chip, unsigned offset);// 请求GPIO
    void (*free)(struct gpio_chip *chip, unsigned offset);  // 释放GPIO
    int (*get_direction)(struct gpio_chip *chip, unsigned offset); // 获取GPIO方向
    int (*direction_input)(struct gpio_chip *chip, unsigned offset); // 设置GPIO为输入
    int (*direction_output)(struct gpio_chip *chip, unsigned offset, int value); // 设置GPIO为输出
    int (*get)(struct gpio_chip chip, unsigned offset);   // 获取GPIO值
    int (*get_multiple)(struct gpio_chip chip, unsigned long *mask, unsigned long *bits); // 获取多个GPIO的值
    void (*set)(struct gpio_chip chip, unsigned offset, int value);    // 设置GPIO值
    void (*set_multiple)(struct gpio_chip chip, unsigned long mask, unsigned long *bits); // 设置多个GPIO的值
    int (*set_config)(struct gpio_chip *chip, unsigned offset, unsigned long config); // 设置GPIO配置
    int (*to_irq)(struct gpio_chip chip, unsigned offset);    // 将GPIO转换为中断
    void (*dbg_show)(struct seq_file *s, struct gpio_chip chip);  // 在调试信息中显示GPIO
    int base;                                     // GPIO编号的基准值
    u16 ngpio;                                    // GPIO的数量
    const char *const *names;                     // GPIO的名称数组
..........
};
```


#### 表示与GPIO设备关联的GPIO芯片（GPIO控制器）(❤️)
>` struct gpio_chip *chip`这一结构体用于**描述 GPIO 芯片的属性和操作函数，可以通过函数指针调用相应的函数来请求、释放、设置、获取 GPIO 的状态和数值等操作**，从而实现对GPIO的控制和管理，需要注意的是这个结构体中的一系列函数都不需要我们来填充，这些工作都是由芯片原厂工程师来完成的，我们只需要学会新gpio子系统相应API函数的使用即可。



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


