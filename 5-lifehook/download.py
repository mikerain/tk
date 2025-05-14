import requests
import sys

def download_image(url, save_path):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        content_type = response.headers.get('Content-Type', '')
        #if content_type in ['image/jpeg', 'image/png']:
        #    with open(save_path, 'wb') as f:
        #        f.write(response.content)
        #    print(f"图片已保存到：{save_path}")
        #else:
        #    print(f"不支持的 Content-Type: {content_type}")
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"图片已保存到：{save_path}")
    except requests.exceptions.RequestException as e:
        print(f"下载失败: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python download_image.py <url> <save_path>")
        sys.exit(1)

    url = sys.argv[1]
    save_path = sys.argv[2]

    download_image(url, save_path)

