---
title: "Echo: AI桌面机器人 / RV1106开发板 - 立创开源硬件平台"
source: "https://oshwhub.com/no_chicken/ai-desktop-robot-echo"
author:
published:
created: 2025-07-11
description: "这是一个十分硬核，功能超多的AI桌面机器人。有LVGL菜单，可以陪你聊天，翻译，看天气，能跑AI相机，是基于RV1106的小巧的linux开发板~"
tags:
  - "clippings"
---
![RV1106（桌面机器人Echo）/资料库/油炸鸡开源文档/非pdf保存/assets/Echo AI桌面机器人介绍/file-20250810171808440.webp](assets/Echo%20AI桌面机器人介绍/file-20250810171808440.webp)

## 描述

## AI桌面机器人Echo-Mate

## 📒 简介

**这可能是你见过最硬核的，功能最全的AI桌面机器人~**

## 资料汇总

[📖 手册链接](https://no-chicken.com/) [💻︎ github仓库](https://github.com/No-Chicken/Echo-Mate) [🔨 3D结构等资料](https://no-chicken.xyz/Echo-Mate/2.%E8%B5%84%E6%96%99%E6%94%B6%E9%9B%86.html) [🔗 功能演示](https://www.bilibili.com/video/BV161ZaYyEmF/) [🔗 教程视频](https://www.bilibili.com/video/BV1685qztEec/) [🏪 淘宝店铺](https://fry-oshw.taobao.com/)

- ✅ **功能丰富** ：本项目基于RV1106，是一个有LVGL菜单，可以陪你聊天，翻译，看天气，能跑AI相机，小巧的linux桌面助手和开发板~
- ✅ **用途广泛** ：提高你的桌面办公体验、作为陪伴、进行二次开发，或者作为课设和毕设的参考
- ✅ **操作简单** ：本项目如果仅复刻，无需编译Linux系统，直接使用提供的固件即可，大大简化操作（但需要会基本的Linux命令）
- ✅ **可多平台移植** ：不想复刻这个开发板，重新编译，软件可以在任何Linux设备跑，可以在你的ubuntu虚拟机跑仿真

如果深入学习，可以掌握的知识如下：

![RV1106（桌面机器人Echo）/资料库/油炸鸡开源文档/非pdf保存/assets/Echo AI桌面机器人介绍/file-20250810171808654.webp](assets/Echo%20AI桌面机器人介绍/file-20250810171808654.webp)

## 🤖 功能展示

部分界面展示如下（功能太多就不全部展示了）：

![RV1106（桌面机器人Echo）/资料库/油炸鸡开源文档/非pdf保存/assets/Echo AI桌面机器人介绍/file-20250810171808767.webp](assets/Echo%20AI桌面机器人介绍/file-20250810171808767.webp)

## 📁 系统组成

系统框图如下图所示，主控芯片RV1106，SDK使用的更改的 `luckfox-pico` 的SDK，图形库使用的LVGL。WIFI使用的SDIO接口，使用的RTL8723BS；屏幕使用的2.4寸触摸屏，存储介质可以自行选择使用SD卡或者板上的NAND Flash。具体的内容详见原理图。

![RV1106（桌面机器人Echo）/资料库/油炸鸡开源文档/非pdf保存/assets/Echo AI桌面机器人介绍/file-20250810171808863.webp](assets/Echo%20AI桌面机器人介绍/file-20250810171808863.webp)

## 📑 功能说明

各个历史版本实现的功能如下表所示：

![RV1106（桌面机器人Echo）/资料库/油炸鸡开源文档/非pdf保存/assets/Echo AI桌面机器人介绍/file-20250810171808997.webp](assets/Echo%20AI桌面机器人介绍/file-20250810171808997.webp)

1. LCD使用的2.4寸屏幕，SPI ST7789V，触摸为IIC FT6336U，触摸屏幕型号为 `P024C128-CTP` ；
2. LVGL菜单可以自行按照仓库代码的范式自行添加内容；
3. 小电视功能暂时就只是一个ffmpeg的一个演示；
4. 游戏参考延续了 [OV-Watch智能手表](https://oshwhub.com/no_chicken/zhi-neng-shou-biao-OV-Watch_V2.2) 的一些游戏的逻辑；
5. AI聊天采用websocket与服务器（你的电脑），进行通信，由于RV1106是单核A7算力不够，所以AI聊天的相关模型推理等放到了 `Server` 端，详细见Server端的 [Python代码](https://github.com/No-Chicken/Demo4Echo/tree/main/AIChat_demo/Server) ，当然，为了照顾不想搭建环境的同学，打包好了一个Server的exe可执行文件，可以自行下载到window电脑运行，作为服务器；
6. 意图理解，这个是用谷歌的 `FastText` 模型进行文字的分类任务，还是深度学习那一套；
7. 供电暂时只有TypeC供电，后续可加入电池提高空间自由度

## 🔨 硬件介绍

Echo-Mate的核心板，硬件框图如下所示：

![RV1106（桌面机器人Echo）/资料库/油炸鸡开源文档/非pdf保存/assets/Echo AI桌面机器人介绍/file-20250810171809092.webp](assets/Echo%20AI桌面机器人介绍/file-20250810171809092.webp)

![RV1106（桌面机器人Echo）/资料库/油炸鸡开源文档/非pdf保存/assets/Echo AI桌面机器人介绍/file-20250810171809208.webp](assets/Echo%20AI桌面机器人介绍/file-20250810171809208.webp)

![RV1106（桌面机器人Echo）/资料库/油炸鸡开源文档/非pdf保存/assets/Echo AI桌面机器人介绍/file-20250810171809333.webp](assets/Echo%20AI桌面机器人介绍/file-20250810171809333.webp)

具体的细节这里不做赘述，详见工程的原理图和PCB。原理图很多地方就是参考RV1106的官方设计手册等资料进行的外围电路设计，如果不想做驱动板不想打外壳，直接打这个RV1106核心板，在核心板上做开发也是可以的。

**注意** ，硬件例如CSI摄像头等地方，需要差分走线，详见PCB的网络差分对。

Echo-Mate AI桌面机器人的“腿”，也就是电机驱动板，使用TC118S驱动减速电机，逻辑比较简单，这里也不再过多赘述。

![RV1106（桌面机器人Echo）/资料库/油炸鸡开源文档/非pdf保存/assets/Echo AI桌面机器人介绍/file-20250810171809404.webp](assets/Echo%20AI桌面机器人介绍/file-20250810171809404.webp)

## 💻 软件介绍

1. **工程的软件框架介绍**
	Echo-Mate的软件框架如下图所示， `Middleware` 用到较多的包，在仓库的 `buildroot` 默认设置已经设置好了，如果需要加库请自行操作。
	这里只对大概框架进行说明，具体的代码细节需要在仓库中自行学习。仓库中都写有 `README` ，有详细的如何编译，如何烧录，请仔细看！
	![RV1106（桌面机器人Echo）/资料库/油炸鸡开源文档/非pdf保存/assets/Echo AI桌面机器人介绍/file-20250810171809546.webp](assets/Echo%20AI桌面机器人介绍/file-20250810171809546.webp)
	1. UI层使用 `LVGL` ， `PageManager` 仍然使用栈，进行多页面的管理，相比之前的OV-Watch手表项目，这个项目中的 `PageManager` 更加完善，可以直接使用char字符来注册和查询页面，相比直接用变量更加方便管理，开源界面空间有限不过多赘述。详细可以到手册或者代码去看。
	2. UI层中，创建APP的逻辑就是，进入页面后，开启一个线程运行APP，主线程还是UI线程，详细内容见仓库代码，例如：
		```cpp
		// 创建并初始化Application对象
		void* create_aichat_app(const char* address, int port, const char* token, const char* deviceId, const char* aliyun_api_key, int protocolVersion, int sample_rate, int channels, int frame_duration) {
		    auto* app = new Application(std::string(address), port, std::string(token), std::string(deviceId), std::string(aliyun_api_key), protocolVersion, sample_rate, channels, frame_duration);
		    return static_cast(app);
		}
		int start_ai_chat(const char* address, int port, const char* token, const char* deviceId, 
		                  const char* aliyun_api_key, int protocolVersion, int sample_rate, 
		                  int channels, int frame_duration) {
		    .....省略此处.....
		    pthread_mutex_lock(&amp;running_mutex);
		    // 创建应用
		    app_instance = create_aichat_app(address, port, token, deviceId, aliyun_api_key, 
		                                     protocolVersion, sample_rate, channels, frame_duration);
		    pthread_mutex_unlock(&amp;running_mutex);
		    .....省略此处.....
		    return 0;
		}
		```
	3. 业务层，就是这些APP的实际实现的具体功能了，例如UI中AI Chat聊天APP的功能，或者AI相机，yolov5的推理，这些运行的结果可以在UI层进行显示，即UI层与具体业务层进行交互。
	4. [DeskBot\_demo](https://github.com/No-Chicken/Demo4Echo/tree/main/DeskBot_demo) 的目录结构说明
		```
		DeskBot_demo/
		├── bin/                   # 可执行文件
		├── build/                 # build缓存
		├── common/                # 通用层
		│   ├── sys_manager/       # 开发板硬件对应的管理
		│   └── xxx_manager/       # xxx对应的管理
		├── conf/                  # 系统设置
		├── gui_app/               # UI层的软件
		│   ├── common/            # UI层扩展lib
		│   ├── font/              # UI字体
		│   ├── images/            # UI图片
		│   ├── pages/             # UI层主要pages
		│   └── ui.c/h             # 
		├── lvgl/                  # lvgl核心组件
		├── utils                  # 其他
		├── lv_conf.h              # lvgl设置
		└── main.c
		```
2. **AI Chat聊天原理介绍**
	AI Chat的原理图如下图所示。 `snowboy` 在开发板部署，作热词唤醒； `FSMN-VAD` 模型实现语音活动端点识别； `SenceVoice` 作语音转文字ASR； `CosyVoice` 作文字转语音TTS； `FastText` 作意图识别，即做文本的多分类任务，后续意图识别改为了 `MCP` ，进行 `function call` ，即大模型直接输出意图相关的内容(json)，再进行解释执行即可。
	为什么不参考小爱同学使用 `bert` 进行分类任务, 是因为 `bert` 要针对特定任务做微调,我电脑有点带不动>.< 。
	**注意** ：这些模型都是在你的电脑运行的，相当于你的电脑作为服务器。
	![RV1106（桌面机器人Echo）/资料库/油炸鸡开源文档/非pdf保存/assets/Echo AI桌面机器人介绍/file-20250810171809639.webp](assets/Echo%20AI桌面机器人介绍/file-20250810171809639.webp)
	由于RV1106开发板是单核A7的，算力不是很够，没有办法在本地运行 `sherpa-onnx` 或 `sherpa-ncnn` ，会导致无法实时的进行语音识别，之前为了实现本地ASR，试过运行模型 `zipformer` ， `RTF(Real-Time Factor)` 非常高，都超过1了，完全无法实现实时的语音识别，所以本地部署方案直接否决。
	![RV1106（桌面机器人Echo）/资料库/油炸鸡开源文档/非pdf保存/assets/Echo AI桌面机器人介绍/file-20250810171809763.webp](assets/Echo%20AI桌面机器人介绍/file-20250810171809763.webp)
	因此采用如下图所示的方法，电脑端（或者你有其他好的做服务器也行）作为服务器 `Server` ，开发板作为 `Client` 。具体的 `websocket` 的数据传输 `协议` 详见手册或者github中的 [AIchat\_demo](https://github.com/No-Chicken/Demo4Echo/tree/main/AIChat_demo) 说明。
	![RV1106（桌面机器人Echo）/资料库/油炸鸡开源文档/非pdf保存/assets/Echo AI桌面机器人介绍/file-20250810171809826.webp](assets/Echo%20AI桌面机器人介绍/file-20250810171809826.webp)
	除了 `CosyVoice` 和 `DeepSeek` ，其他模型都是部署到电脑本地，为了照顾没有GPU的同学， `Server` 中的的生成式模型， `CosyVoice` 和 `DeepSeek` ，调用的API，因为没有卡想要效果好就很慢。当然有GPU的同学有卡的同学，可以完全实现部署到电脑本地~
	`AI Chat` client端的具体的状态机转换如下图所示：
	![RV1106（桌面机器人Echo）/资料库/油炸鸡开源文档/非pdf保存/assets/Echo AI桌面机器人介绍/file-20250810171809942.webp](assets/Echo%20AI桌面机器人介绍/file-20250810171809942.webp)
	意图识别目前已经从FastText更换至MCP和function call，在开发板端，只需要向服务器注册function就可以了，例如在开发板上注册机器人移动的意图：
	```cpp
	void IntentsRegistry::RegisterAllFunctions(IntentHandler&amp; intent_handler) {
	    // 注册机器人移动相关的函数
	    intent_handler.RegisterFunction("robot_move", RobotMove::Move);
	    // 如果有其他功能模块，可以在这里继续注册
	    // intent_handler.RegisterFunction("audio_play", AudioControl::Play);
	}
	Json::Value IntentsRegistry::GenerateRegisterMessage() {
	    Json::Value message;
	    message["type"] = "functions_register";
	    // 添加 robot_move 的元信息
	    Json::Value robot_move;
	    robot_move["name"] = "robot_move";
	    robot_move["description"] = "让机器人运动";
	    // 添加多个 arguments
	    Json::Value arguments;
	    arguments["direction"] = "字符数据,分别有forward,backward,left和right";
	    arguments["speed"] = "整数数据,表示运动速度";
	    arguments["duration"] = "浮点数,表示运动持续时间（秒）";
	    robot_move["arguments"] = arguments;
	    // 将 robot_move 添加到 functions 数组中
	    message["functions"].append(robot_move);
	    return message;
	}
	```
	然后按照上述例子再自行完善 `RobotMove::Move` 这个函数即可了，十分方便~
3. **智能相机YOLO Camera原理介绍**
	这里的YOLO相机为了方便直接使用的 `nihui` 大佬的 `OpenCV-Mobile`, 使用 opencv-mobile 捕获摄像头图像的方式较为方便，但是失去了 VI 组件和 VPSS 组件的硬件加速，在性能上有明显损失，如果想要帧率更高，可以基于VI, VPSS进行图像捕获。
	![RV1106（桌面机器人Echo）/资料库/油炸鸡开源文档/非pdf保存/assets/Echo AI桌面机器人介绍/file-20250810171810054.webp](assets/Echo%20AI桌面机器人介绍/file-20250810171810054.webp)
	我已经编译好了适配Echo开发板的opencv-mobile包（与luckfox-pico相同，只是白名单需要改一下然后重新编译），可以直接拿去使用，这里不再赘述，东西太多了。
	YOLO相机具体实现的流程如下图（参考 `Luckfox-pico` 例程）：
4. **其他原理介绍**  
	更多软件细节，请到代码仓库中自行学习。例如：基本的数据结构堆栈链等，通信协议，C++状态机，C++设计模式，多线程管理，如何部署RKNN调用NPU，如何进行数据处理与模型训练等等。  
	**注意** ：天气和自动获取时间需要连接WIFI，地理地区对应的adcode城市代码已经放在附件的excel表中。

## 🔨 3D打印外壳介绍

可以直接拿到打包好的文件进行光固化打印即可，直接在立创3D打印下单，外壳的配件和组装好的图片如下所示：

![RV1106（桌面机器人Echo）/资料库/油炸鸡开源文档/非pdf保存/assets/Echo AI桌面机器人介绍/file-20250810171810175.webp](assets/Echo%20AI桌面机器人介绍/file-20250810171810175.webp) ![a1447fe33ab9c580dbfd43b6f466019b\_MD5](<assets/Echo AI桌面机器人介绍/file-20250810171810350.webp>)

## 📥 复刻指南

1. 需要的物料如下：
	- Echo核心板（BOM参见原理图，注意WIFI模块是 `RTL8723BS` 模块）
	- 3D打印外壳（去立创3D打印即可，注意主动轮和从动轮，都要打两份）
	- 焊接工具，焊接软线等
	- 螺丝螺母若干, 马达，双面胶等，详见附件 `配件表pdf`
2. 复刻需要的开发环境如下：
	- windows电脑一台
	- USB连接线
	- SD卡, 读卡器
	- usb转ttl串口模块
	- RK瑞芯微驱动助手
	- RK瑞芯微烧录工具
	- MobaXterm
3. 深入学习需要的开发环境如下：
	- Ubuntu22.04
	- python环境（python=3.10）
	- 以及带脑子，会查资料~

这里会简单说明一些固件烧录和程序执行，详细内容见 [手册](https://no-chicken.xyz/Echo-Mate/4.%E9%95%9C%E5%83%8F%E7%83%A7%E5%BD%95.html) 。

1. **固件烧录** ：  
	附件中上传了SD卡上的buildroot固件，由于只能上传50M的包，所以将多个part01-03全选然后解压缩即可。以下是简易的烧录示意：  
	首先格式化SD卡(可以使用SD Card formatter)，然后使用RK瑞芯微烧录工具进行烧录，烧好插上开发板即可。 **注意** ，使用SD卡作为存储介质启动，需要保证NAND Flash为空内容！
	![RV1106（桌面机器人Echo）/资料库/油炸鸡开源文档/非pdf保存/assets/Echo AI桌面机器人介绍/file-20250810171810487.webp](assets/Echo%20AI桌面机器人介绍/file-20250810171810487.webp)
	NAND FLASH的烧录和擦除方法可以详见 [手册](https://no-chicken.xyz/Echo-Mate/4.%E9%95%9C%E5%83%8F%E7%83%A7%E5%BD%95.html) 。
2. **开发板使用** ：
	1. 登录，可以使用串口登录和SSH登录（USB虚拟网卡）
	2. WIFI连接，时区设置, 文件传输等，详见 [手册](https://no-chicken.xyz/Echo-Mate/5.%E5%BC%80%E5%8F%91%E6%9D%BF%E6%93%8D%E4%BD%9C.html)
	3. 默认登录用户和密码为：
	```
	登录账号: root
	登录密码: root
	```
3. **程序执行** ：  
	首先解压附件中的 `bin.rar` ，然后把bin文件夹传到开发板中，然后vi更改 `system_para.conf`, 需要更改AI\_Chat\_Server地址为同网络下运行server的电脑地址，可通过ipconfig命令查看，开发板和电脑互ping一下就知道了；  
	还需要更改高德的api\_key，用于访问天气；以及需要更改阿里云百炼的api\_key。这两个key都需要注册一下，应该都是个人用户免费的。  
	想要正常访问天气等，需要连接WIFI哦，连接WIFI的指令可以看手册，或者网上搜~
	![RV1106（桌面机器人Echo）/资料库/油炸鸡开源文档/非pdf保存/assets/Echo AI桌面机器人介绍/file-20250810171810627.webp](assets/Echo%20AI桌面机器人介绍/file-20250810171810627.webp)
	![RV1106（桌面机器人Echo）/资料库/油炸鸡开源文档/非pdf保存/assets/Echo AI桌面机器人介绍/file-20250810171810739.webp](assets/Echo%20AI桌面机器人介绍/file-20250810171810739.webp)
	然后再进入 `bin` 文件夹内，执行 `main` 即可，注意必须进入 `bin` 文件夹中执行，因为有各种文件依赖:
	```sh
	cd ./bin
	chmod +x ./main
	./main
	```
	![RV1106（桌面机器人Echo）/资料库/油炸鸡开源文档/非pdf保存/assets/Echo AI桌面机器人介绍/file-20250810171810804.webp](assets/Echo%20AI桌面机器人介绍/file-20250810171810804.webp)
	如果想要正常运行聊天功能，还需要在电脑上运行 `Server` 服务，如果有 `python` 环境的可以参考仓库按照 [Server环境搭建与运行](https://github.com/No-Chicken/Demo4Echo/blob/main/AIChat_demo/Server/README.md) 搭建环境然后运行即可。 `ctrl+C` 可中断程序.
	```sh
	python ./main.py --access_token="123456"
	```
	![RV1106（桌面机器人Echo）/资料库/油炸鸡开源文档/非pdf保存/assets/Echo AI桌面机器人介绍/file-20250810171810945.webp](assets/Echo%20AI桌面机器人介绍/file-20250810171810945.webp)
	如果不想搭建环境不想用python，这里也打包好了`.exe` 可执行文件（有点大2个G），直接运行即可，运行方式如下：  
	解压完 `AiChatServer-Win-exe-V1.0.rar`, 进入main文件夹，然后在这个文件中进入cmd，运行即可. `ctrl+双击C` 可中断程序.
	```sh
	.\main.exe --access_token="123456"
	```
	![RV1106（桌面机器人Echo）/资料库/油炸鸡开源文档/非pdf保存/assets/Echo AI桌面机器人介绍/file-20250810171811037.webp](assets/Echo%20AI桌面机器人介绍/file-20250810171811037.webp)
	Server打包好的exe百度网盘：  
	`AiChatServer-Win-exe-V1.1.rar` 网盘链接: [https://pan.baidu.com/s/1\_s\_79DHZS9EZjnfybqlNJw?pwd=r7f7](https://pan.baidu.com/s/1_s_79DHZS9EZjnfybqlNJw?pwd=r7f7) 提取码: r7f7
4. **3D外壳装配** ：  
	详见附件的复刻视频或者B站视频~

## 📑 课后作业

有能力的同学可以完成以下作业，我会大致给出解决的方向：

1. 整体：熟悉整个工程包括软件和硬件 **（基本项）**
2. 硬件：自行更改核心板，加入 `EMMC` 作为存储介质 **（困难）**
3. 软件：在LVGL菜单添加一个简单的 `APP` ，例如 `定时器`, 可以参考之前手表项目的逻辑实现 **（简单）**
4. 软件：不使用 `Opencv-mobile`, 使用 `VI`,`VPSS` 组件进行捕获图形, 试下提高帧率 **（中等）**
5. 软件：在 `意图识别` 中加入一个意图分类，例如 `增减屏幕亮度` **(中等)**  
	(目前有的意图只有: 前后左右运动，以及对话结束说拜拜)
6. 驱动：是否可以实现 `DRM` 驱动ST7789V屏幕，目前使用的 `fb` ，可以参考网上的 `tinydrm` 的移植 **（困难）**
7. 驱动：修改设备树，使能和禁止蓝色的LED **（简单）**
8. 驱动：加入OV2685 **（困难）**
9. 其他...

## 🔗 参考资料

[\[1\] luckfox rkmpi学习指南](https://wiki.luckfox.com/zh/Luckfox-Pico/RKMPI-example)  
[\[2\] 新一代kaldi（k2-fsa）sherpa-onnx](https://k2-fsa.github.io/sherpa/intro.html)  
[\[3\] FunASR](https://github.com/modelscope/FunASR)  
[\[4\] SenceVoice](https://github.com/FunAudioLLM/SenseVoice/blob/main/README_zh.md)  
[\[5\] SenceVoice论文](https://arxiv.org/abs/2407.04051)  
[\[6\] CosyVoice](https://github.com/FunAudioLLM/CosyVoice)  
[\[7\] FastText](https://github.com/facebookresearch/fastText)  
[\[8\] OpenCV-Mobile](https://github.com/nihui/opencv-mobile)  
[\[8\] 小智ESP32](https://github.com/78/xiaozhi-esp32)

## ⚠️ 注意事项

1. WIFI模块别搞错了，是RTL8723BS模块！
2. 如果想要学习开发，请在ubuntu虚拟机上下拉仓库学习！
3. 层叠结构，免费的7628，免费的20%阻抗
4. WIFI的天线购买立创的 AIWF022 即可，WIFI7 内置FPC天线 2.4G&5.8G双频PCB柔性天线
5. 屏幕型号是淘宝浦洋的：P024C128-CTP触摸屏
6. 软件请以仓库和手册为准，硬件以立创开源平台的PCB为准！
7. 最新SD卡固件和NAND固件，请到手册中下载，立创不一定上传的最新的！

<video src="https://image.lceda.cn/oshwhub/project/attachments/001b197eebdb4a31b5c6a00a93ad475b.mp4" controls=""></video>

