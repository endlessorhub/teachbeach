<template>
<div :class="{'cropper-container': true, 'is-url-under': isUrlUnder}" :style="containerStyle">
    <v-text-field class="url-field" :label="label" @click='pickFile' v-model='imageName' prepend-icon='attach_file' :disabled="readonly">
        <template v-slot:append-outer>
            <v-btn v-if="confirmable && imageUrl" color="success" @click="onConfirmFile" :disabled="!isEditing">Save
                <v-icon right dark>cloud_upload</v-icon>
            </v-btn>
        </template>
    </v-text-field>

    <div class="image-container" style="position: relative;">
        <Cropper
            v-if="imageUrl"
            :src="imageUrl"
            ref="cropper"
            @change="onChange"
            :stencilComponent="$options.components.RectangleStencil"
            :stencilProps="stencilProps"
            :defaultPosition="defaultPosition"
            :defaultSize="defaultSize"
        />
        <v-btn v-if="imageUrl && !readonly" class="remove-photo-btn" flat icon @click="onDeleteFile"><v-icon>cancel</v-icon></v-btn>
    </div>
    <v-alert
      :value="isSuccess"
      type="success"
      transition="scale-transition"
    >
      Image was processed successfully
    </v-alert>



    <input
        type="file"
        style="display: none"
        ref="image"
        accept="image/*"
        @change="onFilePicked"
    >
</div>
</template>

<script>
import _ from 'lodash'
import { Cropper, RectangleStencil } from 'vue-advanced-cropper'
import axios from 'axios'

export default {
    components: {
        Cropper,
        RectangleStencil
    },
    props: {
        'readonly': {
            default: false,
            type: Boolean,
        },
        'imageName': {
            default: '',
            type: String,
        },
        'imageUrl': {
            default: '',
            type: String,
        },
        'imageFile': {
            default: null,
            type: Object,
        },
        aspectRatio: {
            default: 1,
            type: Number
        },
        width: {
            default: null,
            type: Number,
        },
        height: {
            default: null,
            type: Number,
        },
        label: {
            default: 'Select Image',
            type: String,
        },
        confirmable: {
            default: false,
            type: Boolean,
        },
        ignoreMountedEventChange: {
            default: true,
            type: Boolean,
        },
        isUrlUnder: {
            default: false,
            type: Boolean,
        },
    },

    data: () => ({
        isFileChanged: false,
        isEditing: false,
        isLoading: false,
        isSuccess: false,
        imageWidth: '200px',
        imageHeight: '200px',
        target: {},
        crop: {},
        skipChange: false,
        lastCoordinates: null,
        lastFile: null,
    }),

    created: function () {
        if (this.width && !this.height) {
            this.imageWidth = this.width
            this.imageHeight = null
        } else if (!this.width && this.height) {
            this.imageWidth = null
            this.imageHeight = this.height
        } else if(this.width && this.height) {
            this.imageWidth = this.width
            this.imageHeight = this.height
        } else {
            this.imageHeight = null
        }
        if (this.ignoreMountedEventChange) {
            // not firing on mount?
            //this.skipChange = true
        }
    },

    beforeMount() {

    },

    computed: {
        containerStyle() {
            let res = {
                position: 'relative',
            }
            if(this.imageWidth) {
                res.width = this.imageWidth
            }
            if(this.imageHeight) {
                res.height = this.imageHeight
            }
            return res
        },
        stencilProps() {
            return {
                aspectRatio: this.aspectRatio,
            }
        }
    },

    methods: {
        defaultSize({visibleArea, imageSize, stencilRatio, sizeRestrictions}) {
            //console.log(visibleArea, imageSize, stencilRatio, sizeRestrictions)
            //console.log(arguments)
            return {
                width: Math.floor(sizeRestrictions.maxWidth)-1,
                height: Math.floor(sizeRestrictions.maxHeight)-1,
            }
        },
        defaultPosition() {
            return {
                top: 1,
                left: 1,
            }
        },
        confirmFile() {
            console.log('confirmed', this.crop.coordinates.width, this.crop.coordinates.height)
            this.isEditing = false
            this.$emit('change', {
                imageName: this.imageName,
                imageUrl: this.imageUrl,
                imageFile: this.imageFile,
                target: this.target,
                crop: this.crop,
            })
            //this.isSuccess = true
            //setTimeout(() => {this.isSuccess = false}, 3000)
        },
        onConfirmFile() {
            this.confirmFile()
        },
        onChange(event) {
            if(this.skipChange) {
                this.skipChange = false
                return
            }
            this.crop = event
            if(this.confirmable)
                return
            // skip change of file if it is not uploaded but changed directly
            if(this.isFileChanged) {
                this.isFileChanged = false
                this.lastCoordinates = this.crop.coordinates
                if(!this.isEditing)
                    return
            }
            // confirm change if file uploading or cropper changed
            if(this.isEditing || this.lastCoordinates && !_.isEqual(this.lastCoordinates, this.crop.coordinates))
                this.confirmFile()
            this.lastCoordinates = this.crop.coordinates
        },
        pickFile() {
            this.$refs.image.value = null
            this.$refs.image.click()
        },
        onFilePicked(e) {
            this.isEditing = true
            this.target = e.target
            const files = e.target.files
			if(files[0] !== undefined) {
				this.imageName = files[0].name
				if(this.imageName.lastIndexOf('.') <= 0) {
					return
				}
				const fr = new FileReader ()
				fr.readAsDataURL(files[0])
				fr.addEventListener('load', () => {
					this.imageUrl = fr.result
					this.imageFile = files[0] // this is an image file that can be sent to server...
                    if(/video/.test(e.target.files[0].type)) {
					    this.crop = {}
					    this.confirmFile()
                    }
				})
			} else {
				this.imageName = ''
				this.imageFile = ''
				this.imageUrl = ''
			}
        },
        onDeleteFile() {
            this.imageName = ''
            this.imageFile = ''
            this.imageUrl = ''
        },
    },
    watch: {
        imageUrl(newVal, oldVal) {
            //console.log(newVal, oldVal)
            if(newVal !== oldVal) {
                this.isFileChanged = true
            }
        }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.remove-photo-btn {
    text-align: right;
    vertical-align: top;
    margin: -30px -30px;
    position: absolute;
    top: 0;
    right: 0;
    //background-color: rgba(200,200,200,0.5);
}
.cropper-container {
    display: flex;
    flex-flow: column;
    .url-field {
        order: 1;
    }
    .image-container {
        order: 2;
    }
    &.is-url-under {
        .url-field {
            order: 2;
        }
        .image-container {
            order: 1;
        }
    }
}

</style>