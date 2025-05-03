provider "google" {
  credentials = file("../secretfile/gcloud-hackathon-bb41d9a38041.json") # サービスアカウントのキー
  project     = "gcloud-hackathon"                              # プロジェクトID
  region      = "asia-east1"                                  # リージョン
}
