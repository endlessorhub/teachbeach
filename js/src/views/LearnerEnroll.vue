<template>
    <v-progress-circular indeterminate></v-progress-circular>
</template>

<script>
import axios from 'axios'

export default {
    name: 'learner_enroll',
    props: [],
    data: () => ({
        step: null,
        id: null,
        order_id: null,
    }),
    components: {

    },
    created() {
        this.$store.commit('resetLearnerData', ['learnerNeeds'])
        if(this.$route.params.step) {
            this.step = Number(this.$route.params.step)
        }
        if(this.$route.params.id) {
            this.id = Number(this.$route.params.id)
        }
        if(this.$route.params.order_id) {
            this.order_id = Number(this.$route.params.order_id)
        }
        if(!this.$store.state.user) {
            this.$store.commit('setLoginFormOpened', {})
        }
        if(this.order_id && this.$store.state.user) {
            axios.get('/api/orders/'+this.order_id+'/').then(res => {
                const dataToSet = {
                    package: res.data.data.package,
                    selectedLessons: [],
                }
                if('persons' in res.data.data)
                    dataToSet.persons = res.data.data.persons
                if('learnerNeeds' in res.data.data)
                    dataToSet.learnerNeeds = res.data.data.learnerNeeds
                this.$store.commit('setLearnerData', dataToSet)
                this.$router.replace(`/learners/${this.id}/${this.step}`)
            }).catch(e => {
                this.$router.replace(`/learners/${this.id}/${this.step}`)
            })
        } else
            this.$router.replace(`/learners/${this.id}/${this.step}`)
    },
}
</script>

<style lang="scss">

</style>