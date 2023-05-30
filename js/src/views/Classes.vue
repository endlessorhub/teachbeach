<template>
<div class="class-page">
    <div class="class-container flex xs12">
      <v-container grid-list-md text-xs-center>
          <ClassGroup v-if="classData && !classData.is_private" v-bind="classData" v-bind:show_enroll="true" v-on:choose:package="choosePackage"/>
          <ClassPrivate v-if="classData && classData.is_private" v-bind="classData" v-bind:show_enroll="true" v-on:choose:package="choosePackage"/>
          <v-layout align-top justify-center row wrap>
            <v-flex xs12 md12 class="text-xs-center">

            </v-flex>
          </v-layout>
      </v-container>
    </div>
</div>
</template>

<script>
import _ from 'lodash'
import axios from 'axios'
import { mapActions, mapState } from 'vuex';

import ClassGroup from '@/components/Classes/Group.vue'
import ClassPrivate from '@/components/Classes/Private.vue'
import {defaultLogoSrc, defaultLogoAlt} from '@/store'
import utils from '@/lib/utils.js'

const weekDays = [
    'Sun',
    'Mon',
    'Tue',
    'Wed',
    'Thu',
    'Fri',
    'Sat',
]

export default {
    props: {

    },

    data: () => ({
        isLoading: false,
        classData: null
    }),

    components: {
        ClassGroup,
        ClassPrivate,
    },

    created: function () {
        //console.log(this.$route)
        this.isLoading = true
        axios.get('/api/classes/'+this.$route.params.id+'/').then((res) => {
            console.log('done', res)
            this.classData = res.data
            this.$store.dispatch('syncLogoCompanyProfile', this.classData.teacher.user.company_profile ? this.classData.teacher.user.company_profile.id : null);
            if (this.classData.teacher.user.company_profile) {
                this.loadCompany(this.classData.teacher.user.company_profile.id);
            }
        }).catch(() => {
            //console.log(arguments)

        }).then(() => {
            this.isLoading = false
        })
    },

    computed: {
        ...mapState('viewingCompany', [
            'company',
        ]),
    },

    methods: {
        ...mapActions('viewingCompany', [
            'loadCompany',
        ]),
        choosePackage(id) {
            console.warn('choosePackage not implemented!', id)
            this.$store.commit('setLearnerChoice', this.classData)
            //this.$router.push({path: '/learners/step/2'})
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.class-page {
    text-align: center;
    .class-container {
        //width: 800px;
        margin: 0 auto;
    }
}
</style>