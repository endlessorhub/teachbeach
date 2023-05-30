<template>
  <div class="learners">
    <v-layout align-center justify-center>
      <LearnerWizard
              v-bind:initialStep="step"
              v-bind:city="city"
              v-bind:initialId="id"
              v-bind:initialOrderId="order_id"
              v-bind:state="state"
              v-bind:category="category"
              v-bind:subcategory="subcategory"
              v-bind:search="search"
              v-bind:venue="venue"
              v-bind:lessontype="lessontype"
      />
    </v-layout>
  </div>
</template>

<script>
import LearnerWizard from '@/components/Learner/Wizard.vue'
import metadata from '@/mixins/metadata'

export default {
    mixins: [metadata],
    props: [],
    data: () => ({
        step: null,
        id: null,
        order_id: null,
        city: null,
        state: null,
        category: null,
        subcategory: null,
        venue: null,
        lessontype: null,
        search: null,
    }),
    name: 'learners',
    components: {
        LearnerWizard
    },
    created() {
        if(this.$route.params.step) {
            this.step = this.$route.params.step
        }
        if(this.$route.params.id) {
            this.id = this.$route.params.id
        }
        if(this.$route.params.order_id) {
            this.order_id = this.$route.params.order_id
        }
        if(this.$route.params.city) {
            this.city = this.$route.params.city
        }
        if(this.$route.params.state) {
            this.state = this.$route.params.state
        }
        if(this.$route.params.category && Number(this.$route.params.category)) {
            this.category = this.$route.params.category
        }
        if(this.$route.params.subcategory && Number(this.$route.params.subcategory)) {
            this.subcategory = this.$route.params.subcategory
        }
        if(this.$route.params.lessontype && this.$route.params.lessontype !== '0') {
            this.lessontype = this.$route.params.lessontype
        }
        if(this.$route.params.venue) {
            this.venue = this.$route.params.venue
        }
        if(this.$route.params.token) {
            this.search = this.$route.params.token
        }
    },
    methods: {

    },
    watch: {
        '$route' (to, from) {
            if(this.$route.params.city) {
                this.city = this.$route.params.city
            }
            if(this.$route.params.state) {
                this.state = this.$route.params.state
            }
            if(from.params.category != to.params.category) {
                this.category = Number(this.$route.params.category) || null
            }
            if(from.params.subcategory != to.params.subcategory) {
                this.subcategory = Number(this.$route.params.subcategory) || null
            }
            if(from.params.step != to.params.step) {
                this.step = this.$route.params.step
            }
            if(from.params.venue != to.params.venue) {
                this.venue = this.$route.params.venue
            }
            if(from.params.lessontype != to.params.lessontype) {
                this.lessontype = this.$route.params.lessontype === '0' ? null : this.$route.params.lessontype
            }
        }
    }
}
</script>

<style lang="scss">

</style>