# Clog : A blogging app

### Features

- User registeration and Login
- User can Create blog, add title , content and image to it.
- Users can also edit the post created by the same user.
- Users can comment on any post and they can also edit and delete the comment.
- They can aslo like and unlike any post.
- They can share the post
- And user can log out.




**Table of Contents**

[TOCM]

[TOC]


### Start code

`$ python manage.py migrate`

`$ python manage.py runserver`



###Screenshots


### EndPoints

### User

> 
- Login : 
	+ Request : **POST**
	+ Endpint :  "auth/login"
	+ Fields(required) : 
		+ username
		+ password
- Register:
	+ Request : **POST**
	+ Endpint :  "auth/register"
	+ Fields(required) : 
		+ username
		+ email
		+ password
		+ password2
- Logout :
	+ Request : **POST**
	+ Endpint : "auth/logout"
	
### Post
* List all posts
	+ Request : **GET**
	+ Endpint :  "posts/"
	+ Login(required) : 
* Create a post
	+ Request : **POST**
	+ Endpint (Login Required) :  "/posts/"
	+ Fields(required)  :
		+ title
		+ content
* Edit a post
	+ Request : **PATCH**
	+ Endpint (Login Required) :  "/posts/{post_id}"
	+ Fields(required)  :
		+ title
		+ content
* Delete a post
	+ Request : **DELETE**
	+ Endpint (Login Required) :  "/posts/{post_id}"
* Get all the likes list
	+ Request : **GET**
	+ Endpint (Login Required) :  "/posts/like"
* Get all the comments list
	+ Request : **GET**
	+ Endpint (Login Required) :  "/posts/like"
	
###Comment
                
> 
+ Comment a post
	+ Request : **POST**
	+ Endpint (Login required) :  "posts/{post_id}/comment"
	+ Fields(required) :
		+ content
+ Delete a comment
	+ Request : **DELETE**
	+ Endpint (Login required) :  "posts/{post_id}/comment"
	+ Fields(required) :
+ Edit Comment
	+ Request : **PATCH**
	+ Endpint (Login required) :  "posts/{post_id}/comment"
	+ Fields(required) :
		+ content
+ Retrieve a comment
	+ Request : **GET**
	+ Endpint (Login required) :  "posts/comment//{comment_id}"

### Like
>                 
+ Like a post
	+ Request : **POST**
	+ Endpint (Login required) :  "posts/{post_id}/like"
+ Unlike a post
	+ Request : **DELETE**
	+ Endpint (Login required) :  "posts/{post_id}/like"
+ Retrieve likes of a post:
	+ Request : **GET**
	+ Endpint (Login required) :  "posts/{post_id}/like"


### End
