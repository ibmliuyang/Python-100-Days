from PIL import Image, ImageDraw, ImageFont

# 创建一张宽度为400像素，高度为300像素，背景为白色的空白图片
img = Image.new('RGB', (400, 300), color='white')

# 获取一个可以在图片上绘制文本的对象
draw = ImageDraw.Draw(img)

# 在图片上添加文本
text = "Hello, World!"
font = ImageFont.truetype("arial.ttf", 36)
draw.text((10, 10), text, font=font, fill=(0, 0, 0))

# 显示图片
img.show()
