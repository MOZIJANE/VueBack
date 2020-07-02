<template>
  <div class="avatar-wrapper clearfix">
    <el-avatar :src="userImg" :size="50"></el-avatar>
    <div class="avatar-info">
      <span>Welcome,</span>
      <h2>{{name}}</h2>
    </div>
  </div>
</template>

<script>
import {mapGetters} from 'vuex'
export default {
  name: 'AvatarWrapper',
  props: {
    
  },
  data() {
    return {
      
    }
  },
  computed: {
    ...mapGetters(["name","userImg"])
  },
}
</script>

<style lang="scss" scoped>
.avatar-wrapper{
  width: 100%;
  margin-bottom: 15px;
  .el-avatar{
    float: left;
    width: 35%;
    margin: 25px 10px 10px;
  }
  .avatar-info{
    padding: 25px 10px 10px;
    float: left;
    width: 65%;
    color: #fff;
    span{
      font-size:13px;
      line-height:30px;
      color:#BAB8B8
    }
    h2{
      font-size:14px;
      color:#ECF0F1;
      margin:0;
      font-weight:300;
    }
  }
}

.clearfix::before, .clearfix::after{
  content:"";
  display: table
}
.clearfix::after{
  clear: both;
}
.clearfix{
  *zoom:1;
}

</style>
