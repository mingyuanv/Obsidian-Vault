---
title: "{{title}}"
aliases: 
tags: 
description: 
source:
---

# 备注(声明)：注册并启用pinctrl设备

## 思维导图
[[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十一期_pinctrl子系统/canvas/第121 章 pinctrl-probe 分析.canvas|第121 章 pinctrl-probe 分析]]



# 参考文章：

```cardlink
url: https://blog.csdn.net/BeiJingXunWei/article/details/135548271?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522788249d8c4d6ce541277d70ace106faa%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fblog.%2522%257D&request_id=788249d8c4d6ce541277d70ace106faa&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~blog~first_rank_ecpm_v1~rank_v31_ecpm-1-135548271-null-null.nonecase&utm_term=%E7%AC%AC121%E7%AB%A0&spm=1018.2226.3001.4450
title: "RK3568驱动指南｜第十一篇 pinctrl子系统-第121章 pinctrl probe函数讲解_rk3568 pinctrl-CSDN博客"
description: "文章浏览阅读1.5k次，点赞20次，收藏24次。（2）第11-15行，对pinctrl描述结构体进行初始化。由于pinctrl驱动的probe函数理解起来较为复杂，所以在讲解pinctrl驱动的probe函数之前，我们先来了解一些与pinctrl相关的数据结构，本章首先会学习pinctrl_desc结构体和rockchip_pinctrl 结构体，最后对pinctrl probe函数进行分析。（3）第23-29行：调用rockchip_pinctrl_get_soc_data函数，根据设备信息获取与该设备相关的rockchip_pin_ctrl结构体。_rk3568 pinctrl"
host: blog.csdn.net
```






# 一、pinctrl probe函数讲解

## pinctrl_desc结构体分析
### 1 、描述引脚控制器（pinctrl）的属性和操作


### 2 、引脚控制器简介：
> 引脚控制器是硬件系统中的一个组件，用于**管理和控制引脚的功能和状态**。pinctrl_desc结构体的作用是提供一个统一的接口，用于配置和管理引脚控制器的行为。


### 3 、pinctrl_desc结构体定义(❤️)
- 1 内核源码目录的“/include/linux/pinctrl/pinctrl.h”文件中

```c
struct pinctrl_desc {
    const char *name;                                // 引脚控制器的名称
    const struct pinctrl_pin_desc *pins;             // 引脚描述符数组
    unsigned int npins;                              // 引脚描述符数组的大小
    const struct pinctrl_ops *pctlops;               // 引脚控制操作函数指针
    const struct pinmux_ops *pmxops;                 // 引脚复用操作函数指针
    const struct pinconf_ops *confops;               // 引脚配置操作函数指针
    struct module *owner;                            // 拥有该结构体的模块
#ifdef CONFIG_GENERIC_PINCONF
    unsigned int num_custom_params;                  // 自定义参数数量
    const struct pinconf_generic_params *custom_params;    // 自定义参数数组
    const struct pin_config_item *custom_conf_items;       // 自定义配置项数组
#endif
};
```

### 4 、常数详解：
> （1）const char `*name`: 引脚控制器的名称，用于标识引脚控制器的唯一性。
> 
> （2）const struct pinctrl_pin_desc `*pins`: 引脚描述符数组，是一个**指向引脚描述符的指针**，用于描述引脚的属性和配置。每个引脚描述符包含了引脚的名称、编号、模式等信息。
> 
> （3）unsigned int npins: 表示引脚描述符**数组中元素的数量**，用于确定引脚描述符数组的长度。
> 
> （4）const struct pinctrl_ops `*pctlops`: 指向引脚控制操作函数的指针，用于定义引脚控制器的操作接口。通过这些操作函数，可以对引脚进行配置、使能、禁用等操作。
> 
> （5）const struct pinmux_ops `*pmxops`: 指向引脚复用操作函数的指针，用于定义引脚的复用功能。复用功能允许将引脚的功能切换为不同的模式，以适应不同的设备需求。
> 
> （6）const struct pinconf_ops `*confops`: 指向引脚配置操作函数的指针，用于定义引脚的其他配置选项。这些配置选项可以包括引脚的上拉、下拉配置、电气特性等。
> 
> （7）struct module `*owner`: 指向拥有该引脚控制器结构体的模块的指针。这个字段用于跟踪引脚控制器结构体的所有者。
> 
> （8）unsigned int num_custom_params: 表示自定义配置参数的数量，用于描述引脚控制器的自定义配置参数。
> 
> （9）const struct pinconf_generic_params` *custom_params`: 指向自定义配置参数的指针，用于描述引脚控制器的自定义配置参数的属性。自定义配置参数可以根据具体需求定义，用于扩展引脚控制器的配置选项。
> 
> （10）const struct pin_config_item `*custom_conf_items`: 指向自定义配置项的指针，用于描述引脚控制器的自定义配置项的属性。自定义配置项可以根据具体需求定义，用于扩展引脚控制器的配置选项。


### 5、





## rockchip_pinctrl 结构体分析
### 1 、struct pinctrl_desc进行了再一次封装(❤️)
- 2 瑞芯微为了适应瑞芯微芯片的特定需求和功能

### 2 、增加了与瑞芯微芯片相关的字段和指针


### 3 、rockchip_pinctrl结构体定义(❤️)
- 1 内核源码目录下的“/drivers/pinctrl/pinctrl-rockchip.h”文件中

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


### 4 、参数详解：
> （1）struct regmap `*regmap_base`：指向基本寄存器映射（regmap）的指针。基本寄存器映射是一个用于**访问芯片寄存器的接口**，它提供了对芯片寄存器的读写操作。
> 
> （2）int reg_size：表示寄存器的字节大小，用于确定寄存器的地址范围。
> 
> （3）struct regmap `*regmap_pull`：指向拉取寄存器映射的指针。拉取寄存器映射用于控制引脚上的**上拉和下拉功能**。
> 
> （4）struct regmap` *regmap_pmu`：指向电源管理单元（PMU）寄存器映射的指针。PMU寄存器映射用于**控制引脚的电源管理功能**。
> 
> （5）struct device `*dev`：指向设备结构体的指针。设备结构体用于**表示与硬件相关的设备，包括设备的物理地址、中断等信息**。
> 
> （6）struct rockchip_pin_ctrl `*ctrl`：指向瑞芯微芯片引脚控制器的指针。这个结构体存储了瑞芯微芯片特定的引脚控制器的相关信息和操作。
> 
> （7）struct pinctrl_desc pctl：包含了struct pinctrl_desc结构体的一个实例。用于描述引脚控制器的属性和操作，包括引脚控制器的名称、引脚描述符数组、函数指针等。
> 
> （8）struct pinctrl_dev `*pctl_dev`：指向引脚控制器设备结构体的指针。引脚控制器设备结构体用于表示引脚控制器在系统中的设备实例，包含了与引脚控制器相关的设备信息和操作接口。
> 
> （9）struct rockchip_pin_group` *groups`：指向瑞芯微芯片引脚组的指针。**引脚组是一组相关的引脚，可以一起进行配置和管理**。
> 
> （10）unsigned int ngroups：表示引脚组数组的大小，用于确定引脚组数组的长度。
> 
> （11）struct rockchip_pmx_func `*functions`：指向瑞芯微芯片引脚功能的指针。引脚功能定义了引脚可以承担的不同功能，例如UART、SPI、I2C等。
> 
> （12）unsigned int nfunctions：引脚功能的数量。它表示引脚功能数组的大小，用于确定引脚功能数组的长度。


### 5、





## pinctrl probe函数分析
### 1 、probe函数，具体内容如下(1--->)

```c
static int rockchip_pinctrl_probe(struct platform_device *pdev)
{
    struct rockchip_pinctrl *info;       // Rockchip GPIO控制器的信息结构体指针
    struct device *dev = &pdev->dev;     // 设备结构体指针
    struct rockchip_pin_ctrl *ctrl;      // Rockchip GPIO控制器的配置结构体指针
    struct device_node *np = pdev->dev.of_node, *node;          // 设备节点指针
    struct resource *res;                                       // 设备资源指针
    void __iomem *base;                                         // 寄存器基地址指针
    int ret;                                                    // 返回值
 
    if (!dev->of_node) {
        dev_err(dev, "device tree node not found\n");
        return -ENODEV;
    }
 
    // 分配并初始化一个rockchip_pinctrl结构体
    info = devm_kzalloc(dev, sizeof(*info), GFP_KERNEL);
    if (!info)
        return -ENOMEM;
 
    info->dev = dev;
 
    // 获取并设置与pdev相关的rockchip_pin_ctrl结构体
    ctrl = rockchip_pinctrl_get_soc_data(info, pdev);
    if (!ctrl) {
        dev_err(dev, "driver data not available\n");
        return -EINVAL;
    }
    info->ctrl = ctrl;
 
    // 解析设备树中的"rockchip,grf"节点，获取寄存器映射基地址
    node = of_parse_phandle(np, "rockchip,grf", 0);
    if (node) {
        info->regmap_base = syscon_node_to_regmap(node);
        if (IS_ERR(info->regmap_base))
            return PTR_ERR(info->regmap_base);
    } else {
        // 如果找不到"rockchip,grf"节点，则获取IORESOURCE_MEM类型的资源，得到寄存器基地址
        res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
        base = devm_ioremap_resource(&pdev->dev, res);
        if (IS_ERR(base))
            return PTR_ERR(base);
 
        // 配置寄存器映射的最大寄存器地址和名称
        rockchip_regmap_config.max_register = resource_size(res) - 4;
        rockchip_regmap_config.name = "rockchip,pinctrl";
        info->regmap_base = devm_regmap_init_mmio(&pdev->dev, base,
                            &rockchip_regmap_config);
 
        // 检查旧的dt-bindings
        info->reg_size = resource_size(res);
 
        // 如果控制器类型为RK3188且reg_size小于0x200，则获取第二个IORESOURCE_MEM类型的资源，作为pull寄存器的基地址
        if (ctrl->type == RK3188 && info->reg_size < 0x200) {
            res = platform_get_resource(pdev, IORESOURCE_MEM, 1);
            base = devm_ioremap_resource(&pdev->dev, res);
            if (IS_ERR(base))
                return PTR_ERR(base);
 
            // 配置pull寄存器映射的最大寄存器地址和名称
            rockchip_regmap_config.max_register =
                            resource_size(res) - 4;
            rockchip_regmap_config.name = "rockchip,pinctrl-pull";
            info->regmap_pull = devm_regmap_init_mmio(&pdev->dev,
                            base,
                            &rockchip_regmap_config);
        }
    }
 
    // 尝试查找可选的pmu syscon引用
    node = of_parse_phandle(np, "rockchip,pmu", 0);
    if (node) {
        info->regmap_pmu = syscon_node_to_regmap(node);
        if (IS_ERR(info->regmap_pmu))
            return PTR_ERR(info->regmap_pmu);
    }
 
    // 对于某些SoC进行特殊处理
    if (ctrl->soc_data_init) {
        ret = ctrl->soc_data_init(info);
        if (ret)
            return ret;
    }
 
    // 注册rockchip_pinctrl设备
    ret = rockchip_pinctrl_register(pdev, info);
    if (ret)
        return ret;
 
    // 设置pdev的私有数据为info
    platform_set_drvdata(pdev, info);
 
    // 注册GPIO设备
    ret = of_platform_populate(np, rockchip_bank_match, NULL, NULL);
    if (ret) {
        dev_err(&pdev->dev, "failed to register gpio device\n");
        return ret;
    }
    dev_info(dev, "probed %s\n", dev_name(dev));
 
    return 0;
}
```
### 2 、详细的分析：(❤️)
> （1）第11-14行：检查设备结构体中的设备树节点是否存在，如果不存在则报错并返回错误码。
> 
> （2）第17-19行：使用devm_kzalloc函数分配一个rockchip_pinctrl结构体的内存，并将其初始化为0。然后将设备结构体指针赋值给info->dev，以便在后续代码中可以使用设备结构体的信息。
> 
> （3）第23-29行：调用rockchip_pinctrl_get_soc_data函数，根据设备信息**获取与该设备相关的rockchip_pin_ctrl结构体**。如果获取失败，则报错并返回错误码。将获取到的结构体指针赋值**给info->ctrl**。
> 
> （4）第32-69行使用of_parse_phandle函数解析设备树中名为"rockchip,grf"的节点。如果解析成功，则调用syscon_node_to_regmap函数将节点转换为寄存器映射的基地址，并将结果存储在info->regmap_base中。如果解析失败，则进入"else"分支。
> 
> 在"else"分支中，通过platform_get_resource函数获取IORESOURCE_MEM类型的资源，以**获取寄存器的基地址**。然后使用devm_ioremap_resource函数将资源映射到内存中，并将结果存储在base中。接下来，配置寄存器映射的最大寄存器地址和名称，并使用devm_regmap_init_mmio函数初始化寄存器映射，将结果存储在info->regmap_base中。
> 
> 如果控制器类型为RK3188且reg_size小于0x200，则获取第二个IORESOURCE_MEM类型的资源，作为pull寄存器的基地址。类似地，**配置pull寄存器**映射的最大寄存器地址和名称，并使用devm_regmap_init_mmio函数初始化pull寄存器映射，将结果存储在info->regmap_pull中。
> 
> （5）第72-77行：使用of_parse_phandle函数解析设备树中名为"rockchip,pmu"的可选节点。如果解析成功，则**调用syscon_node_to_regmap函数将节点转换为寄存器映射的基地址，并将结果存储在info->regmap_pmu中**。
> 
> （6）第80-84行：如果ctrl->soc_data_init不为空，则调用该函数指针所指向的函数，对特定的SoC进行特殊处理。处理完成后，如果返回值不为0，则返回该错误码。
> 
> （7）第87-89行：调用rockchip_pinctrl_register函数**注册rockchip_pinctrl设备**。如果注册失败，则返回错误码。
> 
> （8）第92行：使用platform_set_drvdata函数将info设置为pdev的私有数据。
> 
> （9）第95-100行：调用of_platform_populate函数**注册GPIO设备**。如果注册失败，则返回错误码。


> 在probe函数中需要特别注意的是第87行的`rockchip_pinctrl_register注册rockchip_pinctrl设备函数`，传入的参数分别为**pdev和rockchip_pinctrl类型的info**

### 3 、rockchip_pinctrl_register函数的定义(2<---)

```c
static int rockchip_pinctrl_register(struct platform_device *pdev,
					struct rockchip_pinctrl *info)
{
	struct pinctrl_desc *ctrldesc = &info->pctl;
	struct pinctrl_pin_desc *pindesc, *pdesc;
	struct rockchip_pin_bank *pin_bank;
	int pin, bank, ret;
	int k;
 
	// 初始化pinctrl描述结构体
	ctrldesc->name = "rockchip-pinctrl";
	ctrldesc->owner = THIS_MODULE;
	ctrldesc->pctlops = &rockchip_pctrl_ops;
	ctrldesc->pmxops = &rockchip_pmx_ops;
	ctrldesc->confops = &rockchip_pinconf_ops;
 
	// 为每个引脚分配内存
	pindesc = devm_kcalloc(&pdev->dev,
			       info->ctrl->nr_pins, sizeof(*pindesc),
			       GFP_KERNEL);
	if (!pindesc)
		return -ENOMEM;
 
	ctrldesc->pins = pindesc;
	ctrldesc->npins = info->ctrl->nr_pins;
 
	pdesc = pindesc;
	// 遍历每个引脚所属的bank，为每个引脚设置编号和名称
	for (bank = 0, k = 0; bank < info->ctrl->nr_banks; bank++) {
		pin_bank = &info->ctrl->pin_banks[bank];
		for (pin = 0; pin < pin_bank->nr_pins; pin++, k++) {
			pdesc->number = k;
			pdesc->name = kasprintf(GFP_KERNEL, "%s-%d",
						pin_bank->name, pin);
			pdesc++;
		}
	}
 
	// 解析设备树中的pinctrl信息
	ret = rockchip_pinctrl_parse_dt(pdev, info);
	if (ret)
		return ret;
 
	// 注册pinctrl设备
	info->pctl_dev = devm_pinctrl_register(&pdev->dev, ctrldesc, info);
	if (IS_ERR(info->pctl_dev)) {
		dev_err(&pdev->dev, "could not register pinctrl driver\n");
		return PTR_ERR(info->pctl_dev);
	}
 
	return 0;
}
```

### 4 、函数详解：
> （1）第4行：将info的pctl参数传递给了`struct pinctrl_desc *`类型的变量ctrldesc，从而使得rockchip_pinctrl结构体和pinctrl_desc 结构体建立了联系。
> 
> （2）第11-15行，**对pinctrl描述结构体进行初始化**。这些结构体成员包括name（pinctrl控制器的名称），owner（拥有该pinctrl控制器的模块），pctlops（pinctrl控制操作函数），pmxops（pinctrl引脚复用操作函数）和confops（pinctrl引脚配置操作函数）。
> 
> （3）第18-22行，使用devm_kcalloc函数在设备的内存上分配一块连续的内存区域，用于存储引脚描述结构体。该函数分配的内存大小为info->ctrl->nr_pins * sizeof(`*pindesc`)字节。如果内存分配失败，则返回-ENOMEM错误码。
> 
> （4）第24-25行：通过将引脚描述结构体的指针pindesc赋值给pinctrl描述结构体的pins成员，将引脚数量info->ctrl->nr_pins赋值给pinctrl描述结构体的npins成员。
> 
> （5）第27-37行：通过**遍历每个引脚所属的bank，为每个引脚设置编号和名称**。首先，定义变量pdesc指向引脚描述结构体的起始地址。然后，使用两个嵌套的循环，外层循环遍历每个引脚所属的bank，内层循环遍历每个bank中的引脚。
> 
> 在内层循环中，首先将当前引脚的编号k赋值给引脚描述结构体的number成员，然后使用kasprintf函数动态分配内存储引脚名称的字符串，并将该字符串赋值给引脚描述结构体的name成员。kasprintf函数在内核堆中分配内存，并格式化生成字符串。格式化的字符串为"%s-%d"，其中pin_bank->name是当前bank的名称，pin是当前引脚在bank中的索引。
> 
> （6）第39-42行：调用rockchip_pinctrl_parse_dt函数来**解析设备树中的pinctrl信息**。该函数根据设备树中的描述，**设置引脚的默认配置**。
> 
> （7）第45-49行：调用devm_pinctrl_register函数**注册pinctrl设备**。该函数将pinctrl描述结构体、pinctrl相关操作函数和私有数据作为参数，将pinctrl设备注册到系统中。
> 

- 2 其中需要注意第45行的devm_pinctrl_register函数

### 5、devm_pinctrl_register函数(3<---)(❤️)
- 1 内核源码目录下的“drivers/pinctrl/core.c”文件中

```c
struct pinctrl_dev *devm_pinctrl_register(struct device *dev,
					  struct pinctrl_desc *pctldesc,
					  void *driver_data)
{
	struct pinctrl_dev **ptr, *pctldev;
 
	// 分配用于存储pinctrl_dev指针的内存
	ptr = devres_alloc(devm_pinctrl_dev_release, sizeof(*ptr), GFP_KERNEL);
	if (!ptr)
		return ERR_PTR(-ENOMEM);
 
	// 注册pinctrl设备
	pctldev = pinctrl_register(pctldesc, dev, driver_data);
	if (IS_ERR(pctldev)) {
		devres_free(ptr);
		return pctldev;
	}
 
	// 将pinctrl_dev指针存储到devres中
	*ptr = pctldev;
	devres_add(dev, ptr);
 
	return pctldev;
}
```


### 6、函数详解：
> 这个函数用于**注册pinctrl设备，并将其与设备关联起来**。下面是对每个部分的详细解释：
> 
> （1）第8-10行：使用devres_alloc函数为存储pinctrl_dev指针的变量ptr分配内存。devres_alloc函数是用于管理设备资源的函数，它在设备的资源列表中分配内存。这里分配的内存大小为sizeof(`*ptr`)字节，即一个pinctrl_dev指针的大小。如果内存分配失败，则返回-ENOMEM错误码。
> 
> （2）第13-17行：调用pinctrl_register函数注册pinctrl设备。该函数将pinctrl_desc结构体、设备指针dev和驱动程序数据driver_data作为参数，并返回注册后的pinctrl_dev指针。如果注册失败（返回错误码），则释放之前分配的内存，并返回相应的错误码。
> 
> （3）第20-21行：将pinctrl_dev指针存储到ptr指向的内存位置。接下来，使用**devres_add函数将ptr添加到设备的资源列表中。这样，在设备释放时，会自动释放之前分配的内存。**
> 

### 7、pinctrl_register函数(4<---)(❤️)
- 2 注册并启用pinctrl设备

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
### 8、函数详解：
> 这个函数用于注册并启用pinctrl设备。以下是对每个部分的详细解释：
> 
> （1）第8-10行：调用pinctrl_init_controller函数初始化pinctrl控制器。该函数接受pinctrl_desc结构体、设备指针dev和驱动程序数据driver_data作为参数，并返回一个指向已初始化的pinctrl_dev结构体的指针。
> 
> （2）第13-15行：调用pinctrl_enable函数启用pinctrl控制器。该函数接受一个pinctrl_dev结构体指针作为参数，并返回一个代表错误码的整数值。
> 
> 至此，关于rk3568的pinctrl probe函数的分析就完成了，这个时候可能大家还是感觉乱乱的，大家不要着急，会在下面的章节中继续填充pinctrl子系统的框架。



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


