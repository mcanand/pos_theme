odoo.define('point_of_sale.ActionPadNew', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');

    class ActionPadNew extends PosComponent {
          async ClickAddLineDescription(){
                const selectedOrderline = this.env.pos.get_order().get_selected_orderline();
                if (!selectedOrderline) return;

                const { confirmed, payload: inputNote } = await this.showPopup('TextAreaPopup', {
                    startingValue: selectedOrderline.get_customer_note(),
                    title: this.env._t('Add Customer Note'),
                });

                if (confirmed) {
                    selectedOrderline.set_customer_note(inputNote);
                }
          }
          async ClickShowProductInfo(){
                console.log(this.env.pos.get_order())
                const orderline = this.env.pos.get_order().get_selected_orderline();
                if (orderline) {
                    const product = orderline.get_product();
                    const quantity = orderline.get_quantity();
                    const info = await this.env.pos.getProductInfo(product, quantity);
                    this.showPopup('ProductInfoPopup', { info: info , product: product });
                }
          }
          async ClickShowOrders(){
               this.showScreen('TicketScreen',{
                ui: { filter: 'SYNCED' },
               });
          }
          async ClickQtyUpdatePlus(){
                var order_line = this.env.pos.get_order().get_selected_orderline()
                if(order_line){
                    var quantity = order_line.quantity + 1
                    order_line.set_quantity(quantity)
                }
                this.env.pos.get_order().trigger('change');
          }
          async ClickQtyUpdateMinus(){
                var order_line = this.env.pos.get_order().get_selected_orderline()
                if(order_line){
                    var quantity = order_line.quantity - 1
                    if (quantity >= 0){
                        order_line.set_quantity(quantity)
                    }
                }
                this.env.pos.get_order().trigger('change');
          }
          async ClickDeleteLine(){
               var order = this.env.pos.get_order()
               var order_line = order.get_selected_orderline()
               if(order && order_line){
                    order.remove_orderline(order_line)
                    order.trigger('change');
               }

          }
    }
    ActionPadNew.template = 'ActionPadNew';
    ActionPadNew.defaultProps = {
        isActionButtonHighlighted: false,
    }

    Registries.Component.add(ActionPadNew);

    return ActionPadNew;
});
