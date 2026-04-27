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
url: https://blog.csdn.net/BeiJingXunWei/article/details/135545864?ops_request_misc=%257B%2522request%255Fid%2522%253A%252205b229a8b81852964598028d108062cf%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fblog.%2522%257D&request_id=05b229a8b81852964598028d108062cf&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~blog~first_rank_ecpm_v1~rank_v31_ecpm-1-135545864-null-null.nonecase&utm_term=%E7%AC%AC120%E7%AB%A0&spm=1018.2226.3001.4450
title: "RK3568驱动指南｜第十一篇 pinctrl子系统-第120章 pinctrl子系统的引入_鲁班猫 rk 3568 dts 设置 spi pinctrl 说明-CSDN博客"
description: "文章浏览阅读2.1k次，点赞29次，收藏24次。在前面设备树相关的章节中已经对pinctrl节点的编写和使用进行了讲解，设备树的pinctrl可以分为客户端和服务端两个部分，在pinctrl客户端可以指定引脚描述、引脚组描述和配置描述，以满足其特定的功能和需求，不同厂商在客户端内容的编写格式是相同的。在上面的pinctrl节点中，描述了RK3568 GPIO控制器的配置和使用方式，pinctrl节点总共描述了五个GPIO控制器，分别是gpio0、gpio1、gpio2、gpio3和gpio4。接下来对rk3568的pinctrl设备树进行详细的讲解。_鲁班猫 rk 3568 dts 设置 spi pinctrl 说明"
host: blog.csdn.net
```




# 一、pinctrl子系统的引入

## pinctrl子系统简介：
### 1 、管理和配置通用输入/输出（GPIO）引脚的框架(❤️)


### 2 、也符合Linux内核的设备模型 规范


### 3 、分为设备、驱动、总线和类四个部分



### 4 、

## pinctrl 设备树（服务端）

### 5、pinctrl节点，具体内容如下
- 1 rk3568.dtsi设备树根节点下 

> 描述了RK3568 **GPIO控制器 的配置和使用方式**，pinctrl节点总共描述了五个GPIO控制器，分别是gpio0、gpio1、gpio2、gpio3和gpio4。通过这些GPIO控制器节点，可以在设备树中配置和控制RK3568芯片上的GPIO引脚，包括设置引脚功能、中断处理等。

```c
   pinctrl: pinctrl {
        compatible = "rockchip,rk3568-pinctrl";
        rockchip,grf = <&grf>;
        rockchip,pmu = <&pmugrf>;
        #address-cells = <2>;
        #size-cells = <2>;
        ranges;
 
        gpio0: gpio@fdd60000 {
            compatible = "rockchip,gpio-bank";
            reg = <0x0 0xfdd60000 0x0 0x100>;
            interrupts = <GIC_SPI 33 IRQ_TYPE_LEVEL_HIGH>;
            clocks = <&pmucru PCLK_GPIO0>, <&pmucru DBCLK_GPIO0>;
 
            gpio-controller;
            #gpio-cells = <2>;
            gpio-ranges = <&pinctrl 0 0 32>;
            interrupt-controller;                                                                                                                                                                                                     
            #interrupt-cells = <2>;
        };
 
        gpio1: gpio@fe740000 {
            compatible = "rockchip,gpio-bank";
            reg = <0x0 0xfe740000 0x0 0x100>;
            interrupts = <GIC_SPI 34 IRQ_TYPE_LEVEL_HIGH>;
            clocks = <&cru PCLK_GPIO1>, <&cru DBCLK_GPIO1>;
 
            gpio-controller;
            #gpio-cells = <2>;
            gpio-ranges = <&pinctrl 0 32 32>;
            interrupt-controller;
            #interrupt-cells = <2>;
        };   
 
        gpio2: gpio@fe750000 {
            compatible = "rockchip,gpio-bank";
            reg = <0x0 0xfe750000 0x0 0x100>;
            interrupts = <GIC_SPI 35 IRQ_TYPE_LEVEL_HIGH>;
            clocks = <&cru PCLK_GPIO2>, <&cru DBCLK_GPIO2>;
 
            gpio-controller;
            #gpio-cells = <2>; 
            gpio-ranges = <&pinctrl 0 64 32>;
            interrupt-controller;
            #interrupt-cells = <2>; 
        };   
 
        gpio3: gpio@fe760000 {
            compatible = "rockchip,gpio-bank";
            reg = <0x0 0xfe760000 0x0 0x100>;
            interrupts = <GIC_SPI 36 IRQ_TYPE_LEVEL_HIGH>;
            clocks = <&cru PCLK_GPIO3>, <&cru DBCLK_GPIO3>;
 
            gpio-controller;
            #gpio-cells = <2>;
            gpio-ranges = <&pinctrl 0 96 32>;
            interrupt-controller;
            #interrupt-cells = <2>;
        };
 
        gpio4: gpio@fe770000 {
            compatible = "rockchip,gpio-bank";
            reg = <0x0 0xfe770000 0x0 0x100>;
            interrupts = <GIC_SPI 37 IRQ_TYPE_LEVEL_HIGH>;
            clocks = <&cru PCLK_GPIO4>, <&cru DBCLK_GPIO4>;
 
            gpio-controller;
            #gpio-cells = <2>;
            gpio-ranges = <&pinctrl 0 128 32>;
            interrupt-controller;
            #interrupt-cells = <2>;
        };
    };
};
 
#include "rk3568-pinctrl.dtsi"
```

- 1 在设备树的最下方通过include包含了rk3568-pinctrl.dtsi设备树

### 6、rk3568-pinctrl.dtsi设备树(❤️)
- 1 包含了所有复用功能的配置
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十一期_pinctrl子系统/assets/第120章 pinctrl子系统的引入/file-20260316094059898.png]]

> 都是由**瑞芯微原厂BSP工程师编写的，我们只需知道如何使用即可**，而pinctrl客户端设备树是由我们自己根据特定需求来编写的，具体可以回顾前面设备树相关的章节，这里就不再进行赘述。





### 7、pinctrl的驱动文件
- 1 内核源码的“/driver/pinctrl/pinctrl-rockchip.c”

![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十一期_pinctrl子系统/assets/第120章 pinctrl子系统的引入/file-20260316094252571.png]]


### 8、



## pinctrl 驱动
- 1 kernel/driver/pinctrl/pinctrl-rockchip.c

### 1 、驱动的入口函数，具体内容如下
> 可以看到pinctrl驱动使用的是**platform 总线**，当设备和驱动匹配成功之后会进入**rockchip_pinctrl_probe函数进行初始化**

```c
static struct platform_driver rockchip_pinctrl_driver = {
    .probe      = rockchip_pinctrl_probe,
    .driver = {
        .name   = "rockchip-pinctrl",
        .pm = &rockchip_pinctrl_dev_pm_ops,
        .of_match_table = rockchip_pinctrl_dt_match,
    },
};
 
static int __init rockchip_pinctrl_drv_register(void)
{                                                                                                                                                                                                                                     
    return platform_driver_register(&rockchip_pinctrl_driver);
}
postcore_initcall(rockchip_pinctrl_drv_register);
 
static void __exit rockchip_pinctrl_drv_unregister(void)
{
    platform_driver_unregister(&rockchip_pinctrl_driver);
}
```

### 2 、probe函数的具体内容如下
> 上面Probe函数的作用是**初始化和配置Rockchip GPIO控制器，并将相关信息存储在rockchip_pinctrl结构体 中**，最后**注册相关设备和GPIO接口**，关于Probe函数会在后面的小节中进行更加具体的分析。


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
### 3 、


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


