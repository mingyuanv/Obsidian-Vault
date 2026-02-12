---
title: "学习笔记之Linux设备树_linux 设备树-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/136991550?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读3k次，点赞36次，收藏79次。本文详细介绍了设备树的概念、在Linux驱动中的应用，包括设备树的文件结构、基本语法、常用术语，以及核心属性如compatible、status、reg、address-cells和size-cells等。它还涵盖了设备树的编译过程和节点组织，为开发者理解和使用设备树提供了全面指南。"
tags:
  - "clippings"
---
本文详细介绍了设备树的概念、在Linux驱动中的应用，包括设备树的文件结构、基本语法、常用术语，以及核心属性如compatible、status、reg、address-cells和size-cells等。它还涵盖了设备树的编译过程和节点组织，为开发者理解和使用设备树提供了全面指南。

摘要生成于 [C知道](https://ai.csdn.net/?utm_source=cknow_pc_ai_abstract) ，由 DeepSeek-R1 满血版支持， [前往体验 >](https://ai.csdn.net/?utm_source=cknow_pc_ai_abstract)

**目录**

[1\. 什么是设备树](https://blog.csdn.net/sincerelover/article/details/?spm=1001.2014.3001.5502#t0)

[2\. 设备树的常用语](https://blog.csdn.net/sincerelover/article/details/?spm=1001.2014.3001.5502#t1)

[3\. 设备树的文件结构](https://blog.csdn.net/sincerelover/article/details/?spm=1001.2014.3001.5502#t2)

[4\. 设备树的基本语法](https://blog.csdn.net/sincerelover/article/details/?spm=1001.2014.3001.5502#t3)

[5\. 设备树属性](https://blog.csdn.net/sincerelover/article/details/?spm=1001.2014.3001.5502#t4)

---

设备树（Device Tree）是一个描述 硬件 平台和系统设备的 [数据结构](https://so.csdn.net/so/search?q=%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84&spm=1001.2101.3001.7020) ，它以一种可读性强的文本形式，将硬件的层次结构、设备的属性和资源配置等信息整合到一个统一的文档中。这使得不同硬件平台之间可以共享相同的内核代码，实现硬件平台与操作系统内核的解耦，提供了更好的可移植性和兼容性。

## 1\. 什么是设备树

在 Linux 驱动程序中，设备树用来替代Platform\_device等 结构体 用来描述设备的板级信息。Linux设备驱动程序通过特定的API接口从设备树中获取设备信息来对设备进行初始化和操作。详细的讲设备树是一种树状的结构，由节点（Node）和属性（Property）组成。每个节点描述一个硬件设备或资源（例如：CPU、时钟、中断控制器、IO控制器、SPI总线控制器、I2C总线控制器、存储设备等），节点通过父子关系和兄弟关系进行连接，如下所示以一个根节点开始。根节点可以包含一些全局属性和设备节点。每个设备节点以一个路径标识符（例如/cpu@0）和多个属性（键值对）组成。设备节点可以包含子节点，形成嵌套的 [层次结构](https://so.csdn.net/so/search?q=%E5%B1%82%E6%AC%A1%E7%BB%93%E6%9E%84&spm=1001.2101.3001.7020) 。

![](https://i-blog.csdnimg.cn/blog_migrate/23d13b2df438169e7f4ba55e1db87c15.png)

## 2\. 设备树的常用语

在设备树（Device Tree）的语境中，有一些常见的术语和概念。以下是一些常见的设备树用语：

1. **Device Tree (DT)** ：设备树本身，是一种数据结构和语言，用于描述硬件资源信息。
2. **Device Tree Source (DTS)** ：设备树源代码文件，使用特定的语法格式描述片上片外的设备信息，可以理解为C语言的.c文件。
3. **Device Tree Source Include (DTSI)** ：更通用的设备树代码，一般包含在DTS文件中，用于提供共用的设备描述，可以理解为可以理解为C语言的.h文件。
4. **Device Tree Blob (DTB)** ：DTS编译后得到的二进制文件，由BootLoader传递给kernel进行解析，可以理解为c语言的.hex或者bin文件。
5. **Device Tree Compiler (DTC)** ：设备树编译器，用于将DTS文件编译成DTB文件。这个工具类似于gcc，用于编译C语言源代码(可以理解为keli工具)。
6. **硬件资源信息** ：设备树描述的信息包括CPU的数量和类别、内存基地址和大小、总线和桥、外设连接、中断控制器和中断使用情况、GPIO控制器和GPIO使用情况、Clock控制器和Clock使用情况等。
7. **节点（Node）** ：在设备树中用来描述硬件设备或资源的一个独立部分。每个节点都有一个唯一的路径和一组属性。
8. **属性（Property）** ：用于描述节点的特征和配置信息，包括设备的名称、地址、中断号、寄存器配置等。
9. **属性值（Property Value）** ：属性中的具体数据，可以是整数、字符串、布尔值等各种类型。
10. **父节点和子节点（Parent Node and Child Node）** ：在设备树中，每个节点都可以有一个父节点和多个子节点，用于描述设备之间的连接关系。

## 3\. 设备树的文件结构

我们通常使用`.dts` （ [设备树源文件](https://so.csdn.net/so/search?q=%E8%AE%BE%E5%A4%87%E6%A0%91%E6%BA%90%E6%96%87%E4%BB%B6&spm=1001.2101.3001.7020) ）或`.dtsi` （设备树源文件包含文件）来写设备树。编写完成以后通过DTC工具编译生成 `.dtb` （设备树二进制）文件，内核在启动时加载这个二进制文件来获得必要的硬件信息。DTS、DTSI、DTC、DTB之间的关系如下图：

![](https://i-blog.csdnimg.cn/blog_migrate/99fd5ab4f60ae99c26e1582903da2008.png)

归类下来常用的文件为以下四类：DTS、DTSI、DTB和Makefile。它们各有不同的作用，并且之间存在一定的关系。

- DTS文件是设备树的源文件，以".dts"为后缀。它使用一种特定的语法，用于描述硬件设备及其相关信息，比如设备名称、类型、地址、中断等。DTS文件是人可读的文本文件，可以被处理器编译成DTB文件，它相当于C语言中的.c文件。
- DTSI文件是设备树源文件的包含文件，以".dtsi"为后缀。它用于存储一些常用的设备树片段，这些片段可以在多个DTS文件中重复使用，避免了代码重复。DTSI文件可以在DTS文件中进行包含（类似C语言的#include），以便重用其中定义的设备树片段。
- DTB文件是设备树的二进制文件，以".dtb"为后缀。它是通过将DTS文件编译而来的，使用了特定的 编译器 工具，比如 `dtc` （Device Tree Compiler）。DTB文件是机器可读的二进制格式，可以被操作系统加载和解析，以用于设备驱动的配置和初始化。它相当于C语言中的.bin文件。
- Makefile：Makefile是一个用于构建和编译项目的脚本文件。在设备树的上下文中，Makefile用于自动化编译和构建DTS/DTSI文件，生成对应的DTB文件。

这里我们可以简单测试一下：

先输入" vim input\_file.dts "命令，生成一个.dts文件，内容简单输入为：

```cobol
/dts-v1/;

 

/ {

};
```

输入完成后按下Esc键，并输入:wq，对文档进行保存。之后在输入 "dtc -I dts -O dtb -o out\_file.dtb input\_file.dts" （不用提前创建out\_file.dtb input\_file.dts文件），之后输入ls查看一下目录可以看到已经产生了两个文件，通过cat命令查看得知out\_file.dtb文件里面是乱码，这里可以再输入 "dtc -I dtb -O dts -o backoutput\_file.dts out\_file.dtb" 进行反编（同样不用预先创建文件），再次使用cat命令查看backoutput\_file.dts文件，可以看到和我们之前在input\_file.dts文件中输入的是一致的。

![](https://i-blog.csdnimg.cn/blog_migrate/78343bd63fb1eb517d273bbb84385daa.png)

## 4\. 设备树的基本语法

**版本**

在设备树文件中通过 `/dts-v1/;`来指定版本，一般写在dts的第一行，如上例所示。这个声明非常重要的，因为他描述了了设备树文件所使用的语法和规范版本。

**注释**

和C语言一样，有两种方法分别如下：//XXX，或者/\*XXX\*/。

**头文件**

前面我们已经讲了dts是源文件，头文件是dtsi，在设备树中主要有两种方法去包含头文件。

- 设备树语法
```cobol
//xxxx是你要包含的文件名称

/include/ "xxxx.dtsi"
```
- C语言语法
```cpp
#include "xxxx.dtsi" //xxxx是你要包含的dtsi文件名称 

或者 #include "xxxx.h" //xxxx是你要包含的.h文件名称
注：由于这种这种方式并非是标志的设备树语言，所以需要利用cpp工具将头文件展开，生成一个临时文件，如下所示：
```
```
cpp -nostdinc -I[dir_with_dts_includes] -x assembler-with-cpp [src_dts_file] > [tmp_dts_file]
```
- `-nostdinc` ：不使用标准的系统头文件目录，避免不必要的报错。
- `-I[dir_with_dts_includes]` ：这里是头文件的目录，如果就是在当前目录就用 `I.`。
- `[src_dts_file]` 是你的源设备树文件（`.dts` ）。
- `[tmp_dts_file]` 是预处理后的输出文件，为了和瑞芯微保持统一我们到时候命名后最写成 `xxxxxxxxxxxx.dtb.dts.tmp`

**设备树节点**

- **根节点**

设备树的根节点是设备树结构中的顶层节点，也是整个设备树的入口点。

**注：根节点没有节点名，它直接使用“/”指代这是一个根节点。**

```bash
/dts-v1/; // 指定这是一个设备树文件的版本（v1）

 

/ {// 根节点定义开始

    /* 这里是根节点，它代表整个设备树的基础。

       在这里可以定义一些全局属性或者包含更多的子节点。 */

    node1-name@unit-address{   //节点1

        compatible = "xxx,xxx";

        a-string-property = "A string"; //节点属性和属性值

        a-string-list-property = "first string";

        a-byte-data-property = [0x00 0x13 0x24 0x36];

        

        label: child-node1{  //节点1的子节点1，label是标签

            first-child-property;

            second-child-property = <1>;

            a-string-property = "hello";

        };

        child-node2{}; //子节点2

    }

    node2-name{ // 节点2

        an-empty-property;

        a-cell-property = <1 2 3 4>;

        

        child-node1{ //节点2的子节点

            my-cousin = <&cousin>;

        };

    }

}; // 根节点定义结束
```
- **子节点**

子节点格式通常由以下几个基本元素组成：

1. **节点名和可选的单元地址**
	1. 节点名通常是相关硬件设备或功能的名称，可选的单元地址表示设备的特定实例或资源，如内存地址、设备ID等。另外，节点名应当使用大写或小写字母开头，并且能够描述设备类别。
	2. 其中的符号“@”可以理解为是一个分割符，“unit- address ”用于指定“单元地址”， 它的值要和节点“reg”属性的第一个地址一致。如果节点没有“reg”属性值，可以直接省略“@unit-address”， 不过要注意这时要求同级别的设备树下(相同级别的子节点)节点名唯一,从这个侧面也可以了解到， 同级别的子节点的节点名可以相同，但是要求“单元地址”不同，node1-name@unit-address的整体要求同级唯一。
2. **一对花括号** **`{}`** ：花括号用于封装节点的属性和子节点内容，包括开始花括号和结束花括号。
3. **属性定义** ：节点中定义了一系列属性，属性有名称和值，具体的值可以是数字、字符串或者数据数组等，属性和值之间使用等号 `=` 相连。节点属性分为标准属性和自定义属性，也就是说我们在设备树中可以根据自己的实际需要定义、添加设备属性。 标准属性的属性名是固定的，自定义属性名可按照要求自行定义。
4. **子节点定义** ：一个节点可以包含多个子节点，这些子节点又可以进一步定义更为详细的属性或包含它们自己的子节点，从而创建一个层次结构。
	```cobol
	/dts-v1/;  // 设备树编译器版本信息
	 
	/ {  // 根节点
	    node1 {  // 第一个子节点
	        child_node {  // node1 的子节点
	            // 空节点，没有定义任何属性或子节点
	        };
	    };
	    
	    node2 {  // 第二个子节点
	        // 空节点，没有定义任何属性或子节点
	    };
	};
	```
- **标签**

标签在节点名中不是必须的，但是我们可以通过他来更方便的操作节点，在设备树文件中有大量使用到。下面例子中定义了标签，并通过引用 `I2C` 标签方式往i2c@91000000中追加一个 `node` 节点。通常节点标签是节点名的简写，所以它的作用是当其它位置需要引用时可以使用节点标签来向该节点中追加内容。

```bash
/dts-v1/;

 

/ {

    

    // I2C 控制器及设备示例，i2c1是标签

    i2c1: i2c@91000000 {

        node_add2{

        };

    };

    // USB 控制器示例，USB是标签

    usb1: usb@92000000 {

    };

};
```

这里需要着重提到的一点是，在实际的代码编程中我们可能常常需要额外添加子节点，这个时候就可以用到标签，例如：

```cobol
&i2c1{ // 通过引用标签的方式往IIC控制器中追加一个节点非覆盖。

    node_add2{

    };

};
```
- **别名**

aliases是一种在设备树中提供简化标识符的方式。它们主要用来为复杂的节点提供一个简单的别名，目的是为了方便引用，和标签有异曲同工之妙，但他们的作用是用途都不同，标签是针对特定设备节点的命名，而别名是针对设备节点路径的命名。

```bash
/dts-v1/;

 

/ {

    // 别名定义

    aliases {

        uart1 = &uart1; // uart1 别名指向名为 uart1 的设备节点

        uart2 = &uart2; // uart2 别名指向名为 uart2 的设备节点

        uart3 = "/serial@10000000"; // uart3 别名指向路径为 /serial@10000000 的设备节点,这里的/表示根目录

    };

 

    // 串口设备示例，地址不同，uart1 是标签

    uart1: serial@80000000 { 

        // 可在此处添加串口设备的配置信息

    };

 

    // 串口设备示例，地址不同，uart2 是标签

    uart2: serial@90000000 {

        // 可在此处添加串口设备的配置信息

    }; 

 

    // 串口设备示例，地址不同，uart3 是标签，通过路径方式定义

    serial@10000000 {

     // 可在此处添加串口设备的配置信息

    }; 

};
```

## 5\. 设备树属性

设备树中的属性通常包括：

- **compatible** ：这是一个非常重要的属性，用于将设备和驱动绑定起来。它的值是一个字符串列表，格式通常为“制造商,模型”，用于选择设备所要使用的驱动程序。例如， `compatible="davicom,dm9000"` ，需要与驱动代码中的`.compatible` 匹配。
- **model** ：该属性描述设备模块的具体信息，如设备的名称。例如， `model="wm8960-audio"` 。
- **status** ：这个属性与设备的状态有关，它描述了设备的当前状态，如“okay”表示设备正常，“disabled”表示设备被禁用等。

| **`status`** 属性值 | 描述 |
| --- | --- |
| **`okay`** | 表示设备是可操作的，即设备当前处于正常状态，可以被系统正常使用 |
| **`disabled`** | 表示设备当前是不可操作的，但在未来可能变得可操作。这通常用于表示某些设备（如热插拔设备）在插入后暂时不可用，但在驱动程序加载或系统配置更改后可能会变得可用 |
| **`fail`** | 表示设备不可操作，且设备检测到了一系列错误，且设备不太可能变得可操作。这通常表示设备硬件故障或严重错误 |

- **#address-cells** 和 **#size-cells** ：这两个属性用于描述子节点的reg属性值中地址表和地址长度的cell数量。reg属性用于描述设备的地址表，包括I/O地址。

**补充** ：reg属性值由一串数字组成，如上图中的reg = <0x900000 0x4000>， ret属性的书写格式为reg = < cells cells cells cells cells cells…>，长度根据实际情况而定， 这些数据分为地址数据(地址字段)，长度数据(大小字段)。

- ```bash
	soc {
	    //用于指定子节点reg属性“地址字段”所占的长度(单元格cells的个数)
	    #address-cells = <1>;
	    //用于指定子节点reg属性“大小字段”所占的长度(单元格cells的个数)
	    #size-cells = <1>;
	    compatible = "simple-bus";
	    interrupt-parent = <&gpc>;
	    ranges;
	    ocrams: sram@900000 {
	            compatible = "fsl,lpm-sram";
	            reg = <0x900000 0x4000>;
	    };
	};
	```
- **reg** ：此属性描述了设备的地址空间，包括起始地址和长度。例如，描述一个设备被映射到CPU地址空间的某个范围，例如： `reg = <[address1] [length1] [address2] [length2] ...>。`
1. `**[addressN]：**表示区域的起始物理地址。用多少个无符号整数来表示这个地址取决于父节点定义的#address-cells的值。例如，如果#address-cells为1，则使用一个32位整数表示地址；如果#address-cells为2，则使用两个32位整数表示一个64位地址。`
2. `**[lengthN]：**表示区域的长度（或大小）。用多少个无符号整数来表示这个长度同样取决于父节点定义的#size-cells的值。`

如果一个设备的寄存器空间位于地址0x03F02000上，并且占用0x1000字节的大小，假设其父节点定义了#address-cells = <1>和#size-cells = <1> ，reg属性的表达方式如下：reg = <0x03F02000 0x1000>

- **device\_type** ：此属性描述了设备的类型，有助于内核理解如何与设备交互。device\_type属性通常只用于CPU节点或Memory节点。例如，在描述一个CPU节点时，device\_type可能会被设置为 `"` CPU `"` ，而在描述内存节点时，它可能会被设置为 `"` Memory `"` 。
```bash
cpus {

            #address-cells = <2>;

            #size-cells = <0>;

 

            cpu0: cpu@0 {

                    device_type = "cpu";

                    compatible = "arm,cortex-a55";

                    reg = <0x0 0x0>;

                    enable-method = "psci";

                    clocks = <&scmi_clk 0>;

                    operating-points-v2 = <&cpu0_opp_table>;

                    cpu-idle-states = <&CPU_SLEEP>;

                    #cooling-cells = <2>;

                    dynamic-power-coefficient = <187>;

            };

    ...

}
```

注：属性中不同的类型属性，其赋值表达式也有所不同：

![](https://i-blog.csdnimg.cn/blog_migrate/1e3ec9064d774b02248f02b3e261e6fb.png)

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/136991550

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

 [![](https://csdnimg.cn/release/blogv2/dist/pc/img/toolbar/Group-dark.png) 点击体验  
DeepSeekR1满血版](https://ai.csdn.net/?utm_source=cknow_pc_blogdetail&spm=1001.2101.3001.10583) 隐藏侧栏

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

![](https://i-blog.csdnimg.cn/blog_migrate/23d13b2df438169e7f4ba55e1db87c15.png)