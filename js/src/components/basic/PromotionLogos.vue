<template>
    <v-layout align-center row wrap>
        <v-flex xs12 class="title">
            Where your classes and experiences are promoted:
        </v-flex>
        <v-flex xs4 md3 lg2 v-for="logo in logos" :key="logo.pk">
            <v-img :src="logo.logo"></v-img>
            <div>{{logo.name}}</div>
        </v-flex>
    </v-layout>
</template>

<script>
import axios from 'axios'

export default {
    props: {

    },

    data: () => ({
        logos: []
    }),

    created() {
        axios.get('/api/events/').then(res => {
            this.logos = res.data
        })
    },

    computed: {

    }
}
</script>
<style scoped lang="scss">

</style>