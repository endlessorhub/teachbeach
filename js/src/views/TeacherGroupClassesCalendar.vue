<template>
  <ClassesCalendar
    :classes="classes"
    :teacher-id="teacherId"
  ></ClassesCalendar>
</template>

<script>
import metadata from '@/mixins/metadata'
import api from '@/lib/api'
import ClassesCalendar from '@/components/basic/ClassesCalendar'

export default {
    props: {
        teacherId: {
            type: Number,
        },
    },
    data: () => ({
        isLoading: false,
        classes: [],
        companyProfile: null,
    }),
    mixins: [metadata],
    name: 'teacher_group_classes_calendar',
    components: {
        ClassesCalendar,
    },
    created() {
        api.getTeacherCalendarData(this.teacherId).then(data => {
            this.classes = data.classes.filter(v => !v.is_private)
            this.companyProfile = data.user.company_profile
        })
    },
    watch: {
        companyProfile(v) {
            this.$store.dispatch('syncLogoCompanyProfile', v ? v.id : null)
        }
    }
}
</script>