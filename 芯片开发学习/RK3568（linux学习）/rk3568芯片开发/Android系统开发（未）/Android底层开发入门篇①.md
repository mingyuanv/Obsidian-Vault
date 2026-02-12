---
title: Android11系统移植
aliases: 
tags: 
description: 
source:
---

# 备注(声明)：




# 一、Android系统与源码

## Android系统架构
### 1 、 Android系统架构图
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172415995.png|Open: Pasted image 20250728160542.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172153232.png](assets/Android底层开发入门篇①/file-20250810172415995.png)

### 2 、Java通过虚拟机用JMI的形式来调用C中的库
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172416026.png|Open: Pasted image 20250728161238.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172153257.png](assets/Android底层开发入门篇①/file-20250810172416026.png)


### 3 、安卓系统分层
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172416070.png|Open: Pasted image 20250728161334.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172153288.png](assets/Android底层开发入门篇①/file-20250810172416070.png)

- 1 一些真正敏感的厂商不愿意去开源的，像驱动的算法数据结构，它就放到了HAL层里面
### 4 、




## Android源码的获取途径
[2_Android源码的获取途径](onenote:#2_Android源码的获取途径&section-id={168DFA21-8560-4CC5-8059-6E043AA24EB4}&page-id={3F421B4C-5EFE-40B9-8AC0-D6C88092C630}&end&base-path=https://d.docs.live.net/52D4B76BB0FFCF51/Documents/\(RK3568\)Linux驱动开发/Android11系统移植.one)

- 1 直接用这种方案厂商做好的源码，快速的来开发自己的项目
### 1 、谷歌网站


### 2 、芯片原厂




# 二、谷歌AOSP源码


## 下载谷歌AOSP源码
[3_下载谷歌AOSP源码](onenote:#3_下载谷歌AOSP源码&section-id={168DFA21-8560-4CC5-8059-6E043AA24EB4}&page-id={68EB6F67-4EB2-4BFF-B683-17122CEF6EC8}&end&base-path=https://d.docs.live.net/52D4B76BB0FFCF51/Documents/\(RK3568\)Linux驱动开发/Android11系统移植.one)
### 1 、


### 2 、

## 编译谷歌AOSP源码
[4_编译谷歌AOSP源码](onenote:#4_编译谷歌AOSP源码&section-id={168DFA21-8560-4CC5-8059-6E043AA24EB4}&page-id={C0E41057-4B2E-4315-883E-610279B48546}&end&base-path=https://d.docs.live.net/52D4B76BB0FFCF51/Documents/\(RK3568\)Linux驱动开发/Android11系统移植.one)

### 1 、


### 2 、

## 通过模拟器启动AOSP系统
[5_通过模拟器启动AOSP系统](onenote:#5_通过模拟器启动AOSP系统&section-id={168DFA21-8560-4CC5-8059-6E043AA24EB4}&page-id={0FB24E99-4402-4215-928B-C735A308A1FD}&end&base-path=https://d.docs.live.net/52D4B76BB0FFCF51/Documents/\(RK3568\)Linux驱动开发/Android11系统移植.one)
### 1 、


### 2 、

# 三、初识安卓系统

## 将原厂Android11源码整体编译通过
### 1 、环境（迅为的ubuntu18.04）


### 2 、解压
- 1 tar -vxf rk_android11.0_sdk_211130.tar.gz

### 3 、整体编译（以后用脚本编译都先要设置环境变量）
- 1 设置jdk
```
source javaenv.sh
java -version
```
- 1 配置编译项为RK3568（环境变量）
```
source build/envsetup.sh
lunch rk3568_r-userdebug
```
- 1 整体编译
```
./build.sh -AUCKu
```

- 2 最终编译生成的镜像在rockdev/lmage-rk3568_r目录下

### 4 、编译命令讲解（build.sh脚本）
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172416189.png|Open: Pasted image 20250728200847.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172153350.png](assets/Android底层开发入门篇①/file-20250810172416189.png)

#### Rockchip Android 11 SDK `build.sh` 编译选项详解表 

| ​**​选项​**​   | ​**​功能描述​**​            | ​**​参数说明​**​                            |
| ------------ | ----------------------- | --------------------------------------- |
| ​**​`-U`​**​ | 编译U-Boot引导程序            | 无参数，生成`uboot.img`及相关镜像文件                |
| ​**​`-C`​**​ | ​**​使用Clang工具链编译内核​**​  | 需搭配`-K`使用，启用LLVM编译优化                    |
| ​**​`-K`​**​ | 编译Linux内核               | 生成`boot.img`及内核设备树                      |
| ​**​`-A`​**​ | 编译Android系统（AOSP）       | 生成`system.img`、`vendor.img`等Android分区镜像 |
| ​**​`-p`​**​ | ​**​生成完整固件包（含分区表）​**​   | 输出`rockdev/Image-*`目录，包含所有分区镜像          |
| ​**​`-o`​**​ | 生成OTA升级包                | 输出OTA增量包（如`update.zip`），用于系统远程更新        |
| ​**​`-u`​**​ | 生成整包镜像`update.img`      | 整合所有分区镜像为单一文件，用于烧录工具                    |
| ​**​`-v`​**​ | ​**​指定Android编译版本类型​**​ | 必选参数：`user`（生产环境）或`userdebug`（调试环境）     |
| ​**​`-d`​**​ | 指定内核设备树名称               | 需提供设备树文件名（如`rk3568-evb`），覆盖默认配置         |
| ​**​`-V`​**​ | 自定义固件版本号                | 参数格式为字符串（如`V1.2.0`），写入版本标识              |
| ​**​`-J`​**​ | ​**​设置并行编译任务数​**​       | 参数为整数（如`-J8`），加速编译过程                    |

### 5、





## 认识瑞芯微Android11原厂BSP
### 1 、系统架构对应源码中的文件夹
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172416351.png|Open: Pasted image 20250728200957.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172153460.png](assets/Android底层开发入门篇①/file-20250810172416351.png)

### 2 、Android 11源码目录分析
[Android 11源码目录结构](onenote:#6_认识瑞芯微Android11原厂BSP&section-id={168DFA21-8560-4CC5-8059-6E043AA24EB4}&page-id={46FF2B27-26C4-4CC7-B730-74D77D2A582F}&object-id={879061E1-CDD0-45A8-8E25-ABB0E082D918}&A&base-path=https://d.docs.live.net/52D4B76BB0FFCF51/Documents/\(RK3568\)Linux驱动开发/Android11系统移植.one)



### 3 、




## RK3568芯片的引导流程
### 1 、Armv8 架构典型引导流程
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172416395.png|Open: Pasted image 20250728202958.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172153526.png](assets/Android底层开发入门篇①/file-20250810172416395.png)

[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172416469.png|Open: Pasted image 20250728203728.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172153664.png](assets/Android底层开发入门篇①/file-20250810172416469.png)

### 2 、所有的不开源的东西都在这个文件夹放着
> topeet@ubuntu:~/rk3568/`rk_android11.0_sdk_211130$ ls rkbin
bin  img  README  RKBOOT  RKBOOT.ini  RKTRUST  scripts  tools



### 3 、开发板上使用的引导流程（流程一）
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172416595.png|Open: Pasted image 20250728204023.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172153700.png](assets/Android底层开发入门篇①/file-20250810172416595.png)

### 4 、




# 四、uboot
## u-boot编译与烧录
### 1 、 U-Boot 源码顶层目录的简要解释
[以下是瑞芯微 U-Boot 源码顶层目录的简要解释：](onenote:#8_原厂uboot源码顶层目录讲解&section-id={168DFA21-8560-4CC5-8059-6E043AA24EB4}&page-id={23989D59-6694-4F52-AB75-1711AA5A919A}&object-id={15B2988E-1278-4FFD-867D-1CD453ED2332}&D&base-path=https://d.docs.live.net/52D4B76BB0FFCF51/Documents/\(RK3568\)Linux驱动开发/Android11系统移植.one)

### 2 、单独编译u-boot
- 1 方法一：    ./build.sh -U
- 2 设置好环境变量后可看到
> topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130$ `get_build_var PRODUCT_UBOOT_CONFIG
> `rk3568


- 1 方法二：   ./make.sh itop_rk3568    在u-boot下

#### uboot编译产物
> `uboot.img
> `rk356x_spl_loader_v1.10.111.bin


### 3 、清除uboot编译中间产物（make clean）
> topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130/`u-boot$ make clean
  CLEAN   dts/../arch/arm/dts
  CLEAN   dts



### 4 、uboot烧录时有一个文件要改名（rk356x_spl_loader_v1.10.111.bin）
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172416677.png|Open: Pasted image 20250728202525.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172153807.png](assets/Android底层开发入门篇①/file-20250810172416677.png)

- 1 MiniLoaderAll.bin
### 5、uboot下编译生成spl_loader.bin（不开源）的命令
> topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130/`u-boot$ ./make.sh loader
/home/topeet/rk3568/rk_android11.0_sdk_211130/prebuilts/gcc/linux-x86/aarch64/gcc-linaro-6.3.1-2017.05-x86_64_aarch64-linux-gnu/bin/aarch64-linux-gnu-gcc
pack loader ok.(rk356x_spl_loader_v1.10.111.bin)(0.02)
pack loader okay! Input: /home/topeet/rk3568/rk_android11.0_sdk_211130/`rkbin/RKBOOT/RK3568MINIALL.ini
/home/topeet/rk3568/rk_android11.0_sdk_211130/u-boot
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172416825.png|Open: Pasted image 20250728204342.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172153873.png](assets/Android底层开发入门篇①/file-20250810172416825.png)



### 6、RK3568MINIALL.ini文件分析
> topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130$ `vim rkbin/RKBOOT/RK3568MINIALL.ini

[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172416900.png|Open: Pasted image 20250728204707.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172153973.png](assets/Android底层开发入门篇①/file-20250810172416900.png)

- 1 spl.bin的作用就是对内存的初始化    


### 7、make menuconfig后要
- 1 cp .config configs/itop_rk3568_defconfig

### 8、make.sh脚本命令解析

| ​**​功能类别​**​   | ​**​命令格式​**​                        | ​**​参数说明​**​                                                 | ​**​输出结果/作用​**​                                  | ​**​来源​**​ |
| -------------- | ----------------------------------- | ------------------------------------------------------------ | ------------------------------------------------ | ---------- |
| ​**​完整编译​**​   | `./make.sh <board_name>`            | `board_name`：开发板配置名（如`rk3588`、`evb-rk3399`）                  | 生成`uboot.img`、`trust.img`、`loader`等镜像文件          |            |
| ​**​增量编译​**​   | `./make.sh`                         | 无参数，基于现有`.config`编译                                          | 复用当前配置重新编译                                       |            |
|                | `./make.sh EXT_DTB=rk-kernel.dtb`   | `EXT_DTB`：指定外部设备树文件                                          | 编译时嵌入自定义设备树                                      |            |
| ​**​环境工具编译​**​ | `./make.sh env`                     | 无参数                                                          | 生成`envtools`工具，用于管理环境变量                          |            |
| ​**​镜像打包​**​   | `./make.sh uboot`                   | 无参数                                                          | 生成`uboot.img`（含U-Boot主程序及头部信息）                   |            |
|                | `./make.sh trust [<ini>]`           | `<ini>`：可选，指定Trust镜像配置文件（默认`RK3588TRUST.ini`）                | 生成`trust.img`（包含BL31/BL32安全固件）                   |            |
|                | `./make.sh loader [<ini>]`          | `<ini>`：可选，指定Loader配置文件（默认`RK3588MINIALL.ini`）               | 生成`rk3588_spl_loader_*.bin`（一级Loader，初始化DDR/USB） |            |
|                | `./make.sh --spl --tpl`             | `--spl`：嵌入SPL；`--tpl`：嵌入TPL                                  | 组合生成带SPL/TPL的Loader镜像                            |            |
| ​**​调试分析​**​   | `./make.sh elf-<opt>`               | `<opt>`：`-D`（默认反汇编）、`-S`（源码混合）、`-d`（详细符号）等                   | 输出ELF格式反汇编信息                                     |            |
|                | `./make.sh <addr> [<reloc_offset>]` | `<addr>`：静态地址；`<reloc_offset>`：重定位偏移（如`0x4FF00000-0x400000`） | 反汇编指定地址代码（支持重定位调整）                               |            |
|                | `./make.sh map` 或 `./make.sh sym`   | 无参数                                                          | 输出`u-boot.map`（内存映射）或`u-boot.sym`（符号表）           |            |
| ​**​配置与清理​**​  | `make <board>_defconfig`            | `<board>`：开发板名（如`mx6ull_14x14_ddr512_emmc_defconfig`）        | 生成`.config`配置文件                                  |            |
|                | `make distclean`                    | 无参数                                                          | 清除所有编译生成文件                                       |            |




## 使用ddrbin_tool工具修改ddr.bin的波特率（解决串口终端打印乱码）
### 1 、说明文档
> topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130$ `vi rkbin/tools/ddrbin_tool_user_guide.txt 


### 2 、ddr.bin文件的位置
> topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130/`rkbin/bin/rk35$ ls
FlashHead.bin                       rk3568_ddr_1332MHz_v1.10.bin
rk3566_ddr_1056MHz_ultra_v1.08.bin  `rk3568_ddr_1560MHz_v1.10.bin
rk3566_ddr_1056MHz_v1.10.bin        rk3568_ddr_528MHz_v1.10.bin
rk3566_ddr_528MHz_ultra_v1.08.bin   rk3568_ddr_630MHz_v1.10.bin
rk3566_ddr_528MHz_v1.10.bin         rk3568_ddr_780MHz_v1.10.bin
rk3566_ddr_630MHz_v1.10.bin         rk3568_ddr_920MHz_v1.10.bin





### 3 、ddrbin_tool工具使用说明
#### 获取 ddr.bin 的配置并生成到gen_param.txt
> topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130/`rkbin/tools$ cp /home/topeet/rk3568/rk_android11.0_sdk_211130/rkbin/bin/rk35/rk3568_ddr_1560MHz_v1.10.bin .
topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130/rkbin/tools$ `./ddrbin_tool -g gen_param.txt rk3568_ddr_1560MHz_v1.10.bin
version v1.07 20210603
version 2
generate info from bin file ok.


- 1 修改gen_param.txt文件
> uart id=2
> uart iomux=0
> uart baudrate=`115200`

#### 根据gen_param.txt文件生成ddr.bin 
> topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130/`rkbin/tools$ ./ddrbin_tool gen_param.txt rk3568_ddr_1560MHz_v1.10.bin
version v1.07 20210603
version 1748323154
version not support

- 1 保存修改
> topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130/`rkbin/bin/rk35$ mv rk3568_ddr_1560MHz_v1.10.bin rk3568_ddr_1560MHz_v1.10.bin.back  备份一下
> topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130/rkbin/bin/rk35$ `cp /home/topeet/rk3568/rk_android11.0_sdk_211130/rkbin/tools/rk3568_ddr_1560MHz_v1.10.bin .



### 4 、重新编译烧写spl_loader.bin（实验）
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172417052.png|Open: Pasted image 20250728212725.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172154036.png](assets/Android底层开发入门篇①/file-20250810172417052.png)
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172417152.png|Open: Pasted image 20250728212742.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172154153.png](assets/Android底层开发入门篇①/file-20250810172417152.png)


### 5、修改uboot.img中的波特率
> topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130/`u-boot$ make menuconfig
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172417280.png|Open: Pasted image 20250729135524.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172154216.png](assets/Android底层开发入门篇①/file-20250810172417280.png)



### 6、



## bootargs和cmdline参数讲解
### 1 、 bootargs（uboot给kernel传参）


### 2 、cmdline参数查看（同bootargs参数是一样,只是在内核阶段的叫法）

[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172417357.png|Open: Pasted image 20250728214902.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172154319.png](assets/Android底层开发入门篇①/file-20250810172417357.png)
- 1 cat /proc/cmdline
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172417523.png|Open: Pasted image 20250728214840.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172154547.png](assets/Android底层开发入门篇①/file-20250810172417523.png)



### 3 、cmdline参数说明
[“12_uboot的bootargs和cmdline参数讲解”页上的图片](onenote:#12_uboot的bootargs和cmdline参数讲解&section-id={168DFA21-8560-4CC5-8059-6E043AA24EB4}&page-id={33805BF3-BA4A-4C85-ABF0-699BEDEB7103}&object-id={1FA312F2-B3B4-459E-A6A0-F9BA1ECA876E}&5F&base-path=https://d.docs.live.net/52D4B76BB0FFCF51/Documents/\(RK3568\)Linux驱动开发/Android11系统移植.one)

### 4 、cmdline参数来源
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172417649.png|Open: Pasted image 20250728215845.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172154711.png](assets/Android底层开发入门篇①/file-20250810172417649.png)

- 1 kernel/arch/arm64/boot/dts/rockchip/rk3568-android.dtsi
> / {
	chosen: chosen {
		bootargs = "earlycon=uart8250,mmio32,0xfe660000 console=ttyFIQ0";
	};

- 1 device/rockchip/common/BoardConfig.mk
```bash
ifeq ($(BOARD_AVB_ENABLE), true)
BOARD_KERNEL_CMDLINE := androidboot.wificountrycode=CN androidboot.hardware=rk30board androidboot.console=ttyFIQ0 firmware_class.path=/vendor/etc/firmware init=/init rootwait ro init=/init
else # BOARD_AVB_ENABLE is false
BOARD_KERNEL_CMDLINE := console=ttyFIQ0 androidboot.baseband=N/A androidboot.wificountrycode=CN androidboot.veritymode=enforcing androidboot.hardware=rk30board androidboot.console=ttyFIQ0 androidboot.verifiedbootstate=orange firmware_class.path=/vendor/etc/firmware init=/init rootwait ro
endif # BOARD_AVB_ENABLE

BOARD_KERNEL_CMDLINE += loop.max_part=7
ROCKCHIP_RECOVERYIMAGE_CMDLINE_ARGS ?= console=ttyFIQ0 androidboot.baseband=N/A androidboot.selinux=permissive androidboot.wificountrycode=CN androidboot.veritymode=enforcing androidboot.hardware=rk30board androidboot.console=ttyFIQ0 firmware_class.path=/vendor/etc/firmware init=/init root=PARTUUID=af01642c-9b84-11e8-9b2a-234eb5e198a0

ifneq ($(BOARD_SELINUX_ENFORCING), true)
BOARD_KERNEL_CMDLINE += androidboot.selinux=permissive
endif
```

[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172417726.png|Open: Pasted image 20250728222718.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172155017.png](assets/Android底层开发入门篇①/file-20250810172417726.png)
- 1 vim u-boot/arch/arm/mach-rockchip/boot_rkimg.c
```c
		/* rknand doesn't need "androidboot.mode="; */
		if (env_exist("bootargs", "androidboot.mode=charger") ||
		    (type == IF_TYPE_RKNAND) ||
		    (type == IF_TYPE_SPINAND) ||
		    (type == IF_TYPE_SPINOR))
			snprintf(boot_options, sizeof(boot_options),
				 "storagemedia=%s", boot_media);
		else
			snprintf(boot_options, sizeof(boot_options),
				 "storagemedia=%s androidboot.mode=%s",
				 boot_media, boot_media);
```



### 5、



## uboot进行本地化
### 1 、寻找uboot用到的config文件
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172417857.png|Open: Pasted image 20250728230424.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172155173.png](assets/Android底层开发入门篇①/file-20250810172417857.png)

[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172417928.png|Open: Pasted image 20250728230730.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172155277.png](assets/Android底层开发入门篇①/file-20250810172417928.png)


### 2 、本地化config 文件
#### 制作自己的config文件
> topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130/`u-boot/configs$ cp rk3568_defconfig itop_rk3568_defconfig

#### 解析make.sh脚本，让他使用自己的config文件
- 1 u-boot/make.sh
```c
				#3. make defconfig
				else
					ARG_BOARD=$1
					if [ ! -f configs/${ARG_BOARD}_defconfig -a ! -f configs/${ARG_BOARD}.config ]; then
						echo -e "\n${SUPPORT_LIST}\n"
```
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172418057.png|Open: Pasted image 20250728232212.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172155488.png](assets/Android底层开发入门篇①/file-20250810172418057.png)

- 1 所以可以   ./make.sh itop_rk3568
> topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130/u-boot$ `./make.sh itop_rk3568
> ## make `itop_rk3568_defconfig` -j8
> #
> # configuration written to .config


#### 解析build.sh脚本，让他使用自己的config文件
> topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130$ `./build.sh -U
> will build u-boot
> -------------------KERNEL_DTS:rk3568-evb1-ddr4-v10
> 
> ============================================
> #### build completed successfully (1 seconds) ####
> 
> grep: .config: 没有那个文件或目录
> ## `make rk3568_defconfig -j8
>   HOSTCC  scripts/basic/fixdep
>   HOSTCC  scripts/kconfig/conf.o
- 2 可知他用的是这个config文件并杯我们本地化的config文件


- 1 build.sh
- 2 看这个build.s h这个脚本,在调用make.sh的时候,它是怎么调用的
> # build uboot
if [ "$BUILD_UBOOT" = true ] ; then
echo "start build uboot"
cd u-boot && make clean &&  make mrproper &&  make distclean && `./make.sh $UBOOT_DEFCONFIG && cd -

> SDK_VERSION=`get_build_var CURRENT_SDK_VERSION`
<span style="background:#b1ffff">UBOOT_DEFCONFIG</span>=`get_build_var PRODUCT_UBOOT_CONFIG`

> topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130/`device$ grep "PRODUCT_UBOOT_CONFIG" -rw
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172418140.png|Open: Pasted image 20250728234810.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172155835.png](assets/Android底层开发入门篇①/file-20250810172418140.png)
- 1 device/rockchip/rk356x/rk3568_r/BoardConfig.mk
> `PRODUCT_UBOOT_CONFIG := itop_rk3568`
- 2 把这个变量的值改成我们本地化的
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172418260.png|Open: Pasted image 20250728235038.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172155912.png](assets/Android底层开发入门篇①/file-20250810172418260.png)

#### 完善一下make.sh脚本的帮助信息
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172418329.png|Open: Pasted image 20250728235413.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172156031.png](assets/Android底层开发入门篇①/file-20250810172418329.png)
- 2 echo "	./make.sh itop_rk3568               --- build for itop_rk3568_defconfig"

### 3 、寻找uboot用到的设备树文件 
- 1 先编译uboot
> topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130/u-boot$ `./make.sh itop_rk3568
> ## make itop_rk3568_defconfig -j8

- 1 看哪个设备树文件会变编译成dtb文件从而得知哪个设备树文件被用到
> topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130/`u-boot/arch/arm/dts`$ `ls rk3568
rk3568.dtsi          rk3568-evb.dts       rk3568-spi-nand.dts
`rk3568-evb.dtb `     rk3568-pinctrl.dtsi  rk3568-u-boot.dtsi
- 2 可知用到的设备树文件是rk3568-evb.dts


### 4 、本地化设备树文件
#### 制作自己的设备树文件
> topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130/u-boot/arch/arm/dts$ `cp rk3568-evb.dts itop_rk3568-evb.dts

#### 添加设备树的编译规则
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172418452.png|Open: Pasted image 20250729134054.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172156116.png](assets/Android底层开发入门篇①/file-20250810172418452.png)

- 1 u-boot/configs/itop_rk3568_defconfig
- 2 CONFIG_DEFAULT_DEVICE_TREE="itop_rk3568-evb"



### 5、修改启动过程中的model名
- 1 u-boot/arch/arm/dts/itop_rk3568-evb.dts
> / {
	`model = "TOPEET RK3568 Evaluation Board";

[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172418532.png|Open: Pasted image 20250729134726.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172156275.png](assets/Android底层开发入门篇①/file-20250810172418532.png)

### 6、增加一个U boot引导内核之前的倒计时（方便进入U boot终端）
#### 方法一： u-boot/configs/itop_rk3568_defconfig
> # CONFIG_SPL_SYS_DCACHE_OFF is not set
`CONFIG_BOOTDELAY=3
CONFIG_SYS_CONSOLE_INFO_QUIET=y

#### 方法二：  uboot终端下用saveenv命令
- 1 配置 uboot支持saveenv命令
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172418641.png|Open: Pasted image 20250729135232.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172156474.png](assets/Android底层开发入门篇①/file-20250810172418641.png)

 - 1 saveenv命令的使用
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172418706.png|Open: Pasted image 20250729135740.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172156545.png](assets/Android底层开发入门篇①/file-20250810172418706.png)



### 7、想改其他的环境变量，也可以按照上面的这个方法来改


### 8、

## 瑞芯微uboot的特殊机制讲解
### 1 、uboot机制
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172419075.png|Open: Pasted image 20250729141902.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172156669.png](assets/Android底层开发入门篇①/file-20250810172419075.png)

### 2 、uboot下对内核设备树的支持
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172419329.png|Open: Pasted image 20250729142020.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172156808.png](assets/Android底层开发入门篇①/file-20250810172419329.png)

> config USING_KERNEL_DTB
>     `bool "使用来自Kernel/resource的dtb进行U-Boot引导"`  # 定义了一个名为USING_KERNEL_DTB的配置项，类型为布尔型（即选择是否启用）。
>     # 提供了在配置菜单中的描述，帮助用户理解此选项的作用。
>     depends on RKIMG_BOOTLOADER && OF_LIVE  # 此选项依赖于RKIMG_BOOTLOADER和OF_LIVE两个配置项同时被选中才能生效。
>     # 这意味着只有当这两个条件都满足时，当前配置项才会出现在配置菜单中并可供选择。
>     `default y  # 默认情况下，此选项是启用状态（'y'表示yes，启用）。
>     help  # 开始提供关于此配置项的帮助信息。
>         This enable support to read dtb from resource and use it for U-Boot,  # 启用从资源读取dtb并用于U-Boot的支持，
>         the uart and emmc will still using U-Boot dtb, but other devices like  # 其中，UART和EMMC仍然使用U-Boot自带的dtb，
>         regulator/pmic, display, usb will use dts node from kernel  # 而其他设备如调节器/电源管理芯片、显示器、USB等将使用来自内核的dts节点。

[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172419407.png|Open: Pasted image 20250729142030.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172156886.png](assets/Android底层开发入门篇①/file-20250810172419407.png)
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172419548.png|Open: Pasted image 20250729142100.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172157008.png](assets/Android底层开发入门篇①/file-20250810172419548.png)


### 3 、实现机制总结:
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172419642.png|Open: Pasted image 20250729142239.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172157114.png](assets/Android底层开发入门篇①/file-20250810172419642.png)

### 4 、






# 五、Android11内核

## 编译原厂Android11内核（要先配置好环境）
### 1 、方法一：`./build.sh -CKA `（要先配置好环境再编译）     

- 1 会将安卓一起编译啊
- 2 译后会在 rockdev/Image-rk3568_r 目录下生成 boot.img。boot.img 镜像里面包含了设备树镜像

### 2 、方法二： 编写makekernel.sh脚本
#### 编译内核的一个通用步骤
> 第一步我们先要安装<span style="background:#d3f8b6">交叉编译器</span>。
> 然后在内核源码中配置我们的<span style="background:#d3f8b6">config文件</span>。
><span style="background:#d3f8b6"> make</span>来编译它了。



#### 编写makekernel.sh脚本（不行，不知道为什么）
> topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130/kernel$ `touch makekernel.sh
> topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130/kernel$ `chmod 777 makekernel.sh 
- 1 kernel/makekernel.sh
```
#!/bin/sh

# 使用指定的架构和编译器进行make操作，设置ARCH为arm64，并使用预构建的clang编译器路径。

# 此处还指定了链接器ld.lld的路径，以及配置文件rockchip_defconfig和android-11.config。

make ARCH=arm64 \

CC=../prebuilts/clang/host/linux-x86/clang-r383902b/bin/clang \

LD=../prebuilts/clang/host/linux-x86/clang-r383902b/bin/ld.lld \

rockchip_defconfig android-11.config && \

# 再次执行make命令以生成boot.img镜像文件。这里同样设置了ARCH、CC、LD变量，

# 并通过BOOT_IMG变量指定了boot.img和目标img文件的位置。

make ARCH=arm64 \

CC=../prebuilts/clang/host/linux-x86/clang-r383902b/bin/clang \

LD=../prebuilts/clang/host/linux-x86/clang-r383902b/bin/ld.lld \

BOOT_IMG=../rockdev/Image-rk3568_r/boot.img rk3568-evb1-ddr4-v10.img
```

#### 注意事项:
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172419773.png|Open: Pasted image 20250729144240.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172157426.png](assets/Android底层开发入门篇①/file-20250810172419773.png)


#### 编译脚本的来源
- 1 build.sh
> #!/bin/bash
usage()
{
   echo "USAGE: [-U] [-CK] [-A] [-p] [-o] [-u] [-v VERSION_NAME]  "
    echo "No ARGS means use default build option                  "
    echo "WHERE: -U = build uboot                                 "
    echo "       -C = build kernel with Clang                     "
    echo "       -K = build kernel                                "
    echo "       -A = build android                               "
    echo "       -p = will build packaging in IMAGE      "
    echo "       -o = build OTA package                           "
    echo "       -u = build update.img                            "
    echo "       -v = build android with 'user' or 'userdebug'    "
    echo "       -d = huild kernel dts name    "
    echo "       -V = build version    "
    echo "       -J = build jobs    "
    exit 1
}
`set -x`   <span style="background:#affad1">加上这个代码，打印出荣誉信息，方便而获取它的完整的脚本命令</span>
- 1 ./build.sh -CKA       
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172419860.png|Open: Pasted image 20250729151946.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172157544.png](assets/Android底层开发入门篇①/file-20250810172419860.png)
```
+ make CC=../prebuilts/clang/host/linux-x86/clang-r383902b/bin/clang LD=../prebuilts/clang/host/linux-x86/clang-r383902b/bin/ld.lld ARCH=arm64 rk3568-evb1-ddr4-v10.img -j16
++ get_make_command CC=../prebuilts/clang/host/linux-x86/clang-r383902b/bin/clang LD=../prebuilts/clang/host/linux-x86/clang-r383902b/bin/ld.lld ARCH=arm64 rk3568-evb1-ddr4-v10.img -j16
++ '[' -f build/soong/soong_ui.bash ']'
++ echo command make
+ _wrap_build command make CC=../prebuilts/clang/host/linux-x86/clang-r383902b/bin/clang LD=../prebuilts/clang/host/linux-x86/clang-r383902b/bin/ld.lld ARCH=arm64 rk3568-evb1-ddr4-v10.img -j16
+ [[ '' == true ]]
```
- 1 有了这个信息之后，可以将这些信息提取到我们的脚本里面。
- 2 通过原厂给我们写的这个build.sh，通过它的打印，将编译内核阶段里面的关键信息提取出来


### 3 、




## 内核本地化
### 1 、寻找内核使用的config文件
- 1 build.sh
> # build kernel
if [ "$BUILD_KERNEL" = true ] ; then
echo "Start build kernel"
cd kernel && make clean && `make $ADDON_ARGS ARCH=$KERNEL_ARCH $KERNEL_DEFCONFIG` && make $ADDON_ARGS ARCH=$KERNEL_ARCH $KERNEL_ DTS.img -j$BUILD_JOBS && cd -

> KERNEL_ARCH=`get_build_var PRODUCT_KERNEL_ARCH`
<span style="background:#b1ffff">KERNEL_DEFCONFIG</span>=`get_build_var PRODUCT_KERNEL_CONFIG`

- 1 设置好环境变量后，查看KERNEL_DEFCONFIG变量的实际值
> topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130$ `get_build_var PRODUCT_KERNEL_CONFIG
> `rockchip_defconfig` `android-11.config`



- 1 通过名字查找实际位置
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172419976.png|Open: Pasted image 20250729152900.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172157723.png](assets/Android底层开发入门篇①/file-20250810172419976.png)
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172420043.png|Open: Pasted image 20250729152939.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172157813.png](assets/Android底层开发入门篇①/file-20250810172420043.png)


#### 俩个config 文件的位置是
- 1 kernel/arch/arm64/configs/rockchip_defconfig
- 1 kernel/kernel/configs/android-11.config


### 2 、本地化config文件
#### 制作自己的config文件
> topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130/`kernel/arch/arm64/configs`$ `cp rockchip_defconfig itop_rockchip_defconfig
> topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130/kernel$ cd kernel/configs/
> topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130/`kernel/kernel/configs`$ `cp android-11.config itop_android-11.config

#### 寻找编译配置文件并修改
- 1 用查找命令，由名字大概就知道他在这个路径之下
##### rockchip_defconfig
> topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130/`device`$ `grep "rockchip_defconfig" -rw
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172420168.png|Open: Pasted image 20250729165701.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172157953.png](assets/Android底层开发入门篇①/file-20250810172420168.png)
- 1 device/rockchip/rk356x/BoardConfig.mk
> PRODUCT_KERNEL_ARCH ?= arm64
> PRODUCT_KERNEL_DTS ?= rk3568-evb1-ddr4-v10
> `PRODUCT_KERNEL_CONFIG ?= itop_rockchip_defconfig
#####  android-11.config
> topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130/`device`$ `grep "android-11.config" -rw
rockchip/rk3328/rk3328_atv/BoardConfig.mk:PRODUCT_KERNEL_CONFIG ?= rockchip_defconfig android-11.config
rockchip/rk3328/rk3328_box_32/BoardConfig.mk:PRODUCT_KERNEL_CONFIG ?= rockchip_defconfig android-11.config
`rockchip/common/BoardConfig.mk:PRODUCT_KERNEL_CONFIG += android-11.config

- 1 device/rockchip/common/BoardConfig.mk
> PRODUCT_FSTAB_TEMPLATE ?= device/rockchip/common/scripts/fstab_tools/fstab.in
`PRODUCT_KERNEL_CONFIG += itop_android-11.config


### 3 、寻找内核使用的设备树文件
> topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130$ `./build.sh -CAK
will build kernel with Clang
will build android
will build kernel
-------------------`KERNEL_DTS:rk3568-evb1-ddr4-v10
- 2 在编译内核的时候,他给我们打印出来了,他用的是哪一个dts

### 4 、本地化dts文件
#### 制作自己的dts文件
> topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130/`kernel/arch/arm64/boot/dts/rockchip`$ ls rk3568-evb1-ddr4-v10
> rk3568-evb1-ddr4-v10.dtb
> rk3568-evb1-ddr4-v10.dts
> rk3568-evb1-ddr4-v10.dtsi
> rk3568-evb1-ddr4-v10-linux.dtb
> rk3568-evb1-ddr4-v10-linux.dts
> topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130/kernel/arch/arm64/boot/dts/rockchip$ `cp rk3568-evb1-ddr4-v10.dts itop_rk3568-evb1-ddr4-v10.dts
- 2 实际上这个dts它会包含这个dtsi,所以这里我们用dts


#### 寻找编译配置文件并修改
> topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130/`device`$ `grep "rk3568-evb1-ddr4-v10" -rw
> rockchip/rk356x/BoardConfig.mk:PRODUCT_KERNEL_DTS `?=` rk3568-evb1-ddr4-v10
> `rockchip/rk356x/rk3568_r/BoardConfig.mk`:PRODUCT_KERNEL_DTS `:=` rk3568-evb1-ddr4-v10
- 2 找文件在哪里配置，一般不加后缀直接用文件名
- 2 冒号等号(:=)就是直接给他赋值，而（?=）没有被赋值才会赋值

- 1 device/rockchip/rk356x/rk3568_r/BoardConfig.mk
> PRODUCT_UBOOT_CONFIG := itop_rk3568
`PRODUCT_KERNEL_DTS := itop_rk3568-evb1-ddr4-v10
BOARD_GSENSOR_MXC6655XA_SUPPORT := true
BOARD_CAMERA_SUPPORT_EXT := true
BOARD_HS_ETHERNET := true

#### 验证：本地化成功
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172420231.png|Open: Pasted image 20250729171654.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172158032.png](assets/Android底层开发入门篇①/file-20250810172420231.png)


### 5、


# 六、RK3568的电源管理

## RK809电源管理芯片讲解
### 1 、RK809介绍
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172420372.png|Open: Pasted image 20250729194357.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172158468.png](assets/Android底层开发入门篇①/file-20250810172420372.png)
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172420441.png|Open: Pasted image 20250729194430.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172158590.png](assets/Android底层开发入门篇①/file-20250810172420441.png)

[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172420586.png|Open: Pasted image 20250729194441.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172158660.png](assets/Android底层开发入门篇①/file-20250810172420586.png)


### 2 、pin脚定义:
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172420753.png|Open: Pasted image 20250729194501.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172214171.png](assets/Android底层开发入门篇①/file-20250810172420753.png)

### 3 、开发板上RK809位置:
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172420894.png|Open: Pasted image 20250729194530.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172150978.png](assets/Android底层开发入门篇①/file-20250810172420894.png)

### 4 、RK809功能:
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172420954.png|Open: Pasted image 20250729194730.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172151040.png](assets/Android底层开发入门篇①/file-20250810172420954.png)

### 5、config文件配置
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172421098.png|Open: Pasted image 20250729194836.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172151138.png](assets/Android底层开发入门篇①/file-20250810172421098.png)

### 6、RK809驱动源码位置（默认添加）
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172421185.png|Open: Pasted image 20250729194912.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172151205.png](assets/Android底层开发入门篇①/file-20250810172421185.png)

### 7、




## IO电压域讲解
### 1 、分析PMIC电路原理图
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172421333.png|Open: Pasted image 20250729195309.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172151309.png](assets/Android底层开发入门篇①/file-20250810172421333.png)

- 1 它使用i2c0，这个器件挂载到i2c0 这个总线下

### 2 、追踪设备树，分析rk809节点
- 1 itop_rk3568-evb1-ddr4-v10.dts --->rk3568-evb1-ddr4-v10.dtsi--->rk3568-evb.dtsi
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172421423.png|Open: Pasted image 20250729200627.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172151377.png](assets/Android底层开发入门篇①/file-20250810172421423.png)




### 3 、IO电源域的了解
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172421528.png|Open: Pasted image 20250729204547.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172151481.png](assets/Android底层开发入门篇①/file-20250810172421528.png)

### 4 、使用IO电压域的好处
- 1 使用I0电压域可以动态调整I0的电压，这样在实际项目中就可以避免电平转换的烦恼。
- 2 软件上通过控制这个pmic，就可以控制这个这个io电压域的一个高低电平，就达到了控制啊这个电瓶的目的

### 5、RK3568的十个IO电压域功能分析
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172421595.png|Open: Pasted image 20250729204826.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172151542.png](assets/Android底层开发入门篇①/file-20250810172421595.png)

### 6、




## 配置3568的IO电压域（分析电路原理图得知实际电压）
> [!PDF|red] [[芯片开发学习/RK3568（linux学习）/linux开发资料库/rk3568迅为开发pdf/6.Android系统开发/【北京迅为】itop-rk3568开发板官方android11移植教程.pdf#page=150&selection=18,0,22,7&color=red|【北京迅为】itop-rk3568开发板官方android11移植教程, p.150]]
> > 12.7 IO 电源域配置方法
> 
> 
### 1 、总结
- 1 kernel/arch/arm64/boot/dts/rockchip/rk3568-evb.dtsi
> &pmu_io_domains {
> 	status = "okay";
> 	pmuio2-supply = <&vcc3v3_pmu>;
> 	vccio1-supply = <&vccio_acodec>;//3.3V
> 	vccio3-supply = <&vccio_sd>;//1.8~3.3V
> 	vccio4-supply = <&vcc_1v8>;
> 	vccio5-supply = <&vcc_3v3>;
> 	vccio6-supply = <&vcc_1v8>;
> 	vccio7-supply = <&vcc_3v3>;
> };
> 

```
&pmu_io_domains {
	status = "okay";
	pmuio2-supply = <&vcc3v3_pmu>;
	vccio1-supply = <&vccio_acodec>;//3.3v
	vccio3-supply = <&vccio_sd>;//1.8~3.3v
	vccio4-supply = <&vcc_1v8>;
	vccio5-supply = <&vcc_3v3>;
	vccio6-supply = <&vcc_1v8>;
	vccio7-supply = <&vcc_3v3>;
};
```


### 2 、


### 3 、


### 4 、



# 七、了解安卓源码，添加自己的产品（device目录）

## 配置Android11的调试串口（默认为uart2）
### 1 、修改串口的波特率
- 1 kernel/arch/arm64/boot/dts/rockchip/rk3568-android.dtsi
- 2 调试串口所用的节点的描述
> 	`fiq-debugger `{
		compatible = "rockchip,fiq-debugger";
		`rockchip,serial-id = <2>;
		rockchip,wake-irq = <0>;
		/* If enable uart uses irq instead of fiq * /
		rockchip,irq-mode-enable = <1>;
		`rockchip,baudrate = <115200>;  /* Only 115200 and 1500000 * /
		interrupts = <GIC_SPI 252 IRQ_TYPE_LEVEL_LOW>;
		`pinctrl-names = "default";
		`pinctrl-0 = <&uart2m0_xfer>;
		status = "okay";
	};
- 2 默认为串口2。若设置为串口1，则要同时设置好pinctrl复用。


### 2 、pinctrl复用节点对应的设备树（rk3568-pinctrl.dtsi）
- 1 kernel/arch/arm64/boot/dts/rockchip/rk3568-pinctrl.dtsi

### 3 、宏定义文件（rockchip.h）
- 1 kernel/include/dt-bindings/pinctrl/rockchip.h
```
#define RK_GPIO0	0
#define RK_GPIO1	1
#define RK_GPIO2	2
#define RK_GPIO3	3

#define RK_PA0		0
#define RK_PA1		1
#define RK_PA2		2
#define RK_PA3		3
#define RK_PA4		4
#define RK_PA5		5
#define RK_PA6		6

#define RK_FUNC_GPIO	0
#define RK_FUNC_0	0
#define RK_FUNC_1	1
#define RK_FUNC_2	2
#define RK_FUNC_3	3
```



### 4 、分析寄存器手册了解GPIO 功能与外设复用
> [!PDF|note] [[芯片开发学习/RK3568（linux学习）/linux开发资料库/rk3568迅为开发pdf/00看视频教程用到的开发手册/Rockchip RK3568 TRM Part1 V1.1-20210301-核心板技术参考手册.pdf#page=180&selection=80,0,80,22&color=note|Rockchip RK3568 TRM Part1 V1.1-20210301-核心板技术参考手册, p.180]]
> > PMU_GRF_GPIO0D_IOMUX_L
> 
> 

- 1 **总结：寄存器功能速查表​**​

| ​**​位域​**​      | 功能            | 选项说明                      | 配置要求           |
| --------------- | ------------- | ------------------------- | -------------- |
| ​**​[31:16]​**​ | 写使能位          | `1`=允许写入对应低位              | 修改前必置 `1`      |
| ​**​[14:12]​**​ | GPIO0_D3 功能选择 | `0`: GPIO；其他保留            | 默认 `0`         |
| ​**​[6:4]​**​   | GPIO0_D1 功能选择 | `0`: GPIO；`1`: UART2_TXM0 | UART2 发送需置 `1` |
| ​**​[2:0]​**​   | GPIO0_D0 功能选择 | `0`: GPIO；`1`: UART2_RXM0 | UART2 接收需置 `1` |

- 2 通过合理配置此寄存器，可灵活切换 GPIO 功能与外设复用，适应不同硬件设计需求。实际开发中需结合设备树（DTS）与驱动代码协同验证



### 5、





## Android源码的device目录讲解（产品目录）
### 1 、device目录结构
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172421847.png|Open: Pasted image 20250729214226.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172151909.png](assets/Android底层开发入门篇①/file-20250810172421847.png)

### 2 、产品目录需要关注的文件

> topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130<span style="background:#b1ffff">/device/rockchip/rk356x</span>$ ls
> Android.mk                  overlay                  rk3568_r
> `AndroidProducts.mk `         package_performance.xml  rk356x.prop
> bluetooth                   public.libraries.txt     sepolicy_ebook
> `BoardConfig.mk`              rk3566_32bit             sepolicy_ebook_public
> `device.mk `                  rk3566_eink              sepolicy_ebook_system
> init.recovery.rk30board.rc  rk3566_einkw6            sepolicy_vendor
> init.rk356x.rc              rk3566_r                 wake_lock_filter.xml
> ota                         rk3566_rgo               wifi_bt.mk
> - 
>topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130/<span style="background:#b1ffff">device/rockchip/rk356x/rk3568_r</span>$ ls
`AndroidBoard.mk`  config.cfg         media_profiles_default.xml  `rk3568_r.mk`
Android.mk       config.cfg_ab      ota
`BoardConfig.mk`   config.cfg_ab_gki  recovery.fstab
bt_vendor.conf   dt-overlay.in      recovery.fstab_AB


### 3 、rk356x目录下文件作用
#### AndroidProducts.mk（产品列表）
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172421875.png|Open: Pasted image 20250729215908.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172151939.png](assets/Android底层开发入门篇①/file-20250810172421875.png)

#### BoardConfig.mk（底层信息）
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172421910.png|Open: Pasted image 20250729215917.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172151976.png](assets/Android底层开发入门篇①/file-20250810172421910.png)


### 4 、rk3568_r目录下文件作用
#### rk3568_r.mk（rk3568开发板信息）
[[RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172414773.png|Open: Pasted image 20250729220012.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172152078.png](RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172414773.png)


#### AndroidBoard.mk （包含其他mk文件）
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172414888.png|Open: Pasted image 20250729220032.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172152142.png](assets/Android底层开发入门篇①/file-20250810172414888.png)

#### BoardConfig.mk（定义和硬件相关的底层特性和变量）
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172414952.png|Open: Pasted image 20250729220023.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172152268.png](assets/Android底层开发入门篇①/file-20250810172414952.png)

### 5、后面我们在本地化的时候，我们肯定需要改这些配置文件


### 6、





## Android源码的device目录的变量讲解（.mk文件）
### 1 、通用变量
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172415075.png|Open: Pasted image 20250729224218.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172152332.png](assets/Android底层开发入门篇①/file-20250810172415075.png)

### 2 、自定义变量
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172415150.png|Open: Pasted image 20250729224256.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172152456.png](assets/Android底层开发入门篇①/file-20250810172415150.png)
- 1 用来在编译的时候选择一些外设的东西，到底要不要编译还是怎么选择的


### 3 、功能变量（重要）
#### PRODUCT_COPY_FILES
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172415268.png|Open: Pasted image 20250729224334.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172152522.png](assets/Android底层开发入门篇①/file-20250810172415268.png)
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172415334.png|Open: Pasted image 20250729224430.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172152623.png](assets/Android底层开发入门篇①/file-20250810172415334.png)

#### -include
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172415445.png|Open: Pasted image 20250729224504.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172152683.png](assets/Android底层开发入门篇①/file-20250810172415445.png)

#### include、inherit-product
- 1 都可以包含对应的mk文件

[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172415513.png|Open: Pasted image 20250729224709.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172152784.png](assets/Android底层开发入门篇①/file-20250810172415513.png)

[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172415627.png|Open: Pasted image 20250729224733.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172152848.png](assets/Android底层开发入门篇①/file-20250810172415627.png)
### 4 、举例
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172415698.png|Open: Pasted image 20250729225002.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172152943.png](assets/Android底层开发入门篇①/file-20250810172415698.png)



### 5、



## 对Android源码本地化添加自己的产品
### 1 、以其他产品为模板复制一个自己的产品
> topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130`/device/rockchip/rk356x`$ `cp rk3568_r/ topeet_rk3568_r -r
> topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130/`device/rockchip/rk356x/topeet_rk3568_r`$ `mv rk3568_r.mk topeet_rk3568_r.mk



### 2 、添加自己的产品在其中
- 1 device/rockchip/rk356x/AndroidProducts.mk
>         $(LOCAL_DIR)/rk3566_einkw6/rk3566_einkw6.mk
        `$(LOCAL_DIR)/topeet_rk3568_r/topeet_rk3568_r.mk

>     rk3566_einkw6-user\
    `topeet_rk3568_r-userdebug\
    `topeet_rk3568_r-user

- 1 device/rockchip/rk356x/topeet_rk3568_r/topeeet_rk3568_r.mk
> include device/rockchip/common/build/rockchip/DynamicPartitions.mk
`include device/rockchip/rk356x/topeet_rk3568_r/BoardConfig.mk

- 2 这里产品的名字也要改好加上使用lunch命令的时候才能找到。
> `PRODUCT_NAME := topeet_rk3568_r
- 2 产品文件夹的名字要和这里一样不然后面会出问题。
> `PRODUCT_DEVICE := topeet_rk3568_r





### 3 、



## 让Android11在开发板上跑起来
### 1 、整体编译
> topeet@ubuntu:~/rk3568/rk_android11.0_sdk_211130$ `./build.sh -CAKUu


### 2 、最终编译生成的镜像在rockdev/lmage-topeet_rk3568_r目录下



### 3 、
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172409338.png|Open: Pasted image 20250730195352.png]]
![RK3568（linux学习）/rk3568芯片开发/Android系统开发（未）/assets/Android底层开发入门篇①/file-20250810172153008.png](assets/Android底层开发入门篇①/file-20250810172409338.png)



### 4 、
