openerp.web_remove_odoo = function (instance) {
    var QWeb = instance.web.qweb,
    _t = instance.web._t;

    instance.web.WebClient = instance.web.WebClient.extend({
        show_application: function() {
            this._super.apply(this, arguments);
        },
        _ab_location: function(dbuuid) {
            this._super.apply(this, arguments);
        },

        show_annoucement_bar: function() {
            this._super.apply(this, arguments);
        },

        init: function(parent, client_options) {
            console.log('WebClient init()');
            this._super(parent);
            this.set('title_part', {"zopenerp": "Hcmulaw"});
            },

        set_title: function(title) {
            console.log('WebClient set_title()');
            title = _.str.clean(title);
            var sep = _.isEmpty(title) ? '' : '- Hcmulaw';
            document.title = title + sep;
        }
    });

    instance.web.UserMenu.include({

        on_menu_help: function() {
            window.open('http://www.hcmulaw.edu.vn/', '_blank');
        }

    });

    instance.web.CrashManager.include({
        rpc_error: function(error) {
            if (!this.active) {
                return;
            }
            var handler = instance.web.crash_manager_registry.get_object(error.data.name, true);
            if (handler) {
                new (handler)(this, error).display();
                return;
            }
            if (error.data.name === "openerp.http.SessionExpiredException" || error.data.name === "werkzeug.exceptions.Forbidden") {
                this.show_warning({type: "Session Expired", data: { message: _t("Your Hcmulaw session expired. Please refresh the current web page.") }});
                return;
            }
            if (error.data.exception_type === "except_osv" || error.data.exception_type === "warning" || error.data.exception_type === "access_error") {
                this.show_warning(error);
            } else {
                this.show_error(error);
            }
        },

        show_warning: function(error) {
            if (!this.active) {
                return;
            }
            if (error.data.exception_type === "except_osv") {
                error = _.extend({}, error, {data: _.extend({}, error.data, {message: error.data.arguments[0] + "\n\n" + error.data.arguments[1]})});
            }
            new instance.web.Dialog(this, {
                size: 'medium',
                title: "Hcmulaw " + (_.str.capitalize(error.type) || "Warning"),
                buttons: [
                    {text: _t("Ok"), click: function() { this.parents('.modal').modal('hide'); }}
                ]
            }, $('<div>' + QWeb.render('CrashManager.warning', {error: error}) + '</div>')).open();
        },

        show_error: function(error) {
            if (!this.active) {
                return;
            }
            var buttons = {};
            buttons[_t("Ok")] = function() {
                this.parents('.modal').modal('hide');
            };
            new instance.web.Dialog(this, {
                title: "Hcmulaw " + _.str.capitalize(error.type),
                buttons: buttons
            }, QWeb.render('CrashManager.error', {session: instance.session, error: error})).open();
        }
    });

    instance.web.RedirectWarningHandler.include({

        display: function() {
            var self = this;
            error = this.error;
            error.data.message = error.data.arguments[0];

            new instance.web.Dialog(this, {
                size: 'medium',
                title: "Hcmulaw " + (_.str.capitalize(error.type) || "Warning"),
                buttons: [
                    {text: _t("Ok"), click: function() { self.$el.parents('.modal').modal('hide');  self.destroy();}},
                    {text: error.data.arguments[2],
                     oe_link_class: 'oe_link',
                     click: function() {
                        window.location.href='#action='+error.data.arguments[1];
                        self.destroy();
                    }}
                ]
            }, QWeb.render('CrashManager.warning', {error: error})).open();
        }
    })


}