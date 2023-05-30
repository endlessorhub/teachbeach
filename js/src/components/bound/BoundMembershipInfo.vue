<template>
    <v-progress-circular
        v-if="isLoading"
        indeterminate
    ></v-progress-circular>
    <base-membership-info v-else v-bind="membership"/>
</template>

<script>
import axios from 'axios'
import BaseMembershipInfo from '@/components/basic/BaseMembershipInfo';

export default {
    name: 'BoundMembershipInfo',
    components: {
        BaseMembershipInfo,
    },
    props: {
        id: {
            type: Number,
            default: 0,
        },
    },
    data: () => ({
        isLoading: false,
        membership: {},
    }),
    created() {
        this.reload()
    },
    computed: {

    },
    methods: {
        reload() {
            this.isLoading = true
            return axios.get(`/api/teacher_membership/${this.id}/`).then((res) => {
                if(res.data.success) {
                    this.membership = res.data.membership
                }
            }).finally(() => {this.isLoading = false})
        },
    },
}
</script>