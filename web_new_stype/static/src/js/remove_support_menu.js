openerp.web_new_stype = function (instance) {
    var QWeb = instance.web.qweb,
        _t = instance.web._t;

    if(openerp.im_chat){
        openerp.im_chat.InstantMessaging.include({

            start: function(){
                console.log('tao deo start function nay len nua');
                this._super.apply(this, arguments);
                this.$('.odoo_support_contact').remove();
            }
        });
    }

    instance.web.WebClient = instance.web.WebClient.extend({
        show_application: function () {
            this._super.apply(this, arguments);
        },
        _ab_location: function (dbuuid) {
            this._super.apply(this, arguments);
        },

        show_annoucement_bar: function () {
            this._super.apply(this, arguments);
        },

        init: function (parent, client_options) {
            console.log('WebClient init()');
            this._super(parent);
            this.set('title_part', {"zopenerp": "FEOS"});
        },

        set_title: function (title) {
            console.log('WebClient set_title()');
            title = _.str.clean(title);
            var sep = _.isEmpty(title) ? '' : '- FEOS';
            document.title = title + sep;
        }
    });

    instance.web.UserMenu.include({

        on_menu_help: function () {
            window.open('http://help.feosco.com', '_blank');
        }

    });
}