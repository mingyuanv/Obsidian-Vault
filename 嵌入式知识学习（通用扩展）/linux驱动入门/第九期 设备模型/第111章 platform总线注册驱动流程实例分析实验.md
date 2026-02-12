---
title: "RK3568驱动指南｜第九篇 设备模型-第111章 platform总线注册驱动流程实例分析实验"
source: "https://blog.csdn.net/BeiJingXunWei/article/details/135415376"
author:
  - "[[BeiJingXunWei]]"
published: 2024-01-06
created: 2025-09-14
description: "文章浏览阅读1.1k次，点赞22次，收藏24次。此行将指定的platform_drv_remove函数赋值给drv->driver.remove，表示驱动程序的移除函数。1 首先，将传递给驱动程序的设备指针 _dev 转换为 platform_driver 结构体指针 drv，将传递给驱动程序的设备指针 _dev 转换为 platform_device 结构体指针 dev。此行将指定的platform_drv_probe函数赋值给drv->driver.probe，表示驱动程序的探测函数。这个函数会根据设备的电源管理需求，将设备与相应的电源域进行关联。_platform总线设备驱动模型"
tags:
  - "clippings"
---
