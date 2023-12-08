odoo.define('pos_custom_theme.TicketScreen', function (require) {
    'use strict';

    const TicketScreen = require('point_of_sale.TicketScreen');
    const Registries = require('point_of_sale.Registries');
     const { useState } = owl.hooks;
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const { isConnectionError } = require('point_of_sale.utils');
    const useSelectEmployee = require('pos_hr.useSelectEmployee');

    const PosThemeTicketScreen = (TicketScreen) => class extends TicketScreen {
        constructor() {
            super(...arguments);
            if(!this.props.active_orders){
                this.props.active_orders = false
            }
        }
    }
    Registries.Component.extend(TicketScreen, PosThemeTicketScreen);
    return TicketScreen;
});