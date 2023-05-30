<template>
    <v-layout align-center row wrap v-if="value">
        <v-flex xs6 class="text-xs-left">
            <v-select
              v-model="timeFrom"
              :items="timeItems"
              label="Time From"
            ></v-select>
        </v-flex>
        <v-flex xs6 class="text-xs-left">
            Until: {{timeTo}}
        </v-flex>
        <v-flex xs12 class="text-xs-left">
            <v-menu
                v-model="menu2"
                :close-on-content-click="false"
                top
                offset-y
                full-width
                min-width="290px"
            >
                <template v-slot:activator="{ on }">
                  <v-text-field
                    v-model="dateStr"
                    label="Date"
                    prepend-icon="event"
                    readonly
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-date-picker
                    :min="min"
                    :max="max"
                    v-model="date"
                    @input="menu2 = false"
                ></v-date-picker>
            </v-menu>
        </v-flex>
    </v-layout>
</template>

<script>
import moment from 'moment'

export default {
    props: {
        'value': {
            type: Date,
        },
        'duration': {
            type: Number,
            default: 1
        },
        'min': {
            type: String,
            'default': moment().format('YYYY-MM-DD')
        },
        'max': String,
    },

    data: () => ({
        isLoading: false,
        menu2: false,
    }),

    computed: {
        dateStr() {
            return this.value ? this.value.toLocaleString('en-us', {year: 'numeric', month: 'long', day: 'numeric', weekday: 'long'}) : ''
        },
        date: {
            get() {
                return moment(this.value).format('YYYY-MM-DD')
            },
            set(v) {
                const newVal = moment(v)
                const tmp = moment(this.value)
                newVal.hour(tmp.hour())
                newVal.minute(tmp.minute())
                this.$emit('input', newVal.toDate())
            }
        },
        timeFrom: {
            get() {
                return moment(this.value).format('HH:mm')
            },
            set(v) {
                const tmp = moment(this.value)
                tmp.hour(Number(v.split(':')[0]))
                tmp.minute(Number(v.split(':')[1]))
                this.$emit('input', tmp.toDate())
            }
        },
        timeTo() {
            const tmp = moment(this.value)
            tmp.add(Number(this.duration), 'm')
            return tmp.format('h:mm a')
        },
        timeItems() {
            const res = []
            let startMinutes = 0
            if(this.timeFrom) {
                startMinutes = (this.timeFrom.split(':')[0]*60+Number(this.timeFrom.split(':')[1])) % this.duration
            }
            let tmp = moment().hour(0).minute(0)
            tmp.add(startMinutes, 'm')
            for (let x = startMinutes; x <= 60*24-this.duration; x+= 15) {

                res.push({
                    value: tmp.format('HH:mm'),
                    text: tmp.format('h:mm a')
                })
                tmp.add(15, 'm')
            }
            return res
        }
    },
}
</script>

<style scoped lang="scss">

</style>