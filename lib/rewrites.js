/**
 * Rewrite settings to be exported from the design doc
 */

module.exports = [
    {from: '/static/*', to: 'static/*'},
    {from: '/bootstrap/*', to: 'bootstrap/*'},
    {from: '/kanso-topbar/*', to: 'kanso-topbar/*'},
    {from: '/', to: '_list/recipe_list/recipe_titles'},
    {from: '*', to: '_show/not_found'}
];
