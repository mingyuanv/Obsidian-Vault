在君正T23平台上使用BusyBox同时制作Squashfs和Jffs2文件系统，可通过以下步骤实现：

---

### **一、准备工作**
#### 1. 确保工具链包含以下组件：
```bash
# 检查BusyBox是否包含所需工具
busybox | grep -E 'mksquashfs|mkfs.jffs2'
# 应输出：
# mksquashfs
# mkfs.jffs2
```

#### 2. 准备文件系统目录结构：
```bash
mkdir -p rootfs/{squashfs,jffs2}/bin
# 将只读文件放入squashfs目录
cp -a /path/to/readonly_files/* rootfs/squashfs/
# 将需要读写的文件放入jffs2目录
cp -a /path/to/writable_files/* rootfs/jffs2/


```

<span style="background:#b1ffff"> -a 参数表示归档模式，保持文件属性等信息不变。</span>

---

### **二、制作Squashfs文件系统**
#### 1. 使用BusyBox生成Squashfs镜像：
```bash
busybox mksquashfs rootfs/squashfs/ rootfs.squashfs \
  -comp xz \                  # 使用XZ压缩算法
  -b 64K \                    # 块大小对齐NorFlash擦除块
  -noappend \                 # 禁止追加写入
  -all-root                   # 统一文件所有权
```

#### 2. 验证Squashfs镜像：
```bash
unsquashfs -lls rootfs.squashfs
```

---

### **三、制作JFFS2文件系统**
#### 1. 生成JFFS2镜像：
```bash
busybox mkfs.jffs2 \
  -d rootfs/jffs2/ \          # 输入目录
  -o rootfs.jffs2 \           # 输出文件
  -e 64KiB \                  # 擦除块大小（需与Flash规格匹配）
  -n \                        # 不添加干净标记
  -l \                        # 小端模式（MIPS架构需要）
  -X zlib \                   # 压缩方式
  -r                          # 保留文件权限
```

#### 2. 验证JFFS2镜像：
```bash
jffs2dump -c rootfs.jffs2 | head -n 20
```

---

### **四、整合到存储布局**
#### 1. NorFlash典型分区方案：
| 分区名   | 起始地址 | 大小    | 内容          |
|---------|----------|--------|---------------|
| uboot   | 0x000000 | 256KB  | Bootloader    |
| kernel  | 0x040000 | 2MB    | Linux内核     |
| squashfs| 0x240000 | 4MB    | Squashfs镜像  |
| jffs2   | 0x640000 | 剩余空间| JFFS2文件系统 |

#### 2. 使用`dd`合并镜像：
```bash
# 创建空镜像文件（假设总大小16MB）
dd if=/dev/zero of=full_image.bin bs=1M count=16

# 写入各分区
dd if=u-boot.bin of=full_image.bin conv=notrunc
dd if=uImage of=full_image.bin bs=1M seek=1 conv=notrunc
dd if=rootfs.squashfs of=full_image.bin bs=1M seek=4 conv=notrunc
dd if=rootfs.jffs2 of=full_image.bin bs=1M seek=8 conv=notrunc
```

---

### **五、烧录与挂载**
#### 1. 通过U-Boot烧录：
```bash
# 在U-Boot命令行中执行
tftp 0x82000000 full_image.bin
sf probe 0
sf erase 0x0 0x1000000       # 擦除16MB区域
sf write 0x82000000 0x0 0x1000000
```

#### 2. 系统启动后挂载：
```bash
# 挂载Squashfs（只读）
mount -t squashfs /dev/mtdblock2 /mnt/squash

# 挂载JFFS2（可读写）
mount -t jffs2 /dev/mtdblock3 /mnt/jffs
```

---

### **六、常见问题解决**
#### 1. **权限问题**：
```bash
# JFFS2挂载时添加权限选项
mount -t jffs2 -o rw,noatime /dev/mtdblock3 /mnt/jffs
```

#### 2. **空间不足**：
```bash
# 检查分区大小
cat /proc/mtd
# 调整mksquashfs参数减少体积：
busybox mksquashfs ... -Xcompression-level 9 -no-recovery
```

#### 3. **启动失败**：
```bash
# 检查U-Boot环境变量
printenv bootargs
# 应包含：
# root=/dev/mtdblock3 rootfstype=squashfs
```

---

### **七、性能优化建议**
1. **Squashfs优化**：
   ```bash
   # 使用ZSTD压缩（需内核支持）
   busybox mksquashfs ... -comp zstd -Xcompression-level 12
   ```

2. **JFFS2优化**：
   ```bash
   # 启用压缩和SUM功能
   busybox mkfs.jffs2 ... -X lzo -s 2048
   ```

3. **Flash参数调优**：
   ```bash
   # 在U-Boot中设置SPI时钟
   sf probe 0 30000000  # 30MHz时钟
   ```

通过以上步骤，可在君正T23平台上高效集成Squashfs和JFFS2文件系统。实际使用时需根据Flash型号（如Winbond W25Q128）调整擦除块大小等参数。




