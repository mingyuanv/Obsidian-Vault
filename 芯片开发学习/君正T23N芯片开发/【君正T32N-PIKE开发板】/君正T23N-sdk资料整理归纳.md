---
title: 
aliases: 
tags: 
description:
---

# 随记：




# 一、文档资料
## 1.BSP

### T23 BSP开发参考V1.1.pdf  --->BSP软件开发介绍
$ <span style="background:#b1ffff">make distclean 清除旧配置。</span>

> [!PDF|important] [[芯片开发学习/君正T23N芯片开发/sdk_资料库/君正T23N开发资料/BSP/T23 BSP开发参考V1.1.pdf#page=12&selection=38,0,40,2&color=important|T23 BSP开发参考V1.1, p.12]]
> > T23 必读
> 
> <span style="background:#affad1">编译</span>


> [!PDF|important] [[芯片开发学习/君正T23N芯片开发/sdk_资料库/君正T23N开发资料/BSP/T23 BSP开发参考V1.1.pdf#page=30&selection=127,0,129,4&color=important|T23 BSP开发参考V1.1, p.30]]
> > 6.3<span style="background:#b1ffff"> GPIO</span>
> 
> 

> [!PDF|important] [[芯片开发学习/君正T23N芯片开发/sdk_资料库/君正T23N开发资料/BSP/T23 BSP开发参考V1.1.pdf#page=33&selection=139,0,142,4&color=important|T23 BSP开发参考V1.1, p.33]]
> > 6.6 Motor
> 
> 

> [!PDF|important] [[芯片开发学习/君正T23N芯片开发/sdk_资料库/君正T23N开发资料/BSP/T23 BSP开发参考V1.1.pdf#page=39&selection=60,1,62,4&color=important|T23 BSP开发参考V1.1, p.39]]
> > .11 <span style="background:#b1ffff">Wifi</span>
> 
> 

> [!PDF|important] [[芯片开发学习/君正T23N芯片开发/sdk_资料库/君正T23N开发资料/BSP/T23 BSP开发参考V1.1.pdf#page=55&selection=0,3,40,4&color=important|T23 BSP开发参考V1.1, p.55]]
> > T23 BSP T23 BSP 开发参考 V1.1 Copyright® 2021-2023 Ingenic Semiconductor Co., Ltd. All rights reserved. 52 7.2 wpa_supplicant 使用方法
> 
> 

### T23 SFC开发指南.pdf---->  flash添加介绍

本文档主要介绍 Ingenic T23 SPI flash 的添加以及配置


### T23 IVDC模块应用指南.pdf

本文为 Ingenic-T23 IVDC 模块应用指南，方便用户在使用该模块时快速了解上手。

IVDC（ISP-VPU-Direct-Connect）模块，使数据可以不经过 DDR，直接从 ISP 传输到 Encoder，节省 DDR 存储空间
## 2.IMP **(实现)**
 
### |T23 SDK开发参考V1.1.pdf| ----->  |SDK API和功能介绍|

### |T23 OSD模块使用指南.pdf|  -----> |OSD模块介绍|

IPU 是图像处理单元，全称是（Image Processing Unit）。支持对从 ISP 模块采集的图像到视频显示模块前的数据处理。例如，将特定的信息叠加到视频中，如点阵数据、直线、矩形框、矩形遮挡、图片数据等。 IPU 模块对图像的操作主要包含 OSD 模块和 CSC 模块。OSD 模块主要在视频帧上叠加框线、矩形遮挡、图片等数据；CSC 可以实现把输入的视频帧转化成硬件支持的图像，如 HSV、 NV12、 NV21、RGB32、和 ARGB 模式中任意一种格式。



### |T23 码率控制使用指南.pdf|   ----->|码率控制参数和使用介绍|


## 3.Ingenic tools

  
### |carrier 工具使用指南.pdf|------>   |rtsp播放上位机|


### |fw_printenv使用.pdf| ------>  |fw 软件使用介绍|


### |USBCloner烧录工具指南V2.pdf| ------->  |USB烧录工具使用说明|


## 4、SDK开发

### |T23 SDK安装及使用指南.pdf|    -------->     |SDK开发环境搭建介绍|



### |T23 SDK调试指南.pdf|   |    -------->    |SDK调试说明|


### |T23 PIKE开发板使用指南.pdf|   -------->     |   |PIKE 38板使用说明|


### |T23 文件系统制作指南.pdf|    -------->    |jffs2/squashfs/ubi/yaffs2文件系统制作说明|

### |T23 软件资源编译指南.pdf|     -------->    |SDK软件资源编译指南|

## 5、应用层



## 6、



## 7、






# 二、文件资料

## 1.开发包


opensource
  
|busybox.7z|   |Busybox工具|
|drivers.7z|   |各种驱动文件|
|kernel.7z|   |内核开发包|
|uboot.7z|   |uboot开发包|



   
文件系统
|root-glibc-toolchain540.squashfs|   |Glibc版本squshfs文件系统|
|root-glibc-toolchain540.tar.bz2|   |Glibc版本文件系统资源|
|root-glibc-toolchain540.ubifs|   |Glibc版本ubi文件系统|
|root-uclibc-toolchain540.squashfs|   |Uclibc版本squshfs文件系统|
|root-uclibc-toolchain540.tar.bz2|   |Uclibc版本文件系统资源|
|root-uclibc-toolchain540.ubifs|   |Uclibc版本ubi文件系统|




## 2.工具包

   
|工具链
|mips-gcc540-uclibc0.9.33.2-64bit-r3.3.0.smaller.md5|   |Uclibc工具链对应的md5值|
|mips-gcc540-uclibc0.9.33.2-64bit-r3.3.0.smaller.tar.bz2|   |Uclibc版本工具链|
|mips-gcc540-glibc222-64bit-r3.3.0.smaller.md5|   |Glibc工具链对应的md5|
|mips-gcc540-glibc222-64bit-r3.3.0.smaller.tar.bz2|   |Glibc版本工具链|


   
|板级工具
|bin|   ||
|config|   ||
|factory_test_plan|   |UVC产测demo|
### |gpio_tool_t23|   |gpio读取和设置工具|
E:\sdk\ISVP-T23-1.1.2-20240204\ISVP-T23-1.1.2-20240204\software\zh\Ingenic-SDK-T23-1.1.2-20240204-zh\resource\tools_t23\gpio_tool_t23

[3-使用命令通过sysfs文件系统控制GPIO](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/第十二期_GPIO子系统.one#3-使用命令通过sysfs文件系统控制GPIO&section-id={70166D78-0FC7-4512-B1CF-4A4481F8C206}&page-id={471F55C3-0F87-4888-BC65-7A714608E9A3}&end)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E7%AC%AC%E5%8D%81%E4%BA%8C%E6%9C%9F_GPIO%E5%AD%90%E7%B3%BB%E7%BB%9F.one%7C70166D78-0FC7-4512-B1CF-4A4481F8C206%2F3-%E4%BD%BF%E7%94%A8%E5%91%BD%E4%BB%A4%E9%80%9A%E8%BF%87sysfs%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E6%8E%A7%E5%88%B6GPIO%7C471F55C3-0F87-4888-BC65-7A714608E9A3%2F%29&wdpartid=%7b6260DF4F-45D8-47AA-89D1-7DBACA718547%7d%7b1%7d&wdsectionfileid=52D4B76BB0FFCF51!s379e81f769634ad2a8a457194a5b5af6))



|Pc tools
|Carrier-V5.1.0.7z|   |PC端播放rtsp上位机|
|rmem_calculator_T23_V1.0.1.xlsx|   |rmem计算表格|
|Uart|   |君正Uart相关驱动|
|USB-cloner-2.5.36-20230815.tar.gz|   |USB最新烧录工具|


   
|script

E:\sdk\ISVP-T23-1.1.2-20240204\ISVP-T23-1.1.2-20240204\software\zh\Ingenic-SDK-T23-1.1.2-20240204-zh<span style="background:#b1ffff">\resource\tools_t23\script</span>
### |init|   |文件系统init脚本|
|mk_ko_dir.sh|   |文件系统制作驱动卸载路劲|
|rootfs|   |rootfs下相关脚本|





## 3.其他


   
|固件|image_T23|   |T23各种芯片的固件|




   
|效果文件|sensor_settings_T23|   |sensor的基础效果文件|


   
|sample|   |   |参考sample文件夹|



## 3.库文件、头文件
 
   
|lib|glibc|libalog.a|alog静态库|
|libalog.so|alog动态库|
|libaudioProcess.so|音频动态库|
|libsysutils.a|sysutils 静态库|
|libsysutils.so|sysutils 动态库|
|libimp.so|imp动态库|
|libimp.a|imp静态库|
|uclibc|libalog.a|alog静态库|
|libalog.so|alog动态库|
|libaudioProcess.so|音频动态库|
|libsysutils.a|sysutils 静态库|
|libsysutils.so|sysutils 动态库|
|libimp.so|imp动态库|
|libimp.a|imp静态库|


|include
|imp|   |Imp相关头文件|
|sysutils|   |sysutils相关头文件|


# 五、


## 1.


## 2.



## 3.



# 六、


## 1.

## 2.

## 3.













