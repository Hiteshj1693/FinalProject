from rest_framework import generics
from .models import BlogPost
from .serializers import BlogPostSerializer
from .permissions import IsAdministrator, IsTeacherOrAdministrator, IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView

class BlogPostListCreateView(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    def get_permissions(self):
        if  self.request.method == 'POST':
            return [IsAuthenticated(), IsTeacherOrAdministrator()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# class BlogPostDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = BlogPost.objects.all()
#     serializer_class = BlogPostSerializer
#     permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


# Custom permission to allow only authors or admins to delete
class IsAuthorOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.role == 'administrator' or obj.author == request.user

# class BlogPostDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = BlogPost.objects.all()
#     serializer_class = BlogPostSerializer
#     permission_classes = [IsAuthenticated, IsAuthorOrAdmin]  # Auth required + Custom rule

#     def delete(self, request, *args, **kwargs):
#         blog = self.get_object()
#         if not self.check_object_permissions(request, blog):
#             return Response({'detail': 'You do not have permission to delete this blog.'}, status=status.HTTP_403_FORBIDDEN)
#         return super().delete(request, *args, **kwargs)

class BlogPostDetailView(RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrAdmin]  # Authentication required + Role-based access

    # Override perform_destroy to ensure permission check
    def perform_destroy(self, instance):
        if not self.request.user.role == 'administrator' and instance.author != self.request.user:
            raise PermissionError("You do not have permission to delete this blog.")
        instance.delete()