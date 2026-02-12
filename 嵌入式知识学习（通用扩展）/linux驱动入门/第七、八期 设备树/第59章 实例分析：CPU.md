---
title: "RK3568驱动指南｜第七期-设备树-第59章 实例分析：CPU_设备树 cpu-map-CSDN博客"
source: "https://blog.csdn.net/BeiJingXunWei/article/details/134005458"
author:
  - "[[成就一亿技术人!]]"
  - "[[hope_wisdom 发出的红包]]"
published:
created: 2025-09-14
description: "文章浏览阅读841次。通过为每个 cluster 子节点指定适当的 cpu-map-mask，可以定义每个集群中使用的核心。通过在 cpu-map 节点中定义 socket 和 cluster 子节点，并为它们指定适当的 cpu-map-mask，可以提供处理器的拓扑结构信息。它的父节点必须是 cpus 节点，而子节点可以是一个或多个 cluster 和 socket 节点。除了处理器的基本属性，cpus 节点还可以包含其他用于描述处理器拓扑关系的节点，以提供更详细的处理器拓扑信息。Core 节点用于描述处理器的核心。_设备树 cpu-map"
tags:
  - "clippings"
---


# 备注(声明)：


# 参考文章：
[RK3568驱动指南｜第七期-设备树-第59章 实例分析：CPU\_设备树 cpu-map-CSDN博客](https://blog.csdn.net/BeiJingXunWei/article/details/134005458)



# 一、cpus节点

> 设备树的 cpus 节点是用于描述系统中的处理器的一个重要节点。它是**处理器拓扑结构的顶层节点，包含了所有处理器相关的信息**。下面将详细介绍设备树的 cpus 节点的各个方面。

## 节点结构：
### 1 、容器节点，其下包含了系统中每个处理器的子节点。


### 2 、每个子节点的名称通常为 cpu@X，其中 X 是处理器的索引号。
> **每个子节点都包含了与处理器相关的属性，例如时钟频率、缓存大小**等。




### 3 、

## 处理器属性：

### 4 、cpu@X 子节点



### 5、device_type：指示设备类型为处理器（"cpu"）。


### 6、reg：指定处理器的地址范围，通常是物理地址或寄存器地址。


### 7、compatible：指定处理器的兼容性信息，用于匹配相应的设备驱动程序。


### 8、clock-frequency：指定处理器的时钟频率。


### cache-size：指定处理器的缓存大小。



## 处理器拓扑关系：
### 1 、其他用于描述处理器拓扑关系的节点
> 这些节点可以帮助操作系统和软件了解处理器之间的连接关系、组织结构和特性。
> 
**这些节点的嵌套关系可以在 cpus 节点下形成一个层次结构**, 反映了处理器的拓扑结构

### 2 、cpu-map 节点：描述处理器的映射关系，通常在多核处理器系统中使用。


### 3 、socket 节点：描述多处理器系统中的物理插槽或芯片组。（💌）


### 4 、cluster 节点：描述处理器集群，即将多个处理器组织在一起形成的逻辑组。（💌）


### 5、core 节点：描述处理器核心，即一个物理处理器内的独立执行单元。（💌）


### 6、thread 节点：描述处理器线程，即一个物理处理器核心内的线程。


### 7、


### 8、



## 举例
### 1 、单核CPU示例：
```d
cpus {
    #address-cells = <1>;
    #size-cells = <0>;
 
    cpu0: cpu@0 {
        compatible = "arm,cortex-a7";
        device_type = "cpu";
        // 其他属性...
    };
}
```



### 2 、多核CPU示例：
```d
cpus {
    #address-cells = <1>;
    #size-cells = <0>;
 
    cpu0: cpu@0 {
        device_type = "cpu";
        compatible = "arm,cortex-a9";
    };
 
    cpu1: cpu@1 {
        device_type = "cpu";
        compatible = "arm,cortex-a9";
    };
 
    cpu2: cpu@2 {
        device_type = "cpu";
        compatible = "arm,cortex-a9";
    };
 
    cpu3: cpu@3 {
        device_type = "cpu";
        compatible = "arm,cortex-a9";
    };
}
```

> cpus 节点是一个容器节点，包含了 cpu0 子节点。该节点使用了 #address-cells 和 #size-cells 属性来指定地址和大小的单元数量。
> 
> cpu0 子节点代表第一个处理器，具有以下属性：
> 
> compatible 属性指定了处理器的兼容性信息
> 
> device_type 属性指示设备类型为处理器。
> 
> 你可以在此基础上继续添加其他属性来描述处理器的特性，如时钟频率、缓存大小等。


### 3 、



### 4 、





# 二、cpu-map、socket、cluster节点

## cpu-map 节点
### 1 、描述大小核架构处理器的映射关系的节点之一


### 2 、父节点必须是 cpus 节点，而子节点可以是一个或多个 cluster 和 socket 节点
> 可以**定义不同核心和集群之间的连接和组织结构。**



### 3 、

## socket 节点

### 4 、描述处理器插槽（socket）之间的映射关系



### 5、每个 socket 子节点表示一个处理器插槽
> 可以**使用 cpu-map-mask 属性来指定该插槽使用的核心**。通过为每个 socket 子节点指定适当的 cpu-map-mask，可以定义不同插槽中使用的核心。这样，操作系统和软件可以了解到不同插槽之间的核心分配情况。





### 6、
## cluster 节点

### 7、描述核心（cluster）之间的映射关系


### 8、每个 cluster 子节点表示一个核心集群
> 可以**使用 cpu-map-mask 属性来指定该集群使用的核心**。通过为每个 cluster 子节点指定适当的 cpu-map-mask，可以定义每个集群中使用的核心。这样，操作系统和软件可以了解到不同集群之间的核心分配情况。



## 一个大小核架构
### 1 、节点的用处
> 通过在 cpu-map 节点中定义 socket 和 cluster 子节点，并为它们指定适当的 cpu-map-mask，可以**提供处理器的拓扑结构信息**。这对于操作系统和软件来说非常有用，因为它们可以根据这些信息进行任务调度和资源分配的优化，以充分利用大小核架构处理器的性能和能效特性。



### 2 、具体示例如下：

> 这个设备树描述了一个具有多个 CPU 核心的系统，包括四个 Cortex-A53 核心和两个 Cortex-A72 核心。下面是对设备树中各个部分的简要介绍：
> 
> `#address-cells = <2>; 和 #size-cells = <0>;`：这些属性指定了设备树中地址和大小的编码方式。
> 
> cpu-map：这个节点定义了 CPU 的映射关系。它包含了两个簇（clusters）：cluster0 和 cluster1。cluster0 包含了四个核心：core0、core1、core2 和 core3，分别对应 cpu_l0、cpu_l1、cpu_l2 和 cpu_l3。cluster1 包含了两个核心：core0 和 core1，分别对应 cpu_b0 和 cpu_b1。
> 
> cpu_l0、cpu_l1、cpu_l2 和 cpu_l3：这些节点描述了 Cortex-A53 核心。它们具有相同的设备类型 cpu 和兼容性属性 "arm,cortex-a53", "arm,armv8"。
> 
> cpu_b0 和 cpu_b1：这些节点描述了 Cortex-A72 核心。它们具有相同的设备类型 cpu 和兼容性属性 "arm,cortex-a72", "arm,armv8"。

```d
cpus {
    #address-cells = <2>;
    #size-cells = <0>;
    cpu-map {
        cluster0 {
            core0 {
                cpu = <&cpu_l0>;
            };
            core1 {
                cpu = <&cpu_l1>;
            };
            core2 {
                cpu = <&cpu_l2>;
            };
            core3 {
                cpu = <&cpu_l3>;
            };
        };
        cluster1 {
            core0 {
                cpu = <&cpu_b0>;
            };
            core1 {
                cpu = <&cpu_b1>;
            };
        };
    };
 
	cpu_l0: cpu@0 {
		device_type = "cpu";
		compatible = "arm,cortex-a53", "arm,armv8";
	};
 
	cpu_l1: cpu@1 {
		device_type = "cpu";
		compatible = "arm,cortex-a53", "arm,armv8";
	};
 
	cpu_l2: cpu@2 {
		device_type = "cpu";
		compatible = "arm,cortex-a53", "arm,armv8";
	};
 
	cpu_l3: cpu@3 {
		device_type = "cpu";
		compatible = "arm,cortex-a53", "arm,armv8";
	};
 
	cpu_b0: cpu@100 {
		device_type = "cpu";
		compatible = "arm,cortex-a72", "arm,armv8";
	};
 
	cpu_b1: cpu@101 {
		device_type = "cpu";
		compatible = "arm,cortex-a72", "arm,armv8";
	};
};
```

### 3 、



### 4 、


# 三、其他

## core、thread节点
### 1 、描述处理器核心和线程的配置


### 2 、Core 节点用于描述处理器的核心
> 一个处理器通常由多个核心组成，每个核心可以独立执行指令和任务。



### 3 、Thread 节点用于描述处理器的线程
> 线程是在处理器核心上执行的基本执行单元，每个核心可以支持多个线程。


### 4 、描述一个具有16个核心的CPU，一个物理插槽，每个集群中有两个核心，每个核心有两个线程的设备树示例（💌）

> 通过使用 Core 和 Thread 节点，设备树可以**准确描述处理器的核心和线程的配置**

```d
cpus {
    #address-cells = <2>;
    cpu-map {
        socket0 {
            cluster0 {
                core0 {
                    thread0 {
                        cpu = <&CPU0>;
                    };
                    thread1 {
                        cpu = <&CPU1>;
                    };
                };
                core1 {
                    thread0 {
                        cpu = <&CPU2>;
                    };
                    thread1 {
                        cpu = <&CPU3>;
                    };
                };
            };
            cluster1 {
                core0 {
                    thread0 {
                        cpu = <&CPU4>;
                    };
                    thread1 {
                        cpu = <&CPU5>;
                    };
                };
                core1 {
                    thread0 {
                        cpu = <&CPU6>;
                    };
                    thread1 {
                        cpu = <&CPU7>;
                    };
                };
            };
        };
        socket1 {
			cluster0 {
				core0 {
					thread0 {
						cpu = <&CPU8>;
					};
					thread1 {
						cpu = <&CPU9>;
					};
				};
				core1 {
					thread0 {
						cpu = <&CPU10>;
					};
					thread1 {
						cpu = <&CPU11>;
					};
				};
			};
			cluster1 {
				core0 {
					thread0 {
						cpu = <&CPU12>;
					};
					thread1 {
						cpu = <&CPU13>;
					};
				};
				core1 {
					thread0 {
						cpu = <&CPU14>;
					};
					thread1 {
						cpu = <&CPU15>;
					};
				};
			};
		};
    };
};
```

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


