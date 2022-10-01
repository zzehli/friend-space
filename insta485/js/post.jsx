import React from 'react';
import PropTypes from 'prop-types';
// import CommentList from './comments'
import CommentAdd from './newcomment'

class Post extends React.Component {
  /* Display number of image and post owner of a single post*/
  constructor(props) {
    // Initialize mutable state
    // TODO: initialize all properties
    super(props);


    this.handleValueChange = this.handleValueChange.bind(this)
    this.handleSubmit = this.handleSubmit.bind(this)


    this.state = { commentInput: '',
                   imgUrl: '', 
                   owner: '',
                   comments: [] };
  }

  handleValueChange(input){
    this.setState({commentInput: input})
  }
  //TODO: make the POST call upon submit and sync with comments
  handleSubmit(comment){
    // console.log(comment)
    
    const postid = this.state.postShowUrl.split('/')[2]
    // console.log(postid)
    // console.log('hjere?')
    // console.log(JSON.stringify({'text': comment}))
    //compose the query param in the fetch url
    //make the POST request with Fetch
    //update comments in the state
    //alternatively, insert and setstate to the res of get comments request
    // handle error
    fetch('/api/v1/comments/' + '?' + new URLSearchParams({postid : postid}), 
          {method: 'POST',
           headers: {'Content-Type': 'application/json'},
           body: JSON.stringify({text: comment}),
           credentials: 'same-origin'})
        .then(res => res.json())
        .then(
          (res) => {
            this.setState({comments: [...this.state.comments, 
                                      {"commentid": res.commentid,
                                       "lognameOwnsThis":true,
                                       "owner": this.state.owner,
                                       "ownerShowUrl": "/users/" + this.state.owner + "/",
                                       "text": comment,
                                       "url": "/api/v1/comments/"+res.commentid+"/"}]})
            },
          (error) => {console.log(error)}
        )
    // console.log(this.props.comments.length)
  }

  componentDidMount() {
    // This line automatically assigns this.props.url to the const variable url
    const { url } = this.props;
    // Call REST API to get the post's information
    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          imgUrl: data.imgUrl,
          owner: data.owner,
          ownerShowUrl: data.ownerShowUrl,
          ownerImgUrl: data.ownerImgUrl,
          postShowUrl: data.postShowUrl,
          created: data.created,
          comments: data.comments
        });
      })
      .catch((error) => console.log(error));
  }
  render() {
    const { imgUrl, 
            owner, 
            ownerShowUrl, 
            ownerImgUrl, 
            postShowUrl, 
            created,
            comments } = this.state;
    
    const input = this.state.commentInput
    // console.log(postShowUrl)
    // console.log(comments.length)

    // Render number of post image and post owner
    return (
      <div className="card">
        <div className = "cardHeader">
        <a className = "user" href = {ownerShowUrl}>
            <img src={ownerImgUrl}/>
            <p>{owner}</p>
        </a>
        <a className = "timestamp" href = {postShowUrl}>{created}</a>
        </div>
        <img src={imgUrl}/>
        <div className="cardComments">
          {/* <CommentList comments = {comments}/> */}
          {comments.map( elem => (
            <div key = {elem.commentid}>
              {elem.text}
            </div>
          ))}
          <CommentAdd value = {input}
                      onValueChange = {this.handleValueChange}
                      onSubmit = {this.handleSubmit}/>
        </div>
      </div>
    );
  }
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};
export default Post;