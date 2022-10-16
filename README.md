# client-side-instagram
Instagram clone through client-sider rendering. This project is the last part of a sequence of projects that implement Instagram through three different ways:
[static site generation](https://github.com/zzehli/static-site-generator), [server-side rendering](https://github.com/zzehli/server-side-instgram) and client-side rendering through React.
This project uses many of the same static files as the server-side rendering version, but porting the main pages from templated server-side rendering to client-sider rendering
using React.

## Website
http://ec2-18-220-20-99.us-east-2.compute.amazonaws.com/

To browse the content, sign up for a new user account. Or use a pre-existing user login:
username: `jflinn`
password: `password`

## Features
* Flask backend with Sqlite database
* Frontend uses a combination of React that takes in REST API and templated Jinja pages 
* authentication system built from scratch, password stored in hashed form
* handcoded layout and CSS
