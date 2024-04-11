odoo.define('requisitos.dynamic_row_color', function (require) {
    "use strict";

    var ListRenderer = require('web.ListRenderer');

    ListRenderer.include({
        _renderRow: function (record) {
            var $row = this._super.apply(this, arguments);
            if (record.data.is_done) {
                $row.addClass('done_row');
            }
            return $row;
        },
        _renderBodyCell: function (record, node) {
            var $td = this._super.apply(this, arguments);
            if (node.attrs.name === 'state') {
                var state = record.data['state'];
                $td.addClass(state.toLowerCase() + '-state');
            }
            return $td;
        },
    });

});
