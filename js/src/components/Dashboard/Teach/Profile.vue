<template>
    <TeacherProfile v-if="profile=='teacher'"></TeacherProfile>
    <CompanyProfile v-else-if="profile=='company'"></CompanyProfile>
</template>

<script>

import TeacherProfile from './TeacherProfile'
import CompanyProfile from './CompanyProfile'

export default {
    name: 'dashboard_teach_profile',
    components: {
        TeacherProfile,
        CompanyProfile,
    },
    data: () => ({
        profile: null,
    }),
    created() {
        if(this.$store.state.user.is_company) {
            this.profile = 'company'
        } else {
            this.profile = 'teacher'
        }
    },
}
</script>
<style lang="scss">

</style>