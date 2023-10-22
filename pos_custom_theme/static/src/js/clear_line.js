odoo.define('pos_custom_buttons.ClearAllButton', function(require) {
'use strict';
   const { Gui } = require('point_of_sale.Gui');
   const PosComponent = require('point_of_sale.PosComponent');
   const { posbus } = require('point_of_sale.utils');
   const ProductScreen = require('point_of_sale.ProductScreen');
   const { useListener } = require('web.custom_hooks');
   const Registries = require('point_of_sale.Registries');
   const PaymentScreen = require('point_of_sale.PaymentScreen');
   class ClearAllButton extends PosComponent {
        ClickClearAllLines(){
            var order = this.env.pos.get_order()
            var order_lines = order.get_orderlines()
            if(order && order_lines){
                for (var i=0;i<=order_lines.length;i++){
                    order.remove_orderline(order_lines[i])
                    order.trigger('change');
                }
            }
        }
   }
   ClearAllButton.template = 'ClearAllButton';
   ProductScreen.addControlButton({
        component: ClearAllButton,
        condition: function() {
            return this.env.pos;
        },
   });
   Registries.Component.add(ClearAllButton);
   return ClearAllButton;
});