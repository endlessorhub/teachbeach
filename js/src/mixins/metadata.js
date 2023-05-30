import _ from 'lodash'

export default {
    updated () {
        this.metadataProcessRoute()
    },
    mounted() {
        this.metadataProcessRoute()
    },
    /*
    metaInfo () {
        return {
            title: this.metadata.title || 'TeachBeach',
            meta: [
                { vmid: 'description', name: 'description', content: this.metadata.metatag || 'online learning' }
            ]
        }
    },
    */
    data() {
        return {
            metadata: {},
            metadataTemplate: {},
        }
    },
    methods: {
        metadataProcessRoute() {
            if(!this.$route || this.metadata.alreadySet)
                return
            //this.metadata.alreadySet = true
            const curRoute = _.findLast(this.$route.matched, r => this.$store.state.metatags[r.path]) || _.last(this.$route.matched)
            const curPath = curRoute ? curRoute.path || '/' : null
            if(curRoute && this.$store.state.metatags[curPath]) {
                this.metadataTemplate = {
                    title: this.$store.state.metatags[curPath].title,
                    metatag: this.$store.state.metatags[curPath].metatag,
                }
            }
            this.setMetadata()
        },
        setMetadataTags() {
            Array.from(document.querySelectorAll('[data-vue-meta-controlled]')).map(el => el.parentNode.removeChild(el))
            if(this.metadata.metatag) {
                const tag = document.createElement('meta')
                tag.setAttribute('name', 'description')
                tag.setAttribute('content', this.metadata.metatag)
                tag.setAttribute('data-vue-meta-controlled', '')
                document.head.appendChild(tag)
            }
            document.title = this.metadata.title || 'Teach Beach - online learning'
        },
        setMetadata() {
            this.metadata = {
                title: this.getMetaTitle(),
                metatag: this.getMetaDescription(),
            }
            this.setMetadataTags()
        },
        getMetaTitle() {
            return this.metadataTemplate.title
        },
        getMetaDescription() {
            return this.metadataTemplate.metatag
        }
    },

}