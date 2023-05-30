export default {
    install(Vue, options) {
        Vue.prototype.openExternalLink = function openExternalLink (url) {
            window.location.href = this.absoluteUrl(url)
        }
        Vue.prototype.absoluteUrl = function (url) {
            return /^http(s|):\/\//.test(url) ? url : `http://${url}`
        }
    }
}