import React from 'react';
import PropTypes from 'prop-types';
class Post extends React.Component {
  /* Display number of image and post owner of a single post
   */
  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = { imgUrl: '', owner: '' };
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
          owner: data.owner
        });
      })
      .catch((error) => console.log(error));
  }
  render() {
    // This line automatically assigns this.state.imgUrl to the const variable imgUrl
    // and this.state.owner to the const variable owner
    const { imgUrl, owner } = this.state;
    // Render number of post image and post owner
    return (
      <div className="post">
        <img src={imgUrl} />
        <p>
          {owner}
        </p>
      </div>
    );
  }
}
Post.propTypes = {
  url: PropTypes.string.isRequired,
};
export default Post;