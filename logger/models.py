from django.db import models


class OuterRequestModel(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    request_url = models.CharField(max_length=255)
    request_headers = models.TextField(blank=True, null=True)
    request_body = models.TextField(blank=True, null=True)
    response_status_code = models.IntegerField()
    response_headers = models.TextField()
    response_body = models.TextField(blank=True, null=True)
