---
title: 
aliases: 
tags:
  - 君正T23-ZN
description:
---

# 随记：




# 一、GPIO 查询设置工具

## 1.位置
为了方便用户测试 GPIO 状态，提供 GPIO 工具。目前工具支持查询 GPIO 的状态、设置 GPIO 功能。路径<span style="background:#b1ffff">“tools/debug/gpiotool”</span>。具体用法请看 READM


## 2.   ./gpiotool 
 
请根据工具链选择不同版本
gpiotool 可用来设置或查看gpio状态
./gpiotool <A|B|C> <0-31> [2mA|4mA|8mA|12mA] [up|down|no] [func0|func1|func2|func3|input|out0|out1]

参数说明：
  `<A|B|C> <0~31>  是两组参数必选`，用来指明GPIO组和gpio pin编号。

后三组配置参数是可选的：
  2mA 4mA 8mA 12mA  4档驱动能力配置参数。
  up down no        依次是是上拉、下拉、取消上下拉，用来配置上下拉状态。
  func0 func1 func2 func3  用来配置复用功能
  input out0 out1   配置输入输出模式

`参数正确会打印出配置后的gpio状态，如果没有配置参数，则直接打印当前gpio状态。
每组配置参数只能选用一个，配置参数重或多选以后一个为准，配置参数错误将被忽略。
所有参数大小写均可。


## 3、举例
例：
设置 GPIO PB20 驱动能力4mA 上拉 输出1
输入如下命令:
./gpiotool B 20 4ma up out1
-------- T31 gpio status --------
PxINT= 0x20000000
PxMSK= 0xde7f80c0
PxPAT1=0x5e6f8080
PxPAT0=0xa059ef00
INT  MSK  PAT1  PAT0
 0    1    0     1
gpio status is output=1     //Port输出状态
Pull up enable              //是否上拉
Pull down disable           //是否下拉
Drive strength is 4mA       //驱动能力




# 二、系统调试命令集
<span style="background:#d3f8b6">获取时钟频率、sensor帧率、ISP基本信息等</span>。
## impdbg
> [!PDF|yellow] [[芯片开发学习/君正T23-ZN芯片开发/sdk资料库/君正T23-ZN开发资料/Ingenic_Zeratul_T23_系统调试命令集.pdf#page=3&selection=20,1,26,14&color=yellow|Ingenic_Zeratul_T23_系统调试命令集, p.3]]
> >  impdbg --enc_info o 获取编码器参数，实时帧率信息





## touch
> [!PDF|yellow] [[芯片开发学习/君正T23-ZN芯片开发/sdk资料库/君正T23-ZN开发资料/Ingenic_Zeratul_T23_系统调试命令集.pdf#page=3&selection=88,1,104,2&color=yellow|Ingenic_Zeratul_T23_系统调试命令集, p.3]]
> >  touch /tmp/fsattr o 程序执行前 touch o 获取初始化的 framesource 参数




## cat
> [!PDF|yellow] [[芯片开发学习/君正T23-ZN芯片开发/sdk资料库/君正T23-ZN开发资料/Ingenic_Zeratul_T23_系统调试命令集.pdf#page=4&selection=37,1,46,4&color=yellow|Ingenic_Zeratul_T23_系统调试命令集, p.4]]
> > cat /proc/jz/isp/isp-m0 o 获取 ISP 基本信息
> 
> 




# 三、

## 1.



## 2.




## 3.




# 四、

## 1.

## 2.


## 3.
 






# 五、


## 1.


## 2.



## 3.



# 六、


## 1.

## 2.

## 3.













