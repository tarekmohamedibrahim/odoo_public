odoo.define('web.transtext', function (require) {
    'use strict';

    /**
     *
     This widget adds a transtext ribbon on the form
     If the it is a sheet form, put it before/after the <sheet> tag
     *
     */

    var widgetRegistry = require('web.widget_registry');
    var Widget = require('web.Widget');

    var TransTextWidget = Widget.extend({
        template: 'transtext',
        xmlDependencies: ['/marquee/static/src/xml/marquee.xml'],

        /**
         * @param {string} options.attrs.direction
         * @param {string} options.attrs.bg_color
         * @param {string} options.attrs.tooltip
         * @param {string} options.attrs.speed
         * @param {string} options.attrs.text
         */
        init: function (parent, data, options) {
            this._super.apply(this, arguments);

            if (['left','right','up','down'].includes(options.attrs.direction)){
                this.direction = options.attrs.direction;
            } else {
                this.direction = 'left';
            }
            this.bg_color = options.attrs.bg_color ? options.attrs.bg_color : 'bg-success';
            this.tooltip = options.attrs.tooltip;
            this.speed = options.attrs.speed ? options.attrs.speed : '10'
            this.text = options.attrs.field ? data.data[options.attrs.field] : options.attrs.text;
        },
    });

    widgetRegistry.add('transtext', TransTextWidget);

    return TransTextWidget;
});