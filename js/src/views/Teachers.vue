<template>
  <div class="teachers">
    <div class="teacher-form-container flex xs12">
      <TeacherWizard v-on:openLoginForm="$emit('openLoginForm')" v-on:register:done="registerDone"/>
    </div>
  </div>
</template>

<script>
import TeacherWizard from '@/components/TeacherWizard.vue'
import metadata from '@/mixins/metadata'

export default {
    mixins: [metadata],
    name: 'teachers',
    components: {
        TeacherWizard
    },
    methods: {
        registerDone() {
            this.$emit('register:done')
        }
    }
}
</script>
<style scoped lang="scss">
.teachers {
    flex: 1 1 auto;
    text-align: center;
    .teacher-form-container {
        //width: 800px;
        margin: 0 auto;
    }
}
</style>