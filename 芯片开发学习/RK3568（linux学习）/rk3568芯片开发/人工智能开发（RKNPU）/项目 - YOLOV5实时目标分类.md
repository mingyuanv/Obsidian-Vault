[YOLOV5实时目标分类](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/嵌入式Linux驱动/YOLOV5实时目标分类.one#section-id={96320DC4-AAFD-4A8E-8909-BF47BCB299C2}&end)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21s4d775f5c20a844779602ca7edfa39f6a&id=documents&wd=target%28YOLOV5%E5%AE%9E%E6%97%B6%E7%9B%AE%E6%A0%87%E5%88%86%E7%B1%BB.one%7C96320DC4-AAFD-4A8E-8909-BF47BCB299C2%2F%29))
# 备注:
<span style="background:#affad1">多线程python代码,自己将其适配到RK3568开发板</span>。
多线程c代码，官方提供的只有3588，3568的话有点难搞，后面再看吧。
# 一、环境配置
[1.环境配置(RKNN Toolkit lite2)](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/嵌入式Linux驱动/YOLOV5实时目标分类.one#1.环境配置\(RKNN%20Toolkit%20lite2\)&section-id={96320DC4-AAFD-4A8E-8909-BF47BCB299C2}&page-id={67F23926-2BC4-41D0-8E32-D88A66B4E254}&end)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21s4d775f5c20a844779602ca7edfa39f6a&id=documents&wd=target%28YOLOV5%E5%AE%9E%E6%97%B6%E7%9B%AE%E6%A0%87%E5%88%86%E7%B1%BB.one%7C96320DC4-AAFD-4A8E-8909-BF47BCB299C2%2F1.%E7%8E%AF%E5%A2%83%E9%85%8D%E7%BD%AE%28RKNN%20Toolkit%20lite2%5C%29%7C67F23926-2BC4-41D0-8E32-D88A66B4E254%2F%29))

[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/RKNPU2 从入门到实践#2.开发板上RKNN Toolkit lite2部署(python接口)]]
[[芯片开发学习/RK3568（linux学习）/rk3568芯片开发/人工智能开发（RKNPU）/RKNPU2 从入门到实践#1.RKNN Toolkit2 环境搭建(python接口)(ubuntu20)]]

[2.配置摄像头](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/嵌入式Linux驱动/YOLOV5实时目标分类.one#2.配置摄像头&section-id={96320DC4-AAFD-4A8E-8909-BF47BCB299C2}&page-id={2FDDBD64-DEF0-4AA5-A99C-A7D6871A1E9E}&end)   ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21s4d775f5c20a844779602ca7edfa39f6a&id=documents&wd=target%28YOLOV5%E5%AE%9E%E6%97%B6%E7%9B%AE%E6%A0%87%E5%88%86%E7%B1%BB.one%7C96320DC4-AAFD-4A8E-8909-BF47BCB299C2%2F2.%E9%85%8D%E7%BD%AE%E6%91%84%E5%83%8F%E5%A4%B4%7C2FDDBD64-DEF0-4AA5-A99C-A7D6871A1E9E%2F%29))
# 二、测试各功能模块 

[4.各个模块的功能介绍 .py](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/嵌入式Linux驱动/YOLOV5实时目标分类.one#4.各个模块的功能介绍%20.py&section-id={96320DC4-AAFD-4A8E-8909-BF47BCB299C2}&page-id={ADAD98C4-5537-4962-92DB-8956078D5ED4}&end)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21s4d775f5c20a844779602ca7edfa39f6a&id=documents&wd=target%28YOLOV5%E5%AE%9E%E6%97%B6%E7%9B%AE%E6%A0%87%E5%88%86%E7%B1%BB.one%7C96320DC4-AAFD-4A8E-8909-BF47BCB299C2%2F4.%E5%90%84%E4%B8%AA%E6%A8%A1%E5%9D%97%E7%9A%84%E5%8A%9F%E8%83%BD%E4%BB%8B%E7%BB%8D%20.py%7CADAD98C4-5537-4962-92DB-8956078D5ED4%2F%29))

# 三、优化模型
[3.固定cpu和npu的频率从而提高性能](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/嵌入式Linux驱动/YOLOV5实时目标分类.one#3.固定cpu和npu的频率从而提高性能&section-id={96320DC4-AAFD-4A8E-8909-BF47BCB299C2}&page-id={21462E84-F2E9-4EC1-8870-D7CE6C0F3257}&end)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21s4d775f5c20a844779602ca7edfa39f6a&id=documents&wd=target%28YOLOV5%E5%AE%9E%E6%97%B6%E7%9B%AE%E6%A0%87%E5%88%86%E7%B1%BB.one%7C96320DC4-AAFD-4A8E-8909-BF47BCB299C2%2F3.%E5%9B%BA%E5%AE%9Acpu%E5%92%8Cnpu%E7%9A%84%E9%A2%91%E7%8E%87%E4%BB%8E%E8%80%8C%E6%8F%90%E9%AB%98%E6%80%A7%E8%83%BD%7C21462E84-F2E9-4EC1-8870-D7CE6C0F3257%2F%29))

[5.通过多线程优化识别帧数](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/嵌入式Linux驱动/YOLOV5实时目标分类.one#5.通过多线程优化识别帧数&section-id={96320DC4-AAFD-4A8E-8909-BF47BCB299C2}&page-id={D7B4BCBA-66A7-468A-8BC8-7C3E12370C71}&end)   ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21s4d775f5c20a844779602ca7edfa39f6a&id=documents&wd=target%28YOLOV5%E5%AE%9E%E6%97%B6%E7%9B%AE%E6%A0%87%E5%88%86%E7%B1%BB.one%7C96320DC4-AAFD-4A8E-8909-BF47BCB299C2%2F5.%E9%80%9A%E8%BF%87%E5%A4%9A%E7%BA%BF%E7%A8%8B%E4%BC%98%E5%8C%96%E8%AF%86%E5%88%AB%E5%B8%A7%E6%95%B0%7CD7B4BCBA-66A7-468A-8BC8-7C3E12370C71%2F%29))



















