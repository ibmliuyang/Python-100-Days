import os
import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple


def extract_api_path(config_content: str) -> Optional[str]:
    """从config.js内容中提取apiPath的值"""
    # 匹配export const apiPath = 'xxx'格式
    match = re.search(r"export\s+const\s+apiPath\s*=\s*['\"]([^'\"]+)['\"]", config_content)
    if match:
        return match.group(1)
    return None


def extract_urls(service_content: str, api_path: Optional[str]) -> List[str]:
    """从services.js内容中提取url的值，并处理与apiPath的拼接"""
    urls = []
    # 匹配url: 'xxx'格式
    url_matches = re.finditer(r"url\s*:\s*['\"`]([^'\"`]+)['\"`]", service_content)

    for match in url_matches:
        url = match.group(1)
        # 处理可能的模板字符串拼接
        if api_path and '${apiPath}' in url:
            url = url.replace('${apiPath}', api_path)
        urls.append(url)

    return urls


def process_directory(root_dir: str) -> Dict[str, Any]:
    """处理目录并提取API信息"""
    result = {}

    # 遍历所有子目录
    for dirpath, dirnames, filenames in os.walk(root_dir):
        config_path = os.path.join(dirpath, 'config.js')
        service_path = os.path.join(dirpath, 'services.js')

        # 检查目录下是否同时存在config.js和services.js
        if os.path.exists(config_path) and os.path.exists(service_path):
            # 读取config.js内容
            with open(config_path, 'r', encoding='utf-8') as f:
                config_content = f.read()

            # 提取apiPath
            api_path = extract_api_path(config_content)

            # 读取services.js内容
            with open(service_path, 'r', encoding='utf-8') as f:
                service_content = f.read()

            # 提取urls
            urls = extract_urls(service_content, api_path)

            # 计算相对路径作为key
            relative_path = os.path.relpath(dirpath, root_dir)
            result[relative_path] = {
                'apiPath': api_path,
                'urls': urls
            }

    return result


def main():
    """主函数，处理命令行参数并输出结果"""
    import argparse

    parser = argparse.ArgumentParser(description='提取前端项目中的API路径信息')
    parser.add_argument('--input', '-i', required=True, help='输入目录路径')
    parser.add_argument('--output', '-o', help='输出JSON文件路径')
    parser.add_argument('--pretty', '-p', action='store_true', help='美化输出JSON')

    args = parser.parse_args()

    # 处理目录
    result = process_directory(args.input)

    # 输出结果
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            if args.pretty:
                json.dump(result, f, ensure_ascii=False, indent=2)
            else:
                json.dump(result, f, ensure_ascii=False)
        print(f"结果已保存到 {args.output}")
    else:
        if args.pretty:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()