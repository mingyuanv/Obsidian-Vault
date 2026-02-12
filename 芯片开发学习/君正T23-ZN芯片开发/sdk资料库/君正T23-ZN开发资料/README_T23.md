# **使用sdk之前，请优先阅读此文本作为步骤引导及文档指南**



- 拿到开发板，先阅读**Ingenic_Zeratul_T23_INDUS开发板使用说明**，认识开发板各个模块、设备的连接、固件烧录、配网、SD卡挂载，然后进行程序的运行，视频的预览等。

  

- 设备连接好之后，可以继续阅读**Ingenic_Zeratul_T23_SDK使用说明**，认识zeratul的SDK结构、系统的分区信息，然后进行toolchain工具链的安装、zeratul—T41基础环境的搭建（uboot、tag、kernel等编译）。固件编译完成可以烧录（观看**Ingenic_Zeratul_T23_烧录说明**文档）。烧录完成，往下进行IMP库中sample的使用方法。可继续查看系统常用的调试、SDK编译常见问题等。

  

- 可以阅读**Ingenic_Zeratul_T23_开发指南**。了解zeratul的产品架构、搭建camera基础环境、调试阶段文件系统的更新与固件的烧录、MCU_WTD功能、Camera快速启动相关操作、ISP驱动的介绍，

  

- 如需要把ISVP中的sensor移植到zeratul中或者新的sensor的添加，可以查看**Ingenic_Zeratul_T23_sensor移植调试说明**说明文档，文档中说明了ISVP与Zeratul驱动的区别、移植流程、移植过程中的一下异常问题。

  

- 进行一些tag、uboot相关的一些操作，可阅读**Ingenic_Zeratul_T23_TAG-ZRT_UBOOT使用说明**。文档包括tag中gpio、adc、pwm、白光灯、IRLD&IRCUT操作方法，双系统/SFC/分区大小设置、tag备份使用、sensor时序调节、recovery按键复发、系统升级、uboot flash clk及uboot debug相关说明。

  

- 进行USB的一些转接配置可阅读**Ingenic_Zeratul_T23_USB接口配置说明**。文档主要包括USB转以太网、USB转U盘、USB转RNDIS、USB转4G、USB转串口操作。

  

- **T23 系统资源及 GPIO 配置**包含了GPIO使用、UART配置、I2c配置、SPI使用、PWM使用、ADC配置等内容

  

- 进行媒体内存优化相关了解，可参考**Ingenic_Zeratul_T23媒体内存优化说明**。

  

- 进行媒体内存池相关操作，可参**考Ingenic_Zeratul_T23媒体内存池使用说明**。文档包括RMEM内存池的简介、mempool的概念及使用方法等。

  

- 在使用过程中的一些容易出现的问题都在**Ingenic_Zeratul_T23常见问题FAQ**文档中有相关说明，包括节点错乱、pad normal uboot无法启动、不出流、编译内核报错、帧率异常等等。

  

- 参考**Ingenic_Zeratul_T23快起环境搭建**文档来搭建快启的环境，之后，如需进行快起效果调试可参考**Ingenic_Zeratul_T23快起效果调试说明**。文档包括起始EV介绍、RISCV介绍、测试环境及IRCUT、IRLED的处理方法。

  

- 了解系统调试的命令，可以参考**Ingenic_Zeratul_T23系统调试命令集**，获取时钟频率、sensor帧率、ISP基本信息等。

  

- 如果有使用白光灯或者红外灯的需求，可以参考**Ingenic_Zeratul_T23_白光灯红外灯使用说明**，按照文档配置使用。

  

- 使用软光敏可以在牺牲一部分出图速度的条件下节省一颗硬件光敏元器件,产品外壳无需开孔以及增加透镜，参考**Ingenic_Zeratul_T23_软光敏调试说明**进行相关开发。

  

- **Ingenic_Zeratul_T23_视频编码常见问题**包含了：编码初始化接口、码控方式、编码方式切换以及动态设置编码参数、jpeg编码等等编码相关的介绍。

  

- 如要进行BSP相关的开发操作，可参考**Ingenic_Zeratul_T23_BSP开发指南.pdf**。文档主要包括系统资源的使用与调试，如：ISP_Sensor驱动、Audio驱动的介绍，GPIO使用、UART配置、I2c配置、SPI使用、PWM使用、ADC配置、Watch dog配置、Motor、GMAC、SD/EMMC/SDIO、USB等配置使用。

  

  

  

