from backend.posts import Tweet, Comment

# tweets = Tweet.objects.filter(id=1)
# print(tweets)
#
# print(tweets.query)
# #
# comment = Comment.objects.get(id=1)
# print(comment.tweet)

# tweet = Tweet.objects.create(title='Tweet', body='Body', user_id=1)
#
# comment1 = Comment(text='Comment', user_id=1, tweet_id=tweet.id)
# comment2 = Comment(text='Comment2', user=User.objects.get(id=1), tweet=tweet)
# comment1.save()
# comment2.save()

# comments = Comment.objects.filter(id=1)
# print(comments)
#
#
# for i in range(10):
#     Tweet.objects.create(title=f'Title {i}', body=f'Body {i}', user_id=1)

#
# tweets = Tweet.objects.filter(id__in=[1, 2, 3, 4, 5]).order_by('-id')
# print(tweets)
# print(tweets.query)
#
# tweets_odds = tweets.filter(id__in=[1, 3, 5])
# print(tweets_odds)
# print(tweets_odds.query)
#
# tweet_not_5 = tweets_odds.exclude(id=5)
# print(tweet_not_5)
# print(tweet_not_5.query)


tweets = Tweet.objects.filter(title__iexact='title 0')

print(tweets)
print(tweets.query)


tweets_contain = Tweet.objects.filter(title__contains='Title')
print(tweets)
print(tweets_contain.query)

itweets_contain = Tweet.objects.filter(title__icontains='title')
print(itweets_contain)
print(itweets_contain.query)

tweets_greater_than_5 = Tweet.objects.filter(id__gt=5)
print(tweets_greater_than_5)
print(tweets_greater_than_5.query)


tweets_greater_than_or_equal_5 = Tweet.objects.filter(id__gte=5)
print(tweets_greater_than_or_equal_5)
print(tweets_greater_than_or_equal_5.query)


comments = Comment.objects.filter(tweet__title__iexact='tweet')
print(comments)
print(comments.query)


comments = Comment.objects.filter(tweet__user__id__lt=2)
print(comments)
print(comments.query)

