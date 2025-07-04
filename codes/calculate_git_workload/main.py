import subprocess
import re
from collections import defaultdict
import argparse
from datetime import datetime, timedelta
import json

def calculate_git_workload(since=None, output_type="table"):
    """
    Gitリポジトリのコミット履歴から各コミッターの作業量を算出します。
    since: 'N days ago' の形式で期間指定可能
    output_type: "table" または "json"
    """
    if output_type == 'table':
        print("Gitコミット履歴から作業量を算出中...")

    # 各コミッターの作業量を格納する辞書
    # キー: コミッター名 (str)
    # 値: {
    #     'commits': int,
    #     'lines_added': int,
    #     'lines_deleted': int,
    #     'files_changed': int
    # }
    author_stats = defaultdict(lambda: {
        'commits': 0,
        'lines_added': 0,
        'lines_deleted': 0,
        'files_changed': 0
    })

    try:
        command_log = ["git", "log", "--pretty=format:%H|%an", "--no-merges"]
        if since:
            command_log.append(f"--since={since}")
        result_log = subprocess.run(command_log, capture_output=True, text=True, check=True, encoding='utf-8')
        commits_info = result_log.stdout.strip().split('\n')

        # 各コミットを処理
        for line in commits_info:
            if not line:
                continue
            
            commit_hash, author_name = line.split('|', 1) # 作者名に'|'が含まれる可能性を考慮

            # コミット数をインクリメント
            author_stats[author_name]['commits'] += 1

            # 2. 各コミットの変更行数と変更ファイル数を取得
            # git show --numstat <commit-hash> で追加行、削除行、ファイル名を出力
            command_show = ["git", "show", "--numstat", "--pretty=format:", commit_hash]
            result_show = subprocess.run(command_show, capture_output=True, text=True, check=True, encoding='utf-8')
            diff_output = result_show.stdout.strip()

            # 各行の差分情報を解析
            # 例: 10     5       src/main.py
            #     -      -       docs/README.md (バイナリファイルなどの場合)
            for diff_line in diff_output.split('\n'):
                if not diff_line:
                    continue
                
                parts = diff_line.split('\t')
                if len(parts) == 3:
                    added_str, deleted_str, file_name = parts
                    
                    # バイナリファイルなどで '-' が入る場合を考慮
                    added = int(added_str) if added_str.isdigit() else 0
                    deleted = int(deleted_str) if deleted_str.isdigit() else 0

                    author_stats[author_name]['lines_added'] += added
                    author_stats[author_name]['lines_deleted'] += deleted
                    author_stats[author_name]['files_changed'] += 1

    except subprocess.CalledProcessError as e:
        print(f"Gitコマンドの実行中にエラーが発生しました: {e}")
        print(f"標準出力: {e.stdout}")
        print(f"標準エラー: {e.stderr}")
        return
    except FileNotFoundError:
        print("Gitコマンドが見つかりません。Gitがインストールされ、パスが通っているか確認してください。")
        return
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")
        return

    # 結果の表示
    if not author_stats:
        print("コミット履歴が見つかりませんでした。")
        return

    # 作業量を合計行数 (lines_added + lines_deleted) でソート
    sorted_authors = sorted(author_stats.items(), key=lambda item: item[1]['lines_added'] + item[1]['lines_deleted'], reverse=True)

    if output_type == "json":
        # JSON形式で出力
        result = []
        for author, stats in sorted_authors:
            total_changed_lines = stats['lines_added'] + stats['lines_deleted']
            result.append({
                "author": author,
                "commits": stats['commits'],
                "lines_added": stats['lines_added'],
                "lines_deleted": stats['lines_deleted'],
                "files_changed": stats['files_changed'],
                "total_changed_lines": total_changed_lines
            })
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # テーブル形式で出力
        print("\n--- 各コミッターの作業量 ---")
        print(f"{'コミッター':<30} | {'コミット数':>10} | {'追加行数':>10} | {'削除行数':>10} | {'変更ファイル数':>12} | {'合計変更行数':>12}")
        print("-" * 100)
        for author, stats in sorted_authors:
            total_changed_lines = stats['lines_added'] + stats['lines_deleted']
            print(f"{author:<30} | {stats['commits']:>10} | {stats['lines_added']:>10} | {stats['lines_deleted']:>10} | {stats['files_changed']:>12} | {total_changed_lines:>12}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gitリポジトリの作業量を集計します。-dで何日前まで集計するか指定できます。-tで出力形式を指定できます。")
    parser.add_argument('-d', type=int, help='何日前まで集計するか (例: 7 で過去7日分)')
    parser.add_argument('-t', type=str, choices=['table', 'json'], default='table', help='出力形式 (table または json)')
    args = parser.parse_args()
    since = None
    if args.d:
        since = f"{args.d} days ago"
    calculate_git_workload(since=since, output_type=args.t)

