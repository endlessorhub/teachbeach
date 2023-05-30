<template>
    <CalendarImportPopup
        :formData="formData"
        :filename="filename"
        @downloaded="$emit('downloaded')"
        :isTooltipVisible="!isTooltipDynamic"
        :isPopupOpened="isPopupOpened"
        @closed="$emit('closed')"
        :isButtonHidden="isButtonHidden"
    />
</template>
<script>
import CalendarImportPopup from '@/components/basic/CalendarImportPopup'

export default {
    name: 'private_lesson_calendar_import',
    data: () => ({

    }),
    components: {
        CalendarImportPopup,
    },
    props: [
        'privateClass',
        'enrollment',
        'isTooltipDynamic',
        'isPopupOpened',
        'isButtonHidden',
    ],
    computed: {
        filename() {
            return this.privateClass.private_className+'-'+this.enrollment.id
        },
        formData() {
            //console.log(this.enrollment, this.privateClass)
            return {
                schedule: {
                    'schedule_dates': [{
                        UID: `PrivateEnrollment${this.enrollment.id}`,
                        date: this.enrollment.date,
                        start: this.enrollment.time_from,
                        end: this.enrollment.time_to,
                    }],
                    'day_select_type': 'monthly',
                    'timezone': this.privateClass.timezone,
                    summary: this.privateClass.private_className,
                    description: `${this.enrollment.student.first_name} ${this.enrollment.student.last_name} (${this.enrollment.student.email}, ${this.enrollment.student.phone})`,
                    location: this.privateClass.address_street ? [
                        this.privateClass.address,
                        this.privateClass.address_street,
                        `${this.privateClass.address_city} ${this.privateClass.address_state}`,
                        this.privateClass.address_zip,
                    ].join(', ') : this.privateClass.class_type[0].toUpperCase()+this.privateClass.class_type.substr(1)
                }
            }
        }
    },
    methods: {

    },
}
</script>
<style lang="scss">

</style>