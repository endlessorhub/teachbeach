<template>
    <v-layout align-start justify-center row wrap class="wrapper">
        <v-flex xs12>
            <router-view base="/dashboard/"/>
        </v-flex>
    </v-layout>
</template>

<script>
import metadata from '@/mixins/metadata'

export default {
    name: 'dashboard',
    mixins: [metadata],
    data: () => ({
        isLoading: false,
        currentTab: null,
    }),
    props: [],
    components: {

    },
    created() {
        /*
        if(this.$route.name == 'dashboard') {
            axios.get('/api/learner/classes/').then(res => {
                if(res.data.private_enroll.length && res.data.group_enroll.length && res.data.orders.length) {
                    this.$router.push('/dashboard/learn')
                } else {
                    this.$router.push('/dashboard/teach/classes')
                }
            })
        }
        */
        /*
        axios.all([axios.get('/api/teacher_classes/'), axios.get('/api/learner/classes/')]).then(axios.spread((tc, lc) => {

        }))
        */
    },
    mounted: function () {
        /*
        this.$nextTick(function () {
            console.log('nextTick')
        })
        */
    },
    computed: {

    },
    methods: {

    },

    watch: {

    }
}
</script>
<style lang="scss" scoped>
.wrapper {
    flex-grow: 0;
}
.nav-btn >>> a {
    opacity: 1;
    font-weight: bold;
    &.active {
        background-color: rgba(25, 118, 210, 0.7);
    }
}
</style>