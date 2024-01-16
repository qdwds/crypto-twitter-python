from tortoise import fields
from tortoise.models import Model
from tortoise.fields.base import Field as BaseField

""""
twitter 推文模型
"""
class Tweets(Model):
    id = fields.IntField(pk=True)
    tweet_username = fields.CharField(max_length=32, description="发送推文的ID")
    link = fields.CharField(max_length=256, description="推文链接", unique=True)
    text = fields.TextField(description="推文内容")
    user = fields.JSONField(description="用户详情")
    date = fields.CharField(max_length=256, description="发布时间")
    is_retweet = fields.BooleanField(description="是否为转发",default=False)
    external_link = fields.CharField(max_length=256, description="外部链接")
    quoted_post = fields.JSONField(max_length=256, description="引用的帖子")
    stats = fields.JSONField(description="帖子详情")
    # pictures = fields.CharField(max_length=256, description="照片")
    # videos = fields.CharField(max_length=256, description="视频")
    # gifs = fields.CharField(max_length=256, description="gif")
    # timestamp = fields.IntField(description="推文的时间戳")
    # username = fields.CharField(max_length=32, description="用户ID")
    # tweetNumber = fields.ForeignKeyField("models.TweetNumber", related_name="tweets")  # 反向查询
