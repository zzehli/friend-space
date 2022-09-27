import React from 'react';
import PropTypes from 'prop-types';
class Posts extends React.Component {
    //determine the len of props
    //make Posts that len with corresponding
    //use key for list

    //first, write a hard-code version of this
    
    //second, replace this with API and state (at this stage, there is no visual change, the state)
    render() {
      const rows = [];
      
      this.props.data.forEach(element => {
        rows.push(
          <Single content = {element}
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

class Single extends React.Component {
    render() {
      return (
        <div>
          <p>{this.props.content.owner}</p>
        </div>
      )
    } 
}


// Posts.propTypes = {
//   url: PropTypes.string.isRequired,
// };
export default Posts;