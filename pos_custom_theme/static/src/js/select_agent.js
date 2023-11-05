odoo.define('waiter_pos.SelectionPopupAgent', function (require) {
    'use strict';

    const { useState } = owl.hooks;
    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');
    const { _lt } = require('@web/core/l10n/translation');
    const models = require('point_of_sale.models');
    const { Gui } = require('point_of_sale.Gui');
    var rpc = require('web.rpc');
    var core = require('web.core');
    var QWeb = core.qweb;
    var _t = core._t;

    class SelectionPopupAgent extends AbstractAwaitablePopup {
        constructor() {
            super(...arguments);
        }
        async willStart() {
            this.props.list = this.props.list
        }
        selectAgent(agent){
            var order = this.env.pos.get_order();
            order.agent_id = agent.id
            order.trigger('change', order)
            this.cancel()
        }
        _onSearchInputAgent(ev){
            var self = this
            var agents = this.env.pos.agents
            var input = $('.search_input').val()
            var list = []
            agents.forEach(function(agent){
                if(agent.name.toLowerCase().includes(input.toLowerCase())){
                    list.push(agent)
                }
            });
            self.cancel()
            self.showPopup('SelectionPopupAgent', {
                title: self.env._t('Add Agent'),
                list: list,
            });
        }
        RemoveAgent(){
            var order = this.env.pos.get_order()
            order.agent_id = false
            order.trigger('change', order)
            this.cancel()
        }
    }
    SelectionPopupAgent.template = 'SelectionPopupAgent';
    SelectionPopupAgent.defaultProps = {
        confirmText: _lt('Confirm'),
        cancelText: _lt('Cancel'),
        title: _lt('Select'),
        body: '',
        list: [],
    };

    Registries.Component.add(SelectionPopupAgent);

    return SelectionPopupAgent;
});
