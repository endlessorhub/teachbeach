<template>
<v-menu
    ref="menuCustomDuration"
    v-model="tRootMenu"
    :close-on-content-click="false"
    :nudge-right="40"

    transition="scale-transition"
    offset-y
    full-width
    max-width="290px"
    min-width="290px"
>
    <v-text-field
      slot="activator"
      v-model="timeLabel"
      :label="label"
      :prepend-icon="showIcon ? access_time : ''"
      readonly
    ></v-text-field>
    <v-time-picker
      v-if="tRootMenu"
      v-model="time"
      full-width
      @click:minute="$refs.menuCustomDuration.save(time)"
      @click:hour="onClickHour"
      :format="format"
      :min="min"
      :max="max"
    ></v-time-picker>
</v-menu>
</template>

<script>
import _ from 'lodash'
import utils from '@/lib/utils.js'
import axios from 'axios'

export default {
    props: {
        time: String,
        format: {
            type: String,
            default: '24h'
        },
        label: {
            type: String,
            default: 'Pick time'
        },
        showIcon: {
            type: Boolean,
            default: true
        },
        min: String,
        max: String,
    },

    watch: {
        time() {
            this.$emit('change', this.time)
        }
    },

    data: () => ({
        tRootMenu: false,
    }),

    created() {
        console.log(this.format)
    },

    computed: {
        timeLabel() {
            if (this.format == 'ampm')
                return utils.time24HtoAMPM(this.time)
            return this.time
        }
    },

    methods: {
        onClickHour(hours) {
            //console.log(arguments)
            this.time = hours > 9 ? hours+':00' : '0'+hours+':00'
        }
    }
}
</script>