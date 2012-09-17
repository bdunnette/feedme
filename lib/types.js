/**
 * Kanso document types to export
 */

var Type = require('couchtypes/types').Type,
    fields = require('couchtypes/fields'),
    widgets = require('couchtypes/widgets');

exports.recipe = new Type('recipe', {
    fields: {
        title: fields.string(),
        source: fields.string({required: false}),
        ns: fields.number({required: false}),
        pageid: fields.number({required: false}),
        templates: fields.string({required: false}),
        iwlinks: fields.string({required: false}),
        displaytitle: fields.string({required: false}),
        langlinks: fields.string({required: false}),
        links: fields.string({required: false}),
        title: fields.string({required: false}),
        text: fields.string({required: false}),
        revid: fields.string({required: false}),
        externallinks: fields.string({required: false}),
        images: fields.string({required: false}),
        sections: fields.string({required: false}),
        properties: fields.string({required: false}),
        categories: fields.string({required: false})
    }
});
