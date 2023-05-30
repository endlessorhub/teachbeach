//import routes from './routes.js'
const _ = require('lodash')

module.exports = function (source) {
    //console.log(source)
    const text = source.toString()
        .replace(/import (\S+) from (\'|")([^\n]+)(\'|")/gi, 'var $1=0')
        .replace(/\(\) => /gi, 'function () ')
        .replace(/\((\S+)\) => /gi, 'function ($1) ')
        .replace(/(import|export)/gi, '')
        .replace('default', 'return ')
    //console.log(text)
    const routes = eval(`(function () {${text}})()`)
    const plainList = []

    const recursiveMap = (node, parents) => {
        if(node.ignoreSitemap) {
            return
        }
        const plainNode = _.pick(node, ['path', 'name', 'meta', 'redirect'])
        if(_.some((parents || []).concat([node]), n => (n.meta && n.meta.requiresAuth)))
            plainNode.requiresAuth = true
        if(parents)
            plainNode.path = _.map(parents, 'path').concat([plainNode.path]).join('/')
        plainList.push(plainNode)
        if(node.children) {
            const p2 = parents ? parents.concat([node]) : [node]
            _.each(node.children, c => recursiveMap(c, p2))
        }
    }
    _.each(routes, r => recursiveMap(r))

    //console.log(plainList)

    return JSON.stringify({routes: plainList});
}