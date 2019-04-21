from django.contrib.auth.models import AnonymousUser, User
from rest_framework.test import APITestCase, APIClient, APIRequestFactory, force_authenticate
from rest_framework.authtoken.models import Token
from myblog.models import Post
from myblog.views import ( UserCreation, PostCreation, AllAbcSorting, AllNumSorting,
                           BloggerPostSorting, Subscribe, UnSubscribe, SubList,
                           ReadPostMark, UnReadPostOutput )


class AccountTests(APITestCase):

    
    # APIRequestFactory method of path('/blog/register/', views.UserCreation.as_view())
    def test_usercreation(self):
        """
        Ensure we can PUT a new user
        """
        factory = APIRequestFactory()
        url = '/blog/register/'
        data = {'username':'new', 'email':'new@new.ru', 'password':'new12345'}
        request = factory.put(url, data)
        force_authenticate(request, user=AnonymousUser(), token=None)
        response = UserCreation.as_view()(request)
        assert response.status_code == 200


    @classmethod
    def setUpTestData(cls):
        """
        Set up data for the whole TestCase
        and creation of new user testing instanse
        """
        cls.client = APIClient()
        cls.factory = APIRequestFactory()
        cls.newuser = {'username':'newuser', 'email':'newuser@newuser.ru',
                       'password':'newuser12345'}
        cls.user = User.objects.create_user(username='newuser',
                                            email='newuser@newuser.ru', password='newuser12345')
        cls.user.save()
        cls.token = Token.objects.get(user__username='newuser')
        newuser = User.objects.get(username='newuser')
        Post.objects.create(blogger=newuser)


    # APIClient method of path('/blog/login/', views.UserLogin.as_view())
    def test_userlogin(self):
        """
        Ensure a new user can LOGIN
        """
        response = self.client.login(username='newuser', password='newuser12345')
        self.assertTrue(response)


    # APIRequestFactory method of path('/blog/postcreate/', views.PostCreation.as_view())
    def test_post_apost(self):
        """
        Ensure we can POST a post by un authenticated user
        """
        url = 'http://blog/postcreate/'
        data = {'title': 'new idea', 'text':'Notre Dame Cathedral rebuilt in 5 years'}
        request = self.factory.post(url, data)
        force_authenticate(request, user=self.user, token=self.token)
        response = PostCreation.as_view()(request)
        assert response.status_code == 200


    # APIRequestFactory method of path('/blog/abcsorting/', views.AllAbcSorting.as_view())
    def test_abc_sorting(self):
        """
        Ensure we can GET all bloggers in abc order by any user
        """
        url = 'http://blog/abcsorting/'
        request = self.factory.get(url)
        force_authenticate(request, user=AnonymousUser(), token=None)
        response = AllAbcSorting.as_view()(request)
        assert response.status_code == 200


    # APIRequestFactory method of path('/blog/numsorting/', views.AllNumSorting.as_view())
    def test_num_sorting(self):
        """
        Ensure we can GET all bloggers in sorting order depending
        of his/her number of posts by any user
        """
        request = self.factory.get('http://blog/numsorting/')
        force_authenticate(request, user=AnonymousUser())
        response = AllNumSorting.as_view()(request)
        assert response.status_code == 200


    # APIRequestFactory method of path('/blog/datesorting/', views.BloggerPostSorting.as_view())
    def test_date_sorting(self):
        """
        Ensure we can GET a blogger post sorted in date creation order by any user
        """
        request = self.factory.get('http://blog/datesorting/?blogger=newuser')
        force_authenticate(request, user=self.user, token=None)
        response = BloggerPostSorting.as_view()(request)
        assert response.status_code == 200


    # APIRequestFactory method of path('/blog/subscribe/<int:pk>/', views.Subscribe.as_view())
    def test_subscribe(self):
        """
        Ensure we can PUT a subscription mark by an authenticated user
        """
        url = 'http://blog/subscribe/0/'
        request = self.factory.put(url)
        force_authenticate(request, user=self.user, token=self.token)
        response = Subscribe.as_view()(request, pk='0')
        assert response.status_code == 200


    # APIRequestFactory method of path('/blog/unsubscribe/<int:pk>/', views.UnSubscribe.as_view())
    def test_unsubscribe(self):
        """
        Ensure we can PUT a usubscription mark by an authenticated user
        """
        url = 'http://blog/unsubscribe/0/'
        request = self.factory.put(url)
        force_authenticate(request, user=self.user, token=self.token)
        response = UnSubscribe.as_view()(request, pk='0')
        assert response.status_code == 200


    # APIRequestFactory method of path('/blog/sublist/', views.SubList.as_view())
    def test_sublist(self):
        """
        Ensure we can GET a list of subscribed posts by an authenticated user
        in time order and with pagination of 10 pages
        """
        url = 'http://blog/sublist/'
        request = self.factory.get(url)
        force_authenticate(request, user=self.user, token=self.token)
        response = SubList.as_view()(request)
        assert response.status_code == 200


    # APIRequestFactory method of path('/blog/readpostmark/<int:pk>/', views.ReadPostMark.as_view())
    def test_readpostmark(self):
        """
        Ensure we can PUT a post is read mark by an authenticated user
        """
        url = 'http://readpostmark/0/'
        request = self.factory.put(url)
        force_authenticate(request, user=self.user, token=self.token)
        response = ReadPostMark.as_view()(request, pk='0')
        assert response.status_code == 200

        
    # APIRequestFactory method of path('/blog/unreadpostoutput/', views.UnReadPostOutput.as_view())
    def test_unreadpostout(self):
        """
        Ensure we can GET an unread posts list by an authenticated user
        """
        url = 'http://readpostmark/'
        request = self.factory.get(url)
        force_authenticate(request, user=self.user, token=self.token)
        response = UnReadPostOutput.as_view()(request)
        assert response.status_code == 200
