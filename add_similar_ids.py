import json
import os
import glob
from difflib import SequenceMatcher

# ファイルパスの定義
DATA_DIR = 'data'
# 類似度の閾値と上位N個の定義
SIMILARITY_THRESHOLD = 0.4  # 類似度がこの値以上のものだけを対象とする (必要に応じて調整)
TOP_N_SIMILAR = 10          # 上位N個を保存する

def similarity(a, b):
    """名前の類似度を0～1で返す"""
    return SequenceMatcher(None, a, b).ratio()

def add_similar_ids():
    """
    dataフォルダ内のすべての.jsonファイルを読み込み、似ているカード名を設定します
    """
    
    # 1. dataフォルダ内の全JSONファイルを検索
    # **.json 拡張子を持つすべてのファイルを対象にします
    search_pattern = os.path.join(DATA_DIR, "*.json")
    json_paths = glob.glob(search_pattern)
    
    if not json_paths:
        print(f"エラー: {DATA_DIR} フォルダ内に .json ファイルが見つかりません。パスを確認してください。")
        return

    # 2. 全てのデータを格納するリスト
    all_cards = {}
    
    # 3. 検索されたJSONファイルを一つずつ読みこっむ
    for json_path in json_paths:
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                card_id = data.get('card_id')
                name_jp = data.get('name_ruby')
                
                # 'card_id'と'name_jp'が存在することを確認
                if card_id and name_jp:
                    all_cards[card_id] = {'name': name_jp, 'path': json_path, 'data': data}
                else:
                    print(f"⚠️ 警告: {os.path.basename(json_path)} に 'card_id' または 'name_jp' がありません。スキップします。")
                
                
        except json.JSONDecodeError:
            print(f"⚠️ 警告: {os.path.basename(json_path)} のJSON形式が正しくありません。スキップします。")
        except Exception as e:
            print(f"⚠️ 警告: {os.path.basename(json_path)} の処理中に予期せぬエラーが発生しました: {e}。スキップします。")

    print(f"✅ 合計 {len(all_cards)} 件のカードデータを読み込みました。類似度計算を開始します...")
    
    
    # 4. 全てのカードに対して類似度を計算し、'similar_ids'を決定
    for target_id, target_card in all_cards.items():
        similarities = []
        target_name = target_card['name']
        # ターゲットカード以外のすべてのカードと比較
        for other_id, other_card in all_cards.items():
            if target_id == other_id:
                continue # 自分自身はスキップ
            
            other_name = other_card['name']
            sim_ratio = similarity(target_name, other_name)
            
            # 閾値以上の類似度を持つものをリストに追加
            if sim_ratio >= SIMILARITY_THRESHOLD:
                similarities.append((sim_ratio, other_id))
            
        # 類似度が高い順にソートし、上位N個（自分自身を除く）を抽出
        # 類似度は降順（大きい順）
        similarities.sort(key=lambda x: x[0], reverse=True)
            
        # 上位N個のIDを抽出
        top_similar_ids = [id for ratio, id in similarities[:TOP_N_SIMILAR]]
        
        # 5. 元のJSONデータに 'similar_ids' を追加・更新
        target_data = target_card['data']
        target_data['similar_ids'] = top_similar_ids 
            
        # 6. JSONファイルを上書き保存
        try:
            with open(target_card['path'], 'w', encoding='utf-8') as f:
                # 読みやすいようにインデントをつけて保存
                json.dump(target_data, f, ensure_ascii=False, indent=4)
            # print(f"✨ {target_id}: 'similar_ids' ({len(top_similar_ids)}件) を保存しました。")

        except Exception as e:
            print(f"❌ エラー: {os.path.basename(target_card['path'])} の書き込み中にエラーが発生しました: {e}")
            
    print("\n🎉 全てのJSONファイルへの類似カードIDの追加処理が完了しました。")

if __name__ == "__main__":
    add_similar_ids()