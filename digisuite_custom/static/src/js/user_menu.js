/** @odoo-module **/

import { UserMenu } from "@web/webclient/user_menu/user_menu";
import { routeToUrl } from "@web/core/browser/router_service";
import { patch } from "@web/core/utils/patch";
import { browser } from "@web/core/browser/browser";
import { registry } from "@web/core/registry";
import { session } from "@web/session";
const userMenuRegistry = registry.category("user_menuitems");

patch(UserMenu.prototype, "digisuite_custom.UserMenu", {
    setup() {
        this._super.apply(this, arguments);
        userMenuRegistry.remove("documentation");
        userMenuRegistry.remove("support");
        userMenuRegistry.remove("odoo_account");
    },
});
