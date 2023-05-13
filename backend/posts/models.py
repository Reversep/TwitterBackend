from django.db import models
from PIL import Image, ImageDraw, ImageFont
from django.core.files import File
from accounts.models import User
import io


class Tweet(models.Model):
    title = models.CharField(max_length=240)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='tweets')

    def get_likes_dislikes(self):
        likes_dislikes = TweetLike.objects.filter(tweet=self)
        likes = likes_dislikes.filter(is_like=True).count()
        dislikes = likes_dislikes.filter(is_like=False).count()
        return {
            'likes': likes,
            'dislikes': dislikes
        }

    def __str__(self):
        return self.title


class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    is_like = models.BooleanField()

    class Meta:
        unique_together = ['user', 'tweet']

    def __str__(self):
        return f'{self.user} - {self.tweet} : {self.is_like}'


def tweet_image_store(instance, filename):
    file_ext = filename.split('.')[-1]
    new_file_name = f'{instance.tweet.user.username}_{instance.id}.{file_ext}'
    return f'tweet_images/tweet_{instance.tweet.id}/{new_file_name}'


class TweetImage(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=tweet_image_store)

    def save(self, *args, **kwargs):
        image = Image.open(self.image)

        #изменен размера под стат ширину
        w, h = image.size
        new_width = 400
        new_height = int(new_width * h / w)
        image = image.resize((new_width, new_height))

        # надпись на картинке
        text = self.tweet.user.username
        font = ImageFont.truetype('Sathu.ttf', size=32)
        text_image = ImageDraw.Draw(image)
        text_image.text((20, 20), text, font=font)


        image_io = io.BytesIO()
        image.save('my_image.png', 'png')
        image.save(image_io, 'png')
        self.image = File(image_io, 'my_image.png')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'image for {self.tweet.id}'


class Comment(models.Model):
    text = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    liked_users = models.ManyToManyField(User, blank=True, through='CommentLike', related_name='likes_count')
    disliked_users = models.ManyToManyField(User, blank=True, through='CommentDislike', related_name='dislike_count')

    # class Meta:
    #     unique_together = ['user', 'tweet']

    def __str__(self):
        return f'{self.text} - {self.tweet}'


class CommentLike(models.Model):
    like_comm = {
        ('like', 'like')
    }
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mark = models.CharField(choices=like_comm, max_length=10)
    liked_at = models.DateField(auto_now_add=True)


class CommentDislike(models.Model):
    like_comm = {
        ('dislike', 'Dislike')
    }
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mark = models.CharField(choices=like_comm, max_length=10)
    liked_at = models.DateField(auto_now_add=True)
