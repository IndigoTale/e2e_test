import requests
import argparse
from response_checker import ResponseChecker

parser = argparse.ArgumentParser(
    description="E2E Test for api/promotion/2.0/search.")
parser.add_argument(
    '--success',
    action='store_true',
    help='execute success pattern.'
)
parser.add_argument(
    '--failed',
    action='store_true',
    help='execute failed pattern.'
)
parser.add_argument(
    '--not-found',
    action='store_true',
    help='execute not found pattern.'
),

# URL 自らチェックする項目
SUCCESS_URL_LIST = [
    "10.38.2.48://api/promotion/2.0/search", # デフォルト値が機能しているか
    "10.38.2.48://api/promotion/2.0/search?promotion_no=0&promotion_no=1", # 左のパラメータを優先しているか1
    "10.38.2.48://api/promotion/2.0/search?method=1,2&method=2,3",  # 左のパラメータを優先しているか2
    "10.38.2.48://api/promotion/2.0/search?repose_group=1", # レスポンスフィールドが仕様書と一致するか1
    "10.38.2.48://api/promotion/2.0/search?repose_group=2", # レスポンスフィールドが仕様書と一致するか2
    "10.38.2.48://api/promotion/2.0/search?send_time_from=2019-09-05 00:00:00", # 指定した日時以前のレコードがないか
    "10.38.2.48://api/promotion/2.0/search?send_time_to=2019-09-05 00:00:00", # 指定した日時以降のレコードがないか",
    "10.38.2.48://api/promotion/2.0/search?method=1,2,3", # 指定したmethod以外のレコードが含まれていないか
    "10.38.2.48://api/promotion/2.0/search?limit=1", # responseCheckerがcheck()可能
    "10.38.2.48://api/promotion/2.0/search?limit=100", # responseCheckerがcheck()可能
    "10.38.2.48://api/promotion/2.0/search?sort=0", # responseCheckerがcheck()可能
    "10.38.2.48://api/promotion/2.0/search?sort=1", # responseCheckerがcheck()可能
    "10.38.2.48://api/promotion/2.0/search?sort=2", # responseCheckerがcheck()可能
    "10.38.2.48://api/promotion/2.0/search?sort=3", # responseCheckerがcheck()可能
]
# URL　チェックしている項目
FAILED_URL_LIST = [
    "10.38.2.48://api/promotion/2.0/search?key=1",  # 存在しないパラメータが指定されたとき
    "10.38.2.48://api/promotion/2.0/search?promotion_no=0",  # 境界値1
    "10.38.2.48://api/promotion/2.0/search?promotion_no=10000000000",  # 境界値2
    "10.38.2.48://api/promotion/2.0/search?promotion_no=-1",  # マイナス値
    "10.38.2.48://api/promotion/2.0/search?promotion_no=１",  # 全角数値
    "10.38.2.48://api/promotion/2.0/search?promotion_no=1.0",  # 浮動小数点数
    "10.38.2.48://api/promotion/2.0/search?promotion_no=text",  # テキスト
    "10.38.2.48://api/promotion/2.0/search?method=7",  # 無効なパラメータ
    "10.38.2.48://api/promotion/2.0/search?method=0",  # 境界値1
    "10.38.2.48://api/promotion/2.0/search?method=14",  # 境界値2
    "10.38.2.48://api/promotion/2.0/search?method=-1",  # マイナス値
    "10.38.2.48://api/promotion/2.0/search?method=１",  # 全角数値
    "10.38.2.48://api/promotion/2.0/search?method=1.0",  # 浮動小数点数
    "10.38.2.48://api/promotion/2.0/search?method=text",  # テキスト
    "10.38.2.48://api/promotion/2.0/search?method=1,",  # カンマ区切り終わり
    "10.38.2.48://api/promotion/2.0/search?method=,1",  # 　カンマ区切り始まり
    "10.38.2.48://api/promotion/2.0/search?method=1,0",  # 無効なパラメータの混在1
    "10.38.2.48://api/promotion/2.0/search?method=0,1",  # 無効なパラメータの混在2
    "10.38.2.48://api/promotion/2.0/search?method=1,7",  # 無効なパラメータの混在3
    "10.38.2.48://api/promotion/2.0/search?method=7,1",  # 無効なパラメータの混在4
    "10.38.2.48://api/promotion/2.0/search?method=1,text",  # 無効なパラメータの混在5
    "10.38.2.48://api/promotion/2.0/search?method=text,1",  # 無効なパラメータの混在6
    "10.38.2.48://api/promotion/2.0/search?send_time_from=1111-11-11 24:00:00", # 存在しない日時1　
    "10.38.2.48://api/promotion/2.0/search?send_time_from=2019-06-31 00:00:00", # 存在しない日時2　
    "10.38.2.48://api/promotion/2.0/search?send_time_from=2019-02-29 00:00:00", # 存在しない日時3 
    "10.38.2.48://api/promotion/2.0/search?send_time_from=2100-02-29 00:00:00", # 存在しない日時4 閏年の落とし穴
    "10.38.2.48://api/promotion/2.0/search?send_time_to=1111-11-11 24:00:00", # 存在しない日時1　
    "10.38.2.48://api/promotion/2.0/search?send_time_to=2019-06-31 00:00:00", # 存在しない日時2　
    "10.38.2.48://api/promotion/2.0/search?send_time_to=2019-02-29 00:00:00", # 存在しない日時3 
    "10.38.2.48://api/promotion/2.0/search?send_time_to=2100-02-29 00:00:00", # 存在しない日時4 閏年の落とし穴
    "10.38.2.48://api/promotion/2.0/search?limit=0", # 境界値1
    "10.38.2.48://api/promotion/2.0/search?limit=101", # 境界値2
    "10.38.2.48://api/promotion/2.0/search?limit=-1", # マイナス値
    "10.38.2.48://api/promotion/2.0/search?limit=１", # 全角数値
    "10.38.2.48://api/promotion/2.0/search?limit=1.0", # 浮動小数点数
    "10.38.2.48://api/promotion/2.0/search?limit=text", # テキスト
    "10.38.2.48://api/promotion/2.0/search?sort=4", # 境界値1
    "10.38.2.48://api/promotion/2.0/search?sort=-1", # 境界値1
    "10.38.2.48://api/promotion/2.0/search?sort=4", # 境界値1
    "10.38.2.48://api/promotion/2.0/search?sort=-1", # 境界値2 マイナス値
]
NOT_FOUND_URL_LIST = [
    "10.38.2.48://api/promotion/2.0/search?promotion_no=9999999999",
    "10.38.2.48://api/promotion/2.0/search?method=1,2,3,4,5",
    "10.38.2.48://api/promotion/2.0/search?send_time_from=2019/09/07 00:00:00&send_time_from=2019/09/06 00:00:00",
]


args = parser.parse_args()


def main():
    if args.success:
        for url in SUCCESS_URL_LIST:
            response_checker = ResponseChecker(url,status_code=200)
            response_checker.check()
    if args.failed
        for url in FAILED_URL_LIST:
            response_checker = ResponseChecker(url,status_code=400)
            response_checker.check()
    if args.not_found:
        for url in NOT_FOUND_URL_LIST:
            response_checker = ResponseChecker(url,status_code=404)
            response_checker.check()

if __name__ == '__main__':
    main()
