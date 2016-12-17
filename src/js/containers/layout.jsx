import React from 'react';
import _ from 'lodash';

import '../../css/layout.less';

import Card from '../components/card.jsx';

class Layout extends React.Component {
    constructor(props) {
        super(props);

        this.state = {};
        this.state.firstColumn = [{
            id: 1,
            title: '#2 - Звягино',
            text: 'АЗК с магазином и кафе',
            date: '01.12.2016',
            month: 'декабрь',
            status: 'new'
        },
        {
            id: 2,
            title: '#3 - Нудоль',
            text: 'АЗК с магазином и кафе',
            date: '05.12.2016',
            month: 'декабрь',
            status: 'new'
        }];
        this.state.secondColumn = [];
    }
    handleDragOver(e) {
        e.preventDefault();
        console.log('DragOver:' + e);
    }
    handleDrop(e) {
        e.preventDefault();
        let cardId = e.dataTransfer.getData("id");
        let array1 = this.state.firstColumn;
        let array2 = this.state.secondColumn;

        let indx = _.findIndex(array2, (o) => { return o.id === +cardId });
        if (indx >= 0) {
            let elem = array2[indx];
            array2.splice(indx, 1);
            array1.push(elem);
            this.setState({
                firstColumn: array1,
                sendColumn: array2
            });
        }
    }
    handleDrop2(e) {
        e.preventDefault();
        let cardId = e.dataTransfer.getData("id");
        let array1 = this.state.firstColumn;
        let array2 = this.state.secondColumn;

        let indx = _.findIndex(array1, (o) => { return o.id === +cardId });
        if (indx >= 0) {
            let elem = array1[indx];
            array1.splice(indx, 1);
            array2.push(elem);
            this.setState({
                firstColumn: array1,
                sendColumn: array2
            });
        }
    }
    handleDragStart(e) {
        console.log('DragStart:' + e);
    }
    render() {
        return (
            <div className="dashboard">
                <div className="row">
                    <div className="col-xs-12 col-sm-12 col-md-12 col-lg-8">
                        <h3>Отчетный период - Декабрь 2016</h3>
                        { this.props.children }
                    </div>
                    <div className="col-xs-12"></div>

                    <div className="col-md-3"><h4>Новые<hr /></h4></div>
                    <div className="col-md-3"><h4>На проверке<hr /></h4></div>
                    <div className="col-md-3"><h4>На подтверждении<hr /></h4></div>
                    <div className="col-md-3"><h4>Готовы<hr /></h4></div>
                </div>
                <div className="row flex-container">
                    <div className="col-md-3" onDragOver={this.handleDragOver.bind(this)} onDrop={this.handleDrop.bind(this)}>
                        { 
                            this.state.firstColumn.map((item, i) => {
                                return <Card key={i} {...item} dragStart={this.handleDragStart.bind(this)} />
                            })
                        }
                    </div>
                    <div className="col-md-3" onDragOver={this.handleDragOver.bind(this)} onDrop={this.handleDrop2.bind(this)}>
                        { 
                            this.state.secondColumn.map((item, i) => {
                                return <Card key={i} {...item} dragStart={this.handleDragStart.bind(this)} />
                            })
                        }
                    </div>
                    <div className="col-md-3"></div>
                    <div className="col-md-3"></div>
                </div>
            </div>
        );
    }
}

export default Layout;