from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="hfl/chinese-macbert-base",
    local_dir="./models/chinese-macbert-base"
)