# Azure 時系列予測デモ

FastAPI と Tailwind CSS を使った最小構成の時系列予測 Web アプリケーションです。Azure Web Apps や Container Apps などへそのままデプロイできるシンプルな設計になっています。

## セットアップ

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## ローカル実行

> **Python バージョン**: FastAPI/Pydantic が公式にサポートしている 3.10–3.12 を利用してください。3.13 以降のプレビューバージョンでは依存ライブラリのインポート時にエラーが発生します。

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

ブラウザで <http://localhost:8000/> を開くと UI にアクセスできます。Tailwind CDN を利用しているためビルド工程は不要です。

## エンドポイント

- `GET /` - Tailwind で作成された UI を返却します。
- `GET /api/sample` - サンプル系列を使って 7 ステップ先の予測結果を返します。
- `POST /api/forecast` - 任意の系列とステップ数を受け取り、平均差分による単純外挿結果を返します。

## 備考

- 予測ロジックは平均差分を使った簡易モデルです。Azure Machine Learning などで学習した本格的なモデルに置き換える場合は、`app/main.py` の `extrapolate` 関数や推論部分を差し替えてください。
- Web フロントはシングルファイルのテンプレートで完結しているため、Azure Static Web Apps 等への分離もしやすい構成です。
