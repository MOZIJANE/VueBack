<template>
  <div class="app-container">
    <el-card>
      <el-row>
        <el-col :md="12" :xs="24">
          <div class="avatar-Info">
            <h4>更换头像</h4>
            <el-form :model="infoForm" label-width="80px">
              <el-form-item label="用户名">
                <el-input v-model="name" disabled></el-input>
              </el-form-item>
            </el-form>
            <div class="eleme">
              <el-upload
                class="upload-demo"
                ref="upload"
                action="https://jsonplaceholder.typicode.com/posts/"
                :before-upload="beforeUpload"
                :on-preview="handlePreview"
                :on-remove="handleRemove"
                :auto-upload="true"
                :show-file-list="false"
              >
                <el-button slot="trigger" size="small" type="primary"
                  >选取图片</el-button
                >
                <el-button
                  style="margin-left: 10px;"
                  size="small"
                  type="success"
                  @click.native.prevent="submitUpload"
                  >上传头像</el-button
                >
                <!-- <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div> -->
              </el-upload>
              <div>
                <br />
                <el-button
                  type="primary"
                  icon="el-icon-refresh-right"
                  circle
                  @click="rotateRight"
                ></el-button>
                <el-button
                  type="success"
                  icon="el-icon-refresh-left"
                  circle
                  @click="rotateLeft"
                ></el-button>
                <el-button
                  type="danger"
                  icon="el-icon-plus"
                  circle
                  @click="changeScale(1)"
                ></el-button>
                <el-button
                  type="warning"
                  icon="el-icon-minus"
                  circle
                  @click="changeScale(-1)"
                ></el-button>
              </div>
              <div class="cropper">
                <div
                  class="cropper-content"
                  style="margin-top:60px;margin-left:60px;"
                >
                  <div class="cropper">
                    <vueCropper
                      ref="cropper"
                      :img="option.img"
                      :outputSize="option.size"
                      :outputType="option.outputType"
                      :info="true"
                      :full="option.full"
                      :canMove="option.canMove"
                      :canMoveBox="option.canMoveBox"
                      :original="option.original"
                      :autoCrop="option.autoCrop"
                      :autoCropWidth="option.autoCropWidth"
                      :autoCropHeight="option.autoCropHeight"
                      :fixedBox="option.fixedBox"
                      @realTime="realTime"
                      @imgLoad="imgLoad"
                    ></vueCropper>
                  </div>
                  <div style="margin-left:20px;">
                    <div
                      class="show-preview"
                      :style="{
                        width: '150px',
                        height: '155px',
                        overflow: 'hidden',
                        margin: '5px'
                      }"
                    >
                      <div :style="previews.div" class="preview">
                        <img :src="previews.url" :style="previews.img" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script>
import { mapState } from "vuex";
import { VueCropper } from "vue-cropper";

export default {
  data() {
    return {
      infoForm: {
        name: "",
        userImg: ""
      },
      headImg: "",
      //剪切图片上传
      crap: false,
      previews: {},
      option: {
        img: "",
        outputSize: 1, //剪切后的图片质量（0.1-1）
        full: false, //输出原图比例截图 props名full
        outputType: "png",
        canMove: true,
        original: false,
        canMoveBox: true,
        autoCrop: true,
        autoCropWidth: 150,
        autoCropHeight: 150,
        fixedBox: true
      },
      fileName: "", //本机文件地址
      downImg: "#",
      imgFile: "",
      uploadImgRelaPath: "" //上传后的图片的地址（不带服务器域名）
    };
  },
  computed: {
    ...mapState("user", ["name", "userImg"])
  },
  created() {},
  methods: {},
  components: {
    VueCropper
  },
  methods: {
    submitUpload(file) {
      // this.$refs.upload.submit();
      this.finish("blob");
    },
    handleRemove(file, fileList) {
      console.log(file, fileList);
    },
    handlePreview(file) {
      console.log(file);
      //   let data = window.URL.createObjectURL(new Blob([file]));
      //   this.option.img = data;
    },
    beforeUpload(file) {
      console.log("上传文件");
      console.log(file);
      let data = window.URL.createObjectURL(new Blob([file]));
      this.fileName = file.name;
      this.option.img = data;
    },
    //放大/缩小
    changeScale(num) {
      console.log("changeScale");
      num = num || 1;
      this.$refs.cropper.changeScale(num);
    },
    //坐旋转
    rotateLeft() {
      console.log("rotateLeft");
      this.$refs.cropper.rotateLeft();
    },
    //右旋转
    rotateRight() {
      console.log("rotateRight");
      this.$refs.cropper.rotateRight();
    },
    //上传图片（点击上传按钮）
    finish(type) {
      console.log("finish");
      let _this = this;
      let formData = new FormData();
      // 输出
      if (type === "blob") {
        this.$refs.cropper.getCropBlob(async data => {
          let img = window.URL.createObjectURL(data);
          this.model = true;
          this.modelSrc = img;
          formData.append("profile", data, this.fileName);
          formData.append("user", this.name);
          await this.$request({
            url: "/cmdb/profile/",
            data: formData,
            method: "post",
            headers: {
              "Content-type": "multipart/form-data"
            }
          })
            .then(res => {
              this.$store.dispatch("user/setUserImg",res.data[0]['profile_path'])
              console.log(res.data[0]['profile_path']);
              this.$message.success("上传头像成功！！");
            })
            .catch(err => {
              this.$message.error("失败，请上传正确的文件！！");
            });
        });
      } else {
        this.$refs.cropper.getCropData(data => {
          this.model = true;
          this.modelSrc = data;
        });
      }
    },
    // 实时预览函数
    realTime(data) {
      console.log("realTime");
      this.previews = data;
    },
    imgLoad(msg) {
      console.log("imgLoad");
      console.log(msg);
    }
  }
};
</script>

<style lang="scss" scoped>
.avatar-Info {
  h4 {
    font-weight: 400;
  }
}
.eleme {
  border: 1px solid #ecf0f1;
  text-align: center;
  padding: 10px;
}
.cropper-content {
  min-width: 540px;
  display: flex;
  //   display: -webkit-flex;
  //   justify-content: flex-end;
  //   -webkit-justify-content: flex-end;
  .cropper {
    width: 260px;
    height: 260px;
  }
  .show-preview {
    flex: 1;
    -webkit-flex: 1;
    display: flex;
    display: -webkit-flex;
    justify-content: center;
    -webkit-justify-content: center;
    .preview {
      overflow: hidden;
      border-radius: 50%;
      border: 1px solid #cccccc;
      background: #cccccc;
      margin-left: 40px;
    }
  }
}
.cropper-content .show-preview .preview {
  margin-left: 0;
  -moz-user-select: none;
  -webkit-user-select: none;
  -ms-user-select: none;
  -khtml-user-select: none;
  user-select: none;
}
</style>
