<template>
    <div class="t-wrapper">
        <v-layout align-top justify-center row wrap class="t-container">
            <v-flex xs12 class="text-xs-center">
                <div class="tc__supheader title">Congratulations on setting up your class</div>
                <div class="display-1 font-weight-bold">
                    Your live instruction business just got easier.
                </div>
                <div class="tc__top-text">
                    Start-up or transionning?  Get ready for the power of 5+ tools for the price and simplicity  of one.<br/>
                    Take back your time • Live support • 14 days free • From $3.90 per class per month
                </div>
            </v-flex>
            <price-compare
                :value="priceCompareData"
            />
            <v-flex xs12 class="text-xs-left">
                <div class="display-1 font-weight-bold">
                    Let's do this
                </div>
                <CreditCards
                    :btnText="btnText"
                    :successBtnText="successBtnText"
                    @cardAdded="submit"
                />
            </v-flex>
          </v-layout>
    </div>
</template>

<script>
import CreditCards from '@/components/basic/CreditCards'
import PriceCompare from '@/components/PriceCompare'
import priceCompareData from './priceCompareData'
import axios from 'axios'
import metadata from '@/mixins/metadata'
import { mapGetters } from 'vuex'

export default {
    mixins: [metadata],
    props: {

    },

    components: {
        CreditCards,
        PriceCompare,
    },

    data: () => ({
        btnText: 'Next',
        successBtnText: 'Great!',
        nextRoute: '/teachers/start',
        unauthRoute: '/teachers_promo',
        timeoutId: false,
        classId: null,
        priceCompareData,
    }),

    created: function () {
        this.classId = Number(this.$route.params.class_id) || null
        if(this.classId) {
            if(this.$route.query.n === 'tc') {
                this.nextRoute = `/dashboard/teach/classes`
            } else
                this.nextRoute = `/teachers/finish/${this.classId}`
        }
        if(!this.isLoggedIn) {
            return this.$router.push(this.unauthRoute)
        }
    },

    computed: {
        ...mapGetters([
            'isLoggedIn',
        ]),
    },

    methods: {
        submit () {
            if(this.timeoutId)
                clearTimeout(this.timeoutId)
            const action = this.classId ? axios.post(`/api/deactivate_class/`, {
                id: this.classId,
                deactivate: false,
            }) : Promise.resolve(true)
            action.then(res => {
                this.timeoutId = setTimeout(() => {
                    this.$router.push(this.nextRoute)
                }, 1000)
            }).catch(e => {
                console.log(e)
            })
        },
    }
}
</script>

<style scoped lang="scss">
    @import "@/styles/_variables.scss";
    .yes {
        font-size: 53px;
        font-weight: 900;
    }
    .separated {
        margin-top: 1em;
    }
    .t-wrapper {
        background-color: $platform-green;
        .t-container {
            padding: 20px;
            border-top-right-radius: 60px;
            border-bottom-left-radius: 60px;
            background-color: #e7e7e7;
            border-bottom: 10px solid $platform-green;
            &> div {
                padding: 0 10px;
            }
            .ver-divider {
                margin: 0px 1px 0px -2px;
            }
            .hor-divider {
                margin: 10px 20px;
            }
        }
    }
    li {
        list-style: none;
        .t-icon {
            margin: 0 5px;
            color: $platform-green;
        }
    }
    .tc {
        &__supheader {
            color: gray;
        }
        &__top-text {
            margin-bottom: 20px;
        }
    }
</style>