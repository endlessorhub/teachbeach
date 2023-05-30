<template>
    <v-layout align-center justify-center row wrap>
        <v-flex xs12>
            <v-btn-toggle v-model="subnav">
              <v-btn flat value="profile" to="/dashboard/teach/profile" active-class="active" class="sub-nav-btn">
                My Profile
              </v-btn>
              <v-btn flat value="classes" to="/dashboard/teach/classes" active-class="active" class="sub-nav-btn">
                Classes
              </v-btn>
              <v-menu flat offset-y>
                <template v-slot:activator="{ on }">
                  <v-btn
                    flat
                    v-on="on"
                    class="sub-nav-btn"
                  >
                    CRM
                  </v-btn>
                </template>

                <v-list>
                  <v-list-tile
                    :key="'dash_teach_stud'"
                    to="/dashboard/teach/students_list"
                  >
                    <v-list-tile-title>Audiences</v-list-tile-title>
                  </v-list-tile>
                  <v-list-tile
                    :key="'dash_teach_refund'"
                    to="/dashboard/teach/students_refund"
                  >
                    <v-list-tile-title>Refund</v-list-tile-title>
                  </v-list-tile>
                  <v-list-tile
                    :key="'dash_teach_crm'"
                    to="/dashboard/teach/new_crm"
                  >
                    <v-list-tile-title>New CRM </v-list-tile-title>
                  </v-list-tile>
                </v-list>
              </v-menu>
              <v-btn flat value="schedule" to="/dashboard/teach/schedule_list" active-class="active" class="sub-nav-btn">
                My Schedule
              </v-btn>
              <v-btn v-if="!isTeacherOfCompany" flat value="calendar" to="/dashboard/teach/reports" active-class="active" class="hidden-xs-only sub-nav-btn">
                Reports
              </v-btn>
              <v-menu v-if="!isTeacherOfCompany" flat offset-y>
                <template v-slot:activator="{ on }">
                  <v-btn
                    flat
                    v-on="on"
                    class="sub-nav-btn"
                  >
                    <v-icon>settings</v-icon>
                  </v-btn>
                </template>

                <v-list>
                  <v-list-tile
                    :key="dash_teach_account_take"
                    to="/dashboard/teach/account_take"
                  >
                    <v-list-tile-title>Take payment</v-list-tile-title>
                  </v-list-tile>
                  <v-list-tile
                    :key="dash_teach_account_make"
                    to="/dashboard/teach/account_make"
                  >
                    <v-list-tile-title>Make payment</v-list-tile-title>
                  </v-list-tile>
                </v-list>
              </v-menu>
            </v-btn-toggle>
        </v-flex>
        <v-flex xs12 class="hidden-sm-and-up">
            <v-btn-toggle v-model="subnav">
              <v-btn flat value="calendar" to="/dashboard/teach/calendar" active-class="active">
                Calendar
              </v-btn>
              <v-btn flat value="calendar" to="/dashboard/teach/reports" active-class="active">
                Reports
              </v-btn>
              <v-btn v-if="!isTeacherOfCompany" flat value="account" to="/dashboard/teach/account" active-class="active">
                <v-icon>settings</v-icon>
              </v-btn>
            </v-btn-toggle>
        </v-flex>
        <v-flex xs11>
            <router-view base="/dashboard/teach/"/>
        </v-flex>
    </v-layout>
</template>

<script>
// @ is an alias to /src
import _ from 'lodash'
import axios from 'axios'
import { mapGetters } from 'vuex';

export default {
    name: 'dashboard_teach',
    data: () => ({
        isLoading: false,
        subnav: 'classes',
        companyProfile: {},
    }),
    props: [],
    components: {

    },
    created() {
        this.subnav = this.$route.path
        if(this.$store.state.user.is_company) {
            axios.get('/api/company_profile/').then(cp => this.companyProfile = cp.data)
        }
    },
    computed: {
        ...mapGetters([
            'isTeacherOfCompany',
        ]),
    },
    methods: {

    },

    watch: {
        companyProfile(v) {
            this.$store.dispatch('syncLogoCompanyProfile', v ? v.id : null)
        }
    }
}
</script>
<style lang="scss" scoped>
.sub-nav-btn {
  opacity: 1;
  font-weight: bold;
  &.active {
    background-color: rgba(25, 118, 210, 0.7);
  }
}
</style>