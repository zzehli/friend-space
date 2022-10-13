### API
Separated routes into `View` and `api` folders. The view folder handles non-api requests.

### Day 18 
I have started the project a while ago and it's been a week since I made some significant progression on it. I was able to finish most of the API routes that I will use on the client side. The challenge is to rewrite the [pages](https://github.com/zzehli/server-side-instgram/tree/main/insta485/templates) in React. It took me a while to get used to the language of React. I still have some questions, but my understanding of it should be able to finish the current project. In the main page, we are essentially making an API call to get all the posts information and display them on the page. The API call is made on the client side through react component, rather than on the server side. The layout will be very similar to a list, except the content of each item might contain additional information such likes and comments, that will activate further UI changes. The main reference I have are
EECS 485 [tutorial](https://eecs485staff.github.io/p3-insta485-clientside/setup_react.html) on React for API calls
React official tutorial on [API calls](https://reactjs.org/docs/faq-ajax.html)
Same for the [list layout](https://reactjs.org/docs/thinking-in-react.html)

Another challenge that I encounter is the password management in the new implementation. Because API calls demand authentication, (no, api calls will work if the user is in session, therefore, no need to save password anywhere)

### Day 27
I have implemented most of the functionalities of the main page with React. Several tasks remain:
- [x] submit with `enter` key
- [x] add comment deletion function
- [x] double click on unliked image to like
- [x] remove the words in the input after submission
- [x] infinite scroll
- [x] human readable time lapse
- [x] make like count more readable
- [ ] more image into db random, randomize name as well
- [x] add other pages
- [ ] image click effect: https://codepen.io/ash_s_west/pen/GRZbvym
- [x] post page doesn't show like nums
- [ ] bug `posts.py` l:33 include the user itself in post search

### Day 28 
Learning react: despite the amont of tutorials online, the [official doc](https://reactjs.org/docs/hello-world.html) remains an execellent entry point to React. The structure of React can be intimidating at first. It's unclear how it fits the traditional HTML/CSS/JS structure. After reading the official doc, I find it easier to think about JSX as a templated language and the rest of React added functionalities to the templates. The problem with the doc is that it starts with setState and hooks are only introduced later. So it takes time to be able to read more recent React codes that use hooks.