odoo.define('pos_custom_theme.GlobalDiscountPopup', function (require) {
    'use strict';

    const Registries = require('point_of_sale.Registries');
    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    var core = require('web.core');
    var _t = core._t;

    class GlobalDiscountPopup extends AbstractAwaitablePopup {
        async CalcDiscAmt(event){
            var percentage = event.target.value
            var total = this.env.pos.get_order().get_total_with_tax()
            var amount = (parseFloat(percentage) / 100) * total
            amount = this.env.pos.format_currency_no_symbol(amount)
            if(parseFloat(percentage) > 100){
                $('.error').html('Should be less than 100')
            }
            else{
                $('.error').html(' ')
            }
            $('.disc_amount').val(amount)
        }
        async CalcDiscPerc(event){
            var amount = event.target.value
            var total = this.env.pos.get_order().get_total_with_tax()
            var percentage = (parseFloat(amount) / total) * 100
            percentage = this.env.pos.format_currency_no_symbol(percentage)
            if(parseFloat(percentage) > 100){
                $('.error').html('Should be less than Total')
            }
            else{
                $('.error').html(' ')
            }
            $('.disc_percentage').val(percentage)
        }
        async confirm(){
            var total = this.env.pos.format_currency_no_symbol(this.env.pos.get_order().get_total_with_tax())
            var val = $('.disc_amount').val();
            if(val < total || val == total){
                 await this.apply_discount_new(val);
                 super.confirm();
            }
        }
        async apply_discount_new(amount){
            if(amount == 0){
                return;
            }
            var order    = this.env.pos.get_order();
            var lines    = order.get_orderlines();
            var product  = this.env.pos.db.get_product_by_id(this.env.pos.config.discount_product_id[0]);
            if (product === undefined) {
                await this.showPopup('ErrorPopup', {
                    title : this.env._t("No discount product found"),
                    body  : this.env._t("The discount product seems misconfigured. Make sure it is flagged as 'Can be Sold' and 'Available in Point of Sale'."),
                });
                return;
            }
            lines.filter(line => line.get_product() === product).forEach(line => order.remove_orderline(line));
            let discount = - amount
            if (discount < 0) {
                await order.add_product(product, {
                    price: discount,
                    lst_price: discount,
                    merge: false,
                    extras: {
                        price_automatically_set: true,
                    },
                });
            }

        }
    };
    GlobalDiscountPopup.template = 'GlobalDiscountPopup';
    GlobalDiscountPopup.defaultProps = {
        confirmText: _t('Apply'),
        cancelText: _t('Close'),
        title: _t('Global Discount'),
        body: '',
        list: [],
    };
    Registries.Component.add(GlobalDiscountPopup);
});