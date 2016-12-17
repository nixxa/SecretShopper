import React from 'react';

class Card extends React.Component {
    constructor(props) {
        super(props);
    }
    handleDragStart(e) {
        e.dataTransfer.setData("id", this.props.id);
        this.props.dragStart(e);
    }
    render() {
        return (
            <div className="panel panel-default" draggable="true" onDragStart={this.handleDragStart.bind(this)}>
                <div className="panel-heading">{this.props.title}</div>
                <div className="panel-body">
                    {this.props.text}<br/>
                    Дата: {this.props.date}<br/>
                    Месяц: <a href="">{this.props.month}</a><br/>
                    <div className="pull-right">
                    <a href="#" className="btn btn-link"><i className="glyphicon glyphicon-eye-open"></i></a>
                    <a href="#" className="btn btn-link"><i className="glyphicon glyphicon-edit"></i></a>
                    <a href="#" className="btn btn-link"><i className="glyphicon glyphicon-plus"></i></a>
                    </div>
                </div>
            </div>
        );
    }
}

Card.propTypes = {
    id: React.PropTypes.number.isRequired,
    status: React.PropTypes.string.isRequired,
    title: React.PropTypes.string.isRequired,
    text: React.PropTypes.string.isRequired,
    date: React.PropTypes.string.isRequired,
    month: React.PropTypes.string.isRequired,
    dragStart: React.PropTypes.func.isRequired
}

export default Card;