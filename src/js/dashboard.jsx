import React from 'react';
import ReactDOM from 'react-dom';

import 'bootswatch/yeti/bootstrap.css';
import '../css/base.less';

import Layout from './containers/layout.jsx';

ReactDOM.render(
   <Layout />,
   document.getElementById('app')
);