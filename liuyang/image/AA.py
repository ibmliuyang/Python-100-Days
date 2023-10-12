from PIL import Image


def Image():
    # 待处理图片存储路径
    import PIL
    img = PIL.Image.open('/Users/ly/Downloads/1.jpg')
    # Resize图片大小，入口参数为一个tuple，新的图片大小
    img = img.resize((600, 800))

    # 处理后的图片的存储路径，以及存储格式
    img.save('C:/Users/KerryChen/Desktop/222.jpg', dpi=(300, 300))


if __name__ == "__main__":
    Image()
