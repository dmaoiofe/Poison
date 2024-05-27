import requests
import pandas as pd
import time

def fetch_comments(song_id, page, limit=20):
    url = f'http://music.163.com/api/v1/resource/comments/R_SO_4_{4172700}?limit={limit}&offset={page*limit}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data['comments']

def parse_comments(comments):
    comments_list = []
    for comment in comments:
        comment_info = {
            'user_id': comment['user']['userId'],
            'nickname': comment['user']['nickname'],
            'comment_id': comment['commentId'],
            'content': comment['content'],
            'time': pd.to_datetime(comment['time'], unit='ms')
        }
        comments_list.append(comment_info)
    return comments_list

def main(song_id, max_pages):
    all_comments = []
    for page in range(max_pages):
        try:
            comments = fetch_comments(song_id, page)
            if not comments:
                break
            comments_list = parse_comments(comments)
            all_comments.extend(comments_list)
            print(f'Fetched page {page + 1}')
            time.sleep(1)  # 添加延迟以避免被封禁
        except Exception as e:
            print(f'Error fetching page {page + 1}: {e}')
            break
    
    df = pd.DataFrame(all_comments)
    df.to_csv('comments.csv', index=False, encoding='utf-8-sig')
    print('评论数据已保存到 comments.csv')

if __name__ == "__main__":
    song_id = '4172700'  # 替换为实际的歌曲 ID
    max_pages = 10  # 设置要获取的页数
    main(song_id, max_pages)
