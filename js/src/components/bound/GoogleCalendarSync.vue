<template>
    <div v-if="gapiStatus === 'authcheckdone'">
        <v-btn
            color="success"
            @click="onClick"
            :loading="loading"
            :disabled="loading"
        >
            {{buttonName}}
        </v-btn>
        <v-menu offset-y bottom left>
          <template v-slot:activator="{ on }">
            <v-btn
                icon

                v-on="on"
            >
              <v-icon color="success darken-2">settings</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-tile
              v-for="(item, index) in buttonItems"
              :key="index"
              @click="item.callback"
            >
              <v-list-tile-title>{{ item.text }}</v-list-tile-title>
            </v-list-tile>
          </v-list>
        </v-menu>
    </div>
</template>

<script>

import {mapMutations, mapState} from 'vuex';

export default {
    props: {

    },
    components: {

    },
    data() {
        return {
            autoFetchEvents: false,
            buttonItems: [
                {text: 'Sync with another account', callback: () => this.syncWithAnother()},
            ]
        }
    },

    created() {
        this.$store.dispatch('gapi/init')
    },

    computed: {
        ...mapState({
            gapiAuthState: (state) => state.gapi.authState,
            gapiStatus: (state) => state.gapi.status,
            gapiLoading: (state) => state.gapi.isLoading,
        }),
        buttonName() {
            return `Sync from Google ${this.gapiAuthState || 'Calendar'}`
        },
        loading() {
            return this.gapiStatus !== 'authcheckdone' || this.gapiLoading
        }
    },

    methods: {
        onClick() {
            if(this.gapiAuthState) {
                this.$store.dispatch('gapi/syncEvents')
            } else {
                this.autoFetchEvents = true
                this.$store.dispatch('gapi/login')
            }
        },
        syncWithAnother() {
            this.$store.dispatch('gapi/logout').then(() => {
                this.autoFetchEvents = true
                return this.$store.dispatch('gapi/login')
            }).catch(e => {
                console.log(e)
            })
        }
    },

    watch: {
        gapiAuthState(val) {
            if(this.autoFetchEvents && val) {
                this.autoFetchEvents = false
                this.$store.dispatch('gapi/syncEvents')
            }
        }
    }
}
</script>