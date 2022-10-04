import React from 'react';
import PropTypes from 'prop-types';

class CommentAdd extends React.Component {
    constructor(props) {
        super(props);

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        this.props.onValueChange(event.target.value)
    }

    handleSubmit(event) {
        //Q: value is already on the upper level, so basically don't need to 
        //pass anything back.
        //TODO: remove the words in the input
        this.props.onSubmit(this.props.value)
        event.preventDefault();
    }

    render() {
        return (
        <p>
            <form onSubmit={this.handleSubmit}>
                <input type="text" value={this.props.value} onChange={this.handleChange}/>
                <input type="submit" value="Submit"/>
            </form>
        </p>
        );
    }
}


export default CommentAdd;