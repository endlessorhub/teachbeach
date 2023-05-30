<template>
    <v-autocomplete
        browser-autocomplete="new-password"
        :class="cssClass"
        :loading="isLoading"
        hide-no-data
        hide-details
        dense
        flat
        return-object
        v-model="topic"
        :placeholder="placeholder"
        :items="topicList"
        @change="changeTopic"
        :menu-props="autocompleteMenuProps"
        attach=".s-type-autocomplete"
        :label="label"
        :search-input.sync="topicInput"
        :cache-items="multiple"
        :multiple="multiple"
    >
        <template v-slot:item="data">
            <template v-if="typeof data.item !== 'object'">
              <v-list-tile-content v-text="data.item"></v-list-tile-content>
            </template>
            <template v-else>
              <v-list-tile-content>
                <v-list-tile-title v-html="data.item.text"></v-list-tile-title>
                <v-list-tile-sub-title v-html="data.item.group"></v-list-tile-sub-title>
              </v-list-tile-content>
            </template>
        </template>
    </v-autocomplete>
</template>

<script>
import _ from 'lodash'
import axios from 'axios'
const CancelToken = axios.CancelToken;
const source = CancelToken.source();
const capitalize = (str) => str.charAt(0).toUpperCase()+str.slice(1);

export default {
    props: {
        'category': Number,
        'subcategory': Number,
        'city': String,
        'state': String,
        'venue': String,
        'topicThreshold': {
            type: Number,
            default: 500,
        },
        'value': Object,
        'multiple': {
            type: Boolean,
            default: false,
        },
        'placeholder': {
            type: String,
            default: 'What do you want to learn?',
        },
        'label': {
            type: String,
            default: 'Topic',
        },
        'blackPlaceholder': {
            type: Boolean,
            default: false,
        },
        categories: Array,
        subcategories: Array,
    },
    data: function () {
        return {
            isLoading: false,
            autocompleteMenuProps: {
                "closeOnClick":false,
                "closeOnContentClick":false,
                "openOnClick":false,
                "maxHeight":'auto',
                "bottom": true,
                "attach": '.type-autocomplete',
                //"content-class": 'search-topic-menu-class',
            },
            topicList: [],
            topicInput: null,
            topicRequest: null,
            topicTimeout: null,
        }
    },
    created() {

    },
    methods: {
        changeTopic(val) {
            this.$emit('input', val)
        }
    },
    computed: {
        cssClass() {
            const baseCSSClass = 's-type-autocomplete search-topic-component'
            return this.blackPlaceholder ? `${baseCSSClass} black-placeholder` : baseCSSClass
        },
        topic() {
            return this.value
        }
    },
    watch: {
        topicInput(val) {
            console.log('search', val, this.topic)
            if(this.topic && val === this.topic.text)
                return;
            if(this.topicTimeout) {
                clearTimeout(this.topicTimeout)
            }
            this.topicTimeout = setTimeout(() => {
                if(this.topicRequest) {
                    console.log(this.topicRequest)
                    source.cancel('Operation canceled by the user.')
                }
                this.isLoading = true
                this.topicRequest = axios.get(`/api/autocomplete/?q=${val}`, {
                    cancelToken: source.token
                }).then(res => {
                    console.log(res)
                    this.topicList = []
                    _.each(res.data.res, (items, type) => {
                        if(items.length) {
                            this.topicList.push(capitalize(type));
                        }
                        _.each(items, item => {
                            if(type === 'venues') {
                                this.topicList.push({
                                    text: item.teaching_venue,
                                    group: type,
                                    type,
                                    id: item.teaching_venue,
                                })
                            } else {
                                this.topicList.push({
                                    text: item.name,
                                    group: type,
                                    type,
                                    id: item.id,
                                })
                            }
                        })
                    })
                    if(res.data.res.categories.length) {
                        //todo: add related subcategories?
                    }
                }).catch(e => {
                    console.log(e)
                }).then(() => {
                    this.isLoading = false
                    this.topicRequest = null
                    this.topicTimeout = null
                })
            }, this.topicThreshold)

        },
    }
}
</script>

<style lang="scss">
.search-topic-component.black-placeholder {
    .v-label {
        color: black;
        font-size: 1.2em;
    }
    input[type='text']::placeholder {
        color: black;
        font-size: 1.2em;
    }
}

.s-type-autocomplete.search-topic-component > .v-input__control > .v-input__slot:after {
    border: none;
}
.s-type-autocomplete.search-topic-component > .v-input__control > .v-input__slot:before {
    border: none;
}
.s-type-autocomplete.search-topic-component .v-input__append-inner {
    padding-right: 16px;
    margin-top: -4px;
}
</style>
