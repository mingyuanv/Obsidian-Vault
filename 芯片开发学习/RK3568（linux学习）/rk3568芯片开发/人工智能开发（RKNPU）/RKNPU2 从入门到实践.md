[RKNPU2 从入门到实践](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/RKNPU2%20从入门到实践.one#section-id={641937CE-3813-4C58-8FF0-46D25EB3FA91}&end)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28RKNPU2%20%E4%BB%8E%E5%85%A5%E9%97%A8%E5%88%B0%E5%AE%9E%E8%B7%B5.one%7C641937CE-3813-4C58-8FF0-46D25EB3FA91%2F%29))
# 备注:

# 一、基础知识

## 第 1 章初识 RKNPU
> [!PDF|important] [[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/assets/RKNPU2 从入门到实践/file-20250810171708398.pdf#page=6&selection=20,0,28,5&color=important|NPU开发配套资料-视频教程（总结）, p.6]]
> > 第 1 章初识 RKNPU
> 
> 

[01 初识RKNPU](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/RKNPU2%20从入门到实践.one#01%20初识RKNPU&section-id={641937CE-3813-4C58-8FF0-46D25EB3FA91}&page-id={97678D01-D821-4DB1-A569-DE7114954F33}&end)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28RKNPU2%20%E4%BB%8E%E5%85%A5%E9%97%A8%E5%88%B0%E5%AE%9E%E8%B7%B5.one%7C641937CE-3813-4C58-8FF0-46D25EB3FA91%2F01%20%E5%88%9D%E8%AF%86RKNPU%7C97678D01-D821-4DB1-A569-DE7114954F33%2F%29))


## 第 2 章 RKNPU 推理软件框架
> [!PDF|important] [[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/assets/RKNPU2 从入门到实践/file-20250810171708398.pdf#page=14&selection=15,0,24,6&color=important|NPU开发配套资料-视频教程（总结）, p.14]]
> > 第 2 章 RKNPU 推理软件框架
> 
> 

[02 RKNPU软件推理框架](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/RKNPU2%20从入门到实践.one#02%20RKNPU软件推理框架&section-id={641937CE-3813-4C58-8FF0-46D25EB3FA91}&page-id={F59CD01D-BFC9-4CB4-BBC3-9968F7B7BDA8}&end)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28RKNPU2%20%E4%BB%8E%E5%85%A5%E9%97%A8%E5%88%B0%E5%AE%9E%E8%B7%B5.one%7C641937CE-3813-4C58-8FF0-46D25EB3FA91%2F02%20RKNPU%E8%BD%AF%E4%BB%B6%E6%8E%A8%E7%90%86%E6%A1%86%E6%9E%B6%7CF59CD01D-BFC9-4CB4-BBC3-9968F7B7BDA8%2F%29))

## 补充
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/框架图|RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/框架图]]
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/assets/RKNPU2 从入门到实践/file-20250810171708585.pdf|RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/assets/RKNPU2 从入门到实践/file-20250810171708585.pdf]]
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/assets/RKNPU2 从入门到实践/file-20250810171708630.pdf|RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/assets/RKNPU2 从入门到实践/file-20250810171708630.pdf]]
# 二、环境配置
## 简介：
## 1.RKNN Toolkit2 环境搭建(python接口)(ubuntu20)
[03_RKNN Toolkit2 环境搭建(pycharm)](onenote:https://d.docs.live.net/52D4B76BB0FFCF51/Documents/\(RK3568\)Linux驱动开发/RKNPU2%20从入门到实践.one#03_RKNN%20Toolkit2%20环境搭建\(pycharm\)&section-id={641937CE-3813-4C58-8FF0-46D25EB3FA91}&page-id={B809C4B4-FA14-4005-999C-D8CE71081A8A}&end)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28RKNPU2%20%E4%BB%8E%E5%85%A5%E9%97%A8%E5%88%B0%E5%AE%9E%E8%B7%B5.one%7C641937CE-3813-4C58-8FF0-46D25EB3FA91%2F03_RKNN%20Toolkit2%20%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA%28pycharm%5C%29%7CB809C4B4-FA14-4005-999C-D8CE71081A8A%2F%29))

### 第 3 章搭建 RKNN Toolkit2 开发环境（手册）
> [!PDF|important] [[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/assets/RKNPU2 从入门到实践/file-20250810171708398.pdf#page=20&selection=16,0,28,4&color=important|NPU开发配套资料-视频教程（总结）, p.20]]
> > 第 3 章搭建 RKNN Toolkit2 开发环境
> 
> 

### 可以直接使用搭建好的环境
[可以直接使用搭建好的环境](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/RKNPU2%20从入门到实践.one#03_RKNN%20Toolkit2%20环境搭建\(pycharm\)&section-id={641937CE-3813-4C58-8FF0-46D25EB3FA91}&page-id={B809C4B4-FA14-4005-999C-D8CE71081A8A}&object-id={965D9CE5-5555-476B-A4AF-CD4345A7292B}&10)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28RKNPU2%20%E4%BB%8E%E5%85%A5%E9%97%A8%E5%88%B0%E5%AE%9E%E8%B7%B5.one%7C641937CE-3813-4C58-8FF0-46D25EB3FA91%2F03_RKNN%20Toolkit2%20%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA%28pycharm%5C%29%7CB809C4B4-FA14-4005-999C-D8CE71081A8A%2F%29))
### 补充
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/assets/RKNPU2 从入门到实践/file-20250810171708754.pdf|RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/assets/RKNPU2 从入门到实践/file-20250810171708754.pdf]]
## 2.开发板上RKNN Toolkit lite2部署(python接口)

### 第 6 章 RKNN-ToolkitLite 2 环境搭建
> [!PDF|red] [[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/assets/RKNPU2 从入门到实践/file-20250810171708398.pdf#page=87&selection=11,0,19,4&color=red|NPU开发配套资料-视频教程（总结）, p.87]]
> > 第 6 章 RKNN-ToolkitLite 2 环境搭建
> 
> 


<span style="background:#b1ffff">RKNN Toolkit2的一个阉割版</span>

[08_RKNN Toolkit lite2部署RKNN模型](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/RKNPU2%20从入门到实践.one#08_RKNN%20Toolkit%20lite2部署RKNN模型&section-id={641937CE-3813-4C58-8FF0-46D25EB3FA91}&page-id={9FCD5CD8-259D-4302-A56F-08E437533D9F}&end)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28RKNPU2%20%E4%BB%8E%E5%85%A5%E9%97%A8%E5%88%B0%E5%AE%9E%E8%B7%B5.one%7C641937CE-3813-4C58-8FF0-46D25EB3FA91%2F08_RKNN%20Toolkit%20lite2%E9%83%A8%E7%BD%B2RKNN%E6%A8%A1%E5%9E%8B%7C9FCD5CD8-259D-4302-A56F-08E437533D9F%2F%29))

- 注意：<span style="background:#affad1">开发板上部署的是ubuntu20系统</span>

### 补充
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/assets/RKNPU2 从入门到实践/file-20250810171708778.pdf|RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/assets/RKNPU2 从入门到实践/file-20250810171708778.pdf]]
## 3.RKNPU2 SDK（c接口）

[09_RKNPU2 初始环境的构建](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/RKNPU2%20从入门到实践.one#09_RKNPU2%20初始环境的构建&section-id={641937CE-3813-4C58-8FF0-46D25EB3FA91}&page-id={8AC9789E-38E1-4A8A-812B-C8735AB0A4C6}&end)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28RKNPU2%20%E4%BB%8E%E5%85%A5%E9%97%A8%E5%88%B0%E5%AE%9E%E8%B7%B5.one%7C641937CE-3813-4C58-8FF0-46D25EB3FA91%2F09_RKNPU2%20%E5%88%9D%E5%A7%8B%E7%8E%AF%E5%A2%83%E7%9A%84%E6%9E%84%E5%BB%BA%7C8AC9789E-38E1-4A8A-812B-C8735AB0A4C6%2F%29))

直接<span style="background:#b1ffff">把整个文件夹放在vscode上交叉编译</span>好,然后把它<span style="background:#affad1">编译出来的install文件夹传输到开发板上运行即可</span> 

- 注意：建议重装一下gcc编译器
## 4.adb连接
[ubuntu通过adb连接到开发板进行连板推理](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/RKNPU2%20从入门到实践.one#ubuntu通过adb连接到开发板进行连板推理&section-id={641937CE-3813-4C58-8FF0-46D25EB3FA91}&page-id={18B98BB8-97DC-46CF-8F94-B4CA88FDF21D}&end)   ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28RKNPU2%20%E4%BB%8E%E5%85%A5%E9%97%A8%E5%88%B0%E5%AE%9E%E8%B7%B5.one%7C641937CE-3813-4C58-8FF0-46D25EB3FA91%2Fubuntu%E9%80%9A%E8%BF%87adb%E8%BF%9E%E6%8E%A5%E5%88%B0%E5%BC%80%E5%8F%91%E6%9D%BF%E8%BF%9B%E8%A1%8C%E8%BF%9E%E6%9D%BF%E6%8E%A8%E7%90%86%7C18B98BB8-97DC-46CF-8F94-B4CA88FDF21D%2F%29))

- 注意：<span style="background:#affad1">开发板上部署的是ubuntu20.04系统</span>
# 三、RKNN Toolkit2的使用
## 简介：
这个主要用于<span style="background:#b1ffff">连板推理测试，优化模型精度</span> 。<span style="background:#affad1">方便后面利用RKNN Toolkit lite2部署在开发板上。</span>
## 1.RKNN模型构建（导出模型）
> [!PDF|note] [[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/assets/RKNPU2 从入门到实践/file-20250810171708398.pdf#page=73&selection=207,0,211,2&color=note|NPU开发配套资料-视频教程（总结）, p.73]]
> > 构建 RKNN 模型
> 
> 

[04_RKNN模型构建](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/RKNPU2%20从入门到实践.one#04_RKNN模型构建&section-id={641937CE-3813-4C58-8FF0-46D25EB3FA91}&page-id={555022B0-C26F-47AF-B7FE-437D1D068FF2}&end)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28RKNPU2%20%E4%BB%8E%E5%85%A5%E9%97%A8%E5%88%B0%E5%AE%9E%E8%B7%B5.one%7C641937CE-3813-4C58-8FF0-46D25EB3FA91%2F04_RKNN%E6%A8%A1%E5%9E%8B%E6%9E%84%E5%BB%BA%7C555022B0-C26F-47AF-B7FE-437D1D068FF2%2F%29))

### 补充
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/assets/RKNPU2 从入门到实践/file-20250810171708856.pdf|RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/assets/RKNPU2 从入门到实践/file-20250810171708856.pdf]]
## 2.RKNN 模型评估-推理测试
> [!PDF|note] [[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/assets/RKNPU2 从入门到实践/file-20250810171708398.pdf#page=76&selection=234,0,234,4&color=note|NPU开发配套资料-视频教程（总结）, p.76]]
> > 模型推理
> 
> 

[(代码)加载非RKNN模型(模拟器或者连板推理) 02_inference](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/RKNPU2%20从入门到实践.one#\(代码\)加载非RKNN模型\(模拟器或者连板推理\)%20%2002_inference&section-id={641937CE-3813-4C58-8FF0-46D25EB3FA91}&page-id={1FA9F05D-01AD-4511-B909-FC7E1A5BECDE}&end)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28RKNPU2%20%E4%BB%8E%E5%85%A5%E9%97%A8%E5%88%B0%E5%AE%9E%E8%B7%B5.one%7C641937CE-3813-4C58-8FF0-46D25EB3FA91%2F%28%E4%BB%A3%E7%A0%81%5C%29%E5%8A%A0%E8%BD%BD%E9%9D%9ERKNN%E6%A8%A1%E5%9E%8B%28%E6%A8%A1%E6%8B%9F%E5%99%A8%E6%88%96%E8%80%85%E8%BF%9E%E6%9D%BF%E6%8E%A8%E7%90%86%5C%29%20%2002_inference%7C1FA9F05D-01AD-4511-B909-FC7E1A5BECDE%2F%29))

[(代码)加载RKNN模型(连板推理) 02_inference](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/RKNPU2%20从入门到实践.one#\(代码\)加载RKNN模型\(连板推理\)%20%2002_inference&section-id={641937CE-3813-4C58-8FF0-46D25EB3FA91}&page-id={DF86737D-E11B-428A-A2A4-0D1A66D7E4EB}&end)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28RKNPU2%20%E4%BB%8E%E5%85%A5%E9%97%A8%E5%88%B0%E5%AE%9E%E8%B7%B5.one%7C641937CE-3813-4C58-8FF0-46D25EB3FA91%2F%28%E4%BB%A3%E7%A0%81%5C%29%E5%8A%A0%E8%BD%BDRKNN%E6%A8%A1%E5%9E%8B%28%E8%BF%9E%E6%9D%BF%E6%8E%A8%E7%90%86%5C%29%20%2002_inference%7CDF86737D-E11B-428A-A2A4-0D1A66D7E4EB%2F%29))
### 模拟器或者连板推理的切换
![RK3568（linux学习）/rk3568芯片开发/人工智能开发（未）/assets/RKNPU2 从入门到实践/file-20250810171708924.png](assets/RKNPU2%20从入门到实践/file-20250810171708924.png)

### 补充
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/assets/RKNPU2 从入门到实践/file-20250810171709067.pdf|RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/assets/RKNPU2 从入门到实践/file-20250810171709067.pdf]]

## 3.RKNN 模型评估-量化精度分析
> [!PDF|red] [[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/assets/RKNPU2 从入门到实践/file-20250810171708398.pdf#page=78&selection=19,0,19,6&color=red|NPU开发配套资料-视频教程（总结）, p.78]]
> > 量化精度分析

[(代码)量化精度分析(模拟器或者连板推理) 03_accuracy_analysis](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/RKNPU2%20从入门到实践.one#\(代码\)量化精度分析\(模拟器或者连板推理\)%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%2003_accuracy_analysis&section-id={641937CE-3813-4C58-8FF0-46D25EB3FA91}&page-id={F6F355FF-E50A-4DFA-A329-1B3D668822F2}&end)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28RKNPU2%20%E4%BB%8E%E5%85%A5%E9%97%A8%E5%88%B0%E5%AE%9E%E8%B7%B5.one%7C641937CE-3813-4C58-8FF0-46D25EB3FA91%2F%28%E4%BB%A3%E7%A0%81%5C%29%E9%87%8F%E5%8C%96%E7%B2%BE%E5%BA%A6%E5%88%86%E6%9E%90%28%E6%A8%A1%E6%8B%9F%E5%99%A8%E6%88%96%E8%80%85%E8%BF%9E%E6%9D%BF%E6%8E%A8%E7%90%86%5C%29%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%2003_accuracy_analysis%7CF6F355FF-E50A-4DFA-A329-1B3D668822F2%2F%29))

### 混合量化，提高模型推理的精度
> [!PDF|red] [[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/assets/RKNPU2 从入门到实践/file-20250810171708398.pdf#page=79&selection=0,10,19,4&color=red|NPU开发配套资料-视频教程（总结）, p.79]]
> > 北京迅为电子有限公司 RKNPU 开发指南日期：2022-2-13 www.topeetboard.com12 4.10 混合量化


[(代码)混合量化(step1) 04_hybrid_quantization](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/RKNPU2%20从入门到实践.one#\(代码\)混合量化\(step1\)%20%20%2004_hybrid_quantization&section-id={641937CE-3813-4C58-8FF0-46D25EB3FA91}&page-id={110A7954-6C2A-42D2-BF1F-9A96B289434D}&end)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28RKNPU2%20%E4%BB%8E%E5%85%A5%E9%97%A8%E5%88%B0%E5%AE%9E%E8%B7%B5.one%7C641937CE-3813-4C58-8FF0-46D25EB3FA91%2F%28%E4%BB%A3%E7%A0%81%5C%29%E6%B7%B7%E5%90%88%E9%87%8F%E5%8C%96%28step1%5C%29%20%20%2004_hybrid_quantization%7C110A7954-6C2A-42D2-BF1F-9A96B289434D%2F%29))
[(代码)混合量化(step2) 04_hybrid_quantization](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/RKNPU2%20从入门到实践.one#\(代码\)混合量化\(step2\)%20%20%20%2004_hybrid_quantization&section-id={641937CE-3813-4C58-8FF0-46D25EB3FA91}&page-id={4D9D7085-1C7E-44A8-BB5B-E2350FE3531E}&end)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28RKNPU2%20%E4%BB%8E%E5%85%A5%E9%97%A8%E5%88%B0%E5%AE%9E%E8%B7%B5.one%7C641937CE-3813-4C58-8FF0-46D25EB3FA91%2F%28%E4%BB%A3%E7%A0%81%5C%29%E6%B7%B7%E5%90%88%E9%87%8F%E5%8C%96%28step2%5C%29%20%20%20%2004_hybrid_quantization%7C4D9D7085-1C7E-44A8-BB5B-E2350FE3531E%2F%29))

### 补充
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/assets/RKNPU2 从入门到实践/file-20250810171709107.pdf|RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/assets/RKNPU2 从入门到实践/file-20250810171709107.pdf]]

## 4.RKNN 模型评估-性能评估和内存评估
> [!PDF|red] [[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/assets/RKNPU2 从入门到实践/file-20250810171708398.pdf#page=80&selection=62,0,64,4&color=red|NPU开发配套资料-视频教程（总结）, p.80]]
> > 4.11 评估性能

> [!PDF|red] [[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/assets/RKNPU2 从入门到实践/file-20250810171708398.pdf#page=80&selection=137,0,140,2&color=red|NPU开发配套资料-视频教程（总结）, p.80]]
> > 4.12 评估内存


[(代码)性能评估 05_eval](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/RKNPU2%20从入门到实践.one#\(代码\)性能评估%20%2005_eval&section-id={641937CE-3813-4C58-8FF0-46D25EB3FA91}&page-id={A9460EF0-8628-4CBE-8671-87FEF54584B3}&end)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28RKNPU2%20%E4%BB%8E%E5%85%A5%E9%97%A8%E5%88%B0%E5%AE%9E%E8%B7%B5.one%7C641937CE-3813-4C58-8FF0-46D25EB3FA91%2F%28%E4%BB%A3%E7%A0%81%5C%29%E6%80%A7%E8%83%BD%E8%AF%84%E4%BC%B0%20%2005_eval%7CA9460EF0-8628-4CBE-8671-87FEF54584B3%2F%29))

[(代码)内存评估 05_eval](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/RKNPU2%20从入门到实践.one#\(代码\)内存评估%20%20%2005_eval&section-id={641937CE-3813-4C58-8FF0-46D25EB3FA91}&page-id={5EED6DF6-E662-4198-89FE-1D63391218A7}&end)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28RKNPU2%20%E4%BB%8E%E5%85%A5%E9%97%A8%E5%88%B0%E5%AE%9E%E8%B7%B5.one%7C641937CE-3813-4C58-8FF0-46D25EB3FA91%2F%28%E4%BB%A3%E7%A0%81%5C%29%E5%86%85%E5%AD%98%E8%AF%84%E4%BC%B0%20%20%2005_eval%7C5EED6DF6-E662-4198-89FE-1D63391218A7%2F%29))
### 补充
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/assets/RKNPU2 从入门到实践/file-20250810171709168.pdf|RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/assets/RKNPU2 从入门到实践/file-20250810171709168.pdf]]
# 四、RKNN Toolkit lite2 的使用


## 简介：
一般只用在<span style="background:#affad1">前期的部署验证</span>
而要想获得更高的性能以及更好的效果
就需要使用RKNPU2 SDK所提供的c接口了
## 1.RKNN Toolkit lite2的使用
[使用RKNN Toolkit lite2](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/RKNPU2%20从入门到实践.one#使用RKNN%20Toolkit%20lite2&section-id={641937CE-3813-4C58-8FF0-46D25EB3FA91}&page-id={177C6E23-9AE4-4A42-A4DA-34733682E0AD}&end)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28RKNPU2%20%E4%BB%8E%E5%85%A5%E9%97%A8%E5%88%B0%E5%AE%9E%E8%B7%B5.one%7C641937CE-3813-4C58-8FF0-46D25EB3FA91%2F%E4%BD%BF%E7%94%A8RKNN%20Toolkit%20lite2%7C177C6E23-9AE4-4A42-A4DA-34733682E0AD%2F%29))

### 第 5 章 RKNN-ToolkitLite 2 API 介绍
> [!PDF|red] [[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/assets/RKNPU2 从入门到实践/file-20250810171708398.pdf#page=84&selection=20,0,33,2&color=red|NPU开发配套资料-视频教程（总结）, p.84]]
> > 第 5 章 RKNN-ToolkitLite 2 API 介绍
> 
> 


### 补充
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/assets/RKNPU2 从入门到实践/file-20250810171708778.pdf|RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/assets/RKNPU2 从入门到实践/file-20250810171708778.pdf]]
# 五、RKNPU2 SDK（c接口）的使用
## 简介：

## 1.RKNPU2 通用API的使用
> [!PDF|red] [[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/assets/RKNPU2 从入门到实践/file-20250810171708398.pdf#page=90&selection=20,0,32,4&color=red|NPU开发配套资料-视频教程（总结）, p.90]]
> > 第 7 章 RKNN C API 详细说明


[RKNPU2 通用API的使用(Main.cc) 01_resnet18](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/RKNPU2%20从入门到实践.one#RKNPU2%20通用API的使用\(Main.cc\)%20%2001_resnet18&section-id={641937CE-3813-4C58-8FF0-46D25EB3FA91}&page-id={E3A2453E-5393-4DE3-AD83-1BFE8DE440CE}&end)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28RKNPU2%20%E4%BB%8E%E5%85%A5%E9%97%A8%E5%88%B0%E5%AE%9E%E8%B7%B5.one%7C641937CE-3813-4C58-8FF0-46D25EB3FA91%2FRKNPU2%20%E9%80%9A%E7%94%A8API%E7%9A%84%E4%BD%BF%E7%94%A8%28Main.cc%5C%29%20%2001_resnet18%7CE3A2453E-5393-4DE3-AD83-1BFE8DE440CE%2F%29))
[通用API讲解](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/RKNPU2%20从入门到实践.one#通用API讲解&section-id={641937CE-3813-4C58-8FF0-46D25EB3FA91}&page-id={3AD2663D-0363-4EF6-9BC4-02AE01EB437A}&end)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28RKNPU2%20%E4%BB%8E%E5%85%A5%E9%97%A8%E5%88%B0%E5%AE%9E%E8%B7%B5.one%7C641937CE-3813-4C58-8FF0-46D25EB3FA91%2F%E9%80%9A%E7%94%A8API%E8%AE%B2%E8%A7%A3%7C3AD2663D-0363-4EF6-9BC4-02AE01EB437A%2F%29))

### 补充
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/assets/RKNPU2 从入门到实践/file-20250810171709280.pdf|RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/assets/RKNPU2 从入门到实践/file-20250810171709280.pdf]]
## 2.RKNPU2 零拷贝API的使用
> [!PDF|red] [[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/assets/RKNPU2 从入门到实践/file-20250810171708398.pdf#page=105&selection=0,0,12,4&color=red|NPU开发配套资料-视频教程（总结）, p.105]]
> > 第 7 章 RKNN C API 详细说明


[RKNPU2 零拷贝API使用（Main.cc）](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/RKNPU2%20从入门到实践.one#RKNPU2%20零拷贝API使用（Main.cc）&section-id={641937CE-3813-4C58-8FF0-46D25EB3FA91}&page-id={28F0BC6E-D982-4E2A-B757-830B198FD28F}&end)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28RKNPU2%20%E4%BB%8E%E5%85%A5%E9%97%A8%E5%88%B0%E5%AE%9E%E8%B7%B5.one%7C641937CE-3813-4C58-8FF0-46D25EB3FA91%2FRKNPU2%20%E9%9B%B6%E6%8B%B7%E8%B4%9DAPI%E4%BD%BF%E7%94%A8%EF%BC%88Main.cc%EF%BC%89%7C28F0BC6E-D982-4E2A-B757-830B198FD28F%2F%29))
[10_RKNPU2 零拷贝API讲解](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/RKNPU2%20从入门到实践.one#10_RKNPU2%20零拷贝API讲解&section-id={641937CE-3813-4C58-8FF0-46D25EB3FA91}&page-id={736DDF61-A3E6-45CA-9ACE-5AF769554AB1}&end)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28RKNPU2%20%E4%BB%8E%E5%85%A5%E9%97%A8%E5%88%B0%E5%AE%9E%E8%B7%B5.one%7C641937CE-3813-4C58-8FF0-46D25EB3FA91%2F10_RKNPU2%20%E9%9B%B6%E6%8B%B7%E8%B4%9DAPI%E8%AE%B2%E8%A7%A3%7C736DDF61-A3E6-45CA-9ACE-5AF769554AB1%2F%29))

零拷贝api<span style="background:#affad1">缺少了数据拷贝的过程</span>
<span style="background:#affad1">会减小内存拷贝的花销</span>
<span style="background:#affad1">从而优化程序的运行效果和性能</span>
### 补充
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/assets/RKNPU2 从入门到实践/file-20250810171709327.pdf|RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/assets/RKNPU2 从入门到实践/file-20250810171709327.pdf]]


# 五、itop-3568开发板npu使用手册（未）

- 1 人工智能开发可以参考

## 1、NPU的介绍
> [!PDF|important] [[芯片开发学习/RK3568（linux学习）/linux开发资料库/rk3568迅为开发pdf/8.人工智能开发/13_【北京迅为】itop-3568开发板npu使用手册【底板v1.7版】v1.1.pdf#page=9&selection=64,0,71,3&color=important|13_【北京迅为】itop-3568开发板npu使用手册【底板v1.7版】v1.1, p.9]]
> > 第 1 章你好！NPU
> 
> 


### 


### 


### 


## 2、准备 RKNPU 开发环境
> [!PDF|important] [[芯片开发学习/RK3568（linux学习）/linux开发资料库/rk3568迅为开发pdf/8.人工智能开发/13_【北京迅为】itop-3568开发板npu使用手册【底板v1.7版】v1.1.pdf#page=13&selection=15,0,25,4&color=important|13_【北京迅为】itop-3568开发板npu使用手册【底板v1.7版】v1.1, p.13]]
> > 第 2 章准备 RKNPU 开发环境
> 
> 


### 


### 


### 



## 3、在 Linux 系统中使用 NPU
> [!PDF|important] [[芯片开发学习/RK3568（linux学习）/linux开发资料库/rk3568迅为开发pdf/8.人工智能开发/13_【北京迅为】itop-3568开发板npu使用手册【底板v1.7版】v1.1.pdf#page=16&selection=27,0,35,3&color=important|13_【北京迅为】itop-3568开发板npu使用手册【底板v1.7版】v1.1, p.16]]
> > 3.1 在 Linux 系统中使用 NPU
> 
> 


### 


### 


### 



## 4、在 Android 系统中使用 NPU
> [!PDF|important] [[芯片开发学习/RK3568（linux学习）/linux开发资料库/rk3568迅为开发pdf/8.人工智能开发/13_【北京迅为】itop-3568开发板npu使用手册【底板v1.7版】v1.1.pdf#page=21&selection=38,0,46,3&color=important|13_【北京迅为】itop-3568开发板npu使用手册【底板v1.7版】v1.1, p.21]]
> > 3.2 在 Android 系统中使用 NPU
> 
> 


### 


### 


### 




## 5、体验 RKNN_DEMO
> [!PDF|important] [[芯片开发学习/RK3568（linux学习）/linux开发资料库/rk3568迅为开发pdf/8.人工智能开发/13_【北京迅为】itop-3568开发板npu使用手册【底板v1.7版】v1.1.pdf#page=31&selection=15,0,23,9&color=important|13_【北京迅为】itop-3568开发板npu使用手册【底板v1.7版】v1.1, p.31]]
> > 第 4 章体验 RKNN_DEMO
> 
> 

- 1 在 RKNPU2 工具下面 examples 中有很多例子，本章节我们来体验一下这些程序。本章节测试开发板使用 Android 系统。
### 


### 


### 

## 6、模型转换工具使用
> [!PDF|important] [[芯片开发学习/RK3568（linux学习）/linux开发资料库/rk3568迅为开发pdf/8.人工智能开发/13_【北京迅为】itop-3568开发板npu使用手册【底板v1.7版】v1.1.pdf#page=37&selection=15,0,21,4&color=important|13_【北京迅为】itop-3568开发板npu使用手册【底板v1.7版】v1.1, p.37]]
> > 第 5 章模型转换
> 
> 

- 1 在使用 RKNN SDK 之前，用户需要使用 RKNN-Toolkit2 工具将自主研发的算法模型转换为 RKNN 模型。

### 


### 


### 

## 7、其他模型转换
> [!PDF|important] [[芯片开发学习/RK3568（linux学习）/linux开发资料库/rk3568迅为开发pdf/8.人工智能开发/13_【北京迅为】itop-3568开发板npu使用手册【底板v1.7版】v1.1.pdf#page=54&selection=15,0,21,6&color=important|13_【北京迅为】itop-3568开发板npu使用手册【底板v1.7版】v1.1, p.54]]
> > 第 6 章其他模型转换
> 
> 

- 1 在官方提供的 rknn-toolkit2 工具中，默认自带了很多测试例程和模型，本章节我们测试并运行这些 demo 程序，模型运行在 RK3568 开发板上。
### 


### 


### 


## 8、使用 RKNN-Toolkit-lite2
> [!PDF|important] [[芯片开发学习/RK3568（linux学习）/linux开发资料库/rk3568迅为开发pdf/8.人工智能开发/13_【北京迅为】itop-3568开发板npu使用手册【底板v1.7版】v1.1.pdf#page=70&selection=15,0,23,18&color=important|13_【北京迅为】itop-3568开发板npu使用手册【底板v1.7版】v1.1, p.70]]
> > 第 7 章使用 RKNN-Toolkit-lite2
> 
> 

- 1 只可以在开发板上部署运行 RKNN 模型，不能进行模型转换，如果非 RKNN 模型，请使用 RKNN-Toolkit2 来进行转换。

### 


### 


### 




# 六、itop-3568开发板NPU例程测试手册（未）
## 1、瑞芯微原厂 NPU 资料介绍
> [!PDF|important] [[芯片开发学习/RK3568（linux学习）/linux开发资料库/rk3568迅为开发pdf/8.人工智能开发/【北京迅为】itop-3568开发板NPU例程测试手册V1.0.pdf#page=11&selection=18,0,28,4&color=important|【北京迅为】itop-3568开发板NPU例程测试手册V1.0, p.11]]
> > 第 1 章瑞芯微原厂 NPU 资料介绍
> 
> 

### 


### 


### 


## 2、rknn-toolkit2 环境搭建和使用
> [!PDF|important] [[芯片开发学习/RK3568（linux学习）/linux开发资料库/rk3568迅为开发pdf/8.人工智能开发/【北京迅为】itop-3568开发板NPU例程测试手册V1.0.pdf#page=20&selection=18,0,26,7&color=important|【北京迅为】itop-3568开发板NPU例程测试手册V1.0, p.20]]
> > 第2章 rknn-toolkit2 环境搭建和使用
> 
> 


### 


### 


### 



## 3、rknn-toolkit-lite2 环境搭建和使用
> [!PDF|important] [[芯片开发学习/RK3568（linux学习）/linux开发资料库/rk3568迅为开发pdf/8.人工智能开发/【北京迅为】itop-3568开发板NPU例程测试手册V1.0.pdf#page=37&selection=18,0,28,7&color=important|【北京迅为】itop-3568开发板NPU例程测试手册V1.0, p.37]]
> > 第3章 rknn-toolkit-lite2 环境搭建和使用
> 
> 

### 


### 


### 



## 4、4 、rknpu2 工具套件使用
> [!PDF|important] [[芯片开发学习/RK3568（linux学习）/linux开发资料库/rk3568迅为开发pdf/8.人工智能开发/【北京迅为】itop-3568开发板NPU例程测试手册V1.0.pdf#page=44&selection=18,0,25,2&color=important|【北京迅为】itop-3568开发板NPU例程测试手册V1.0, p.44]]
> > 第4章 rknpu2 工具套件使用
> 
> 

- 1 rknpu2 的 C API 部署和推理进行讲解。迅为有录制 rknpu2 C API 的视频教程，详细的讲解了 rknpu2 各个 API 的使用，具体超链接如下所示

### 


### 


### 




## 5、rknn-model-zoo 例程演示
> [!PDF|important] [[芯片开发学习/RK3568（linux学习）/linux开发资料库/rk3568迅为开发pdf/8.人工智能开发/【北京迅为】itop-3568开发板NPU例程测试手册V1.0.pdf#page=48&selection=18,0,28,3&color=important|【北京迅为】itop-3568开发板NPU例程测试手册V1.0, p.48]]
> > 第5章 rknn-model-zoo 例程演示
> 
> 

- 1 提供了当前主流算法部署到 RK SOC 的例程，包含了模型的转换、模型的 Python api 推理、模型的 C api 推理，rknn-model-zoo 仓库在 1.5 小节已经讲解了获取方法，
### 


### 


### 



## 6、rknn-model-zoo 模型推理测试
> [!PDF|important] [[芯片开发学习/RK3568（linux学习）/linux开发资料库/rk3568迅为开发pdf/8.人工智能开发/【北京迅为】itop-3568开发板NPU例程测试手册V1.0.pdf#page=56&selection=18,0,28,6&color=important|【北京迅为】itop-3568开发板NPU例程测试手册V1.0, p.56]]
> > 第6章 rknn-model-zoo 模型推理测试
> 
> 

- 1 在上一章节中以 deeplabv3 为例进行了 rknn-model-zoo 中例程的演示，而在本章节将对其余剩下的例程进行测试


### 


### 



### 










