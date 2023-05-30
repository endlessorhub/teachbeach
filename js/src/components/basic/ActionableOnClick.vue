<template>
    <span>
        <slot :loading="isLoading" :click="onClick" :isDone="isDone" :isFail="isFail"></slot>
        <Snack v-model="error"/>
    </span>
</template>

<script>
import Snack from '@/components/basic/Snack'

export default {
    props: {
        'action': {
            type: Function,
            default: () => new Promise((resolve, reject) => resolve(true))
        },
    },

    components: {
        Snack,
    },

    data: () => ({
        isLoading: false,
        error: '',
        isDone: false,
        isFail: false,
    }),

    methods: {
        onClick() {
            this.isLoading = true
            this.action().then((res) => {
                this.isDone = true
                this.$emit('success', res)
            }).catch(e => {
                this.isFail = true
                this.$emit('fail', e)
                if(e.message)
                    this.error = e.message
            }).finally(() => {
                this.isLoading = false
            })
        },
    },

}
</script>

<style scoped lang="scss">

</style>