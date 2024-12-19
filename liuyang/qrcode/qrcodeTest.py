import base64
import qrcode
from io import BytesIO


def file_to_base64_chunks(file_path, chunk_size=2000):
    # 读取文件的二进制数据
    with open(file_path, 'rb') as f:
        binary_data = f.read()

    # 将二进制数据转换为Base64编码的字符串
    base64_data = base64.b64encode(binary_data).decode('utf-8')

    print("11111")
    print(base64_data)
    # 分块处理
    chunks = [base64_data[i:i + chunk_size] for i in range(0, len(base64_data), chunk_size)]
    return chunks


def generate_qr_code(data, output_file):
    # 创建QRCode对象
    qr = qrcode.QRCode(
        version=None,  # 自动确定版本
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # 添加数据到QRCode对象
    qr.add_data(data)
    qr.make(fit=True)

    # 创建QR码图像
    img = qr.make_image(fill_color="black", back_color="white")

    # 保存图像
    img.save(output_file)


# 主函数
if __name__ == "__main__":
    # 文件路径
    file_path = 'pingan.zip'  # 请替换为你实际的文件路径

    # 输出的二维码图片路径前缀
    output_prefix = 'qr_code_'

    # 获取Base64字符串分块
    base64_chunks = file_to_base64_chunks(file_path)

    # 生成二维码
    for i, chunk in enumerate(base64_chunks):
        output_file = f"{output_prefix}{i + 1}.png"
        generate_qr_code(chunk, output_file)
        print(f"二维码已生成，并保存为 {output_file}")