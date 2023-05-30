<template>
    <span>
        <slot name="button">
            <v-tooltip top content-class="teachbeach-tooltip" v-model="tooltipOpened">
              <template v-slot:activator="{ on }">
                <v-btn icon @click="formOpened=true" v-on="on" :style="btnStyle">
                    <v-icon color="platform-green" class="icon">event</v-icon>
                </v-btn>
              </template>
              <span>Sync to calendar</span>
            </v-tooltip>
        </slot>
        <v-dialog v-model="formOpened" max-width="500px">
            <v-card>
              <v-card-title>
                Sync to Calendar
              </v-card-title>

              <v-card-text>
                  <v-layout align-center justify-center row wrap>
                      <v-flex v-else xs12 class="text-xs-left" v-if="formSent">
                          Open downloaded file and import into your calendar
                      </v-flex>
                      <v-flex v-if="!formSent" xs12 class="text-xs-center" v-else>
                          <v-btn color="primary" @click="sendForm">Add to Calendar</v-btn>
                      </v-flex>

                  </v-layout>
              </v-card-text>

              <v-card-actions>
              </v-card-actions>
            </v-card>
        </v-dialog>
    </span>
</template>
<script>
import axios from 'axios'

export default {
    name: 'calendar_popup_form',
    data: () => ({
        isLoading: false,
        formOpened: false,
        formSent: false,
        tooltipOpened: false,
    }),
    props: [
        'formData',
        'filename',
        'isTooltipVisible',
        'isPopupOpened',
        'isButtonHidden',
    ],
    mounted() {
        this.formOpened = this.isPopupOpened
        this.$nextTick(() => {
            if(this.isTooltipVisible) {
                this.tooltipOpened = true
            }
        })
    },
    computed: {
        btnStyle() {
            const res = {
                'margin': '6px',
            }
            if(this.isButtonHidden)
                res.display = 'none'
            return res
        }
    },
    methods: {
        sendForm() {
            this.isLoading = true
            axios.post('/api/ical/', this.formData).then(res => {
                const blob = new Blob([res.data], { type: res.headers['content-type'] })
                const link = document.createElement('a')
                link.href = window.URL.createObjectURL(blob)
                link.setAttribute('download', this.filename)
                link.click()
            }).then(() => {
                this.formSent = true
                this.$emit('downloaded')
            }).catch((e) => {
                console.log(e)
            }).then(() => {
                this.isLoading = false
            })
        },

    },
    watch: {
        isPopupOpened(v) {
            this.formOpened = v
        },
        formOpened(v) {
            if(!v)
                this.$emit('closed')
        }
    },
}
</script>
<style lang="scss" scoped>
.icon {
    font-size: 2.6em;
}
</style>