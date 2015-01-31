(function(){

    "use strict";

    var _t = openerp._t;
    openerp.im_odoo_support = {};



    if(openerp.im_chat){
        openerp.im_chat.InstantMessaging.include({

            start: function(){
                console.log('tao deo start function nay len nua');
                this._super.apply(this, arguments);
                this.$('.odoo_support_contact').remove();
            }
        });
    }


})();
