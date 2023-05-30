<template>
<v-rating
        v-if="rating || rating === 0"
        :value="rating"
        dense
        color="platform-green"
></v-rating>
</template>

<script>
import _ from 'lodash'
import axios from 'axios'

export default {
    props: [
        'objectType',
        'objectId',
    ],

    data: () => ({
        isLoading: false,
        rating: 5,
    }),

    components: {

    },

    created() {

    },

    mounted() {

    },

    computed: {

    },

    methods: {

    }
}
</script>

<style scoped lang="scss">

</style>