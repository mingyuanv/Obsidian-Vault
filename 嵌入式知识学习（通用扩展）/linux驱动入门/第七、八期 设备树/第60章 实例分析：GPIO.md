---
title: "RK3568驱动指南｜第七期-设备树-第60章 实例分析：GPIO_gpio-ranges-CSDN博客"
source: "https://blog.csdn.net/BeiJingXunWei/article/details/134037994"
author:
  - "[[成就一亿技术人!]]"
  - "[[hope_wisdom 发出的红包]]"
published:
created: 2025-09-14
description: "文章浏览阅读2.7k次。其中gpio0节点是在内核源码的“/arch/arm64/boot/dts/rockchip/rk3568.dtsi”设备树的3549-3560行定义的，而ft5x06: ft5x06@38触摸芯片节点是在内核源码的“/arch/arm64/boot/dts/rockchip/topeet_rk3568_lcds.dtsi”设备树的301-313行定义的。&gpio0 是引脚控制器的引用，RK_PB7 是引脚的编号或标识，GPIO_ACTIVE_HIGH 表示该 GPIO 引脚的活动电平是高电平。_gpio-ranges"
tags:
  - "clippings"
---

# 备注(声明)：


# 参考文章：
[RK3568驱动指南｜第七期-设备树-第60章 实例分析：GPIO\_gpio-ranges-CSDN博客](https://blog.csdn.net/BeiJingXunWei/article/details/134037994)



# 一、GPIO相关属性

## RK ft5x06设备树节点
### 1 、源码中的ft5x06设备树节点
```d
gpio0: gpio@fdd60000 {
    compatible = "rockchip,gpio-bank";
    reg = <0x0 0xfdd60000 0x0 0x100>;
    interrupts = <GIC_SPI 33 IRQ_TYPE_LEVEL_HIGH>;
    clocks = <&pmucru PCLK_GPI00>, <&pmucru DBCLK_GPI00>;
    gpio-controller;
    #gpio-cells = <2>;
    gpio-ranges = <&pinctrl 0 0 32>;
    interrupt-controller;
    #interrupt-cells = <2>;
};
 
ft5x06: ft5x06@38 { 
    status = "disabled";
    compatible = "edt,edt-ft5306";
    reg = <0x38>;
    touch-gpio = <&gpio0 RK_PB5 IRQ_TYPE_EDGE_RISING>;
    interrupt-parent = <&gpio0>;
    interrupts = <RK_PB5 IRQ_TYPE_LEVEL_LOW>;
    reset-gpios = <&gpio0 RK_PB6 GPIO_ACTIVE_LOW>;
    touchscreen-size-x = <800>;
    touchscreen-size-y = <1280>;
    touch_type = <1>;
};
```

### 2 、节点在源码中的位置
- 2 gpio0节点是在内核源码的“/arch/arm64/boot/dts/rockchip/rk3568.dtsi”设备树的3549-3560行定义

- 2 ft5x06: ft5x06@38触摸芯片节点是在内核源码的“/arch/arm64/boot/dts/rockchip/topeet_rk3568_lcds.dtsi”设备树的301-313行定义


### 3 、



### 4 、

## gpio-controller 

### 5、标识一个设备节点作为GPIO控制器(❤️)
> 通常会**定义一组GPIO引脚**，并**提供相关的GPIO控制和配置功能**。


### 6、GPIO控制器是负责管理和控制GPIO引脚的硬件模块或驱动程序。



### 7、其他节点引用
> **其他设备节点可以使用该GPIO控制器来控制和管理其GPIO引脚。**
> 
> 通过使用gpio-controller属性，设备树可以明确标识出GPIO控制器设备节点，使系统可以正确识别和管理GPIO引脚的配置和控制。



### 8、



## `#gpio-cells`
### 1 、指定GPIO引脚描述符的编码方式
> `GPIO引脚描述符`是用于标识和配置GPIO引脚的一组值，例如**引脚编号、引脚属性**等。

### 2 、编码GPIO引脚描述符的单元数(❤️)
> **通常，这个值为2。**

- 1 决定下面单元数。
```d
ft5x06: ft5x06@38 { 
    .....
    reset-gpios = <&gpio0 RK_PB6 GPIO_ACTIVE_LOW>;
    .....
};
```




### 3 、

## gpio-ranges
### 4 、描述GPIO范围映射(❤️)


### 5、描述具有大量GPIO引脚的GPIO控制器


### 6、将本地编号映射到实际的引脚编号
> 在设备树中，GPIO控制器的每个引脚都有一个本地编号，用于在控制器内部进行引脚寻址。然而，这些本地编号并不一定与外部引脚的物理编号或其他系统中使用的编号一致。为了**解决这个问题**，可以使用gpio-ranges属性


### 7、举例分析：(❤️)
```d
    gpio-ranges = <&pinctrl 0 0 32>;
```
> （1）**外部**引脚编号的起始值。
> 
> （2）GPIO控制器**内部本地编号的起始值**。
> 
> （3）**引脚范围的大小（引脚数量）**。

> 其中<&pinctrl>表示引用了名为pinctrl的引脚控制器节点，0 0 32表示外部引脚从0开始，控制器本地编号从0开始，共映射了32个引脚。





### 8、



## gpio引脚描述属性
### 1 、reset-gpios 
```d
ft5x06: ft5x06@38 { 
    .....
    reset-gpios = <&gpio0 RK_PB6 GPIO_ACTIVE_LOW>;
    .....
};
```


### 2 、相关宏定义文件：(❤️)

#### rockchip.h

- 1 内核源码目录下的“include/dt-bindings/pinctrl/rockchip.h”头文件中

```d
/* SPDX-License-Identifier: GPL-2.0-or-later */
/*
 * Header providing constants for Rockchip pinctrl bindings.
 *
 * Copyright (c) 2013 MundoReader S.L.
 * Author: Heiko Stuebner <heiko@sntech.de>
 */

#ifndef __DT_BINDINGS_ROCKCHIP_PINCTRL_H__
#define __DT_BINDINGS_ROCKCHIP_PINCTRL_H__

#define RK_PA0		0
#define RK_PA1		1
#define RK_PA2		2
#define RK_PA3		3
#define RK_PA4		4
#define RK_PA5		5
#define RK_PA6		6
#define RK_PA7		7
#define RK_PB0		8
#define RK_PB1		9
#define RK_PB2		10
#define RK_PB3		11
#define RK_PB4		12
#define RK_PB5		13
#define RK_PB6		14
#define RK_PB7		15
#define RK_PC0		16
#define RK_PC1		17
#define RK_PC2		18
#define RK_PC3		19
#define RK_PC4		20
#define RK_PC5		21
#define RK_PC6		22
#define RK_PC7		23
#define RK_PD0		24
#define RK_PD1		25
#define RK_PD2		26
#define RK_PD3		27
#define RK_PD4		28
#define RK_PD5		29
#define RK_PD6		30
#define RK_PD7		31

#define RK_FUNC_GPIO	0

#endif


```

#### gpio.h
- 1 kernel/include/dt-bindings/gpio/gpio.h

```d
/* SPDX-License-Identifier: GPL-2.0 */
/*
 * This header provides constants for most GPIO bindings.
 *
 * Most GPIO bindings include a flags cell as part of the GPIO specifier.
 * In most cases, the format of the flags cell uses the standard values
 * defined in this header.
 */

#ifndef _DT_BINDINGS_GPIO_GPIO_H
#define _DT_BINDINGS_GPIO_GPIO_H

/* Bit 0 express polarity */
#define GPIO_ACTIVE_HIGH 0
#define GPIO_ACTIVE_LOW 1

/* Bit 1 express single-endedness */
#define GPIO_PUSH_PULL 0
#define GPIO_SINGLE_ENDED 2

/* Bit 2 express Open drain or open source */
#define GPIO_LINE_OPEN_SOURCE 0
#define GPIO_LINE_OPEN_DRAIN 4

/*
 * Open Drain/Collector is the combination of single-ended open drain interface.
 * Open Source/Emitter is the combination of single-ended open source interface.
 */
#define GPIO_OPEN_DRAIN (GPIO_SINGLE_ENDED | GPIO_LINE_OPEN_DRAIN)
#define GPIO_OPEN_SOURCE (GPIO_SINGLE_ENDED | GPIO_LINE_OPEN_SOURCE)

/* Bit 3 express GPIO suspend/resume and reset persistence */
#define GPIO_PERSISTENT 0
#define GPIO_TRANSITORY 8

/* Bit 4 express pull up */
#define GPIO_PULL_UP 16

/* Bit 5 express pull down */
#define GPIO_PULL_DOWN 32

#endif

```


### 3 、

## 其他属性

### 4 、举例：
```d
gpio-controller@00000000 {
    compatible = "foo";
    reg = <0x00000000 0x1000>;
    gpio-controller;
    #gpio-cells = <2>;
    ngpios = <18>;
    gpio-reserved-ranges = <0 4>, <12 2>;
    gpio-line-names = "MMC-CD", "MMC-WP",
                      "voD eth", "RST eth", "LED R",
                      "LED G", "LED B", "col A",
                      "col B", "col C", "col D",
                      "NMI button", "Row A", "Row B",
                      "Row C", "Row D", "poweroff",
                      "reset";
};
```


### 5、ngpios
> 第6行的ngpios 属性**指定了 GPIO 控制器所支持的 GPIO 引脚数量**。它表示该设备上可用的 GPIO 引脚的总数。在这个例子中，ngpios 的值为 18，意味着该 GPIO 控制器支持 18 个 GPIO 引脚。


### 6、gpio-reserved-ranges
> 第7行的gpio-reserved-ranges属性**定义了保留的GPIO范围**。每个范围由两个整数值表示，用尖括号括起来。保留的GPIO范围意味着这些GPIO引脚**不可用或已被其他设备或功能保留**。在这个例子中，有两个保留范围：<0 4>和<12 2>。<0 4>表示**从第0个引脚开始的连续4个引脚被保留**，而<12 2>表示从第12个引脚开始的连续2个引脚被保留。



### 7、gpio-line-names
> 第8行的gpio-line-names 属性**定义了GPIO引脚的名称**，以逗号分隔。**每个名称对应一个 GPIO 引脚**。这些名称用于标识和识别每个GPIO引脚的作用或连接的设备。在这个例子中，gpio-line-names属性列出了多个GPIO引脚的名称，如 "MMC-CD"、"MMC-WP"、"voD eth" 等等。通过这些名称，可以清楚地了解每个GPIO引脚的功能或用途。
> 


### 8、




# 二、中断实例编写

## RK3568上LED灯的中断设备树。
### 1 、LED原理图
![嵌入式知识学习（通用扩展）/linux驱动入门/第七、八期 设备树/assets/第60章 实例分析：GPIO/file-20260116185204075.png](assets/第60章%20实例分析：GPIO/file-20260116185204075.png)

- 1 对应的引脚为GPIO0_B7。

### 2 、led的驱动文件：compatible(❤️)
- 1 drivers/drivers/leds/leds-gpio.c
![嵌入式知识学习（通用扩展）/linux驱动入门/第七、八期 设备树/assets/第60章 实例分析：GPIO/file-20260116185243072.png](assets/第60章%20实例分析：GPIO/file-20260116185243072.png)


- 2 compatible匹配值为gpio-leds。

### 3 、编写完成的设备树如下
```d
/dts-v1/;
 
#include "dt-bindings/pinctrl/rockchip.h"
#include "dt-bindings/gpio/gpio.h"
/{
	model = "This is my devicetree!";
 
	led led@1 {
		compatible = "gpio-leds";
		gpios = <&gpio0 RK_PB7 GPIO_ACTIVE_HIGH>
	};
};
```


### 4 、

## 其他SOC ft5x06设备树对比

### 5、恩智浦
```d
gpio1: gpio@0209c000 {
    compatible = "fsl,inx6ul-gpio", "fsl,imx35-gpio";
    reg = <0x0209c000 0x4000>;
    interrupts = <GIC_SPI 66 IRQ_TYPE_LEVEL_HIGH>, <GIC_SPI 67 IRQ_TYPE_LEVEL_HIGH>;
    gpio-controller;
    #gpio-cells = <2>;
    interrupt-controller;
    #interrupt-cells = <2>;
 
    edt-ft5x06@38 {
        compatible = "edt,edt-ft5306", "edt,edt-ft5x06", "edt,edt-ft5406";
        pinctrl-names = "default";
        pinctrl-0 = <&ts_int_pin &ts_reset_pin>;
        reg = <0x38>;
        interrupt-parent = <&gpio1>;
        interrupts = <9 0>;
        reset-gpios = <&gpio5 9 GPIO_ACTIVE_LOW>;
        irq-gpios = <&gpio1 9 GPIO_ACTIVE_LOW>;
        status = "disabled";
    };
};
```

### 6、三星
```d
gpio_c: gpioc {
    compatible = "gpio-controller";
    #gpio-cells = <2>;
    interrupt-controller;
    #interrupt-cells = <2>;
};
 
ft5x06: ft5x06038 {
    compatible = "edt,edt-ft5406";
    reg = <0x38>;
    pinctrl-names = "default";
 
    #if defined(RGB_1024x600) || defined(RGB_800x480)
    pinctrl-0 = <&tsc2007_irq>;
    interrupt-parent = <&gpio_c>;
    interrupts = <26 IRQ_TYPE_EDGE_FALLING>;
    #endif
 
    #if defined(LvDs_800×1280) || defined(LvDS_1024x768)
    pinctrl-0 = <&gt911_irq>;
    interrupt-parent = <&gpio_b>;
    interrupts = <29 IRQ_TYPE_EDGE_FALLING>;
    #endif
 reset-gpios = <&gpio_e 30 0>;
};
```

### 7、不同厂商对于gpio的配置都是类似的，只是里面的参数有些许区别


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


