---
title: "{{title}}"
aliases: 
tags: 
description: 
source:
---

# 备注(声明)：

## 思维导图：
[[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十一期_pinctrl子系统/canvas/1-pinctrl-probe 流程分析.canvas|1-pinctrl-probe 流程分析]]



# 参考文章：


```cardlink
url: https://blog.csdn.net/BeiJingXunWei/article/details/135553025?spm=1001.2101.3001.10796
title: "RK3568驱动指南｜第十一篇 pinctrl 子系统-第123章dt_node_to_map函数分析_rockchip-pinctrl pinctrl: unable to find group for-CSDN博客"
description: "文章浏览阅读1.3k次，点赞21次，收藏26次。设备树（Device Tree）中存放的是对硬件设备信息的描述，包含了硬件设备的配置和连接信息，例如在pinctrl节点中的引脚的配置和映射关系。而rockchip_dt_node_to_map 函数的作用就是根据设备树中的节点信息，生成对应的引脚映射数组。函数设置映射的类型为PIN_MAP_TYPE_CONFIGS_PIN，并将引脚的名称作为映射的数据。然后，函数设置第一个映射的类型为PIN_MAP_TYPE_MUX_GROUP，并将父节点的名称作为映射的数据。同时，将设备节点的名称作为映射的组名。_rockchip-pinctrl pinctrl: unable to find group for node"
host: blog.csdn.net
```



# 一、dt_node_to_map函数分析

## 函数功能：
### 1 、根据设备树中的节点信息，生成对应的引脚映射数组(❤️)



### 2 、这个映射数组将描述硬件功能（如复用功能和配置信息）与设备树中的引脚信息进行绑定。




### 3 、

## dt_node_to_map函数详细的介绍

### 4 、实现在内核源码的“drivers/pinctrl/pinctrl-rockchip.c”文件中



### 5、struct pinctrl_map 你结构体介绍
- 1 内核源码的“include/linux/pinctrl/machine.h”目录下

> 该结构体用于**在引脚控制器中定义引脚的映射关系**。通过映射类型的不同，可以将引脚与具体的复用功能或配置信息关联起来，从而实现引脚的配置和控制。

```c
struct pinctrl_map {
	const char *dev_name;       // 设备名称
	const char *name;           // 映射名称
	enum pinctrl_map_type type; // 映射类型
	const char *ctrl_dev_name;  // 控制设备名称
	union {
		struct pinctrl_map_mux mux;         // 复用映射数据
		struct pinctrl_map_configs configs; // 配置映射数据
	} data;
};
```


### 6、函数定义如下：

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


### 7、函数详解：(❤️)
> 第14-20行：函数根据设备节点的名称使用pinctrl_name_to_group函数**查找与该节点对应的引脚组**。如果找不到引脚组，则函数打印错误消息并返回EINVAL错误代码。
> 
> 第22行：函数**根据引脚组的引脚数量计算需要创建的映射数量**。映射数量包括复用映射和配置映射。
> 
> 第24-26行：函数使用kcalloc函数为映射数组（new_map）分配内存空间。分配的大小为映射数量乘以每个映射的大小。如果内存分配失败，函数将返回ENOMEM错误代码。
> 
> 第28-29行：函数将分配的映射数组（new_map）和映射数量（map_num）通过输出参数map和num_maps返回给调用者。
> 
> 第31-40行：函数首先获取设备节点的**父节点，并将其作为复用映射的功能名称**。然后，函数设置第一个映射的类型为PIN_MAP_TYPE_MUX_GROUP，并将父节点的名称作为映射的数据。同时，**将设备节点的名称作为映射的组名**。最后，函数使用of_node_put释放父节点的引用计数。
> 
> 第42-52行：函数**遍历引脚组的引脚数组**，并**为每个引脚创建一个配置映射**。函数设置映射的类型为PIN_MAP_TYPE_CONFIGS_PIN，并将引脚的名称作为映射的数据。同时，将引脚组中该引脚的配置信息和配置数量设置为映射的配置数据。函数使用pin_get_name函数获取引脚的名称。
> 
> rockchip_dt_node_to_map函数**根据设备节点的信息创建引脚映射，包括复用映射和配置映射**。复用映射用于将引脚组的功能与父节点的功能关联起来，而配置映射用于将引脚的配置信息与引脚的名称关联起来。这些映射将用于配置引脚控制器，以确保引脚在系统中正确地配置和使用。这个函数在设备树解析过程中被调用，以便为每个设备节点创建相应的引脚映射。


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


