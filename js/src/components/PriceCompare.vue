<template>
    <div class="price-compare">
        <v-card flat style="border-radius: 5px;">
            <v-card-text>
                <v-layout align-top justify-center row wrap>
                    <v-flex xs3 sm6 class="text-xs-left">

                    </v-flex>
                    <v-flex xs3 sm2 class="text-xs-center">
                        <div class="price-compare__cell-title price-compare__cell-title_aqua">Instructor</div>
                        <div class="price-compare__cell-subtitle">For individuals</div>
                        <div class="price-compare__cell-text">
                            $5/class<br>
                            Up to 3 class pages<br>
                            & all core tools
                        </div>
                        <div class="price-compare__cell-start">
                            <v-btn depressed large class="platform-blgr" to="/teachers/company-or-individual" style="border-radius: 5px;height: 56px;"><span class="button-text">Start Free</span></v-btn>
                        </div>
                    </v-flex>
                    <v-flex xs3 sm2 class="text-xs-center">
                        <div class="price-compare__cell-title price-compare__cell-title_green">Academy</div>
                        <div class="price-compare__cell-subtitle">For teams and start-ups<br/>BEST VALUE</div>
                        <div class="price-compare__cell-text">
                            $3.90 class <br>
                            Up to 10 classes<br>
                            Core tools, full website with your logo & marketing
                        </div>
                        <div class="price-compare__cell-start">
                            <v-btn depressed large class="platform-blgr" to="/teachers/company-or-individual" style="border-radius: 5px;height: 56px;"><span class="button-text">Start Free</span></v-btn>
                        </div>
                    </v-flex>
                    <v-flex xs3 sm2 class="text-xs-center">
                        <div class="price-compare__cell-title price-compare__cell-title_gold">Powerhouse</div>
                        <div class="price-compare__cell-subtitle">For scaling up</div>
                        <div class="price-compare__cell-text">
                            From $179 month <br>
                            Unlimited classes <br>
                            Academy plus extra services
                        </div>
                        <div class="price-compare__cell-start">
                            <v-btn depressed large class="platform-blgr" to="/teachers/company-or-individual" style="border-radius: 5px;height: 56px;"><span class="button-text">Start Free</span></v-btn>
                        </div>
                    </v-flex>
                    <template v-for="(section, i) in value">
                        <v-flex xs12 class="text-xs-left">
                            <div class="price-compare__row-title">{{ section.title }}</div>
                        </v-flex>
                        <template v-for="(row, j) in section.items">
                            <v-flex xs3 sm6 class="text-xs-left">
                                <span>{{ row.title }}</span>
                                <v-tooltip v-if="row.tooltip"top>
                                  <template v-slot:activator="{ on }">
                                    <v-btn icon v-on="on">
                                      <v-icon>info</v-icon>
                                    </v-btn>
                                  </template>
                                  <span>{{ row.tooltip }}</span>
                                </v-tooltip>
                            </v-flex>
                            <v-flex xs3 sm2 class="text-xs-center">
                                <v-icon v-if="row.p1" color="platform-green">check</v-icon>
                                <v-icon v-else color="gray">clear</v-icon>
                            </v-flex>
                            <v-flex xs3 sm2 class="text-xs-center">
                                <v-icon v-if="row.p2" color="platform-green">check</v-icon>
                                <v-icon v-else color="gray">clear</v-icon>
                            </v-flex>
                            <v-flex xs3 sm2 class="text-xs-center">
                                <v-icon v-if="row.p3" color="platform-green">check</v-icon>
                                <v-icon v-else color="gray">clear</v-icon>
                            </v-flex>
                        </template>
                    </template>
                    <v-flex xs3 sm6 class="text-xs-left">

                    </v-flex>
                    <v-flex xs3 sm2 class="text-xs-center">
                        <div class="price-compare__cell-title price-compare__cell-title_aqua">Instructor</div>
                        <div class="price-compare__cell-text">
                            From $5/class<br>
                            $15/mo
                        </div>
                        <div class="price-compare__cell-start">
                            <v-btn depressed large class="platform-blgr" to="/teachers/company-or-individual" style="border-radius: 5px;height: 56px;"><span class="button-text">Start Free</span></v-btn>
                        </div>
                    </v-flex>
                    <v-flex xs3 sm2 class="text-xs-center">
                        <div class="price-compare__cell-title price-compare__cell-title_green">Academy</div>
                        <div class="price-compare__cell-text">
                            From $3.50/class<br>
                            $35 a month
                        </div>
                        <div class="price-compare__cell-start">
                            <v-btn depressed large class="platform-blgr" to="/teachers/company-or-individual" style="border-radius: 5px;height: 56px;"><span class="button-text">Start Free</span></v-btn>
                        </div>
                    </v-flex>
                    <v-flex xs3 sm2 class="text-xs-center">
                        <div class="price-compare__cell-title price-compare__cell-title_gold">Powerhouse</div>
                        <div class="price-compare__cell-text">
                            From $179/month <br>
                            <br>
                        </div>
                        <div class="price-compare__cell-start">
                            <v-btn depressed large class="platform-blgr" to="/teachers/company-or-individual" style="border-radius: 5px;height: 56px;"><span class="button-text">Start Free</span></v-btn>
                        </div>
                    </v-flex>
                </v-layout>
            </v-card-text>
        </v-card>
    </div>
</template>
<script>
export default {
    name: 'PriceCompare',
    props: {
        value: {
            type: Array,
            default: () => ([]),
        }
    },
    mounted() {
        console.log(this.value);
    },
}
</script>

<style scoped lang="scss">
.price-compare {
    &__cell-title {
        font-size: 2em;
        font-weight: bold;

        &_aqua {
            color: aqua;
        }
        &_green {
            color: green;
        }
        &_gold {
            color: gold;
        }
    }
    &__cell-subtitle {
        font-size: 1.2em;
    }
    &__cell-text {

    }
    &__cell-start {

    }
    &__row-title {
        font-weight: bold;
    }
}
</style>