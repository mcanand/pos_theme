odoo.define('pos_custom_theme.PaymentScreen', function (require) {
    'use strict';

    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const { isConnectionError } = require('point_of_sale.utils');
    const useSelectEmployee = require('pos_hr.useSelectEmployee');

    const PosThemePaymentScreen = (PaymentScreen) => class extends PaymentScreen {
        async validateOrder(isForceValidate) {
            if(this.env.pos.config.auto_invoice){
                var currentOrder = this.env.pos.get_order();
                currentOrder.set_to_invoice(!currentOrder.is_to_invoice());
            }
            return super.validateOrder(...arguments);
        }
    };
    Registries.Component.extend(PaymentScreen, PosThemePaymentScreen);
    return PaymentScreen;
});