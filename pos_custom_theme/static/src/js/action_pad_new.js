odoo.define('pos_custom_theme.ActionPadNew', function(require) {
    'use strict';

    const { useState } = owl.hooks;
    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');
    const ProductsWidget = require('point_of_sale.ProductsWidget');
    const { useRef } = owl.hooks;
    const { debounce } = owl.utils;

    class ActionPadNew extends ProductsWidget{
          constructor() {
                super(...arguments);
//                this.searchWordInput = useRef('search-word-input');
//                this.updateSearch = debounce(this.updateSearch, 100);
//                this.state = useState({ searchWord: '' });
//                console.log(PosComponent)
          }
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
          async UpdateQtyBarcodeInput(){
                var qty = $('#InputBarcodeUpdateQty').val()
                if (parseInt(qty)){
                    $('#InputBarcodeUpdateQty').val(parseInt(qty) + 1)
                }else{
                    $('#InputBarcodeUpdateQty').val(1)
                }
          }
          async ClickClearAllLines(){
            var order = this.env.pos.get_order()
            var order_lines = order.get_orderlines()
            if(order && order_lines.length >= 1){
                this.showPopup('NumberPopupCustom', {
                    isPassword: true,
                    title: this.env._t('Manager Password ?'),
                    startingValue: false,
                    cachier: this.env.pos.get_cashier(),
                    order_remove: true,
                    error: false,
                });

            }
        }

//          _toggleMobileSearchbar() {
//                this.trigger('toggle-mobile-searchbar');
//          }
//          clearSearch() {
//                this.searchWordInput.el.value = '';
//                this.trigger('clear-search');
//          }
//          updateSearch(event) {
//                this.trigger('update-search', event.target.value);
//                console.log(this.trigger('update-search', event.target.value))
//                this.state.searchWord = event.target.value;
//                if (event.key === 'Enter') {
//                    console.log('usss')
//                // We are passing the searchWordInput ref so that when necessary,
//                // it can be modified by the parent.
//                     this.trigger('try-add-product', { searchWordInput: this.searchWordInput });
//                }
//                this.trigger('change', this)
//          }
//          async loadProductFromDB() {
//            if(!this.searchWordInput.el.value)
//                return;
//
//            try {
//                let ProductIds = await this.rpc({
//                    model: 'product.product',
//                    method: 'search',
//                    args: [['&',['available_in_pos', '=', true], '|','|',
//                     ['name', 'ilike', this.searchWordInput.el.value],
//                     ['default_code', 'ilike', this.searchWordInput.el.value],
//                     ['barcode', 'ilike', this.searchWordInput.el.value]]],
//                    context: this.env.session.user_context,
//                });
//                if(!ProductIds.length) {
//                    this.showPopup('ErrorPopup', {
//                        title: '',
//                        body: this.env._t("No product found"),
//                    });
//                } else {
//                    await this.env.pos._addProducts(ProductIds, false);
//                }
//                this.trigger('update-product-list');
//            } catch (error) {
//                const identifiedError = identifyError(error)
//                if (identifiedError instanceof ConnectionLostError || identifiedError instanceof ConnectionAbortedError) {
//                    return this.showPopup('OfflineErrorPopup', {
//                        title: this.env._t('Network Error'),
//                        body: this.env._t("Product is not loaded. Tried loading the product from the server but there is a network error."),
//                    });
//                } else {
//                    throw error;
//                }
//            }
//        }
    }
    ActionPadNew.template = 'ActionPadNew';
    ActionPadNew.defaultProps = {
        isActionButtonHighlighted: false,
    }

    Registries.Component.add(ActionPadNew);

    return ActionPadNew;
});
