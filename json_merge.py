import json
import os
import glob

# ファイルパスの定義
DATA_DIR = 'data' 
# 出力ファイル名
OUTPUT_FILE = 'CardMetadata.json' 

def merge_json_files():
    """
    dataフォルダ内のすべての.jsonファイルを読み込み、内容を一つのリストに結合して出力します。
    """
    
    # 1. dataフォルダ内の全JSONファイルを検索
    # **.json 拡張子を持つすべてのファイルを対象にします
    search_pattern = os.path.join(DATA_DIR, "*.json")
    json_paths = glob.glob(search_pattern)
    
    if not json_paths:
        print(f"エラー: {DATA_DIR} フォルダ内に .json ファイルが見つかりません。パスを確認してください。")
        return

    # 2. 全てのデータを格納するリスト
    all_data = []
    
    # 3. 検索されたJSONファイルを一つずつ読み込み、結合
    for json_path in json_paths:
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # 結合処理：
                # 個別JSONファイルの内容をそのままリストに追加します。
                # 個別JSONファイルがオブジェクト（{...}）でも、リスト（[...]）でも対応します。
                if isinstance(data, list):
                    all_data.extend(data)
                else:
                    all_data.append(data)
                    
                print(f"✅ {os.path.basename(json_path)} を結合しました。")
                
        except json.JSONDecodeError:
            print(f"⚠️ 警告: {os.path.basename(json_path)} のJSON形式が正しくありません。スキップします。")
        except Exception as e:
            print(f"⚠️ 警告: {os.path.basename(json_path)} の処理中に予期せぬエラーが発生しました: {e}。スキップします。")

    # 4. 結合したデータを新しいJSONファイルとして書き出す
    if all_data:
        try:
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                # JSONデータを整形して書き出す (indent=4で読みやすく)
                json.dump(all_data, f, ensure_ascii=False, indent=4)
            print(f"\n🎉 成功: 全 {len(json_paths)} ファイルの内容を {OUTPUT_FILE} に結合しました。")
        except IOError:
            print(f"❌ エラー: {OUTPUT_FILE} への書き込みに失敗しました。")
    else:
        print("\n⚠ 警告: 処理できるデータが見つかりませんでした。")

if __name__ == "__main__":
    merge_json_files()