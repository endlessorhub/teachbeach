<template>
<v-layout align-top justify-center row wrap>
    <v-flex xs12 sm6 class="text-xs-center h-padded">
        <v-autocomplete
            browser-autocomplete="new-password"
            :disabled="isLoading"
            hide-no-data
            hide-details
            dense
            flat
            v-model="cityObj"
            placeholder="City"
            :items="citiesList"
            @change="changeCity"
            label="Location"
        >
        </v-autocomplete>
    </v-flex>
    <v-flex xs12 sm6 class="text-xs-center h-padded">
        <SearchTopic
            v-model="topic"
            :categories="availableCategories"
            :subcategories="availableSubcategories"
        >
        </SearchTopic>
    </v-flex>
</v-layout>
</template>

<script>
import _ from 'lodash'
import SearchTopic from '@/components/basic/SearchTopic.vue'
import axios from 'axios'

export default {
    props: [
        'category',
        'subcategory',
        'city',
        'state',
        'venue',
        'lessonType',
    ],
    components: {
        SearchTopic,
    },
    data: function () {
        return {
            isLoading: false,
            citiesList: [],
            availableCategories: [],
            availableSubcategories: [],
            categoryBtnStyle: {
                'width': '170px',
                'word-break': 'break-word',
                'white-space': 'normal',
                'line-height': '1em',
                'font-family': 'Montserrat, sans-serif',
                'font-weight': '500',
                'font-size': '14px',
                'color': 'rgba(0,0,0,0.87)',
            },
            autocompleteMenuProps: {
                "closeOnClick":false,
                "closeOnContentClick":false,
                "openOnClick":false,
                "maxHeight":'auto',
                "bottom": true,
                "attach": '.type-autocomplete'
            },
            typeInput: '',
        }
    },
    created() {
        this.isLoading = true

        Promise.all([axios.get('/api/cities/'), axios.get('/api/categories/'), axios.get('/api/subcategories/')]).then(([cities, categories, subcategories]) => {
            this.citiesList = _.sortBy(_.map(cities.data, (v) => ({
                text: v.address_city+', '+v.address_state,
                value: v,
                //selected: v.address_city == 'St. Petersburg' &&  v.address_state == 'FL',
            })), c => (c.text.indexOf('St. Petersburg') !== -1 && c.text.indexOf('FL') !== -1 ? '  ' : c.text))
            /*
            this.categoryList = _.map(categories.data, (v) => ({
                text: v.name,
                value: v.id,
            }))
            */
            this.citiesList.unshift({
                text: ' LIVE ONLINE',
                value: {
                    address_city: 'online',
                    address_state: 'none'
                }
            })
            this.availableCategories = categories.data
            this.availableSubcategories = subcategories.data
        }).catch((e1, e2) => {
            console.log('err', e1, e2)
        }).then(() => {
            this.isLoading = false
        })
    },
    methods: {
        onTypeFocus(event) {
            console.log(event)
        },
        typeFilter(item, queryText, itemText) {
            if(queryText.length < 1)
                return false
            return itemText.toLocaleLowerCase().indexOf(queryText.toLocaleLowerCase()) > -1
        },
        changeCity(city) {
            //this.city = city
            setTimeout(() => {
                this.searchClasses()
            }, 100)
        },
        changeType(type) {
            //this.city = city
            setTimeout(() => {
                this.searchClasses()
            }, 100)
        },
        searchClasses() {
            console.log(this.topic, this.selectedLocation)
            let city = 'all',
                state = 'all',
                category = '0',
                subcategory = '0',
                venue = ''
            if(this.cityObj === 'online') {
                city = 'online'
                state = 'none'
            } else if (this.cityObj) {
                city = this.cityObj.address_city
                state = this.cityObj.address_state
            }
            if(this.topic) {
                if(this.topic.type === 'venues') {
                    venue = this.topic.id
                }
                if(this.topic.type === 'categories') {
                    category = this.topic.id
                }
                if(this.topic.type === 'subcategories') {
                    subcategory = this.topic.id
                }
            }
            this.$router.push(`/learners/search/${city}/${state}/${category}/${subcategory}/${this.lessonType || '0'}/${venue}`)
        },
    },
    computed: {
        topic: {
            get() {
                if (this.venue) {
                    return {
                        type: 'venues',
                        id: this.venue,
                    }
                }
                if (this.subcategory) {
                    return {
                        type: 'subcategories',
                        id: Number(this.subcategory),
                    }
                }
                if (this.category) {
                    return {
                        type: 'categories',
                        id: Number(this.category),
                    }
                }
            },
            set(v) {
                this.venue = null
                this.category = null
                this.subcategory = null
                if(v.type === 'venues') {
                    this.venue = v.id
                }
                if(v.type === 'categories') {
                    this.category = v.id
                }
                if(v.type === 'subcategories') {
                    this.subcategory = v.id
                }
                setTimeout(() => {
                    this.searchClasses()
                }, 100)
            }
        },
        cityObj: {
            get() {
                if(this.city && this.state)
                    return {
                        address_city: this.city,
                        address_state: this.state
                    }
                return {}
            },
            set(v) {
                this.city = v.address_city
                this.state = v.address_state
            }
        },
        typesList() {
            if(!this.typeInput && !this.category && !this.subcategory)
                return []
            const categoryDict = _.keyBy(this.availableCategories, 'id')
            const res = _.map(this.availableSubcategories, sc => ({
                value: `${categoryDict[sc.category].id}:${sc.id}`,
                text: `${categoryDict[sc.category].name} - ${sc.name}`
            }))
            _.each(this.availableCategories, (c) => {
                res.push({
                    value: `${c.id}:`,
                    text: ` ${c.name} - All`
                })
            })
            res.unshift({
                value: ':',
                text:  '  All'
            })
            return _.sortBy(res, 'text')
        },
        type: {
            get() {
                const category = _.find(this.availableCategories, {id: Number(this.category)})
                const subCategory = _.find(this.availableSubcategories, {id: Number(this.subcategory)})
                if(!category && !subCategory)
                    return ''
                const res = []
                res.push(category ? category.id : subCategory.category)
                res.push(subCategory ? subCategory.id : '')
                return res.join(':')
            },
            set(v) {
                if(v) {
                    const res = v.split(':')
                    this.category = res[0]
                    if(res.length > 1)
                        this.subcategory = res[1]
                } else {
                    console.log('not found', v)
                }
            }
        },
        locationText() {
            return (_.find(this.citiesList, {value: this.cityObj}) || {}).text
        },
        categoryText() {
            return (_.find(this.typesList, {value: this.type}) || {}).text
        }
    },
    watch: {

    }
}
</script>

<style lang="scss" scoped>

</style>
