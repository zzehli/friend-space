import React from 'react';
import { createRoot } from 'react-dom/client';
import PostList from './posts';

// create a root
const root = createRoot(document.getElementById('reactEntry'));
// This method is only called once
// Insert the post component into the DOM
root.render(<PostList url = "/api/v1/posts/?size=5" />);
  