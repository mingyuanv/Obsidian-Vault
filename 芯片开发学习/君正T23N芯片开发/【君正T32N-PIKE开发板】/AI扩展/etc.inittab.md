```sh
# /etc/inittab - BusyBox初始化系统配置文件
# 注意：BusyBox init不支持运行级别（runlevels字段无意义）

# 系统初始化阶段 ----------------------------------------------

# 关闭所有交换分区（嵌入式系统通常不需要swap）
::sysinit:/sbin/swapoff -a

# 创建动态设备节点目录（使用tmpfs内存文件系统加速设备访问）
::sysinit:/bin/mount -t tmpfs tmpfs /dev

# 创建伪终端和共享内存目录（为后续服务提供基础支持）
::sysinit:/bin/mkdir -p /dev/pts    # 伪终端设备节点
::sysinit:/bin/mkdir -p /dev/shm    # POSIX共享内存目录

# 挂载/etc/fstab中定义的所有文件系统（如/proc /sys等）
::sysinit:/bin/mount -a

# 从/etc/hostname文件设置系统主机名
::sysinit:/bin/hostname -F /etc/hostname


# 启动系统初始化脚本 ------------------------------------------
# 执行/etc/init.d/rcS脚本（用户自定义启动脚本入口）
::sysinit:/etc/init.d/rcS


# 终端配置 ----------------------------------------------------
# 在串口控制台启动登录终端（respawn表示崩溃后自动重启）
# -L参数强制将console视为本地终端
# 115200为波特率，vt100指定终端仿真类型
console::respawn:/sbin/getty -L console 115200 vt100


# 高级功能（当前禁用）-----------------------------------------
# 三指礼帽快捷键（Ctrl+Alt+Del）默认行为
#::ctrlaltdel:/sbin/reboot

# 系统关闭时操作：卸载所有文件系统（-r表示若卸载失败则重新挂载为只读）
::shutdown:/bin/umount -a -r
```

**关键配置说明**：
1. **动作类型解析**：
   - `sysinit`：系统初始化阶段执行（仅执行一次）
   - `respawn`：进程终止后自动重启（用于关键服务）
   - `shutdown`：系统关机时执行

2. **典型启动流程**：
   ```mermaid
   graph TD
     A[关闭swap] --> B[挂载/dev]
     B --> C[创建设备目录]
     C --> D[挂载全部文件系统]
     D --> E[设置主机名]
     E --> F[执行rcS脚本]
     F --> G[启动控制台终端]
   ```

3. **安全增强建议**：
   - 建议注释`::shutdown:/bin/umount -a -r`修改为：
     ```sh
     ::shutdown:/bin/umount -a -r -t no,nfs  # 排除网络文件系统
     ```
   - 生产环境应移除`console::respawn`的`-L`参数，改用：
     ```sh
     console::respawn:/sbin/getty 115200 vt100
     ```

4. **扩展配置示例**：
   ```sh
   # 增加USB串口终端（适用于多调试接口设备）
   ttyUSB0::respawn:/sbin/getty -L ttyUSB0 115200 vt100
   # 看门狗保活监控（每5秒喂狗）
   ::respawn:/sbin/watchdog -T 5 /dev/watchdog
   ```

需要更详细的配置说明或安全加固建议可以随时告诉我！