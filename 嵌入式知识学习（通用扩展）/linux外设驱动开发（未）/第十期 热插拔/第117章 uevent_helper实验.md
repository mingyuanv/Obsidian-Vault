---
title: "{{title}}"
aliases: 
tags: 
description: 
source:
---

# 备注(声明)：内核发送事件到用户空间的第二种方法-调用可执行程序。


# 参考文章：

```cardlink
url: https://blog.csdn.net/BeiJingXunWei/article/details/135527770?spm=1001.2101.3001.10796
title: "RK3568驱动指南｜第十篇 热插拔-第117章uevent_helper实验_support for uevent helper-CSDN博客"
description: "文章浏览阅读1.2k次，点赞20次，收藏24次。瑞芯微RK3568芯片是一款定位中高端的通用型SOC，采用22nm制程工艺，搭载一颗四核Cortex-A55处理器和Mali G52 2EE 图形处理器。RK3568 支持4K 解码和 1080P 编码，支持SATA/PCIE/USB3.0 外围接口。RK3568内置独立NPU，可用于轻量级人工智能应用。RK3568 支持安卓 11 和 linux 系统，主要面向物联网网关、NVR 存储、工控平板、工业检测、工控盒、卡拉 OK、云终端、车载中控等行业。​【公众号】迅为电子【粉丝群】82441201_support for uevent helper"
host: blog.csdn.net
```


# 一、uevent_helper实验

## 设置uevent_helper
### 1 、在114.2小节的第十部分中进行了定义
```c
#ifdef CONFIG_UEVENT_HELPER
	/* call uevent_helper, usually only enabled during early boot */
	if (uevent_helper[0] && !kobj_usermode_filter(kobj)) {
		struct subprocess_info *info;
 
		retval = add_uevent_var(env, "HOME=/");
		if (retval)
			goto exit;
		retval = add_uevent_var(env,
					"PATH=/sbin:/bin:/usr/sbin:/usr/bin");
		if (retval)
			goto exit;
		retval = init_uevent_argv(env, subsystem);
		if (retval)
			goto exit;
 
		retval = -ENOMEM;
		info = call_usermodehelper_setup(env->argv[0], env->argv,
						 env->envp, GFP_KERNEL,
						 NULL, cleanup_uevent_env, env);
		if (info) {
			retval = call_usermodehelper_exec(info, UMH_NO_WAIT);
			env = NULL;	/* freed by cleanup_uevent_env */
		}
	}
#endif
```


### 2 、uevent_helper 数组解析：
> 第3行为一个if表达式，它**检查 uevent_helper 数组的第一个元素是否为真**。并调用 kobj_usermode_filter 函数进行用户模式过滤， 

- 1 uevent_helper定义如下所示：
```c
char uevent_helper[UEVENT_HELPER_PATH_LEN] = CONFIG_UEVENT_HELPER_PATH;
```

> 其中CONFIG_UEVENT_HELPER_PATH 是一个
- 2 宏定义在内核源码的“include/generated/autoconf.h”文件中，如下所示：

`#define CONFIG_UEVENT_HELPER_PATH  ""      //该宏为空    `


### 3 、使能uevent_helper功能
- 1 在图形配置界面使能CONFIG_UEVENT_HELPER和CONFIG_UEVENT_HELPER_PATH两个宏

> ![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第117章 uevent_helper实验/file-20260313155818170.png]]
#### 配置方法1：（需要重新编译内核）
- 1 设置了uevent helper和相对应的路径。

> 配置1:
> ![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第117章 uevent_helper实验/file-20260313155907391.png]]
> 配置2:
> ![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第117章 uevent_helper实验/file-20260313155912958.png]]
> 配置3:
> ![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第117章 uevent_helper实验/file-20260313155925716.png]]
> 配置4:
> ![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第117章 uevent_helper实验/file-20260313155951338.png]]
> 

#### 配置方法2：（更快捷）(❤️)
> 无论是否配置了CONFIG_UEVENT_HELPER_PATH，在系统启动后，可以使用以下命令来设置uevent_helper：

```c
echo /sbin/mdev > /sys/kernel/uevent_helper
```

- 1 这将把uevent_helper设置为/sbin/mdex。


#### 配置方法3：（更快捷）(❤️)
> 无论是否配置了CONFIG_UEVENT_HELPER_PATH，在系统启动后，可以使用以下命令来设置uevent_helper：

```c
echo /sbin/mdev > /proc/sys/kernel/hotplug
```

- 1 这将把uevent_helper设置为/sbin/mdexw.。


#### 注意： 
> **配置方法2和配置方法3依赖于上面的配置2、3、4选项**，并且**可以通过配置方法2和配置方法3修改配置方法1中已经写好的值。**


- 2 都是为了对uevent_helper属性进行读写操作。




### 4 、uevent_helper属性文件
- 2 /sys/kernel/uevent_helper  是uevent_helper属性的接口。

- 1 kernel/ksysfs.c目录下可以找到对uevent_helper属性的定义和相关操作的实现

> `uevent_helper_show`函数用于将uevent_helper的值写入buf中，并返回写入的字符数。
> 
> `uevent_helper_store`函数用于**将buf中的值复制到uevent_helper中**，并根据需要进行处理，然后返回写入的字符数。
```c
#ifdef CONFIG_UEVENT_HELPER
/* uevent helper program, used during early boot */
static ssize_t uevent_helper_show(struct kobject *kobj, struct kobj_attribute *attr, char *buf)
{
    return sprintf(buf, "%s\n", uevent_helper);
}
 
static ssize_t uevent_helper_store(struct kobject *kobj, struct kobj_attribute *attr,
                                   const char *buf, size_t count)
{
    if (count + 1 > UEVENT_HELPER_PATH_LEN)
        return -ENOENT;
 
    memcpy(uevent_helper, buf, count);
    uevent_helper[count] = '\0';
 
    if (count && uevent_helper[count - 1] == '\n')
        uevent_helper[count - 1] = '\0';
 
    return count;
}
 
KERNEL_ATTR_RW(uevent_helper);
#endif
```




### 5、虚拟文件：/proc/sys/kernel/hotplug
> 用于**配置内核中的热插拔事件处理程序**。通过对该文件进行写操作，可以设置uevent_helper属性的值。

- 1 kernel/sysctl.c文件中   对hotplug操作其实是对uevent_helper进行操作。
> 这段代码定义了一个名为hotplug的文件，用于处理uevent事件。它**与uevent_helper属性相关联**。
> 
> .procname表示文件名，即/proc/hotplug。
> 
> .data是一个指向uevent_helper结构体的指针，用于保存与该文件相关的数据。该指针指向uevent_helper结构体，用于处理uevent事件。
> 
> .maxlen表示文件的最大长度，即文件内容的最大长度。该值为UEVENT_HELPER_PATH_LEN，表示文件内容的最大长度为UEVENT_HELPER_PATH_LEN。
> 
> .mode表示文件的访问权限。该值为0644，表示该文件的权限为 -rw-r--r--，即所有用户都可以读取该文件，但只有root用户可以写入该文件。

```c
#ifdef CONFIG_UEVENT_HELPER
{
	.procname = "hotplug",
	.data = &uevent_helper,
	.maxlen = UEVENT_HELPER_PATH_LEN,
	.mode = 0644,
	.proc_handler = proc_dostring,
}
```

### 6、




## 处理uevent事件
### 1 、网盘路径
> 本应用程序对应的网盘路径为：iTOP-RK3568开发板【底板V1.7版本】\03_【iTOP-RK3568开发板】指南教程\02_Linux驱动配套资料\04_Linux驱动例程\81_mdev。 

### 2 、获取SUBSYSTEM环境变量并打印即可


### 3 、编写完成的应用程序内容如下：(❤️)

```c
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
 
int main(int argc, char *argv[])
{
    // 打开特定设备（此处为"/dev/ttyFIQ0"）用于写操作
    int fd = open("/dev/ttyFIQ0", O_WRONLY);
    
    // 将标准输出重定向到打开的文件描述符fd
    dup2(fd, STDOUT_FILENO);
    
    // 打印环境变量"SUBSYSTEM"的值到标准输出（现在已重定向至"/dev/ttyFIQ0"）
    printf("SUBSYSTEM is %s\n", getenv("SUBSYSTEM"));
    
    return 0;
}
```


### 4 、

## 运行测试
### 5、使用的驱动文件为115章编译生成的uevent_ops.ko


### 6、配置方法2：(❤️)
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第117章 uevent_helper实验/file-20260313162926008.png]]

### 7、配置方法3：
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十期 热插拔/assets/第117章 uevent_helper实验/file-20260313163055590.png]]

### 8、都可以打印出内核加载时传递的SUBSYSTEM环境变量



## 
### 1 、


### 2 、


### 3 、



### 4 、



### 5、


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


