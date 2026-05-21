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
url: https://blog.csdn.net/beijingxunwei/article/details/135569175?ops_request_misc=elastic_search_misc&request_id=1cb427dfcedd148bf28da484eecc17f7&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~ElasticSearch~search_v2-1-135569175-null-null.nonecase&utm_term=%E7%AC%AC130%E7%AB%A0&spm=1018.2226.3001.4450
title: "RK3568驱动指南｜第十二篇 GPIO子系统-第130章 GPIO的调试方法_3568配置输入gpio-CSDN博客"
description: "文章浏览阅读2.2k次，点赞21次，收藏21次。6. /sys/kernel/debug/pinctrl/*/pinconf-pins：这些文件包含了GPIO引脚的配置信息，如输入/输出模式、上拉/下拉设置等。如下图所示，我们进入/sys/kernel/debug/目录下。5. /sys/kernel/debug/pinctrl/*/pingroups：该路径提供有关用于配置和控制系统上的 GPIO引脚的引脚组的信息。2. /sys/kernel/debug/pinctrl/*/pins：这些文件列出了GPIO的引脚编号，可以查看GPIO编号。_3568配置输入gpio"
host: blog.csdn.net
```




# 一、GPIO的调试方法

## 方法一：debugfs
### 1 、Linux内核提供的一个调试文件系统


### 2 、查看和调试内核中的各种信息，包括GPIO的使用情况
> 通过挂载debugfs文件系统，并**查看/sys/kernel /debug/目录下的相关文件**，可以**获取GPIO的状态，配置和其他调试信息**。如下图所示，我们进入/sys/kernel/debug/目录下。



### 3 、/sys/kernel/debug/目录
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第130章 GPIO的调试方法/file-20260324180813497.png]]


### 4 、Linux内核源码配置debugfs方法：
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第130章 GPIO的调试方法/file-20260324180956364.png]]

- 2 重新编译内核源码，烧写内核镜像

### 5、debugfs的使用：(❤️)
> 如果没有debugfs，可以使用以下命令进行挂载:
> mount -t debugfs none /sys/kernel/debug/

- 1 查看GPIO的复用、状态信息。
```c
cat /sys/kernel/debug/gpio
```

### 6、


### 7、




## 方法二：pinctrl
### 1 、/sys/kernel/debug/pinctrl目录
- 1 可以获取有关GPIO控制器的调试信息

### 2 、GPIO引脚的引脚复用配置(❤️)
- 1  `/sys/kernel/debug/pinctrl/*/pinmux-pins`

> 你可以查看每个引脚的功能模式、引脚复用选择以及其他相关的配置信息。我们进入到/sys/kernel/debug/pinctrl/pinctrl-rockchip-pinctrl/下面，输入“cat pinmux-pins”，如下图所示：
> ![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第130章 GPIO的调试方法/file-20260512115225290.png]]



### 3 、查看GPIO编号
- 1  `/sys/kernel/debug/pinctrl/*/pins`

> 我们进入**到/sys/kernel/debug/pinctrl/pinctrl-rockchip-pinctrl/下面**，输入“cat pins”，如下图所示：
> ![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第130章 GPIO的调试方法/file-20260512115332657.png]]



### 4 、查看GPIO编号的范围和对应的控制器名称
- 1 `/sys/kernel/debug/pinctrl/*/gpio-ranges：`

> 这些文件列出了每个GPIO控制器支持的GPIO范围。你可以查看GPIO编号的范围和对应的控制器名称。我们进入**到/sys/kernel/debug/pinctrl/pinctrl-rockchip-pinctrl/下面**，输入“cat gpio-ranges”，如下图所示：
> ![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第130章 GPIO的调试方法/file-20260512115543184.png]]





### 5、查看各个功能模式的名称和对应的引脚列表
- 1 ` /sys/kernel/debug/pinctrl/*/pinmux-functions`

> 这些文件列出了每个功能模式的名称以及与之关联的GPIO引脚。你可以查看各个功能模式的名称和对应的引脚列表。我们进入到/sys/kernel/debug/pinctrl/pinctrl-rockchip-pinctrl/下面，输入“cat pinmux-functions”，如下图所示：
> ![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第130章 GPIO的调试方法/file-20260512115643233.png]]




### 6、查看配置和控制系统 上的 GPIO引脚的引脚组的信息
- 1  `/sys/kernel/debug/pinctrl/*/pingroups：`

> 该路径提供有关用于配置和控制系统 上的 GPIO引脚的引脚组的信息。我们进入到/sys/kernel/debug/pinctrl/pinctrl-rockchip-pinctrl/下面，输入“cat pingroups”，如下图所示：
> ![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第130章 GPIO的调试方法/file-20260512115831983.png]]




### 7、查看和修改GPIO的电气属性(❤️)
- 1 `/sys/kernel/debug/pinctrl/*/pinconf-pins：`

> 这些文件包含了GPIO引脚的配置信息，如**输入/输出模式、上拉/下拉设置**等。你可以查看和修改GPIO的电气属性，以便进行GPIO的调试和配置。我们进入到/sys/kernel/debug/pinctrl/pinctrl-rockchip-pinctrl/下面，输入“cat pinconf-pins”，如下图所示：
> ![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第130章 GPIO的调试方法/file-20260512120043315.png]]





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


