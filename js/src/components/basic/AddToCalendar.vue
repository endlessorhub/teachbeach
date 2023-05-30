<template>
    <v-layout align-center row wrap>
        <v-flex xs12 class="text-xs-center">
            <span>Add to: </span>
            <v-btn @click="addToCalendar('google')" :loading="isLoading">Google Calendar</v-btn>
            <v-btn @click="addToCalendar('outlook')" :loading="isLoading">Outlook Calendar</v-btn>
            <v-btn @click="addToCalendar('yahoo')" :loading="isLoading">Yahoo Calendar</v-btn>
        </v-flex>
    </v-layout>
</template>

<script>
import _ from 'lodash'
import axios from 'axios'
import moment from 'moment'
import utils from '@/lib/utils.js'

export default {
    props: {
        'type': {
            type: String,
            default: 'file'
        },
        'events': {
            type: Array,
            default: []
        },
        'schedule': {
            type: Object,
            default: {}
        },
        'filename': {
            type: String,
            default: 'event.ics'
        },
    },

    data: () => ({
        isLoading: false,

    }),

    components: {

    },

    created() {
        console.log('calendars')
    },

    computed: {

    },

    methods: {
        addToCalendar(type) {
            this.isLoading = type
            axios.post('/api/ical/', {
                events: this.events,
                schedule: this.schedule,
            }).then(res => {
                const blob = new Blob([res.data], { type: res.headers['content-type'] })
                const link = document.createElement('a')
                link.href = window.URL.createObjectURL(blob)
                link.setAttribute('download', this.filename)
                link.click()
            }).catch((e) => {
                console.log(e)
            }).then(() => {
                this.isLoading = false
            })
        },
        isBtnLoading(type) {
            return this.isLoading && this.isLoading === type
        }
    },

    watch: {

    }
}
</script>

<style scoped lang="scss">

</style>