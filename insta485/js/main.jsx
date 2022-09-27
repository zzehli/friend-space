import React from 'react';
import { createRoot } from 'react-dom/client';
import Post from './post';
import Posts from './posts';

const DATA = [{
    "comments": [
      {
        "commentid": 1,
        "lognameOwnsThis": true,
        "owner": "awdeorio",
        "ownerShowUrl": "/users/awdeorio/",
        "text": "#chickensofinstagram",
        "url": "/api/v1/comments/1/"
      },
      {
        "commentid": 2,
        "lognameOwnsThis": false,
        "owner": "jflinn",
        "ownerShowUrl": "/users/jflinn/",
        "text": "I <3 chickens",
        "url": "/api/v1/comments/2/"
      },
      {
        "commentid": 3,
        "lognameOwnsThis": false,
        "owner": "michjc",
        "ownerShowUrl": "/users/michjc/",
        "text": "Cute overload!",
        "url": "/api/v1/comments/3/"
      }
    ],
    "comments_url": "/api/v1/comments/?postid=3",
    "created": "2021-05-06 19:52:44",
    "imgUrl": "/uploads/9887e06812ef434d291e4936417d125cd594b38a.jpg",
    "likes": {
      "lognameLikesThis": true,
      "numLikes": 1,
      "url": "/api/v1/likes/6/"
    },
    "owner": "awdeorio",
    "ownerImgUrl": "/uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg",
    "ownerShowUrl": "/users/awdeorio/",
    "postShowUrl": "/posts/3/",
    "postid": 3,
    "url": "/api/v1/posts/3/"
  }]
  
// create a root
const root = createRoot(document.getElementById('reactEntry'));
// This method is only called once
// Insert the post component into the DOM
root.render(<Posts data = {DATA} />);
  