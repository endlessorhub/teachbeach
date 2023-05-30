<template>
    <div class="dashboard-teach-membership">
        <bound-membership
            cancel-btn-text="Cancel"
            submit-btn-text="Save"
            :is-back-btn-visible="true"
            :is-submit-btn-duplicated="true"
            back-btn-url="/dashboard/teach/classes"
            @saved="onSaved"
            @cancel="onCancel"
        />
        <v-snackbar
            v-model="snackbar"
            color="platform-green"
            :timeout="timeout"
            top
        >
            Membership saved successfully
        </v-snackbar>
    </div>
</template>

<script>
import BoundMembership from '@/components/bound/BoundMembership'

export default {
    name: 'DashboardTeacherMembership',
    components: {
        BoundMembership,
    },
    data() {
        return {
            snackbar: false,
            timeout: 3000,
        }
    },
    methods: {
        onSaved() {
            this.snackbar = true
            setTimeout(() => this.$router.push('/dashboard/teach/classes'), this.timeout+500)
        },
        onCancel() {
            this.$router.push('/dashboard/teach/classes')
        }
    },
}
</script>
<style lang="scss">
@import "../../../styles/_variables.scss";

</style>