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
    name: 'buyMembership',
    components: {
        BaseBuyMembership,
    },
    props: {
        class_id: {
            type: Number,
        },
    },
    data() {
        return {
            teacher: null,
            membership: null,
        }
    },
    computed: {
        componentData() {
            if(!this.teacher || !this.membership)
                return null
            console.log(this.$route)
            return {
                ...this.membership,
                provider: this.teacher.user.is_company
                    ? this.teacher.user.company_profile.name
                    : `${this.teacher.first_name} ${this.teacher.last_name}`,
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
            axios.all([
                axios.get(`/api/class_teacher/${this.class_id}/`),
                axios.get(`/api/class_membership/${this.class_id}/`),
            ]).then(([teacher, membership]) => {
                this.teacher = teacher.data.teacher
                this.membership = membership.data.membership
            })
        },
    },
}
</script>