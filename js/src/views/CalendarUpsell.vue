<template>
<div class="email-upsell-page">
    <v-container grid-list-md text-xs-center>
        <v-layout align-top justify-center row wrap>
            <v-flex xs1 >
                <v-icon x-large>fas fa-rocket</v-icon>
            </v-flex>
            <v-flex xs11 class="text-xs-left">
                <h3>Media boost:</h3>
                <div class="description-text">
                    <v-radio-group v-model="paymentOption" hide-details>
                        <v-radio
                            :value="250"
                        >
                            <template v-slot:label >
                                <div :class="{'description-item': true, 'active': paymentOption === 250}">
Go national with your Zoom and online lessons. <br/>
Submit  your class to 900 online and print community calendars across the country for $250
                                </div>
                            </template>
                        </v-radio>
                        <v-radio
                            :value="25"
                        >
                            <template v-slot:label >
                                <div :class="{'description-item': true, 'active': paymentOption === 25}">
Post to all community event calendars in my city  $25
                                </div>
                            </template>
                        </v-radio>
                    </v-radio-group>
                </div>
            </v-flex>
            <v-flex xs12 class="text-xs-right">
                <CreditCards v-if="showCreditCard"
                             :payment-options="{boost_option_id: options[paymentOption]}"
                             :cancel-btn="true"
                             :url="`/api/boost_class/${class_id}/`"
                             successBtnText="Done"
                             @cardAdded="submit"
                             @cancel="cancel" />
                <v-btn v-if="!showCreditCard" @click="cancel" :disabled="isLoading">No, thanks</v-btn>
                <v-btn v-if="!showCreditCard" @click="submit" :loading="isLoading" :disabled="isLoading" color="platform-green">ADD</v-btn>
            </v-flex>
        </v-layout>
        <PromotionLogos />
    </v-container>
</div>
</template>

<script>
import CreditCards from '@/components/basic/CreditCards'
import PromotionLogos from '@/components/basic/PromotionLogos'
import axios from 'axios'

import utils from '@/lib/utils.js'
import metadata from '@/mixins/metadata'

export default {
    mixins: [metadata],
    props: {
        class_id: Number,
    },
    components: {
        CreditCards,
        PromotionLogos,
    },

    data: () => ({
        isLoading: false,
        options: {
            250: 1,
            25: 2,
        },
        paymentOption: 250,
        showCreditCard: true,
    }),

    created: function () {

    },

    computed: {

    },

    methods: {
        submit(id) {
            console.log('submit', id)
            //this.$router.push(`/teacher_checkout/${id}`)
            // checkout and redirect to dashboard
            setTimeout(() => this.$router.push('/dashboard/teach/classes'), 1000)
        },
        cancel() {
            this.$router.push('/dashboard/teach/classes')
        }
    }
}
</script>

<style scoped lang="scss">
.email-upsell-page {
    h3 {
        font-size: 34px;
    }
    .description-text {
        height: 100px;
    }
    .description-item {
        font-size: 20px;
        transition: all .5s ease;

        &.active {
            color: #000;
        }
    }
}
</style>