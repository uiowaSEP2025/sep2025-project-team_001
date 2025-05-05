import base64
import importlib

import pytest
from app.utils import image_upload as img_utils


class DummyS3Client:
    def __init__(self):
        self.uploads = []
        self.deletes = []

    def put_object(self, Bucket, Key, Body, ContentType):
        self.uploads.append((Bucket, Key, Body, ContentType))

    def delete_object(self, Bucket, Key):
        self.deletes.append((Bucket, Key))


@pytest.fixture
def s3_enabled(monkeypatch, settings):
    # Turn on S3 in settings
    settings.USE_S3 = True
    settings.S3_BUCKET_NAME = "mybucket"

    # Patch boto3.client
    monkeypatch.setattr("boto3.client", lambda *a, **kw: DummyS3Client())
    importlib.reload(img_utils)
    return img_utils.s3


def test_save_and_delete_s3(s3_enabled):
    # a fully-padded 1×1 PNG in base64
    png = (
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0"
        "lEQVR42mP8/AMD/4wAAtUB8RkGAAAAAElFTkSuQmCC"
    )
    b64 = f"data:image/png;base64,{png}"

    # 1) Save → should go to S3
    url = img_utils.save_image_from_base64(b64, "avatars", ref_id=42)
    assert url.startswith("https://mybucket.s3.amazonaws.com/avatars/42_")
    assert len(s3_enabled.uploads) == 1
    bucket, key, body, ctype = s3_enabled.uploads[0]
    assert bucket == "mybucket"
    assert key.endswith(".png")
    assert ctype == "image/png"
    # body matches decoded PNG bytes
    assert body == base64.b64decode(png)

    # 2) Delete
    img_utils.delete_s3_image(url)
    assert len(s3_enabled.deletes) == 1
    assert s3_enabled.deletes[0] == ("mybucket", key)


def test_local_save(tmp_path, settings):
    # disable S3
    settings.USE_S3 = False
    importlib.reload(img_utils)

    # simple text payload
    b64 = "dGVzdA=="  # "test"
    url = img_utils.save_image_from_base64(b64, "files", ref_id=1)
    assert url.startswith("/media/files/1_") and url.endswith(".jpg")

    path = img_utils.Path("media") / url[len("/media/"):]
    assert path.exists()
    assert path.read_bytes() == b"test"

    # delete_s3_image must be no-op without raising
    img_utils.delete_s3_image(url)
