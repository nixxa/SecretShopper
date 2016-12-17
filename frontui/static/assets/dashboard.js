webpackJsonp([0],{

/***/ 0:
/*!******************************!*\
  !*** ./src/js/dashboard.jsx ***!
  \******************************/
/***/ function(module, exports, __webpack_require__) {

	'use strict';
	
	var _react = __webpack_require__(/*! react */ 1);
	
	var _react2 = _interopRequireDefault(_react);
	
	var _reactDom = __webpack_require__(/*! react-dom */ 32);
	
	var _reactDom2 = _interopRequireDefault(_reactDom);
	
	__webpack_require__(/*! bootswatch/yeti/bootstrap.css */ 178);
	
	__webpack_require__(/*! ../css/base.less */ 185);
	
	var _layout = __webpack_require__(/*! ./containers/layout.jsx */ 186);
	
	var _layout2 = _interopRequireDefault(_layout);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	_reactDom2.default.render(_react2.default.createElement(_layout2.default, null), document.getElementById('app'));

/***/ },

/***/ 178:
/*!*****************************************!*\
  !*** ./~/bootswatch/yeti/bootstrap.css ***!
  \*****************************************/
/***/ function(module, exports) {

	// removed by extract-text-webpack-plugin

/***/ },

/***/ 185:
/*!***************************!*\
  !*** ./src/css/base.less ***!
  \***************************/
/***/ function(module, exports) {

	// removed by extract-text-webpack-plugin

/***/ },

/***/ 186:
/*!**************************************!*\
  !*** ./src/js/containers/layout.jsx ***!
  \**************************************/
/***/ function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; };
	
	var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();
	
	var _react = __webpack_require__(/*! react */ 1);
	
	var _react2 = _interopRequireDefault(_react);
	
	var _lodash = __webpack_require__(/*! lodash */ 187);
	
	var _lodash2 = _interopRequireDefault(_lodash);
	
	__webpack_require__(/*! ../../css/layout.less */ 190);
	
	var _card = __webpack_require__(/*! ../components/card.jsx */ 191);
	
	var _card2 = _interopRequireDefault(_card);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }
	
	function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }
	
	function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }
	
	var Layout = function (_React$Component) {
	    _inherits(Layout, _React$Component);
	
	    function Layout(props) {
	        _classCallCheck(this, Layout);
	
	        var _this = _possibleConstructorReturn(this, (Layout.__proto__ || Object.getPrototypeOf(Layout)).call(this, props));
	
	        _this.state = {};
	        _this.state.firstColumn = [{
	            id: 1,
	            title: '#2 - Звягино',
	            text: 'АЗК с магазином и кафе',
	            date: '01.12.2016',
	            month: 'декабрь',
	            status: 'new'
	        }, {
	            id: 2,
	            title: '#3 - Нудоль',
	            text: 'АЗК с магазином и кафе',
	            date: '05.12.2016',
	            month: 'декабрь',
	            status: 'new'
	        }];
	        _this.state.secondColumn = [];
	        return _this;
	    }
	
	    _createClass(Layout, [{
	        key: 'handleDragOver',
	        value: function handleDragOver(e) {
	            e.preventDefault();
	            console.log('DragOver:' + e);
	        }
	    }, {
	        key: 'handleDrop',
	        value: function handleDrop(e) {
	            e.preventDefault();
	            var cardId = e.dataTransfer.getData("id");
	            var array1 = this.state.firstColumn;
	            var array2 = this.state.secondColumn;
	
	            var indx = _lodash2.default.findIndex(array2, function (o) {
	                return o.id === +cardId;
	            });
	            if (indx >= 0) {
	                var elem = array2[indx];
	                array2.splice(indx, 1);
	                array1.push(elem);
	                this.setState({
	                    firstColumn: array1,
	                    sendColumn: array2
	                });
	            }
	        }
	    }, {
	        key: 'handleDrop2',
	        value: function handleDrop2(e) {
	            e.preventDefault();
	            var cardId = e.dataTransfer.getData("id");
	            var array1 = this.state.firstColumn;
	            var array2 = this.state.secondColumn;
	
	            var indx = _lodash2.default.findIndex(array1, function (o) {
	                return o.id === +cardId;
	            });
	            if (indx >= 0) {
	                var elem = array1[indx];
	                array1.splice(indx, 1);
	                array2.push(elem);
	                this.setState({
	                    firstColumn: array1,
	                    sendColumn: array2
	                });
	            }
	        }
	    }, {
	        key: 'handleDragStart',
	        value: function handleDragStart(e) {
	            console.log('DragStart:' + e);
	        }
	    }, {
	        key: 'render',
	        value: function render() {
	            var _this2 = this;
	
	            return _react2.default.createElement(
	                'div',
	                { className: 'dashboard' },
	                _react2.default.createElement(
	                    'div',
	                    { className: 'row' },
	                    _react2.default.createElement(
	                        'div',
	                        { className: 'col-xs-12 col-sm-12 col-md-12 col-lg-8' },
	                        _react2.default.createElement(
	                            'h3',
	                            null,
	                            '\u041E\u0442\u0447\u0435\u0442\u043D\u044B\u0439 \u043F\u0435\u0440\u0438\u043E\u0434 - \u0414\u0435\u043A\u0430\u0431\u0440\u044C 2016'
	                        ),
	                        this.props.children
	                    ),
	                    _react2.default.createElement('div', { className: 'col-xs-12' }),
	                    _react2.default.createElement(
	                        'div',
	                        { className: 'col-md-3' },
	                        _react2.default.createElement(
	                            'h4',
	                            null,
	                            '\u041D\u043E\u0432\u044B\u0435',
	                            _react2.default.createElement('hr', null)
	                        )
	                    ),
	                    _react2.default.createElement(
	                        'div',
	                        { className: 'col-md-3' },
	                        _react2.default.createElement(
	                            'h4',
	                            null,
	                            '\u041D\u0430 \u043F\u0440\u043E\u0432\u0435\u0440\u043A\u0435',
	                            _react2.default.createElement('hr', null)
	                        )
	                    ),
	                    _react2.default.createElement(
	                        'div',
	                        { className: 'col-md-3' },
	                        _react2.default.createElement(
	                            'h4',
	                            null,
	                            '\u041D\u0430 \u043F\u043E\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043D\u0438\u0438',
	                            _react2.default.createElement('hr', null)
	                        )
	                    ),
	                    _react2.default.createElement(
	                        'div',
	                        { className: 'col-md-3' },
	                        _react2.default.createElement(
	                            'h4',
	                            null,
	                            '\u0413\u043E\u0442\u043E\u0432\u044B',
	                            _react2.default.createElement('hr', null)
	                        )
	                    )
	                ),
	                _react2.default.createElement(
	                    'div',
	                    { className: 'row flex-container' },
	                    _react2.default.createElement(
	                        'div',
	                        { className: 'col-md-3', onDragOver: this.handleDragOver.bind(this), onDrop: this.handleDrop.bind(this) },
	                        this.state.firstColumn.map(function (item, i) {
	                            return _react2.default.createElement(_card2.default, _extends({ key: i }, item, { dragStart: _this2.handleDragStart.bind(_this2) }));
	                        })
	                    ),
	                    _react2.default.createElement(
	                        'div',
	                        { className: 'col-md-3', onDragOver: this.handleDragOver.bind(this), onDrop: this.handleDrop2.bind(this) },
	                        this.state.secondColumn.map(function (item, i) {
	                            return _react2.default.createElement(_card2.default, _extends({ key: i }, item, { dragStart: _this2.handleDragStart.bind(_this2) }));
	                        })
	                    ),
	                    _react2.default.createElement('div', { className: 'col-md-3' }),
	                    _react2.default.createElement('div', { className: 'col-md-3' })
	                )
	            );
	        }
	    }]);
	
	    return Layout;
	}(_react2.default.Component);
	
	exports.default = Layout;

/***/ },

/***/ 190:
/*!*****************************!*\
  !*** ./src/css/layout.less ***!
  \*****************************/
/***/ function(module, exports) {

	// removed by extract-text-webpack-plugin

/***/ },

/***/ 191:
/*!************************************!*\
  !*** ./src/js/components/card.jsx ***!
  \************************************/
/***/ function(module, exports, __webpack_require__) {

	"use strict";
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();
	
	var _react = __webpack_require__(/*! react */ 1);
	
	var _react2 = _interopRequireDefault(_react);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }
	
	function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }
	
	function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }
	
	var Card = function (_React$Component) {
	    _inherits(Card, _React$Component);
	
	    function Card(props) {
	        _classCallCheck(this, Card);
	
	        return _possibleConstructorReturn(this, (Card.__proto__ || Object.getPrototypeOf(Card)).call(this, props));
	    }
	
	    _createClass(Card, [{
	        key: "handleDragStart",
	        value: function handleDragStart(e) {
	            e.dataTransfer.setData("id", this.props.id);
	            this.props.dragStart(e);
	        }
	    }, {
	        key: "render",
	        value: function render() {
	            return _react2.default.createElement(
	                "div",
	                { className: "panel panel-default", draggable: "true", onDragStart: this.handleDragStart.bind(this) },
	                _react2.default.createElement(
	                    "div",
	                    { className: "panel-heading" },
	                    this.props.title
	                ),
	                _react2.default.createElement(
	                    "div",
	                    { className: "panel-body" },
	                    this.props.text,
	                    _react2.default.createElement("br", null),
	                    "\u0414\u0430\u0442\u0430: ",
	                    this.props.date,
	                    _react2.default.createElement("br", null),
	                    "\u041C\u0435\u0441\u044F\u0446: ",
	                    _react2.default.createElement(
	                        "a",
	                        { href: "" },
	                        this.props.month
	                    ),
	                    _react2.default.createElement("br", null),
	                    _react2.default.createElement(
	                        "div",
	                        { className: "pull-right" },
	                        _react2.default.createElement(
	                            "a",
	                            { href: "#", className: "btn btn-link" },
	                            _react2.default.createElement("i", { className: "glyphicon glyphicon-eye-open" })
	                        ),
	                        _react2.default.createElement(
	                            "a",
	                            { href: "#", className: "btn btn-link" },
	                            _react2.default.createElement("i", { className: "glyphicon glyphicon-edit" })
	                        ),
	                        _react2.default.createElement(
	                            "a",
	                            { href: "#", className: "btn btn-link" },
	                            _react2.default.createElement("i", { className: "glyphicon glyphicon-plus" })
	                        )
	                    )
	                )
	            );
	        }
	    }]);
	
	    return Card;
	}(_react2.default.Component);
	
	Card.propTypes = {
	    id: _react2.default.PropTypes.number.isRequired,
	    status: _react2.default.PropTypes.string.isRequired,
	    title: _react2.default.PropTypes.string.isRequired,
	    text: _react2.default.PropTypes.string.isRequired,
	    date: _react2.default.PropTypes.string.isRequired,
	    month: _react2.default.PropTypes.string.isRequired,
	    dragStart: _react2.default.PropTypes.func.isRequired
	};
	
	exports.default = Card;

/***/ }

});
//# sourceMappingURL=dashboard.js.map