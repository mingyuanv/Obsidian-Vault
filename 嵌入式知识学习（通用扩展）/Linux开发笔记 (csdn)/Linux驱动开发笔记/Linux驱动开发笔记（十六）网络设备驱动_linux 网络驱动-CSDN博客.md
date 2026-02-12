---
title: "Linux驱动开发笔记（十六）网络设备驱动_linux 网络驱动-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/140179143?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读1.1k次，点赞33次，收藏40次。Linux的驱动主要分为三大类：字符驱动、块设备驱动和网络设备驱动，今天我们进行最后一类——网络驱动的学习。_linux 网络驱动"
tags:
  - "clippings"
---
---

## 前言

Linux 的驱动主要分为三大类： [字符驱动](https://so.csdn.net/so/search?q=%E5%AD%97%E7%AC%A6%E9%A9%B1%E5%8A%A8&spm=1001.2101.3001.7020) 、块设备驱动和网络设备驱动，今天我们进行最后一类——网络驱动的学习。

---

## 一、网络设备的引入

  网络设备和另外两类设备不同，不强调“ **文件** ”的概念而更偏重于“ **通信** ”，网络设备及其驱动属于整个 TCP /IP协议层的一部分，实现遵循TCP/IP协议栈的要求(网卡驱动属于网络接口层）。

### 1.1 网络子系统（Net）

  网络子系统在Linux内核中主要负责管理各种网络设备，并实现各种网络协议栈，最终实现通过网络连接其它系统的功能。在Linux内核中，网络子系统几乎是自成体系，它包括5个子模块，它们的功能如下：  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/cd19b30082b00f3095062e3bff2f0b3a.png#pic_center)

- Network Device Drivers：网络设备驱动，和VFS子系统中的设备驱动一样
- Device Independent Interface：该模块定义了描述硬件设备的统一方式（统一设备模型），同时可以用一致的形势向上提供接口
- NetsworkProtocols：各种网络协议，例如：IP、TCP、UDP等
- Protocol Independent Interface：屏蔽不同硬件设备和对应网络协议，以相同格式提供统一接口（socket）
- System Call Interface：系统调用接口，向用户提供访问网络设备的统一接口标准

### 1.2 网络设备框架

  可以说Linux的网络子系统是一个复杂而强大的 组件 ，它包括了网络协议接口、网络设备接口、设备驱动层、网络层等多个层次。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c59e9084c937afe52029cb8b35d02b23.png#pic_center)  
  当上层的ARP或IP协议需要发送数据包时，就会调用dev\_queue\_xmit() 函数 ；同样地，上层协议需要接收数据包时，就会调用netif\_rx()函数。

```c
//网络数据发送
dev_queue_xmit(struct sk_buff *skb);  

//网络数据接收
int netif_rx(struct sk_buff *skb);    
12345
```

  网络设备接口层向协议接口层提供统一的用于描述具体网络设备属性和操作的 结构体 net\_device，该结构体是设备驱动功能层中各函数的容器。实际上，网络设备接口层从宏观上规划了具体操作硬件的设备驱动功能层的结构。  
  网络驱动接口层各函数是网络设备接口层net\_device数据结构的具体成员，是驱使网络设备硬件完成相应动作的程序，他通过hard\_start\_xmit()函数启动发送操作，并通过网络设备上的中断触发接收操作。  
  网络设备与媒介层是完成数据包发送和接收的物理实体，包括网络适配器和具体的传输媒介，网络适配器被驱动功能层中的函数物理上驱动。对于Linux系统而言，网络设备和媒介都可以是虚拟的。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/02ad99ec87ee4c139c32b89ef82eac3e.png#pic_center)

## 二、网络设备驱动

### 2.1 核心数据结构

  这里我们可以看到整个框架的核心在于 **net\_device** 结构体，它主要用于内核网络子系统管理和操作网络设备，并不直接用于内核空间和用户空间的交互。

```c
struct net_device {
    char name[IFNAMSIZ];                    // 网络设备名称
    struct net_device_stats stats;             // 网络设备统计信息
    int (*open)(struct net_device *dev);    // 打开网络设备的函数
    int (*stop)(struct net_device *dev);    // 关闭网络设备的函数
    netdev_tx_t (*hard_start_xmit) (struct sk_buff *skb, struct net_device *dev); // 发送数据包的函数
    struct net_device_ops *netdev_ops;          // 网络设备操作集合
    // 其他成员...
};
123456789
```

  其中 **netdev\_ops** 是最为重要的成员，它是网络设备的操作集，net\_device\_ops 结构体里面都是一些以“ndo\_”开头的函数，这些函数就需要网络驱动人员去实现，不需要全部都实现，根据实际驱动情况实现其中一小部分即可。

```c
struct net_device_ops {
    int (*ndo_init)(struct net_device *dev);
    void (*ndo_uninit)(struct net_device *dev);
    int (*ndo_open)(struct net_device *dev);
    int (*ndo_stop)(struct net_device *dev);
    netdev_tx_t (*ndo_start_xmit)(struct sk_buff *skb, struct net_device *dev);
    u16 (*ndo_select_queue)(struct net_device *dev, struct sk_buff *skb, struct net_device *sb_dev);
    void (*ndo_change_rx_flags)(struct net_device *dev, int flags);
    void (*ndo_set_rx_mode)(struct net_device *dev);
    int (*ndo_set_mac_address)(struct net_device *dev, void *addr);
    int (*ndo_validate_addr)(struct net_device *dev);
    int (*ndo_do_ioctl)(struct net_device *dev, struct ifreq *ifr, int cmd);
    int (*ndo_set_config)(struct net_device *dev, struct ifmap *map);
    int (*ndo_change_mtu)(struct net_device *dev, int new_mtu);
    int (*ndo_neigh_setup)(struct net_device *dev, struct neigh_parms *);
    void (*ndo_tx_timeout)(struct net_device *dev);
    void (*ndo_get_stats64)(struct net_device *dev, struct rtnl_link_stats64 *storage);
    struct net_device_stats* (*ndo_get_stats)(struct net_device *dev);
    int (*ndo_vlan_rx_add_vid)(struct net_device *dev, __be16 proto, u16 vid);
    int (*ndo_vlan_rx_kill_vid)(struct net_device *dev, __be16 proto, u16 vid);
    int (*ndo_set_features)(struct net_device *dev, netdev_features_t features);
    netdev_features_t (*ndo_fix_features)(struct net_device *dev, netdev_features_t features);
    // 其他成员...
}
123456789101112131415161718192021222324
```
- ndo\_open：当网络设备打开时调用。
- ndo\_stop：当网络设备关闭时调用。
- ndo\_start\_xmit：当网络设备发送数据包时调用。
- ndo\_select\_queue：选择发送队列。
- ndo\_set\_rx\_mode：设置网络设备的接收模式。
- ndo\_set\_mac\_address：设置网络设备的MAC地址。
- ndo\_validate\_addr：验证 MAC 地址是否合法。
- ndo\_do\_ioctl ：用户程序调用 ioctl 的时候此函数就会执行，比如 PHY 芯片  
	相关的命令操作，一般会直接调用 phy\_mii\_ioctl 函数。
- ndo\_change\_mtu：更改 MTU 大小。
- ndo\_tx\_timeout：当发送超时的时候产生会执行，一般都是网络出问题了导  
	致发送超时。一般可能会重启 MAC 和 PHY，重新开始数据发送等。
- ndo\_poll\_controller：使用查询方式来处理网卡数据的收发。
- ndo\_set\_features：修改 net\_device 的 features 属性，设置相应的硬件属性。

**sk\_buff** 结构体（ socket buffer）是 [Linux 内核](https://so.csdn.net/so/search?q=Linux%20%E5%86%85%E6%A0%B8&spm=1001.2101.3001.7020) 中用于网络数据包的基本数据结构。它封装了网络层之间传递的数据，并包含了与数据包处理相关的元数据。

```c
struct sk_buff {
    /* These two members must be first. */
    struct sk_buff          *next;
    struct sk_buff          *prev;

    struct sock             *sk;
    struct net_device       *dev;

    char                    cb[48] __aligned(8);

    unsigned long           _skb_refdst;
    struct sec_path         *sp;

    unsigned int            len,
                            data_len;
    __u16                   mac_len,
                            hdr_len;

    union {
        __wsum              csum;
        struct {
            __u16           csum_start;
            __u16           csum_offset;
        };
    };

    __u32                   priority;
    ktime_t                 tstamp;

    struct net_device       *input_dev;

    union {
        struct tcphdr       *th;
        struct udphdr       *uh;
        struct icmphdr      *icmph;
        struct igmphdr      *igmph;
        struct iphdr        *ipiph;
        struct ipv6hdr      *ipv6h;
        struct arphdr       *arph;
        unsigned char       *raw;
    } h;

    union {
        struct iphdr        *iph;
        struct ipv6hdr      *ipv6h;
        struct arphdr       *arph;
        unsigned char       *raw;
    } nh;

    union {
        struct ethhdr       *eth;
        unsigned char       *raw;
    } mac;

    /* Transport layer header */
    union {
        struct tcphdr       *th;
        struct udphdr       *uh;
        struct icmphdr      *icmph;
        struct igmphdr      *igmph;
        struct iphdr        *ipiph;
        struct ipv6hdr      *ipv6h;
        struct arphdr       *arph;
        unsigned char       *raw;
    } transport_header;

    /* Network layer header */
    union {
        struct iphdr        *iph;
        struct ipv6hdr      *ipv6h;
        struct arphdr       *arph;
        unsigned char       *raw;
    } network_header;

    /* MAC layer header */
    union {
        struct ethhdr       *eth;
        unsigned char       *raw;
    } mac_header;

    unsigned int            truesize;
    atomic_t                users;

    /* Data pointer */
    unsigned char           *head,
                            *data,
                            *tail,
                            *end;
};
1234567891011121314151617181920212223242526272829303132333435363738394041424344454647484950515253545556575859606162636465666768697071727374757677787980818283848586878889
```

主要成员解释：

- next, prev：用于将多个 sk\_buff 结构体链接成一个链表。
- sk：指向与此数据包相关联的套接字。
- dev：指向接收或发送此数据包的网络设备。
- cb：控制缓冲区，用于存储协议相关的临时数据。
- \_skb\_refdst：引用目标，涉及 IP 路由。
- sp：指向安全路径，涉及 IPSec。
- len：数据包总长度。
- data\_len：分片数据的长度。
- mac\_len：MAC 层头部长度。
- hdr\_len：头部长度。
- csum：校验和。
- priority：数据包的优先级。
- tstamp：时间戳。
- input\_dev：输入设备。
- h, nh, mac：分别指向传输层头部、网络层头部和链路层头部。
- transport\_header、network\_header、mac\_header：分别指向传输层、网络层和 MAC 层的头部。
- truesize：缓冲区的实际大小。
- users：引用计数，用于跟踪该缓冲区被多少个实体引用。
- head, data, tail, end：指向缓冲区的指针，分别表示缓冲区的开始、有效数据的开始、有效数据的结束和缓冲区的结束。  
	![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/e037ec86528d48b7b472681fcff6ef6f.png#pic_center)

### 2.2 驱动的编写

#### 2.2.1 net\_device申请及释放

  每一个网络设备都由struct net\_device来描述，该结构可使用如下内核函数进行动态分配

```c
//申请网络设备资源
struct net_device *alloc_netdev(int sizeof_priv, const char *mask, void(*setup)(struct net_device *))

//初始化net_device并填充一些以太网中的设备结构体的项
ether_setup(net_device);
12345
```

  sizeof\_priv是私有数据区大小；mask是设备名,setup是初始化函数，在注册该设备时，该函数被调用。也就是net\_deivce的init成员。

```c
申请网络设备资源（以太网设备）
struct net_device *alloc_etherdev(intsizeof_priv)
12
```

  这个函数和上面的函数不同之处在于内核知道会将该设备做一个以太网设备看待并做一些相关的初始化。

```c
//释放网络设备资源
void free_netdev(struct net_device *dev);
12
```

#### 2.2.2 网络驱动设备的注册与注销

  net\_device 结构体的分配和网络设备驱动注册需在网络设备驱动程序的模块加载函数中进行，而net\_device 结构体的释放和网络设备驱动的注销则需在模块卸载函数中完成。

```c
//注册网络设备
int register_netdev(struct net_device *dev);
//注销网络设备
void unregister_netdev(struct net_device *dev);
1234
```

#### 2.2.3 数据的传输

  在网络设备中，我们通常利用对sk\_buff进行操作来实现消息的传递。网络是分层的，对于应用层而言不用关系具体的底层是如何工作的，只需要按照协议将要发送或接收的数据打包好即可。打包好以后都通过 dev\_queue\_xmit 函数将数据发送出去，接收数据的话使用 netif\_rx 函数即可，我们依次来看一下这两个函数。  
**alloc\_skb**

```c
//用于分配并初始化 sk_buff 结构体，以便在内核中处理网络数据包。
struct sk_buff *alloc_skb(unsigned int size, gfp_t priority);
12
```
- 参数：
	- size：要分配的缓冲区的大小，以字节为单位。
	- priority：用于内存分配的优先级标志，通常是 GFP\_KERNEL 或其他 GFP 标志。
- 返回值：
	- 成功：指向新分配的 sk\_buff 结构体的指针。
	- 失败：NULL。

**kfree\_skb** 和 **dev\_kfree\_skb**

```c
//用于释放先前分配的 sk_buff 结构体，并释放其关联的内存
void kfree_skb(struct sk_buff *skb);

/*dev_kfree_skb 类似于 kfree_skb，但它会记录释放缓冲区的设备信息*/
void dev_kfree_skb(struct sk_buff *skb);
12345
```

**skb\_put** 、 **skb\_pull** 和 **skb\_reserve**

```c
//用于在 sk_buff 的数据区末尾增加数据，并更新 tail 和 len 字段。
unsigned char *skb_put(struct sk_buff *skb, unsigned int len);

//用于从 sk_buff 的数据区前部移除数据，并更新 data 和 len 字段。
unsigned char *skb_pull(struct sk_buff *skb, unsigned int len);

//用于在数据区前部预留一定长度的空闲空间，通常用于为头部预留空间。
void skb_reserve(struct sk_buff *skb, int len);
12345678
```

### 2.3 NAPI处理方式

  在之前单片机的网络数据接收有轮询和中断两种，除此之外Linux提出了另外一种网络数据接收的处理方法：NAPI(New API)，NAPI 是一种高效的网络处理技术。NAPI 的核心思想就是不全部采用中断来读取网络数据，而是 **采用中断来唤醒** 数据接收服务程序，在接收服务程序中采用 POLL 的方法来 **轮询处理数据** 。这种方法的好处就是可以提高短数据包的接收效率，减少中断处理的时间。

#### 2.3.1 napi\_struct

  napi\_struct 结构体用于表示一个 NAPI 上下文，它包含了用于处理网络包的相关信息和状态。

```c
struct napi_struct {
    struct list_head poll_list;       // 链接到活动的 napi_struct 列表
    unsigned long state;              // 状态位
    int weight;                       // 权重，用于限制每次处理的包数
    unsigned int gro_count;           // GRO（Generic Receive Offload）计数
    struct net_device *dev;           // 指向关联的网络设备
    struct sk_buff *skb;              // 当前正在处理的包
    int (*poll)(struct napi_struct *, int); // 轮询函数指针
    // 其他字段...
};
12345678910
```

#### 2.3.2 NAPI 处理流程

  NAPI 的处理流程主要包括以下几个步骤：

- 注册 NAPI：在网络设备驱动程序初始化时，注册 napi\_struct 并将其与网络设备关联。
```c
void netif_napi_add(struct net_device *dev, struct napi_struct *napi,
            int (*poll)(struct napi_struct *, int), int weight);
/*
    - dev：每个 NAPI 必须关联一个网络设备，此参数指定 NAPI 要关联的网络设备。
    - napi：要初始化的 NAPI 实例。
    - poll：NAPI 所使用的轮询函数，非常重要，一般在此轮询函数中完成网络数据接收的工作。
    - weight：NAPI 默认权重(weight)，一般为 NAPI_POLL_WEIGHT。
 */
12345678
```
- 使能NAPI
```c
static inline void napi_enable(struct napi_struct *n)
1
```
- 查询调度：这里使用了一个内联函数，它的主要作用是安排 napi\_struct 的轮询，通过检查和设置 NAPI 的调度状态，并将其添加到软中断（softirq）处理队列中。
```c
static inline void napi_schedule(struct napi_struct *n)
{
    if (!test_and_set_bit(NAPI_STATE_SCHED, &n->state))
        ____napi_schedule(this_cpu_ptr(&softnet_data), n);
}
12345
```
- 检验是否完成：NAPI 处理完成以后需要调用 napi\_complete 函数来标记 NAPI 处理完成
```c
static inline void napi_complete(struct napi_struct *n);
1
```
- 删除NAPI
```c
void netif_napi_del(struct napi_struct *napi);
1
```

**免责声明：本内容部分参考正点原子及其他相关公开资料，若有侵权或者勘误请联系作者。**

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/140179143

作者主页：https://blog.csdn.net/sincerelover

实付 元

[使用余额支付](https://blog.csdn.net/sincerelover/article/details/)

点击重新获取

扫码支付

钱包余额 0

抵扣说明：

1.余额是钱包充值的虚拟货币，按照1:1的比例进行支付金额的抵扣。  
2.余额无法直接购买下载，可以购买VIP、付费专栏及课程。

[余额充值](https://i.csdn.net/#/wallet/balance/recharge)

举报

![程序员都在用的中文IT技术交流社区](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_app.png)

程序员都在用的中文IT技术交流社区

程序员都在用的中文IT技术交流社区

![专业的中文 IT 技术社区，与千万技术人共成长](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_wechat.png)

专业的中文 IT 技术社区，与千万技术人共成长

专业的中文 IT 技术社区，与千万技术人共成长

![关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_video.png)

关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！

关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！

客服 返回顶部