<template>
    <v-select
      :items="timezonesWithValue"
      label="Timezone"
      :value="value"
      @change="v => $emit('input', v)"
    ></v-select>
</template>
<script>
import axios from 'axios'

export default {
    name: 'class_list_item_actions',
    data: () => ({
        timezones: [
            {value: 'US/Alaska', text: 'Alaska'},
            {value: 'US/Aleutian', text: 'Aleutian'},
            {value: 'US/Central', text: 'Central'},
            {value: 'US/Eastern', text: 'Eastern'},
            {value: 'US/Hawaii', text: 'Hawaii'},
            {value: 'US/Mountain', text: 'Mountain'},
            {value: 'US/Pacific', text: 'Pacific'},
            {value: 'US/Samoa', text: 'Samoa'},
        ]
    }),
    props: [
        'value'
    ],
    computed: {
        timezonesWithValue() {
            if(this.value && !this.timezones.find(v => v.value === this.value))
                return [{value: this.value, text: this.value}, ...this.timezones]
            return this.timezones
        }
    },
    methods: {

    },
}
</script>
<style lang="scss">

</style>