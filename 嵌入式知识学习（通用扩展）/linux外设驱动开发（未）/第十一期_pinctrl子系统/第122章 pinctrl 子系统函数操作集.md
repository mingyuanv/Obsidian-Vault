---
title: "{{title}}"
aliases: 
tags: 
description: 
source:
---

# 备注(声明)：对pinctrl_desc结构体中的三个函数操作集进行详细的讲解

## 思维导图：

[[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十一期_pinctrl子系统/canvas/第122章 groups 和 function 与操作集分析.canvas|第122章 groups 和 function 与操作集分析]]



# 参考文章：


```cardlink
url: https://blog.csdn.net/BeiJingXunWei/article/details/135548342?spm=1001.2101.3001.10796
title: "RK3568驱动指南｜第十一篇 pinctrl 子系统-第122章pinctrl 子系统函数操作集_rk3568-pinctrl.dtsi-CSDN博客"
description: "文章浏览阅读1.9k次，点赞25次，收藏27次。在pinctrl的probe函数中，首先定义了一个struct rockchip_pinctrl *类型的结构体指针类型的变量info，然后传入了rockchip_pinctrl_register函数，然后又分别传入了rockchip_pinctrl_parse_dt函数和devm_pinctrl_register函数。其中，RK_PA2用于CAN0的接收引脚（can0_rxm1），RK_PA1用于CAN0的发送引脚（can0_txm1）。结构体pinconf_ops，用于定义引脚配置操作的函数指针。_rk3568-pinctrl.dtsi"
host: blog.csdn.net
```



# 一、groups和function

## 引脚组（Groups）:这个功能使用那组引脚。(❤️)
### 1 、一组具有相似功能、约束条件或共同工作的引脚的集合


### 2 、每个引脚组通常与特定的硬件功能或外设相关联
> 例如，一个引脚组可以用于控制串行通信接口（如UART或SPI），另一个引脚组可以用于驱动GPIO。
> 
### 3 、


## 功能（Function）：外设功能
### 4 、定义了芯片上具有外设功能的功能



### 5、定义了芯片上具有外设功能的功能(❤️)
- 2 这些功能可以是串口、SPI、I2C 等外设功能。

### 6、




## 举例
### 1 、rk3568-pinctrl.dtsi设备树文件中的can0和can1

> 在上面的设备树中，**can0和can1 对应两个不同的function**，分别为 CAN0 控制器和CAN1控制器。**每个控制器中又都有两个不同的groups引脚组**

```c
can0 {
        /omit-if-no-ref/
        can0m0_pins: can0m0-pins {
            rockchip,pins =
                /* can0_rxm0 */
                <0 RK_PB4 2 &pcfg_pull_none>,
                /* can0_txm0 */
                <0 RK_PB3 2 &pcfg_pull_none>;
        };
 
        /omit-if-no-ref/
        can0m1_pins: can0m1-pins {
            rockchip,pins =
                /* can0_rxm1 */
                <2 RK_PA2 4 &pcfg_pull_none>,
                /* can0_txm1 */
                <2 RK_PA1 4 &pcfg_pull_none>;
        };
    };
 
    can1 {
        /omit-if-no-ref/
        can1m0_pins: can1m0-pins {
            rockchip,pins =
                /* can1_rxm0 */
                <1 RK_PA0 3 &pcfg_pull_none>,
                /* can1_txm0 */
                <1 RK_PA1 3 &pcfg_pull_none>;
        };
 
        /omit-if-no-ref/
        can1m1_pins: can1m1-pins {
            rockchip,pins =
                /* can1_rxm1 */
                <4 RK_PC2 3 &pcfg_pull_none>,
                /* can1_txm1 */
                <4 RK_PC3 3 &pcfg_pull_none>;
        };
    };
```
### 2 、CAN0控制器：
> `引脚组 can0m0-pins`：这是CAN0控制器的第一个引脚组，用于**配置CAN0的引脚**。它定义了两个引脚：**RK_PB4和RK_PB3**。其中，RK_PB4用于 CAN0 的接收引脚（can0_rxm0），RK_PB3用于CAN0的发送引脚（can0_txm0）。
> 
> `引脚组 can0m1-pins`：这是CAN0控制器的第二个引脚组，也用于配置CAN0的引脚。它定义了两个引脚：**RK_PA2和RK_PA1**。其中，RK_PA2用于CAN0的接收引脚（can0_rxm1），RK_PA1用于CAN0的发送引脚（can0_txm1）。


### 3 、CAN1 控制器：
引脚组 can1m0-pins：这是CAN1控制器的第一个引脚组，用于配置CAN1的引脚。它定义了两个引脚：RK_PA0和RK_PA1。其中，RK_PA0用于CAN1的接收引脚（can1_rxm0），RK_PA1用于CAN1的发送引脚（can1_txm0）。

引脚组 can1m1-pins：这是CAN1控制器的第二个引脚组，也用于配置CAN1 的引脚。它定义了两个引脚：RK_PC2和RK_PC3。其中，RK_PC2用于CAN1的接收引脚（can1_rxm1），RK_PC3用于CAN1的发送引脚（can1_txm1）。


### 4 、



# 二、操作集结构体与rockchip_pinctrl 分析 

## 函数操作集结构体讲解

### 1 、pinctrl_desc结构体中总共有三个函数操作集(❤️)

```c
    const struct pinctrl_ops *pctlops;               // 引脚控制操作函数指针
    const struct pinmux_ops *pmxops;                 // 引脚复用操作函数指针
    const struct pinconf_ops *confops;               // 引脚配置操作函数指针
```
### 2 、pinctrl_ops
- 1 内核源码的“include/linux/pinctrl/pinctrl.h”文件中


```c
struct pinctrl_ops {
	int (*get_groups_count)(struct pinctrl_dev *pctldev); //获取指定的 Pin Control 设备支持的引脚组数量
	const char *(*get_group_name)(struct pinctrl_dev *pctldev,
				      unsigned selector);// 获取指定引脚组选择器对应的引脚组名称
	int (*get_group_pins)(struct pinctrl_dev *pctldev,
			      unsigned selector,
			      const unsigned **pins,
			      unsigned *num_pins);// 获取指定引脚组选择器对应的引脚组中的引脚列表
	void (*pin_dbg_show)(struct pinctrl_dev *pctldev, struct seq_file *s,
			     unsigned offset);//在调试信息中输出指定引脚选择器对应的引脚信息
	int (*dt_node_to_map)(struct pinctrl_dev *pctldev,
			      struct device_node *np_config,
			      struct pinctrl_map **map, unsigned *num_maps);// 根据给定的设备树节点，创建与之相关联的 Pin Control 映射
	void (*dt_free_map)(struct pinctrl_dev *pctldev,
			    struct pinctrl_map *map, unsigned num_maps);//释放之前通过 dt_node_to_map 创建的 Pin Control 映射
};
```

#### 每个操作函数的简要说明：
>  pinctrl_ops结构体定义了一组操作函数，用于**与 Pin Control设备交互**。以下是对每个操作函数的简要说明：
> 
> （1）get_groups_count：获取引脚组的数量。
> 
> （2）get_group_name：获取引脚组的名称。
> 
> （3）get_group_pins：获取引脚组的引脚列表。
> 
> （4）pin_dbg_show：在调试信息中输出引脚信息。
> 
> （5）dt_node_to_map：根据设备树节点创建与之相关联的 Pin Control 映射。
> 
> （6）dt_free_map：释放通过 dt_node_to_map 创建的 Pin Control 映射。
> 
> 这些操作函数用于**对引脚控制器进行配置和管理，例如获取引脚组和引脚信息，以及创建和释放与设备树节点相关的引脚映射**
> 




### 3 、pinmux_ops
- 1 内核源码的“include/linux/pinctrl/pinctrl.h”文件中

```c
struct pinmux_ops {
	int (*request) (struct pinctrl_dev *pctldev, unsigned offset);//查看是否可以将某个引脚设置为可用于复用
	int (*free) (struct pinctrl_dev *pctldev, unsigned offset);//request() 回调的反向函数，在请求后释放引脚
	int (*get_functions_count) (struct pinctrl_dev *pctldev);//返回此 Pinmux 驱动程序中可选择的命名函数数量
	const char *(*get_function_name) (struct pinctrl_dev *pctldev,
					  unsigned selector);//返回复用选择器的函数名称，核心调用此函数来确定应将某个设备映射到哪个复用设置
	int (*get_function_groups) (struct pinctrl_dev *pctldev,
				  unsigned selector,
				  const char * const **groups,
				  unsigned *num_groups);//返回与某个函数选择器相关联的一组组名称（依次引用引脚）
	int (*set_mux) (struct pinctrl_dev *pctldev, unsigned func_selector,
			unsigned group_selector);//使用特定引脚组启用特定复用功能
	int (*gpio_request_enable) (struct pinctrl_dev *pctldev,
				    struct pinctrl_gpio_range *range,
				    unsigned offset);//在特定引脚上请求并启用 GPIO
	void (*gpio_disable_free) (struct pinctrl_dev *pctldev,
				   struct pinctrl_gpio_range *range,
				   unsigned offset);//在特定引脚上释放 GPIO 复用
	int (*gpio_set_direction) (struct pinctrl_dev *pctldev,
				   struct pinctrl_gpio_range *range,
				   unsigned offset,
				   bool input);//根据 GPIO 配置为输入或输出而进行不同的配置
	bool strict;//不允许将同一引脚同时用于 GPIO 和其他功能。在批准引脚请求之前，严格检查 gpio_owner 和 mux_owner
};
```

#### 结构体成员的详细解释：
> struct  pinmux_ops是一个用于**描述引脚复用操作的结构体**。它定义了一组函数指针，这些函数指针指向了引脚控制器驱动程序中实现的具体功能。下面是对该结构体成员的详细解释：
> 
> （1）request: 判断是否可以将某个引脚设置为可用于复用。
> 
> （2）free: 该函数是request()函数的反向操作，用于在引脚请求后释放引脚。
> 
> （3）get_functions_count: 返回在该引脚控制器驱动程序 中可选择的命名函数的数量。
> 
> （4）get_function_name: 返回复用选择器的函数名称
> 
> （5）get_function_groups: 返回与某个函数选择器相关联的一组组名称（依次引用引脚）。
> 
> （6）set_mux: 用于启用特定的复用功能。
> 
> （7）gpio_request_enable: 在特定引脚上请求并启用GPIO。
> 
> （8）gpio_disable_free: 释放特定引脚上的GPIO复用。
> 
> （9）gpio_set_direction: 根据GPIO配置将引脚设置为输入或输出。
> 
> （10）strict: 表示是否严格检查将同一引脚同时用于GPIO和其他功能的情况。在批准引脚请求之前，会严格检查gpio_owner和mux_owner。如果设置为true，则不允许同时使用同一引脚作为GPIO和其他功能；如果设置为false，则允许同时使用。
> 
> pinmux_ops结构体提供了一组函数指针，这些函数指针定义了引脚复用操作的各个方面。**通过实现这些函数，引脚控制器驱动程序可以与核心交互，并提供引脚复用的功能**。核心可以通过调用这些函数来请求、释放引脚，设置复用功能，操作GPIO等。这个结构体的设计允许引脚控制器驱动程序根据具体的硬件需求和功能定义自己的操作。




### 4 、pinconf_ops
- 1 内核源码的“include/linux/pinctrl/pinconf.h”文件中
```c
struct pinconf_ops {
#ifdef CONFIG_GENERIC_PINCONF
	bool is_generic; // 是否为通用引脚配置操作
#endif
	int (*pin_config_get) (struct pinctrl_dev *pctldev,
			       unsigned pin,
			       unsigned long *config); // 获取引脚配置信息
	int (*pin_config_set) (struct pinctrl_dev *pctldev,
			       unsigned pin,
			       unsigned long *configs,
			       unsigned num_configs); // 设置引脚配置信息
	int (*pin_config_group_get) (struct pinctrl_dev *pctldev,
				     unsigned selector,
				     unsigned long *config); // 获取引脚组配置信息
	int (*pin_config_group_set) (struct pinctrl_dev *pctldev,
				     unsigned selector,
				     unsigned long *configs,
				     unsigned num_configs); // 设置引脚组配置信息
	int (*pin_config_dbg_parse_modify) (struct pinctrl_dev *pctldev,
					   const char *arg,
					   unsigned long *config); // 解析和修改引脚配置的调试函数
	void (*pin_config_dbg_show) (struct pinctrl_dev *pctldev,
				     struct seq_file *s,
				     unsigned offset); // 调试函数，显示引脚配置信息
	void (*pin_config_group_dbg_show) (struct pinctrl_dev *pctldev,
					   struct seq_file *s,
					   unsigned selector); // 调试函数，显示引脚组配置信息
	void (*pin_config_config_dbg_show) (struct pinctrl_dev *pctldev,
					    struct seq_file *s,
					    unsigned long config); // 调试函数，显示引脚配置的具体信息
};
```

#### 参数详解：定义引脚配置操作的函数指针
> （1）is_generic: 一个布尔值，表示是否为通用引脚配置操作。在配置文件中定义了CONFIG_GENERIC_PINCONF时可用。
> 
> （2）pin_config_get: 获取引脚配置信息。
> 
> （3）pin_config_set: 设置引脚配置信息。
> 
> （4）pin_config_group_get: 获取引脚组配置信息。
> 
> （5）pin_config_group_set: 设置引脚组配置信息。
> 
> （6）pin_config_dbg_parse_modify: 解析和修改引脚配置的调试函数。
> 
> （7）pin_config_dbg_show: 显示引脚配置信息的调试函数。
> （8）pin_config_group_dbg_show: 显示引脚组配置信息的调试函数。
> 
> （9）pin_config_config_dbg_show: 显示引脚配置具体信息的调试函数。
> 
> 结构体pinconf_ops，用于定义引脚配置操作的函数指针。每个函数指针都对应了一个特定的操作，如获取引脚配置、设置引脚配置、获取引脚组配置等。这些函数在驱动程序中实现，用于对硬件引脚进行配置和控制。


### 5、





## rockchip_pinctrl 进一步分析
### 1 、具体内容如下
```c
struct rockchip_pinctrl {
    struct regmap           *regmap_base;        // 基本寄存器映射指针
    int                     reg_size;            // 寄存器大小
    struct regmap           *regmap_pull;        // 拉取寄存器映射指针
    struct regmap           *regmap_pmu;         // 电源管理单元寄存器映射指针
    struct device           *dev;                // 设备指针
    struct rockchip_pin_ctrl *ctrl;              // 瑞芯微芯片引脚控制器指针
    struct pinctrl_desc     pctl;                // 引脚控制器描述符
    struct pinctrl_dev      *pctl_dev;           // 引脚控制器设备指针
    struct rockchip_pin_group *groups;           // 瑞芯微芯片引脚组指针
    unsigned int            ngroups;             // 引脚组数量
    struct rockchip_pmx_func *functions;         // 瑞芯微芯片引脚功能指针
    unsigned int            nfunctions;          // 引脚功能数量
};
```

### 2 、对最后四个结构体参数groups、ngroups、functions和nfunctions的具体作用进行讲解。(❤️)

- 1 存放groups和functions。


### 3 、pinctrl_register函数内容如下：(4<---3.2)
> 在pinctrl的probe函数中，首先定义了一个`struct rockchip_pinctrl *`类型的结构体指针类型的**变量info**，然后传入了rockchip_pinctrl_register函数，然后又分别传入了rockchip_pinctrl_parse_dt函数和devm_pinctrl_register函数。rockchip_pinctrl_parse_dt函数稍后再进行讲解，参数传入devm_pinctrl_register函数函数之后又**作为私有数据传入到了pinctrl_register函数**，pinctrl_register函数内容如下所示：

> 该函数的作用是**注册一个引脚控制设备，用pinctrl_dev来表示**，上面提到的私有数据会传输到pinctrl_init_controller函数进行初始化和构建pinctrl_dev结构体，然后跳转到pinctrl_init_controller的函数定义，具体内容如下所示：


```c
struct pinctrl_dev *pinctrl_register(struct pinctrl_desc *pctldesc,
				    struct device *dev, void *driver_data)
{
	struct pinctrl_dev *pctldev;
	int error;
 
	// 初始化pinctrl控制器
	pctldev = pinctrl_init_controller(pctldesc, dev, driver_data);
	if (IS_ERR(pctldev))
		return pctldev;
 
	// 启用pinctrl控制器
	error = pinctrl_enable(pctldev);
	if (error)
		return ERR_PTR(error);
 
	return pctldev;
}
```



### 4 、pinctrl_init_controller的函数定义(5<---4)
> 在该函数中我们要关注的是第19行内容**pctldev->driver_data = driver_data**，其中右值driver_data是从pinctrl函数的probe一步一步传递过来的，是一个`struct rockchip_pinctrl *类型的结构体指针变量`，左值**pctldev为要注册的引脚控制设备**（pin controller device），至此两个数据结构建立起了关联，可以通过pctldev来对rockchip_pinctrl中的数据进行访问。
> 


```c
static struct pinctrl_dev *pinctrl_init_controller(struct pinctrl_desc *pctldesc, struct device *dev,void *driver_data)
{
	struct pinctrl_dev *pctldev;
	int ret;
 
	if (!pctldesc)
		return ERR_PTR(-EINVAL);
	if (!pctldesc->name)
		return ERR_PTR(-EINVAL);
 
	pctldev = kzalloc(sizeof(*pctldev), GFP_KERNEL);
	if (!pctldev)
		return ERR_PTR(-ENOMEM);
 
	/* 初始化引脚控制设备结构体 */
	pctldev->owner = pctldesc->owner; // 设置所有者
	pctldev->desc = pctldesc; // 设置描述符
	pctldev->driver_data = driver_data; // 设置驱动程序数据
	INIT_RADIX_TREE(&pctldev->pin_desc_tree, GFP_KERNEL); // 初始化引脚描述符树
#ifdef CONFIG_GENERIC_PINCTRL_GROUPS
	INIT_RADIX_TREE(&pctldev->pin_group_tree, GFP_KERNEL); // 初始化引脚组树
#endif
#ifdef CONFIG_GENERIC_PINMUX_FUNCTIONS
	INIT_RADIX_TREE(&pctldev->pin_function_tree, GFP_KERNEL); // 初始化引脚功能树
#endif
	INIT_LIST_HEAD(&pctldev->gpio_ranges); // 初始化GPIO范围链表
	INIT_LIST_HEAD(&pctldev->node); // 初始化节点链表
	pctldev->dev = dev; // 设置设备指针
	mutex_init(&pctldev->mutex); // 初始化互斥锁
 
	/* 检查核心操作函数的有效性 */
	ret = pinctrl_check_ops(pctldev);
	if (ret) {
		dev_err(dev, "pinctrl ops lacks necessary functions\n");
		goto out_err;
	}
 
	/* 如果实现了引脚复用功能，检查操作函数的有效性 */
	if (pctldesc->pmxops) {
		ret = pinmux_check_ops(pctldev);
		if (ret)
			goto out_err;
	}
 
	/* 如果实现了引脚配置功能，检查操作函数的有效性 */
	if (pctldesc->confops) {
		ret = pinconf_check_ops(pctldev);
		if (ret)
			goto out_err;
	}
 
	/* 注册所有引脚 */
	dev_dbg(dev, "try to register %d pins ...\n",  pctldesc->npins);
	ret = pinctrl_register_pins(pctldev, pctldesc->pins, pctldesc->npins);
	if (ret) {
		dev_err(dev, "error during pin registration\n");
		pinctrl_free_pindescs(pctldev, pctldesc->pins,
				      pctldesc->npins);
		goto out_err;
	}
 
	return pctldev;
 
out_err:
	mutex_destroy(&pctldev->mutex);
	kfree(pctldev);
	return ERR_PTR(ret);
}
```
### 5、rockchip_pinctrl_parse_dt函数(3.1<---)

> （1）第10-14行：调用函数 rockchip_pinctrl_child_count，计算设备节点 np 的子节点数量，并更新 info 结构体中的计数器，最后打印function和组的数量。
> 
> （2）第17-22行：使用 devm_kcalloc 函数为函数分配内存空间，将函数数量乘以每个函数的大小 sizeof(struct rockchip_pmx_func)，并将指针保存在 info->functions 中。
> 
> （3）第24-29行：使用 devm_kcalloc 函数为组分配内存空间，将组数量乘以每个组的大小 sizeof(struct rockchip_pin_group)，并将指针保存在 info->groups 中。
> 
> （4）第33-46行使用 for_each_child_of_node 宏遍历设备节点 np 的每个子节点 child。如果节点 child 不是函数节点，则跳过当前节点，继续遍历下一个节点，**在每一个循环中调用函数 rockchip_pinctrl_parse_functions，解析函数信息，并将结果存储在 info 结构体中的相应位置。**


```c
static int rockchip_pinctrl_parse_dt(struct platform_device *pdev,
				     struct rockchip_pinctrl *info)
{
	struct device *dev = &pdev->dev;
	struct device_node *np = dev->of_node;
	struct device_node *child;
	int ret;
	int i;
 
	// 计算子节点数量并更新 info 结构体中的计数器
	rockchip_pinctrl_child_count(info, np);
 
	dev_dbg(&pdev->dev, "nfunctions = %d\n", info->nfunctions);
	dev_dbg(&pdev->dev, "ngroups = %d\n", info->ngroups);
 
	// 为函数和组分配内存空间
	info->functions = devm_kcalloc(dev,
				       info->nfunctions,
				       sizeof(struct rockchip_pmx_func),
				       GFP_KERNEL);
	if (!info->functions)
		return -ENOMEM;
 
	info->groups = devm_kcalloc(dev,
				    info->ngroups,
				    sizeof(struct rockchip_pin_group),
				    GFP_KERNEL);
	if (!info->groups)
		return -ENOMEM;
 
	i = 0;
 
	// 遍历每个子节点，解析函数信息
	for_each_child_of_node(np, child) {
		// 如果节点不是函数节点，则继续下一个节点
		if (!is_function_node(child))
			continue;
 
		// 解析函数信息并存储到 info 结构体中
		ret = rockchip_pinctrl_parse_functions(child, info, i++);
		if (ret) {
			dev_err(&pdev->dev, "failed to parse function\n");
			of_node_put(child);
			return ret;
		}
	}
 
	return 0;
}
```
### 6、rockchip_pinctrl_child_count函数进行讲解(4.1<---3.1)

> 在第一个小节中已经讲解了function和groups，在上面的函数中首先会遍历function，从而得到系统设备树中实际使用的function数量，保存到nfunctions参数中，而groups变量保存的是function中的引脚组数量，需要通过遍历function子节点来进行获取，到这里就可以确定rockchip_pinctrl 结构体中的**nfunctions用来记录function数量，ngroups用来记录groups数量。**


```c
static void rockchip_pinctrl_child_count(struct rockchip_pinctrl *info,
						struct device_node *np)
{
	struct device_node *child;
 
	// 遍历设备节点的子节点
	for_each_child_of_node(np, child) {
		// 如果子节点不是function节点，则跳过当前节点，继续遍历下一个节点
		if (!is_function_node(child))
			continue;
 
		// 子节点是function节点，增加function计数器
		info->nfunctions++;
 
		// 获取子节点的子节点数量，并增加到组计数器中
		info->ngroups += of_get_child_count(child);
	}
}
```



### 7、rockchip_pinctrl_parse_functions函数（4.2<---3.1）
> 第6-7行：定义了` struct rockchip_pmx_func *类型的变量func`和`struct rockchip_pin_group *类型的变量grp`，分别用来**存放function信息和groups信息**。
> 
> 第16行：将 info的functions地址赋值给了func，所以rockchip_pinctrl的functions参数的作用就是用来存放pinctrl设备树中的function信息。
> 
> 第37行：将 info的groups地址赋值给了grp，所以rockchip_pinctrl的groups参数的作用就是用来存放pinctrl设备树中的groups信息。
> 
> 在第40行：使用rockchip_pinctrl_parse_groups函数来解析组信息，并将结果存储到对应的组指针中。

```c
static int rockchip_pinctrl_parse_groups(struct device_node *np,
					      struct rockchip_pin_group *grp,
					      struct rockchip_pinctrl *info,
					      u32 index)
{
	struct rockchip_pin_bank *bank;
	int size;
	const __be32 *list;
	int num;
	int i, j;
	int ret;
 
	// 打印调试信息，显示正在解析的组节点和索引
	dev_dbg(info->dev, "group(%d): %pOFn\n", index, np);
 
	// 初始化组信息
	grp->name = np->name;
 
	/*
	 * 绑定格式为 rockchip,pins = <bank pin mux CONFIG>，
	 * 进行合法性检查并计算引脚数量
	 */
	list = of_get_property(np, "rockchip,pins", &size);
	// 对返回值不进行检查，因为传递的节点是安全的
	size /= sizeof(*list);
	if (!size || size % 4) {
		dev_err(info->dev, "wrong pins number or pins and configs should be by 4\n");
		return -EINVAL;
	}
 
	// 计算组的引脚数量
	grp->npins = size / 4;
 
	// 为组的引脚数组和数据数组分配内存空间
	grp->pins = devm_kcalloc(info->dev, grp->npins, sizeof(unsigned int),
						GFP_KERNEL);
	grp->data = devm_kcalloc(info->dev,
					grp->npins,
					sizeof(struct rockchip_pin_config),
					GFP_KERNEL);
	if (!grp->pins || !grp->data)
		return -ENOMEM;
 
	// 遍历列表中的每个元素，每4个元素表示一个引脚的信息
	for (i = 0, j = 0; i < size; i += 4, j++) {
		const __be32 *phandle;
		struct device_node *np_config;
 
		// 获取管脚号
		num = be32_to_cpu(*list++);
		bank = bank_num_to_bank(info, num);
		if (IS_ERR(bank))
			return PTR_ERR(bank);
 
		// 计算引脚编号
		grp->pins[j] = bank->pin_base + be32_to_cpu(*list++);
		// 获取引脚对应的功能选择值
		grp->data[j].func = be32_to_cpu(*list++);
 
		// 获取与引脚相关的配置信息
		phandle = list++;
		if (!phandle)
			return -EINVAL;
 
		// 通过句柄查找配置节点
		np_config = of_find_node_by_phandle(be32_to_cpup(phandle));
		// 解析配置信息，并将结果存储到组的数据数组中
		ret = pinconf_generic_parse_dt_config(np_config, NULL,
				&grp->data[j].configs, &grp->data[j].nconfigs);
		if (ret)
			return ret;
	}
 
	return 0;
}
```

### 8、rockchip_pinctrl_parse_groups函数的定义(5<---4.2)\
- 1 解析组信息，并将结果存储到对应的组指针中。

> 第17行：初始化组信息，将引脚组的名称设置为节点的名称。
> 
> 第23-29行：通过of_get_property函数获取引脚组节点的属性"rockchip,pins"的值，该属性的格式为"bank pin mux CONFIG"。对返回的属性值进行合法性检查，并计算引脚数量。如果属性值为空或者数量不是4的倍数，将返回错误代码EINVAL。
> 
> 第31-42行：首先计算得到的引脚数量，然后根据计算得到的引脚数量为引脚数组和数据数组分配内存空间，这些数组将用于存储引脚的编号和相关的配置信息。如果内存分配失败，函数将返回错误代码ENOMEM。
> 
> 第45行：遍历属性值列表中的每个元素，每4个元素表示一个引脚的信息。
> 
> 第50-53行：首先从列表中获取银行号，并使用bank_num_to_bank函数将引脚号转换为对应的引脚结构体指针。如果转换失败，函数将返回相应的错误代码。
> 
> 第56行：根据引脚结构体中的引脚基地址（pin_base）和列表中的值计算引脚的编号，并将其存储在引脚数组（grp->pins）中。
> 
> 第58行：从列表中获取与当前引脚相关的功能选择值，并将其存储在数据数组（grp->data）中的相应位置。
> 
> 第60-72行从列表中获取与当前引脚相关的配置信息的句柄，并通过该句柄查找对应的配置节点（np_config）。然后，函数使用pinconf_generic_parse_dt_config解析配置信息，并将解析结果存储在数据数组的相应位置。
> 

```c
static int rockchip_pinctrl_parse_groups(struct device_node *np,
					      struct rockchip_pin_group *grp,
					      struct rockchip_pinctrl *info,
					      u32 index)
{
	struct rockchip_pin_bank *bank;
	int size;
	const __be32 *list;
	int num;
	int i, j;
	int ret;
 
	// 打印调试信息，显示正在解析的组节点和索引
	dev_dbg(info->dev, "group(%d): %pOFn\n", index, np);
 
	// 初始化组信息
	grp->name = np->name;
 
	/*
	 * 绑定格式为 rockchip,pins = <bank pin mux CONFIG>，
	 * 进行合法性检查并计算引脚数量
	 */
	list = of_get_property(np, "rockchip,pins", &size);
	// 对返回值不进行检查，因为传递的节点是安全的
	size /= sizeof(*list);
	if (!size || size % 4) {
		dev_err(info->dev, "wrong pins number or pins and configs should be by 4\n");
		return -EINVAL;
	}
 
	// 计算组的引脚数量
	grp->npins = size / 4;
 
	// 为组的引脚数组和数据数组分配内存空间
	grp->pins = devm_kcalloc(info->dev, grp->npins, sizeof(unsigned int),
						GFP_KERNEL);
	grp->data = devm_kcalloc(info->dev,
					grp->npins,
					sizeof(struct rockchip_pin_config),
					GFP_KERNEL);
	if (!grp->pins || !grp->data)
		return -ENOMEM;
 
	// 遍历列表中的每个元素，每4个元素表示一个引脚的信息
	for (i = 0, j = 0; i < size; i += 4, j++) {
		const __be32 *phandle;
		struct device_node *np_config;
 
		// 获取管脚号
		num = be32_to_cpu(*list++);
		bank = bank_num_to_bank(info, num);
		if (IS_ERR(bank))
			return PTR_ERR(bank);
 
		// 计算引脚编号
		grp->pins[j] = bank->pin_base + be32_to_cpu(*list++);
		// 获取引脚对应的功能选择值
		grp->data[j].func = be32_to_cpu(*list++);
 
		// 获取与引脚相关的配置信息
		phandle = list++;
		if (!phandle)
			return -EINVAL;
 
		// 通过句柄查找配置节点
		np_config = of_find_node_by_phandle(be32_to_cpup(phandle));
		// 解析配置信息，并将结果存储到组的数据数组中
		ret = pinconf_generic_parse_dt_config(np_config, NULL,
				&grp->data[j].configs, &grp->data[j].nconfigs);
		if (ret)
			return ret;
	}
 
	return 0;
}
```





# 三、函数操作集的具体实现

## rockchip_pinctrl_register函数填充
### 1 、在rockchip_pinctrl_register函数中对三个函数操作集进行了填充(❤️)
- 1 内核源码目录下的“/drivers/pinctrl/pinctrl-rockchip.c”文件

```c
ctrldesc->pctlops = &rockchip_pctrl_ops;
ctrldesc->pmxops = &rockchip_pmx_ops;
ctrldesc->confops = &rockchip_pinconf_ops;
```

### 2 、简单的了解即可


### 3 、

## pinctrl_ops

### 4 、瑞芯微在源码中实现了其中五个函数：
```c
static const struct pinctrl_ops rockchip_pctrl_ops = {
	.get_groups_count	= rockchip_get_groups_count,	// 获取引脚组数量的函数
	.get_group_name		= rockchip_get_group_name,// 获取引脚组名称的函数
	.get_group_pins		= rockchip_get_group_pins,// 获取引脚组引脚列表的函数
	.dt_node_to_map		= rockchip_dt_node_to_map,// 将设备树节点转换为引脚控制器映射的函数
	.dt_free_map		= rockchip_dt_free_map,		// 释放引脚控制器映射资源的函数
};
```



### 5、rockchip_get_groups_count
```c
static int rockchip_get_groups_count(struct pinctrl_dev *pctldev)
{
	// 从 pinctrl_dev 结构中获取私有数据指针，将其转换为 rockchip_pinctrl 结构
	struct rockchip_pinctrl *info = pinctrl_dev_get_drvdata(pctldev);
 
	// 返回 rockchip_pinctrl 结构中存储的引脚组数量
	return info->ngroups;
}
```

### 6、rockchip_get_group_name
```c
static const char *rockchip_get_group_name(struct pinctrl_dev *pctldev,
							unsigned selector)
{
	// 从 pinctrl_dev 结构中获取私有数据指针，将其转换为 rockchip_pinctrl 结构
	struct rockchip_pinctrl *info = pinctrl_dev_get_drvdata(pctldev);
 
	// 返回指定引脚组的名称
	return info->groups[selector].name;
}
```

### 7、rockchip_get_group_pins
```c
static int rockchip_get_group_pins(struct pinctrl_dev *pctldev,
				      unsigned selector, const unsigned **pins,
				      unsigned *npins)
{
	// 从 pinctrl_dev 结构中获取私有数据指针，将其转换为 rockchip_pinctrl 结构
	struct rockchip_pinctrl *info = pinctrl_dev_get_drvdata(pctldev);
 
	// 如果选择器超出引脚组的范围，则返回错误码 -EINVAL
	if (selector >= info->ngroups)
		return -EINVAL;
 
	// 将指向引脚组的引脚数组的指针赋值给传入的 pins 指针
	*pins = info->groups[selector].pins;
	// 将引脚组中的引脚数量赋值给传入的 npins 变量
	*npins = info->groups[selector].npins;
 
	// 返回成功的状态码 0
	return 0;
}
```

### 8、rockchip_dt_node_to_map  (❤️)
```c
static int rockchip_dt_node_to_map(struct pinctrl_dev *pctldev,
				 struct device_node *np,
				 struct pinctrl_map **map, unsigned *num_maps)
{
struct rockchip_pinctrl *info = pinctrl_dev_get_drvdata(pctldev); // 获取引脚控制器的私有数据指针
	const struct rockchip_pin_group *grp; // 引脚组指针
	struct device *dev = info->dev; // 设备指针
	struct pinctrl_map *new_map; // 新的引脚映射数组
	struct device_node *parent; // 父节点指针
	int map_num = 1; // 映射数量，默认为1
	int i;
 
	/* 查找引脚组 */
	grp = pinctrl_name_to_group(info, np->name); // 根据节点名称查找对应的引脚组
	if (!grp) {
		dev_err(dev, "unable to find group for node %pOFn\n", np); // 如果找不到引脚组，打印错误信息
		return -EINVAL;
	}
 
	map_num += grp->npins; // 计算映射数量，包括复用映射和配置映射
 
	new_map = kcalloc(map_num, sizeof(*new_map), GFP_KERNEL); // 分配内存空间用于存储映射数组
	if (!new_map)
		return -ENOMEM;
 
	*map = new_map; // 将分配的映射数组赋值给输出参数
	*num_maps = map_num; // 将映射数量赋值给输出参数
 
	/* 创建复用映射 */
	parent = of_get_parent(np); // 获取节点的父节点
	if (!parent) {
		kfree(new_map); // 如果父节点不存在，释放分配的映射数组内存空间
		return -EINVAL;
	}
	new_map[0].type = PIN_MAP_TYPE_MUX_GROUP; // 设置映射类型为复用映射
	new_map[0].data.mux.function = parent->name; // 复用功能名称为父节点的名称
	new_map[0].data.mux.group = np->name; // 引脚组名称为节点的名称
	of_node_put(parent); // 释放父节点的引用计数
 
	/* 创建配置映射 */
	new_map++; // 映射数组指针向后移动一个位置
	for (i = 0; i < grp->npins; i++) {
		new_map[i].type = PIN_MAP_TYPE_CONFIGS_PIN; // 设置映射类型为配置映射
		new_map[i].data.configs.group_or_pin =
			pin_get_name(pctldev, grp->pins[i]); // 引脚组或引脚名称为引脚组中的引脚名称
		new_map[i].data.configs.configs = grp->data[i].configs; // 配置信息数组为引脚组中该引脚的配置信息
		new_map[i].data.configs.num_configs = grp->data[i].nconfigs; // 配置信息数量为引脚组中该引脚的配置数量
	}
 
	dev_dbg(dev, "maps: function %s group %s num %d\n",
		(*map)->data.mux.function, (*map)->data.mux.group, map_num); // 打印调试信息，显示创建的引脚映射的功能名称、组名和数量
 
	return 0; // 返回成功标志
}
```


### 9、rockchip_dt_free_map

```c
static void rockchip_dt_free_map(struct pinctrl_dev *pctldev,
				    struct pinctrl_map *map, unsigned num_maps)
{
	kfree(map);  // 释放引脚控制器映射的内存块
}
```

## pinmux_ops
### 1 、实现了其中的四个函数：
```c
static const struct pinmux_ops rockchip_pmx_ops = {
	.get_functions_count	= rockchip_pmx_get_funcs_count,// 获取引脚复用功能数量的函数
	.get_function_name	= rockchip_pmx_get_func_name,	// 获取引脚复用功能名称的函数
	.get_function_groups	= rockchip_pmx_get_groups,// 获取引脚复用功能对应的引脚组的函数
	.set_mux		= rockchip_pmx_set,			// 设置引脚复用功能的函数
};
```


### 2 、rockchip_pmx_get_funcs_count
```c
static int rockchip_pmx_get_funcs_count(struct pinctrl_dev *pctldev)
{
	struct rockchip_pinctrl *info = pinctrl_dev_get_drvdata(pctldev);
 
	return info->nfunctions;  // 返回引脚复用功能的数量
}
```



### 3 、rockchip_pmx_get_func_name
```c
static const char *rockchip_pmx_get_func_name(struct pinctrl_dev *pctldev,
					  unsigned selector)
{
	struct rockchip_pinctrl *info = pinctrl_dev_get_drvdata(pctldev);
 
	return info->functions[selector].name;  // 返回引脚复用功能的名称
}
```


### 4 、rockchip_pmx_get_groups
```c
static int rockchip_pmx_get_groups(struct pinctrl_dev *pctldev,
				unsigned selector, const char * const **groups,
				unsigned * const num_groups)
{
	struct rockchip_pinctrl *info = pinctrl_dev_get_drvdata(pctldev);
 
	*groups = info->functions[selector].groups;  // 返回引脚复用功能对应的引脚组数组
	*num_groups = info->functions[selector].ngroups;  // 返回引脚组的数量
 
	return 0;  // 返回成功
}
```

### 5、rockchip_pmx_set(❤️)
```c
static int rockchip_pmx_set(struct pinctrl_dev *pctldev, unsigned selector,
		    unsigned group)
{
	struct rockchip_pinctrl *info = pinctrl_dev_get_drvdata(pctldev);
	const unsigned int *pins = info->groups[group].pins;
	const struct rockchip_pin_config *data = info->groups[group].data;
	struct device *dev = info->dev;
	struct rockchip_pin_bank *bank;
	int cnt, ret = 0;
 
	dev_dbg(dev, "enable function %s group %s\n",
		info->functions[selector].name, info->groups[group].name);
 
	/*
	 * 针对所选的引脚组中的每个引脚，将相应的引脚功能号码编程到配置寄存器中。
	 */
	for (cnt = 0; cnt < info->groups[group].npins; cnt++) {
		bank = pin_to_bank(info, pins[cnt]);
		ret = rockchip_set_mux(bank, pins[cnt] - bank->pin_base,
				       data[cnt].func);
		if (ret)
			break;
	}
 
	if (ret && cnt) {
		/* 恢复已经设置的引脚设置 */
		for (cnt--; cnt >= 0 && !data[cnt].func; cnt--)
			rockchip_set_mux(bank, pins[cnt] - bank->pin_base, 0);
 
		return ret;
	}
 
	return 0;  // 返回成功
}
```

### 6、




## pinconf_ops
### 1 、源码中实现了其中两个函数：
```c
static const struct pinconf_ops rockchip_pinconf_ops = {
	.pin_config_get		= rockchip_pinconf_get,	// 获取引脚配置的函数
	.pin_config_set		= rockchip_pinconf_set,	// 设置引脚配置的函数
	.is_generic			= true,	// 表示是通用的引脚配置操作
};
```


### 2 、rockchip_pinconf_set(❤️)
```c
static int rockchip_pinconf_set(struct pinctrl_dev *pctldev, unsigned int pin,
				unsigned long *configs, unsigned num_configs)
{
	struct rockchip_pinctrl *info = pinctrl_dev_get_drvdata(pctldev);
	struct rockchip_pin_bank *bank = pin_to_bank(info, pin);
	struct gpio_chip *gpio = &bank->gpio_chip;
	enum pin_config_param param;
	u32 arg;
	int i;
	int rc;
 
	for (i = 0; i < num_configs; i++) {
		param = pinconf_to_config_param(configs[i]);
		arg = pinconf_to_config_argument(configs[i]);
 
		if (param == PIN_CONFIG_OUTPUT || param == PIN_CONFIG_INPUT_ENABLE) {
			/*
			 * 检查 GPIO 驱动程序是否已经探测到。
			 * 锁定确保 GPIO 探测完成或者 GPIO 驱动程序尚未探测到。
			 */
			mutex_lock(&bank->deferred_lock);
			if (!gpio || !gpio->direction_output) {
				// 如果驱动程序尚未探测到，则将配置信息延迟处理并返回。
				rc = rockchip_pinconf_defer_pin(bank, pin - bank->pin_base, param, arg);
				mutex_unlock(&bank->deferred_lock);
				if (rc)
					return rc;
 
				break;
			}
			mutex_unlock(&bank->deferred_lock);
		}
 
		switch (param) {
		case PIN_CONFIG_BIAS_DISABLE:
			// 禁用上下拉电阻
			rc = rockchip_set_pull(bank, pin - bank->pin_base, param);
			if (rc)
				return rc;
			break;
		case PIN_CONFIG_BIAS_PULL_UP:
		case PIN_CONFIG_BIAS_PULL_DOWN:
		case PIN_CONFIG_BIAS_PULL_PIN_DEFAULT:
		case PIN_CONFIG_BIAS_BUS_HOLD:
			// 检查上下拉电阻是否有效
			if (!rockchip_pinconf_pull_valid(info->ctrl, param))
				return -ENOTSUPP;
 
			if (!arg)
				return -EINVAL;
 
			// 设置上下拉电阻
			rc = rockchip_set_pull(bank, pin - bank->pin_base, param);
			if (rc)
				return rc;
			break;
		case PIN_CONFIG_OUTPUT:
			// 设置引脚复用功能为 GPIO
			rc = rockchip_set_mux(bank, pin - bank->pin_base, RK_FUNC_GPIO);
			if (rc != RK_FUNC_GPIO)
				return -EINVAL;
 
			// 设置引脚为输出模式
			rc = gpio->direction_output(gpio, pin - bank->pin_base, arg);
			if (rc)
				return rc;
			break;
		case PIN_CONFIG_INPUT_ENABLE:
			// 设置引脚复用功能为 GPIO
			rc = rockchip_set_mux(bank, pin - bank->pin_base, RK_FUNC_GPIO);
			if (rc != RK_FUNC_GPIO)
				return -EINVAL;
 
			// 设置引脚为输入模式
			rc = gpio->direction_input(gpio, pin - bank->pin_base);
			if (rc)
				return rc;
			break;
		case PIN_CONFIG_DRIVE_STRENGTH:
			// 仅支持某些芯片（如 rk3288）的每个引脚独立的驱动强度设置
			if (!info->ctrl->drv_calc_reg)
				return -ENOTSUPP;
 
			// 设置引脚的驱动强度
			rc = rockchip_set_drive_perpin(bank, pin - bank->pin_base, arg);
			if (rc < 0)
				return rc;
			break;
		case PIN_CONFIG_INPUT_SCHMITT_ENABLE:
			// 仅支持某些芯片的施密特触发设置
			if (!info->ctrl->schmitt_calc_reg)
				return -ENOTSUPP;
 
			// 设置引脚的施密特触发模式
			rc = rockchip_set_schmitt(bank, pin - bank->pin_base, arg);
			if (rc < 0)
				return rc;
			break;
		case PIN_CONFIG_SLEW_RATE:
			// 仅支持某些芯片的引脚驱动速率设置
			if (!info->ctrl->slew_rate_calc_reg)
				return -ENOTSUPP;
 
			// 设置引脚的驱动速率
			rc = rockchip_set_slew_rate(bank, pin - bank->pin_base, arg);
			if (rc < 0)
				return rc;
			break;
		default:
			// 不支持的配置参数
			return -ENOTSUPP;
		}
	} /* for each config */
 
	return 0;
}
```

### 3 、rockchip_pinconf_get
```c
/* 获取指定引脚的配置设置 */
static int rockchip_pinconf_get(struct pinctrl_dev *pctldev, unsigned int pin,
				unsigned long *config)
{
	struct rockchip_pinctrl *info = pinctrl_dev_get_drvdata(pctldev);
	struct rockchip_pin_bank *bank = pin_to_bank(info, pin);
	struct gpio_chip *gpio = &bank->gpio_chip;
	enum pin_config_param param = pinconf_to_config_param(*config);
	u16 arg;
	int rc;
 
	switch (param) {
	case PIN_CONFIG_BIAS_DISABLE:
		// 检查上下拉电阻是否禁用
		if (rockchip_get_pull(bank, pin - bank->pin_base) != param)
			return -EINVAL;
 
		arg = 0;
		break;
	case PIN_CONFIG_BIAS_PULL_UP:
	case PIN_CONFIG_BIAS_PULL_DOWN:
	case PIN_CONFIG_BIAS_PULL_PIN_DEFAULT:
	case PIN_CONFIG_BIAS_BUS_HOLD:
		// 检查上下拉电阻是否有效，并获取当前的上下拉电阻配置
		if (!rockchip_pinconf_pull_valid(info->ctrl, param))
			return -ENOTSUPP;
 
		if (rockchip_get_pull(bank, pin - bank->pin_base) != param)
			return -EINVAL;
 
		arg = 1;
		break;
	case PIN_CONFIG_OUTPUT:
		// 检查引脚是否配置为 GPIO 输出模式
		rc = rockchip_get_mux(bank, pin - bank->pin_base);
		if (rc != RK_FUNC_GPIO)
			return -EINVAL;
 
		if (!gpio || !gpio->get) {
			arg = 0;
			break;
		}
 
		// 获取引脚的输出状态
		rc = gpio->get(gpio, pin - bank->pin_base);
		if (rc < 0)
			return rc;
 
		arg = rc ? 1 : 0;
		break;
	case PIN_CONFIG_DRIVE_STRENGTH:
		// 仅支持某些芯片（如 rk3288）的每个引脚独立的驱动强度设置
		if (!info->ctrl->drv_calc_reg)
			return -ENOTSUPP;
 
		// 获取引脚的驱动强度配置
		rc = rockchip_get_drive_perpin(bank, pin - bank->pin_base);
		if (rc < 0)
			return rc;
 
		arg = rc;
		break;
	case PIN_CONFIG_INPUT_SCHMITT_ENABLE:
		// 仅支持某些芯片的施密特触发设置
		if (!info->ctrl->schmitt_calc_reg)
			return -ENOTSUPP;
 
		// 获取引脚的施密特触发配置
		rc = rockchip_get_schmitt(bank, pin - bank->pin_base);
		if (rc < 0)
			return rc;
 
		arg = rc;
		break;
	case PIN_CONFIG_SLEW_RATE:
		// 仅支持某些芯片的引脚驱动速率设置
		if (!info->ctrl->slew_rate_calc_reg)
			return -ENOTSUPP;
 
		// 获取引脚的驱动速率配置
		rc = rockchip_get_slew_rate(bank, pin - bank->pin_base);
		if (rc < 0)
			return rc;
 
		arg = rc;
		break;
	default:
		// 不支持的配置参数
		return -ENOTSUPP;
	}
 
	*config = pinconf_to_config_packed(param, arg);
 
	return 0;
}
```


### 4 、






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


