<template>
    <v-layout align-center justify-center row wrap>
        <h3>Payment account:</h3>
        <v-flex xs12 class="text-xs-left">
            <CreditCards
                btnText="Save"
            />
        </v-flex>
    </v-layout>
</template>

<script>

import CreditCards from '@/components/basic/CreditCards'

export default {
    name: 'dashboard_learner_account',
    data: () => ({

    }),
    props: [],
    components: { CreditCards },
}
</script>
<style lang="scss">

</style>