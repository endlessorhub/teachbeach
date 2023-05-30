<template>
    <div style="max-width: 200px;">
    <v-select
      :items="timezones"
      label="Timezone"
      hide-details
      :value="value"
      @change="event => $emit('input', event)"
      :menu-props="{auto: true}"
    ></v-select>
    </div>
</template>

<script>

import moment from 'moment-timezone';

const timezones = moment.tz.names();

export default {
    props: {
        value: String,
    },

    data: () => ({
        timezones,
    }),

    created() {
        //console.log(Intl.DateTimeFormat().resolvedOptions().timeZone)
    },

    computed: {

    },

    methods: {

    }
}
</script>