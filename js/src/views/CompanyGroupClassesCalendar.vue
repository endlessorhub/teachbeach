<template>
  <ClassesCalendar
    :classes="classes"
  ></ClassesCalendar>
</template>

<script>
import metadata from '@/mixins/metadata'
import api from '@/lib/api'
import ClassesCalendar from '@/components/basic/ClassesCalendar'

export default {
    props: {
        companyId: {
            type: Number,
        },
    },
    data: () => ({
        isLoading: false,
        classes: [],
        companyProfile: null,
    }),
    mixins: [metadata],
    name: 'company_group_classes_calendar',
    components: {
        ClassesCalendar,
    },
    created() {
        api.getCompanyCalendarData(this.companyId).then(data => {
            this.classes = data.classes.filter(v => !v.is_private)
            this.companyProfile = data
        })
    },
    watch: {
        companyProfile(v) {
            this.$store.dispatch('syncLogoCompanyProfile', v ? v.id : null)
        }
    }
}
</script>