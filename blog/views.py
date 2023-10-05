from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from .serializers import BlogPostSerializer, LikeSerializer, CommentSerializer
from .models import BlogPost, Like, Comment



class PostsListCreateView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = BlogPost.objects.all().order_by("created_at")
        #No need to pass the request now as the serializer doesn't need it for getting absolute url 
        posts = BlogPostSerializer(serializer, many=True, context={'request': request})
        return Response({"posts":posts.data})

    def post(self, request, **kwargs):
        data = request.data.copy()  # Create a mutable copy of the data
        data['author'] = request.user.pk  # Modify the copy
        serializer = BlogPostSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class PostRetrieveUpdateDeleteView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    allowed_methods = ['GET', "PATCH", "DELETE"]

    def get(self , request, *args, **kwargs):
        post_id = kwargs['pk']
        try:
            post = BlogPost.objects.get(id=post_id)
            #pass the request if you want the absolute url
            serializer = BlogPostSerializer(post, context={'request': request})
            return Response({'post':serializer.data},status=status.HTTP_200_OK)

        except BlogPost.DoesNotExist:
            return Response({"details":"Blog does not found."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"details":"Something went wrong."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self,request, *args, **kwargs):
        try:
            post = BlogPost.objects.get(id=kwargs['pk'])
            if request.user != post.author:
                raise PermissionDenied(detail="This user is not allowed to perform this operation.")

            serializer = BlogPostSerializer(post, data=request.data, partial=True, context={"request":request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

        except BlogPost.DoesNotExist:
            return Response({'details':"Requested post does not exists."},status=status.HTTP_404_NOT_FOUND )
        except PermissionDenied as p:
            return Response({"details":p.detail}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception:
            return Response({'details':'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
    def delete(self, request, *args, **kwargs):
        try:
            post = BlogPost.objects.get(pk=kwargs['pk'])
            if request.user != post.author:
                return Response({"details":"You can't perform this operation."},status=status.HTTP_403_FORBIDDEN)
            post.delete()
            return Response({"details":"Post deleted successfully."}, status=status.HTTP_200_OK)
        except BlogPost.DoesNotExist:
            return Response({'details':"Requested post does not exists."},status=status.HTTP_404_NOT_FOUND )
        except Exception as e:
            return Response({"details":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            


class CommentCreateListView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            post = BlogPost.objects.get(pk=kwargs['pk'])
            comments_qs = post.comment_set.all()
            serializer = CommentSerializer(comments_qs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except BlogPost.DoesNotExist:
            return Response({'details':"Requested post does not exists."},status=status.HTTP_404_NOT_FOUND )
        except Exception as e:
            return Response({"details":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        author = request.user.pk
        content = request.data.get("content")
        if not content:
            return Response({"details":"please provide content to the comment."})
        try:
            post = BlogPost.objects.get(pk=kwargs['pk']).pk
            serializer = CommentSerializer(data={'author':author, 'post':post, 'content':content})
            if serializer.is_valid():
                comment = serializer.save()
                return Response({"details":"Comment added successfully"}, status=status.HTTP_200_OK)
            
            return Response({"detials": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except BlogPost.DoesNotExist:
            return Response({'details':"Requested post does not exists."},status=status.HTTP_404_NOT_FOUND )
        except Exception as e:
            return Response({"details":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CommentRetrieveDeleteView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request, *args , **kwargs):
        try:
            comments_qs = Comment.objects.get(pk=kwargs['pk'])
            serializer = CommentSerializer(comments_qs)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response({'details':"Requested comment does not exists."},status=status.HTTP_404_NOT_FOUND )
        except Exception as e:
            return Response({"details":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        try:
            comments_qs = Comment.objects.get(pk=kwargs['pk'])
            if request.user != comments_qs.author:
                return Response({"details":"You can't perform this operation."},status=status.HTTP_403_FORBIDDEN)
            comments_qs.delete()
            return Response({"details":"Comment deleted successfully."}, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response({'details':"Requested post does not exists."},status=status.HTTP_404_NOT_FOUND )
        except Exception as e:
            return Response({"details":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddLike(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            post = BlogPost.objects.get(pk=kwargs['pk'])
            likes = post.like_set.all()
            serializer = LikeSerializer(likes, many=True)          
            return Response({'liked_by':serializer.data},status=status.HTTP_200_OK)
        except BlogPost.DoesNotExist:
            return Response({"details":"requested post doesn't exists."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"details":"Something went wrong."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        already_liked  = Like.objects.filter(post=kwargs['pk'], author=request.user)
        if already_liked:
            return Response({"details":"You already liked this post."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            post = BlogPost.objects.get(id=kwargs['pk'])
        except BlogPost.DoesNotExist:
            return Response({"details":"requested post deos not exist."},status=status.HTTP_404_NOT_FOUND)
        Like.objects.create(post=post, author=request.user)
        return Response({"details":"liked"}, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        try:
            post = BlogPost.objects.get(id=kwargs['pk'])
            post.like_set.filter(post=kwargs['pk'], author=request.user).delete()
            return Response({"details":"unliked"})
        except BlogPost.DoesNotExist:
            return Response({"details":"requested post deos not exist."},status=status.HTTP_404_NOT_FOUND)
        
