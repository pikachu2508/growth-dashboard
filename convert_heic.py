import os
from PIL import Image
from pillow_heif import register_heif_opener

# 注册HEIF支持
register_heif_opener()

def convert_heic_to_jpg(folder_path):
    # 确保路径存在
    if not os.path.exists(folder_path):
        print(f"❌ 错误：找不到文件夹 {folder_path}")
        return

    # 遍历文件夹
    count = 0
    print(f"📂 正在扫描文件夹：{folder_path} ...")
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".heic"):
            heic_path = os.path.join(folder_path, filename)
            jpg_filename = os.path.splitext(filename)[0] + ".jpg"
            jpg_path = os.path.join(folder_path, jpg_filename)
            
            # 如果jpg已存在，跳过
            if os.path.exists(jpg_path):
                print(f"⚠️ 跳过（已存在）：{jpg_filename}")
                continue
                
            try:
                # 打开并转换
                image = Image.open(heic_path)
                # 转换颜色模式（HEIC可能是CMYK或其它，JPG需要RGB）
                image = image.convert('RGB')
                image.save(jpg_path, "JPEG", quality=95)
                print(f"✅ 成功转换：{filename} -> {jpg_filename}")
                count += 1
            except Exception as e:
                print(f"❌ 转换失败 {filename}: {str(e)}")

    if count == 0:
        print("\n🎉 没有发现需要转换的 HEIC 文件。")
    else:
        print(f"\n✨ 大功告成！共转换了 {count} 张图片。")

if __name__ == "__main__":
    # 默认转换 "02_Ep2_人设_我是皮卡丘" 文件夹，因为用户刚把图片放进去
    target_folder = r"..\40_个人作品_VLOG支教日记\02_Ep2_人设_我是皮卡丘"
    
    # 也可以让用户输入路径
    # target_folder = input("请输入包含HEIC图片的文件夹路径: ")
    
    convert_heic_to_jpg(target_folder)
