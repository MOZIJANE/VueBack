<template>
  <d3-sankey-circular
    :nodes="data.nodes"
    :links="data.links"
    :options="options"
    @max-period-updated="(period) => yourMethod(period)"
    width="100%"
    height="400px" class="circular">
</d3-sankey-circular>
</template>
<script>
import Vs from 'd3-vs'
import Vue from "vue";
Vue.use(Vs);
import { d3SankeyCircular } from 'd3-vs'

export default {
  name: "vue-line-chart",
  props: {
    id: {
      type: String,
      default: "chart"
    }
  },
  data() {
    return {
      data: {},
      options:{
        arrowHeadSize:7,
        arrowLength:17,
        linkColor:"#003535",
        nodePadding:20
      }
    };
  },
  mounted() {
    this.getData();
  },
  methods: {
    getData(){
      this.$request({
        url: "/api/getSankeyFromUrl/",
        method: "get",
      }).then(res => {
         if(res.data){
           console.log(res)
           this.data=res.data["NetFlow"]
         }
      })
    },
    timer() {
      return setTimeout(() => {
        this.getData();
      }, 10 * 60 * 1000);
    }
  },
  watch: {
    data: {
      handler(newVal, oldVal) {
        this.timer();
      },
      deep: true //对象内部属性的监听，关键。
    }
  },
  destroyed() {
    clearTimeout(this.timer);
  }
};
</script>
<style lang="scss" scoped>
.circular{
  border: 1px solid #eee;
  background-color: #eee;
}
</style>
