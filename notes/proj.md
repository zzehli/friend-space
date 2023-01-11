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
- [x] add other pages
- [ ] image click effect: https://codepen.io/ash_s_west/pen/GRZbvym
- [x] post page doesn't show like nums
- [x] bug `posts.py` l:33 include the user itself in post search
- [x] bug `EDT` in `routes.py`
- [ ] homepage posting time diff: momentjs
- [x] sql in api posts

### Day 28 
Learning react: despite the amont of tutorials online, the [official doc](https://reactjs.org/docs/hello-world.html) remains an execellent entry point to React. The structure of React can be intimidating at first. It's unclear how it fits the traditional HTML/CSS/JS structure. After reading the official doc, I find it easier to think about JSX as a templated language and the rest of React added functionalities to the templates. The problem with the doc is that it starts with setState and hooks are only introduced later. So it takes time to be able to read more recent React codes that use hooks.

### Date x
`moment.utc(created).fromNow()` This assumes the when server creates the DB, the server is on UTC. Since this piece of code is run on the local browser, `fromNow()` will be able to convert UTC to local time and calculate the time difference. In addition, when you test the code on local machine, it will say "4 hours ago" since even tho the DB is created just now, the browser still assumes that the DB is created at UTC time zone, which is 4 hours ago from ETS.

### Reset procedure
1. reset db
`./bin/fsdb reset`
2. start python venv at project root folder
`source env/bin/activate`
`echo $VIRTUAL_ENV`
2. recompile
`./bin/fsrun`