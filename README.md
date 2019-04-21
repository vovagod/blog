## Blog-API Description

#### This is an example of REST API service for a blog with the following actions:
    
1. Sign up for new users and enter into for existing ones.
2. Authorized users to create posts. The post has the title and text of the post.
3. View a list of users with the ability to sort by the number of posts.
4. View a list of posts by other users sorted by date created, first fresh.
5. Authorized users to subscribe and unsubscribe to posts of other users.
6. Authorized users to form a feed from user posts to which they subscribed.
   New posts are added to the tape after the subscription is completed.
   Sort by post creation date, fresh first. The list of posts is given in pages of 10pcs.
7. Authorized users to mark posts in the feed as read and filter posts by this attribute.
8. Administrator to manage users and content using Django admin.

## Technology stack

- Python 3.5
- Django 2.0
- PostgreSQL

#### For testing REST API service was used [httpie](https://httpie.org/):

##### 1. New user registration client request:
    
###### httpie test for unauthorized users:
http PUT 127.0.0.1:8000/blog/register/ username=user password=user12345
    
    Method: PUT, URL string: /blog/register/,
    json data in request body: {'username':'username', 'password':'user12345'}

    Server json response example:
        {
    "email": "",
    "first_name": "",
    "last_name": "",
    "password": "user12345",
    "username": "user"
}
##### 2. User login:

###### httpie test for unauthorized users:
http POST 127.0.0.1:8000/blog/login/ username=user password=user12345

    Method: POST, URL string: /blog/login/,
    json data in request body: {'username':'username', 'password':'user12345'}

    Server json response example:
        {
    "email": "user@user.com",
    "token": "a626ca5d468814b9e473a4857fd2567cd9663995",
    "user_id": 1
}
    
##### 3. User post creation:
    
###### httpie test for authorized users:
http POST 127.0.0.1:8000/blog/postcreate/ "Authorization: Token a626ca5d468814b9e473a4857fd2567cd9663995" title=title text=text

    Method: POST, URL string: /blog/postcreate/,
    json data in request body: {'title':'title', 'text':'text'},
               in header body: {'Authorization': 'Token a626ca5d468814b9e473a4857fd2567cd9663995'}

    Server json response example:
    {
    "blogger": "user",
    "id": 5,
    "posts": 0,
    "readposts": "",
    "subscriptions": "",
    "text": "text",
    "time_created": "2019-04-19T11:14:33.243339Z",
    "title": "title"
}

##### 4. Bloggers ABC sorting: 
    
###### httpie test for authorized and unathorized users:
http GET 127.0.0.1:8000/blog/abcsorting/

    Method: GET, URL string: /blog/abcsorting/

    Server json string response example:
         {
        "blogger": "user",
        "id": 1,
        "posts": 0,
        "readposts": "",
        "subscriptions": "",
        "text": "text",
        "time_created": "2019-04-18T14:20:06.709474Z",
        "title": "title"
    }

##### 5. Sorting on number of posts:
    
###### httpie test for authorized and unathorized users: 
http GET 127.0.0.1:8000/blog/numsorting/

    Method: GET, URL string: /blog/numsorting/

    Server json response example:
            {
        "blogger": "admin",
        "id": 5,
        "posts": 5,
        "readposts": "",
        "subscriptions": "",
        "text": "example",
        "time_created": "2019-04-19T11:14:33.243339Z",
        "title": "test"
    }

##### 6. Sorting in date order for one of bloggers:
    
###### httpie test for authorized and unathorized users: 
http GET 127.0.0.1:8000/blog/datesorting/ blogger=admin

    Method: GET, URL string: /blog/datesorting/,
    json data in request body: {'blogger':'blogger'}

    Server json response example:
        {
        "blogger": "admin",
        "id": 1,
        "posts": 5,
        "readposts": "",
        "subscriptions": "",
        "text": "text",
        "time_created": "2019-04-18T14:20:06.709474Z",
        "title": "title"
    },
    {
        "blogger": "admin",
        "id": 2,
        "posts": 5,
        "readposts": "",
        "subscriptions": "",
        "text": "example",
        "time_created": "2019-04-19T09:47:42.770750Z",
        "title": "test"
    }


##### 7. Subscription on post of one of bloggers:
    
###### httpie test for authorized users only: 
http PUT 127.0.0.1:8000/blog/subscribe/6/ "Authorization: Token a626ca5d468814b9e473a4857fd2567cd9663995"

    Method: PUT, URL string: /blog/subscribe/<id of post to subscribe>/,
    json data in in header body: {'Authorization': 'Token a626ca5d468814b9e473a4857fd2567cd9663995'}

    Server json response example:
        {
    "blogger": "admin",
    "id": 1,
    "posts": 5,
    "readposts": "",
    "subscriptions": "16",
    "text": "text",
    "time_created": "2019-04-19T12:08:35.771853Z",
    "title": "title"
}

##### 8. Unsubscription on post of the blogger:
    
###### httpie test for authorized users only:
http PUT 127.0.0.1:8000/blog/unsubscribe/1/ "Authorization: Token a626ca5d468814b9e473a4857fd2567cd9663995"

    Method: PUT, URL string: /blog/unsubscribe/<id of post to unsubscribe>/,
    json data in in header body: {'Authorization': 'Token a626ca5d468814b9e473a4857fd2567cd9663995'}

    Server json response example:
        {
    "blogger": "admin",
    "id": 1,
    "posts": 5,
    "readposts": "",
    "subscriptions": "",
    "text": "text",
    "time_created": "2019-04-19T12:20:53.342234Z",
    "title": "title"
}

##### 9. Output the list of subscribed posts in time order and with pagination of 10 pages:
    
###### httpie test for authorized users only: 
http GET 127.0.0.1:8000/blog/sublist/ "Authorization: Token a626ca5d468814b9e473a4857fd2567cd9663995"

    Method: GET, URL string: /blog/sublist/,
    json data in in header body: {'Authorization': 'Token a626ca5d468814b9e473a4857fd2567cd9663995'}

    Server json string response example:
        {
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "blogger": "user",
            "id": 6,
            "posts": 0,
            "readposts": "",
            "subscriptions": "",
            "text": "text",
            "time_created": "2019-04-19T12:08:17.735064Z",
            "title": "title"
        },
        {
            "blogger": "admin",
            "id": 1,
            "posts": 5,
            "readposts": "",
            "subscriptions": "61",
            "text": "text",
            "time_created": "2019-04-19T12:40:33.472725Z",
            "title": "title"
        }
    ]
}

##### 10. Mark the post as read: 
    
###### httpie test for authorized users only: 
http PUT 127.0.0.1:8000/blog/readpostmark/6/ "Authorization: Token a626ca5d468814b9e473a4857fd2567cd9663995"

    Method: PUT, URL string: /blog/readpostmark/<id of post to mark as read>/,
    json data in in header body: {'Authorization': 'Token a626ca5d468814b9e473a4857fd2567cd9663995'}

    Server json response example:
        {
    "blogger": "admin",
    "id": 1,
    "posts": 5,
    "readposts": "6",
    "subscriptions": "61",
    "text": "text",
    "time_created": "2019-04-19T12:56:52.594631Z",
    "title": "title"
}

##### 11. Output the list of unread posts:
    
###### httpie test for authorized users only: 
http GET 127.0.0.1:8000/blog/unreadpostoutput/ "Authorization: Token a626ca5d468814b9e473a4857fd2567cd9663995"

    Method: GET, URL string: /blog/unreadpostoutput/,
    json data in in header body: {'Authorization': 'Token a626ca5d468814b9e473a4857fd2567cd9663995'}

    Server json response example:
        
        [
    {
        "blogger": "admin",
        "id": 2,
        "posts": 5,
        "readposts": "",
        "subscriptions": "",
        "text": "text",
        "time_created": "2019-04-19T09:47:42.770750Z",
        "title": "title"
    },
    {
        "blogger": "admin",
        "id": 3,
        "posts": 5,
        "readposts": "",
        "subscriptions": "",
        "text": "text",
        "time_created": "2019-04-19T10:12:29.424320Z",
        "title": "title"
    },
   
        "posts": 5,
        "readposts": "6",
        "subscriptions": "61",
        "text": "text",
        "time_created": "2019-04-19T12:56:52.594631Z",
        "title": "title"
    }
]
        
    
## License
                              
#### Code is licensed under the BSD License. See [LICENSE](https://en.wikipedia.org/wiki/BSD_licenses) for more information.
        
