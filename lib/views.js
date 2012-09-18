/**
 * Show functions to be exported from the design doc.
 */

exports.recipe_titles = {
    map: function (doc) {
        if (doc.type === 'recipe') {
            emit(doc.title, null);
        }
    }
};

exports.recipe_text = {
    map: function (doc) {
        if (doc.type === 'recipe' && doc.text) {
            emit(doc.title, doc.text);
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

exports.categories = {
    map: function (doc) {
        if (doc.type === 'recipe' && doc.categories) {
            for (category in doc.categories) {
                emit(doc.categories[category]['*'].replace(/_/g, ' '), null);
            }
        }
    },
    
    reduce: function(keys, values, rereduce) {
        return true;
    }
};
