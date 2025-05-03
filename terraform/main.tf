# 手動作成したプロジェクトを参照
data "google_project" "gCloud_Hackathon" {
  project_id = "gcloud-hackathon"           # プロジェクトID
}

# App Engin アプリケーションの作成
resource "google_app_engine_application" "app_engine_Hackathon" {
  location_id = "asia-northeast1"       # リージョン
  database_type = "CLOUD_FIRESTORE" # Firestoreを利用（例）
}

# App Engine用のサービスアカウントを作成
resource "google_service_account" "app_engine_sa" {
  account_id   = "gemini-app-engine-sa"
  display_name = "Gemini App Engine Service Account"
}

# APIキーの設定（Gemini API用）
resource "google_service_account_key" "key" {
  service_account_id = google_service_account.app_engine_sa.name
}

# Cloud Storage バケットの作成
resource "google_storage_bucket" "gCloudHackathon_bucket" {
  name          = "gcloudhackathon-storage-bucket"  # バケット名
  location      = "asia-northeast1"                      # リージョン
  storage_class = "STANDARD"                # ストレージクラス
  force_destroy = true                      # バケット削除時にデータも削除
}

# vertex AI api の有効化
resource "google_project_service" "gCloudHackathon_enable_generative_ai" {
  service = "aiplatform.googleapis.com"
  project = data.google_project.gCloud_Hackathon.project_id
}

# iam api の有効化
resource "google_project_service" "gCloudHackathon_enable_iam_api"{
  service = "iam.googleapis.com"
  project = data.google_project.gCloud_Hackathon.project_id
}

# Secret Manager の設定
resource "google_secret_manager_secret" "gCloudHackathon_secret" {
  secret_id = "gcloudhackathon-secret"

  labels = {
    label = "hackathon-secret-label"
  }

  replication {
    user_managed {
      replicas {
        location = "us-central1"
      }
      replicas {
        location = "us-east1"
      }
    }
  }
}

resource "google_secret_manager_secret_version" "gCloudHackathon_secret_version" {
    secret = google_secret_manager_secret.gCloudHackathon_secret.id

    secret_data = file("../secretfile/secret.json")
}
