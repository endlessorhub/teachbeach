<template>
  <v-layout align-center justify-center row wrap>
      <Notifications
        :classes="classes"
        :private_enroll="private_enroll"
      >
        <template v-slot:empty >
            <v-flex xs12 md10 text-xs-center>
              <h3 style="text-align: center;">Thanks! You've responded to this notification.</h3>
            </v-flex>
        </template>
      </Notifications>

  </v-layout>
</template>

<script>
import axios from 'axios'
import metadata from '@/mixins/metadata'
import Notifications from '@/components/Dashboard/Teach/Components/Notifications'

export default {
    name: 'unauth_teacher_confirm_lessons',
    components: {
        Notifications,
    },
    mixins: [
        metadata,
    ],
    data: () => ({
        isLoading: false,
        private_enroll: [],
        classes: [],
    }),
    computed: {

    },
    methods: {
        reloadData() {
            this.isLoading = true
            axios.get(`/api/enr_from_secret/${this.$route.params.hash}/`).then((res) => {
                console.log('done', res)
                this.classes = res.data.classes
                this.private_enroll = res.data.private_enroll
            }).catch((e) => {
                console.log(e)

            }).then(() => {
                this.isLoading = false
            })
        },
    },
    created() {
        this.reloadData()
    }
}
</script>

<style lang="scss">

</style>