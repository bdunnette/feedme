/**
 * Show functions to be exported from the design doc.
 */

exports.recipe_titles = {
    map: function (doc) {
        if (doc.type === 'recipe') {
            emit(doc.title, doc);
        }
    }
};

exports.recipes_without_text = {
    map: function (doc) {
        if (doc.type === 'recipe' && !doc.text) {
            emit(doc._id, doc);
        }
    }
};
