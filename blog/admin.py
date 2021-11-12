from django.contrib import admin
from .models import CommentLike, CommentReply, Like, Post, Comment
# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(CommentReply)
admin.site.register(CommentLike)