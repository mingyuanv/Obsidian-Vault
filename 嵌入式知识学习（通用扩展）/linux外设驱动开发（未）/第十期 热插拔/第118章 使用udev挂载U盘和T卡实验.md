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
url: https://blog.csdn.net/BeiJingXunWei/article/details/135530883?spm=1001.2101.3001.10796
title: "RK3568驱动指南｜第十篇 热插拔-第118章 使用udev挂载U盘和T卡实验_rk3568 挂载u盘-CSDN博客"
description: "文章浏览阅读3k次，点赞26次，收藏21次。\"/etc/udev/rules.d/usb/usb-add.sh\"：是要执行的命令的路径，即在设备添加时执行 /etc/udev/rules.d/usb/usb-add.sh 脚本文件。\"/etc/udev/rules.d/tf/tf-add.sh\"：是要执行的命令的路径，即在设备添加时执行 /etc/udev/rules.d/tf/tf-add.sh 脚本文件。检查到/sbin/udevd进程就表示当前系统使用的是udev，至此配置buildroot文件系统支持udev就完成了。_rk3568 挂载u盘"
host: blog.csdn.net
```




# 一、使用udev挂载U盘和T卡实验

## 配置buildroot文件系统支持udev
### 1 、添加udev应用程序
> 上一章中我们编写了一个名为mdev的应用程序，用来处理uevent事件，而**实际上udev和mdev的可执行程序都是很复杂的**，也并不需要我们自己来写，只需要在构建buildroot文件系统 时**勾选对应的选项即可**。



### 2 、图形化配置界面(❤️)
> ![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第118章 使用udev挂载U盘和T卡实验/file-20260313164103003.png]]
> 
> ![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第118章 使用udev挂载U盘和T卡实验/file-20260313164222613.png]]
> 




### 3 、网盘路径：
> 相应的镜像已经放在了“iTOP-RK3568开发板【底板V1.7版本】\03_【iTOP-RK3568开发板】指南教程\02_Linux驱动配套资料\04_Linux驱动程序\82_udev_u盘_TF卡”目录下如下图所示：


### 4 、查看udev是否已经启用：检查/sbin/udevd进程(❤️)
```c
ps -aux | grep -nR udev
```
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第118章 使用udev挂载U盘和T卡实验/file-20260313164338077.png]]


### 5、





## 使用udev挂载U盘
### 1 、网盘路径：
本小节编写完成的文件对应的网盘路径为：iTOP-RK3568开发板【底板V1.7版本】\03_【iTOP-RK3568开发板】指南教程\02_Linux驱动配套资料\04_Linux驱动例程04_Linux驱动程序\82_udev_u盘_TF卡\U盘。

### 2 、创建相应的规则文件

> 还需在开发板的`/etc/udev/rules.d目录下`创建相应的规则文件（/etc/udev/rules.d目录不存在可以手动创建，一般都已经存在了），这里我们创建一个名为**001.rules**的文件
> ![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第118章 使用udev挂载U盘和T卡实验/file-20260313164916192.png]]

- 1 添加以下内容：   /etc/udev/rules.d/001.rules
```c
KERNEL=="sd[a-z][0-9]", SUBSYSTEM=="block", ACTION=="add", RUN+="/etc/udev/rules.d/usb/usb-add.sh %k"
SUBSYSTEM=="block", ACTION=="remove", RUN+="/etc/udev/rules.d/usb/usb-remove.sh"
```

#### 规则内容解析：(❤️)
> （1）`KERNEL=="sd [a-z][0-9]"`
> 
> KERNEL：表示**匹配设备的内核名**。
> 
> "sd[a-z][0-9]"：是一个正则表达式 模式，sd：表示设备名以 "sd" 开头，[a-z]：表示设备名的第三个字符是小写字母，[0-9]：表示设备名的第四个字符是数字。
> 
> 这个模式用于**匹配 USB 存储设备的块设备节点，如 /dev/sda1**、/dev/sdb2 等。
> 

> （2）`SUBSYSTEM=="block"`
> 
> SUBSYSTEM：表示匹配设备的子系统名称。
> 
> "block"：表示设备的子系统是**块设备子系统**，即**与磁盘、分区等相关**的设备。
> 
> 这部分规则是为了确保只匹配块设备子系统下的设备。
> 

> （3）`ACTION=="add"和 ACTION=="remove"`
> 
> ACTION：表示**匹配设备的动作**。
> 
> "add"：表示设备被添加。
> 
> "remove"：表示设备被yichu。
> 
> 这部分规则是为了处理设备被添加和被删除的事件。
> 

> （5）`RUN+="/etc/udev/rules.d/usb/usb-add.sh %k"`
> 
> RUN+="..."：表示**在匹配的设备上执行指定的命令**。
> 
> "/etc/udev/rules.d/usb/usb-add.sh"：是要执行的命令的路径，即在设备添加时执行 /etc/udev/rules.d/usb/usb-add.sh 脚本文件。
> 
> `%k`：是 Udev 提供的一个变量，表示**匹配的设备的内核名**。



### 3 、完善这两个脚本内容(❤️)
> 可以注意到当块设备被添加的时候会执行/etc/udev/rules.d/usb/usb-add.sh脚本，块设备被删除的时候会执行/etc/udev/rules.d/usb/usb-remove.sh脚本

- 1  /etc/udev/rules.d/usb/usb-add.sh 
```c
#!/bin/sh
/bin/mount -t vfat /dev/$1 /mnt
```


- 1 /etc/udev/rules.d/usb/usb-remove.sh 
```c
#!/bin/sh
sync
/bin/umount -l /mnt
```

- 2 赋予两个脚本的可执行权限
> ![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第118章 使用udev挂载U盘和T卡实验/file-20260313170641029.png]]
> 
> ![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第118章 使用udev挂载U盘和T卡实验/file-20260313170651042.png]]




### 4 、df命令查看当前的挂载情况
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第118章 使用udev挂载U盘和T卡实验/file-20260313170742406.png]]

### 5、插入U盘，相关打印如下
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第118章 使用udev挂载U盘和T卡实验/file-20260313170752750.png]]

### 6、df命令重新查看当前的挂载情况
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第118章 使用udev挂载U盘和T卡实验/file-20260313170822433.png]]

### 7、


### 8、



## 使用udev挂载TF卡

### 1 、网盘路径
本小节编写完成的文件对应的网盘路径为：iTOP-RK3568开发板【底板V1.7版本】\03_【iTOP-RK3568开发板】指南教程\02_Linux驱动配套资料\04_Linux驱动例程04_Linux驱动程序\82_udev_u盘_TF卡\TF卡。

### 2 、不做任何修改的情况下，TF卡直接挂载到了/mnt/sdcard目录

![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第118章 使用udev挂载U盘和T卡实验/file-20260313171322754.png]]

#### 原因：/lib/udev/rules.d下自动添加很多udev规则(❤️)
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第118章 使用udev挂载U盘和T卡实验/file-20260313171404541.png]]


### 3 、 /etc/udev/rules.d/目录的规则文件优先级更高(❤️)



### 4 、要实现TF卡自动挂载到/mnt



### 5、 /etc/udev/rules.d/002.rules(❤️)
```c
KERNEL=="mmcblk[0-9]p[0-9]", SUBSYSTEM=="block", ACTION=="add", RUN+="/etc/udev/rules.d/tf/tf-add.sh %k"
SUBSYSTEM=="block", ACTION=="remove", RUN+="/etc/udev/rules.d/tf/tf-remove.sh"
```

#### 规则解析：
> （1）`KERNEL=="mmcblk[0-9]p[0-9]"`
> 
> KERNEL：表示匹配设备的内核名。
> 
> "mmcblk[a-z][0-9]"：是一个正则表达式模式，mmcblk：表示设备名以 "mmcblk" 开头，[0-9]：表示设备名的第7个字符和第9个字符是数字。
> 
> 这个模式用于匹配TF卡存储设备的块设备节点，如 /dev/mmcblk1p1 等。
> 
> （2）`SUBSYSTEM=="block"`
> 
> SUBSYSTEM：表示匹配设备的子系统名称。
> 
> "block"：表示设备的子系统是块设备子系统，即与磁盘、分区等相关的设备。
> 
> 这部分规则是为了确保只匹配块设备子系统下的设备。
> 
> （3）`ACTION=="add"和 ACTION=="remove"`
> 
> ACTION：表示匹配设备的动作。
> 
> "add"：表示设备被添加。
> 
> "remove"：表示设备被yichu。
> 
> 这部分规则是为了处理设备被添加和被删除的事件。
> 
> （5）`RUN+="/etc/udev/rules.d/tf/tf-add.sh %k"`
> 
> RUN+="..."：表示在匹配的设备上执行指定的命令。
> 
> "/etc/udev/rules.d/tf/tf-add.sh"：是要执行的命令的路径，即在设备添加时执行 /etc/udev/rules.d/tf/tf-add.sh 脚本文件。
> 
> %k：是 Udev 提供的一个变量，表示匹配的设备的内核名。



### 6、要完善这两个脚本内容(❤️)
> 当TF卡块设备被添加的时候会执行/etc/udev/rules.d/usb/tf-add.sh脚本，TF卡块设备被删除的时候会执行/etc/udev/rules.d/tf/tf-remove.sh脚本
> ![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第118章 使用udev挂载U盘和T卡实验/file-20260313172358697.png]]

- 2 在 /etc/udev/rules.d/usb/tf-add.sh 文件中写入以下内容：
```c
#!/bin/sh
/bin/mount -t vfat /dev/$1 /mnt
```

- 2 在 /etc/udev/rules.d/usb/tf-remove.sh 文件中写入以下内容：
```c
#!/bin/sh
sync
/bin/umount -l /mnt
```

- 2 赋予两个脚本的可执行权限
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第118章 使用udev挂载U盘和T卡实验/file-20260313172508884.png]]

### 7、df命令查看当前的挂载情况
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第118章 使用udev挂载U盘和T卡实验/file-20260313172527248.png]]

### 8、插入SD卡，相关打印如下
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第118章 使用udev挂载U盘和T卡实验/file-20260313172540520.png]]

![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第118章 使用udev挂载U盘和T卡实验/file-20260313172615540.png]]


### 9、TF卡mmcblk1p1就成功挂载到了/mnt目录



### 10、






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


