from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Post, Like
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType

class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)  # ✅ exact format required
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response({"message": "Already liked"}, status=status.HTTP_400_BAD_REQUEST)

        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb='liked',
            content_type=ContentType.objects.get_for_model(post),
            object_id=post.id
        )

        return Response({"message": "Post liked"}, status=status.HTTP_201_CREATED)


class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)  # ✅ exact format required
        deleted, _ = Like.objects.filter(user=request.user, post=post).delete()
        if deleted:
            return Response({"message": "Post unliked"}, status=status.HTTP_200_OK)
        return Response({"message": "You had not liked this post"}, status=status.HTTP_400_BAD_REQUEST)
