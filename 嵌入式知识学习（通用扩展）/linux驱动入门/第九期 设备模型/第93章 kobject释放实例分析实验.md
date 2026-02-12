---
title: "RK3568驱动指南｜第九篇 设备模型-第93章 kobject释放实例分析实验"
source: "https://blog.csdn.net/BeiJingXunWei/article/details/135346414"
author:
  - "[[BeiJingXunWei]]"
published: 2024-01-03
created: 2025-09-14
description: "文章浏览阅读1k次，点赞28次，收藏17次。kobject_create_and_add()函数首先调用 kobject_create()函数，该函数使用 kzalloc()为 kobject分配内存空间。接下来，kobject_create_and_add()函数调用 kobject_add()函数将 kobject添加到系统中，使其可见。kobject_add()函数内部调用了kobject_add_internal()函数，该函数负责将 kobject添加到父对象的子对象列表中，并创建相应的 sysfs 文件系统条目。_rk3568 kobject"
tags:
  - "clippings"
---
