odoo.define('pos_custom_theme.ProductInfoEditPopup', function (require) {
    'use strict';

    const Registries = require('point_of_sale.Registries');
    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    var core = require('web.core');
    var _t = core._t;

    class ProductInfoEditPopup extends AbstractAwaitablePopup {
        constructor() {
            super(...arguments);
            this.props.line = this.env.pos.get_order().get_selected_orderline() || false;
            this.ConvertDiscount(this.props.line.discount)
        }
        async ConvertDiscount(disc){
            if(parseFloat(disc)){
                var amount = ((parseFloat(disc) * this.props.line.price)/ 100 )
                var amt = this.env.pos.format_currency_no_symbol(amount)
                this.discount_amount = amt
            }
        }
        async onKeyUpDiscountAmt(event){
            var input = event.target.value
//            if(event.key == 'Enter'){

                if(event.target.name=='name'){
                    this.props.line.product.display_name = input
                    this.props.line.full_product_name = input
                }
                if(!input){
                    input = 0
                }
                if(event.target.name=='discount_amt'){
                    var discount_perc = (parseFloat(input) / this.props.line.price) * 100
                    var disc = this.env.pos.format_currency_no_symbol(discount_perc)
                    this.props.line.set_discount(disc)
                }
                else if(event.target.name=='discount_perc'){
                    this.props.line.set_discount(parseFloat(input))
                }
                else if(event.target.name == 'rate'){
                      this.props.line.price = parseFloat(input)
                      this.props.line.trigger('change')
                }
                else if(event.target.name == 'qty'){
                      this.props.line.set_quantity(parseFloat(input))
                      this.props.line.trigger('change')
                }
//            }
            else if(event.key == 'ArrowUp'){
                var input_list = $('.ProductInfoEditPopup input')
                var indexes = []
                _.each(input_list, function(tag, index){
                    if(event.target.name == tag.name){
                        indexes.push(index)
                    }
                });
                var new_index = indexes[0] - 1
                if(new_index < 0){
                    new_index = input_list.length - 1
                }
                if(new_index >= 0){
                    input_list[new_index].focus();
                }
            }
            else if(event.key == 'ArrowDown'){
                var input_list = $('.ProductInfoEditPopup input')
                var indexes = []
                _.each(input_list, function(tag, index){
                    if(event.target.name == tag.name){
                        indexes.push(index)
                    }
                });
                var new_index = indexes[0] + 1
                if(new_index > input_list.length - 1){
                    new_index = 0
                }
                if(new_index >= 0){
                    input_list[new_index].focus();
                }
            }
            this.env.pos.get_order().set_total_discount_amt()
            this.props.line.trigger('change')
            this.ConvertDiscount()
        }
        async confirm(){
            super.confirm();
        }

    };
    ProductInfoEditPopup.template = 'ProductInfoEditPopup';
    ProductInfoEditPopup.defaultProps = {
        confirmText: _t('Ok'),
        cancelText: _t('Close'),
        title: _t('Product Info'),
        body: '',
        list: [],
    };
    Registries.Component.add(ProductInfoEditPopup);
});