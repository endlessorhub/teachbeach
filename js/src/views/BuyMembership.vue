<template>
    <div class="text-xs-center" style="width: 100%;">
        <base-buy-membership
            v-if="componentData"
            v-bind="componentData"
        />
        <v-progress-circular
            v-else
            indeterminate
            color="grey"
        ></v-progress-circular>
    </div>
</template>

<script>
import axios from 'axios'
import { mapMutations } from 'vuex'
import BaseBuyMembership from '@/components/basic/BaseBuyMembership'
import utils from "@/lib/utils";

export default {
    name: 'BuyMembership',
    components: {
        BaseBuyMembership,
    },
    props: {
        id: {
            type: Number,
        },
    },
    data() {
        return {
            membership: null,
        }
    },
    computed: {
        componentData() {
            if(!this.membership)
                return null
            return {
                ...this.membership,
                provider: this.membership.owner.is_company
                    ? this.membership.owner.company_profile.name
                    : `${this.membership.owner.teacher.first_name} ${this.membership.owner.teacher.last_name}`,
                paymentOptions: {
                    membership_id: this.membership.id,
                },
                returnRoute: this.$route.query.return,
                curBtnColor: 'platform-green',
                isPreview: this.isPreview,
            }
        },
        isPreview() {
            return 'preview' in this.$route.query;
        },
    },
    mounted() {
        this.loadData()
    },
    methods: {
        loadData() {
            return axios.get(`/api/teacher_membership/${this.id}/`).then((membership) => {
                this.membership = membership.data.membership
            })
        },
    },
}
</script>