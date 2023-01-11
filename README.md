![FriendSpace](./friendspace-banner.png)

Friend Space is a fully fledged social media web application. Friend Space has everything you'd expect from a instagram-like social media application: share, comment and like photos, follow friends and discover other users.

## Website
http://ec2-18-220-20-99.us-east-2.compute.amazonaws.com/

To browse the content, sign up for a new user account. Or use a pre-existing user login:  
username: `awd`  
password: `password`

If you choose to register a new user, the email formatting is not reinforced. Once you log in, your homepage, which shows yours and posts from users you follow, will be empty. You can either click your username on the top right corner to enter your user page and create new posts, or you can click the `explore` button on the top right corner to see all the users you have not followed in the app and follow them.

## Features
* User interface deploys a combination of React and templated Jinja pages
* Flask backend provisions REST APIs and SQLite database
* Authentication system built from scratch with session cookies, the password stored in hashed form in db
* Hosted on AWS EC2
* hand coded layout and CSS
