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
url: https://blog.csdn.net/BeiJingXunWei/article/details/135556463?spm=1001.2101.3001.10796
title: "RK3568驱动指南｜第十一篇 pinctrl 子系统-第125章 add_setting函数分析_rk3568 settings目录-CSDN博客"
description: "文章浏览阅读1k次，点赞15次，收藏22次。本文详细介绍了瑞芯微RK3568芯片的特性，如处理器、图形处理器、接口支持和AI能力，并深入剖析了Linux内核中的create_pinctrl和add_setting函数，关注于设备树映射和pincontrol系统的设置过程。"
host: blog.csdn.net
```



# 一、add_setting函数分析

## create_pinctrl函数解析(上一章未讲解完)
### 1 、函数的具体内容如下(1--->)

```c
static struct pinctrl *create_pinctrl(struct device *dev,
				      struct pinctrl_dev *pctldev)
{
	struct pinctrl *p;
	const char *devname;
	struct pinctrl_maps *maps_node;
	int i;
	const struct pinctrl_map *map;
	int ret;
 
	/*
	 * 为每个映射创建状态 cookie 持有者 struct pinctrl。
	 * 这是当使用 pinctrl_get() 请求引脚控制句柄时消费者将获得的对象。
	 */
	p = kzalloc(sizeof(*p), GFP_KERNEL);
	if (!p)
		return ERR_PTR(-ENOMEM);
	p->dev = dev;
	INIT_LIST_HEAD(&p->states);
	INIT_LIST_HEAD(&p->dt_maps);
 
	ret = pinctrl_dt_to_map(p, pctldev);
	if (ret < 0) {
		kfree(p);
		return ERR_PTR(ret);
	}
 
	devname = dev_name(dev);
 
	mutex_lock(&pinctrl_maps_mutex);
	/* 遍历引脚控制映射以定位正确的映射 */
	for_each_maps(maps_node, i, map) {
		/* 映射必须适用于此设备 */
		if (strcmp(map->dev_name, devname))
			continue;
		/*
		 * 如果 pctldev 不为空，我们正在声明它的独占使用权，
		 * 这意味着它自己提供了该设置。
		 *
		 * 因此，我们必须跳过适用于此设备但由其他设备提供的映射。
		 */
		if (pctldev &&
		    strcmp(dev_name(pctldev->dev), map->ctrl_dev_name))
			continue;
 
		ret = add_setting(p, pctldev, map);
		/*
		 * 在这一点上，添加设置可能会导致：
		 *
		 * - 延迟，如果引脚控制设备尚不可用
		 * - 失败，如果引脚控制设备尚不可用，
		 *   并且该设置是一个独占设置。我们不能推迟它，因为
		 *   该独占设置会在设备注册后立即生效。
		 *
		 * 如果返回的错误不是 -EPROBE_DEFER，则我们将
		 * 累积错误，以查看是否最终得到 -EPROBE_DEFER，
		 * 因为那是最糟糕的情况。
		 */
		if (ret == -EPROBE_DEFER) {
			pinctrl_free(p, false);
			mutex_unlock(&pinctrl_maps_mutex);
			return ERR_PTR(ret);
		}
	}
	mutex_unlock(&pinctrl_maps_mutex);
 
	if (ret < 0) {
		/* 如果发生了除推迟以外的其他错误，则在此处返回 */
		pinctrl_free(p, false);
		return ERR_PTR(ret);
	}
 
	kref_init(&p->users);
 
	/* 将引脚控制句柄添加到全局列表 */
	mutex_lock(&pinctrl_list_mutex);
	list_add_tail(&p->node, &pinctrl_list);
	mutex_unlock(&pinctrl_list_mutex);
 
	return p;
}
```

- 1 第32行使用for_each_maps宏定义对引脚控制映射进行了遍历

### 2 、for_each_maps宏定义：对引脚控制映射进行了遍历
- 1 定义在内核源码目录下的“drivers/pinctrl/core.h”文件中

```c
// 宏定义：用于遍历映射表链表中的每个映射表条目
// _maps_node_: 遍历时使用的映射表节点指针
// _i_: 遍历时使用的计数器变量
// _map_: 遍历时使用的映射表条目指针
#define for_each_maps(_maps_node_, _i_, _map_) \
	list_for_each_entry(_maps_node_, &pinctrl_maps, node) \ // 遍历映射表链表中的每个节点
		for (_i_ = 0, _map_ = &_maps_node_->maps[_i_]; \ // 初始化计数器和映射表条目指针
			_i_ < _maps_node_->num_maps; \ // 循环条件：计数器小于当前节点的映射表数量
			_i_++, _map_ = &_maps_node_->maps[_i_]) // 每次循环增加计数器并更新映射表条目指针
```

> 在遍历过程中，首先会**检查映射的设备名称**是否与当前设备的名称匹配，如果不匹配则跳过。当检查 pctldev 不为空且映射是为 pctldev 提供的，则跳过该映射。



### 3 、add_setting函数：将映射添加到引脚控制器中(2<---)

#### 将传入的map参数值传入到pinctrl_setting类型的变量中(❤️)
- 1 从而进一步提取pinctrl_map结构体类型变量中的内容。

```c
static int add_setting(struct pinctrl *p, struct pinctrl_dev *pctldev,
		       const struct pinctrl_map *map)
{
	struct pinctrl_state *state; // 状态对象指针
	struct pinctrl_setting *setting; // 设置对象指针
	int ret;
 
	// 查找状态对象，如果不存在则创建新的状态对象
	state = find_state(p, map->name);
	if (!state)
		state = create_state(p, map->name);
	if (IS_ERR(state))
		return PTR_ERR(state);
 
	// 如果映射类型为虚拟状态映射类型，直接返回
	if (map->type == PIN_MAP_TYPE_DUMMY_STATE)
		return 0;
 
	// 分配设置对象的内存空间
	setting = kzalloc(sizeof(*setting), GFP_KERNEL);
	if (!setting)
		return -ENOMEM;
 
	setting->type = map->type; // 设置设置对象的映射类型
 
	// 设置设置对象的引脚控制设备
	if (pctldev)
		setting->pctldev = pctldev;
	else
		setting->pctldev =
			get_pinctrl_dev_from_devname(map->ctrl_dev_name);
	if(!setting->pctldev) {
		kfree(setting);
		// 如果引脚控制设备不存在，返回错误
		// 注意：不推迟探测 hogs（循环依赖）
		if (!strcmp(map->ctrl_dev_name, map->dev_name))
			return -ENODEV;
		/*
		 * 好吧，我们假设驱动程序目前不存在，
		 * 让我们将获取此 pinctrl 句柄推迟到以后...
		 */
		dev_info(p->dev, "unknown pinctrl device %s in map entry, deferring probe",
			map->ctrl_dev_name);
		return -EPROBE_DEFER;
	}
 
	// 设置设置对象的设备名称
	setting->dev_name = map->dev_name;
 
	switch (map->type) {
	case PIN_MAP_TYPE_MUX_GROUP:
		// 对于复用组映射类型，执行引脚复用映射到设置对象的转换
		ret = pinmux_map_to_setting(map, setting);
		break;
	case PIN_MAP_TYPE_CONFIGS_PIN:
	case PIN_MAP_TYPE_CONFIGS_GROUP:
		// 对于配置映射类型，执行引脚配置映射到设置对象的转换
		ret = pinconf_map_to_setting(map, setting);
		break;
	default:
		ret = -EINVAL;
		break;
	}
	if (ret < 0) {
		kfree(setting);
		return ret;
	}
 
	// 将设置对象插入状态对象的设置链表末尾
	list_add_tail(&setting->node, &state->settings);
 
	return 0;
}
```

#### 函数解析：(❤️)

> 第4-5行：分别定义了一个`struct pinctrl_state *类型的状态对象指针`和`struct pinctrl_setting *的设置对象指针`
> 
> （2）第8-13行：根据映射表条目的名称，使用find_state函数在引脚控制器对象中查找对应的状态对象，在此之前我们并没有设置状态对象，所以会进入到第二个if判断，使用**create_state函数创建新的状态对象**。

> （3）第15-17行：如果映射类型为虚拟状态映射类型（PIN_MAP_TYPE_DUMMY_STATE），直接返回成功。
> 
> （4）第19-22行：分配一个设置对象的内存空间。
> 
> （5）第24行：设置对象的映射类型为映射表条目中定义的类型。
> 
> （6）第26-56行：根据情况设置设置对象的引脚控制设备：
> 
> ·如果pctldev 参数为非空，则将其设置为设置对象的引脚控制设备。
> 
> ·如果 pctldev 参数为空，则根据映射表条目中的ctrl_dev_name，使用get_pinctrl_dev_from_devname 函数获取引脚控制设备对象，并将其设置为设置对象的引脚控制设备。
> 
> ·如果获取的引脚控制设备对象为空，说明引脚控制设备不存在，释放设置对象的内存空间并返回错误。如果 ctrl_dev_name 与 dev_name 相同，表示映射表条目中的设备名称与控制设备名称相同，返回错误码 -ENODEV。如果不相同，表示引脚控制设备目前不存在，打印一条信息并返回错误码-EPROBE_DEFER，表示推迟探测引脚控制设备。
> 
> （7）第48行：设置设置对象的设备名称为映射表条目中的dev_name。
> 
> （8）第50-63行：根据设置对象的映射类型执行相应的映射转换操作：
> 
> ·对于`复用组映射类型（PIN_MAP_TYPE_MUX_GROUP）`，调用**pinmux_map_to_setting 函数执行引脚复用映射到设置对象的转换。**
> 
> ·对于`配置映射类型（PIN_MAP_TYPE_CONFIGS_PIN 或PIN_MAP_TYPE_CONFIGS_GROUP）`，调用 **pinconf_map_to_setting 函数执行引脚配置映射到设置对象的转换。**
> 
> 对于其他映射类型，返回错误码 -EINVAL。
> 
> （9）第64行：如果映射转换操作失败（返回值小于0），释放设置对象的内存空间并返回错误码。
> 
> （10）第70行：将设置对象插入状态对象的设置链表末尾。


#### struct pinctrl_state 结构体定义
- 1 内核源码目录下的“drivers/pinctrl/core.h”文件中
```c
struct pinctrl_state {
	struct list_head node;         // 链表节点，用于将状态对象连接到引脚控制器对象的状态链表
	const char *name;              // 状态对象的名称字符串指针
	struct list_head settings;     // 设置对象链表，包含该状态的所有设置对象
};
```


#### struct pinctrl_setting 结构体定义
- 1 内核源码目录下的“drivers/pinctrl/core.h”文件中

```c
struct pinctrl_setting {
	struct list_head node;           // 链表节点，用于将设置对象连接到状态对象的设置链表
	enum pinctrl_map_type type;      // 映射类型，表示设置对象的类型
	struct pinctrl_dev *pctldev;     // 引脚控制设备对象指针
	const char *dev_name;            // 设备名称字符串指针
	union {
		struct pinctrl_setting_mux mux;           // 复用组映射类型的数据结构
		struct pinctrl_setting_configs configs;   // 配置映射类型的数据结构
	} data;
};
```



### 4 、create_state函数(3.1<---2)

#### 创建新的状态对象

```c
static struct pinctrl_state *create_state(struct pinctrl *p,
					  const char *name)
{
	struct pinctrl_state *state;
 
	// 为 pinctrl_state 结构体分配内存
	state = kzalloc(sizeof(*state), GFP_KERNEL);
	if (!state)
		// 内存分配失败，返回错误指针
		return ERR_PTR(-ENOMEM);
 
	// 设置状态的名称
	state->name = name;
	// 初始化状态的设置列表
	INIT_LIST_HEAD(&state->settings);
 
	// 将状态添加到 pinctrl 的状态链表中
	list_add_tail(&state->node, &p->states);
 
	return state;
}
```




### 5、pinmux_map_to_setting 函数(3.2<---2)
- 1 内核源码目录下的“drivers/pinctrl/pinmux.c”文件中

#### 将引脚映射转换为设置对象

```c
/**
 * pinmux_map_to_setting - 将引脚映射转换为设置对象
 *
 * @map: 引脚映射结构指针
 * @setting: 引脚设置结构指针
 *
 * 返回值：0 表示转换成功，负值表示转换失败
 */
int pinmux_map_to_setting(const struct pinctrl_map *map,
                          struct pinctrl_setting *setting)
{
    struct pinctrl_dev *pctldev = setting->pctldev; // 获取引脚控制设备指针
    const struct pinmux_ops *pmxops = pctldev->desc->pmxops; // 获取引脚复用操作指针
    char const * const *groups; // 引脚复用组数组
    unsigned num_groups; // 引脚复用组数量
    int ret;
    const char *group; // 引脚复用组名称
 
    if (!pmxops) {
        dev_err(pctldev->dev, "does not support mux function\n");
        return -EINVAL;
    }

    // 将复用函数名称转换为选择器
    ret = pinmux_func_name_to_selector(pctldev, map->data.mux.function);
    if (ret < 0) {
        dev_err(pctldev->dev, "invalid function %s in map table\n",
                map->data.mux.function);
        return ret;
    }
    setting->data.mux.func = ret; // 设置设置对象的复用函数选择器
 
    // 查询函数对应的复用组信息
    ret = pmxops->get_function_groups(pctldev, setting->data.mux.func,
                                      &groups, &num_groups);
    if (ret < 0) {
        dev_err(pctldev->dev, "can't query groups for function %s\n",
                map->data.mux.function);
        return ret;
    }
    if (!num_groups) {
        dev_err(pctldev->dev,
                "function %s can't be selected on any group\n",
                map->data.mux.function);
        return -EINVAL;
    }
    if (map->data.mux.group) {
        group = map->data.mux.group;
        ret = match_string(groups, num_groups, group);
        if (ret < 0) {
            dev_err(pctldev->dev,
                    "invalid group \"%s\" for function \"%s\"\n",
                    map->data.mux.function, group);
            return ret;
        }
    } else {
        group = groups[0];
    }
 
    // 获取复用组的选择器
    ret = pinctrl_get_group_selector(pctldev, group);
    if (ret < 0) {
        dev_err(pctldev->dev, "invalid group %s in map table\n",
                map->data.mux.group);
        return ret;
    }
    setting->data.mux.group = ret; // 设置设置对象的复用组选择器
 
    return 0;
}
```


#### 函数解析：
> （1）第19-22行：检查引脚控制设备是否支持引脚复用操作，如果不支持，则返回错误。
> 
> （2）第24-31行：将映射表中的复用函数名称转换为复用函数的选择器，并将其保存在设置对象的data.mux .func字段中。
> 
> （3）第33-46行：通过调用引脚复用操作对象的get_function_groups函数查询复用函数对应的复用组信息，获取复用组的名称数组和数量，并将它们保存在groups和num_groups变量中。如果没有任何复用组可供选择，则返回错误。
> 
> （4）第47-58行：根据映射表中指定的复用组名称或者选择第一个复用组名称，并在复用组数组中查找对应的索引。
> 
> （5）第60-67行：通过调用引脚控制设备对象的`pinctrl_get_group_selector函数`**获取复用组的选择器，并将它保存在设置对象的data.mux.group**



### 6、pinconf_map_to_setting 函数(3.3<---2)

#### 将引脚配置映射转换为设置对象。
```c
/**
 * pinconf_map_to_setting - 将引脚配置映射转换为设置对象
 *
 * @map: 引脚映射结构指针
 * @setting: 引脚设置结构指针
 *
 * 返回值：0 表示转换成功，负值表示转换失败
 */
int pinconf_map_to_setting(const struct pinctrl_map *map,
                           struct pinctrl_setting *setting)
{
    struct pinctrl_dev *pctldev = setting->pctldev; // 获取引脚控制设备指针
    int pin;
 
    switch (setting->type) {
        case PIN_MAP_TYPE_CONFIGS_PIN: // 针对单个引脚的配置
            pin = pin_get_from_name(pctldev, map->data.configs.group_or_pin); // 通过引脚名称获取引脚号
            if (pin < 0) {
                dev_err(pctldev->dev, "could not map pin config for \"%s\"",
                        map->data.configs.group_or_pin);
                return pin;
            }
            setting->data.configs.group_or_pin = pin; // 设置设置对象的引脚号
            break;
        case PIN_MAP_TYPE_CONFIGS_GROUP: // 针对引脚组的配置
            pin = pinctrl_get_group_selector(pctldev, map->data.configs.group_or_pin); // 获取引脚组的选择器
            if (pin < 0) {
                dev_err(pctldev->dev, "could not map pin config for \"%s\"",
                        map->data.configs.group_or_pin);
                return pin;
            }
            setting->data.configs.group_or_pin = pin; // 设置设置对象的引脚组选择器
            break;
        default:
            return -EINVAL;
    }
 
    setting->data.configs.num_configs = map->data.configs.num_configs; // 设置设置对象的配置数量
    setting->data.configs.configs = map->data.configs.configs; // 设置设置对象的配置指针
 
    return 0;
}
```

#### 函数解析：(❤️)
> （1）第15-38行：根据设置对象的类型进行不同的处理：
> 
> ·对于针对`单个引脚的配置，通过调用pin_get_from_name函数`，根据映射表中的引脚名称**获取引脚号，并将其设置到设置对象的data.configs.group_or_pin字段**中。如果获取引脚号失败，则返回错误。
> 
> ·对于针对`引脚组的配置，它通过调用pinctrl_get_group_selector函数`，根据映射表中的引脚组名称**获取引脚组的选择器，并将其设置到设置对象的data.configs.group_or_pin字段中**。
> 
> ·如果获取引脚组选择器失败，则返回错误。
> 
> （2）第40-42行：**设置设置对象的配置数量和配置指针，分别从映射表中获取**。完成转换后，函数返回0表示转换成功。






### 7、



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


