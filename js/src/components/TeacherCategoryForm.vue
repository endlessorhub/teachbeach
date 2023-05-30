<template>
  <form autocomplete="off">
    <v-btn @click="submit">Next</v-btn>
    <v-progress-circular
      v-if="isLoadingData"
      indeterminate
    ></v-progress-circular>
    <v-container v-if="!isLoadingData" grid-list-md text-xs-center>
      <h4>Click to see topics or enter your own. Select up to three categories.</h4>
      <v-layout row wrap>
        <v-flex v-for="(c, i) in categorySelects" :key="c.id" xs12 md6 lg4>
          <CategorySelect v-bind="c" v-on:update:selection="onSelectionUpdate" v-on:update:input-string="onCategoryInputUpdate"/>
        </v-flex>
      </v-layout>
    </v-container>
    <v-btn @click="submit">Next</v-btn>
  </form>
</template>

<script>
import _ from 'lodash'
import CategorySelect from '@/components/basic/CategoryCombobox.vue'

import { validationMixin } from 'vuelidate'
import { required, maxLength, email, sameAs } from 'vuelidate/lib/validators'
import axios from 'axios'
import { mapGetters } from 'vuex'

export default {
    props: ['alreadyRegistered'],
    mixins: [validationMixin],

    components: {
        CategorySelect
    },

    validations: {

    },

    data: () => ({
        isLoadingData: false,
        availableCategories: [],
        availableSubcategories: [],
        categoriesSelected: [],
        selectedLimit: 3,
        savedInput: {}
    }),

    created: function () {
        if(this.$store.state.user && this.$store.state.user.is_company) {
            this.selectedLimit = 3
        }
        this.isLoadingData = true
        let _this = this
        // skip draft if this is class edit task
        const preload = this.$store.state.teacherGroupClass && this.$store.state.teacherGroupClass.id ?
            Promise.resolve(true) :
            this.$store.dispatch('loadDraft')
        preload.then(() => {
            return axios.all([axios.get('/api/categories/'), axios.get('/api/subcategories/')])
        }).then(axios.spread(function (categories, subcategories) {
            // Both requests are now complete
            _this.availableCategories = categories.data
            _this.availableSubcategories = subcategories.data
            const subsDict = _.keyBy(_this.availableSubcategories, 'id')
            if (_this.$store.state.categoriesSelected.length) {
                _this.categoriesSelected = _.filter(_this.$store.state.categoriesSelected, v => subsDict[v])
            }
        })).catch(function () {

        }).then(function () {
            _this.isLoadingData = false
        })
    },

    mounted() {

    },

    computed: {
        ...mapGetters([
            'isLoggedIn',
        ]),
        categorySelects: function () {
            let res = []
            let subCats = _.groupBy(this.availableSubcategories, 'category')
            _.each(this.availableCategories, (c) => {
                const items = _.sortBy(_.map(subCats[c.id] || [], (sc) => ({text: sc.name, value: sc.id})), v => v.text.toLowerCase())
                res.push({
                    items: items,
                    label: c.name,
                    id: c.id,
                    multiple: true,
                    selected: this.categoriesSelected ? _.filter(items, v => this.categoriesSelected.indexOf(v.value) != -1) : undefined
                })
            })
            /*
            res.push({
                items: _.map(this.availableSubcategories, (sc) => ({text: sc.name, value: sc.id})),
                label: 'Click to see topics in each category or enter your own.',
                id: 0,
                selected: this.categoriesSelected[0] || []
            })
            */
            return res
        }
    },

    methods: {
        submit () {
            const finish = () => {
                this.$store.commit('setTeacherCategory', this.categoriesSelected)
                fbq('trackCustom', 'teacherWizard', {step: 'category'})
                this.$emit('next:step')
            }
            let uncommitedSubcats = _.filter(_.map(this.savedInput, (v, i) => ({
                category: Number(i),
                name: v,
            })), v => v.name)
            if(uncommitedSubcats.length) {
                const unsavedSubcats = _.filter(uncommitedSubcats, v => !_.find(this.availableSubcategories, v))
                if (unsavedSubcats.length) {
                    Promise.all(_.map(unsavedSubcats, s => axios.post(`/api/add_subcategory/`, {
                        category_id: s.category,
                        subcategory_name: s.name,
                    }))).then(results => {
                        this.categoriesSelected = _.concat(this.categoriesSelected, _.map(results, res => res.data.id))
                        finish()
                    })
                } else {
                    this.categoriesSelected = _.concat(this.categoriesSelected, _.map(uncommitedSubcats, v => _.find(this.availableSubcategories, v).id))
                    finish()
                }
            } else {
                finish()
            }

        },
        clear () {

        },
        onSelectionUpdate: function (event) {
            let subCats = _.groupBy(this.availableSubcategories, 'category')
            let supposedCount = _.filter(this.categoriesSelected, subcatId => !_.find(subCats[event.id], {id: subcatId})).length
            supposedCount += event.value.length
            if(_.some(event.value, v => _.isString(v))) {
                const name = _.find(event.value, v => _.isString(v))
                axios.post(`/api/add_subcategory/`, {
                    category_id: event.id,
                    subcategory_name: name,
                }).then(res => {
                    const addSubcat = {
                        name: name,
                        id: res.data.id,
                        category: event.id,
                    }
                    this.availableSubcategories.push(addSubcat)
                    if(supposedCount <= this.selectedLimit)
                        this.categoriesSelected.push(res.data.id)
                })
            } else {
                //filter out existing subcategories from category, add ids from event
                if(supposedCount <= this.selectedLimit) {
                    this.categoriesSelected = _.filter(this.categoriesSelected, subcatId => !_.find(subCats[event.id], {id: subcatId}))
                    this.categoriesSelected = this.categoriesSelected.concat(_.map(event.value, v => Number(v.value)))
                }
            }
            /// a bit hack to force update
            this.availableSubcategories = _.concat([], this.availableSubcategories)
            this.categoriesSelected = _.concat([], this.categoriesSelected)
            //this.categoriesSelected = {}
            //this.categoriesSelected[event.id] = event.value
            //this.$forceUpdate()
        },
        onCategoryInputUpdate(event) {
            this.savedInput[event.id] = event.value
        },
        oncreateds() {
            console.log(this, arguments)
        }
    },
    watch: {
        isLoggedIn() {
            const subsDict = _.keyBy(this.availableSubcategories, 'id')
            this.categoriesSelected = _.filter(this.$store.state.categoriesSelected, v => subsDict[v])
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>