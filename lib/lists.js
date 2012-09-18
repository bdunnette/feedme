/**
 * List functions to be exported from the design doc.
 */

var templates = require('duality/templates');

exports.recipe_list = function (head, req) {

    start({code: 200, headers: {'Content-Type': 'text/html'}});

    // fetch all the rows
    var recipe, recipes= [];

    while (recipe = getRow()) {
        recipes.push(recipe);
    }

    // generate the markup for a list of transactions
    var content = templates.render('recipe_list.html', req, {
        recipes: recipes
    });

    return {title: 'Recipe Index', content: content};

};
