/** @odoo-module **/

import { WebClient } from "@web/webclient/webclient";
import { patch } from "@web/core/utils/patch";
import { session } from "@web/session";
import rpc from 'web.rpc';


//patch(WebClient.prototype, "digisuite_custom.WebClient", {
//    setup() {
//            this._super.apply(this, arguments);
//            var domain = session.user_companies.allowed_companies;
//            this.title.setParts({ zopenerp: "New title" }); // zopenerp is easy to grep
//            var obj = this;
//            var def = rpc.query({
//                fields: ['name','id',],
//                model: 'res.config.settings',
//                method: 'current_company_id',
//                args: [domain, domain],
//            })
//                .then(function (result) {
//                const app_system_name = session.app_system_name || 'New title';
//                obj.title.setParts({ zopenerp: result }); // zopenerp is easy to grep
//            });
//    }
//});

patch(WebClient.prototype, "digisuite_custom.WebClient", {
setup() {
this._super.apply(this, arguments);
const app_system_name = 'Digisuite';
this.title.setParts({ zopenerp: app_system_name }); // zopenerp is easy to grep
}
});
