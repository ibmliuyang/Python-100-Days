import base64


class Base64Tool:
    @staticmethod
    def encode(data: str) -> str:
        """
        将字符串数据进行 Base64 编码。

        :param data: 需要编码的字符串。
        :return: 编码后的 Base64 字符串。
        """
        # 将字符串转换为字节串
        data_bytes = data.encode('utf-8')
        # 进行 Base64 编码
        encoded_data = base64.b64encode(data_bytes)
        # 返回编码后的字符串
        return encoded_data.decode('utf-8')

    @staticmethod
    def decode(encoded_data: str) -> str:
        """
        将 Base64 编码的字符串进行解码。

        :param encoded_data: 需要解码的 Base64 字符串。
        :return: 解码后的原始字符串。
        """
        # 将字符串转换为字节串
        encoded_data_bytes = encoded_data.encode('utf-8')
        # 进行 Base64 解码
        decoded_data = base64.b64decode(encoded_data_bytes)
        # 返回解码后的字符串
        return decoded_data.decode('utf-8')


# 示例用法
if __name__ == '__main__':
    encoded_data = "eyJzYnV1aWQiOiI3QjRCMzFBOEJBMkE0RUE1RjQ1NUEwMDM5M0QzM0E2QyIsInNrc3NxcSI6IjIwMjMtMTAtMDEiLCJkanhoIjoiMTAyMTUxMTUwMDAwMDAwMzIwNzYiLCJ6Znl5IjoiIiwienN4bURtIjoiMTAxMDQiLCJ5enB6emxEbSI6IkJEQTA2MTExNTkiLCJwenhoIjoiMTAwMTUxMjQwMDAwMDgwMTAyOTYiLCJza3NzcXoiOiIyMDIzLTEyLTMxIn0="
   # encoded_data = Base64Tool.encode(original_data)
    print(f"Encoded Data: {encoded_data}")

    decoded_data = Base64Tool.decode(encoded_data)
    print(f"Decoded Data: {decoded_data}")