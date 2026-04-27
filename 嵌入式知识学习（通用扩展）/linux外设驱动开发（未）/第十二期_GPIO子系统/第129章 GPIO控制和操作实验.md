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
url: https://blog.csdn.net/BeiJingXunWei/article/details/135566608?ops_request_misc=%257B%2522request%255Fid%2522%253A%25223086799c0de6831d6343f5d64547b291%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fblog.%2522%257D&request_id=3086799c0de6831d6343f5d64547b291&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~blog~first_rank_ecpm_v1~rank_v31_ecpm-1-135566608-null-null.nonecase&utm_term=%E7%AC%AC129%E7%AB%A0&spm=1018.2226.3001.4450
title: "RK3568驱动指南｜第十二篇 GPIO子系统-第129章 GPIO控制和操作实验_处理器的gpio口驱动-CSDN博客"
description: "文章浏览阅读6.3k次，点赞48次，收藏75次。GPIO软件编程方式有多种，可以写驱动程序调用GPIO函数操作GPIO，也可以直接通过操作寄存器的方式操作GPIO，还可以通过sysfs方式实现对GPIO的控制。会发现在/sys/class/gpio 目录下生成了一个名为 gpio15 的文件夹（gpioX，X 表示对应的编 号），该文件夹就是导出来的 GPIO 引脚对应的文件夹，用于管理、控制该 GPIO 引脚。出现上图报错的原因是该GPIO已经被其他GPIO使用，需要在内核中找到使用GPIO的驱动，并取消该驱动才可以正常使用GPIO。_处理器的gpio口驱动"
host: blog.csdn.net
```




# 一、使用命令通过sysfs文件系统控制GPIO

## 内核配置
### 1 、make menuconfig图形化配置(❤️)
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324150150019.png]]



### 2 、

## GPIO编号计算
### 3 、常用以下公式计算引脚：
- 1 有 5 组 GPIO bank：GPIO0~GPIO4，每组又以 A0~A7, B0~B7, C0~C7, D0~D7 作为编号区分
```c
GPIO pin脚计算公式：pin = bank * 32 + number     //bank为组号，number为小组编号
GPIO 小组编号计算公式：number = group * 8 + X  
```


### 4 、LED灯的GPIO0_PB7 pin脚计算：(❤️)
```c
bank = 0;       //GPIO0_B7=> 0, bank ∈ [0,4]
group = 1;      //GPIO0_B7 => 1, group ∈ {(A=0), (B=1), (C=2), (D=3)}
X = 7;         //GPIO4_D7 => 5, X ∈ [0,7]
number = group * 8 + X = 1 * 8 + 7 =15
pin = bank*32 + number= 0 * 32 + 15 = 15;
```


### 5、


### 6、




##  GPIO 引脚导出实验：

### 1 、/sys/class/gpio/export 
- 1 用于将GPIO控制从内核空间导出到用户空间
- 2 export 文件是只写文件，不能读取

### 2 、/sys/class/gpio/unexport 
- 1 用于取消GPIO控制从内核空间到用户空间的导出


### 3 、导出GPIO0_PB7引脚：(❤️)
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324150940638.png]]

- 2 gpio15 的文件夹 （gpioX，X 表示对应的编 号），该文件夹就是导出来的 GPIO 引脚对应的文件夹，用于管理、控制该 GPIO 引脚。


### 4 、如果对应的 GPIO 已经被导出或者在内核中被使用了，那便无法成功导出
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324151206188.png]]

> 出现上图报错的原因是该GPIO已经被其他GPIO使用，需要在内核中找到使用GPIO的驱动，并**取消该驱动才可以正常使用GPIO**。在使用GPIO15时，需要取消Linux 内核源码中LED灯的配置，如下所示：
> ![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324151256780.png]]
> 

### 5、








## gpio15文件夹下属性文件
### 1 、echo 15 > export
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324151401591.png]]

### 2 、direction：配置 GPIO 引脚为输入或输出模式。(❤️)
> 该文件**可读、可写**，读表示查看 GPIO 当前是输入还是输出模式，写表示将 GPIO 配置为输入或输出模式；读取或写入操作可取的值为 **out （输出模式）和 in （输入模式）**。

#### cat direction
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324151535465.png]]

#### echo out > direction
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324152329146.png]]




### 3 、active_low：用于控制极性的属性文件
- 2 可读可写，默认情况下为 0，使用cat命令进行文件内容的查看

![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324152541748.png]]

>` 当 active_low 等于 0 时`， **value 值若为1则引脚输出高**电平，value 值若为0则引脚输出低电平。`当 active_low 等于 1 时` ，**value 值若为0则引脚输出高**电平，value 值若为1则引脚输出低电平。



### 4 、edge：控制中断的触发模式
- 2 该文件可读可写。在配置 GPIO 引脚的中断触发模式之前，需将其设置为输入模式

- 1 四种触发模式的设置如下所示：

> 非中断引脚：echo "none" > edge
> 
> 上升沿触发：echo "rising" > edge
> 
> 下降沿触发：echo "falling" > edge
> 
> 边沿触发：  echo "both" > edge



### 5、value: 设置高低电平(❤️)
- 2 如果我们要把这个管脚设置成高电平，我们只需要给value设置成1即可，反之，则设置成0。使用命令 

![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324153027864.png]]




### 6、





# 二、使用C程序通过sysfs文件系统控制GPIO

## 控制GPIO输出实验
### 1 、网盘路径：
本小节代码在配套资料“iTOP-RK3568开发板【底板V1.7版本】\03_【iTOP-RK3568开发板】指南教程\02_Linux驱动配套资料\04_Linux驱动例程\82_gpioctrl01”目录下。

### 2 、通过GPIO输出应用程序控制GPIO口输出高低电平，以此来控制LED灯的亮灭。


### 3 、


### 4 、gpioctrl.c文件如下：(❤️)
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324153222216.png]]


```c
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
 
int fd;                   // 文件描述符
int ret;                  // 返回值
char gpio_path[100];      // GPIO路径
int len;                  // 字符串长度
 
// 导出GPIO引脚
int gpio_export(char *argv)
{
    fd = open("/sys/class/gpio/export", O_WRONLY); // 打开export文件
    if (fd < 0)
    {
        printf("open /sys/class/gpio/export error \n"); // 打开文件失败
        return -1;
    }
    len = strlen(argv); // 获取参数字符串的长度
    ret = write(fd, argv, len); // 将参数字符串写入文件，导出GPIO引脚
    if (ret < 0)
    {
        printf("write /sys/class/gpio/export error \n"); // 写入文件失败
        return -2;
    }
    close(fd); // 关闭文件
}
 
// 取消导出GPIO引脚
int gpio_unexport(char *argv)
{
    fd = open("/sys/class/gpio/unexport", O_WRONLY); // 打开unexport文件
    if (fd < 0)
    {
        printf("open /sys/class/gpio/unexport error \n"); // 打开文件失败
        return -1;
    }
    len = strlen(argv); // 获取参数字符串的长度
    ret = write(fd, argv, len); // 将参数字符串写入文件，取消导出GPIO引脚
    if (ret < 0)
    {
        printf("write /sys/class/gpio/unexport error \n"); // 写入文件失败
        return -2;
    }
    close(fd); // 关闭文件
}
 
// 控制GPIO引脚的属性
int gpio_ctrl(char *arg, char *val)
{
    char file_path[100]; // 文件路径
    sprintf(file_path, "%s/%s", gpio_path, arg); // 构建文件路径，格式为“gpio_path/arg”
    fd = open(file_path, O_WRONLY); // 打开文件
    if (fd < 0)
    {
        printf("open file_path error \n"); // 打开文件失败
        return -1;
    }
    len = strlen(val); // 获取参数字符串的长度
    ret = write(fd, val, len); // 将参数字符串写入文件，控制GPIO引脚的属性
    if (ret < 0)
    {
        printf("write file_path error\n"); // 写入文件失败
        return -2;
    }
    close(fd); // 关闭文件
}
 
int main(int argc, char *argv[]) // 主函数
{
    sprintf(gpio_path, "/sys/class/gpio/gpio%s", argv[1]); // 构建GPIO路径，格式为“/sys/class/gpio/gpio引脚号”
    if (access(gpio_path, F_OK)) // 检查GPIO路径是否存在
    {
        gpio_export(argv[1]); // 不存在则导出GPIO引脚
    }
    else
    {
        gpio_unexport(argv[1]); // 存在则取消导出GPIO引脚
    }
 
    gpio_ctrl("direction", "out"); // 配置GPIO为输出模式
    gpio_ctrl("value", argv[2]);   // 控制GPIO输出高低电平
 
    gpio_unexport(argv[1]); // 最后取消导出GPIO引脚
 
    return 0; // 返回0表示程序正常退出
}
```





### 5、对gpioctrl.c进行交叉编译
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324153312561.png]]

```c
export PATH=/usr/local/arm64/gcc-linaro-6.3.1-2017.05-x86_64_aarch64-linux-gnu/bin:$PATH

aarch64-linux-gnu-gcc gpioctrl.c -o gpioctrl
```




### 6、运行测试：
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324153421123.png]]

- 2 输入“./gpioctrl 15 1”命令LED灯点亮，输入“./gpioctrl 15 0”命令LED灯熄灭。



### 7、


### 8、




##  控制GPIO输入实验
### 1 、网盘路径：
本小节代码在配套资料“iTOP-RK3568开发板【底板V1.7版本】\03_【iTOP-RK3568开发板】指南教程\02_Linux驱动配套资料\04_Linux驱动例程\83_gpioctrl02”目录下。

### 2 、通过GPIO输入应用程序读取GPIO口的输入电平。


### 3 、实验硬件连接：
> 使用迅为iTOP-RK3568开发板，使用导线连接开发板背面的**引脚GPIO1_B2,另一端连接到电源或者GND**


### 4 、


### 5、gpioctrl.c文件内容如下：(❤️)
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324153645824.png]]

```c
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
 
int fd;              // 文件描述符
int ret;             // 返回值
char gpio_path[100]; // GPIO路径
int len;             // 字符串长度
char file_path[100]; // 文件路径
char buf[2];         // 用于读取 GPIO 值的缓冲区
 
// 导出 GPIO 引脚
int gpio_export(char *argv)
{
    fd = open("/sys/class/gpio/export", O_WRONLY); // 打开 export 文件
    if (fd < 0)
    {
        printf("open /sys/class/gpio/export error\n"); // 打开文件失败
        return -1;
    }
    len = strlen(argv);         // 获取参数字符串的长度
    ret = write(fd, argv, len); // 将参数字符串写入文件，导出 GPIO 引脚
    if (ret < 0)
    {
        printf("write /sys/class/gpio/export error\n"); // 写入文件失败
        return -2;
    }
    close(fd); // 关闭文件
}
 
// 取消导出 GPIO 引脚
int gpio_unexport(char *argv)
{
    fd = open("/sys/class/gpio/unexport", O_WRONLY); // 打开 unexport 文件
    if (fd < 0)
    {
        printf("open /sys/class/gpio/unexport error\n"); // 打开文件失败
        return -1;
    }
    len = strlen(argv);         // 获取参数字符串的长度
    ret = write(fd, argv, len); // 将参数字符串写入文件，取消导出 GPIO 引脚
    if (ret < 0)
    {
        printf("write /sys/class/gpio/unexport error\n"); // 写入文件失败
        return -2;
    }
    close(fd); // 关闭文件
}
 
// 控制 GPIO 引脚的属性
int gpio_ctrl(char *arg, char *val)
{
    sprintf(file_path, "%s/%s", gpio_path, arg); // 构建文件路径，格式为 "gpio_path/arg"
    fd = open(file_path, O_WRONLY);              // 打开文件
    if (fd < 0)
    {
        printf("open file_path error\n"); // 打开文件失败
        return -1;
    }
    len = strlen(val);         // 获取参数字符串的长度
    ret = write(fd, val, len); // 将参数字符串写入文件，控制 GPIO 引脚的属性
    if (ret < 0)
    {
        printf("write file_path error\n"); // 写入文件失败
        return -2;
    }
    close(fd); // 关闭文件
}
 
// 读取 GPIO 引脚的值
int gpio_read_value(char *arg)
{
    sprintf(file_path, "%s/%s", gpio_path, arg); // 构建文件路径，格式为 "gpio_path/arg"
    fd = open(file_path, O_RDONLY);              // 打开文件
    if (fd < 0)
    {
        printf("open file_path error\n"); // 打开文件失败
        return -1;
    }
    ret = read(fd, buf, 1); // 读取文件内容到缓冲区
    if (!strcmp(buf, "1"))
    {
        printf("The value is high\n"); // GPIO 引脚值为高电平
        return 1;
    }
    else if (!strcmp(buf,"0"))
    {
        printf("The value is low\n"); // GPIO 引脚值为低电平
        return 0;
    }
    
    close(fd); // 关闭文件
    return -1;
    
}
 
int main(int argc, char *argv[]) // 主函数
{
    int value;
    sprintf(gpio_path, "/sys/class/gpio/gpio%s", argv[1]); // 构建 GPIO 路径，格式为 "/sys/class/gpio/gpio引脚号"
    if (access(gpio_path, F_OK))                           // 检查 GPIO 路径是否存在
    {
        gpio_export(argv[1]); // 不存在则导出 GPIO 引脚
    }
    else
    {
        gpio_unexport(argv[1]); // 存在则取消导出 GPIO 引脚
    }
 
    gpio_ctrl("direction", "in");       // 配置 GPIO 为输入模式
    
    value = gpio_read_value("value");   // 读取 GPIO 引脚的值
    printf("The value is %d\n", value); // 打印读取的 GPIO 引脚的值
    gpio_unexport(argv[1]);             // 最后取消导出 GPIO 引脚
 
    return 0; // 返回 0 表示程序正常退出
}
```




### 6、测试：3.3V接到了GPIO1_PB2 pin脚上
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324153740711.png]]






### 7、




# 三、使用C程序通过sysfs文件系统使用GPIO中断

## 使用C程序通过sysfs文件系统使用GPIO中断
### 1 、网盘路径：
本小节代码在配套资料“iTOP-RK3568开发板【底板V1.7版本】\03_【iTOP-RK3568开发板】指南教程\02_Linux驱动配套资料\04_Linux驱动例程\84_gpioctrl03”目录下。

### 2 、通过GPIO的输入中断程序，将中断触发方式设置为边沿触发，每当触发中断会打印value的值。
- 1 

### 3 、



### 4 、 gpioctrl.c文件内容如下(❤️)
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324154701176.png]]

> 函数 gpio_interrupt("**value**") 实现了阻塞等待：
> **打开文件**：以只写模式
> 利**用 `poll()` 机制高效地阻塞等待内核发出的中断通知**，从而实现低功耗、实时性的按键或信号检测。
> 


```c
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <poll.h>
 
int fd;              // 文件描述符
int ret;             // 返回值
char gpio_path[100]; // GPIO路径
int len;             // 字符串长度
char file_path[100]; // 文件路径
char buf[2];         // 缓冲区
 
struct pollfd fds[1]; // poll结构体数组
 
// 导出GPIO引脚
int gpio_export(char *argv)
{
    fd = open("/sys/class/gpio/export", O_WRONLY); // 打开export文件
    if (fd < 0)
    {
        printf("open /sys/class/gpio/export error \n"); // 打开文件失败
        return -1;
    }
    len = strlen(argv);         // 获取字符串长度
    ret = write(fd, argv, len); // 写入引脚号到export文件
    if (ret < 0)
    {
        printf("write /sys/class/gpio/export error \n"); // 写入失败
        return -2;
    }
    close(fd); // 关闭文件
}
 
// 取消导出GPIO引脚
int gpio_unexport(char *argv)
{
    fd = open("/sys/class/gpio/unexport", O_WRONLY); // 打开unexport文件
    if (fd < 0)
    {
        printf("open /sys/class/gpio/unexport error \n"); // 打开文件失败
        return -1;
    }
    len = strlen(argv);        // 获取字符串长度
    ret = write(fd, argv, len); // 写入引脚号到unexport文件
    if (ret < 0)
    {
        printf("write /sys/class/gpio/unexport error \n"); // 写入失败
        return -2;
    }
    close(fd); // 关闭文件
}
 
// 控制GPIO引脚的属性
int gpio_ctrl(char *arg, char *val)
{
    sprintf(file_path, "%s/%s", gpio_path, arg); // 构建属性文件的路径
    fd = open(file_path, O_WRONLY);              // 打开属性文件
    if (fd < 0)
    {
        printf("open file_path error \n"); // 打开文件失败
        return -1;
    }
    len = strlen(val);         // 获取字符串长度
    ret = write(fd, val, len); // 写入属性值到属性文件
    if (ret < 0)
    {
        printf("write file_path error\n"); // 写入失败
        return -2;
    }
    close(fd); // 关闭文件
}
 
// 监听GPIO引脚的中断事件
int gpio_interrupt(char *arg)
{
    sprintf(file_path, "%s/%s", gpio_path, arg); // 构建文件路径
    fd = open(file_path, O_WRONLY);              // 打开文件
    if (fd < 0)
    {
        printf("open file_path error \n"); // 打开文件失败
        return -1;
    }
    memset((void *)fds, 0, sizeof(fds)); // 清空poll结构体数组
    fds[0].fd = fd;                      // 设置poll结构体的文件描述符
    fds[0].events = POLLPRI;             // 设置poll结构体的事件类型为POLLPRI，表示有紧急数据可读
 
    read(fd, buf, 2); // 读取文件内容，清除中断事件
 
    ret = poll(fds, 1, -1); // 调用poll函数等待中断事件发生，阻塞直到事件发生
    if (ret <= 0)
    {
        printf("poll error \n"); // 调用poll失败或超时
        return -1;
    }
    if (fds[0].revents & POLLPRI)
    {
        lseek(fd, 0, SEEK_SET); // 重新定位文件指针到文件开头
        read(fd, buf, 2);       // 读取文件内容，获取中断事件的值
        buf[1] = '\0';
        printf("value is %s\n", buf); // 输出中断事件的值
    }
}
 
// 读取GPIO引脚的值
int gpio_read_value(char *arg)
{
    sprintf(file_path, "%s/%s", gpio_path, arg); // 构建文件路径
   fd = open(file_path, O_WRONLY); // 打开文件，以只写模式打开是一个错误，应该使用只读模式
    if (fd < 0)
    {
        printf("open file_path error\n"); // 打开文件失败
        return -1;
    }
    ret = read(fd, buf, 1); // 读取文件内容，获取引脚的值
    if (!strcmp(buf, "1"))
    {
        printf("The value is high\n"); // 引脚值为高电平
    }
    else if (!strcmp(buf, "0"))
    {
        printf("The value is low\n"); // 引脚值为低电平
    }
    return -1; // 这里应该返回读取到的引脚值（0或1），而不是返回固定的-1
    close(fd); // 关闭文件（这行代码无法执行到，应该放在read之前）
}
 
int main(int argc, char *argv[]) // 主函数
{
    int value;
    sprintf(gpio_path, "/sys/class/gpio/gpio%s", argv[1]); // 构建GPIO路径
    if (access(gpio_path, F_OK))                            // 检查GPIO路径是否存在
    {
        gpio_export(argv[1]); // 不存在则导出GPIO引脚
    }
    else
    {
        gpio_unexport(argv[1]); // 存在则取消导出GPIO引脚
    }
 
    gpio_ctrl("direction", "in"); // 设置GPIO引脚为输入模式
    gpio_ctrl("edge", "both");    // 设置GPIO引脚的中断触发方式为上升沿和下降沿
    gpio_interrupt("value");      // 监听GPIO引脚的中断事件
 
    gpio_unexport(argv[1]); // 最后取消导出GPIO引脚
 
    return 0; // 返回0表示程序正常退出
}
```


### 5、GPIO底座的3.3V接到GPIO1_PB2 pin脚，进行中断的测试：
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324155449006.png]]

### 6、






# 四、使用IO命令操作寄存器控制GPIO

## IO命令
### 1 、用于读取和写入指定 I/O 端口的值


### 2 、用于与硬件设备进行低级别的交互和调试，在内核阶段读写寄存器


### 3 、语法如下：(❤️)
```c
io [选项] [地址] [操作] [数据]
```

> `-b`：**以字节为单位**进行 I/O 操作（默认为字）。
> 
> -w：以字为单位进行 I/O 操作。
> 
> -l：以双字为单位进行 I/O 操作。
> 
地址是要读取或写入的 I/O 端口的十六进制值。
操作可以是以下之一：
>` r`：读取 I/O 端口的值。
> 
>` w`：写入数据到 I/O 端口。
> 
**数据是要写入 I/O 端口的十六进制值**。





### 4 、
##  `io` 命令的示例：


### 5、读取 I/O 端口的值：
```c
io -b -r 0x80
```

这将以字节为单位读取 I/O 端口 0x80的值，并将其显示在终端上。




### 6、向 I/O 端口写入数据：
```c
io -b -w 0x80 0xAB
```

这将向 I/O 端口 0x80 写入十六进制值 0xAB。



### 7、以字为单位进行读取：
```c
io -w -r 0x1000
```

### 8、 以双字为单位进行写入：
```c
io -l -w 0x2000 0xDEADBEEF
```





##  LED引脚寄存器查找
### 1 、LED灯的GPIO为GPIO0_B7


### 2 、需要对GPIO的复用寄存器，方向寄存器，数据寄存器进行配置(❤️)


### 3 、RK3568的参考手册part1查找这几个寄存器的地址



### 4 、
## 查找复用寄存器

### 5、part1的第三章，GPIOB的复用寄存器的偏移地址如下(❤️)
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324162254023.png]]

### 6、搜索gpio0b7(❤️)
> **gpio0b7_sel在PMU_GRF_GPIO0B_IOMUX_H上**，所以偏移地址为0x000C。gpio0b7可以**通过控制[14:12]位来选择复用为哪个功能**，我们要控制led灯，所以功能要复用为**gpio**。


![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324162352258.png]]


### 7、复用寄存器的基地址如下(❤️)
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324162438278.png]]

### 8、复用寄存器地址=基地址+偏移地址=0xFDC2000C 
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324162511593.png]]


#### 寄存器值为00000001，[14:12]位为000 ：
- 1 默认设置的为gpio功能


![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324162542074.png]]





## 查找方向寄存器
### 1 、参考手册part1的第16章节，数据寄存器的偏移地址如下(❤️)
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324162756446.png]]

> GPIO有**四组GPIO**，分别是GPIOA，GPIOB，GPIOC，GPIOD。每组又以 A0~A7, B0~B7, C0~C7, D0~D7 作为编号区分。**所以GPIO0B7在GPIO_SWPORT_DDR_L上**所以，方向寄存器的偏移地址为0x0008。




### 2 、GPIO_SWPORT_DDR_L寄存器的具体描述
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324162954972.png]]

> 如上图（图 129-25）所示，`[31:16]位`属性是WO，也就是只可写入。这[31:16]位是写标志位，是**低16位的写使能**。如果低16位中某一位要设置输入输入输出，则对应高位写标志也应该设置为1。 `[15：0] 是数据方向控制寄存器低位`，如果要**设置某个GPIO为输出，则对应位置1**，如果要设置某个GPIO为输入，则对应位置0。那么GPIO0 B7 ，我们要设置**第15位设置为输出**，那么对应的[31:16]位写使能也要置1。







### 3 、part1的1.1小节Address Mapping。(❤️)
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324164052901.png]]


### 4 、地址计算与默认值确定(❤️)

> 如上图（图129-27）所示，**GPIO0的基地址为0xFDD60000**。方向寄存器的地址=基地址+偏移地址=0xFDD60000+0x0008=0xFDD60008
> 
> 然后使用IO命令查看该寄存器的值，如下（图129-28）所示：
> ![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324164117187.png]]
> 如下图（图 129-29）所示，**第15位默认为1，设置GPIO0_B7为输出。**
> ![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324164125988.png]]
> 






## 查找数据寄存器

### 5、part1的1.1小节Address Mapping。(❤️)
> ![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324164226984.png]]
> ![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324164231345.png]]
> 
> 如上图（图18-13）所示，**GPIO0的基地址为0xFDD60000。**
> 



### 6、数据寄存器的偏移地址如下(❤️)
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324164311369.png]]



### 7、数据寄存器的描述
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324164333154.png]]



### 8、地址计算与寄存器值确定(❤️)

> 数据寄存器的地址为**基地址+偏移地址=0xFDD60000**。使用IO命令查看地址的值，如下（图129-33）所示：
> ![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324164554579.png]]
> 分析上图的方法和在分析方向寄存器的方法同理，由上图可知，如果**要控制第15位为高电平（置1），需要设置31位为1**，那么点亮灯，需要**向数据寄存器写入0x8000c040**，如下图（图129-35）所示：
> ![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324164606571.png]]
> 如果**要灭灯，需要设置第15位为0 ，第31位为1，那么向数据寄存器中写入0x80004040**，如下图（图 129-36）所示：
> ![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324164622847.png]]
> 







## 总结
### 1 、复用关系寄存器，要操作的地址为基地址+偏移地址=0xFDC2000C
> 复用关系寄存器的基地址为0xFDC20000 ，偏移地址为000C 

### 2 、给方向寄存器写入0x80000044设置为输出。
> GPIO的基地址为0xFDD60000，偏移地址为0x0008，所以方向寄存器要操作的地址为基地址+偏移地址=**0xFDD60008**，

### 3 、默认的数据寄存器的值：0x8000c040亮灯，0x80004040灭灯

> GPIO的基地址为0xFDD60000，偏移地址为0x0000，所以数据寄存器要操作的地址为基地址+偏移地址=**0xFDD60000**

### 4 、


##  IO命令点灯测试
### 5、将方向寄存器设置为输出。
- 2 默认GPIO0_B7是GPIO模式

```c
io -w -4 0xFDD60008 0x80008044
```



### 6、查看数据寄存器的值
```c
io -r -4 0xFDD60000
```

![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324172149367.png]]


### 7、给数据寄存器写入0x8000c040输出高电平，灯亮
```c
io -w -4 0xFDD60000 0x8000c040

```

### 8、给数据寄存器写入0x80008040输出高电平，灯灭。

```c
io -w -4 0xFDD60000 0x80004040
```




# 五、通过mem设备控制GPIO

## mem设备映射物理内存
### 1 、用/dev/mem设备来操作物理内存


### 2 、以实现对GPIO寄存器的访问(❤️)
> 通过**打开/dev/mem设备文件，并将其映射到用户空间的内存中**，我们可以直接读写物理内存地址，从而实现对GPIO寄存器的控制。这种方法相对于IO命令更加灵活，**可以使用**更高级的**编程语言（如C/C++）来编写控制逻辑**。



### 3 、


##  Linux系统用户态访问内核态方式
### 4 、通过read/write/ioctl
> 使用这种方式，用户态程序可以通过**读写文件描述符或使用ioctl系统调用**与内核进行通信。例如，可以通过读写特定文件描述符来控制设备或获取设备状态。


### 5、通过sysfs虚拟文件系统
> sysfs是一种以文件的形式表示设备和内核信息的虚拟文件系统。通过在**sysfs中的特定路径下读写文件**，用户态程序可以与内核进行交互，例如控制GPIO引脚或获取系统信息。

### 6、通过内存映射(❤️)
> 内存映射是**将用户空间的一段内存区域映射到内核空间的一种机制**。通过内存映射，**用户态程序可以直接修改内存区域的内容，从而与内核进行通信**。这种方式可以实现高效的数据传输和共享。

### 7、通过Netlink
> Netlink是Linux内核提供的一种通信机制，用于用户态程序与内核之间的双向通信。**通过创建Netlink套接字，用户态程序可以与内核进行交互，发送请求、接收事件通知等**。这种方式适用于需要与内核进行复杂交互的场景，例如配置系统参数或发送命令。

### 8、


## /dev/mem设备
### 1 、虚拟设备，通常与mmap结合使用，可以将设备的物理内存映射到用户态


### 2 、实现用户空间对内核态的直接访问(❤️)
> 直接访问内核空间是一项潜在危险的操作，因**此只有root用户**才能访问/dev/mem设备。此外有些系统**可能需要单独启动**/dev/mem设备的功能。

> **IO命令实际上就是基于/dev/mem设备实现的**。如果Linux内核源码没有配置支持/dev/mem，IO命令是不能使用的。


### 3 、配置启动/dev/mem设备方法如下(❤️)
- 1 在Linux源码内核中配置以下选项。
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324173348033.png]]



### 4 、


### 5、




##  /dev/mem设备的使用方法。
### 1 、需要具有root权限，并且谨慎操作


### 2 、open函数打开"/dev/mem"文件描述符
> 并**指定访问权限和阻塞方式**，访问权限可以是只读（O_RDONLY）、只写（O_WRONLY）或读写（O_RDWR）阻塞方式或非阻塞（O_NDELAY）。

```c
int fd = 0;

fd = open("/dev/mem", O_RDWR | O_NDELAY); /* 读写权限，非阻塞 */
```



### 3 、用mmap函数将需要访问的物理地址与"/dev/mem"文件描述符建立映射(❤️)
- 1 mmap函数将返回一个指向映射内存区域的指针。
```c
char *mmap_addr = NULL;

mmap_addr = (char *)mmap(NULL, MMAP_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, MMAP_ADDR);
```

> 在这里，使用mmap函数**将物理内存地址映射到mmap_addr指针所指向的内存区域**。
> 
> `MMAP_SIZE`表示映射的大小，`PROT_READ | PROT_WRITE`表示访问权限为读写，`MAP_SHARED`表示**共享映射**，fd是之前打开的/dev/mem文件描述符，`MMAP_ADDR`是**要映射的物理地址**。



### 4 、对映射的地址进行访问
- 2 即对寄存器进行读写操作。
```c
int a = 0;

*(int *)mmap_addr = 0xff; // 写地址

a = *(int *)mmap_addr; // 读地址
```

> 在这里，使用指针操作对mmap_addr指向的地址进行读写操作。`*(int *)mmap_addr`表示将mmap_addr解释为int类型的指针，对于写操作，**将0xff写入该地址**；对于读操作，将地址的值读取到变量a中。



### 5、



## mmap函数

### 6、函数原型：
```c
void* mmap(void* start,size_t length,int prot,int flags,int fd,off_t offset);
```

### 7、函数参数：(❤️)
> `start`: 指定文件应被映射到进程空间的起始地址 ，一般被指**定为一个空指针，选择起始地址的任务留给内核来完成**。映射成功之后，函数返回值为最后文件映射到进程空间的地址，进程可直接操作起始地址为该值的有效地址。
> 
> length: 是映射到调用进程地址空间的字节数。
> 
> prot: 参数指定共享内存的访问权限。可取如下几个值的或。PROT_READ(映射区域可读)、PROT_EXEC(映射区域可执行)、PROT_WRITE(映射区域可写)、PROT_NONE(映射区域不可访问)。
> 
> flags: 由以下几个常值指定，MAP_SHARED，MAP_PRIVATE，MAP_FIXED，其中MAP_SHARED，MAP_PRIVATE必选其一，MAP_FIXED不推荐使用。
> 
> fd: 有效的文件描述符。一般是由open()函数返回。
> 
> `offset:` **文件映射的偏移量，offset的大小必须是页的整数倍**，如果设备为0代表从文件最前方开始映射。
> 
> 函数返回值：**成功执行时，mmap()返回被映射区的指针**，失败时，mmap()返回-1.


### 8、




##  LED灯实验
### 1 、网盘路径：
本小节代码在配套资料“iTOP-RK3568开发板【底板V1.7版本】\03_【iTOP-RK3568开发板】指南教程\02_Linux驱动配套资料\04_Linux驱动例程\85_gpioctrl04”目录下。



### 2 、通过编写mem设备控制GPIO（LED灯）的应用程序实现LED灯闪烁的效果。




### 3 、LED9



### 4 、应用程序编写如下：(❤️)
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324174754230.png]]

- 1 修改数据寄存器和方向寄存器

```c
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <sys/mman.h>
 
#define GPIO_REG_BASE 0xFDD60000
#define GPIO_SWPORT_DDR_L_OFFSET 0x0008
#define GPIO_SWPORT_DR_L_OFFSET 0x0000
#define SIZE_MAP 0x1000
 
// 打开LED灯
void LED_ON(unsigned char *base)
{
    // 设置LED灯的方向为输出
    *(volatile unsigned int *)(base + GPIO_SWPORT_DDR_L_OFFSET) = 0x80008044;
    // 将LED灯打开
    *(volatile unsigned int *)(base + GPIO_SWPORT_DR_L_OFFSET) = 0x80008040;
}
 
// 关闭LED灯
void LED_OFF(unsigned char *base)
{
    // 设置LED灯的方向为输出
    *(volatile unsigned int *)(base + GPIO_SWPORT_DDR_L_OFFSET) = 0x80008044;
    // 将LED灯关闭
    *(volatile unsigned int *)(base + GPIO_SWPORT_DR_L_OFFSET) = 0x80000040;
}
 
int main(int argc, char *argv[])
{
    int fd;
    unsigned char *map_base;
 
    // 打开/dev/mem设备
    fd = open("/dev/mem", O_RDWR);
    if (fd < 0)
    {
        printf("open /dev/mem error \n");
        return -1;
    }
 
    // 将物理地址映射到用户空间
    map_base = (unsigned char *)mmap(NULL, SIZE_MAP, PROT_READ | PROT_WRITE, MAP_SHARED, fd, GPIO_REG_BASE);
    if (map_base == MAP_FAILED)
    {
        printf("map_base error \n");
        return -2;
    }
 
    while (1)
    {
        // 打开LED灯
        LED_ON(map_base);
        // 等待1秒
        usleep(1000000);
        // 关闭LED灯
        LED_OFF(map_base);
        // 等待1秒
        usleep(1000000);
    }
 
    // 解除映射
    munmap(map_base, SIZE_MAP);
 
    // 关闭文件描述符
    close(fd);
 
    return 0; // 返回0表示程序正常退出
}
```



### 5、程序运行之后，开发板上的用户灯LED实现了闪烁的效果。
![[嵌入式知识学习（通用扩展）/linux外设驱动开发（未）/第十二期_GPIO子系统/assets/第129章 GPIO控制和操作实验/file-20260324175018523.png]]

```c
chmod 777 gpioctrl

./gpioctrl 15
```



### 6、


### 7、

