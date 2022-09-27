import React from 'react';
import PropTypes from 'prop-types';
import Post from './post';

class PostList extends React.Component {

      constructor(props) {
      super(props);
      this.state = {
        next : "",
        pos : []
      };
    }

    componentDidMount() {
      const { url } = this.props;

      fetch(url, { credentials: 'same-origin'})
        .then( res => res.json())
        .then(
          (result) => {
            this.setState({
              next: result.next,
              pos: result.results
            });
          },
          (error) => {
            console.log(error)
          }
        )
    }

    render() {
      const rows = [];
      const {next, pos} = this.state;
      pos.forEach(element => {
        rows.push(
          <Post 
            url = {element.url}
            key = {element.postid}/>
        )
      });
        
      return (
        <div>
          {rows}
        </div>
      )
    }
}


PostList.propTypes = {
  url: PropTypes.string.isRequired,
};
export default PostList;