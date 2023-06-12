<template>
    <v-layout align-start justify-center row wrap>
        <v-flex xs12>
            <v-btn-toggle v-model="subnav" mandatory>
              <v-btn flat value="classes" to="/dashboard/learn/classes" active-class="active" class="sub-nav-btn">
                Classes
              </v-btn>
              <v-btn flat value="calendar" to="/dashboard/learn/calendar" active-class="active" class="sub-nav-btn">
                Calendar
              </v-btn>
              <v-btn flat value="account" to="/dashboard/learn/account" active-class="active" class="sub-nav-btn">
                Account
              </v-btn>
              <v-btn flat value="memberships" to="/dashboard/learn/memberships" active-class="active" class="sub-nav-btn">
                Memberships
              </v-btn>
              <v-btn flat value="history" to="/dashboard/learn/history" active-class="active" class="sub-nav-btn">
                History
              </v-btn>
            </v-btn-toggle>
        </v-flex>

        <v-flex xs11>
            <router-view base="/dashboard/learn/"/>
        </v-flex>
    </v-layout>
</template>

<script>
// @ is an alias to /src
import _ from 'lodash'
import { mapActions } from 'vuex';
import axios from 'axios'

export default {
    name: 'dashboard_learn',
    data: () => ({
        isLoading: false,
        subnav: 'classes',
    }),
    props: [],
    components: {

    },
    created() {
        this.subnav = this.$route.path
        this.loadMemberships();
    },
    computed: {

    },
    methods: {
      ...mapActions('learnerMembership', [
        'loadMemberships',
      ]),
    },

    watch: {

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