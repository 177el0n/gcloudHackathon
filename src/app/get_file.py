from google.cloud import storage

def get_md_file_content(bucket_name: str, file_path: str) -> str:
    """
    Google Cloud Storage 上の Markdown ファイルを取得して内容を返す関数
    Args:
        bucket_name (str): GCS バケット名
        file_path (str): GCS 上のファイルパス
    Returns:
        str: Markdown ファイルの内容
    """
    # Google Cloud Storage クライアントの初期化
    client = storage.Client()

    # バケットの取得
    bucket = client.bucket(bucket_name)

    # Blob の取得
    blob = bucket.blob(file_path)

    # Blob からデータをダウンロードして内容を取得
    content = blob.download_as_text()

    return content