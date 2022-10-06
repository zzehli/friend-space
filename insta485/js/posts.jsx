import React from 'react';
import PropTypes from 'prop-types';
import Post from './post';
import InfiniteScroll from 'react-infinite-scroll-component';

class PostList extends React.Component {

      constructor(props) {
      super(props);
      this.state = {
        next : "",
        pos : []
      };

      this.fetchMore = this.fetchMore.bind(this)
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
    //append next page to the current page
    //handle edge cases
    fetchMore() {
      const url = this.state.next
      fetch(url, { credentials: 'same-origin'})
        .then( res => res.json())
        .then(
          (result) => { 
            this.setState(prevState => ({
              next: result.next,
              pos: prevState.pos.concat(result.results)
              //or [...prevState.pos, ...result.results]
            }));
          },
          (error) => {
            console.log(error)
          }
        )
    }

    render() {
      const rows = [];
      const {next, pos} = this.state;
      const{ url } = this.props;
      pos.forEach(element => {
        rows.push(
          <Post 
            url = {element.url}
            key = {element.postid}/>
        )
      });
      //TODO: get params for dataLength
      return (
        <div
        style={{
          overflow: 'auto',
        }}
          >
          <InfiniteScroll
            dataLength={this.state.pos.length}
            next={this.fetchMore}
            hasMore={true}
            >
            {rows}
          </InfiniteScroll>   
        </div>
      )
    }
}


PostList.propTypes = {
  url: PropTypes.string.isRequired,
};
export default PostList;