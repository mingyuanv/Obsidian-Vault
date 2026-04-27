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
url: https://blog.csdn.net/BeiJingXunWei/article/details/135534359?ops_request_misc=%257B%2522request%255Fid%2522%253A%252237ec34eeed053b61a90d7daa25a5dcc1%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fblog.%2522%257D&request_id=37ec34eeed053b61a90d7daa25a5dcc1&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~blog~first_rank_ecpm_v1~rank_v31_ecpm-1-135534359-null-null.nonecase&utm_term=%E7%AC%AC119%E7%AB%A0&spm=1018.2226.3001.4450
title: "RK3568驱动指南｜第十篇 热插拔-第119章使用mdev挂载U盘和T卡实验_rk3568 u盘自动挂载-CSDN博客"
description: "文章浏览阅读1.9k次，点赞45次，收藏27次。瑞芯微RK3568芯片是一款定位中高端的通用型SOC，采用22nm制程工艺，搭载一颗四核Cortex-A55处理器和Mali G52 2EE 图形处理器。RK3568 支持4K 解码和 1080P 编码，支持SATA/PCIE/USB3.0 外围接口。RK3568内置独立NPU，可用于轻量级人工智能应用。RK3568 支持安卓 11 和 linux 系统，主要面向物联网网关、NVR 存储、工控平板、工业检测、工控盒、卡拉 OK、云终端、车载中控等行业。​【公众号】迅为电子。_rk3568 u盘自动挂载"
host: blog.csdn.net
```


# 一、使用mdev挂载U盘和T卡实验

##  配置buildroot文件系统支持mdev
### 1 、图形化配置界面(❤️)
> ![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第119章 使用mdev挂载U盘和T卡实验/file-20260313181013984.png]]
> 
> ![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第119章 使用mdev挂载U盘和T卡实验/file-20260313181021604.png]]

#### 还需要配置busybox的相关选项（默认配好）
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第119章 使用mdev挂载U盘和T卡实验/file-20260313181111937.png]]



### 2 、网盘路径：
编译完成的镜像已经放在了“iTOP-RK3568开发板【底板V1.7版本】\03_【iTOP-RK3568开发板】指南教程\02_Linux驱动配套资料\04_Linux驱动程序\83_mdev_u盘_TF卡”目录下如下图所示：



### 3 、查看mdev是否已经启用了（进程）
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第119章 使用mdev挂载U盘和T卡实验/file-20260313181146708.png]]


### 4 、





## 使用mdev挂载U盘
### 1 、网盘路径
本小节编写完成的文件对应的网盘路径为：iTOP-RK3568开发板【底板V1.7版本】\03_【iTOP-RK3568开发板】指南教程\02_Linux驱动配套资料\04_Linux驱动例程04_Linux驱动程序\83_mdev_u盘_TF卡\U盘。

### 2 、mdev使用/etc/mdev.conf 文件来配置 mdev 工具的规则和行为(❤️)


### 3 、mdev自动挂载U盘配置：(❤️)
- 1 /etc/mdev.conf 
```c
sd[a-z][0-9] 0:0 666 @/etc/mdev/usb_insert.sh
sd[a-z] 0:0 666 $/etc/mdev/usb_remove.sh
```


#### 两个规则的详细介绍：

> （1）sd [a-z][0-9] 是一个正则表达式模式，用于匹配以 "sd" 开头，后跟一个小写字母和一个数字的设备节点，例如 /dev/sda1、/dev/sdb2 等。
> 
> （2）0:0 666 表示设置设备节点的所有者和权限。0:0 表示所有者和所属组的用户 ID 和组 ID 均为 **0，即root用户**。666 表示权限为可读可写。
> 
> `@/etc/mdev/usb_insert.sh`表示当符合规则的设备插入时，mdev会执行 /etc/mdev/usb_insert.sh 脚本。**@ 符号表示执行的是一个shell命令**。
> `$/etc/mdev/usb_remove.sh` 表示当符合规则的设备移除时，mdev会执行 /etc/mdev/usb_remove.sh 脚本。**$ 符号表示执行的是一个内部命令。**
> 




### 4 、 /etc/mdev.conf 文件语法：
- 1 每一行都是一个规则

```c
<设备节点正则表达式> <设备的所有者:设备的所属组> <设备的权限> <设备插入或移除时需要执行的命令>
```



### 5、添加usb_insert.sh 和usb_remove.sh 脚本文件(❤️)
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第119章 使用mdev挂载U盘和T卡实验/file-20260313181816383.png]]


- 1 在/etc/mdev/usb_insert.sh 文件中写入以下内容：
```c
#!/bin/sh
 
if [ -d /sys/block/*/$MDEV ]; then
    mount /dev/$MDEV /mnt
    sync
fi
```


- 1 /etc/mdev/usb_remove.sh 文件中写入以下内容：
```c
#!/bin/sh
sync
/bin/umount -l /mnt
```


- 1 chmod命令赋予两个脚本的可执行权限
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第119章 使用mdev挂载U盘和T卡实验/file-20260313181924496.png]]



### 6、df命令查看当前的挂载情况
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第119章 使用mdev挂载U盘和T卡实验/file-20260313181939758.png]]



### 7、插入U盘，相关打印如下
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第119章 使用mdev挂载U盘和T卡实验/file-20260313181950158.png]]

![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第119章 使用mdev挂载U盘和T卡实验/file-20260313181954376.png]]

### 8、



## 使用mdev挂载TF卡
### 1 、网盘路径：
本小节编写完成的文件对应的网盘路径为：iTOP-RK3568开发板【底板V1.7版本】\03_【iTOP-RK3568开发板】指南教程\02_Linux驱动配套资料\04_Linux驱动例程04_Linux驱动程序\83_mdev_u盘_TF卡\TF卡。



### 2 、向/etc/mdev.conf 文件中添加以下两条类似的规则(❤️)
```c
mmcblk[0-9]p[0-9] 0:0 666 @/etc/mdev/tf_insert.sh
mmcblk[0-9] 0:0 666 $/etc/mdev/tf_remove.sh
```

#### 两个规则的详细介绍：
> （1）mmcblk[0-9]p[0-9] 是一个正则表达式 模式，用于匹配以 "mmcblk" 开头的TF卡块设备，例如 /dev/mmcblk1p1等。
> 
> （2）0:0 666 表示设置设备节点的所有者和权限。0:0 表示所有者和所属组的用户 ID 和组 ID 均为 0，即root用户。666 表示权限为可读可写。
> 
> `@/etc/mdev/tf_insert.sh`表示当符合规则的设备插入时，mdev会执行 /etc/mdev/tf_insert.sh 脚本。@ 符号表示执行的是一个shell命令。
> `$/etc/mdev/tf_remove.sh` 表示当符合规则的设备移除时，mdev会执行 /etc/mdev/tf_remove.sh 脚本。$ 符号表示执行的是一个内部命令。
> 

### 3 、添加tf_insert.sh 和tf_remove.sh 脚本文件(❤️)
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第119章 使用mdev挂载U盘和T卡实验/file-20260313182238741.png]]

- 2 在/etc/mdev/tf_insert.sh 文件中写入以下内容：
```c
#!/bin/sh
 
if [ -d /sys/block/*/$MDEV ]; then
    mount /dev/$MDEV /mnt
    sync
fi
```

- 2  /etc/mdev/tf_remove.sh 文件中写入以下内容：
```c
#!/bin/sh
sync
/bin/umount -l /mnt
```


- 2 chmod命令赋予两个脚本的可执行权限
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第119章 使用mdev挂载U盘和T卡实验/file-20260313182321255.png]]



### 4 、df命令查看当前的挂载情况
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第119章 使用mdev挂载U盘和T卡实验/file-20260313182331783.png]]


### 5、插入TF卡，相关打印如下
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第119章 使用mdev挂载U盘和T卡实验/file-20260313182346157.png]]

![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第119章 使用mdev挂载U盘和T卡实验/file-20260313182351297.png]]






### 6、


### 7、


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


