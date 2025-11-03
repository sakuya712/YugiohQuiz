# YugiohQuiz
遊戯王カード名当てクイズ

※画像、個々のjsonはこのリポジトリにはない
実際は以下のようになっている。
```
data
  └─CardId4007.json
  └─CardId4008.json
  └─ …
  └─CardMetadata.json (実際に使うjsonはこれのみ)
images
  └─4007.webp
  └─4008.webp
  └─ …
```
`add_similar_ids.py`で似ているカードを"similar_ids"に登録する。

個々のjsonは`json_merge.py`で`CardMetadata.json`にマージする。


index.htmlを直接開いてもjsonが読み込めないので
```cmd
python -m http.server
```
でローカルサーバ開いて
```
http://localhost:8000/
```