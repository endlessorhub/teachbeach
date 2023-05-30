<template>
  <TeacherPage>
    <TeacherAllDone :isEditMode="isEditMode" :isSuccess="!!classId" :classId="classId"/>
  </TeacherPage>
</template>

<script>
import { mapState } from 'vuex'
import TeacherPage from './Page.vue'
import TeacherAllDone from '@/components/TeacherAllDone.vue'

export default {
    name: 'teachers-finish',
    components: {
        TeacherPage,
        TeacherAllDone,
    },
    data: () => ({
        classId: null,
    }),
    created() {
        if(this.$route.params.class_id) {
            this.classId = Number(this.$route.params.class_id)
        } else
            this.$store.dispatch('loadDraft')
    },
    computed: {
        ...mapState({
            isEditMode: state => !!(state.teacherGroupClass && state.teacherGroupClass.id)
        })
    }
}
</script>
<style scoped lang="scss">

</style>