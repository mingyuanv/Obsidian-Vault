[[芯片开发学习/RK3568（linux学习）/小项目/基于rk3568的智能家居项目/基于rk3568完成智能家居项目#2.buildroot文件系统]]
# 备注：


# 1.buildroot文件系统  
[1.buildroot文件系统下的目录解析](onenote:https://d.docs.live.net/52D4B76BB0FFCF51/Documents/嵌入式Linux驱动/@智能家居项目.one#1.buildroot文件系统下的目录解析&section-id={4C75FDDB-412B-4A23-BC4B-2C3C1569577B}&page-id={5A4465FA-AA00-4362-8C71-F2DD91390618}&end)


## 2.1 配置buildroot开发环境
[配置buildroot开发环境](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/文件系统构建_基于RK3568.one#08-使用buildroot构建文件系统-以RK3568为例&section-id={D274A68A-A696-4F4A-B6FE-98047B597794}&page-id={2B066D02-3D4E-410B-B78F-B0F61C37D1E7}&object-id={0A0F4B9E-AF17-407F-967C-60F62DAA52A9}&1D)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E6%9E%84%E5%BB%BA_%E5%9F%BA%E4%BA%8ERK3568.one%7CD274A68A-A696-4F4A-B6FE-98047B597794%2F08-%E4%BD%BF%E7%94%A8buildroot%E6%9E%84%E5%BB%BA%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F-%E4%BB%A5RK3568%E4%B8%BA%E4%BE%8B%7C2B066D02-3D4E-410B-B78F-B0F61C37D1E7%2F%29))

## 2.2 移植QT
[09-给buildroot文件系统增加QT库功能](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/文件系统构建_基于RK3568.one#09-给buildroot文件系统增加QT库功能&section-id={D274A68A-A696-4F4A-B6FE-98047B597794}&page-id={B67816DA-A7F0-40F7-A968-AD5C840DBAC9}&end)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E6%9E%84%E5%BB%BA_%E5%9F%BA%E4%BA%8ERK3568.one%7CD274A68A-A696-4F4A-B6FE-98047B597794%2F09-%E7%BB%99buildroot%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E5%A2%9E%E5%8A%A0QT%E5%BA%93%E5%8A%9F%E8%83%BD%7CB67816DA-A7F0-40F7-A968-AD5C840DBAC9%2F%29))

## 2.3 移植SSH
[移植SSH](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/文件系统构建_基于RK3568.one#08-使用buildroot构建文件系统-以RK3568为例&section-id={D274A68A-A696-4F4A-B6FE-98047B597794}&page-id={2B066D02-3D4E-410B-B78F-B0F61C37D1E7}&object-id={0A0F4B9E-AF17-407F-967C-60F62DAA52A9}&A)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E6%9E%84%E5%BB%BA_%E5%9F%BA%E4%BA%8ERK3568.one%7CD274A68A-A696-4F4A-B6FE-98047B597794%2F08-%E4%BD%BF%E7%94%A8buildroot%E6%9E%84%E5%BB%BA%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F-%E4%BB%A5RK3568%E4%B8%BA%E4%BE%8B%7C2B066D02-3D4E-410B-B78F-B0F61C37D1E7%2F%29))

## 2.3 配置buzybox
[在buildroot中配置buzybox的内容](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/文件系统构建_基于RK3568.one#08-使用buildroot构建文件系统-以RK3568为例&section-id={D274A68A-A696-4F4A-B6FE-98047B597794}&page-id={2B066D02-3D4E-410B-B78F-B0F61C37D1E7}&object-id={0A0F4B9E-AF17-407F-967C-60F62DAA52A9}&31)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E6%9E%84%E5%BB%BA_%E5%9F%BA%E4%BA%8ERK3568.one%7CD274A68A-A696-4F4A-B6FE-98047B597794%2F08-%E4%BD%BF%E7%94%A8buildroot%E6%9E%84%E5%BB%BA%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F-%E4%BB%A5RK3568%E4%B8%BA%E4%BE%8B%7C2B066D02-3D4E-410B-B78F-B0F61C37D1E7%2F%29))



# 2、手册指导

## Buildroot 系统构建
> [!PDF|important] [[芯片开发学习/RK3568（linux学习）/linux开发资料库/rk3568迅为开发pdf/16.开发板学习教程/文件系统构建手册_rk3568_v1.1.pdf#page=66&selection=17,1,25,4&color=important|文件系统构建手册_rk3568_v1.1, p.66]]
> >  5 章 Buildroot 系统构建
> 
> 












