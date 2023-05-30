<template>
  <div class="learners">
    <v-layout align-center justify-center>
      <TeacherForm v-bind:on-success="onSuccess" v-bind:registerButton="true"/>
    </v-layout>
  </div>
</template>

<script>
import TeacherForm from '@/components/TeacherForm.vue'
import metadata from '@/mixins/metadata'

export default {
    mixins: [metadata],
    props: [],
    data: () => ({

    }),
    name: 'register',
    components: {
        TeacherForm
    },
    created() {

    },
    methods: {
        onSuccess() {
            this.$router.go(-1)
        },
    },
}
</script>

<style lang="scss">

</style>