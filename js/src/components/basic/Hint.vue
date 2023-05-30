<template>
    <div class="hint-container" :style="containerStyle">
        <div class="hint" :style="styles">
            <div class="hint-body">
                <slot></slot>
            </div>
            <div class="arrow"></div>
        </div>
    </div>
</template>
<script>

export default {
    name: 'hint',
    data: () => ({

    }),
    props: [
        'bgcolor',
        'width',
        'position',
    ],
    computed: {
        styles() {
            const res = {}
            if(this.width)
                res['--width'] = this.width+'px'
            if(this.bgcolor)
                res['--bgcolor'] = this.bgcolor
            return res
        },
        containerStyle() {
            const res = {}
            if(this.position === 'right')
                res['justify-items'] = 'flex-end'
            return res
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
    .hint-container {
        height: 0;
        position: relative;
        display: flex;
        align-items: flex-start;
        justify-content: flex-end;
        .hint {
            --width: auto;
            --bgcolor: white;
            width: var(--width);
            border: 1px solid gray;
            position: absolute;
            background-color: var(--bgcolor);
            border-radius: 3px;
            z-index: 1;
            transform: translateY(-100%);
            transition: background-color 0.3s ease;
            min-height: 1.2em;
            .arrow {

                &::before {
                    content: "";
                    width: 0;
                    height: 0;
                    position: absolute;
                    border-left: 10px solid transparent;
                    border-right: 10px solid transparent;
                    border-top: 10px solid gray;
                    border-bottom: 10px solid transparent;
                    right: calc(50% - 10px);
                    bottom: -21px;
                }
                &::after {
                    content: "";
                    width: 0;
                    height: 0;
                    position: absolute;
                    border-left: 10px solid transparent;
                    border-right: 10px solid transparent;
                    border-top-color: var(--bgcolor);
                    border-top-width: 10px;
                    border-top-style: solid;
                    border-bottom: 10px solid transparent;
                    right: calc(50% - 10px);
                    bottom: -20px;
                    transition: border-top-color 0.3s ease;
                }
            }
            .hint-body {
                padding: 0.1em 1em;
                overflow: hidden;

                & > * {
                    will-change: opacity, transform, max-height;
                }
            }

        }
    }
</style>