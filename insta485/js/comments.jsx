import React from 'react';
import PropTypes from 'prop-types';
import CommentAdd from './newcomment'
class CommentList extends React.Component{
    render() {
        const {comments} = this.props;
        return (
            <div>
                <ul>
                    {comments.map(elem => (
                        <li key = {elem.commentid}>
                            {elem.text}
                        </li>
                    ))}
                </ul>
                <CommentAdd fish=""/>
            </div>
        )
    }
}

export default CommentList;