import React from 'react';
import PropTypes from 'prop-types';
// import CommentList from './comments'
import CommentAdd from './newcomment'
import Like from './like'

class Post extends React.Component {
  /* Display number of image and post owner of a single post*/
  constructor(props) {
    // Initialize mutable state
    // TODO: initialize all properties
    super(props);


    this.handleValueChange = this.handleValueChange.bind(this)
    this.handleSubmit = this.handleSubmit.bind(this)
    this.handleClick = this.handleClick.bind(this)


    this.state = { commentInput: '',
                   imgUrl: '', 
                   owner: '',
                   comments: [],
                   likes: {} };
  }

  handleValueChange(input){
    this.setState({commentInput: input})
  }

  handleSubmit(comment){
    // console.log(comment)
    
    const postid = this.state.postShowUrl.split('/')[2]
    // console.log(postid)
    // console.log('hjere?')
    // console.log(JSON.stringify({'text': comment}))
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
    this.setState({commentInput:''})
  }

  handleClick(liked){
    const postid = this.state.postShowUrl.split('/')[2]
    let newLike = liked? this.state.likes.numLikes-1: this.state.likes.numLikes+1
    console.log(this.state.likes)

    if (!liked) {
      fetch('/api/v1/likes/' + '?' + new URLSearchParams({postid : postid}), 
      {method: 'POST',
      headers: {'Content-Type': 'application/json'},
      credentials: 'same-origin'})
      .then(res => res.json())
      .then(
        (res) => {
          this.setState(prevState => ({
            likes: {
              ...prevState.likes,
              numLikes: newLike,
              lognameLikesThis: true,
              url: res.url
            }
          }))
          },
        (error) => {console.log(error)}
    )} else {
      let likeId = this.state.likes.url.split('/')[4]
      fetch('/api/v1/likes/' + likeId + '/', 
      {method: 'DELETE',
      headers: {'Content-Type': 'application/json'},
      credentials: 'same-origin'})
      .then(res => res)
      .then(
        (res) => {
          this.setState(prevState => ({
            likes: {
              ...prevState.likes,
              numLikes: newLike,
              lognameLikesThis: false
            }
          }))
          },
        (error) => {console.log(error)}
        )
        }    
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
          comments: data.comments,
          likes: data.likes
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
          <p className='likes'>{this.state.likes.numLikes}</p>
          <div className = "comments">
            {comments.map( elem => (
              <p key = {elem.commentid}><a href = {elem.ownerShowUrl}>{elem.owner}</a>
                {elem.text}
              </p>
            ))}
            <CommentAdd value = {input}
                      onValueChange = {this.handleValueChange}
                      onSubmit = {this.handleSubmit}/>
          </div>
          
          <p className='likes'><Like  value = {this.state.likes}
                                      onClick = {() => this.handleClick(this.state.likes.lognameLikesThis)}/>
          </p>
        </div>
      </div>
    );
  }
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};
export default Post;