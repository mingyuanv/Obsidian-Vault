# 报错：加载成功，但是没有生成设备节点，没有识别到mmc1进行配置

![Pasted image 20250421204851.png](../../../../通用文件夹/媒体库/图片库/Pasted%20image%2020250421204851.png)


# 一、wifi驱动源码配置

## 图形化界面配置(.config文件)

```
#
# Automatically generated file; DO NOT EDIT.
# Atbm Wifi Driver Configuration
#
CONFIG_ATBM_MENUCONFIG=y
CONFIG_ATBM_WIRELESS=y
# CONFIG_ATBM_WEXT is not set

#
# select which atbm Wi-Fi chip type
#
# CONFIG_ATBM603x is not set
CONFIG_ATBM6012B_y=y
# CONFIG_ATBM6132 is not set
# CONFIG_ATBM_USB_BUS is not set
CONFIG_ATBM_SDIO_BUS=y
# CONFIG_ATBM_SPI_BUS is not set
# CONFIG_ATBM_USE_FIRMWARE_BIN is not set
CONFIG_ATBM_USE_FIRMWARE_H=y
CONFIG_ATBM_SUPPORT_BAN_24G=y
# CONFIG_ATBM_SUPPORT_BAN_5G_PRETEND_24 is not set

#
# Driver Extern Function Select
#

#
# Select WIFI bandwidth configuration 
#
CONFIG_ATBM_WITHBAND_2_4G_ONLY_HT20=y
CONFIG_ATBM_SUPPORT_BRIDGE=y
CONFIG_ATBM_FUNC_NOTXCONFIRM=y
# CONFIG_ATBM_FUNC_EARLYSUSPEND is not set
CONFIG_ATBM_FUNC_MONITOR=y
# CONFIG_ATBM_FUNC_MONITOR_HDR_PRISM is not set
# CONFIG_ATBM_FUNC_SKB_DEBUG is not set
# CONFIG_ATBM_FUNC_MEM_DEBUG is not set
# CONFIG_ATBM_FUNC_P2P_ENABLE is not set
# CONFIG_ATBM_FUNC_SW_ENC is not set
CONFIG_ATBM_FUNC_DEV_CTRL_API=y
CONFIG_ATBM_FUNC_MODULE_FS=y
CONFIG_ATBM_FUNC_PRIVE_IE=y
CONFIG_ATBM_FUNC_SAE_AUTHEN=y

#
# Driver debug features
#
CONFIG_ATBM_APOLLO_DEBUGFS=y
# CONFIG_ATBM_APOLLO_DEBUG_ON_BOOT is not set
CONFIG_ATBM_APOLLO_BH_DEBUG=y
# CONFIG_ATBM_APOLLO_WSM_DEBUG is not set
# CONFIG_ATBM_APOLLO_WSM_DUMPS is not set
# CONFIG_ATBM_APOLLO_WSM_DUMPS_SHORT is not set
# CONFIG_ATBM_APOLLO_TXRX_DEBUG is not set
# CONFIG_ATBM_APOLLO_TX_POLICY_DEBUG is not set
# CONFIG_ATBM_APOLLO_STA_DEBUG is not set
# CONFIG_ATBM_APOLLO_DUMP_ON_ERROR is not set
# CONFIG_CERT_FIRMWARE is not set
# CONFIG_BLUEDROID is not set
CONFIG_ATBM_SDIO_MMCx="mmc1"
# CONFIG_ATBM_APOLLO_USE_GPIO_IRQ is not set
CONFIG_ATBM_APOLLO_SUPPORT_SGI=y
CONFIG_ATBM_WIFIIF1_NAME="wlan%d"
CONFIG_NEED_P2P0_INTERFACE=y
CONFIG_ATBM_WIFIIF2_NAME="p2p%d"
CONFIG_ATBM_MODULE_PM_STAYAWK="pm_stayawake"
CONFIG_ATBM_MODULE_DRIVER_NAME="atbm_wlan"
CONFIG_ATBM_PLATFORM_DEVICE_NAME="atbm_dev_wifi"
CONFIG_ATBM_SDIO_VID=0x007a
CONFIG_ATBM_SDIO_PID=0x6011
CONFIG_ATBM_MODULE_NAME="atbm6x3x_wifi_usb"
CONFIG_MAC80211_ATBM_RC_DEFAULT=""
CONFIG_ATBM_BLE=y
CONFIG_ATBM_BLE_WIFI_PLATFORM=y
# CONFIG_ATBM_ONLY_BLE_WIFI_PLATFORM is not set



```
![君正T23N芯片开发/【君正T23N\_IPC】/wifi开发记录/assets/wifi配置记录(报错)/file-20250810171421107.png](assets/wifi配置记录(报错)/file-20250810171421107.png)

![君正T23N芯片开发/【君正T23N\_IPC】/wifi开发记录/assets/wifi配置记录(报错)/file-20250810171421342.png](assets/wifi配置记录(报错)/file-20250810171421342.png)







## Makefile
<span style="background:#b1ffff">配置编译环境</span>
/home/ming/workspace/ATBM_LINUX_WIFI4_BLE_SVN3407_AsmLite19040_ARESM18826_Meru19963_V1.1_20241023/Makefile

```
platform +=PLATFORM_INGENICT31
#ATBM_BUILD_IN_KERNEL?=

// 重点，直接导出环境，防止出错。
KERDIR:=/home/ming/workspace/ISVP-T23-1.1.2-20240204/software/zh/Ingenic-SDK-T23-1.1.2-20240204-zh/opensource/kernel/
CROSS_COMPILE:=/home/ming/workspace/ISVP-T23-1.1.2-20240204/software/zh/Ingenic-SDK-T23-1.1.2-20240204-zh/resource/toolchain/gcc_540/mips-gcc540-glibc222-64bit-r3.3.0.smaller/bin/mips-linux-gnu-
ATBM_WIFI__EXT_CCFLAGS = -DATBM_WIFI_PLATFORM=24


#Android
#Linux
sys ?= Linux
#arch:arm or arm64 or mips(NVT98517)
arch ?= mips

#cross compile path
ifeq ($(platform),PLATFORM_INGENICT31)
KERDIR:=/home/ming/workspace/ISVP-T23-1.1.2-20240204/software/zh/Ingenic-SDK-T23-1.1.2-20240204-zh/opensource/kernel/
CROSS_COMPILE:=mips-linux-gnu-
ATBM_WIFI__EXT_CCFLAGS = -DATBM_WIFI_PLATFORM=24
arch = mips
endif

```


## hal_apollo/atbm_platform.c

/home/ming/workspace/ATBM_LINUX_WIFI4_BLE_SVN3407_AsmLite19040_ARESM18826_Meru19963_V1.1_20241023/hal_apollo/atbm_platform.c

```
#endif  //CONFIG_ATBM_APOLLO_USE_GPIO_IRQ
#endif
#endif
struct atbm_platform_data platform_data = {
#ifdef SDIO_BUS
	.mmc_id       = CONFIG_ATBM_SDIO_MMC_ID,
	.clk_ctrl     = NULL,
	.power_ctrl   = atbm_power_ctrl,
	.insert_ctrl  = atbm_insert_crtl,
#if(ATBM_WIFI_PLATFORM == PLATFORM_XUNWEI)
	.irq_gpio	= EXYNOS4_GPX2(4),
	.power_gpio	= EXYNOS4_GPC1(1),
#endif
#if(ATBM_WIFI_PLATFORM == PLATFORM_AMLOGIC_S805)
	.irq_gpio	= INT_GPIO_4,
	.power_gpio	= 0,
#endif
#if(ATBM_WIFI_PLATFORM == PLATFORM_AMLOGIC_905)
	.irq_gpio	= 100,
	.power_gpio	= 0,
#endif
#if(ATBM_WIFI_PLATFORM == PLATFORM_FRIENDLY)
	.power_gpio	= EXYNOS4_GPK3(2),
#endif
#if(ATBM_WIFI_PLATFORM == PLATFORM_GK7202V330)
	.power_gpio = GK7202V330_WIFI_RESET_GPIO,
#endif
#if(ATBM_WIFI_PLATFORM == PLATFORM_INGENICT31)
    .power_gpio = 0*32+6,
#endif
	.reset_gpio = 0,
#else
	.clk_ctrl     = NULL,
	.power_ctrl   = NULL,
	.insert_ctrl  = NULL,
#endif
};

```


```
#if (ATBM_WIFI_PLATFORM == PLATFORM_INGENICT31)
#define PLATFORMINF     "ingenic_t23"
#endif

#if (ATBM_WIFI_PLATFORM == PLATFORM_INGENICT31)
extern int jzmmc_manual_detect(int index,int on);
static int WL_REG_EN = 32+26;
#endif

```

```
static int atbm_platform_power_ctrl(const struct atbm_platform_data *pdata,bool enabled)
{
	int ret = 0; 
#if (ATBM_WIFI_PLATFORM == PLATFORM_INGENICT31)

	printk("this is atbm_platform_power_ctrl");

	if(enabled)
	{
		atbm_printk_platform("[%s]:reset altobeam platform wifi...\n",__func__);
		gpio_request(WL_REG_EN,"sdio_wifi_power_on");

		atbm_printk_platform("[%s]:reset altobeam platform wifi to 0\n",__func__);
		gpio_direction_output(WL_REG_EN,0);
		msleep(300);

		atbm_printk_platform("[%s]:reset altobeam platform wifi to 1\n",__func__);
		gpio_direction_output(WL_REG_EN,1);
		msleep(100);

	}
#endif

```


```
static int atbm_platform_insert_crtl(const struct atbm_platform_data *pdata,bool enabled)
{
	int ret = 0;
#ifdef SDIO_BUS

	#if (ATBM_WIFI_PLATFORM == PLATFORM_INGENICT31)
		mdelay(100);
		jzmmc_manual_detect(1,enabled);
		atbm_printk_platform("=========platform insert ctrl = %d====================\n",enabled);

		printk("this is atbm_platform_insert_crtl");

	#endif


```

## hal_apollo/apollo_plat.h
/home/ming/workspace/ATBM_LINUX_WIFI4_BLE_SVN3407_AsmLite19040_ARESM18826_Meru19963_V1.1_20241023/hal_apollo/apollo_plat.h
```
#ifndef  ATBM_WIFI_PLATFORM
#define ATBM_WIFI_PLATFORM			PLATFORM_INGENICT31
#endif

```

## hal_apollo/Makefile

/home/ming/workspace/ATBM_LINUX_WIFI4_BLE_SVN3407_AsmLite19040_ARESM18826_Meru19963_V1.1_20241023/hal_apollo/Makefile
```
ifeq ($(SDIO_BUS),y)
ccflags-y += -DATBM_WIFI_PLATFORM=24
ccflags-y += -DATBM_SDIO_PATCH
ccflags-y += -DCONFIG_TX_NO_CONFIRM
endif

```




# 内核配置

## 图形化界面配置
直接用唐工提供的config文件

## board.h
/home/ming/workspace/ISVP-T23-1.1.2-20240204/software/zh/Ingenic-SDK-T23-1.1.2-20240204-zh/opensource/kernel/arch/mips/xburst/soc-t23/chip-t23/isvp/Pike/board.h
```
#ifndef __BOARD_H__
#define __BOARD_H__
#include <gpio.h>
#include <soc/gpio.h>
#include <linux/jz_dwc.h>

/* ****************************GPIO I2C 配置开始******************************** */
#ifdef CONFIG_SOFT_I2C0_GPIO_V12_JZ
#define GPIO_I2C0_SDA GPIO_PA(12)  // I2C0 数据线，使用 PA12 引脚
#define GPIO_I2C0_SCK GPIO_PA(13)  // I2C0 时钟线，使用 PA13 引脚
#endif

#ifdef CONFIG_SOFT_I2C1_GPIO_V12_JZ
#define GPIO_I2C1_SDA GPIO_PB(25)  // I2C1 数据线，使用 PB25 引脚
#define GPIO_I2C1_SCK GPIO_PB(26)  // I2C1 时钟线，使用 PB26 引脚
#endif

#ifdef CONFIG_SOFT_I2C2_GPIO_V12_JZ
#define GPIO_I2C2_SDA GPIO_PC(27)  // I2C2 数据线，使用 PC27 引脚
#define GPIO_I2C2_SCK GPIO_PC(28)  // I2C2 时钟线，使用 PC28 引脚
#endif
/* ****************************GPIO I2C 配置结束********************************** */

/* ****************************GPIO SPI 配置开始******************************** */
#ifndef CONFIG_SPI_GPIO
#define GPIO_SPI_SCK  GPIO_PC(13)  // SPI 时钟线，使用 PC13 引脚
#define GPIO_SPI_MOSI GPIO_PC(11)  // SPI 主出从入，使用 PC11 引脚
#define GPIO_SPI_MISO GPIO_PC(12)  // SPI 主入从出，使用 PC12 引脚
#endif
/* ****************************GPIO SPI 配置结束********************************** */

/* ****************************GPIO MMC/SD 配置开始******************************** */
#define GPIO_MMC_RST_N			-1        // MMC 复位引脚，未使用
#define GPIO_MMC_RST_N_LEVEL	LOW_ENABLE // 复位有效电平为低
#define GPIO_MMC_CD_N			GPIO_PB(27) // 卡检测引脚，使用 PB27
#define GPIO_MMC_CD_N_LEVEL		LOW_ENABLE // 卡插入检测有效电平为低
#define GPIO_MMC_PWR			-1        // 电源控制引脚，未使用
#define GPIO_MMC_PWR_LEVEL		HIGH_ENABLE // 电源使能电平为高
#define GPIO_MMC_WP_N			-1        // 写保护引脚，未使用
#define GPIO_MMC_WP_N_LEVEL		LOW_ENABLE // 写保护有效电平为低
/* ****************************GPIO MMC 配置结束******************************** */

/* ****************************GPIO USB 配置开始******************************** */
#define GPIO_USB_ID			-1        // USB ID 引脚，未使用
#define GPIO_USB_ID_LEVEL		LOW_ENABLE // ID 检测有效电平为低
#define GPIO_USB_DETE			-1        // USB 检测引脚，未使用
#define GPIO_USB_DETE_LEVEL		LOW_ENABLE // 检测有效电平为低
#define GPIO_USB_DRVVBUS		-1        // USB VBUS 驱动引脚，未使用
#define GPIO_USB_DRVVBUS_LEVEL		HIGH_ENABLE // VBUS 驱动有效电平为高
/* ****************************GPIO USB 配置结束********************************** */

/* ****************************GPIO DVP 摄像头配置开始***************************** */
#define DVP_CAMERA_RST				GPIO_PA(18)  // 摄像头复位引脚，使用 PA18
#define DVP_CAMERA_PWDN_N           GPIO_PA(19)  // 摄像头电源控制引脚，使用 PA19
/* ****************************GPIO 摄像头配置结束******************************* */

/* ****************************GPIO 音频配置开始****************************** */
#define GPIO_HP_MUTE		-1	// 耳机静音控制引脚，未使用
#define GPIO_HP_MUTE_LEVEL	-1	// 静音有效电平，未使用

#define GPIO_SPEAKER_EN	   GPIO_PB(31)	      // 扬声器使能引脚，使用 PB31
#define GPIO_SPEAKER_EN_LEVEL	1           // 扬声器使能有效电平为高

#define GPIO_HANDSET_EN		-1	// 听筒使能引脚，未使用
#define GPIO_HANDSET_EN_LEVEL   -1          // 听筒使能有效电平，未使用

#define	GPIO_HP_DETECT	-1		// 耳机检测引脚，未使用
#define GPIO_HP_INSERT_LEVEL    1           // 耳机插入检测有效电平为高
#define GPIO_MIC_SELECT		-1	// 麦克风选择引脚，未使用
#define GPIO_BUILDIN_MIC_LEVEL	-1	// 内置麦克风选择电平，未使用
#define GPIO_MIC_DETECT		-1    // 麦克风检测引脚，未使用
#define GPIO_MIC_INSERT_LEVEL   -1         // 麦克风插入检测电平，未使用
#define GPIO_MIC_DETECT_EN	-1  // 麦克风检测使能引脚，未使用
#define GPIO_MIC_DETECT_EN_LEVEL -1        // 麦克风检测使能电平，未使用

#define HP_SENSE_ACTIVE_LEVEL	1          // 耳机检测有效电平为高
#define HOOK_ACTIVE_LEVEL		-1        // 挂机检测有效电平，未使用
/* ****************************GPIO 音频配置结束******************************** */

/* ****************************GPIO GMAC 配置开始******************************* */
#ifdef CONFIG_JZ_MAC // 如果启用了JZ系列SoC的MAC支持
#ifndef CONFIG_MDIO_GPIO // 如果未启用MDIO GPIO模式

#ifdef CONFIG_JZGPIO_PHY_RESET // 如果启用了通过GPIO控制PHY复位的功能
#define GMAC_PHY_PORT_GPIO GPIO_PE(11)     // 定义用于PHY复位的GPIO引脚为PE11
// PHY复位时，首先需要将该引脚设置为输出低电平（即拉低）
#define GMAC_PHY_PORT_START_FUNC GPIO_OUTPUT0 
// 在完成复位后，将该引脚设置为输出高电平（即释放）
#define GMAC_PHY_PORT_END_FUNC GPIO_OUTPUT1   
// 定义PHY复位期间的延迟时间，确保复位信号稳定，单位为微秒
#define GMAC_PHY_DELAYTIME 100000            
#endif

#else /* CONFIG_MDIO_GPIO */ // 若启用了MDIO GPIO模式，则定义MDIO相关的GPIO引脚
// MDIO（管理数据输入输出）是用于以太网设备管理和诊断的接口
#define MDIO_MDIO_MDC_GPIO GPIO_PF(13)      // 定义MDIO时钟信号使用的GPIO引脚PF13
#define MDIO_MDIO_GPIO GPIO_PF(14)          // 定义MDIO数据信号使用的GPIO引脚PF14
#endif

#endif /* CONFIG_JZ4775_MAC */ // 结束对特定型号MAC的支持判断
/* ****************************GPIO GMAC 配置结束********************************* */

/* ****************************GPIO WiFi 配置开始******************************* */

// 修改后的配置
#define WL_WAKE_HOST    GPIO_PB(28)     // WiFi 唤醒主机引脚，使用 PB28（原为 PC8）
#define WL_REG_EN    GPIO_PB(26)        // WiFi 使能引脚，使用 PB26（原为 PC9）
#define WL_MMC_NUM    1                 // SDIO 使用 MMC1 接口

#define WLAN_PWR_EN    GPIO_PA(6)       // WiFi 电源使能引脚，使用 PA6（原为未使用）
#define BCM_PWR_EN    (-1)              // BCM 电源使能引脚，未使用
#define PWM_32K_OUTPUT 1                // 使能 32K 时钟输出

#define GPIO_MMC_WIFI_POWER_LEVEL        1  // WiFi 电源控制有效电平为高
#define GPIO_MMC_WIFI_RST_N_LEVEL       0   // WiFi 复位有效电平为低
#define GPIO_WLAN_WP -1                     // WiFi 写保护引脚，未使用
#define GPIO_WLAN_CD -1                     // WiFi 卡检测引脚，未使用
/* ****************************GPIO WiFi 配置结束********************************* */

#endif /* __BOARD_H__ */


```

## mmc.c
/home/ming/workspace/ISVP-T23-1.1.2-20240204/software/zh/Ingenic-SDK-T23-1.1.2-20240204-zh/opensource/kernel/arch/mips/xburst/soc-t23/chip-t23/isvp/common/mmc.c

```
#include <linux/mmc/host.h>
#include <linux/regulator/consumer.h>
#include <linux/gpio.h>
#include <linux/wakelock.h>
#include <linux/err.h>
#include <linux/delay.h>

#include <mach/jzmmc.h>

#include "board_base.h"

#include "board_base.h"

#ifdef CONFIG_JZMMC_V12_MMC0
static struct card_gpio tf_gpio = {
	.wp	    	= {GPIO_MMC_WP_N,	GPIO_MMC_WP_N_LEVEL},
	.cd			= {GPIO_MMC_CD_N,	GPIO_MMC_CD_N_LEVEL},
	.pwr		= {GPIO_MMC_PWR,	GPIO_MMC_PWR_LEVEL},
	.rst		= {GPIO_MMC_RST_N,	GPIO_MMC_RST_N_LEVEL},
};

/* common pdata for both tf_card and sdio wifi on fpga board */
struct jzmmc_platform_data tf_pdata = {
#if 1
	.removal  			= REMOVABLE,
	.sdio_clk			= 1,
	.ocr_avail			= MMC_VDD_32_33 | MMC_VDD_33_34,
	.capacity  			= MMC_CAP_SD_HIGHSPEED | MMC_CAP_MMC_HIGHSPEED | MMC_CAP_4_BIT_DATA,
	.pm_flags			= 0,
	.recovery_info			= NULL,
	.gpio				= &tf_gpio,
	.max_freq                       = CONFIG_MMC0_MAX_FREQ,
#ifdef CONFIG_MMC0_PIO_MODE
	.pio_mode                       = 1,
#else
	.pio_mode                       = 0,
#endif
#else
	 .removal  			= MANUAL,
	 .sdio_clk			= 1,
	 .ocr_avail			= MMC_VDD_29_30 | MMC_VDD_30_31,
	 .capacity  			= MMC_CAP_4_BIT_DATA | MMC_CAP_SDIO_IRQ,
	 .max_freq                       = CONFIG_MMC1_MAX_FREQ,
	 .recovery_info			= NULL,
	 .gpio				= NULL,
 #ifdef CONFIG_MMC1_PIO_MODE
	 .pio_mode			= 1,
 #else
	 .pio_mode			= 0,
 #endif
#ifdef CONFIG_BCM_PM_CORE
	 .private_init			= bcm_wlan_init,
#else
	 .private_init			= NULL,
#endif
#endif
};
#endif


#ifdef CONFIG_JZMMC_V12_MMC1

// 定义WiFi模块使用的GPIO配置结构体，用于管理WiFi的写保护(wp)、卡检测(cd)、电源控制(pwr)和复位(rst)引脚
static struct card_gpio wifi_gpio = {
    .wp            = {GPIO_WLAN_WP,    GPIO_MMC_WIFI_RST_N_LEVEL},  // 写保护引脚及电平设置
    .cd            = {GPIO_WLAN_CD,    GPIO_MMC_WIFI_RST_N_LEVEL},  // 卡检测引脚及电平设置
    .pwr        = {WLAN_PWR_EN,    GPIO_MMC_WIFI_POWER_LEVEL},      // 电源使能引脚及电平设置
    .rst        = {WL_REG_EN,    GPIO_MMC_WIFI_RST_N_LEVEL},        // 复位引脚及电平设置
};

#ifdef CONFIG_BCM_PM_CORE
// 如果定义了BCM电源管理核心模块，则声明bcm_wlan_init函数，该函数用于初始化无线局域网设备
extern int bcm_wlan_init(void);
#endif

// SDIO平台数据结构体，为SDIO接口提供必要的参数配置
struct jzmmc_platform_data sdio_pdata = {
     .removal              = MANUAL,          // 卡片移除方式：手动模式
     .sdio_clk            = 1,               // SDIO时钟使能标志
     .ocr_avail            = MMC_VDD_29_30 | MMC_VDD_30_31,  // 支持的电压范围
     .capacity              = MMC_CAP_4_BIT_DATA | MMC_CAP_SDIO_IRQ,  // 支持的能力：4位数据总线宽度和SDIO中断
     .max_freq             = CONFIG_MMC1_MAX_FREQ,           // 最大频率配置，使用宏定义值
     .recovery_info        = NULL,           // 恢复信息指针，当前未使用
     .gpio                = &wifi_gpio,            // GPIO配置指针，应该指向上面定义的wifi_gpio结构体，这里可能需要调整
 #ifdef CONFIG_MMC1_PIO_MODE
     .pio_mode            = 1,               // 使用PIO模式，根据CONFIG_MMC1_PIO_MODE宏定义确定
 #else
     .pio_mode            = 0,               // 不使用PIO模式
 #endif
#ifdef CONFIG_BCM_PM_CORE
     .private_init        = bcm_wlan_init,   // 私有初始化函数指针，如果启用了BCM电源管理核心，则调用bcm_wlan_init进行初始化
#else
     .private_init        = NULL,            // 否则不执行私有初始化
#endif
};
#endif

```





# 其他：
sdio中断方式。WIFI固件没有进行修改替换。
除了以上修改，其他地方无修改。

直接编译 make;          make strip
