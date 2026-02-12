---
title: "RK3568驱动指南｜第七篇 设备树-第61章 实例分析：pinctrl_rk3568设备树-CSDN博客"
source: "https://blog.csdn.net/BeiJingXunWei/article/details/134260474"
author:
  - "[[成就一亿技术人!]]"
  - "[[hope_wisdom 发出的红包]]"
published:
created: 2025-09-14
description: "文章浏览阅读2.5k次。引脚复用通过硬件和软件的方式实现。可以看到功能4对应串口4的发送端和接收端，pinctrl服务端的配置和数据手册中的引脚复用功能是一一对应，那如果要将RK_PB1和RK_PB2设置为GPIO功能要如何设置呢，从上图可以看到GPIO对应功能0，所以可以通过以下pinctrl内容将设置RK_PB1和RK_PB2设置为GPIO功能（pinctrl-0 属性指定了第一个状态 default 对应的引脚配置，但与之前的例子不同的是，它引用了两个引脚描述符：pinctrl_hog_1 和 pinctrl_hog_2。_rk3568设备树"
tags:
  - "clippings"
---

# 备注(声明)：


# 参考文章：




# 一、pinmux介绍

## Pinmux（引脚复用）
### 1 、在系统中配置和管理引脚功能的过程


### 2 、硬件层面
> 芯片设计会为每个引脚提供多个功能的选择。这些功能通常由芯片厂商在芯片规格文档中定义。**通过编程设置寄存器或开关**，可以选择某个功能来连接引脚。这种硬件层面的配置通常是**由引脚控制器（Pin Controller）或引脚复用控制器（Pin Mux Controller）负责管理**。




### 3 、软件层面
> 操作系统或设备驱动程序需要了解和配置引脚的功能。它们使用**设备树**（Device Tree）或设备树绑定（Device Tree Bindings）来**描述和配置引脚的功能**。在设备树中，可以指定引脚的复用功能，将其连接到特定的硬件接口或功能。操作系统或设备驱动程序在启动过程中解析设备树，并根据配置对引脚进行初始化和设置。



### 4 、一般在核心板原理图都会标注出每个管脚的复用功能(❤️)
![嵌入式知识学习（通用扩展）/linux驱动入门/第七、八期 设备树/assets/第61章 实例分析：pinctrl/file-20260119094101719.png](assets/第61章%20实例分析：pinctrl/file-20260119094101719.png)


### 5、


## BGA引脚标号(❤️)
- 2 比如上图：GPIO3_B1_d，对应的BGA引脚标号为AG1

### 6、 BGA（Ball Grid Array，球栅阵列）封装
> **引脚标号是用于唯一标识每个引脚的标识符**。这些标号通常由芯片制造商定义，并在芯片的规格文档或数据手册中提供。
> 
### 7、在芯片的封装底部的焊盘上进行标记


### 8、RK3568的引脚标号图如下：
![嵌入式知识学习（通用扩展）/linux驱动入门/第七、八期 设备树/assets/第61章 实例分析：pinctrl/file-20260119094544503.png](assets/第61章%20实例分析：pinctrl/file-20260119094544503.png)

可以看到纵向为A-AH的28个字母类型标号，横向为1-28的28个字母类型标号

### 9、根据BGA位置制作的复用功能图
- 1 在对应的3568数据手册中
![嵌入式知识学习（通用扩展）/linux驱动入门/第七、八期 设备树/assets/第61章 实例分析：pinctrl/file-20260119094650465.png](assets/第61章%20实例分析：pinctrl/file-20260119094650465.png)

> **黑色框代表被保留的引脚**，其他有颜色的框一般为电源和地，白色的框代表有具体复用功能的引脚。





# 二、使用pinctrl设置复用关系

## pinctrl（引脚控制）
### 1 、描述和配置硬件设备上的引脚功能和连接方式


### 2 、


## 客户端（Client）

### 3 、例1：pinctrl-names = "default";(❤️)
```d
node {
    pinctrl-names = "default";
    pinctrl-0 = <&pinctrl_hog_1>;
}
```

> 在例1中，pinctrl-names 属性定义了一个状态名称：default。
> 
> **pinctrl-0 属性指定了第一个状态 default 对应的引脚配置。**
> 
> <&pinctrl_hog_1> 是一个引脚描述符，它引用了一个名为 **pinctrl_hog_1 的引脚控制器节点**。这表示在 **default 状态下，设备的引脚配置将使用 pinctrl_hog_1 节点中定义的配置**。




### 4 、例2：pinctrl-names = "default", "wake up";

```d
node {
    pinctrl-names = "default", "wake up";
    pinctrl-0 = <&pinctrl_hog_1>;
    pinctrl-1 = <&pinctrl_hog_2>;
}
```

> 在例2中，pinctrl-names 属性定义了两个状态名称：default 和 wake up。
> 
> pinctrl-0 属性指定了第一个状态 default 对应的引脚配置，引用了 pinctrl_hog_1 节点。
> 
> pinctrl-1 属性指定了第二个状态 wake up 对应的引脚配置，引用了 pinctrl_hog_2 节点。
> 
> 这意味着**设备可以处于两个不同的状态之一，每个状态分别使用不同的引脚配置**。


### 5、例3：pinctrl-0 = <&pinctrl_hog_1 &pinctrl_hog_2>;
```d
node {
    pinctrl-names = "default";
    pinctrl-0 = <&pinctrl_hog_1 &pinctrl_hog_2>;
}
```

> pinctrl-0 属性指定了第一个状态 default 对应的引脚配置，但与之前的例子不同的是，它引用了两个引脚描述符：pinctrl_hog_1 和 pinctrl_hog_2。
> 
> 这表示在 default 状态下，设备的引脚配置将使用 pinctrl_hog_1 和 pinctrl_hog_2 两个节点中定义的配置。这种方式可以**将多个引脚控制器的配置组合在一起，以满足特定状态下的引脚需求。**




### 6、






##  服务端（Server）
### 1 、定义引脚配置的部分，包含引脚组和引脚描述符
- 1 服务端在设备树中定义了 pinctrl 节点，其中包含引脚组和引脚描述符的定义。

### 2 、为客户端提供引脚配置选择


### 3 、/rk3568-pinctrl.dtsi：所有的复用关系(❤️)
- 1 arch/arm64/boot/dts/rockchip/rk3568-pinctrl.dtsi
![嵌入式知识学习（通用扩展）/linux驱动入门/第七、八期 设备树/assets/第61章 实例分析：pinctrl/file-20260203113246668.png](assets/第61章%20实例分析：pinctrl/file-20260203113246668.png)




### 4 、uart4的pinctrl服务端内容如下：
![嵌入式知识学习（通用扩展）/linux驱动入门/第七、八期 设备树/assets/第61章 实例分析：pinctrl/file-20260203113547766.png](assets/第61章%20实例分析：pinctrl/file-20260203113547766.png)


#### 解析：
> 其中<3 RK_PB1 4 &pcfg_pull_up>和<3 RK_PB2 4 &pcfg_pull_up>分别表示将GPIO3的PB1引脚设置为**功能4**，将GPIO3的PB2也设置为功能4，且电器属性都会设置为上拉。通过查找原理图可以得到两个引脚**在BGA封装位置分别为AG1和AF2**，如下图（图 61-6）所示：
![嵌入式知识学习（通用扩展）/linux驱动入门/第七、八期 设备树/assets/第61章 实例分析：pinctrl/file-20260203114603499.png](assets/第61章%20实例分析：pinctrl/file-20260203114603499.png)



#### 通过封装编号在数据手册了解引脚复用：(❤️)
![嵌入式知识学习（通用扩展）/linux驱动入门/第七、八期 设备树/assets/第61章 实例分析：pinctrl/file-20260203114801109.png](assets/第61章%20实例分析：pinctrl/file-20260203114801109.png)

![嵌入式知识学习（通用扩展）/linux驱动入门/第七、八期 设备树/assets/第61章 实例分析：pinctrl/file-20260203115032463.png](assets/第61章%20实例分析：pinctrl/file-20260203115032463.png)

> 可以看到**功能4对应串口4的发送端和接收端**，pinctrl服务端的配置和数据手册中的引脚复用功能是一一对应，


#### 设置为GPIO功能配置：
> 那如果要将RK_PB1和RK_PB2设置为GPIO功能要如何设置呢，从上图可以看到GPIO**对应功能0**，所以可以通过以下pinctrl内容将设置RK_PB1和RK_PB2设置为GPIO功能（事实上如果不对该管脚进行功能复用该**引脚默认就会设置为GPIO功能**）：
> 

```c
	<3 RK_PB1 0 &pcfg_pull_up>,                                                                                                  
	<3 RK_PB2 0 &pcfg_pull_up>;
```

#### 看客户端对uart4服务端的引用(❤️)
- 1 arch/arm64/boot/dts/rockchip/rk3568-evb1-ddr4-v10-linux.dts
![嵌入式知识学习（通用扩展）/linux驱动入门/第七、八期 设备树/assets/第61章 实例分析：pinctrl/file-20260204162843887.png](assets/第61章%20实例分析：pinctrl/file-20260204162843887.png)

> 通过在客户端中引用服务端的引脚描述符，设备树可以将客户端和服务端的引脚配置关联起来。这样，在设备树被解析和处理时，操作系统和设备驱动程序可以根据客户端的需求，查找并应用适当的引脚配置。

### 5、


# 三、pinctrl实例编写

## 将led的控制引脚复用为GPIO模式。


## 对rk3568的设备树结构认识
### 1 、整理好的设备树之间包含关系列表如下(❤️)
![嵌入式知识学习（通用扩展）/linux驱动入门/第七、八期 设备树/assets/第61章 实例分析：pinctrl/file-20260204163638872.png](assets/第61章%20实例分析：pinctrl/file-20260204163638872.png)



### 2 、通过默认配置文件可以了解(❤️)
- 1 device/rockchip/rk356x/BoardConfig-rk3568-evb1-ddr4-v10.mk
- 



### 3 、Led在rk3568-evb.dtsi设备树中已经被正常配置了
![嵌入式知识学习（通用扩展）/linux驱动入门/第七、八期 设备树/assets/第61章 实例分析：pinctrl/file-20260204163745804.png](assets/第61章%20实例分析：pinctrl/file-20260204163745804.png)

- 2 当一个引脚没有被复用为任何功能时，默认就是GPIO功能



### 4 、仍旧使用pinctrl对led进行配置，从而熟练pinctrl

#### 填写led节点客户端：

- 1 进入到rk3568-evb1-ddr4-v10.dtsi设备树中

```d
 my_led: led {
    compatible = "topeet,led";
    gpios = <&gpio0 RK_PB7 GPIO_ACTIVE_HIGH>;
    pinctrl-names = "default";
    pinctrl-0 = <&rk_led_gpio>;
    };   
```
- 2 可以仿照rk_485_ctl节点

> 第1行：节点名称为 led，标签名为my_led。
> 
> 第2行：compatible 属性指定了设备的兼容性标识，即设备与驱动程序之间的匹配规则。在这里，设备标识为 "topeet,led"，表示该 LED 设备与名为 "topeet,led" 的驱动程序兼容。
> 
> 第3行：gpios 属性指定了与LED相关的GPIO（通用输入/输出）引脚配置。
> 
> 第4行：pinctrl-names 属性指定了与引脚控制相关的命名。default表示状态 0
> 
> 第5行：pinctrl-0 属性指定了与 pinctrl-names 属性中命名的引脚控制相关联的实际引脚控制器配置。<&rk_led_gpio> 表示引用了名为 rk_led_gpio 的引脚控制器配置。

#### 仿写led控制引脚pinctrl服务端节点：(❤️)
```d
rk_led{
		rk_led_gpio:rk-led-gpio {
			rockchip,pins = <0 RK_PB7 RK_FUNC_GPIO &pcfg_pull_none>;
		};
	};
```


- 1 添加完成之后如下图
![嵌入式知识学习（通用扩展）/linux驱动入门/第七、八期 设备树/assets/第61章 实例分析：pinctrl/file-20260204164536383.png](assets/第61章%20实例分析：pinctrl/file-20260204164536383.png)




### 5、一般服务端都不用自己写(❤️)




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


