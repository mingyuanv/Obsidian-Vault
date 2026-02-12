---
title: "RK3568驱动指南｜第九篇 设备模型-第109章 probe函数执行流程分析实验"
source: "https://blog.csdn.net/BeiJingXunWei/article/details/135389470"
author:
  - "[[BeiJingXunWei]]"
published: 2024-01-04
created: 2025-09-14
description: "文章浏览阅读1.1k次，点赞21次，收藏23次。drv->bus->match(dev, drv)表示调用总线对象的 match函数，并将设备对象和驱动程序对象作为参数传递给该函数。总的来说， bus_for_each_dev() 函数主要是提供了一个遍历指定总线上的设备对象列表，并对每个设备对象进行特定操作的快捷方式，可以用于驱动程序中需要管理和操作大量设备实例的场景。这个函数的作用是遍历指定总线上的所有设备，并对每个设备执行指定的函数 fn。2. 如果 match`函数存在，则调用总线对象的 match函数，传入设备对象和驱动程序对象作为参数。_驱动函数执行流程"
tags:
  - "clippings"
---
