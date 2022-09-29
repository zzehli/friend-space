import React from 'react';
import PropTypes from 'prop-types';
import CommentList from './comments'
class Post extends React.Component {
  /* Display number of image and post owner of a single post*/
  constructor(props) {
    // Initialize mutable state
    // TODO: initialize all properties
    super(props);
    this.state = { imgUrl: '', 
                   owner: '',
                   comments: [] };
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
          <CommentList comments = {comments}/>
          {/* {comments.map( elem => (
            <div key = {elem.commentid}>
              {elem.text}
            </div>
          ))} */}
        </div>
      </div>
    );
  }
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};
export default Post;