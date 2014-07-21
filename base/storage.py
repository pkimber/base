# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.core.files.storage import get_storage_class
from storages.backends.s3boto import S3BotoStorage


class CachedS3BotoStorage(S3BotoStorage):
    """
    S3 storage backend that saves the files locally, too.

    I think this is used for 'collectstatic' so the files are copied to the
    local file system as well as to Amazon S3.

    Copied from:
    http://django-compressor.readthedocs.org/en/latest/remote-storages/#using-staticfiles
    """
    def __init__(self, *args, **kwargs):
        super(CachedS3BotoStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class(
            "compressor.storage.CompressorFileStorage")()

    def save(self, name, content):
        name = super(CachedS3BotoStorage, self).save(name, content)
        self.local_storage._save(name, content)
        return name
