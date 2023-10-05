from django.urls import path
from .views import( PostsListCreateView,
    PostRetrieveUpdateDeleteView,
    AddLike,
    CommentCreateListView,
    CommentRetrieveDeleteView
    )


urlpatterns = [
    path("",  PostsListCreateView.as_view(), name="post_create_list"),
    path("<int:pk>",PostRetrieveUpdateDeleteView.as_view() , name='post_get_update'),
    path("<int:pk>/like",AddLike.as_view()),
    path("<int:pk>/comment", CommentCreateListView.as_view(), name="post_comment"),
    path("comment/<int:pk>", CommentRetrieveDeleteView.as_view(), name="comment_get_delete")
]