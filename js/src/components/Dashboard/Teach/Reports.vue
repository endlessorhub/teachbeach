<template>
    <v-layout align-center justify-center row wrap>
        <v-flex xs9>
            <v-radio-group
                v-model="entity"
                :error-messages="entityErr"
                @change="downloadTableReport()"
                row
            >
                <v-radio v-for="item in items" :value="item.value" :label="item.text" :key="item.value"></v-radio>
            </v-radio-group>

            <!--v-select
              :items="items"
              label="Export"
              :error-messages="entityErr"
              v-model="entity"
              @change="entityErr=[]"
              return-object
            ></v-select-->
        </v-flex>
        <v-flex xs3>

        </v-flex>
        <v-flex xs4 class="text-xs-left">
            <v-menu
                ref="menuCSVStartDate"
                v-model="openedCSVStartDate"
                :nudge-right="40"
                :return-value.sync="csvStartDate"
                :close-on-content-click="false"
                lazy
                transition="scale-transition"
                offset-y
                full-width
                max-width="290px"
                min-width="290px"
            >
                <template v-slot:activator="{ on }">
                  <v-text-field
                    v-model="csvStartDate"
                    label="Start Date"
                    prepend-icon="event"
                    readonly
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-date-picker
                  v-model="csvStartDate"
                  scrollable
                  @change="$refs.menuCSVStartDate.save(csvStartDate)"
                >
                </v-date-picker>
            </v-menu>
        </v-flex>
        <v-flex xs4 class="text-xs-left">
            <v-menu
                ref="menuCSVEndDate"
                v-model="openedCSVEndDate"
                :nudge-right="40"
                :return-value.sync="csvEndDate"
                :close-on-content-click="false"
                lazy
                transition="scale-transition"
                offset-y
                full-width
                max-width="290px"
                min-width="290px"
            >
                <template v-slot:activator="{ on }">
                  <v-text-field
                    v-model="csvEndDate"
                    label="End Date"
                    prepend-icon="event"
                    readonly
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-date-picker
                  v-model="csvEndDate"
                  scrollable
                  @change="$refs.menuCSVEndDate.save(csvEndDate)"
                >
                </v-date-picker>
            </v-menu>
        </v-flex>
        <v-flex sm4 xs8 class="text-xs-left">

        </v-flex>
        <v-flex xs12>
            <v-progress-circular
              v-if="isLoading"
              indeterminate
              color="grey"
            ></v-progress-circular>
            <v-toolbar flat color="white" v-if="tableReady">
              <v-toolbar-title>{{toolbarTitle}}</v-toolbar-title>
              <v-spacer></v-spacer>
              <v-btn
                  color="platform-green"
                  @click="downloadCSVReport()"
                  :disabled="downloadBtnDisabled"
                  :loding="downloadBtnDisabled"
              >
                Download CSV
              </v-btn>
            </v-toolbar>
            <v-data-table
                v-if="tableReady"
                :headers="tableHeaders"
                :items="tableItems"
                class="elevation-1"
                :custom-sort="tableSort"
                :pagination.sync="pagination"
              >
                <template v-slot:items="props">
                    <td v-for="(cell, i) in props.item" class="text-xs-left" :key="i">{{ cell }}</td>
                </template>
            </v-data-table>
        </v-flex>
    </v-layout>
</template>

<script>
// @ is an alias to /src
import _ from 'lodash'
import axios from 'axios'
import parse from 'csv-parse'
import moment from 'moment'

export default {
    name: 'dashboard_teach_reports',
    data: () => ({
        isLoading: false,
        openedCSVStartDate: false,
        csvStartDate: '',
        openedCSVEndDate: false,
        csvEndDate: '',
        items: [
            {value: 'class', text: 'Transaction activity', url: '/api/csv_export/'},
            {value: 'student', text: 'Students', url: '/api/csv_student_export/'},
            {value: 'members', text: 'Members transactions', url: '/api/csv_members_export/'},
        ],
        entity: 'class',
        entityErr: [],
        //showInApp: false,
        tableReady: false,
        tableHeaders: [],
        tableItems: [],
        downloadBtnDisabled: false,
        pagination: {
            descending: true,
            page: 1,
            rowsPerPage: 20,
            sortBy: 0,
            totalItems: 0
        },
    }),
    props: [],

    components: {

    },
    created() {
        //this.entity = this.items[0]
        this.downloadTableReport()
    },
    computed: {
        toolbarTitle() {
            return _.find(this.items, {value: this.entity}).text
        },
        entityUrl() {
            return _.find(this.items, {value: this.entity}).url
        }
    },
    methods: {
        downloadTableReport() {
            this.entityErr = []
            if(!this.entity) {
                this.entityErr.push('Please select entity to export')
                return
            }
            this.isLoading = true
            this.tableReady = false
            axios.get(this.entityUrl, {
                params: {
                    from_date: this.csvStartDate,
                    to_date: this.csvEndDate,
                }
            }).then(res => {
                parse(res.data, {}, (err, out) => {
                    if(err) {
                        console.warn(err)
                        return
                    }
                    //console.log(out)
                    this.tableHeaders = _.map(out[0], (v, i) => ({
                        text: v,
                        value: i,
                        align: 'left',
                    }))
                    this.tableItems = _.filter(out.splice(1), v => v)
                    this.tableReady = true
                })
            }).catch(e => console.log(e)).then(res => {
                this.isLoading = false
            })
        },
        downloadCSVReport() {
            this.entityErr = []
            if(!this.entity) {
                this.entityErr.push('Please select entity to export')
                return
            }
            this.downloadBtnDisabled = true
            axios.get(this.entityUrl, {
                params: {
                    from_date: this.csvStartDate,
                    to_date: this.csvEndDate,
                }
            }).then(res => {
                const blob = new Blob([res.data], { type: res.headers['content-type'] })
                const link = document.createElement('a')
                link.href = window.URL.createObjectURL(blob)
                const contentDispositionParsed = res.headers['content-disposition'].match(/filename="(.+)"/)
                link.setAttribute('download', contentDispositionParsed[1])
                link.click()
            }).catch(e => console.log(e)).then(res => {
                this.downloadBtnDisabled = false
            })
        },
        tableSort(items, index, isDescending) {
            console.log(items, index, isDescending)
            if(index === 0) {
                return items.sort((a, b) => {
                    const d1 = moment(a[0], 'MMM DD, YYYY')
                    const d2 = moment(b[0], 'MMM DD, YYYY')
                    return isDescending ? d2-d1 : d1-d2
                })
            }
            return isDescending ? _.reverse(_.sortBy(items, index)) : _.sortBy(items, index)
        }
    },

    watch: {
        csvStartDate(v) {
            this.downloadTableReport()
        },
        csvEndDate(v) {
            this.downloadTableReport()
        },
    }
}
</script>
<style lang="scss">

</style>