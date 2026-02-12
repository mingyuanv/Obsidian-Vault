---
title: "RK3568驱动指南｜第九篇 设备模型-第102章 platform总线注册流程实例分析实验"
source: "https://blog.csdn.net/BeiJingXunWei/article/details/135384934"
author:
  - "[[BeiJingXunWei]]"
published: 2024-01-04
created: 2025-09-14
description: "文章浏览阅读904次，点赞17次，收藏19次。然后使用调用device_register(platform_bus_type) 注册平台总线设备，将platform_bus结构体注册到设备子系统中。然后使用bus_register(&platform_bus_type)函数注册平台总线类型，将 platform_bus_type 结构体注册到总线子系统中。如果匹配成功，则返回匹配（非零）。如果存在，则调用platform_match_id(pdrv->id_table, pdev)函数来检查设备是否与ID表中的任何条目匹配。_平台总线注册"
tags:
  - "clippings"
---
