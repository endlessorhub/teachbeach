<template>
<v-layout align-top justify-center row>
    <v-flex xs12 sm10 md12 lg10 class="text-xs-center">
        <div class="text-lg-center white--text display-1 hidden-xs-only">Find live lessons from local and online experts</div>
        <v-layout align-top justify-center row wrap>
            <v-flex xs12 md3 class="text-xs-center h-padded v-margined">
                <v-menu
                    full-width
                    offset-x
                    :close-on-content-click="false"
                    v-model="locationMenuVisible">
                    <v-btn slot="activator" flat light :style="firstBarStyle">
                        <div>{{selectedLocationText}}</div>
                        <v-spacer></v-spacer>
                        <v-icon v-if="locationMenuVisible">arrow_right</v-icon>
                        <v-icon v-else>arrow_drop_down</v-icon>
                    </v-btn>
                    <v-list dense class="search-home-location-menu">
                        <v-list-tile @click.stop.prevent="setLocation('online')">
                            <v-list-tile-title>Virtual</v-list-tile-title>
                        </v-list-tile>
                        <v-menu
                                full-width
                                offset-x
                                :close-on-content-click="true"
                                right
                                :open-on-hover="!screenXS"
                        >
                            <v-list-tile slot="activator">
                              <v-list-tile-title>Local</v-list-tile-title>
                              <v-spacer></v-spacer>
                              <v-list-tile-action class="justify-end">
                                <v-icon>play_arrow</v-icon>
                              </v-list-tile-action>
                            </v-list-tile>
                            <v-list dense class="search-home-location-menu">
                              <v-list-tile v-for="(c, i) in citiesList" :key="c.value" @click.stop.prevent="setLocation(c.value)">
                                  <v-list-tile-title>{{ c.text }}</v-list-tile-title>
                              </v-list-tile>
                            </v-list>
                        </v-menu>
                        <v-list-tile @click.stop.prevent="setLocation('')">
                            <v-list-tile-title>All</v-list-tile-title>
                        </v-list-tile>
                    </v-list>
                </v-menu>
            </v-flex>
            <v-flex xs12 md9 class="text-xs-center h-padded v-margined">
                <v-layout align-top justify-center row wrap>
                    <v-flex xs12 class="text-xs-center" style="display: flex;" :style="secondBarStyle">
                        <SearchTopic
                            data-mobile-search-topic
                            v-model="topic"
                            label="Type in"
                            placeholder="What Do You Want To Learn?"
                            style="padding-left: 16px;"
                        >
                        </SearchTopic>
                        <v-btn
                            class="hidden-xs-only"
                            color="platform-green"
                            dark
                            @click="searchClasses"
                            aria-label="search"
                            :loading="isLoading"
                            :disabled="isInitialLoading"
                        >
                            <v-icon >search</v-icon>
                        </v-btn>
                    </v-flex>
                    <v-flex xs12 class="text-xs-center hidden-sm-and-up">
                        <v-btn color="platform-green" dark block @click="searchClasses" aria-label="search" :loading="isLoading" :disabled="isInitialLoading">
                            GO
                        </v-btn>
                    </v-flex>
                </v-layout>
                <div class="text-xs-left"><router-link to="/teachers/light-register" style="color: white;">Become an instructor</router-link></div>
            </v-flex>
        </v-layout>
    </v-flex>
</v-layout>
</template>

<script>
import _ from 'lodash'
import axios from 'axios'
const CancelToken = axios.CancelToken;
const source = CancelToken.source();
import SearchTopic from '@/components/basic/SearchTopic.vue'

export default {
    props: [
        'category',
        'subcategory',
        'city',
        'state'
    ],
    components: {
        SearchTopic,
    },
    data: function () {
        return {
            isLoading: false,
            isInitialLoading: false,
            citiesList: [],
            categories: [],
            subcategories: [],
            selectedLocation: null,
            categoryMenuVisible: false,
            subcategoryCountInColumn: 13,
            categoryBtnStyle: {
                'width': '100%',
                'word-break': 'break-word',
                'white-space': 'normal',
                'line-height': '1em',
                'font-family': 'Montserrat, sans-serif',
                'font-weight': '500',
                'font-size': '20px',
                'color': 'rgba(0,0,0,0.87)',
                'text-align': 'left',
                'text-transform': 'capitalize',
            },
            categoryListItemStyle: {

            },
            locationLabelStyle: {
                'display': 'block',
                'text-transform': 'capitalize',
                'font-family': "Montserrat, sans-serif",
                'text-align': 'center',
                'font-size': '20px',
                'top': '6px',
                'height': '20px',
                'line-height': '20px',
                'color': 'rgba(0,0,0,0.54)',
                'position': 'absolute',
                'transform': 'translateY(-16px) scale(0.75)',
                'width': '90%',
            },
            autocompleteMenuProps: {
                "closeOnClick":false,
                "closeOnContentClick":false,
                "openOnClick":false,
                "maxHeight":'auto',
                "bottom": true,
                "attach": '.type-autocomplete'
            },
            firstBarStyle: {
                "border-radius": '7px',
                "background-color": 'rgba(245,245,245,1)',
                "width": '100%',
                "margin": '0px',
                "height": '48px',
                'font-family': 'Montserrat, sans-serif',
                'font-weight': '500',
                'font-size': '20px',
                'text-transform': 'capitalize',
            },
            secondBarStyle: {
                "border-radius": '7px',
                "background-color": 'rgba(245,245,245,1)',
                "padding": "0"
            },
            typeItems: [
                {text: 'All', value: null},
                {text: 'Classes', value: 'group'},
                {text: 'Private Tutors', value: 'private'},
            ],
            type: null,
            locationMenuVisible: false,
            topic: null,
        }
    },
    created() {
        this.isInitialLoading = true
        Promise.all([axios.get('/api/cities/'), axios.get('/api/subcategories/'), axios.get('/api/categories/')]).then(([cities, subcategories, categories]) => {
            this.citiesList = _.sortBy(_.map(cities.data, (v) => ({
                text: v.address_city+', '+v.address_state,
                value: v,
                //selected: v.address_city == 'St. Petersburg' &&  v.address_state == 'FL',
            })), c => (c.text.indexOf('St. Petersburg') !== -1 && c.text.indexOf('FL') !== -1 ? '  ' : c.text))
            this.subcategories = subcategories.data
            this.categories = categories.data
        }).catch((e1, e2) => {
            console.log('err', e1, e2)
        }).then(() => {
            this.isInitialLoading = false
        })
    },
    methods: {
        setLocation(locationId) {
            console.log('setLocation', locationId)
            this.selectedLocation = locationId
            this.locationMenuVisible = false
        },
        searchClasses() {
            console.log(this.topic, this.selectedLocation)
            if(this.isLoading)
                return
            this.isLoading = true
            let city = 'all',
                state = 'all',
                category = '0',
                subcategory = '0',
                venue = ''
            if(this.selectedLocation === 'online') {
                city = 'online'
                state = 'none'
            } else if (this.selectedLocation) {
                city = this.selectedLocation.address_city
                state = this.selectedLocation.address_state
            }
            let additionalUrlParams = ''
            if(this.topic) {
                const additional = []
                if(this.topic.type === 'venues') {
                    venue = this.topic.id
                }
                if(this.topic.type === 'categories') {
                    category = this.topic.id
                }
                if(this.topic.type === 'subcategories') {
                    subcategory = this.topic.id
                }
                if(this.topic.type === 'subcategories') {
                    subcategory = this.topic.id
                }
                if(this.topic.type === 'teachers') {
                    additional.push(`teacher=${this.topic.id}`);
                }
                if(this.topic.type === 'classes') {
                    additional.push(`class=${this.topic.id}`);
                }
                if(additional.length) {
                    additionalUrlParams = `?${additional.join('&')}`
                }
            }
            setTimeout(() => {
                this.$router.push(`/learners/search/${city}/${state}/${category}/${subcategory}/${this.type || '0'}/${venue}`+additionalUrlParams)
            }, 50)
        },
        setTopic(subcategory, category) {
            if(subcategory) {
                this.topic = {
                    type: 'subcategories',
                    id: subcategory
                }
            } else if(category) {
                this.topic = {
                    type: 'categories',
                    id: category
                }
            } else {
                this.topic = null
            }
            this.categoryMenuVisible = false
        }
    },
    computed: {
        screenXS() {
            return this.$vuetify.breakpoint.xsOnly
        },
        selectedLocationText() {
            if(this.selectedLocation === '')
                return 'All'
            if(!this.selectedLocation)
                return 'Virtual or Local'
            if(this.selectedLocation === 'online')
                return 'Virtual'
            return (_.find(this.citiesList, {value: this.selectedLocation}) || {}).text
        },
        selectedSubcategory() {
            if(this.topic) {
                if(this.topic.type === 'subcategories') {
                    return (_.find(this.subcategories, {id: Number(this.topic.id)}) || {name: ''}).name
                }
                if(this.topic.type === 'categories') {
                    return (_.find(this.categories, {id: Number(this.topic.id)}) || {name: ''}).name
                }
            }
            return 'What do you want to learn?'
        },
        categoryList() {
            let res = []
            let sortedSubcats = _.sortBy(this.subcategories, 'name')
            let groups = _.groupBy(sortedSubcats, 'category')
            let sortedCats = _.sortBy(this.categories, 'name')
            sortedCats.unshift({
                id: '',
                name: '--All--'
            })
            return _.map(sortedCats, c => {
                if(groups[c.id]) {
                    groups[c.id] = _.sortBy(groups[c.id], v => v.name.toLowerCase())
                    groups[c.id].unshift({
                        id: '',
                        name: '--All--',
                    })
                }
                return {
                    value: c.id,
                    text: c.name,
                    children: _.map(groups[c.id] || [], sc => ({
                        value: sc.id,
                        text: sc.name,
                        category: c.id,
                    }))
                }
            })
        },
    },
    watch: {
        locationMenuVisible(v, o) {
            console.log(v, o)
        }
    }
}
</script>

<style lang="scss" >
.topic-textfield {
    input[type="text"] {
        font-size: larger;
    }
}
.topic-menu-content {
    width: 300px;
}
.v-margined {
    margin: 1px 0;
}
.search-home-location-menu {
    .v-list__tile__title {
        font-size: 16px;
    }
}
</style>
<style lang="scss" >
.justify-end {
    justify-content: flex-end;
}
</style>
