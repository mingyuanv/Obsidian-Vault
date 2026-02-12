#!/bin/sh

<span style="background:#b1ffff">嵌入式系统启动初始化：设备管理 → 环境配置 → 网络服务 → 存储管理 → 用户自定义启动</span>
# 核心硬件初始化流程（适用于嵌入式摄像头设备）

# 设备节点管理 --------------------------------------------------
echo /sbin/mdev > /proc/sys/kernel/hotplug  # 启用动态设备节点管理
/sbin/mdev -s && echo "mdev is ok......"     # 扫描/sys生成基础设备节点

# 系统环境配置 --------------------------------------------------
export PATH=/bin:/sbin:/usr/bin:/usr/sbin    # 基础命令路径
export PATH=/system/bin:$PATH                # 添加自定义工具路径
export LD_LIBRARY_PATH=/system/lib           # 指定动态库搜索路径

# 网络基础服务 --------------------------------------------------
ifconfig lo up                               # 启用回环接口
telnetd &                                    # 启动远程登录服务（注意安全风险）

# 视频流优化配置 ------------------------------------------------
sysctl -w net.core.wmem_max=26214400        # 设置最大写缓冲区（25MB）
sysctl -w net.core.wmem_default=26214400    # 默认写缓冲区适配RTSP视频流

# 存储系统初始化 ------------------------------------------------
mount -t jffs2 /dev/mtdblock3 /system       # 挂载闪存分区到/system

# 首次启动格式化流程（典型日志）---------------------------------
if [ ! -f /system/.system ]; then
    echo "Formatting system partition..."   # 擦除闪存分区日志示例：
    umount -f /system                       # [ 3.215558] jffs2: Erase block 128 at 0x01000000
    flash_eraseall /dev/mtd3                # [ 3.225671] mtd: erasing block at 0x0
    mount -t jffs2 /dev/mtdblock3 /system   # 重新挂载后创建目录结构
    cd /system && mkdir -p bin init etc/sensor lib/firmware lib/modules
    echo "#!/bin/sh" > init/app_init.sh     # 生成初始化脚本模板
    chmod 755 init/app_init.sh              # 设置可执行权限（drwxr-xr-x）
    touch .system                           # 创建初始化标记文件
    cd / && echo "Done"                     # 日志输出：Done
fi

# 关键硬件驱动加载（需注意顺序）---------------------------------
insmod /opt/drivers/tx-isp-t32.ko isp_clk=200000000   # 加载ISP驱动（设置200MHz时钟）
insmod /opt/drivers/sensor_gc2053_t32.ko              # 加载GC2053图像传感器驱动
insmod /opt/drivers/audio.ko spk_gpio=-1               # 加载音频驱动（需检查路径是否缺少/开头）

# 用户自定义初始化 ----------------------------------------------
[ -f /system/init/app_init.sh ] && /system/init/app_init.sh &  # 后台执行自定义脚本