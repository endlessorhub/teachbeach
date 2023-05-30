<template>
    <v-menu
        v-model="menu"
        :close-on-content-click="false"
        :nudge-right="40"
        lazy
        transition="scale-transition"
        offset-y
        full-width
        min-width="290px"
    >
        <template v-slot:activator="{ on }">
            <v-btn class="platform-green" v-on="on">Sign in</v-btn>
        </template>
        <v-date-picker
            v-model="date"
            @input="commitDate"
            :allowed-dates="allowedDates"
        ></v-date-picker>
    </v-menu>
</template>
<script>

export default {
    name: 'class_order_student_enroll',
    data: () => ({
        menu: false,
        date: '',
    }),
    props: [
        'order',
        'gclass',
    ],
    computed: {
        allowed() {
            return new Map(this.gclass.schedule_dates ? this.gclass.schedule_dates.map(sd => [sd.date, true]) : [])
        }
    },
    methods: {
        commitDate() {
            this.$emit('selection', {date: this.date, order: this.order})
            this.menu = false
        },
        allowedDates(date) {
            return this.allowed.has(date)
        }
    },
}
</script>
<style lang="scss">

</style>