<script>
import {VDatePickerDateTable, VDatePicker} from 'vuetify/es5/components/VDatePicker'
import {VTooltip} from 'vuetify/es5/components/VTooltip'
import {pad} from 'vuetify/es5/components/VDatePicker/util'
import isDateAllowed from 'vuetify/es5/components/VDatePicker/util/isDateAllowed'

import _ from 'lodash'
import utils from '@/lib/utils.js'

let VDatePickerDateTableMod = {
    extends: VDatePickerDateTable,
    props: {
        dateTimeDict: Object,
    },
    methods: {
        genButton: function genButton(value, isFloating, mouseEventType, formatter) {
            //console.log(isDateAllowed, pad)
            let isAllowed = isDateAllowed(value, this.min, this.max, this.allowedDates);
            let isSelected = value === this.value || Array.isArray(this.value) && this.value.indexOf(value) !== -1;
            let isCurrent = value === this.current;
            let setColor = isSelected ? this.setBackgroundColor : this.setTextColor;
            let color = (isSelected || isCurrent) && (this.color || 'accent');
            let btn = this.$createElement('button', setColor(color, {
                staticClass: 'v-btn',
                'class': this.genButtonClasses(isAllowed, isFloating, isSelected, isCurrent),
                attrs: {
                    type: 'button'
                },
                domProps: {
                    disabled: this.disabled || !isAllowed
                },
                on: this.genButtonEvents(value, isAllowed, mouseEventType)
            }), this.createButtonContent(formatter, value));

            return this.dateTimeDict[value] ? this.$createElement(VTooltip, {
                    props: {
                        openDelay: 100,
                    },
                    scopedSlots: {
                        activator: props => {
                            _.assign(btn.data.on, props.on)
                            return btn
                        }
                    },
                },
                [this.$createElement('span', `${utils.time24HtoAMPM(this.dateTimeDict[value].start)} - ${utils.time24HtoAMPM(this.dateTimeDict[value].end)}`)]
            ) : btn
        },

        createButtonContent(formatter, value) {
            //console.log(value, this.dateTimeDict[value])
            let res = [
                this.$createElement('div', {
                    staticClass: `v-btn__content${this.dateTimeDict[value] ? ' timed-date-label' : ''}`
                }, [formatter(value)]),
                this.genEvents(value),
            ]
            if(this.dateTimeDict[value]) {
                res.unshift(this.getPieFromTimePeriod(this.dateTimeDict[value].start, this.dateTimeDict[value].end))
            }
            return res
        },

        getPieFromTimePeriod(start, end) {
            let startPerc = this.timeToPerc(start)
            let endPerc = this.timeToPerc(end)
            let pie = this.timeToHours(end)-this.timeToHours(start) > 12 ? 'radial-gradient(orange 40%, transparent 41%), ' : 'radial-gradient(white 40%, transparent 41%), '
            let sectors = []
            if(startPerc > endPerc) {
                sectors.push(`orange 0% ${endPerc}%`)
                sectors.push(`white ${endPerc}% ${startPerc}%`)
                sectors.push(`orange ${startPerc}% 100%`)
            } else {
                sectors.push(`white 0% ${startPerc}%`)
                sectors.push(`orange ${startPerc}% ${endPerc}%`)
                sectors.push(`white ${endPerc}% 100%`)
            }
            let conic = `conic-gradient(${sectors.join(',')})`
            return this.$createElement('div', {
                staticClass: 'timed-date',
                style: {
                    color: 'red',
                    background: `${pie} ${conic}`
                }
            })
        },

        timeToHours(time) {
            return Number(time.split(':')[0])+time.split(':')[1]/60
        },

        timeToDeg(time) {
            return (this.timeToHours(time) % 12) / 12 * 360
        },

        timeToPerc(time) {
            return (this.timeToHours(time) % 12) / 12 * 100
        },
    }
}

export default {
    props: {
        dateTimeDict: Object,
    },
    extends: VDatePicker,
    methods: {
        genDateTable: function genDateTable() {
            var _this5 = this;

            return this.$createElement(VDatePickerDateTableMod, {
                props: {
                    allowedDates: this.allowedDates,
                    color: this.color,
                    current: this.current,
                    dark: this.dark,
                    disabled: this.disabled,
                    events: this.events,
                    eventColor: this.eventColor,
                    firstDayOfWeek: this.firstDayOfWeek,
                    format: this.dayFormat,
                    light: this.light,
                    locale: this.locale,
                    min: this.min,
                    max: this.max,
                    readonly: this.readonly,
                    scrollable: this.scrollable,
                    showWeek: this.showWeek,
                    tableDate: pad(this.tableYear, 4) + '-' + pad(this.tableMonth + 1),
                    value: this.value,
                    weekdayFormat: this.weekdayFormat,
                    dateTimeDict: this.dateTimeDict || {},

                },
                ref: 'table',
                on: {
                    input: this.dateClick,
                    tableDate: function tableDate(value) {
                        return _this5.tableDate = value;
                    },
                    'click:date': function clickDate(value) {
                        return _this5.$emit('click:date', value);
                    },
                    'dblclick:date': function dblclickDate(value) {
                        return _this5.$emit('dblclick:date', value);
                    }
                }
            });
        },
    }
}
</script>

<style lang="scss">
.v-picker--date {
    div.timed-date {
        width: 100%;
        height: 100%;
        display: block;
        border-radius: 50%;
        border: 1px solid orange;
        position: absolute;
        top: 0;
        left: 0;
    }
    .v-btn--active {
        div.timed-date {
            opacity: 0.2;
        }
    }
}

</style>