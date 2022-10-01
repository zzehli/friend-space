import React from 'react';
import PropTypes from 'prop-types';
import CommentAdd from './newcomment'
class CommentList extends React.Component{
    constructor(props) {
        super(props)

        this.handleValueChange = this.handleValueChange.bind(this)
        this.handleSubmit = this.handleSubmit.bind(this)
        this.state = {value: '',
                      comments: props.comments};
    }


    handleValueChange(input){
        this.setState({value: input});
    }
    // need to add new comment into db
    //TODO: 1 where to make the POST comment api call
    //TODO: 2 how to initialize the comments value
    handleSubmit(comment){
        console.log('wait to be added')
        // console.log(this.props.comments.length)

    }

    render() {
        const {comments} = this.props;
        const input = this.state.value
        console.log(this.props.comments.length)
        return (
            <div>
                <ul>
                    {comments.map(elem => (
                        <li key = {elem.commentid}>
                            {elem.text}
                        </li>
                    ))}
                </ul>
                <CommentAdd value = {input}
                            onValueChange = {this.handleValueChange}
                            onSubmit = {this.handleSubmit}/>
            </div>
        )
    }
}

export default CommentList;