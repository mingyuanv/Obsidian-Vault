---
title: "RK3568驱动指南｜第九篇 设备树模型-第85章设备模型基本框架-kobject和kset_rk nvr源码 linux-CSDN博客"
source: "https://blog.csdn.net/BeiJingXunWei/article/details/135226684"
author:
  - "[[成就一亿技术人!]]"
  - "[[hope_wisdom 发出的红包]]"
published:
created: 2025-09-14
description: "文章浏览阅读1.4k次，点赞19次，收藏22次。一个kobject可以有一个父kobject和多个子kobject，通过parent指针可以将它们连接起来形成一个层次化的结构，类似于目录结构中，一个目录可以有一个父目录和多个子目录，通过目录的路径可以表示目录之间的层次关系。对于一些常见的硬件设备，如USB、i2c和平台设备，内核已经提供了相应的设备模型和相关驱动，开发人员可以基于这些模型来编写驱动，从而更快地实现特定设备的功能，并且可以借助内核的电源管理和热插拔事件管理功能。通过kset和kobject之间的关系，可以实现对内核对象的层次化管理和操作。_rk nvr源码 linux"
tags:
  - "clippings"
---
