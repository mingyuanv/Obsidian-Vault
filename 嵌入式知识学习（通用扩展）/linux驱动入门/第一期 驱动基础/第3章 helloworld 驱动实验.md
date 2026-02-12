---
title: "RK3568驱动指南｜第一篇 驱动基础-第3章 helloworld 驱动实验_3568 rknpu 0.8.2驱动-CSDN博客"
source: "https://blog.csdn.net/BeiJingXunWei/article/details/132731512"
author:
  - "[[成就一亿技术人!]]"
  - "[[hope_wisdom 发出的红包]]"
published:
created: 2025-09-08
description: "文章浏览阅读1.3k次。在学习C语言或者其他语言的时候，我们通常是打印一句“helloworld”来开启编程世界的大门。学习驱动程序编程亦可以如此，使用helloworld作为我们的第一个驱动程序。接下来开始编写第一个驱动程序—helloworld。_3568 rknpu 0.8.2驱动"
tags:
  - "clippings"
---
AI 搜索

## 3.1 驱动编写
### 最简单的驱动——helloworld驱动。
```c
#include <linux/module.h>
#include <linux/kernel.h>

static int __init helloworld_init(void)    //驱动入口函数
{
    printk(KERN_EMERG "helloworld_init\r\n");//注意：内核打印用printk而不是printf
    return 0;
}

static void __exit helloworld_exit(void)    //驱动出口函数
{
    printk(KERN_EMERG "helloworld_exit\r\n");
}

module_init(helloworld_init);    //注册入口函数
module_exit(helloworld_exit);    //注册出口函数
MODULE_LICENSE("GPL v2");    //同意GPL开源协议
MODULE_AUTHOR("topeet");    //作者信息
```



## 3.2 驱动的基本框架

> Linux 驱动的基本框架主要由模块加载函数，模块卸载函数，模块许可证声明，模块参数，模块导出符号，模块作者信息等几部分组成，其中模块参数，模块导出符号，模块作者信息是可选的部分，也就是可要可不要。剩余部分是必须有的。我们来看一下这几个部分的作用：

#### 1 模块加载函数
当使用加载驱动模块时，内核会执行模块加载函数，完成模块加载函数中的初始化工作。
```c
static int __init helloworld_init(void)    //驱动入口函数
{
    printk(KERN_EMERG "helloworld_init\r\n");
    return 0;
}
module_init(helloworld_init);    //注册入口函数

```
#### 2 模块卸载函数

当卸载某模块时，内核会执行模块卸载函数，完成模块卸载函数中的退出工作。
```c
static void __exit helloworld_exit(void)    //驱动出口函数
{
    printk(KERN_EMERG "helloworld_exit\r\n");
}
module_exit(helloworld_exit);    //注册出口函数
```
#### 3 模块许可证声明

> 许可证声明描述了内核模块的许可权限，如果不声明模块许可，模块在加载的时候，会收到“内核被污染（ kernel tainted）”的警告。可接受的内核模块声明许可**包括“GPL”“GPL v2”**。
```c
MODULE_LICENSE("GPL v2");    //同意GPL开源协议

```
#### 4 模块参数（可选择）

> 模块参数是**模块被加载的时候可以传递给它的值。**

#### 5 模块导出符号（可选择）

> 内核模块可以导出的符号，如果导出，其**他模块可以使用本模块中的变量或函数。**

#### 6 模块作者信息等说明（可选择）
```c
MODULE_AUTHOR("topeet");    //作者信息

```















![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第3章 helloworld 驱动实验/9ef150903c5aea7be8384317160f631f\_MD5.jpg](assets/第3章%20helloworld%20驱动实验/9ef150903c5aea7be8384317160f631f_MD5.jpg)

微信公众号

内容来源：csdn.net

作者昵称：北京迅为

原文链接：https://blog.csdn.net/BeiJingXunWei/article/details/132731512

作者主页：https://blog.csdn.net/BeiJingXunWei

博客[*RK3568* *驱动* *指南* *｜* *第一篇* *驱动* *基础* -第4 *章* 内核模块 *实验*](https://blog.csdn.net/mucheni/article/details/136184095)

[mucheni的博客](https://blog.csdn.net/mucheni)

02-20 962[在上个小节中编译了 *驱动* 模块 *hello* *world*.ko，在 *RK3568* *开发* 板上通过“insmod *hello* *world*.ko”命令可以加载 *驱动* ，在加载 *驱动* 模块的时候会执行 *驱动* 入口的函数，也就是 *hello* *world* 程序中的 *hello* *world* \_init函数，所以可以看到打印出来的字符串信息“ *hello* *world* \_init”。同样，在卸载 *驱动* 模块的时候，如果模块存在依赖关系，如果使用insmod命令，需要手动卸载依赖的内核模块，但是使用modprobe命令可以自动卸载 *驱动* 模块所依赖的其他模块。](https://blog.csdn.net/mucheni/article/details/136184095)

博客[*RK3568* *驱动* *指南* *｜* *第一篇* *驱动* *基础* -第5 *章* *驱动* 模块传参 *实验*](https://blog.csdn.net/mucheni/article/details/136225903)

[

最新发布

](https://blog.csdn.net/mucheni/article/details/136225903)

[mucheni的博客](https://blog.csdn.net/mucheni)

02-22 1076[Linux内核提供了 module\_param(name, type, perm)、module\_param\_array(name, type, nump, perm)宏和module\_param\_string(name, string, len, perm)宏，分别进行基本类型、数组和字符串参数的传递。经过前两 *章* *实验* 的实战操作，我们已经完成最简单的 *hello* *world* *驱动* *实验* 和模块 *驱动* *实验* ，加载模块可以使用“insmod”函数，使用“insmod”函数进行模块加载时也能进行参数的传递。](https://blog.csdn.net/mucheni/article/details/136225903)

评论

被折叠的 0 条评论 [为什么被折叠?](https://blogdev.blog.csdn.net/article/details/122245662)[到【灌水乐园】发言](https://bbs.csdn.net/forums/FreeZone)

添加红包

实付 元

[使用余额支付](https://blog.csdn.net/BeiJingXunWei/article/details/)

点击重新获取

扫码支付

钱包余额 0

抵扣说明：

1.余额是钱包充值的虚拟货币，按照1:1的比例进行支付金额的抵扣。  
2.余额无法直接购买下载，可以购买VIP、付费专栏及课程。

[余额充值](https://i.csdn.net/#/wallet/balance/recharge)

举报

![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第3章 helloworld 驱动实验/90bd0cbf3aff8fdff8bf9b011b581e20\_MD5.png](assets/第3章%20helloworld%20驱动实验/90bd0cbf3aff8fdff8bf9b011b581e20_MD5.png)

程序员都在用的中文IT技术交流社区

![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第3章 helloworld 驱动实验/08a47e60886378fe60a3d9c8f4ae8bc6\_MD5.png](assets/第3章%20helloworld%20驱动实验/08a47e60886378fe60a3d9c8f4ae8bc6_MD5.png)

专业的中文 IT 技术社区，与千万技术人共成长

![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第3章 helloworld 驱动实验/a51be6c085b867a5bd82d8dc1cea9b46\_MD5.png](assets/第3章%20helloworld%20驱动实验/a51be6c085b867a5bd82d8dc1cea9b46_MD5.png)

关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！

客服 返回顶部

微信公众号

![嵌入式知识学习（通用扩展）/linux驱动入门/第一期 驱动基础/assets/第3章 helloworld 驱动实验/efb7921311640694e61fee00900550d6\_MD5.jpg](assets/第3章%20helloworld%20驱动实验/efb7921311640694e61fee00900550d6_MD5.jpg) 公众号名称：迅为电子 微信扫码关注或搜索公众号名称

复制公众号名称