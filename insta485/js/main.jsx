import React from 'react';
import { createRoot } from 'react-dom/client';
import Post from './post';
// create a root
const root = createRoot(document.getElementById('reactEntry'));
// This method is only called once
// Insert the post component into the DOM
root.render(<Post url="/api/v1/posts/1/" />);