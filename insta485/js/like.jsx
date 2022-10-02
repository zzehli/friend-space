import React from 'react';

function Like(props) {
    let label = props.value.lognameLikesThis? "unlike": "like";
    return (
        <button onClick={props.onClick}>
            {label}
        </button>
    )
}

export default Like;