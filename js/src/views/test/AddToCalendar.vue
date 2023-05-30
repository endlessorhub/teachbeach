<template>
    <AddToCalendar
        :schedule="schedule2"
        :filename="filename"
    ></AddToCalendar>
</template>

<script>
import AddToCalendar from '@/components/basic/AddToCalendar'

export default {

    data: () => ({
        isLoading: false,
        schedule: {
            "schedule_dates":[],
            "schedule_excluded":["2020-08-26","2020-08-27"],
            "day_select_type":"weekly",
            "start_date":"2020-08-20",
            "timezone":"EST",
            "until_date":null,
            "weekdays_schedule":[
                {"end":"08:45","start":"06:15","weekday":0},
                {"end":"08:45","start":"06:15","weekday":3},
                {"end":"08:45","start":"06:15","weekday":2},
                {"end":"10:15","start":"06:15","weekday":4}
            ],
            "summary": "class name",
            "location": "some location"
        },
        schedule2: {
            day_select_type: "monthly",
            location: "location",
            schedule_dates: [{date: "2020-08-26", start: "06:30", end: "10:30"}],
            schedule_excluded: [],
            start_date: "2020-08-26",
            summary: "cvxv",
            until_date: "2020-08-26",
            weekdays_schedule: [],
            "timezone":"EST",
        }
    }),

    components: {
        AddToCalendar,
    },

    created() {
        console.log('calendars')
    },

    computed: {
        filename() {
            return `event_${(new Date()).getTime()}`
        }
    },

    methods: {

    },

    watch: {

    }
}
</script>

<style scoped lang="scss">

</style>