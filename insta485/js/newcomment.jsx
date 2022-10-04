import React from 'react';
import PropTypes from 'prop-types';

class CommentAdd extends React.Component {
    constructor(props) {
        super(props);

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleKeypress = this.handleKeypress.bind(this);
    }

    handleChange(event) {
        this.props.onValueChange(event.target.value)
    }

    handleSubmit(event) {
        //Q: value is already on the upper level, so basically don't need to 
        //pass anything back.
        this.props.onSubmit(this.props.value)
        event.preventDefault();
    }

    handleKeypress(e) {
        if (e.keyCode === 13) {
            this.handleSubmit(e);
        }
    }

    render() {
        return (
        <p>
            <form onSubmit={this.handleSubmit}>
                <input 
                type="text" 
                value={this.props.value} 
                onChange={this.handleChange}
                onKeyPress={this.handleKeypress}/>
            </form>
        </p>
        );
    }
}


export default CommentAdd;