import boto3
import os
from tqdm import tqdm

aws_access_key_id = 'AKIA6GBMFUPGZC7HYL73'
aws_secret_access_key = '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'

s3 = boto3.client("s3", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

file_path = "/Users/shota/Coding/TennisBuddy/Flutter/flask_backend/_TrackNet1.mp4"
bucket = "swinganalysis"
key = "test.mp4" #set it manually

file_size = os.stat(file_path).st_size

create_multipart_upload_response = s3.create_multipart_upload(Bucket=bucket, Key=key)
upload_id = create_multipart_upload_response["UploadId"]

part_size = 50 * 1024 * 1024
parts_count = -(-file_size // part_size)

parts = []
with open(file_path, "rb") as f:
    # tqdmを使ってプログレスバーを表示
    with tqdm(total=file_size, unit="B", unit_scale=True, desc=f"Uploading {file_path}") as pbar:
        for i in range(parts_count):
            part_number = i + 1
            part_data = f.read(part_size)

            upload_part_response = s3.upload_part(
                Bucket=bucket,
                Key=key,
                UploadId=upload_id,
                PartNumber=part_number,
                Body=part_data,
            )

            parts.append(
                {"ETag": upload_part_response["ETag"], "PartNumber": part_number}
            )

            # プログレスバーを更新
            pbar.update(len(part_data))

s3.complete_multipart_upload(
    Bucket=bucket,
    Key=key,
    UploadId=upload_id,
    MultipartUpload={"Parts": parts},
)

print(f"File '{file_path}' uploaded to '{bucket}/{key}' as a multipart upload.")
