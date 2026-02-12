---
title: "{{title}}"
aliases: 
tags: 
description: 
source:
---

# 备注(声明)：




# 一、ConfigFS的核心数据结构

## 关键数据结构
### 1 、ConfigFS的核心数据结构
> `configfs_subsystem`：是一个**顶层的数据结构**，用于**表示整个ConfigFS子系统**。它包含了根配置项组的指针，以及ConfigFS的其他属性和状态信息。
> `config_group`：是一种特殊类型的配置项，表示一个**配置项组**。它可以包含一组相关的配置项，形成一个层次结构。config_group结构**包含了父配置项的指针，以及指向子配置项的链表**。
> `config_item`：这是ConfigFS中最基本的数据结构，用于表示一个**配置项**。每个配置项都是一个<span style="background:#d3f8b6">内核对象，可以是设备、驱动程序、子系统等</span>。<span style="background:#d3f8b6">结构包含了配置项的类型、名称、属性、状态等信息</span>，以及指向父配置项和子配置项的指针。


### 2 、树形结构关系
> 这些数据结构之间的关系可以形成一个树形结构，其中configfs_subsystem是根节点，config_group表示配置项组，config_item表示单个配置项。**子配置项通过链表连接在一起，形成父子关系**。如下表（图 75-1）所示：

[[嵌入式知识学习（通用扩展）/linux驱动入门/第七、八期 设备树/assets/第75章 ConfigFS的核心数据结构 - 设备树插件/a8b7b8a7b67e5fab28065774bbd834f9_MD5.jpeg|Open: file-20250903124559608.png]]
![嵌入式知识学习（通用扩展）/linux驱动入门/第七、八期 设备树/assets/第75章 ConfigFS的核心数据结构 - 设备树插件/a8b7b8a7b67e5fab28065774bbd834f9\_MD5.jpeg](assets/第75章%20ConfigFS的核心数据结构%20-%20设备树插件/a8b7b8a7b67e5fab28065774bbd834f9_MD5.jpeg)



### 3 、





## 子系统、容器和config_item
### 1 、configfs_subsystem结构体

```c
struct configfs_subsystem {
	struct config_group su_group;
	struct mutex su_mutex;
};
```

- 2 configfs_subsystem结构体中包含config_group结构体
### 2 、config_group结构体
```c
struct config_group {
	struct config_item cg_item;
	struct list_head cg_children;
	struct configfs_subsystem *cg_subsys;
	struct list_head default_group;
	struct list_head group_entry;
};
```


- 2 config_group结构体中包含config_item结构体
### 3 、config_item结构体
```c
struct config_item {
	char *ci_name;
	char ci_namebuf[CONFIGFS_ITEM_NAME_LEN];  //目录的名字
	struct kref ci_kref;
	struct list_head ci_entry;

	struct config_item *ci_parent;
	struct config_group *ci_group;
	const struct config_item_type *ci_type; //目录下属性文件和属性操作
	struct dentry *ci_dentry;
};

```


### 4 、分析设备树插件驱动代码（结构体）
[[嵌入式知识学习（通用扩展）/linux驱动入门/第七、八期 设备树/assets/第75章 ConfigFS的核心数据结构 - 设备树插件/f9bb17fb010fd25197b3f9a017aafa9e_MD5.jpeg|Open: file-20250906202845746.png]]
![嵌入式知识学习（通用扩展）/linux驱动入门/第七、八期 设备树/assets/第75章 ConfigFS的核心数据结构 - 设备树插件/f9bb17fb010fd25197b3f9a017aafa9e\_MD5.jpeg](assets/第75章%20ConfigFS的核心数据结构%20-%20设备树插件/f9bb17fb010fd25197b3f9a017aafa9e_MD5.jpeg)

> 这段代码定义了一个名为dtbocfg_root_subsys的configfs_subsystem结构体实例，表示**ConfigFS中的一个子系统。**
> 首先，dtbocfg_root_subsys.su_group是一个config_group结构体，它表示子系统的根配置项组。
> 在这里，该结构体的.cg_item字段表示根配置项组的基本配置项。
> = "device-tree"：配置项的名称设置为"device-tree"，表示该**配置项的名称为"device-tree"。**
> = &dtbocfg_root_type：**配置项的类型设置为dtbocfg_root_type**，这是一个自定义的配置项类型。
> 接下来，**.su_mutex字段是一个互斥锁，用于保护子系统的操作**。在这里，使用了__MUTEX_INITIALIZER宏来初始化互斥锁。



> 通过这段代码，**创建了一个名为"device-tree"的子系统，它的根配置项组为空。可以在该子系统下添加更多的配置项和配置项组**，用于动态配置和管理设备树相关的内核对象。Linux系统下创建了device-tree这个子系统，如下图（图 75-3）所示：
[[嵌入式知识学习（通用扩展）/linux驱动入门/第七、八期 设备树/assets/第75章 ConfigFS的核心数据结构 - 设备树插件/5c85fbaa9cf2b09b0857f06a715a7745_MD5.jpeg|Open: file-20250906203218315.png]]
![嵌入式知识学习（通用扩展）/linux驱动入门/第七、八期 设备树/assets/第75章 ConfigFS的核心数据结构 - 设备树插件/5c85fbaa9cf2b09b0857f06a715a7745\_MD5.jpeg](assets/第75章%20ConfigFS的核心数据结构%20-%20设备树插件/5c85fbaa9cf2b09b0857f06a715a7745_MD5.jpeg)



### 5、分析注册配置项组的部分

```c
//初始化和注册ConfigFS子系统和配置项组
static int __init dtbocfg_module_init(void) {
	int retval = 0;
	
	pr_info("%s\n",__func__);

	// 初始化了dtbocfg_root_subsys.su_group，即子系统的根配置项组
	config_group_init(&dtbocfg_root_subsys.su_group);
	
	// 初始化了dtbocfg_overlay_group，表示名为"overlays"的配置项组，并指定了配置项组的类型为dtbocfg_overlays_type，
	config_group_init_type_name(&dtbocfg_overlay_group, "overlays", &dtbocfg_overlays_type);

	// 注册根配置子系统
	retval = configfs_register_subsystem(&dtbocfg_root_subsys);
	if (retval != 0) {
		pr_err("%s: couldn't register subsys\n", __func__);
		goto register_subsystem_failed; 
	}

	// 注册了dtbocfg_overlay_group配置项组，并将其添加到dtbocfg_root_subsys.su_group下。
	retval = configfs_register_group(&dtbocfg_root_subsys.su_group, &dtbocfg_overlay_group);
	if (retval != 0) {
		pr_err("%s: couldn't register group\n", __func__); 
		goto register_group_failed; 
	}

	pr_info("%s: ok\n", __func__); // 打印初始化成功信息
	return 0;

register_group_failed:
	configfs_unregister_subsystem(&dtbocfg_root_subsys); //注销之前注册的子系统

register_subsystem_failed:
	return retval; // 返回注册失败的错误码retval。

}
```

> 这段代码的作用是初始化和注册一个名为"device-tree"的ConfigFS子系统，并在其下创建一个名为"overlays"的配置项组。Linux系统下，**在device-tree子系统下创建了overlays容器**，如下图（图 75-5）所示：
[[嵌入式知识学习（通用扩展）/linux驱动入门/第七、八期 设备树/assets/第75章 ConfigFS的核心数据结构 - 设备树插件/34c3b989db7b4f84447d520b09ccdd5a_MD5.jpeg|Open: file-20250906203815157.png]]
![嵌入式知识学习（通用扩展）/linux驱动入门/第七、八期 设备树/assets/第75章 ConfigFS的核心数据结构 - 设备树插件/34c3b989db7b4f84447d520b09ccdd5a\_MD5.jpeg](assets/第75章%20ConfigFS的核心数据结构%20-%20设备树插件/34c3b989db7b4f84447d520b09ccdd5a_MD5.jpeg)



### 6、



## 属性和方法
### 1 、config_item结构体（目录）
- 1 在容器下放目录或属性文件，所以我们看一下config_item结构体
```c
struct config_item {
	char			*ci_name;
	char			ci_namebuf[CONFIGFS_ITEM_NAME_LEN];  //目录的名字
	struct kref		ci_kref;
	struct list_head	ci_entry;
	struct config_item	*ci_parent;
	struct config_group	*ci_group;
	const struct config_item_type	*ci_type;  //目录下属性文件和属性操作
	struct dentry		*ci_dentry;
};
```

#### config_item_type结构体（目录下属性文件和属性操作）
```c
struct config_item_type {
	struct module *ct_owner;
	struct configfs_item_operations *ct_item_ops; //item（目录）的操作方法
	struct configfs_group_opereations *ct_group_ops; //group（容器）的操作方法
	struct configfs_attribute **ct_attrs; //属性文件的操作方法
	struct configfs_bin_attribute **ct_bin_attrs; //bin属性文件的操作方法

};
```


##### struct configfs_item_operations结构体（item（目录）的操作方法）
```c
struct configfs_item_operations {
//删除item方法，在group下面使用rmdir命令会调用这个方法
	void (*release)(struct config_item *);
	int (*allow_link)(struct config_item *src, struct config_item *target);
	void (*drop_link)(struct config_item *src, struct config_item *target);
};

```

##### struct configfs_attribute结构体（属性文件的操作方法）
```c
struct configfs_group_operations {
	//创建item的方法，在group下面使用mkdir命令会调用这个方法
struct config_item *(*make_item)(struct config_group *group, const char *name); 
	//创建group的方法
struct config_group *(*make_group)(struct config_group *group, const char *name);
	int (*commit_item)(struct config_item *item);
	void (*disconnect_notify)(struct config_group *group, struct config_item *item);
	void (*drop_item)(struct config_group *group, struct config_item *item);
};
```

##### struct configfs_group_operations结构体（group（容器）的操作方法）
```c
struct configfs_group_operations {
	//创建item的方法，在group下面使用mkdir命令会调用这个方法
struct config_item *(*make_item)(struct config_group *group, const char *name); 
	//创建group的方法
struct config_group *(*make_group)(struct config_group *group, const char *name);
	int (*commit_item)(struct config_item *item);
	void (*disconnect_notify)(struct config_group *group, struct config_item *item);
	void (*drop_item)(struct config_group *group, struct config_item *item);
};
```





## 总结
### 1 、核心数据结构相互关联


### 2 、通过在ConfigFS层级结构进行组织和管理，使得设备的配置和管理更加灵活和可定制


### 3 、图解
[[嵌入式知识学习（通用扩展）/linux驱动入门/第七、八期 设备树/assets/第75章 ConfigFS的核心数据结构 - 设备树插件/3e242a0d1e6e45db8bf8d2afdfa705f5_MD5.jpeg|Open: file-20250906215745527.png]]
![嵌入式知识学习（通用扩展）/linux驱动入门/第七、八期 设备树/assets/第75章 ConfigFS的核心数据结构 - 设备树插件/3e242a0d1e6e45db8bf8d2afdfa705f5\_MD5.jpeg](assets/第75章%20ConfigFS的核心数据结构%20-%20设备树插件/3e242a0d1e6e45db8bf8d2afdfa705f5_MD5.jpeg)


### 移植设备树插件驱动实验（官方驱动）
> [root@topeet:~]# ls
> device_tree.ko  dtbocfg.ko
> [root@topeet:~]# `insmod dtbocfg.ko`
> 
> [root@topeet:`/sys/kernel/config`]# ls
> `device-tree`  usb_gadget
> [root@topeet:/sys/kernel/config]# cd device-tree/
> [root@topeet:/sys/kernel/config/device-tree]# ls
> `overlays`
> [root@topeet:/sys/kernel/config/device-tree]# cd overlays/
> [root@topeet:/sys/kernel/config/device-tree/overlays]# ls
> [root@topeet:/sys/kernel/config/device-tree/overlays]# ls
> [root@topeet:/sys/kernel/config/device-tree/overlays]# `mkdir test`
> [root@topeet:/sys/kernel/config/device-tree/overlays]# ls
> `test`
> [root@topeet:/sys/kernel/config/device-tree/overlays]# cd test
> [root@topeet:/sys/kernel/config/device-tree/overlays/test]# ls
> `dtbo  status`
> 






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


