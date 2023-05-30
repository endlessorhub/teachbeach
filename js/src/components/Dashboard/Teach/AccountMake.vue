<template>
    <v-layout align-top justify-center row wrap>
        <v-flex xs12 class="text-xs-left">
          Please choose card or add payment information
        </v-flex>
        <v-flex xs12 class="text-xs-left">
            <CreditCards
                :btnColor="btnColor"
                :btnText="btnText"
            />
        </v-flex>
        <v-flex xs12 class="text-xs-center" v-if="currentOption">
            <v-btn @click="cancelMembership" :loading="isLoading" >
                Cancel {{packageName}} membership
            </v-btn>
        </v-flex>
    </v-layout>
</template>

<script>
import utils from '@/lib/utils.js'
import axios from 'axios'

import CreditCards from '@/components/basic/CreditCards'

export default {
    props: {

    },

    components: { CreditCards },

    data: () => ({
        btnText: 'Add',
        btnColor: '',
        isLoading: false,
        package: null,
        currentOption: null,
    }),

    created: function () {
        this.isLoading = true
        axios.get('/api/buy_membership').then(res => {
            this.options = res.data.available_options
            this.canBook = res.data.can_book
            this.currentOption = res.data.current_option
            this.isLoading = false
        })
    },

    computed: {
        cost() {
            return utils.formatPrice(this.costNumber, 'usd')
        },
        costNumber() {
            return this.currentOption ? this.currentOption.amount : 0
        },
        packageName() {
            return this.currentOption ? this.currentOption.name : ''
        },
        classNumber() {
            return this.currentOption ? this.currentOption.num_classes : 0
        },
        monthly() {
            return this.currentOption && this.currentOption.is_monthly ? 'per month' : ''
        }
    },

    methods: {
        cancelMembership() {
            this.isLoading = true
            axios.post(`/api/cancel_membership`, {id: this.currentOption.id}).then(res => {
                this.isLoading = false
                this.$router.go(0)
            })
        },
    }
}
</script>

<style scoped lang="scss">
.teacher-checkout-page {
    .shrinked {
        padding: 0 !important;
    }
    .expanded{
        padding: 20px 0 !important;
        margin: 20px 0 !important;
    }
}
</style>