from rest_framework.settings import api_settings
from django.http import Http404
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, exceptions
from rest_framework.authentication import ( SessionAuthentication,
                                            BasicAuthentication, TokenAuthentication
                                            )
from rest_framework.permissions import ( BasePermission, IsAuthenticated,
                                         AllowAny, SAFE_METHODS
                                         )
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from myblog.models import Post
from myblog.serializers import UserSerializer, PostSerializer



class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class UserAuthentication(authentication.SessionAuthentication):
    '''
    User authentication check
    '''
    
    def authenticate(self, request):
        
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        if not username or not password:
            raise exceptions.AuthenticationFailed('No credentials provided.')
        
        user = authenticate(username=username, password=password)
        print('Username:{}, Password:{}, USER:{}'.format(username, password, user))
        if user is None:
            raise exceptions.AuthenticationFailed('Invalid username/password.')
        if not user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted.')
        return (user, None) 


class UserCreation(APIView):
    """
    Put a new user
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (AllowAny,)
    
    def put(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(ObtainAuthToken):
    """
    Post a user login
    """
    authentication_classes = (SessionAuthentication, UserAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        print('TOKEN_KEY:{}'.format(token))
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class PostCreation(APIView):
    """
    Post a post by an authenticated user
    """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        blogger = User.objects.get(username=request.user)
        request.data.update({'blogger':blogger})
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            blogger = serializer.validated_data['blogger']
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllAbcSorting(APIView):
    """
    GET all bloggers in abc order by any user
    """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated|ReadOnly,)
    
    def get(self, request):
        abc = Post.objects.order_by('blogger').distinct('blogger')
        if abc is None:    # check the condition!
            raise Http404
        serializer = PostSerializer(abc, many=True)
        return Response(serializer.data)


class AllNumSorting(APIView):
    """
    GET all bloggers in sorting order depending of his/her number of posts
    by any user
    """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated|ReadOnly,)
    
    def get(self, request, format=None):
        bloggers = Post.objects.order_by('blogger').distinct('blogger')
        if bloggers is None:   # check the condition!
            raise Http404
        for b in bloggers:
            q = Post.objects.filter(blogger=b.blogger).annotate(Count('title'))
            Post.objects.filter(blogger=b.blogger).update(posts=len(q))
        bloggers = Post.objects.order_by('blogger', 'posts').distinct('blogger')
        serializer = PostSerializer(bloggers, many=True)
        return Response(serializer.data)


class BloggerPostSorting(APIView):
    """
    GET a blogger post sorted in date creation order by any user
    """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated|ReadOnly,)
    
    def get(self, request):
        postmen = request.GET.get('blogger')
        if not postmen:
            raise exceptions.AuthenticationFailed('No blogger set')
        blogger = Post.objects.filter(blogger=postmen).order_by('time_created')
        if not blogger:
            raise exceptions.AuthenticationFailed('User inactive or deleted.')
        serializer = PostSerializer(blogger, many=True)
        return Response(serializer.data)


class Subscribe(APIView):
    """
    Put a subscription mark by an authenticated user
    """

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        blogger = User.objects.get(username=self.request.user)
        sub = Post.objects.filter(blogger=blogger).order_by('id')
        sublist = sub[0].subscriptions+str(pk)
        inst = self.get_object(sub[0].id)
        serializer = PostSerializer(inst, data={'subscriptions':sublist,
                                                'blogger':blogger}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnSubscribe(APIView):
    """
    Put an unsubscription by an authenticated user
    """

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404
    
    def put(self, request, pk):
        blogger = User.objects.get(username=self.request.user)
        sub = Post.objects.filter(blogger=blogger).order_by('id')
        unsublist = sub[0].subscriptions
        newunsub = ''
        for unsub in unsublist:
            if unsub == str(pk): 
                continue
            newunsub += unsub 
        inst = self.get_object(sub[0].id)
        serializer = PostSerializer(inst, data={'subscriptions':newunsub,
                                                'blogger':blogger}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubList(APIView):
    """
    GET a list of subscribed posts by an authenticated user
    in time order and with pagination of 10 pages
    """
    
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    
    authentication_classes = (SessionAuthentication, TokenAuthentication) #, UserAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        blogger = Post.objects.filter(blogger=self.request.user).order_by('id')
        if not blogger:
            raise exceptions.AuthenticationFailed('User inactive or deleted.')
        blogger = Post.objects.filter(id__in=[c for c in blogger[0].subscriptions]).order_by('time_created')

        page = self.paginate_queryset(blogger)
        if page is not None:
            serializer = PostSerializer(blogger, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = PostSerializer(blogger, many=True)
        return Response(serializer.data)

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class ReadPostMark(APIView):
    """
    Put a Post is read mark by an authenticated user
    """

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404
    
    def put(self, request, pk):
        
        blogger = User.objects.get(username=self.request.user)
        mark = Post.objects.filter(blogger=blogger).order_by('id')
        readlist = mark[0].readposts+str(pk)
        inst = self.get_object(mark[0].id)
        serializer = PostSerializer(inst, data={'readposts':readlist,
                                                'blogger':blogger},
                                    partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnReadPostOutput(APIView):
    """
    Get an unread posts list by an authenticated user
    """
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        
        blogger = Post.objects.filter(blogger=self.request.user).order_by('id')
        if not blogger:
            raise exceptions.AuthenticationFailed('User inactive or deleted.')
        blogger = Post.objects.exclude(id__in=[c for c in blogger[0].readposts]).order_by('time_created')
        serializer = PostSerializer(blogger, many=True)
        return Response(serializer.data)
        


