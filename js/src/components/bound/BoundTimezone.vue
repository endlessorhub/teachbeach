<template>
    <Timezone
        v-model="currentTimezone"
    />
</template>

<script>

import moment from 'moment-timezone';
import axios from 'axios';
import Timezone from '@/components/basic/Timezone';
import {mapMutations, mapState} from 'vuex';

export default {
    props: {
        'connect': {
            type: String,
            default: '',
        }
    },
    components: {
        Timezone,
    },
    data: () => ({

    }),

    created() {
        //console.log(Intl.DateTimeFormat().resolvedOptions().timeZone)
    },

    computed: {
        ...mapState(['timezone']),
        currentTimezone: {
            get() {
                return this.timezone || moment.tz.guess();
            },
            set(v) {
                if(this.connect) {
                    axios.post(this.connect, {timezone: v}).then(() => this.setTimezone(v))
                } else
                    this.setTimezone(v)
            }
        }
    },

    methods: {
        ...mapMutations(['setTimezone'])
    }
}
</script>