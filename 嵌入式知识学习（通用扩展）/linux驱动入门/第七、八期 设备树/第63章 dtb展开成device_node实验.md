---
title: "{{title}}"
aliases: 
tags: 
description: 
source:
---

# 备注(声明)：deb文件是怎样传递给内核的呢？



# 参考文档：
```cardlink
url: https://blog.csdn.net/BeiJingXunWei/article/details/134333827
title: "RK3568驱动指南｜第七期-第63章 dtb展开成device_node实验_rk3568 android 更新dtb-CSDN博客"
description: "文章浏览阅读669次。本文围绕Linux系统中dtb展开成device_node实验展开。先介绍dtb展开流程，包括设备树编写、编译、镜像生成、加载及内核初始化等步骤。接着对dtb解析过程进行源码分析，详细讲解setup_machine_fdt和unflatten_device_tree两个关键函数的实现逻辑。"
host: blog.csdn.net
```




# 一、dtb展开流程和device_node结构体

## dtb展开流程
### 1 、图解
[[嵌入式知识学习（通用扩展）/linux驱动入门/第七、八期 设备树/assets/第63章 dtb展开成device_node实验/3a4ee1de36929360447bbb6abde88f00_MD5.jpeg|Open: file-20250901114930347.png]]
![嵌入式知识学习（通用扩展）/linux驱动入门/第七、八期 设备树/assets/第63章 dtb展开成device\_node实验/3a4ee1de36929360447bbb6abde88f00\_MD5.jpeg](assets/第63章%20dtb展开成device_node实验/3a4ee1de36929360447bbb6abde88f00_MD5.jpeg)

### 2 、dtb的展开流程进行详细的讲解(❤️)
> （1）`设备树源文件编写`：根据之前的章节中讲解的设备树的基本语法和相关知识编写符合规范的设备树。
> 
> （2）`设备树编译`：设备树源文件经过设备树编译器（dtc）进行编译，生成设备树二进制文件（.dtb）。设备树编译器会检查源文件的语法和语义，并将其转换为二进制格式，以便内核能够解析和使用。
> 
> （3）`boot.img镜像生成`：boot.img是一个包含内核镜像、设备树二进制文件和其他一些资源文件的镜像文件（目前只是适用于瑞芯微的soc上，其他厂商的soc需要具体问题具体分析）。在生成boot.img时，通常会将内核镜像、设备树二进制文件和其他一些资源文件**打包**在一起。这个过程可以使用特定的工具或脚本完成。
> 
> （4）`U-Boot加载`：U-Boot（Universal Bootloader）是一种常用的开源引导加载程序，用于引导嵌入式系统。在系统启动过程中，U-Boot会将boot.img中的内核和设备树的二进制文件**加载到系统内存的特定地址**。
> 
> （5）`内核初始化`：U-Boot将内核和设备树的二进制文件加载到系统内存的特定地址后，控制权会转交给内核。在内核初始化的过程中，会**解析设备树二进制文件，将其展开为内核可以识别的数据结构**，以便内核能够正确地初始化和管理硬件资源。
> 
> （6）`设备树展开`：设备树展开是指将设备树二进制文件解析成内核中的设备节点（device_node）的过程。内核会读取设备树二进制文件的内容，并根据设备树的描述信息，**构建设备树数据结构，例如设备节点、中断控制器、寄存器、时钟等**。这些设备树数据结构将在内核运行时用于管理和配置硬件资源。

### 3 、device_node结构体（最终设备树二进制文件会被解析成）(❤️)
- 1 定义在内核源码的“/include/linux/of.h”文件中
```c
struct device_node {
	const char *name;                // 设备节点的名称
	const char *type;                // 设备节点的类型
	phandle phandle;                  // 设备节点的句柄
	const char *full_name;           // 设备节点的完整名称
	struct fwnode_handle fwnode;     // 设备节点的固件节点句柄
 
	struct property *properties;     // 设备节点的属性列表
	struct property *deadprops;      // 已删除的属性列表
	struct device_node *parent;      // 父设备节点指针
	struct device_node *child;       // 子设备节点指针
	struct device_node *sibling;     // 兄弟设备节点指针
#if defined(CONFIG_OF_KOBJ)
	struct kobject kobj;             // 内核对象（用于 sysfs）
#endif
	unsigned long _flags;            // 设备节点的标志位
	void *data;                      // 与设备节点相关的数据指针
#if defined(CONFIG_SPARC)
	const char *path_component_name; // 设备节点的路径组件名称
	unsigned int unique_id;          // 设备节点的唯一标识
	struct of_irq_controller *irq_trans; // 设备节点的中断控制器
#endif
};
```

#### 参数进行讲解(❤️)
> （1）name：name 字段表示**设备节点的名称**。设备节点的名称是在设备树中唯一标识该节点的字符串。它通常用于在设备树中引用设备节点。

> （2）type：type 字段表示**设备节点的类型**。设备节点的类型提供了关于设备节点功能和所属设备类别的信息。它可以用于识别设备节点的用途和特性。


> （3）`properties`：properties 字段是**指向设备节点属性列表的指针**。设备节点的属性包含了与设备节点相关联的配置和参数信息。**属性以键值对的形式存在**，可以提供设备的特定属性、寄存器地址、中断信息等。property字段同样定义在内核源码的“/include/linux/of.h”文件中，具体内容如下所示：
```c
struct property {
	char *name;                    // 属性的名称
	int length;                    // 属性值的长度（字节数）
	void *value;                   // 属性值的指针
	struct property *next;         // 下一个属性节点指针
	
#if defined(CONFIG_OF_DYNAMIC) || defined(CONFIG_SPARC)
	unsigned long _flags;          // 属性的标志位
#endif

#if defined(CONFIG_OF_PROMTREE)
	unsigned int unique_id;        // 属性的唯一标识
#endif

#if defined(CONFIG_OF_KOBJ)
	struct bin_attribute attr;     // 内核对象二进制属性
#endif
};

```

> （4）parent：parent 字段**指向父设备节点**。设备树中的设备节点按照层次结构组织，父设备节点是当前设备节点的直接上级。通过 parent 字段，可以在设备树中遍历设备节点的父子关系。

> （5）child：child 字段指向**子设备节点**。在设备树中，一个设备节点可以拥有多个子设备节点。通过 child 字段，可以遍历设备节点的所有子设备节点。

> （6）sibling：sibling 字段指向**兄弟设备节点**。在设备树中，同一级别的兄弟设备节点共享相同的父设备节点。通过 sibling 字段，可以在同级设备节点之间进行遍历。






### 4 、






# 二、dtb解析过程源码分析

## start_kernel 函数
### 1 、Linux 内核启动的入口点


### 2 、完成内核的初始化和启动过程


### 3 、函数具体内容分析
- 1 源码目录下的“/init/main.c”文件      kernel/init/main.c
```c
asmlinkage __visible void __init start_kernel(void)
{
    char *command_line;
    char *after_dashes;
 
    set_task_stack_end_magic(&init_task);    // 设置任务栈的魔数
    smp_setup_processor_id();    // 设置处理器ID
    debug_objects_early_init();    // 初始化调试对象
    cgroup_init_early();    // 初始化cgroup（控制组）
 
    local_irq_disable();    // 禁用本地中断
    early_boot_irqs_disabled = true;     // 标记早期引导期间中断已禁用
 
    /*
     * 中断仍然被禁用。进行必要的设置，然后启用它们。
     */
    boot_cpu_init();    // 初始化引导CPU
    page_address_init();    // 设置页地址
    pr_notice("%s", linux_banner);    // 打印Linux内核版本信息
    setup_arch(&command_line);    // 架构相关的初始化
    mm_init_cpumask(&init_mm);    // 初始化内存管理的cpumask（CPU掩码）
    setup_command_line(command_line);    // 设置命令行参数
    setup_nr_cpu_ids();    // 设置CPU个数
    setup_per_cpu_areas();    // 设置每个CPU的区域
    smp_prepare_boot_cpu();    // 准备启动CPU（架构特定的启动CPU钩子）
    boot_cpu_hotplug_init();    // 初始化热插拔的引导CPU
 
    build_all_zonelists(NULL);    // 构建所有内存区域列表
    page_alloc_init();    // 初始化页面分配器
	........
}
```

- 1 跟设备树相关的函数为第20行的 `setup_arch(&command_line);`
- 2 定义在内核源码的“/arch/arm64/kernel/setup.c”文件中
```c
void __init setup_arch(char **cmdline_p)
{
	init_mm.start_code = (unsigned long) _text;
	init_mm.end_code   = (unsigned long) _etext;
	init_mm.end_data   = (unsigned long) _edata;
	init_mm.brk	   = (unsigned long) _end;
 
	*cmdline_p = boot_command_line;
 
	early_fixmap_init();    // 初始化 early fixmap
	early_ioremap_init();    // 初始化 early ioremap
 
	setup_machine_fdt(__fdt_pointer);    // 设置机器的 FDT（平台设备树）
 
	// 初始化静态密钥，早期可能会被 cpufeature 代码和早期参数启用
	jump_label_init();
	parse_early_param();
 
	// 在启动可能的早期控制台后，解除屏蔽异步中断和 FIQ（一旦我们可以报告发生的系统错误）
	local_daif_restore(DAIF_PROCCTX_NOIRQ);
 
	// 在这个阶段，TTBR0仅用于身份映射。将其指向零页面，以避免做出猜测性的新条目获取。
	cpu_uninstall_idmap();
 
	xen_early_init();    // Xen 平台的早期初始化
	efi_init();    // EFI 平台的初始化
	arm64_memblock_init();    // ARM64 内存块的初始化
 
	paging_init();    // 分页初始化
 
	acpi_table_upgrade();    // ACPI 表的升级
 
	// 解析 ACPI 表以进行可能的引导时配置
	acpi_boot_table_init();
 
	if (acpi_disabled)
		unflatten_device_tree();    // 展开设备树
 
	bootmem_init();    // 引导内存的初始化
	............
}
```
- 1 与设备树相关的函数分别为第13行的`setup_machine_fdt(__fdt_pointer)`和第37行的`unflatten_device_tree()`


### 4 、函数调用关系(❤️)
```c
start_kernel(void)


	setup_arch(&command_line); // 架构相关的初始


		setup_machine_fdt(__fdt_pointer); // 设置机器的 FDT（平台设备树）
		unflatten_device_tree(); // 展开设备树

```

### 5、



## `setup_machine_fdt(__fdt_pointer)`
### 1 、设置机器的 FDT（平台设备树）


### 2 、`__fdt_pointer`参数的来源(❤️)
> `__fdt_pointer`是**dtb二进制文件加载到内存的地址**，


> 该地址`由bootloader启动kernel时透过x0寄存器传递过来`的，具体的汇编代码在内核源码目录下的“/arch/arm64/kernel/head.S”文件中，具体内容如下所示：
```c
preserve_boot_args:
	mov	x21, x0				// x21=FDT
 
__primary_switched:
	str_l	x21, __fdt_pointer, x5		// Save FDT pointer
```
> 第2行: 将寄存器 x0 的值复制到寄存器 x21。x0 寄存器中保存了一个指针，该指针指向设备树（Device Tree）。
> 
> 第4行: 将寄存器 x21 的值存储到内存地址 `__fdt_pointer `中。



### 3 、setup_machine_fdt函数解析
- 1 定义在内核源码的“/arch/arm64/kernel/setup.c”文件
```c
// 初始化设置机器的设备树
static void __init setup_machine_fdt(phys_addr_t dt_phys)
{
    int size;
    // 将设备树物理地址映射到内核虚拟地址空间
    void *dt_virt = fixmap_remap_fdt(dt_phys, &size, PAGE_KERNEL);
    const char *name;
 
    // 如果映射成功
    if (dt_virt) {
        // 保留设备树占用的内存区域
        memblock_reserve(dt_phys, size);
    }
 
    // 如果设备树映射失败或者设备树解析失败
    if (!dt_virt || !early_init_dt_scan(dt_virt)) {
        // 输出错误信息
		pr_crit("\n"
			"Error: invalid device tree blob at physical address %pa (virtual address 0x%p)\n"
			"The dtb must be 8-byte aligned and must not exceed 2 MB in size\n"
			"\nPlease check your bootloader.",
			&dt_phys, dt_virt);
        // 无限循环，等待系统崩溃
        while (true)
            cpu_relax();
    }
 
    // 早期修复完成，将设备树映射为只读模式
    fixmap_remap_fdt(dt_phys, &size, PAGE_KERNEL_RO);
 
    // 获取设备树的机器名
    name = of_flat_dt_get_machine_name();
    // 如果设备树没有机器名，则返回
    if (!name)
        return;
	    pr_info("Machine model: %s\n", name); // 输出机器型号信息
    dump_stack_set_arch_desc("%s (DT)", name); // 设置栈转储的架构描述为机器型号
}
```

> 此函数用于在内核启动过程中设置机器的设备树。在此函数中，将执行以下步骤：
> 
> 1.使用 fixmap_remap_fdt() 将设备树**映射到内核虚拟地址空间**中的 fixmap 区域。
> 
> 2.如果映射成功，则使用 memblock_reserve() **保留设备树占用的物理内存区域**。
> 
> 3.**检查**设备树的有效性和完整性，通过调用early_init_dt_scan()进行早期扫描。 如果设备树无效或扫描失败，则会输出错误信息并进入死循环。
> 
> 4.早期修复已完成，现在将设备树**映射为只读**，通过调用 fixmap_remap_fdt() 实现。
> 
> 5.**获取设备树中的机器模型名称**，通过调用 of_flat_dt_get_machine_name()。
> 
> 6.如果机器模型名称存在，则输出机器模型的信息，并通过 dump_stack_set_arch_desc() **设置堆栈描述信息**。

#### 第3步调用的early_init_dt_scan() 需要详细的讲解一下
- 1 定义在内核源码的“drivers/of/fdt.c”目录下
```c
bool __init early_init_dt_scan(void *params)
{
    bool status;
 
    // 验证设备树的兼容性和完整性
    status = early_init_dt_verify(params);
    if (!status)
        return false;
 
    // 扫描设备树节点
    early_init_dt_scan_nodes();
    return true;
}
```

##### early_init_dt_verify() 函数解析
> 该函数可能会检查设备树中的**一致性标记、版本信息以及必需的节点和属性是否存在**。如果验证失败，函数会返回 false。
```c
bool __init early_init_dt_verify(void *params)
{
    // 验证传入的参数是否为空
    if (!params)
        return false;
 
    // 检查设备树头部的有效性
    // 如果设备树头部无效，返回 false
    if (fdt_check_header(params))
        return false;
 
    // 设置指向设备树的指针为传入的参数
    initial_boot_params = params;
 
    // 计算设备树的 CRC32 校验值
    // 并将结果保存在全局变量 of_fdt_crc32 中
    of_fdt_crc32 = crc32_be(~0, initial_boot_params, fdt_totalsize(initial_boot_params));
 
    // 返回 true，表示设备树验证和初始化成功
    return true;
}
```

> 第4行：该进行参数的有效性检查，如果 params 为空，则直接返回 false，表示参数无效。
> 
> 第9行：检查设备树头部的有效性。fdt_check_header 是一个用于检查设备树头部的函数，如果设备树头部无效，则返回 false，表示设备树不合法。
> 
> 第13行：如果设备树头部有效，程序继续执行，**将传入的 params 赋值给全局变量 initial_boot_params，用来保存设备树的指针**。
> 
> 第17行，使用 crc32_be 函数计算设备树的 **CRC32 校验值**，其中 crc32_be 是一个用于计算 CRC32 校验值的函数，~0 表示初始值为全1的位模式。计算完成后，将**结果保存在全局变量 of_fdt_crc32 中**。


##### early_init_dt_scan_nodes() 函数解析(❤️)
- 1 扫描设备树的节点并进行相应的处理
```c
void __init early_init_dt_scan_nodes(void)
{
	/* 从 /chosen 节点中检索各种信息 */
	of_scan_flat_dt(early_init_dt_scan_chosen, boot_command_line);
 
	/* 初始化 {size,address}-cells 信息 */
	//
	of_scan_flat_dt(early_init_dt_scan_root, NULL);
 
	/* 设置内存信息，调用 early_init_dt_add_memory_arch 函数 */
	of_scan_flat_dt(early_init_dt_scan_memory, NULL);
}
```
> 函数early_init_dt_scan_nodes被**声明为__init，这表示它是在内核初始化阶段被调用**，并且**在初始化完成后不再需要**。该函数的目的是在早期阶段扫描设备树节点，并执行一些初始化操作。

> 函数中主要调用了of_scan_flat_dt函数，该函数用于扫描平面设备树（flat device tree）。平面设备树是一种将设备树以紧凑形式表示的数据结构，它不使用树状结构，而是使用线性结构，以节省内存空间。

> 具体来看，early_init_dt_scan_nodes函数的执行步骤如下：
> 
> （1）`of_scan_flat_dt(early_init_dt_scan_chosen, boot_command_line)`：从设备树的<span style="background:#d3f8b6">/chosen节点中检索各种信息</span>。/chosen节点通常包含了一些系统的全局配置参数，比如命令行参数。early_init_dt_scan_chosen是一个回调函数，用于处理/chosen节点的信息。<span style="background:#d3f8b6">boot_command_line是一个参数，表示内核启动时的命令行参数</span>。
> 
> （2）`of_scan_flat_dt(early_init_dt_scan_root, NULL)`：**初始化{size,address}-cells信息**。{size,address}-cells描述了设备节点中地址和大小的编码方式。early_init_dt_scan_root是一个回调函数，用于**处理设备树的根节点**。
> 
> （3）`of_scan_flat_dt(early_init_dt_scan_memory, NULL)`：**设置内存信息**，并调用early_init_dt_add_memory_arch函数。这个步骤主要用于在设备树中获取内存的相关信息，并将其传递给内核的内存管理模块。early_init_dt_scan_memory是一个回调函数，用于处理内存信息。




### 4 、


### 5、




## `unflatten_device_tree`
### 1 、展开设备树


### 2 、解析设备树，将紧凑的设备树数据结构转换为树状结构的设备树(❤️)


### 3 、`unflatten_device_tree`函数解析
- 1 定义在内核源码目录下的“/drivers/of/fdt.c”文件
```c
void __init unflatten_device_tree(void)
{
    /* 解析设备树 */
    __unflatten_device_tree(initial_boot_params, NULL, &of_root,
                            early_init_dt_alloc_memory_arch, false);
 
    /* 获取指向 "/chosen" 和 "/aliases" 节点的指针，以供全局使用 */
    of_alias_scan(early_init_dt_alloc_memory_arch);
 
    /* 运行设备树的单元测试 */
    unittest_unflatten_overlay_base();
}
```
> 函数主要用于解析设备树，并**将解析后的设备树存储在全局变量of_root中**。
> 
> 函数首先调用__unflatten_device_tree函数来执行设备树的解析操作。解析后的设备树将使用of_root指针进行存储。
> 
> 接下来，函数调用of_alias_scan函数。这个函数用于**扫描设备树中的/chosen和/aliases节点，并为它们分配内存**。这样，其他部分的代码可以通过全局变量访问这些节点。**以供全局使用**
> 
> 最后，函数调用unittest_unflatten_overlay_base函数，用于**运行设备树的单元测试**。**展开和叠加的基础**


#### `__unflatten_device_tree`函数解析
```c
void *__unflatten_device_tree(const void *blob,
		      struct device_node *dad,
			      struct device_node **mynodes,
			      void *(*dt_alloc)(u64 size, u64 align),
			      bool detached)
{
	int size;
	void *mem;
 
	pr_debug(" -> unflatten_device_tree()\n");
 
	if (!blob) {
		pr_debug("No device tree pointer\n");
		return NULL;
	}
 
 
	pr_debug("Unflattening device tree:\n");
	pr_debug("magic: %08x\n", fdt_magic(blob));
	pr_debug("size: %08x\n", fdt_totalsize(blob));
	pr_debug("version: %08x\n", fdt_version(blob));
 
	if (fdt_check_header(blob)) {
		pr_err("Invalid device tree blob header\n");
		return NULL;
	}
 
	/* 第一遍扫描，计算大小 */
	size = unflatten_dt_nodes(blob, NULL, dad, NULL);
	if (size < 0)
		return NULL;
 
	size = ALIGN(size, 4);
	pr_debug("  大小为 %d，正在分配内存...\n", size);
 
	/* 为展开的设备树分配内存 */
	mem = dt_alloc(size + 4, alignof(struct device_node));
	if (!mem)
		return NULL;
 
	memset(mem, 0, size);
 
	*(__be32 *)(mem + size) = cpu_to_be32(0xdeadbeef);
 
	pr_debug("  正在展开 %p...\n", mem);
 
	/* 第二遍扫描，实际展开设备树 */
	unflatten_dt_nodes(blob, mem, dad, mynodes);
	if (be32_to_cpup(mem + size) != 0xdeadbeef)
		pr_warning("End of tree marker overwritten: %08x\n",
			   be32_to_cpup(mem + size));
 
	if (detached && mynodes) {
		of_node_set_flag(*mynodes, OF_DETACHED);
		pr_debug("unflattened tree is detached\n");
	}
 
	pr_debug(" <- unflatten_device_tree()\n");
	return mem;
}
```
> 该函数的重点在两次设备树的扫描上，第一遍扫描的目的是计算展开设备树所需的内存大小。
> 
> 第29行：`unflatten_dt_nodes函数`的作用是**递归地遍历设备树数据块，并计算展开设备树所需的内存大小**。它接受四个参数：blob（设备树数据块指针）、start（当前节点的起始地址，初始为NULL）、dad（父节点指针）和mynodes（用于存储节点指针数组的指针，初始为NULL）。

> `第一遍扫描`完成后，unflatten_dt_nodes函数会**返回展开设备树所需的内存大小**，然后在对大小进行对齐操作，并为展开的设备树**分配内存**。

> `第二遍扫描`的目的是**实际展开设备树，并填充设备节点的名称、类型和属性**等信息。
> 
> 第49行：再次调用了unflatten_dt_nodes函数进行第二遍扫描。通过这样的过程，第二遍扫描会将设备树数据块中的节点展开为真正的设备节点，并填充节点的名称、类型和属性等信息。这样就完成了设备树的展开过程。

##### unflatten_dt_nodes函数解析
```c
static int unflatten_dt_nodes(const void *blob,
			      void *mem,
			      struct device_node *dad,
			      struct device_node **nodepp)
{
	struct device_node *root;  // 根节点
	int offset = 0, depth = 0, initial_depth = 0;  // 偏移量、深度和初始深度
#define FDT_MAX_DEPTH	64  // 最大深度
	struct device_node *nps[FDT_MAX_DEPTH];  // 设备节点数组
	void *base = mem;  // 基地址，用于计算偏移量
	bool dryrun = !base;  // 是否只是模拟运行，不实际处理
 
	if (nodepp)
		*nodepp = NULL;  // 如果指针不为空，将其置为空指针
 
	/*
	 * 如果 @dad 有效，则表示正在展开设备子树。
	 * 在第一层深度可能有多个节点。
	 * 将 @depth 设置为 1，以使 fdt_next_node() 正常工作。
	 * 当发现负的 @depth 时，该函数会立即退出。
	 * 否则，除第一个节点外的设备节点将无法成功展开。
	 */
	if (dad)
		depth = initial_depth = 1;
 
	root = dad;  // 根节点为 @dad
	nps[depth] = dad;  // 将根节点放入设备节点数组
 
	for (offset = 0;
	     offset >= 0 && depth >= initial_depth;
	     offset = fdt_next_node(blob, offset, &depth)) {
		if (WARN_ON_ONCE(depth >= FDT_MAX_DEPTH))
			continue;
 
		// 如果未启用 CONFIG_OF_KOBJ 并且节点不可用，则跳过该节点
		if (!IS_ENABLED(CONFIG_OF_KOBJ) &&
		    !of_fdt_device_is_available(blob, offset))
			continue;
 
		// 填充节点信息，并将子节点添加到设备节点数组
		if (!populate_node(blob, offset, &mem, nps[depth],
				   &nps[depth+1], dryrun))
			return mem - base;
 
		if (!dryrun && nodepp && !*nodepp)
			*nodepp = nps[depth+1];  // 将子节点指针赋值给 @nodepp
		if (!dryrun && !root)
			root = nps[depth+1];  // 如果根节点为空，则将子节点设置为根节点
	}
 
	if (offset < 0 && offset != -FDT_ERR_NOTFOUND) {
		pr_err("Error %d processing FDT\n", offset);
		return -EINVAL;
	}
 
	// 反转子节点列表。一些驱动程序假设节点顺序与 .dts 文件中的节点顺序一致
	if (!dryrun)
		reverse_nodes(root);
 
	return mem - base;  // 返回处理的字节数
}
```

> nflatten_dt_nodes 函数的作用我们在上面已经讲解过了，这里重点介绍第31行的 fdt_next_node()函数和第41行的populate_node函数。
> 
>` fdt_next_node()` 函数用来**遍历设备树的节点**。从偏移量为 0 开始，只要偏移量大于等于 0 且深度大于等于初始深度，就执行循环。**循环中的每次迭代都会处理一个设备树节点**。
> 
> 在每次迭代中，首先检查深度是否超过了最大深度 FDT_MAX_DEPTH，如果超过了，则跳过该节点。
> 
> 如果未启用 CONFIG_OF_KOBJ 并且节点不可用（通过 of_fdt_device_is_available() 函数判断），则跳过该节点。
> 
> 随后调用` populate_node() `函数**填充节点信息，并将子节点添加到设备节点数组 nps 中**。


###### populate_node() 函数解析
- 1 填充节点信息，并将子节点添加到设备节点数组 nps 中
```c
static bool populate_node(const void *blob,
			  int offset,
			  void **mem,
			  struct device_node *dad,
			  struct device_node **pnp,
			  bool dryrun)
{
	struct device_node *np;  // 设备节点指针
	const char *pathp;  // 节点路径字符串指针
	unsigned int l, allocl;  // 路径字符串长度和分配的内存大小
 
	pathp = fdt_get_name(blob, offset, &l);  // 获取节点路径和长度
	if (!pathp) {
		*pnp = NULL;
		return false;
	}
 
	allocl = ++l;  // 分配内存大小为路径长度加一，用于存储节点路径字符串
 
	np = unflatten_dt_alloc(mem, sizeof(struct device_node) + allocl,
				__alignof__(struct device_node));  // 分配设备节点内存
	if (!dryrun) {
		char *fn;
		of_node_init(np);  // 初始化设备节点
		np->full_name = fn = ((char *)np) + sizeof(*np);  // 设置设备节点的完整路径名
 
		memcpy(fn, pathp, l);  // 将节点路径字符串复制到设备节点的完整路径名中
 
		if (dad != NULL) {
			np->parent = dad;  // 设置设备节点的父节点
			np->sibling = dad->child;  // 设置设备节点的兄弟节点
			dad->child = np;  // 将设备节点添加为父节点的子节点
		}
	}
 
	populate_properties(blob, offset, mem, np, pathp, dryrun);  // 填充设备节点的属性信息
	if (!dryrun) {
		np->name = of_get_property(np, "name", NULL);  // 获取设备节点的名称属性
		np->type = of_get_property(np, "device_type", NULL);  // 获取设备节点的设备类型属性
 
		if (!np->name)
			np->name = "<NULL>";  // 如果设备节点没有名称属性，则设置为"<NULL>"
		if (!np->type)
			np->type = "<NULL>";  // 如果设备节点没有设备类型属性，则设置为"<NULL>"
	}
 
	*pnp = np;  // 将设备节点指针赋值给*pnp
	return true;
}
```

> 在populate_node 函数中首先会调用第18行的 `unflatten_dt_alloc 函数`**分配设备节点内存**。分配的内存大小为 sizeof(struct device_node) + allocl 字节，并使用 `__alignof__(struct device_node) `对齐。然后调用 `populate_properties 函数`**填充设备节点的属性信息**。该函数会解析设备节点的属性，并根据需要分配内存来存储属性值。




### 4 、




## 完整的源码分析流程图(❤️)
[[嵌入式知识学习（通用扩展）/linux驱动入门/第七、八期 设备树/assets/第63章 dtb展开成device_node实验/c875fabaf8e2ad7c3381121f27bbbc78_MD5.jpeg|Open: file-20250901215046931.png]]
![嵌入式知识学习（通用扩展）/linux驱动入门/第七、八期 设备树/assets/第63章 dtb展开成device\_node实验/c875fabaf8e2ad7c3381121f27bbbc78\_MD5.jpeg](assets/第63章%20dtb展开成device_node实验/c875fabaf8e2ad7c3381121f27bbbc78_MD5.jpeg)


## 很复杂，后面再深究



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


