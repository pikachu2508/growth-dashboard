import os
from PIL import Image, ImageOps
from pillow_heif import register_heif_opener

# 注册HEIF支持
register_heif_opener()

def process_images_for_wechat(folder_path):
    # 确保路径存在
    if not os.path.exists(folder_path):
        print(f"❌ 错误：找不到文件夹 {folder_path}")
        return

    print(f"📂 正在为微信朋友圈优化图片：{folder_path} ...")
    count = 0
    
    # 微信朋友圈建议最大分辨率（长边不超过 2560px 既能保证清晰度又能避免上传失败）
    MAX_SIZE = 2560

    for filename in os.listdir(folder_path):
        # 处理 heic 和 jpg
        if filename.lower().endswith((".heic", ".jpg", ".jpeg", ".png")):
            file_path = os.path.join(folder_path, filename)
            
            # 生成新的文件名，避免覆盖原图（加上 _wx 后缀）
            name, ext = os.path.splitext(filename)
            if name.endswith("_wx"): # 避免重复处理
                continue
                
            new_filename = f"{name}_wx.jpg"
            new_path = os.path.join(folder_path, new_filename)
            
            # 如果目标文件已存在，跳过
            if os.path.exists(new_path):
                continue

            try:
                with Image.open(file_path) as img:
                    # 1. 自动旋转（根据Exif）
                    img = ImageOps.exif_transpose(img)
                    
                    # 2. 转换颜色空间为 sRGB (微信最喜欢的格式)
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # 3. 调整尺寸 (Downsample)
                    # 如果图片太大 (比如 iPhone 4800w 像素)，微信电脑版会崩溃
                    width, height = img.size
                    max_dim = max(width, height)
                    
                    if max_dim > MAX_SIZE:
                        scale = MAX_SIZE / max_dim
                        new_width = int(width * scale)
                        new_height = int(height * scale)
                        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                        print(f"📉 缩放: {filename} ({width}x{height} -> {new_width}x{new_height})")
                    
                    # 4. 保存为标准 JPEG
                    # quality=85 是朋友圈画质平衡点，exif=b"" 去除所有元数据避免兼容问题
                    img.save(new_path, "JPEG", quality=88, optimize=True, exif=b"")
                    print(f"✅ 优化成功: {new_filename}")
                    count += 1
                    
            except Exception as e:
                print(f"❌ 处理失败 {filename}: {str(e)}")

    if count == 0:
        print("\n🎉 没有发现需要处理的新图片。")
    else:
        print(f"\n✨ 处理完成！请使用以 '_wx.jpg' 结尾的图片发朋友圈。")

if __name__ == "__main__":
    target_folder = r"..\40_个人作品_VLOG支教日记\02_Ep2_人设_我是皮卡丘"
    process_images_for_wechat(target_folder)
