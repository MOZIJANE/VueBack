<template>
  <div>
    <el-tooltip
      effect="dark"
      content="主题"
      placement="bottom">
      <el-button
        class="d2-ml-0 d2-mr btn-text can-hover"
        type="text"
        @click="dialogVisible = true">
        <i class="el-icon-magic-stick"  style="font-size: 30px;margin-right:17px;color:'#eee';"/>
      </el-button>
    </el-tooltip>
    <el-dialog
      title="主题"
      width="24rem"
      :visible.sync="dialogVisible"
      :append-to-body="true">
      <d2-theme-list style="margin-top: -25px;"/>
    </el-dialog>
  </div>
</template>

<script>
import themeList from './d2-theme-list'
export default {
  components: {
    'd2-theme-list': themeList
  },
  data () {
    return {
      dialogVisible: false
    }
  }
}
</script>
