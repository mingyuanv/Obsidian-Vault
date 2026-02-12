---
title: 
aliases: 
tags: 
description:
---

# 随记：

<span style="background:#fdbfff">四个必要驱动对应硬件接口同pike板一样，编译方式也一样。</span>

## make strip命令的遍写
[[嵌入式知识学习（通用扩展）/linux基础知识/🔨linux常用命令记录#命令脚本遍写]]

# 一、音频驱动(audio.ko)

## 1.注意
 Audio 驱动加载时提供了参数 spk_gpio 用于配置功放的使能，<span style="background:#affad1">驱动默认配置的是 PB31</span>；
 如果不需要驱动控制该引脚，配置该参数为 spk_gpio=-1。
-# insmod audio.ko spk_gpio=-1 2) Audio 只支持使用 Amic 功能。
如果使用需要内核配置上 Amic 。

## 2.了解引脚配置
 
[[芯片开发学习/君正T23N芯片开发/【君正T23N_IPC】/BSP驱动开发/2、IPC上硬件引脚解析#一、音频（麦克风和扬声器）]]

## 3.驱动遍译
[[芯片开发学习/君正T23N芯片开发/【君正T32N-PIKE开发板】/5.T31驱动移植及加载、测试#四、音频驱动（audio.ko）]]

`KERDIR:=/home/ming/workspace/ISVP-T23-1.1.2-20240204/software/zh/Ingenic-SDK-T23-1.1.2-20240204-zh/opensource/kernel/`
`CROSS_COMPILE:=/home/ming/workspace/ISVP-T23-1.1.2-20240204/software/zh/Ingenic-SDK-T23-1.1.2-20240204-zh/resource/toolchain/gcc_540/mips-gcc540-glibc222-64bit-r3.3.0.smaller/bin/mips-linux-gnu-`


## 4.测试
[[#1.音频测试]]



# 二、Sinfo 探测驱动（sinfo.ko ）

[[芯片开发学习/君正T23N芯片开发/【君正T32N-PIKE开发板】/5.T31驱动移植及加载、测试#三、Sinfo 探测驱动（sinfo.ko ）]]
## 1.


## 2.
 


## 3.






# 三、sensor驱动（sensor_xxxx_t23.ko）

[[芯片开发学习/君正T23N芯片开发/【君正T32N-PIKE开发板】/5.T31驱动移植及加载、测试#二、sensor驱动（sensor_xxxx_t23.ko）]]
## 1.



## 2.
```
CROSS_COMPILE ?= /home/ming/workspace/ISVP-T23-1.1.2-20240204/software/zh/Ingenic-SDK-T23-1.1.2-20240204-zh/resource/toolchain/gcc_540/mips-gcc540-glibc222-64bit-r3.3.0.smaller/bin/mips-linux-gnu-
KDIR := /home/ming/workspace/ISVP-T23-1.1.2-20240204/software/zh/Ingenic-SDK-T23-1.1.2-20240204-zh/opensource/kernel/

ISP_DRIVER_DIR =/home/ming/workspace/ISVP-T23-1.1.2-20240204/software/zh/Ingenic-SDK-T23-1.1.2-20240204-zh/opensource/drivers/isp-t23/tx-isp-t23/
```




## 3.




# 四、音频驱动（audio.ko）

[[芯片开发学习/君正T23N芯片开发/【君正T32N-PIKE开发板】/5.T31驱动移植及加载、测试#四、音频驱动（audio.ko）]]
## 1.

## 2.


## 3.
 






# 五、


## 1.


## 2.



## 3.



# 六、sample测试

## 1.音频测试
> [!PDF|note] [[芯片开发学习/君正T23N芯片开发/sdk_资料库/君正T23N开发资料/BSP/T23 BSP开发参考V1.1.pdf#page=38&selection=167,0,174,2&color=note|T23 BSP开发参考V1.1, p.38]]
> > 6.10.3 Sample 使用
> 
> 

sample-Ai.c 
模拟 mic 录音
生成录音文件 ai_record.pcm

### 测试成功

```

[root@Ingenic-uc1_1:bin]# ls
sample-Ai       sample-chipid   wpa_cli         wpa_supplicant
[root@Ingenic-uc1_1:bin]# ./sample-Ai
[INFO] Test 1: Start audio record test.  //正在进行音频记录的测试。
[INFO]        : Can create the ai_record.pcm file.//成功创建了一个名为 `ai_record.pcm` 的文件
[INFO]        : Please input any key to continue.//输入任意键以继续程序的执行
rewwrfsf
Audio In GetVol    vol : 60  //音频输入设备（如麦克风）当前的音量级别为60。
fsffd
fgv
ete

[root@Ingenic-uc1_1:bin]# ls
ai_record.pcm   sample-Ai       sample-chipid   wpa_cli         wpa_supplicant
[root@Ingenic-uc1_1:bin]# 

```

## 2.


## 3.总测试

<span style="background:#b1ffff">用主程序</span>

/home/ming/workspace/appfs/init/<span style="background:#b1ffff">start.sh</span>
```
# Get Ingenic chip ID
CHIP_ID=/system/bin/sample-chipid

export AWS_DEFAULT_REGION=ap-east-1
export AWS_KVS_CACERT_PATH=/system/certs/cert.pem
export AWS_IOT_CORE_CREDENTIAL_ENDPOINT=cys.gznscy.com
export AWS_IOT_CORE_CERT=/system/certs/star_gznscy_com_cert.pem
export AWS_IOT_CORE_PRIVATE_KEY=/system/certs/star_gznscy_com.key
export AWS_IOT_CORE_ROLE_ALIAS=ingenic
export AWS_IOT_CORE_THING_NAME=$(${CHIP_ID})
export AWS_KVS_LOG_LEVEL=3
export DEBUG_LOG_SDP=false

if [ -d "/system/certs" ]; then
    echo "/system/certs exists."
else
    echo "/system/certs does not exist then create."
    mkdir /system/certs
fi

/system/bin/cyipc &
```










