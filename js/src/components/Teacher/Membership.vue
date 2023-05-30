<template>
    <bound-membership
        @saved="onSaved"
        @cancel="onCancel"
    />
</template>

<script>
import BoundMembership from '@/components/bound/BoundMembership'

export default {
    name: 'TeacherMembership',
    components: {
        BoundMembership,
    },
    methods: {
        onSaved() {
            this.$emit('next:step')
        },
        onCancel() {
            this.$emit('prev:step')
        }
    },
}
</script>