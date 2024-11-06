# 開発メモ

## Rye

### 仮想環境の起動
```. .venv/bin/activate```

### パッケージ追加
```rye add ---```

**バージョン指定**
```rye add "---==3.1.1"```

## LLMでデータを取得した際のNULLについて
NULLが入力されるのは以下の2パターン
1. エラー等による処理の中断における未実行
2. 取得を試みたが失敗

上記どちらの2パターンに当てはまるかは、メール作成ログを確認することで判定可能

**その他**
https://rye.astral.sh/guide/basics/#adding-dependencies

## テスト
* coverage導入済み
