<template>
    <v-layout class="buy-membership" align-start justify-center row wrap>
        <v-flex xs12 v-if="media">
            <div class="buy-membership__image-container">
                <v-img :src="media"/>
            </div>
        </v-flex>
        <v-flex xs12 >
            <h1 class="buy-membership__title">{{name}}</h1>
            <div v-if="isMemberOfCompany" class="buy-membership__join-status">
                <v-chip color="platform-green" text-color="white">
                  <v-avatar>
                    <v-icon>check_circle</v-icon>
                  </v-avatar>
                  Joined
                </v-chip>
                {{ formattedPrice }}
            </div>
            <div v-else class="buy-membership__join-status">
                Join as a member for
                <v-radio-group v-model="selectedPrice" row>
                  <v-radio v-for="price in priceItems" :key="price.value" :label="price.text" :value="price"></v-radio>
                </v-radio-group>
            </div>
        </v-flex>
        <v-flex xs12 md6>
            <div class="buy-membership__description" v-html="formattedDescription"></div>
        </v-flex>
        <v-flex xs12 md6 v-show="!isMemberOfCompany">
            <v-card
                class="buy-membership__preview-payments"
            >
              <v-card-title primary-title>
                <div>
                  <div class="headline text-xs-left">Payment information</div>
                </div>
              </v-card-title>
              <v-card-text class="text-xs-left">
                  <span v-if="isPreview">List of saved credit cards and form to add a new one</span>
                  <credit-cards
                    v-else
                    url="/api/stripe/buy_membership"
                    btn-text="JOIN"
                    success-btn-text="Done"
                    btn-color="#95d807"
                    :payment-options="paymentOptionsWithPeriod"
                    @cancel="onCancel"
                    @doneSubmit="onDoneSubmit"
                    @cardError="onCardError"
                    @cardAdded="onCardAdded"
                  />
              </v-card-text>
              <v-card-actions v-if="isPreview" class="buy-membership__preview-payments-actions">
                  <v-btn color="platform-green">Buy Membership</v-btn>
              </v-card-actions>
            </v-card>
        </v-flex>
        <v-flex xs12 md6 v-show="isMemberOfCompany">
            <v-btn color="platform-green" @click="onReturn">Return</v-btn>
        </v-flex>
    </v-layout>
</template>

<script>
import { mapMutations, mapGetters } from 'vuex'
import CreditCards from '@/components/basic/CreditCards'
import utils from "@/lib/utils";

const periods = {
    weekly: 'week',
    monthly: 'month',
    yearly: 'year',
};

export default {
    name: 'BaseBuyMembership',
    components: {
        CreditCards,
    },
    props: {
        id: {
            type: Number,
        },
        name: {
            type: String,
        },
        media: {
            type: String,
        },
        currency: {
            type: String,
        },
        weekly_rate: {
            type: Number,
        },
        monthly_rate: {
            type: Number,
        },
        yearly_rate: {
            type: Number,
        },
        period: {
            type: Number,
        },
        description: {
            type: String,
        },
        provider: {
            type: String,
        },
        returnRoute: {
            type: String,
        },
        paymentOptions: {
            type: Object,
        },
        curBtnColor: {
            type: String,
            default: ''
        },
        isPreview: {
            type: Boolean,
            default: false,
        },
    },
    data() {
        return {
            selectedPrice: null,
        }
    },
    created() {
        if (this.priceItems.length > 0) this.selectedPrice = this.priceItems[0];
    },
    computed: {
        ...mapGetters([
            'isMember',
        ]),
        isMemberOfCompany() {
            return this.isMember(this.id) && !this.isPreview;
        },
        formattedName() {
            return this.name ? '' : `"${this.name}"`
        },
        formattedPrice() {
            if (this.isMemberOfCompany) {
                const membership = this.$store.state.user.memberships.find(m => m.membership === this.id);
                return `${utils.formatPrice(membership[`${membership.period}_rate`], this.currency)} per ${periods[membership.period]}`;
            }
            return this.selectedPrice ? this.selectedPrice.text : 'Please select a pricing option';
        },
        priceItems() {
            const res = [];
            if (Number(this.weekly_rate)) res.push({text: `${utils.formatPrice(this.weekly_rate, this.currency)} per week`, value: 'weekly'});
            if (Number(this.monthly_rate)) res.push({text: `${utils.formatPrice(this.monthly_rate, this.currency)} per month`, value: 'monthly'});
            if (Number(this.yearly_rate)) res.push({text: `${utils.formatPrice(this.yearly_rate, this.currency)} per year`, value: 'yearly'});
            return res;
        },
        formattedDescription() {
            return '<p>'+this.description.replace(/\n/g, '<p>')
        },
        paymentOptionsWithPeriod() {
            return {
                ...this.paymentOptions,
                period: this.selectedPrice ? this.selectedPrice.value : null,
            };
        },
    },
    watch: {
        priceItems(vals) {
            if (vals.length > 0) this.selectedPrice = vals[0];
        },
    },
    methods: {
        ...mapMutations([
            'setGlobalError'
        ]),
        onCancel() {
            this.$router.push(this.returnRoute)
        },
        onDoneSubmit() {
            this.$router.push(this.returnRoute)
        },
        onReturn() {
            this.$router.push(this.returnRoute)
        },
        onCardError(err) {
            this.setGlobalError(err.message)
        },
        onCardAdded(res) {
            this.$store.commit('setUser', {
                ...this.$store.state.user,
                memberships: [...(this.$store.state.user.memberships || []), res.student_membership],
            })
            setTimeout(() => {
                this.$router.push(this.returnRoute)
            }, 1000)
        }
    },
}
</script>
<style lang="scss">
@import "../../styles/_variables.scss";

.buy-membership {
    margin-top: 1em;
    padding: 0 1em;
    &__title {
        text-align: left;
    }
    &__join-status {
        text-align: left;
        font-weight: bold;
    }
    &__description {
        text-align: left;
        padding: 20px 0;
    }
    &__image-container {
        width: 300px;
    }
    &__preview-payments {
        min-height: 200px;
    }
    &__preview-payments-actions {
        justify-content: center;
    }
    p {
        text-indent: 1em;
    }
}
</style>