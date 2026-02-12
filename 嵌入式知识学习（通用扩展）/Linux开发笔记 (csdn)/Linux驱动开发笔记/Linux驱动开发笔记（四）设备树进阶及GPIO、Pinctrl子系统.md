---
title: "Linux驱动开发笔记（四）设备树进阶及GPIO、Pinctrl子系统_设备树gpio-ranges-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/139253603?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读1.7k次，点赞20次，收藏20次。在早期笔者已经简单介绍过设备树的相关信息，本章将详细展开学习一下这部分内容。_设备树gpio-ranges"
tags:
  - "clippings"
---
---

## 前言

  在早期笔者已经简单介绍过设备树的相关信息，本章将详细展开学习一下这部分内容。

---

## 一、设备树的进阶知识

### 1\. 追加/修改节点内容

```c
&cpu0 {
    cpu-supply = <&vdd_cpu>;
};
123
```

  这些源码并不包含在 [根节点](https://so.csdn.net/so/search?q=%E6%A0%B9%E8%8A%82%E7%82%B9&spm=1001.2101.3001.7020) “/{…}”内，它们不是一个新的节点，而是向原有节点追加内容。 以上方源码为例，“&cpu0”表示向“节点标签”为“cpu0”的节点追加数据， 这个节点可能定义在本文件也可能定义在本文件所包含的设备树文件中。

### 2.chosen子节点

```c
chosen {
   bootargs = "earlycon=uart8250,mmio32,0xfe660000 console=ttyFIQ0 root=PARTUUID=614e0000-0000 rw rootwait";
};
123
```

  chosen子节点不代表实际 硬件 ，它主要用于给内核传递参数。 此外这个节点还用作uboot向 linux 内核传递配置参数的“通道”， 我们在Uboot中设置的参数就是通过这个节点传递到内核的， 这部分内容是uboot和内核自动完成的，作为初学者我们不必深究。

### 3\. 获取设备树节点信息

  这一小节我们就开始学习如何从设备树的设备节点获取我们想要的数据。 内核提供了一组 函数 用于从设备节点获取资源(设备节点中定义的属性)的函数，这些函数以of\_开头，称为OF操作函数。 常用的OF函数介绍如下：

| 名称 | 描述 |
| --- | --- |
| of\_find\_node\_by\_path( ) | 根据节点路径寻找节点函数 |
| of\_find\_node\_by\_name( ) | 根据节点名字寻找节点函数 |
| of\_find\_node\_by\_type( ) | 根据节点类型寻找节点函数 |
| of\_find\_compatible\_node( ) | 根据节点类型和compatible属性寻找节点函数 |
| of\_find\_matching\_node\_and\_match( ) | 根据匹配表寻找节点函数 |
| of\_get\_parent( ) | 寻找父节点函数 |
| of\_get\_next\_child( ) | 寻找子节点函数 |

#### 3.1 of\_find\_node\_by\_path( )函数

```c
//根据节点路径寻找节点
struct device_node *of_find_node_by_path(const char *path)
12
```
- 参数：
	- path： 指定节点在设备树中的路径。
- 返回值：
	- device\_node： 结构体指针，如果查找失败则返回NULL，否则返回device\_node类型的结构体指针，它保存着设备节点的信息。
```c
struct device_node {
    const char *name;  //节点名
    #const char *type;  //节点类型
    #phandle phandle; //唯一标识
    const char *full_name;  //节点全名
    #struct fwnode_handle fwnode; //用于支持不同设备
 
    struct  property *properties;  //设备数属性键值对的链表
    #struct property *deadprops;    /* removed properties */ 链表头
    struct  device_node *parent; //父节点
    struct  device_node *child;  //子节点
    struct  device_node *sibling; //兄弟节点
#if defined(CONFIG_OF_KOBJ)
    #struct kobject kobj;//内核对象
#endif
    #unsigned long _flags;//状态标志
    #void   *data;//节点相关的私有数据
#if defined(CONFIG_SPARC)
    #const char *path_component_name;//表示设备节点路径的一部分
    #unsigned int unique_id;//唯一ID
    #struct of_irq_controller *irq_trans;//中断控制器结构体指针
#endif
};
1234567891011121314151617181920212223
```

#### 3.2 of\_find\_node\_by\_name( )函数

```c
//根据节点名字寻找节点
struct device_node *of_find_node_by_name(struct device_node *from,const char *name);
12
```
- 参数：
	- from： 指定从哪个节点开始查找，它本身并不在查找行列中，只查找它后面的节点，如果设置为NULL表示从根节点开始查找。
	- name： 要寻找的节点名。
- 返回值：
	- device\_node： 结构体指针，如果查找失败则返回NULL，否则返回device\_node类型的结构体指针，它保存着设备节点的信息。

#### 3.3 of\_find\_node\_by\_type( )函数

```c
//根据节点类型寻找节点
struct device_node *of_find_node_by_type(struct device_node *from,const char *type)
12
```
- 参数：
	- from： 指定从哪个节点开始查找，它本身并不在查找行列中，只查找它后面的节点，如果设置为NULL表示从根节点开始查找。
	- type： 要查找节点的类型，这个类型就是device\_node-> type。
- 返回值：
	- device\_node： device\_node类型的结构体指针，保存获取得到的节点。同样，如果失败返回NULL。

#### 3.4 of\_find\_compatible\_node( )函数

```c
// 根据节点类型和compatible属性寻找节点
struct device_node *of_find_compatible_node(struct device_node *from,const char *type, const char *compatible)
12
```

  相比of\_find\_node\_by\_name函数增加了一个compatible属性作为筛选条件。

- 参数：
	- from： 指定从哪个节点开始查找，它本身并不在查找行列中，只查找它后面的节点，如果设置为NULL表示从根节点开始查找。
	- type： 要查找节点的类型，这个类型就是device\_node-> type。
	- compatible： 要查找节点的compatible属性。
- 返回值：
	- device\_node： device\_node类型的结构体指针，保存获取得到的节点。同样，如果失败返回NULL。

#### 3.5 of\_find\_matching\_node\_and\_match( )函数

```c
//根据匹配表寻找节点
static inline struct device_node *of_find_matching_node_and_match(struct device_node *from, const struct of_device_id *matches, const struct of_device_id **match)
12
```

  可以看到，该结构体包含了更多的匹配参数，也就是说相比前三个寻找节点函数，这个函数匹配的参数更多，对节点的筛选更细。参数match，查找得到的结果。

- 参数：
	- from： 指定从哪个节点开始查找，它本身并不在查找行列中，只查找它后面的节点，如果设置为NULL表示从根节点开始查找。
	- matches： 源匹配表，查找与该匹配表想匹配的设备节点。
	- of\_device\_id： 结构体如下:
```c
struct of_device_id {
    char    name[32];         //节点中属性为name的值
    char    type[32];        //节点中属性为device_type的值
    char    compatible[128];//节点的名字，在device_node结构体后面放一个字符串，full_name指向它
    const void *data;        //链表，连接该节点的所有属性
};
123456
```
- 返回值：
	- device\_node： device\_node类型的结构体指针，保存获取得到的节点。同样，如果失败返回NULL。

#### 3.6 of\_get\_parent( )函数

```c
//寻找父节点
struct device_node *of_get_parent(const struct device_node *node)
12
```
- 参数：
	- node： 指定谁(节点)要查找父节点。
- 返回值：
	- device\_node： device\_node类型的结构体指针，保存获取得到的节点。同样，如果失败返回NULL。

#### 3.7 of\_get\_next\_child( )函数

```c
//寻找子节点
struct device_node *of_get_next_child(const struct device_node *node, struct device_node *prev)
12
```
- 参数：
	- node： 指定谁(节点)要查找它的子节点。
	- prev： 前一个子节点，寻找的是prev节点之后的节点。这是一个迭代寻找过程，例如寻找第二个子节点，这里就要填第一个子节点。参数为NULL 表示寻找第一个子节点。
- 返回值：
	- device\_node： device\_node类型的结构体指针，保存获取得到的节点。同样，如果失败返回NULL。

### 4\. 提取属性值的of函数

| 名称 | 描述 |
| --- | --- |
| of\_find\_property( ) | 查找节点属性函数 |
| of\_property\_read\_uX\_array( ) | 读取整型属性函数 |
| of\_property\_read\_uX( ) | 简化后的读取整型属性函数,对读取整型属性函数的简单封装 |
| of\_property\_read\_string\_index( ) | 它用于指定读取属性值中第几个字符串,上位替代 |
| of\_property\_read\_bool( ) | 读取布尔型属性函数 |
| of\_iomap( ) | 自动完成物理地址到虚拟地址的转换 |
| of\_address\_to\_resource( ) | 得到在设备树中设置的地址值 |

#### 4.1 of\_find\_property( )函数

```c
struct property *of_find_property(const struct device_node *np,const char *name,int *lenp)
1
```
- 参数：
	- np： 指定要获取那个设备节点的属性信息。
	- name： 属性名。
	- lenp： 获取得到的属性值的大小，这个指针作为输出参数，这个参数“带回”的值是实际获取得到的属性大小。
- 返回值：
	- property： 获取得到的属性。property结构体，我们把它称为节点属性结构体，如下所示。失败返回NULL。从这个结构体中我们就可以得到想要的属性值了。
```c
struct property {
    char    *name;            //属性名
    int     length;            //属性长度
    void    *value;            //属性值
    struct property *next;    //下一个属性
#if defined(CONFIG_OF_DYNAMIC) || defined(CONFIG_SPARC)
    unsigned long _flags;
#endif
#if defined(CONFIG_OF_PROMTREE)
    unsigned int unique_id;
#endif
#if defined(CONFIG_OF_KOBJ)
    struct bin_attribute attr;
#endif
};
123456789101112131415
```

#### 4.2 of\_property\_read\_uX\_array( )函数

```c
//8位整数读取函数
int of_property_read_u8_array(const struct device_node *np, const char *propname, u8 *out_values, size_t sz)

//16位整数读取函数
int of_property_read_u16_array(const struct device_node *np, const char *propname, u16 *out_values, size_t sz)

//32位整数读取函数
int of_property_read_u32_array(const struct device_node *np, const char *propname, u32 *out_values, size_t sz)

//64位整数读取函数
int of_property_read_u64_array(const struct device_node *np, const char *propname, u64 *out_values, size_t sz)
1234567891011
```
- 参数：
	- np： 指定要读取那个设备节点结构体，也就是说读取那个设备节点的数据。
	- propname： 指定要获取设备节点的哪个属性。
	- out\_values： 这是一个输出参数，是函数的“返回值”，保存读取得到的数据。
	- sz： 这是一个输入参数，它用于设置读取的长度。
- 返回值：
	- 返回值，成功返回0，错误返回错误状态码(非零值)，-EINVAL(属性不存在)，-ENODATA(没有要读取的数据)，-EOVERFLOW(属性值列表太小)。

#### 4.3 of\_property\_read\_uX( )函数

```c
//8位整数读取函数
int of_property_read_u8 (const struct device_node *np, const char *propname,u8 *out_values)

//16位整数读取函数
int of_property_read_u16 (const struct device_node *np, const char *propname,u16 *out_values)

//32位整数读取函数
int of_property_read_u32 (const struct device_node *np, const char *propname,u32 *out_values)

//64位整数读取函数
int of_property_read_u64 (const struct device_node *np, const char *propname,u64 *out_values)
1234567891011
```

#### 4.4 of\_property\_read\_string( )函数

&wmsp; 在设备节点中存在很多字符串属性，例如compatible、status、type等等，这些属性可以使用查找节点属性函数of\_find\_property来获取，但是这样比较繁琐。内核提供了一组用于读取字符串属性的函数，介绍如下：

```c
//读取字符串属性函数
int of_property_read_string(const struct device_node *np,const char *propname,const char **out_string)
12
```
- 参数：
	- np： 指定要获取那个设备节点的属性信息。
	- propname： 属性名。
	- out\_string： 获取得到字符串指针，这是一个“输出”参数，带回一个字符串指针。也就是字符串属性值的首地址。这个地址是“属性值”在内存中的真实位置，也就是说我们可以通过对地址操作获取整个字符串属性(一个字符串属性可能包含多个字符串，这些字符串在内存中连续存储，使用’0’分隔)。
- 返回值：
	- 返回值：成功返回0，失败返回错误状态码。

#### 4.5 of\_property\_read\_string\_index( )函数

```c
int of_property_read_string_index(const struct device_node *np,const char *propname, int index,const char **out_string)
1
```

&wmsp; 相比前面的函数增加了参数index，它用于指定读取属性值中第几个字符串，index从零开始计数。 上一个函数只能得到属性值所在地址，也就是第一个字符串的地址，其他字符串需要我们手动修改移动地址，非常麻烦，推荐使用第本函数。

#### 4.6 of\_property\_read\_bool( )函数

&wmsp; 在设备节点中一些属性是BOOL型，当然内核会提供读取BOOL型属性的函数，介绍如下：

```c
//读取布尔型属性
static inline bool of_property_read_bool(const struct device_node *np, const char *propname);
12
```
- 参数：
	- np： 指定要获取那个设备节点的属性信息。
	- propname： 属性名。
- 返回值：
	- 这个函数不按套路出牌，它不是读取某个布尔型属性的值，仅仅是读取这个属性存在或者不存在。如果想要或取值，可以使用之前讲解的“全能”函数查找节点属性函数of\_find\_property。

#### 4.7 of\_iomap( )函数

&wmsp; 在设备树的设备节点中大多会包含一些内存相关的属性，比如常用的reg属性。通常情况下，得到寄存器地址之后我们还要通过ioremap函数将物理地址转化为虚拟地址。现在内核提供了of函数，自动完成物理地址到虚拟地址的转换。介绍如下：

```c
void __iomem *of_iomap(struct device_node *np, int index)
1
```
- 参数：
	- np： 指定要获取那个设备节点的属性信息。
	- index： 通常情况下reg属性包含多段，index 用于指定映射那一段，标号从0开始。
- 返回值：
	- 成功，得到转换得到的地址。失败返回NULL。

  内核也提供了常规获取地址的of函数，这些函数得到的值就是我们在设备树中设置的地址值。介绍如下：

```c
int of_address_to_resource(struct device_node *dev, int index, struct resource *r)
1
```
- 参数：
	- np： 指定要获取那个设备节点的属性信息。
	- index： 通常情况下reg属性包含多段，index 用于指定映射那一段，标号从0开始。
	- r： 这是一个resource结构体，是“输出参数”用于返回得到的地址信息。
```c
struct resource {
    resource_size_t start;        //起始地址
    resource_size_t end;        //结束地址
    const char *name;            //属性名字
    unsigned long flags;
    unsigned long desc;
    struct resource *parent, *sibling, *child;
};
12345678
```
- 返回值：
	- 成功返回0，失败返回错误状态码。

  这里介绍了三类常用的of函数，这些基本满足我们的需求，其他of函数后续如果使用到我们在详细介绍。

## 二、Pinctrl子系统

  在之前我们进行字符设备编辑的时候已经简单提到过引脚复用功能及其修改方法，接下来将讲述一下引脚复用相关的pinctrl子系统，其主要用于管理芯片的引脚，比如引脚的复用，引脚上下拉，驱动能力等。pinctrl核心层是内核抽象出来，向下为个SoC pin controler drvier提供底层通信接口的能力， 向上为其他驱动提供了控制pin的能力，比如pin复用、配置引脚的电气特性，同时也为GPIO子系统提供pin操作。而pin控制器驱动层，主要提供了操作pin的方法。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/84f60383925ce02255485e8b9500df4d.png)

### 2.1 使用pinctrl设置复用关系

  在设备树中，pinctrl（引脚控制）使用客户端和服务端的概念来描述引脚控制的关系和配置，以便在系统启动时正确地初始化和管理硬件设备的引脚。这种划分提供了对引脚功能的抽象，使得设备驱动程序能够以一种标准化的方式使用这些引脚。

#### 2.1.1 客户端（Client）

  pinctrl客户端可以指定引脚描述、引脚组描述和配置描述，以满足其特定的功能和需求。客户端通常与某个具体的硬件设备相关联，例如一个LED灯或者一个传感器。

```c
node {
    pinctrl-names = "default", "wake up";
    pinctrl-0 = <&pinctrl_hog_1>;
    pinctrl-1 = <&pinctrl_hog_2>;
}
12345
```

pinctrl-names 属性定义了两个状态名称：default 和 wake up。  
pinctrl-0 属性指定了第一个状态 default 对应的引脚配置，引用了 pinctrl\_hog\_1 节点。  
pinctrl-1 属性指定了第二个状态 wake up 对应的引脚配置，引用了 pinctrl\_hog\_2 节点。这意味着设备可以处于两个不同的状态之一，每个状态分别使用不同的引脚配置。

#### 2.1.2 服务端（Server）

  服务端是设备树中定义引脚配置的部分。它包含引脚组和引脚描述符，为客户端提供引脚配置选择。服务端在设备树中定义了 pinctrl 节点，其中包含引脚组和引脚描述符的定义。以下是pinctrl节点下的描述形式：

```c
&pinctrl {
    /*----------新添加的内容--------------*/
    led_test {
        led_test_pin: led_test_pin { //led_test_pin”节点标签
            //“rockchip,pins”是固定的格式，后面的内容自定义的，我们将通过这个标签引用这个节点
            rockchip,pins = <0 RK_PC7 RK_FUNC_GPIO &pcfg_pull_none>;
        };
    };
};
123456789
```

  如上述的一个外设xxx，由其使用的引脚为GPIO0\_C7，”RK\_FUNC\_GPIO”设置复用功能为GPIO，每个引脚可以复用的功能具体参考下手册，”&pcfg\_pull\_none”指定上下拉，这里的没有设置不用上下拉。  
  之后我们再去编写leds下的设备节点：

```c
my_led: led {
    compatible = "topeet,led";
    gpios = <&gpio0 RK_PC7 GPIO_ACTIVE_HIGH>;
    pinctrl-names = "default";
    pinctrl-0 = <&rk_led_gpio>;
    };   
123456
```

  此时我们就完成了GPIO的复用功能设置。

### 2.2 pinctrl相关结构体

  内核将pinctrl驱动抽象为pinctrl\_desc对象，具体到soc厂商的pinctrl驱动便是该对象一个实例， 在驱动所有的pin信息以及对于pin的控制接口实例化成pinctrl\_desc，并将pinctrl\_desc注册到内核中，如下

```c
struct pinctrl_desc {
   const char *name;
   const struct pinctrl_pin_desc *pins;   //描述一个pin控制器的引脚,
   unsigned int npins;                    //描述该控制器有多少个引脚
   const struct pinctrl_ops *pctlops;     //引脚操作函数，有描述引脚，获取引脚等，全局控制函数
   const struct pinmux_ops *pmxops;       //引脚复用相关的操作函数
   const struct pinconf_ops *confops;     //引脚配置相关
   struct module *owner;
#ifdef CONFIG_GENERIC_PINCONF
   unsigned int num_custom_params;
   const struct pinconf_generic_params *custom_params;
   const struct pin_config_item *custom_conf_items;
#endif
};
1234567891011121314
```

  一般控制器驱动匹配设备，调用probe，最后会调用pinctrl\_register函数，向内核注册pinctrl，产生pinctrl\_dev，该函数如下：

```c
struct pinctrl_dev *pinctrl_register(struct pinctrl_desc *pctldesc,
                                 struct device *dev, void *driver_data);
12
```

  描述一个引脚的结构体 struct pinctrl\_pin\_desc：

```c
pinctrl_pin_desc
struct pinctrl_pin_desc {
   unsigned number;
   const char *name;
   void *drv_data;
};
123456
```

  很多pin组合在一起，实现特定功能，使用struct group\_desc：

```c
group_desc
struct group_desc {
   const char *name;
   int *pins;
   int num_pins;
   void *data;
};
1234567
```

## 三、GPIO子系统

  在Linux系统中所有的设备树已经设置好了，我们只需要将GPIO口和控制器对接即可。GPIO子系统结构简单描述如下图：  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0fe9bcda3db7285deb5ad77943f992cc.png)

### 1\. 相关API

| 函数名 | 描述 |
| --- | --- |
| of\_get\_named\_gpio( ) | 获取GPIO编号 |
| gpio\_request( ) | 申请GPIO |
| gpio\_direction\_input( ) | 将GPIO配置为输入 |
| gpio\_direction\_output( ) | 将GPIO配置为输出 |
| gpio\_set\_value( ) | GPIO电平输出 |
| gpio\_get\_value( ) | 获取电平状态 |
| gpio\_free( ) | 释放GPIO资源 |

#### 1.1 of\_get\_named\_gpio( )函数

```c
//获取gpio编号
static inline int of_get_named_gpio(struct device_node *np, const char *propname, int index)
12
```
- 参数：  
	\- np：结构体指针  
	\- propname：属性名  
	\- index：编号
- 返回值：  
	\- 成功：返回gpio编号  
	\- 失败：返回错误码

#### 1.2 gpio\_request( )函数

```c
//申请gpio
static inline int gpio_request(unsigned gpio, const char *label)
12
```
- 参数：  
	\- gpio：GPIO编号  
	\- label： 标签 NULL
- 返回值：  
	\- 成功: 返回0  
	\- 失败: 返回错误码

#### 1.3 gpio\_direction\_input( )函数

```c
//设置gpio为输入
static inline int gpio_direction_input(unsigned gpio)
12
```
- 参数：  
	\- gpio：GPIO编号
- 返回值：  
	\- 成功：返回0  
	\- 失败：返回错误码

#### 1.4 gpio\_direction\_output( )函数

```c
//设置gpio为输出
static inline int gpio_direction_output(unsigned gpio, int value)
12
```
- 参数：  
	\- gpio：GPIO编号  
	\- value：输出电平(1高电平;0是低电平)
- 返回值：  
	\- 成功：返回0  
	\- 失败：返回错误码

#### 1.5 gpio\_set\_value( )函数

```c
//设置gpio输出电平
gpio_set_value()static inline void gpio_set_value(unsigned int gpio, int value)
12
```
- 参数：  
	\- gpio：GPIO编号  
	\- value：输出电平
- 返回值：  
	\- 成功：返回0  
	\- 失败：返回错误码

#### 1.6 gpio\_get\_value( )函数

```c
//获取gpio电平状态
static inline int gpio_get_value(unsigned int gpio)
12
```
- 参数：  
	\- gpio：GPIO编号
- 返回值：  
	\- 1： 是高电平  
	\- 0： 是低电平

#### 1.7 gpio\_free( )函数

```c
//释放gpio
static inline void gpio_free(unsigned gpio)
12
```
- 参数：  
	\- gpio GPIO编号
- 返回值：无

### 2.相关结构体

#### 2.1 gpio\_device结构体

  gpio\_device结构体在 [Linux内核](https://so.csdn.net/so/search?q=Linux%E5%86%85%E6%A0%B8&spm=1001.2101.3001.7020) 中用于表示一个GPIO控制器，它管理一个或多个gpio\_chip和该组下的所有引脚（pin）。多个gpio\_device结构体在内核中通常通过链表来组织和管理

```c
struct gpio_device {
   int                       id;           //gpio控制器的id，也就是第几个
   struct device             dev;
   struct cdev               chrdev;
   struct device             *mockdev;
   struct module             *owner;
   struct gpio_chip  *chip;
   struct gpio_desc  *descs;
   int                       base;         gpio在内核中的编号，申请gpio口时就是根据这个编号来查找
   u16                       ngpio;        //该gpio控制器有多少个引脚
   const char                *label;    //标签
   void                      *data;
   struct list_head        list;

#ifdef CONFIG_PINCTRL
   /*
   * If CONFIG_PINCTRL is enabled, then gpio controllers can optionally
   * describe the actual pin range which they serve in an SoC. This
   * information would be used by pinctrl subsystem to configure
   * corresponding pins for gpio usage.
   */
   struct list_head pin_ranges;
#endif
};
123456789101112131415161718192021222324
```

id：表示这是系统中第几个GPIO控制器。  
dev：通用设备结构体，包含了该设备的基本信息和操作函数。  
chip：指向关联的gpio\_chip结构体的指针，gpio\_chip描述了该组GPIO引脚的具体操作方式。  
descs：指向一个gpio\_desc结构体的数组，用于描述该组GPIO控制器下的所有引脚。每个引脚都有一个对应的gpio\_desc。  
base：表示该GPIO控制器中引脚的起始编号，加上偏移量可以得到每个引脚的编号。  
ngpio：表示该GPIO控制器管理的引脚数量。  
label：用于标识该GPIO控制器的标签或名称。  
data：私有数据指针，可以用于存储与该GPIO控制器相关的任何额外信息。  
list：链表节点，用于将多个gpio\_device结构体链接在一起。

#### 2.2 gpio\_chip结构体

  gpio\_chip结构体是Linux GPIO子系统中描述GPIO控制器功能和操作的核心数据结构，它包含了控制GPIO引脚所需的所有信息和接口，包括相关操作函数和中断相关。

```c
struct gpio_chip {
   const char                *label;       //GPIO端口的名字，标签
   struct device             *dev;
   struct module             *owner;
   
    //gpio在内核中的编号，申请gpio口时就是根据这个编号来查找
   int                       base;      
       
   u16                       ngpio;         //该控制器的GPIO数目
   const char                *const *names;
   unsigned                  can_sleep;
   
   /*操作gpio口的方法*/
   int (*request)(struct gpio_chip *chip, unsigned offset);
   void (*free)(struct gpio_chip *chip, unsigned offset);
   int (*direction_input)(struct gpio_chip *chip, unsigned offset);
   int (*get)(struct gpio_chip *chip, unsigned offset);
   int (*direction_output)(struct gpio_chip *chip, unsigned offset, int value);
   int (*set_debounce)(struct gpio_chip *chip, unsigned offset, unsigned debounce);
   void (*set)(struct gpio_chip *chip, unsigned offset, int value);
   int (*to_irq)(struct gpio_chip *chip, unsigned offset);
   /*......*/
};
1234567891011121314151617181920212223
```

label：一个字符串，用于标识GPIO控制器的名称或标签。  
base：表示该GPIO控制器管理的第一个GPIO引脚的编号。  
ngpio：表示该GPIO控制器管理的GPIO引脚数量。  
descs：指向gpio\_desc结构体的数组，详细描述了该GPIO控制器下的每一个引脚的状态和信息。

#### 2.3 gpio\_desc结构体

  GPIO Controller中每一个引脚用gpio\_desc表示。

```c
struct gpio_desc {
   struct gpio_device        *gdev;      //gpio_device里面描述了gpio信息，
   unsigned long             flags;
   /* flag symbols are bit numbers */
   #define FLAG_REQUESTED    0
   #define FLAG_IS_OUT       1
   #define FLAG_EXPORT       2       /* protected by sysfs_lock */
   #define FLAG_SYSFS        3       /* exported via /sys/class/gpio/control */
   #define FLAG_ACTIVE_LOW   6       /* value has active low */
   #define FLAG_OPEN_DRAIN   7       /* Gpio is open drain type */
   #define FLAG_OPEN_SOURCE 8        /* Gpio is open source type */
   #define FLAG_USED_AS_IRQ 9        /* GPIO is connected to an IRQ */
   #define FLAG_IS_HOGGED    11      /* GPIO is hogged */
   #define FLAG_TRANSITORY 12        /* GPIO may lose value in sleep or reset */

   /* Connection label */
   const char                *label;
   /* Name of the GPIO */
   const char                *name;
};
1234567891011121314151617181920
```

gdev：指向gpio\_device结构体的指针。  
flags：标志位字段，用于指示当前GPIO引脚的状态。例如，当使用gpio\_request函数申请GPIO资源时，这个字段会被置位；当使用gpio\_free函数释放GPIO资源时，这个字段会被清零。  
name：GPIO引脚的名称，通常用于调试和日志输出。  
label：GPIO引脚的标签，用于在用户空间或其他内核模块中标识这个引脚。

### 3\. GPIO设备树分析

  这里以GPIO3为例：

```c
gpio3: gpio@fe760000 {//节点名
    compatible = "rockchip,gpio-bank"; //厂商名  设备名
    reg = <0x0 0xfe760000 0x0 0x100>; //地址  0x0 0xfe760000控制器地址   0x0 0x100地址范围
    interrupts = <GIC_SPI 36 IRQ_TYPE_LEVEL_HIGH>;//中断
    clocks = <&cru PCLK_GPIO3>, <&cru DBCLK_GPIO3>;//时钟
 
    gpio-controller;//标识
    #gpio-cells = <2>;//描述子节点个数
    gpio-ranges = <&pinctrl 0 96 32>; //引脚范围 &pinctrl 引用pinctrl节点 0    96 GPIO起始序号  32引脚范围
    interrupt-controller;
    #interrupt-cells = <2>;//描述子节点个数
};
123456789101112
```

  在这个实例中，大部分的内容我们已经提前讲到过了，这里主要介绍一下gpio-controller、gpio-cells和gpio- ranges 这两个部分：

#### 3.1 gpio-controller属性

**gpio-controller** 用于标识一个设备节点作为GPIO控制器（GPIO控制器是负责管理和控制GPIO引脚的硬件模块或驱动程序），其通常作为设备节点的一个属性出现，位于设备节点的属性列表中。当一个设备节点被标识为GPIO控制器时，它通常会定义一组GPIO引脚，并提供相关的GPIO控制和配置功能。其他设备节点可以使用该GPIO控制器来控制和管理其GPIO引脚。  
  通过使用gpio-controller属性，设备树可以明确标识出GPIO控制器设备节点，使系统可以正确识别和管理GPIO引脚的配置和控制。

#### 3.2 gpio-cells属性

**gpio-cells** 用于指定GPIO引脚描述符的编码方式（GPIO引脚描述符是用于标识和配置GPIO引脚的一组值，例如引脚编号、引脚属性等），该属性的属性值是一个整数，表示用于编码GPIO引脚描述符的单元数。通常，这个值为2。  
gpio-ranges属性是设备树中一个用于描述GPIO范围映射的属性。它通常用于描述具有大量GPIO引脚的GPIO控制器，以简化GPIO引脚的编码和访问。

#### 3.3 gpio-ranges属性

  在设备树中，GPIO控制器的每个引脚都有一个本地编号，用于在控制器内部进行引脚寻址。然而，这些本地编号并不一定与外部引脚的物理编号或其他系统中使用的编号一致。为了解决这个问题，可以使用gpio-ranges属性将本地编号映射到实际的引脚编号。  
  gpio-ranges属性是一个包含一系列整数值的列表，每个整数值对应于设备树中的一个GPIO控制器。列表中的每个整数值按照特定的顺序提供以下信息：  
（1）外部引脚编号的起始值。  
（2）GPIO控制器内部本地编号的起始值。  
（3）引脚范围的大小（引脚数量）。

  例如将gpio-ranges属性的值设置为<&pinctrl 0 0 32>，其中<&pinctrl>表示引用了名为pinctrl的引脚控制器节点，0 0 32表示外部引脚从0开始，控制器本地编号从0开始，共映射了32个引脚。这样，gpio-ranges属性将GPIO控制器的本地编号直接映射到外部引脚编号，使得GPIO引脚的编码和访问更加简洁和直观。

**免责声明：本文参考了野火和讯为的部分资料，仅供学习参考使用，若有侵权或勘误请联系笔者。**

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/139253603

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