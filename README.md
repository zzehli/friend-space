# client-side-instagram
Instagram clone through client-sider rendering. This project is the last part of a sequence of projects that implement Instagram in three different ways:
[static site generation](https://github.com/zzehli/static-site-generator), [server-side rendering](https://github.com/zzehli/server-side-instgram) and client-side rendering through React.
This project uses many of the same static files as the server-side rendering version but porting the main pages from templated server-side rendering to client-side rendering
using React.

## Website
http://ec2-18-220-20-99.us-east-2.compute.amazonaws.com/

To browse the content, sign up for a new user account. Or use a pre-existing user login:  
username: `jflinn`  
password: `password`

If you choose to register a new user, the email formatting is not reinforced. Once you log in, your homepage, which shows yours and posts from users you follow, will be empty. You can either click your username on the top right corner to enter your user page and create new posts, or you can click the `explore` button on the top right corner to see all the users you have not followed in the app and follow them.

## Features
* Flask backend with SQLite database
* Frontend uses a combination of React that takes in REST API and templated Jinja pages 
* authentication system built from scratch, the password stored in hashed form
* hand coded layout and CSS
