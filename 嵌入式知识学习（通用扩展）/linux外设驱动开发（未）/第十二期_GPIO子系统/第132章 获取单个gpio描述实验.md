---
title: "{{title}}"
aliases: 
tags: 
description: 
source:
---

# 备注(声明)：新gpio子系统中获取单个gpio描述的api接口进行讲解


# 参考文章：

```cardlink
url: https://blog.csdn.net/beijingxunwei/article/details/135570716?ops_request_misc=elastic_search_misc&request_id=1a931c97597edac449fc0a91b41a5290&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~ElasticSearch~search_v2-1-135570716-null-null.nonecase&utm_term=132&spm=1018.2226.3001.4450
title: "RK3568驱动指南｜第十二篇 GPIO子系统-132章 获取单个gpio描述实验_rk3568 gpio设置无效-CSDN博客"
description: "文章浏览阅读2.1k次，点赞25次，收藏23次。相较于上面介绍的gpiod_get函数，下面的三个函数可能会多一个index参数和optional的函数后缀，其中index 表示GPIO的索引值，当设备树的GPIO属性值包含多个GPIO引脚描述时，使用index来表示每个GPIO引脚的唯一标识。在第三行的内容中，1 表示引脚索引，RK_PA0表示资源描述符，用于标识与该引脚相关联的物理资源，表示引脚所属的功能组，RK _FUNC_GPI0 表示将引脚的功能设置为GPIO，&pcfg_pull_none表示引脚配置为无上下拉。_rk3568 gpio设置无效"
host: blog.csdn.net
```


# 一、函数介绍

## 获取GPIO描述符
### 1 、`struct  gpio_desc *gpiod_get` (❤️)


### 2 、该函数的详细介绍：
```c
函数原型：
struct gpio_desc *__must_check gpiod_get(struct device *dev,const char *con_id,enum gpiod_flags flags);

头文件：
#include <linux/gpio/consumer.h>

```

> 参数：
> 
> dev：指向设备结构体的指针，表示与GPIO相关联的设备。
> 
> **con_id：连接标识符**（connection identifier），用于标识所需的GPIO连接。通常由设备树（Device Tree）或其他设备描述信息定义
> 
> flags：GPIO 描述符的选项标志，用于指定GPIO的属性和操作模式。以下是一些常用的选项标志（enum gpiod_flags）：
> 
> GPIOF_INPUT：将GPIO配置为输入模式。
> 
> GPIOF_OUTPUT：将GPIO配置为输出模式。
> 
> GPIOF_ACTIVE_LOW：指示GPIO的默认电平为低电平（激活低电平）。
> 
> GPIOF_OPEN_DRAIN：将GPIO配置为开漏输出模式。
> 
> GPIOF_OPEN_SOURCE：将GPIO配置为开源输出模式。
> 
> 函数功能：
> 
> **获取与给定设备和连接标识符（con_id）相关联的GPIO描述符**。
> 
> 返回值：
> 
> 如果成功获取到 GPIO 描述符，则返回指向 struct gpio_desc 的指针；如果获取失败，则返回 NULL。






### 3 、另外三个同样是获取GPIO描述符资源的函数

```c
struct gpio_desc *gpiod_get_index(struct device *dev, const char *con_id, unsigned int idx, enum gpiod_flags flags);

struct gpio_desc *gpiod_get_optional(struct device *dev, const char *con_id, enum gpiod_flags flags);

struct gpio_desc *gpiod_get_index_optional(struct device *dev, const char *con_id, unsigned int index, enum gpiod_flags flags);
```
> 相较于上面介绍的gpiod_get函数，下面的三个函数可能会多一个index参数和optional 的函数后缀，其中`index `表示**GPIO的索引值**，当设备树的GPIO属性值包含多个GPIO引脚描述时，使用index来表示每个GPIO引脚的唯一标识。而带optional() 后缀的函数与不带 optional 后缀的函数在功能上是相同的，都用于获取GPIO描述符，两者的区别在于返回值的不同：
> 
> 使用**带optional() 的函数时，如果获取失败，返回值为 NULL**。
> 
> 使用不带 optional 的函数时，如果获取失败，返回值是一个特殊的结构表示获取GPIO描述符失败。


### 4 、

## 释放GPIO描述符

### 5、gpiod_put() 函数(❤️)


### 6、函数的详细介绍：

```c
函数原型：
void gpiod_put(struct gpio_desc *desc);

头文件：
#include <linux/gpio/consumer.h>

参数：
desc：指向要释放的 GPIO 描述符的指针。

功能：
gpiod_put() 函数用于释放之前通过 gpiod_get() 或类似函数获取的 GPIO 描述符。

返回值：
无返回值。

```

### 7、


# 二、获取单个gpio描述实验

## 设备树的修改
### 1 、网盘路径：
> 本小节修改好的设备树以及编译好的boot.img镜像 存放路径为：iTOP-RK3568开发板【底板V1.7版本】\03_【iTOP-RK3568开发板】指南教程\02_Linux驱动配套资料\04_Linux驱动例程\86_gpioctrl05\01_内核镜像。

### 2 、引脚位置：
> 这里选择RK3568开发板 背面20Pin GPIO座子的1号引脚，右边对应的丝印为**I2C3_SDA_M0**，这里的丝印表示该引脚可以复用为I2C3的SDA功能，而在当前的设备树源码中这个引脚是没有任何复用的，该引脚的具体位置如下所示：
> 
> ![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第132章 获取单个gpio描述实验/file-20260512163949448.png]]






### 3 、找到引脚对应的GPIO(❤️)
> ![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第132章 获取单个gpio描述实验/file-20260512164026407.png]]

> 可以看到1号管脚的**网络标号为I2C3_SDA_M0**，然后打开核心板原理图，根据这个网络标号进行**搜索**，查找到的核心板内容如下所示：
> ![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第132章 获取单个gpio描述实验/file-20260512164117367.png]]


> 左侧为该引脚的一些复用功能，箭头指向的部分为接下来要用到的GPIO引脚编号**GPIO1_A0**，然后对设备树进行内容的添加，从而将该引脚复用为GPIO的功能。



### 4 、将该引脚复用为GPIO(❤️)
> 首先根据上图中的复用功能查看设备树中是否已经对该引脚进行了复用，在**确保该引脚无任何复用之后**，对rk3568-evb1-ddr4-v10.dtsi设备树进行内容的添加，在根节点的结尾添加以下内容：

#### rk3568-evb1-ddr4-v10.dtsi设备树
```c
my_gpio:gpiol_a0 {
    compatible = "mygpio";
    my-gpios = <&gpio1 RK_PA0 GPIO_ACTIVE_HIGH>;
    pinctrl-names = "default";
    pinctrl-0 = <&mygpio_ctrl>;
};
```

> compatible: 用于指定设备的兼容性字符串 ，与驱动程序中的值相匹配。
> 
> my-gpios: 指定了与该设备相关联的GPIO。&gpiol 表示 GPIO 控制器的句柄（handle），RK_PA0 是与该GPIO相关的资源描述符（resource specifier），GPIO_ACTIVE_HIGH 表示GPIO的默认电平为高电平。
> 
> pinctrl-names 和 pinctrl-0: 用于指定引脚控制器（pinctrl）的配置。pinctrl-names 表示引脚控制器配置的名称，这里为 "default"。**pinctrl-0 指定了与该配置相关联的引脚控制器句柄，这里为 &mygpio_ctrl**。

#### 然后找到pinctrl节点，在节点尾部添加以下内容，
```c
mygpio {
    mygpio_ctrl: my-gpio-ctrl {
        rockchip,pins = <1 RK_PA0 RK_FUNC_GPIO &pcfg_pull_none>;
    };
};
```
> 在第三行的内容中，1 表示引脚索引，RK_PA0表示资源描述符，用于标识与该引脚相关联的物理资源，表示引脚所属的功能组，`RK _FUNC_GPI0` 表示将引脚的功能设置为GPIO，&pcfg_pull_none表示引脚配置为无上下拉。






### 5、编译内核，然后将生成的boot.img镜像烧写到开发板上即可。


### 6、






## 驱动程序的编写
### 1 、网盘路径
> 本实验对应的网盘路径为：iTOP-RK3568开发板【底板V1.7版本】\03_【iTOP-RK3568开发板】指南教程\02_Linux驱动配套资料\04_Linux驱动例程\86_gpioctrl05\02_module。

### 2 、编写完成的gpio_api.c代码如下所示:
```c
#include <linux/module.h>
#include <linux/platform_device.h>
#include <linux/mod_devicetable.h>
#include <linux/gpio/consumer.h>
#include <linux/gpio.h>
 
struct gpio_desc *mygpio1;  // GPIO 描述符指针
int dir, value, irq;  // 方向、值和中断号变量
 
//平台设备初始化函数
static int my_platform_probe(struct platform_device *dev) {
    printk("This is mydriver_probe\n");
	// 获取GPIO描述符
    mygpio1 = gpiod_get_optional(&dev->dev, "my", 0);
    if (mygpio1 == NULL) {
        printk("gpiod_get_optional error\n");
        return -1;
    }
 
    gpiod_direction_output(mygpio1, 0);  // 将 GPIO 设置为输出模式并设置初始值为低电平
    gpiod_set_value(mygpio1, 1);  // 设置 GPIO 为高电平
 
    dir = gpiod_get_direction(mygpio1);  // 获取 GPIO 的方向
    if (dir == GPIOF_DIR_IN) {
        printk("dir is GPIOF_DIR_IN\n");  // 输出方向为输入
    } else if (dir == GPIOF_DIR_OUT) {
        printk("dir is GPIOF_DIR_OUT\n");  // 输出方向为输出
    }
 
    value = gpiod_get_value(mygpio1);  // 获取 GPIO 的值
    printk("value is %d\n", value);  // 输出 GPIO 的值
 
    irq = gpiod_to_irq(mygpio1);  // 将 GPIO 转换为中断号
    printk("irq is %d\n", irq);  // 输出中断号
 
    return 0;
}
 
// 平台设备的移除函数
static int my_platform_remove(struct platform_device *pdev)
{
    printk(KERN_INFO "my_platform_remove: Removing platform device\n");
 
    // 清理设备特定的操作
    // ...
 
    return 0;
}
 
 
const struct of_device_id of_match_table_id[]  = {
	{.compatible="mygpio"},
};
 
// 定义平台驱动结构体
static struct platform_driver my_platform_driver = {
    .probe = my_platform_probe,
    .remove = my_platform_remove,
    .driver = {
        .name = "my_platform_device",
        .owner = THIS_MODULE,
		.of_match_table =  of_match_table_id,
    },
};
 
// 模块初始化函数
static int __init my_platform_driver_init(void)
{
    int ret;
 
    // 注册平台驱动
    ret = platform_driver_register(&my_platform_driver);
    if (ret) {
        printk(KERN_ERR "Failed to register platform driver\n");
        return ret;
    }
 
    printk(KERN_INFO "my_platform_driver: Platform driver initialized\n");
 
    return 0;
}
 
// 模块退出函数
static void __exit my_platform_driver_exit(void)
{
    // 注销平台驱动
    platform_driver_unregister(&my_platform_driver);
 
    printk(KERN_INFO "my_platform_driver: Platform driver exited\n");
}
 
module_init(my_platform_driver_init);
module_exit(my_platform_driver_exit);
 
MODULE_LICENSE("GPL");
MODULE_AUTHOR("topeet");
```

### 3 、关键代码：(❤️)
```c
struct gpio_desc *mygpio1;  // GPIO 描述符指针
int dir, value, irq;  // 方向、值和中断号变量

static int my_platform_probe(struct platform_device *dev) {

	// 获取GPIO描述符
    mygpio1 = gpiod_get_optional(&dev->dev, "my", 0);

    gpiod_direction_output(mygpio1, 0);  // 将 GPIO 设置为输出模式并设置初始值为低电平
    gpiod_set_value(mygpio1, 1);  // 设置 GPIO 为高电平
 
    dir = gpiod_get_direction(mygpio1);  // 获取 GPIO 的方向
    value = gpiod_get_value(mygpio1);  // 获取 GPIO 的值

    irq = gpiod_to_irq(mygpio1);  // 将 GPIO 转换为中断号


```



### 4 、





## 运行测试
### 1 、驱动的加载
> ![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第132章 获取单个gpio描述实验/file-20260512170246390.png]]

### 2 、



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


