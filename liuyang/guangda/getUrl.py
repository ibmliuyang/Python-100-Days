import os
import re
import json
from typing import Dict, List, Optional, Any

# 配置参数
INPUT_DIR = '/Users/ly/VSCodeWorkspace/taxmpv5-front-iinv/src/pages/iinv/views'
OUTPUT_FILE = 'api_full_paths.json'
PRETTY_PRINT = True


def extract_path(config_content: str) -> Optional[str]:
    """从config.js内容中提取path的值"""
    # 匹配export const path = 'xxx'、"xxx"或`xxx`格式，支持分号结尾
    pattern = r"export\s+const\s+path\s*=\s*(['\"`])(.+?)\1\s*;?"
    match = re.search(pattern, config_content)
    if match:
        return match.group(2)
    return None


def extract_api_path(config_content: str) -> Optional[str]:
    """从config.js内容中提取apiPath的值"""
    pattern = r"export\s+const\s+apiPath\s*=\s*(['\"`])(.+?)\1\s*;?"
    match = re.search(pattern, config_content)
    if match:
        return match.group(2)
    return None


def extract_urls(service_content: str, api_path: Optional[str]) -> List[str]:
    """从services.js内容中提取url的值，并处理与apiPath的拼接"""
    urls = []
    url_pattern = r"url\s*:\s*(['\"`])(.+?)\1\s*;?"
    url_matches = re.finditer(url_pattern, service_content)

    for match in url_matches:
        url = match.group(2)
        if api_path and '${apiPath}' in url:
            url = url.replace('${apiPath}', api_path)
        urls.append(url)

    return urls


def process_directory(root_dir: str) -> Dict[str, Dict]:
    """处理目录并提取API信息，使用config.js中的path作为键"""
    result = {}

    for dirpath, _, filenames in os.walk(root_dir):
        if 'config.js' in filenames and 'services.js' in filenames:
            config_path = os.path.join(dirpath, 'config.js')
            service_path = os.path.join(dirpath, 'services.js')

            try:
                # 读取config.js内容
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_content = f.read()

                # 提取path作为键
                path_key = extract_path(config_content)
                if not path_key:
                    # 如果没找到path，则使用文件夹名
                    path_key = os.path.basename(dirpath)
                    print(f"警告: {config_path} 中未找到path，使用文件夹名 {path_key} 作为键")

                # 提取apiPath
                api_path = extract_api_path(config_content)

                # 读取services.js内容
                with open(service_path, 'r', encoding='utf-8') as f:
                    service_content = f.read()

                # 提取urls
                urls = extract_urls(service_content, api_path)

                result[path_key] = {
                    'apiPath': api_path,
                    'urls': urls
                }
            except Exception as e:
                print(f"处理目录 {dirpath} 时出错: {str(e)}")

    return result


def join_api_paths(data: Dict[str, Any]) -> Dict[str, List[str]]:
    """将apiPath和对应的urls进行拼接"""
    result = {}

    for path_key, info in data.items():
        api_path = info.get('apiPath')
        urls = info.get('urls', [])
        full_urls = []

        if not api_path:
            full_urls = urls
        else:
            for url in urls:
                if url.startswith('/'):
                    full_urls.append(f"{api_path}{url}")
                elif '${apiPath}' in url:
                    full_urls.append(url)
                else:
                    full_urls.append(f"{api_path}/{url}")

        result[path_key] = full_urls

    return result


def main():
    """主函数，处理前端工程目录并输出拼接后的API路径"""
    print(f"正在处理目录: {INPUT_DIR}")

    # 步骤1: 提取API信息，使用config.js中的path作为键
    api_data = process_directory(INPUT_DIR)

    # 步骤2: 拼接API路径
    full_paths = join_api_paths(api_data)

    # 输出结果
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        if PRETTY_PRINT:
            json.dump(full_paths, f, ensure_ascii=False, indent=2)
        else:
            json.dump(full_paths, f, ensure_ascii=False)

    print(f"路径提取和拼接完成，结果已保存到 {OUTPUT_FILE}")

    # 打印示例结果
    print("\n示例拼接结果:")
    printed_modules = 0
    for path_key, urls in full_paths.items():
        if not urls:
            continue

        print(f"\n模块路径: {path_key}")
        for url in urls[:3]:
            print(f"  - {url}")
        if len(urls) > 3:
            print("  ...")

        printed_modules += 1
        if printed_modules >= 3:
            break


if __name__ == "__main__":
    main()