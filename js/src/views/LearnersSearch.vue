<template>
    <v-layout align-center justify-center>
        <v-flex xs11 >
            <CityCategory
                v-bind:city="city"
                v-bind:state="state"
                v-bind:category="category"
                v-bind:subcategory="subcategory"
                v-bind:venue="venue"
                v-bind:lessonType="lessontype"
                v-bind:class-id="classId"
                v-bind:teacher="teacher"
            />
            <v-dialog v-model="dialog" persistent max-width="390">
              <v-card class="on-top">
                <v-card-title class="headline">
                    <div>{{ regHeader }}</div>
                    <v-spacer></v-spacer>
                    <v-btn icon @click="skipDialog=true">
                        <v-icon>close</v-icon>
                    </v-btn>
                </v-card-title>
                <v-card-text>
                    <two-step-student-reg @stepChange="(v) => {regStep=v}"></two-step-student-reg>
                </v-card-text>
              </v-card>
            </v-dialog>
        </v-flex>
    </v-layout>
</template>

<script>
import CityCategory from '@/components/Learner/CityCategory.vue'
import TwoStepStudentReg from '@/components/basic/forms/TwoStepStudentReg'
import metadata from '@/mixins/metadata'
import {mapGetters} from 'vuex'

export default {
    mixins: [metadata],
    props: [],
    data: () => ({
        city: null,
        state: null,
        category: null,
        subcategory: null,
        venue: null,
        classId: null,
        teacher: null,
        lessontype: null,
        search: null,
        regStep: 1,
        skipDialog: false,
    }),
    name: 'learners',
    components: {
        TwoStepStudentReg,
        CityCategory
    },
    computed: {
        ...mapGetters([
            'isLoggedIn',
        ]),
        regHeader() {
            return this.regStep === 1 ? 'Looks like you’re new here!' : ''
        },
        dialog() {
            return !this.isLoggedIn && !this.skipDialog
        },
    },
    created() {
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
        if(this.$route.query.teacher) {
            this.teacher = Number(this.$route.query.teacher)
        }
        if(this.$route.query.class) {
            this.classId = Number(this.$route.query.class)
        }
    },
    methods: {
        openLoginForm() {
            this.$emit('openLoginForm', {register: 'close'})
        },
    },
    watch: {
        '$route' (to, from) {
            if(this.$route.params.city) {
                this.city = this.$route.params.city
            }
            if(this.$route.params.state) {
                this.state = this.$route.params.state
            }
            if(from.params.category !== to.params.category) {
                this.category = Number(this.$route.params.category) || null
            }
            if(from.params.subcategory !== to.params.subcategory) {
                this.subcategory = Number(this.$route.params.subcategory) || null
            }
            if(from.params.venue !== to.params.venue) {
                this.venue = this.$route.params.venue
            }
            if(from.params.lessontype !== to.params.lessontype) {
                this.lessontype = this.$route.params.lessontype === '0' ? null : this.$route.params.lessontype
            }
            if(from.query.teacher !== to.query.teacher) {
                this.teacher = Number(to.query.teacher)
            }
            if(from.query.class !== to.query.class) {
                this.classId = Number(to.query.class)
            }
        }
    }
}
</script>

<style lang="scss">
.on-top {
    z-index: 1000001;
}
</style>