---
title: "{{title}}"
aliases: 
tags: 
description: 
source:
---

# 备注(声明)：


# 参考文章：




# 一、pinctrl_bind_pins函数分析：

## 继续分析pinctrl_bind_pins函数
> 前面的小节都只是对pinctrl_bind_pins函数的第15行获取设备的pinctrl句柄所使用的 devm_pinctrl_get 函数进行的讲解，**接下来将继续对后面重要的内容进行讲解。**

### 1 、内容如下所示：（1---->）
```c
int pinctrl_bind_pins(struct device *dev)
{
	int ret;
 
	// 检查设备是否重用了节点
	if (dev->of_node_reused)
		return 0;
 
	// 为设备的引脚分配内存空间
	dev->pins = devm_kzalloc(dev, sizeof(*(dev->pins)), GFP_KERNEL);
	if (!dev->pins)
		return -ENOMEM;
 
	// 获取设备的 pinctrl 句柄
	dev->pins->p = devm_pinctrl_get(dev);
	if (IS_ERR(dev->pins->p)) {
		dev_dbg(dev, "没有 pinctrl 句柄\n");
		ret = PTR_ERR(dev->pins->p);
		goto cleanup_alloc;
	}
 
	// 查找设备的默认 pinctrl 状态
	dev->pins->default_state = pinctrl_lookup_state(dev->pins->p, PINCTRL_STATE_DEFAULT);
	if (IS_ERR(dev->pins->default_state)) {
		dev_dbg(dev, "没有默认的 pinctrl 状态\n");
		ret = 0;
		goto cleanup_get;
	}
 
	// 查找设备的初始化 pinctrl 状态
	dev->pins->init_state = pinctrl_lookup_state(dev->pins->p, PINCTRL_STATE_INIT);
	if (IS_ERR(dev->pins->init_state)) {
		/* 不提供此状态是完全合法的 */
		dev_dbg(dev, "没有初始化的 pinctrl 状态\n");
 
		// 选择默认的 pinctrl 状态
		ret = pinctrl_select_state(dev->pins->p, dev->pins->default_state);
	} else {
		// 选择初始化的 pinctrl 状态
		ret = pinctrl_select_state(dev->pins->p, dev->pins->init_state);
	}
 
	if (ret) {
		dev_dbg(dev, "无法激活初始的 pinctrl 状态\n");
		goto cleanup_get;
	}
 
#ifdef CONFIG_PM
	/*
	 * 如果启用了电源管理，我们还会寻找可选的睡眠和空闲的引脚状态，其语义在
	 * <linux/pinctrl/pinctrl-state.h> 中定义
	 */
	dev->pins->sleep_state = pinctrl_lookup_state(dev->pins->p, PINCTRL_STATE_SLEEP);
	if (IS_ERR(dev->pins->sleep_state))
		/* 不提供此状态是完全合法的 */
		dev_dbg(dev, "没有睡眠的 pinctrl 状态\n");
 
	dev->pins->idle_state = pinctrl_lookup_state(dev->pins->p, PINCTRL_STATE_IDLE);
	if (IS_ERR(dev->pins->idle_state))
		/* 不提供此状态是完全合法的 */
		dev_dbg(dev, "没有空闲的 pinctrl 状态\n");
#endif
 
	return 0;
 
	/*
	 * 如果对于此设备没有找到 pinctrl 句柄或默认状态，
	 * 让我们明确释放设备中的引脚容器，因为保留它没有意义。
	 */
cleanup_get:
	devm_pinctrl_put(dev->pins->p);
cleanup_alloc:
	devm_kfree(dev, dev->pins);
	dev->pins = NULL;
 
	/* 返回延迟 */
	if (ret == -EPROBE_DEFER)
		return ret;
	/* 返回严重错误 */
	if (ret == -EINVAL)
		return ret;
	/* 我们忽略诸如 -ENOENT 的错误，表示没有 pinctrl 状态 */
 
	return 0;
}
```

### 2 、函数解析：
> 第22-28行：查找设备的默认pinctrl状态。使用 `pinctrl_lookup_state 函数`通过 dev->pins->p 和 PINCTRL_STATE_DEFAULT 参数**查找设备的默认pinctrl状态**，并将其赋值给 **dev->pins->default_state**。如果查找失败，函数会打印一条调试信息，并将返回值设置为0，表示继续执行。

> （2）第30-41行：**查找设备的初始化pinctrl状态**。使用 pinctrl_lookup_state 函数通过 dev->pins->p 和 PINCTRL_STATE_INIT 参数查找设备的初始化pinctrl状态，并将其赋值给 dev->pins->init_state。如果查找失败，函数会打印一条调试信息。如果找不到初始化状态，会选择默认的 pinctrl 状态，并将返回值设置为 pinctrl_select_state 函数的返回值。
> 
> （3）第48-56行：如果配置了电源管理（CONFIG_PM 宏定义），则会继续执行以下步骤。首先，**查找设备的睡眠pinctrl状态**。使用 pinctrl_lookup_state 函数通过 dev->pins->p 和 PINCTRL_STATE_SLEEP 参数查找设备的睡眠pinctrl状态，并将其赋值给 dev->pins->sleep_state。如果查找失败，函数会打印一条调试信息。
> 
> （4）第58-64行：**查找设备的空闲pinctrl状态**。使用pinctrl_lookup_state 函数通过 dev->pins->p 和 PINCTRL_STATE_IDLE 参数查找设备的空闲pinctrl状态，并将其赋值给 dev->pins->idle_state。如果查找失败，函数会打印一条调试信息。函数返回0，表示引脚绑定成功。
> 
> 第37行和第40行会`使用 pinctrl_select_state `**选择并切换到指定的pinctrl_state**（引脚控制状态），该
> 


### 3 、pinctrl_lookup_state函数(2.1<---1)
#### 查找设备的pinctrl状态
- 1 函数定义在内核源码目录下的“drivers/pinctrl/core.c”文件中

```c
struct pinctrl_state *pinctrl_lookup_state(struct pinctrl *p,
						 const char *name)
{
	struct pinctrl_state *state;
 
	// 在状态链表中查找指定名称的状态对象
	state = find_state(p, name);
	if (!state) {
		if (pinctrl_dummy_state) {
			/* 创建虚拟状态 */
			dev_dbg(p->dev, "使用 pinctrl 虚拟状态(%s)\n",
				name);
			// 如果找不到 指定的状态对象，并且存在虚拟状态，则创建一个虚拟状态对象
			state = create_state(p, name);
		} else
			// 如果找不到指定的状态对象，并且不存在虚拟状态，则返回错误指针 -ENODEV
			state = ERR_PTR(-ENODEV);
	}
 
	return state;
}
```





### 4 、pinctrl_select_state 函数(2.2<---1)

#### 选择并切换到指定的pinctrl_state（引脚控制状态）(❤️)
- 1 内核源码目录下的“drivers/pinctrl/core.c”文件中

```c
int pinctrl_select_state(struct pinctrl *p, struct pinctrl_state *state)
{
	// 如果当前状态已经是要选择的状态，则无需进行任何操作，直接返回0表示成功
	if (p->state == state)
		return 0;
 
	// 调用 pinctrl_commit_state 函数来应用并切换到新的状态
	return pinctrl_commit_state(p, state);
}
```


#### 调用pinctrl_commit_state函数应用并切换到新的状态



### 5、pinctrl_commit_state函数(3<---2.2)

#### 应用并切换到新的状态

```c
static int pinctrl_commit_state(struct pinctrl *p, struct pinctrl_state *state)
{
	struct pinctrl_setting *setting, *setting2;
	struct pinctrl_state *old_state = p->state;
	int ret;
 
	if (p->state) {
		/*
		 * 对于旧状态中的每个引脚复用设置，取消 SW 记录的该引脚组的复用所有者。
		 * 任何仍由新状态拥有的引脚组将在下面循环中的 pinmux_enable_setting() 调用中重新获取。
		 */
		list_for_each_entry(setting, &p->state->settings, node) {
			if (setting->type != PIN_MAP_TYPE_MUX_GROUP)
				continue;
			pinmux_disable_setting(setting);
		}
	}
 
	p->state = NULL;
 
	/* 应用新状态的所有设置 */
	list_for_each_entry(setting, &state->settings, node) {
		switch (setting->type) {
		case PIN_MAP_TYPE_MUX_GROUP:
			ret = pinmux_enable_setting(setting);
			break;
		case PIN_MAP_TYPE_CONFIGS_PIN:
		case PIN_MAP_TYPE_CONFIGS_GROUP:
			ret = pinconf_apply_setting(setting);
			break;
		default:
			ret = -EINVAL;
			break;
		}
 
		if (ret < 0) {
			// 如果应用设置失败，则回滚新状态的设置
			goto unapply_new_state;
		}
	}
 
	p->state = state;
 
	return 0;
 
unapply_new_state:
	// 回滚新状态的设置
	list_for_each_entry_safe(setting, setting2, &state->settings, node) {
		switch (setting->type) {
		case PIN_MAP_TYPE_MUX_GROUP:
			pinmux_disable_setting(setting);
			break;
		case PIN_MAP_TYPE_CONFIGS_PIN:
		case PIN_MAP_TYPE_CONFIGS_GROUP:
			pinconf_remove_setting(setting);
			break;
		}
	}
 
	// 回滚完成后，将状态恢复为旧状态
	p->state = old_state;
 
	return ret;
}
```

#### 函数解析：
> （1）第4行：保存当前的状态对象到变量 old_state 中。
> 
> （2）第7-18行：检查是否存在旧的状态，如果存在则取消记录在软件中的旧状态中每个引脚复用设置的复用所有者。这样做是为了确保任何仍由新状态拥有的引脚组在后面的循环中重新获取（通过pinmux_enable_setting()函数调用 ）。
> 
> （3）第20行：将当前的状态设置为NULL，以便在应用新状态时可以正确处理。
> 
> （4）第22-41行：**遍历新状态的所有设置，并根据设置的类型执行相应的操作**：
> 
> ·对于引脚复用设置（PIN_MAP_TYPE_MUX_GROUP），`调用pinmux_enable_setting()`函数来**启用该设置**。
> 
> ·对于引脚配置设置（PIN_MAP_TYPE_CONFIGS_PIN或PIN_MAP_TYPE_CONFIGS_GROUP），`调用pinconf_apply_setting()`函数来**应用该设置**。
> 
> ·对于其他类型的设置，将返回一个错误码（-EINVAL）。
> 
> ·如果应用设置失败，则跳转到标签unapply_new_state，执行回滚操作。
> 


### 6、pinmux_enable_setting函数(4.1<---3)
#### 启用引脚复用设置(❤️)

```c
int pinmux_enable_setting(const struct pinctrl_setting *setting)
{
    // 获取相关结构体指针
    struct pinctrl_dev *pctldev = setting->pctldev;
    const struct pinctrl_ops *pctlops = pctldev->desc->pctlops;
    const struct pinmux_ops *ops = pctldev->desc->pmxops;
    int ret = 0;
    const unsigned *pins = NULL;
    unsigned num_pins = 0;
    int i;
    struct pin_desc *desc;
 
    // 如果pctlops->get_group_pins函数存在，则调用该函数获取组中的引脚信息
    if (pctlops->get_group_pins)
        ret = pctlops->get_group_pins(pctldev, setting->data.mux.group,
                                      &pins, &num_pins);
 
    if (ret) {
        const char *gname;
 
        // 错误只影响调试数据，因此只发出警告
        gname = pctlops->get_group_name(pctldev,
                                        setting->data.mux.group);
        dev_warn(pctldev->dev,
                 "could not get pins for group %s\n",
                 gname);
        num_pins = 0;
    }
 
    // 逐个申请组中的引脚
    for (i = 0; i < num_pins; i++) {
        ret = pin_request(pctldev, pins[i], setting->dev_name, NULL);
        if (ret) {
            const char *gname;
            const char *pname;
 
            desc = pin_desc_get(pctldev, pins[i]);
            pname = desc ? desc->name : "non-existing";
            gname = pctlops->get_group_name(pctldev,
                                            setting->data.mux.group);
            dev_err(pctldev->dev,
                    "could not request pin %d (%s) from group %s "
                    " on device %s\n",
                    pins[i], pname, gname,
                    pinctrl_dev_get_name(pctldev));
            goto err_pin_request;
        }
    }
 
    // 分配引脚后，编码复用设置
    for (i = 0; i < num_pins; i++) {
        desc = pin_desc_get(pctldev, pins[i]);
        if (desc == NULL) {
            dev_warn(pctldev->dev,
                     "could not get pin desc for pin %d\n",
                     pins[i]);
            continue;
        }
        desc->mux_setting = &(setting->data.mux);
    }
 
    // 调用ops->set_mux函数设置复用
    ret = ops->set_mux(pctldev, setting->data.mux.func,
                       setting->data.mux.group);
 
    if (ret)
        goto err_set_mux;
 
    return 0;
 
err_set_mux:
    // 复用设置失败，清除复用设置
    for (i = 0; i < num_pins; i++) {
        desc = pin_desc_get(pctldev, pins[i]);
        if (desc)
            desc->mux_setting = NULL;
    }
err_pin_request:
    // 在错误发生时释放已申请的引脚
    while (--i >= 0)
        pin_free(pctldev, pins[i], NULL);
 
    return ret;
}
```

#### 函数解析：
> （1）第13-28行：调用pctlops->get_group_pins函数获取指定组中的引脚信息，如果函数存在，则调用该函数，并将引脚信息存储在pins和num_pins变量中。如果获取引脚信息失败，发出警告并将num_pins设置为0。
> 
> （2）第30-48行：**使用pin_request函数申请引脚**，并传入引脚控制器设备、引脚编号、设备名称和其他参数。如果申请引脚失败，发出错误信息并跳转到错误处理步骤。
> 
> （3）第50-60行：分配引脚后，使用pin_desc_get函数获取引脚描述符，并将复用设置指针指向引脚复用信息。
> 
> （4）第62-64行：**调用ops->set_mux函数设置引脚复用**，传入引脚控制器设备、复用功能和组信息，以便设置引脚复用。
> 
> （5）第66行：如果引脚复用设置失败，跳转到错误处理步骤。


### 7、pinconf_apply_setting()函数(4.2<---3)
#### 应用引脚配置设置(❤️)
- 1 内核源码目录下的“drivers/pinctrl/pinconf.c”文件中
```c
int pinconf_apply_setting(const struct pinctrl_setting *setting)
{
    // 获取相关结构体指针
    struct pinctrl_dev *pctldev = setting->pctldev;
    const struct pinconf_ops *ops = pctldev->desc->confops;
    int ret;
 
    // 检查是否存在 pinconf 操作函数集
    if (!ops) {
        dev_err(pctldev->dev, "missing confops\n");
        return -EINVAL;
    }
 
    // 根据设置类型选择相应的操作
    switch (setting->type) {
        case PIN_MAP_TYPE_CONFIGS_PIN:
            // 检查是否存在 pin_config_set 操作函数
            if (!ops->pin_config_set) {
                dev_err(pctldev->dev, "missing pin_config_set op\n");
                return -EINVAL;
            }
 
            // 调用 pin_config_set 函数设置单个引脚的配置
            ret = ops->pin_config_set(pctldev,
                                      setting->data.configs.group_or_pin,
                                      setting->data.configs.configs,
                                      setting->data.configs.num_configs);
            if (ret < 0) {
                dev_err(pctldev->dev,
                        "pin_config_set op failed for pin %d\n",
                        setting->data.configs.group_or_pin);
                return ret;
            }
            break;
 
        case PIN_MAP_TYPE_CONFIGS_GROUP:
            // 检查是否存在 pin_config_group_set 操作函数
            if (!ops->pin_config_group_set) {
                dev_err(pctldev->dev, "missing pin_config_group_set op\n");
                return -EINVAL;
            }
 
            // 调用 pin_config_group_set 函数设置引脚组的配置
            ret = ops->pin_config_group_set(pctldev,
                                            setting->data.configs.group_or_pin,
                                            setting->data.configs.configs,
                                            setting->data.configs.num_configs);
            if (ret < 0) {
                dev_err(pctldev->dev,
                        "pin_config_group_set op failed for group %d\n",
                        setting->data.configs.group_or_pin);
                return ret;
            }
            break;
 
        default:
            return -EINVAL;
    }
 
    return 0;
}
```

#### 函数解析：
> （1）第8-12行：检查是否存在引脚配置操作函数集，如果不存在，则返回错误码 -EINVAL。
> 
> （2）第14-59：**根据设置类型进行相应的处理**：
> 
> ·如果设置类型为 PIN_MAP_TYPE_CONFIGS_PIN，表示对单个引脚进行配置设置。然后检查是否存在 pin_config_set 操作函数，如果存在则调用 pin_config_set 函数设置单个引脚的配置。如果设置失败，则返回相应的错误码。
> 
> ·如果设置类型为 PIN_MAP_TYPE_CONFIGS_GROUP，表示对引脚组进行配置设置，然后检查是否存在 pin_config_group_set 操作函数，如果存在则调用 pin_config_group_set 函数设置引脚组的配置。如果设置失败，则返回相应的错误码。
> 
> ·如果设置类型不是上述两种类型，则返回错误码 -EINVAL。





### 8、



## pinctrl_bind_pins函数作用：
### 1 、为给定的设备绑定引脚


### 2 、并在绑定过程中选择和设置适当的pinctrl状态(❤️)


### 3 、


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


