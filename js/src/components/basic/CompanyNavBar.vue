<template>
<div class="company-nav-bar">
    <v-toolbar-items class="hidden-md-and-down">
    <v-btn key="member-center" :disabled="!memberCenterUrl" flat @click="onClickMemberCenter">Member Center</v-btn>
    <v-menu key="cources" offset-y>
      <template v-slot:activator="{ on }">
        <v-btn flat v-on="on">Courses</v-btn>
      </template>
      <v-list>
        <v-list-tile
          key="group"
          @click="$router.push(`/company_classes/group/${companyId}`)"
        >
          <v-list-tile-title>Group</v-list-tile-title>
        </v-list-tile>
        <!--v-list-tile
          key="private"
          @click="$router.push(`/company_classes/private/${companyId}`)"
        >
          <v-list-tile-title>Private</v-list-tile-title>
        </v-list-tile-->
      </v-list>
    </v-menu>
    <v-btn key="calendar" flat :to="`/company_group_calendar/${companyId}`">Calendar</v-btn>
    <v-btn v-if="company && company.about_us_url" key="about" flat @click="openExternalLink(company.about_us_url)">About</v-btn>
    <v-menu key="my-account" offset-y>
      <template v-slot:activator="{ on }">
        <v-btn flat v-on="on">My Collab</v-btn>
      </template>
      <v-list>
        <v-list-tile
          v-if="isLoggedIn"
          key="dashboard"
          @click="onDashboardClick"
        >
          <v-list-tile-title>Dashboard</v-list-tile-title>
        </v-list-tile>
        <v-list-tile
          v-if="isLoggedIn"
          key="logout"
          @click="onAccountClick"
        >
          <v-list-tile-title>Log-out</v-list-tile-title>
        </v-list-tile>
        <v-list-tile
          v-if="!isLoggedIn"
          key="login"
          @click="() => onAccountClick({section: 'login'})"
        >
          <v-list-tile-title>Log-in</v-list-tile-title>
        </v-list-tile>
      </v-list>
    </v-menu>
    </v-toolbar-items>
    <v-menu class="hidden-lg-and-up">
    <v-toolbar-side-icon slot="activator" data-mobile-nav-menu-icon></v-toolbar-side-icon>
    <v-list>
        <v-list-tile @click="onClickMemberCenter">
            <v-list-tile-content>
                <v-list-tile-title>Member Center</v-list-tile-title>
            </v-list-tile-content>
        </v-list-tile>
        <v-list-tile :to="`/company_classes/group/${companyId}`">
            <v-list-tile-content>
                <v-list-tile-title>Group Classes</v-list-tile-title>
            </v-list-tile-content>
        </v-list-tile>
        <!--v-list-tile :to="`/company_classes/private/${companyId}`">
            <v-list-tile-content>
                <v-list-tile-title>Private Classes</v-list-tile-title>
            </v-list-tile-content>
        </v-list-tile-->
        <v-list-tile :to="`/company_group_calendar/${companyId}`">
            <v-list-tile-content>
                <v-list-tile-title>Calendar</v-list-tile-title>
            </v-list-tile-content>
        </v-list-tile>
        <v-list-tile v-if="aboutUsUrl" @click="openExternalLink(company.about_us_url)">
            <v-list-tile-content>
                <v-list-tile-title>About</v-list-tile-title>
            </v-list-tile-content>
        </v-list-tile>
        <v-list-tile v-if="isLoggedIn" :to="onDashboardClick">
            <v-list-tile-content>
                <v-list-tile-title>Dashboard</v-list-tile-title>
            </v-list-tile-content>
        </v-list-tile>
        <v-list-tile v-if="isLoggedIn" :to="onAccountClick">
            <v-list-tile-content>
                <v-list-tile-title>Log-out</v-list-tile-title>
            </v-list-tile-content>
        </v-list-tile>
        <v-list-tile v-if="!isLoggedIn" :to="() => onAccountClick({section: 'login'})">
            <v-list-tile-content>
                <v-list-tile-title>Log-in</v-list-tile-title>
            </v-list-tile-content>
        </v-list-tile>
    </v-list>
    </v-menu>
</div>
</template>
<script>
import { mapGetters, mapActions, mapState } from 'vuex';

export default {
    props: {
        companySlug: [Number, String],
        onTeacherDashboardClick: Function,
        onAccountClick: Function,
    },

    data: () => ({
        //select: null
    }),

    computed: {
        ...mapGetters([
            'isLoggedIn',
            'isTeacher',
            'isLearner',
            'isTeacherOfCompany',
        ]),
        ...mapState('viewingCompany', [
            'company',
            'status',
        ]),
        memberCenterUrl() {
            return this.company && this.company.member_center_url;
        },
        companyId() {
            return this.company && this.company.id;
        },
        homeUrl() {
            return this.company && this.company.home_url;
        },
        aboutUsUrl() {
            return this.company && this.company.about_us_url;
        },
    },

    watch: {

    },

    created: function () {
        this.loadCompany(this.companySlug);
    },

    methods: {
        ...mapActions('viewingCompany', [
            'loadCompany',
        ]),
        onClickMemberCenter() {
            if(this.memberCenterUrl) this.openExternalLink(this.memberCenterUrl);
        },
        onDashboardClick() {
            this.isTeacher ? this.$router.push('/dashboard/teach/classes') : this.$router.push('/dashboard/learn');
        },
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.company-nav-bar {
    height: inherit;
    display: flex;
}
</style>