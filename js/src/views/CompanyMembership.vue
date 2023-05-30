<template>
    <base-buy-membership
        v-if="componentData"
        v-bind="componentData"
    />
    <v-progress-circular
        v-else
        indeterminate
        color="grey"
    ></v-progress-circular>
</template>

<script>
import axios from 'axios'
import { mapMutations } from 'vuex'
import BaseBuyMembership from '@/components/basic/BaseBuyMembership'
import utils from "@/lib/utils";

export default {
    name: 'CompanyMembership',
    components: {
        BaseBuyMembership,
    },
    props: {
        company_id: {
            type: Number,
        },
    },
    data() {
        return {
            company: null,
            membership: null,
        }
    },
    computed: {
        componentData() {
            if(!this.company || !this.membership)
                return null
            return {
                name: this.membership.name,
                currency: this.membership.currency,
                monthly_rate: this.membership.monthly_rate,
                description: this.membership.description,
                provider: this.company.name,
                paymentOptions: {
                    membership_id: this.membership.id,
                },
                returnRoute: this.$route.query.return
            }
        }
    },
    mounted() {
        this.loadData()
    },
    methods: {
        loadData() {
            axios.get(`/api/company_profile/${this.company_id}/`).then((company) => {
                this.company = company.data
                if (this.company.user.membership)
                    return axios.get(`/api/teacher_membership/${this.company.user.membership}/`)
            }).then((membership) => {
                this.membership = membership.data.membership
            })
        },
    },
}
</script>